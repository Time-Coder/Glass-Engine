from .CommonRenderer import CommonRenderer

from ..Frame import Frame

from glass import \
    ShaderProgram, GLConfig, sampler2D, FBO, RBO, sampler2DMS
from glass.utils import profiler

from OpenGL import GL
import glm
        
class ForwardRenderer(CommonRenderer):

    def __init__(self):
        CommonRenderer.__init__(self)

    def draw_opaque(self):
        self._transparent_meshes.clear()
        with GLConfig.LocalConfig(depth_test=True, blend=False):
            with self.OIT_fbo:
                GLConfig.clear_buffers()

                # 绘制实体
                self.forward_program["camera"] = self.camera
                self.forward_program["is_opaque_pass"] = True
                self.forward_program["SSAO_map"] = self._SSAO_map
                self.forward_program["use_skybox_map"] = self.scene.skybox.is_completed
                self.forward_program["skybox_map"] = self.scene.skybox.skybox_map
                self.forward_program["use_skydome_map"] = self.scene.skydome.is_completed
                self.forward_program["skydome_map"] = self.scene.skydome.skydome_map
                for mesh, instances in self.scene.all_meshes.items():
                    if mesh.has_opaque:
                        self.forward_draw_mesh(mesh, instances)

                    if mesh.has_transparent:
                        self._transparent_meshes[mesh] = instances

                # 绘制天空盒
                if self.scene.skybox.is_completed:
                    self.scene.skybox.draw(self.camera)

                # 绘制天空穹顶
                elif self.scene.skydome.is_completed:
                    self.scene.skydome.draw(self.camera)

        self.OIT_fbo.draw_to_active(0)

    @property
    def ssao_gbuffer_program(self):
        if "ssao_gbuffer" in self.programs:
            return self.programs["ssao_gbuffer"]
        
        program = ShaderProgram()
        program.compile("../glsl/Pipelines/forward_rendering/forward_rendering.vs")
        program.compile("../glsl/Pipelines/forward_rendering/forward_rendering.gs")
        program.compile("../glsl/Pipelines/SSAO/ssao_gbuffer.fs")
        self.programs["ssao_gbuffer"] = program
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
        with GLConfig.LocalConfig(clear_color=glm.vec4(0,0,0,0), polygon_mode=GL.GL_FILL):
            GLConfig.clear_buffers()
            if self._enable_SSAO or self.DOF:
                with self.ssao_gbuffer:
                    self.ssao_gbuffer_program["camera"] = self.camera
                    for mesh, instances in self.scene.all_meshes.items():
                        if not mesh.is_filled:
                            continue

                        self.ssao_gbuffer_program["material"] = mesh.material
                        self.ssao_gbuffer_program["back_material"] = mesh._back_material
                        self.ssao_gbuffer_program["explode_distance"] = mesh.explode_distance
                        mesh.draw(self.ssao_gbuffer_program, instances)

                view_pos_alpha_map = self.ssao_gbuffer.resolved.color_attachment(0)
                view_normal_map = self.ssao_gbuffer.resolved.color_attachment(1)
                if self.DOF:
                    self.filters["DOF"].view_pos_map = view_pos_alpha_map
            
            if self._enable_SSAO:
                with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
                    with self.ssao_fbo:
                        self.ssao_generate_program["camera"] = self.camera
                        self.ssao_generate_program["view_pos_alpha_map"] = view_pos_alpha_map
                        self.ssao_generate_program["view_normal_map"] = view_normal_map
                        self.ssao_generate_program["SSAO_radius"] = self.SSAO_radius
                        self.ssao_generate_program["SSAO_samples"] = self.SSAO_samples
                        self.ssao_generate_program["SSAO_power"] = self.SSAO_power
                        self.ssao_generate_program.draw_triangles(Frame.vertices, Frame.indices)

                self._SSAO_map = self._SSAO_blur_filter(self.ssao_fbo.color_attachment(0))
                
    def render(self, camera, scene):
        # profiler.enable()
        self._should_update = False
        self.generate_SSAO()
        self.draw_opaque()
        self.draw_transparent()
        # profiler.disable()
        return self._should_update
