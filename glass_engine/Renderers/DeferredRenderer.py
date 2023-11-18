from .CommonRenderer import CommonRenderer
from ..Frame import Frame
from ..GlassEngineConfig import GlassEngineConfig

from glass import \
    ShaderProgram, GLConfig, FBO, sampler2DMS, sampler2D, usampler2D, usampler2DMS

from OpenGL import GL
import glm
import os
        
class DeferredRenderer(CommonRenderer):

    def __init__(self):
        CommonRenderer.__init__(self)
        
    def startup(self):
        CommonRenderer.startup(self)
        screen = self.camera.screen
        if not screen._samples_set_by_user and not screen._is_gl_init:
            screen._set_samples(1)
        screen.FXAA = True

    @property
    def deferred_render_program(self):
        if "deferred_render" in self.programs:
            return self.programs["deferred_render"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        GlassEngineConfig.define_for_program(program)
        program.compile(Frame.draw_frame_vs)
        program.compile(self_folder + "/../glsl/Pipelines/deferred_rendering/deferred_rendering.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)
        
        self.programs["deferred_render"] = program

        return program

    @property
    def draw_to_gbuffer_program(self):
        if "draw_to_gbuffer" in self.programs:
            return self.programs["draw_to_gbuffer"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        GlassEngineConfig.define_for_program(program)
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_rendering.vs")
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_rendering.gs")
        program.compile(self_folder + "/../glsl/Pipelines/deferred_rendering/draw_to_gbuffer.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)
        self.programs["draw_to_gbuffer"] = program

        return program
    
    @property
    def draw_lines_to_gbuffer_program(self):
        if "draw_lines_to_gbuffer" in self.programs:
            return self.programs["draw_lines_to_gbuffer"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        GlassEngineConfig.define_for_program(program)
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_draw_lines.vs")
        program.compile(self_folder + "/../glsl/Pipelines/deferred_rendering/draw_points_to_gbuffer.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)
        self.programs["draw_lines_to_gbuffer"] = program

        return program

    @property
    def draw_points_to_gbuffer_program(self):
        if "draw_points_to_gbuffer" in self.programs:
            return self.programs["draw_points_to_gbuffer"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        GlassEngineConfig.define_for_program(program)
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_draw_points.vs")
        program.compile(self_folder + "/../glsl/Pipelines/deferred_rendering/draw_points_to_gbuffer.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)
        self.programs["draw_points_to_gbuffer"] = program

        return program
    
    @property
    def screen_fbo(self):
        fbo = None
        screen_size = GLConfig.screen_size
        if "screen" in self.fbos:
            fbo = self.fbos["screen"]
            fbo.resize(screen_size.x, screen_size.y)
        else:
            fbo = FBO(screen_size.x, screen_size.y)
            fbo.attach(0, sampler2D)
            self.fbos["screen"] = fbo

        return fbo

    @property
    def gbuffer(self):
        fbo = None
        screen_size = GLConfig.screen_size
        samples = self.camera.screen.samples
        if samples > 1:
            if "gbuffer_ms" in self.fbos:
                fbo = self.fbos["gbuffer_ms"]
                fbo.resize(screen_size.x, screen_size.y, samples)
            else:
                fbo = FBO(screen_size.x, screen_size.y, samples)
                fbo.attach(0, sampler2DMS, GL.GL_RGBA32F) # view_pos_and_alpha
                fbo.attach(1, sampler2DMS, GL.GL_RGBA32F) # view_normal_and_emission_r
                fbo.attach(2, sampler2DMS, GL.GL_RGBA32F) # ambient_and_emission_g
                fbo.attach(3, sampler2DMS, GL.GL_RGBA32F) # diffuse_or_base_color_and_emission_b
                fbo.attach(4, sampler2DMS, GL.GL_RGBA32F) # specular_or_preshading_and_shininess
                fbo.attach(5, sampler2DMS, GL.GL_RGBA32F) # reflection
                fbo.attach(6, sampler2DMS, GL.GL_RGBA32F) # env_center_and_mixed_value
                fbo.attach(7, usampler2DMS, GL.GL_RGBA32UI) # mixed_uint
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, sampler2DMS)
                fbo.auto_clear = False
                self.fbos["gbuffer_ms"] = fbo
            return fbo
        else:
            if "gbuffer" in self.fbos:
                fbo = self.fbos["gbuffer"]
                fbo.resize(screen_size.x, screen_size.y)
            else:
                fbo = FBO(screen_size.x, screen_size.y)
                fbo.attach(0, sampler2D, GL.GL_RGBA32F) # view_pos_and_alpha
                fbo.attach(1, sampler2D, GL.GL_RGBA32F) # view_normal_and_emission_r
                fbo.attach(2, sampler2D, GL.GL_RGBA32F) # ambient_and_emission_g
                fbo.attach(3, sampler2D, GL.GL_RGBA32F) # diffuse_or_base_color_and_emission_b
                fbo.attach(4, sampler2D, GL.GL_RGBA32F) # specular_or_preshading_and_shininess
                fbo.attach(5, sampler2D, GL.GL_RGBA32F) # reflection
                fbo.attach(6, sampler2D, GL.GL_RGBA32F) # env_center_and_mixed_value
                fbo.attach(7, usampler2D, GL.GL_RGBA32UI) # mixed_uint
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, sampler2D)
                fbo.auto_clear = False
                self.fbos["gbuffer"] = fbo
            return fbo

    def prepare_draw_to_gbuffer(self):
        self.draw_to_gbuffer_program["camera"] = self.camera

    def draw_to_gbuffer(self, mesh, instances):
        if mesh.material.need_env_map or mesh._back_material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.draw_to_gbuffer_program["material"] = mesh.material
        self.draw_to_gbuffer_program["back_material"] = mesh._back_material
        self.draw_to_gbuffer_program["explode_distance"] = mesh.explode_distance
        self.draw_to_gbuffer_program["is_sphere"] = mesh.is_sphere
        self.draw_to_gbuffer_program["mesh_center"] = mesh.center
        mesh.draw(self.draw_to_gbuffer_program, instances)

    def prepare_draw_lines_to_gbuffer(self):
        self.draw_lines_to_gbuffer_program["camera"] = self.camera

    def draw_lines_to_gbuffer(self, mesh, instances):
        if mesh.material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.draw_lines_to_gbuffer_program["material"] = mesh.material
        self.draw_lines_to_gbuffer_program["mesh_center"] = mesh.center
        mesh.draw(self.draw_lines_to_gbuffer_program, instances)

    def prepare_draw_points_to_gbuffer(self):
        self.draw_points_to_gbuffer_program["camera"] = self.camera

    def draw_points_to_gbuffer(self, mesh, instances):
        if mesh.material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.draw_points_to_gbuffer_program["material"] = mesh.material
        self.draw_points_to_gbuffer_program["mesh_center"] = mesh.center
        mesh.draw(self.draw_points_to_gbuffer_program, instances)

    def draw_opaque(self):
        if not self._opaque_meshes and \
           not self._opaque_lines and \
           not self._opaque_points:
            return
        
        with GLConfig.LocalConfig(clear_color=glm.vec4(0)):
            with self.gbuffer:
                GLConfig.clear_buffers()

                if self._opaque_meshes:
                    self.prepare_draw_to_gbuffer()
                    for mesh, instances in self._opaque_meshes:
                        self.draw_to_gbuffer(mesh, instances)

                if self._opaque_lines:
                    self.prepare_draw_lines_to_gbuffer()
                    for mesh, instances in self._opaque_lines:
                        self.draw_lines_to_gbuffer(mesh, instances)

                if self._opaque_points:
                    self.prepare_draw_points_to_gbuffer()
                    for mesh, instances in self._opaque_points:
                        self.draw_points_to_gbuffer(mesh, instances)

        resolved = self.gbuffer.resolved
        view_pos_and_alpha_map = resolved.color_attachment(3)
        view_normal_and_emission_r_map = resolved.color_attachment(4)
        ambient_and_emission_g_map = resolved.color_attachment(2)
        diffuse_or_base_color_and_emission_b_map = resolved.color_attachment(0)
        specular_or_preshading_and_shininess_map = resolved.color_attachment(1)
        reflection_map = resolved.color_attachment(5)
        env_center_and_mixed_value_map = resolved.color_attachment(6)
        mixed_uint_map = resolved.color_attachment(7)

        self._view_pos_map = view_pos_and_alpha_map
        self._view_normal_map = view_normal_and_emission_r_map
        self._depth_map = resolved.depth_attachment

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            GLConfig.clear_buffers()
            self.deferred_render_program["camera"] = self.camera
            self.deferred_render_program["view_pos_and_alpha_map"] = view_pos_and_alpha_map
            self.deferred_render_program["view_normal_and_emission_r_map"] = view_normal_and_emission_r_map
            self.deferred_render_program["ambient_and_emission_g_map"] = ambient_and_emission_g_map
            self.deferred_render_program["diffuse_or_base_color_and_emission_b_map"] = diffuse_or_base_color_and_emission_b_map
            self.deferred_render_program["specular_or_preshading_and_shininess_map"] = specular_or_preshading_and_shininess_map
            self.deferred_render_program["reflection_map"] = reflection_map
            self.deferred_render_program["env_center_and_mixed_value_map"] = env_center_and_mixed_value_map
            self.deferred_render_program["mixed_uint_map"] = mixed_uint_map
            self.deferred_render_program["background"] = self.scene.background
            if GlassEngineConfig["USE_FOG"]:
                self.deferred_render_program["fog"] = self.scene.fog
            self.deferred_render_program.draw_triangles(Frame.vertices, Frame.indices)

        self.gbuffer.draw_to_active(GL.GL_DEPTH_ATTACHMENT)

        # draw skybox
        if self.scene.skybox.is_completed:
            self.scene.skybox.draw(self.camera)

        # draw skydome
        elif self.scene.skydome.is_completed:
            self.scene.skydome.draw(self.camera)
        
        if self._transparent_meshes or self._transparent_lines or self._transparent_points:
            self.gbuffer.draw_to(self.OIT_fbo, GL.GL_DEPTH_ATTACHMENT)

    def render(self):
        self._should_update = False
        sampler2D._should_update = False
        self.classify_meshes()
        self.update_dir_lights_depth()
        self.update_point_lights_depth()
        self.update_spot_lights_depth()
        self.draw_opaque()
        self.draw_transparent()
        return (self._should_update or sampler2D._should_update)