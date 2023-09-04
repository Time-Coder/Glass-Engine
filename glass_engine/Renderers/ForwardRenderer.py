from .CommonRenderer import CommonRenderer

from ..Frame import Frame

from glass import ShaderProgram, GLConfig, sampler2D, FBO, RBO, sampler2DMS
# from glass.utils import profiler

from OpenGL import GL
import glm
import os
        
class ForwardRenderer(CommonRenderer):

    def __init__(self):
        CommonRenderer.__init__(self)

    def startup(self):
        CommonRenderer.startup(self)
        screen = self.camera.screen
        if not screen._samples_set_by_user and not screen._is_gl_init:
            screen.samples = 4

    def draw_opaque(self):
        if not self._opaque_meshes and \
           not self._opaque_lines and \
           not self._opaque_points:
            return

        with GLConfig.LocalConfig(depth_test=True, blend=False):
            with self.OIT_fbo:
                GLConfig.clear_buffers()

                if self._opaque_meshes:
                    self.prepare_forward_draw_mesh(True)
                    for mesh, instances in self._opaque_meshes:
                        self.forward_draw_mesh(mesh, instances)

                if self._opaque_lines:
                    self.prepare_forward_draw_lines(True)
                    for mesh, instances in self._opaque_lines:
                        self.forward_draw_lines(mesh, instances)

                if self._opaque_points:
                    self.prepare_forward_draw_points(True)
                    for mesh, instances in self._opaque_points:
                        self.forward_draw_points(mesh, instances)

                # 绘制天空盒
                if self.scene.skybox.is_completed:
                    self.scene.skybox.draw(self.camera)

                # 绘制天空穹顶
                elif self.scene.skydome.is_completed:
                    self.scene.skydome.draw(self.camera)

        self.OIT_fbo.draw_to_active(0)

    @property
    def draw_to_ssao_gbuffer_program(self):
        if "draw_to_ssao_gbuffer" in self.programs:
            return self.programs["draw_to_ssao_gbuffer"]
        
        program = ShaderProgram()
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/forward_rendering/forward_rendering.vs")
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/forward_rendering/forward_rendering.gs")
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/SSAO/draw_to_ssao_gbuffer.fs")
        self.programs["draw_to_ssao_gbuffer"] = program
        return program
    
    @property
    def ssao_gbuffer(self):
        samples = self.camera.screen.samples
        if samples > 1:
            screen_size = GLConfig.screen_size
            if "ssao_gbuffer_ms" in self.fbos:
                self.fbos["ssao_gbuffer_ms"].resize(screen_size.x, screen_size.y, samples)
            else:
                fbo = FBO(screen_size.x, screen_size.y, samples)
                fbo.attach(0, sampler2DMS)
                fbo.attach(1, sampler2DMS)
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
                self.fbos["ssao_gbuffer_ms"] = fbo

            return self.fbos["ssao_gbuffer_ms"]
        else:
            screen_size = GLConfig.screen_size
            if "ssao_gbuffer" in self.fbos:
                self.fbos["ssao_gbuffer"].resize(screen_size.x, screen_size.y)
            else:
                fbo = FBO(screen_size.x, screen_size.y)
                fbo.attach(0, sampler2D)
                fbo.attach(1, sampler2D)
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
                self.fbos["ssao_gbuffer"] = fbo

            return self.fbos["ssao_gbuffer"]

    def generate_SSAO(self):
        self._SSAO_map = None
        view_pos_alpha_map = None
        view_normal_map = None
        with GLConfig.LocalConfig(clear_color=glm.vec4(0), polygon_mode=GL.GL_FILL):
            GLConfig.clear_buffers()
            if self._enable_SSAO or self.DOF:
                with self.ssao_gbuffer:
                    self.draw_to_ssao_gbuffer_program["camera"] = self.camera
                    for mesh, instances in self.scene.all_meshes.items():
                        if not mesh.is_filled:
                            continue

                        self.draw_to_ssao_gbuffer_program["material"] = mesh.material
                        self.draw_to_ssao_gbuffer_program["back_material"] = mesh._back_material
                        self.draw_to_ssao_gbuffer_program["explode_distance"] = mesh.explode_distance
                        mesh.draw(self.draw_to_ssao_gbuffer_program, instances)

                view_pos_alpha_map = self.ssao_gbuffer.resolved.color_attachment(0)
                view_normal_map = self.ssao_gbuffer.resolved.color_attachment(1)
                if self.DOF:
                    self.filters["DOF"].view_pos_map = view_pos_alpha_map
            
            if self._enable_SSAO:
                with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
                    with self.ssao_fbo:
                        self.generate_ssao_program["camera"] = self.camera
                        self.generate_ssao_program["view_pos_alpha_map"] = view_pos_alpha_map
                        self.generate_ssao_program["view_normal_map"] = view_normal_map
                        self.generate_ssao_program["SSAO_radius"] = self.SSAO_radius
                        self.generate_ssao_program["SSAO_samples"] = self.SSAO_samples
                        self.generate_ssao_program["SSAO_power"] = self.SSAO_power
                        self.generate_ssao_program.draw_triangles(Frame.vertices, Frame.indices)

                self._SSAO_map = self._SSAO_filter(self.ssao_fbo.color_attachment(0))
    
    def render(self):
        # profiler.enable()
        self._should_update = False
        sampler2D._should_update = False
        self.classify_meshes()
        self.update_dir_lights_depth()
        self.update_point_lights_depth()
        self.update_spot_lights_depth()
        self.generate_SSAO()
        self.draw_opaque()
        self.draw_transparent()
        # profiler.disable()
        return (self._should_update or sampler2D._should_update)
