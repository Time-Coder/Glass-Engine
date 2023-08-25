from .CommonRenderer import CommonRenderer
from ..Frame import Frame

from glass import \
    ShaderProgram, GLConfig, FBO, RBO, sampler2DMS, sampler2D, usampler2D, usampler2DMS

from OpenGL import GL
import glm
import os
        
class DeferredRenderer(CommonRenderer):

    def __init__(self):
        CommonRenderer.__init__(self)
        self.filters["FXAA"].enabled = True

    @property
    def deferred_render_program(self):
        if "deferred_render" in self.programs:
            return self.programs["deferred_render"]
        
        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/deferred_rendering/deferred_rendering.fs")
        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)
        
        self.programs["deferred_render"] = program

        return program

    @property
    def draw_to_gbuffer_program(self):
        if "draw_to_gbuffer" in self.programs:
            return self.programs["draw_to_gbuffer"]
        
        program = ShaderProgram()
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/forward_rendering/forward_rendering.vs")
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/forward_rendering/forward_rendering.gs")
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/deferred_rendering/draw_to_gbuffer.fs")
        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)
        self.programs["draw_to_gbuffer"] = program

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
                fbo.attach(2, sampler2DMS, GL.GL_RGBA32F) # ambient_or_arm_and_emission_g
                fbo.attach(3, sampler2DMS, GL.GL_RGBA32F) # diffuse_or_base_color_and_emission_b
                fbo.attach(4, sampler2DMS, GL.GL_RGBA32F) # specular_or_prelight_and_shininess
                fbo.attach(5, sampler2DMS, GL.GL_RGBA32F) # reflection
                fbo.attach(6, sampler2DMS, GL.GL_RGBA32F) # env_center_and_refractive_index
                fbo.attach(7, usampler2DMS, GL.GL_RGB32UI) # mix_uint
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
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
                fbo.attach(2, sampler2D, GL.GL_RGBA32F) # ambient_or_arm_and_emission_g
                fbo.attach(3, sampler2D, GL.GL_RGBA32F) # diffuse_or_base_color_and_emission_b
                fbo.attach(4, sampler2D, GL.GL_RGBA32F) # specular_or_prelight_and_shininess
                fbo.attach(5, sampler2D, GL.GL_RGBA32F) # reflection
                fbo.attach(6, sampler2D, GL.GL_RGBA32F) # env_center_and_refractive_index
                fbo.attach(7, usampler2D, GL.GL_RGB32UI) # mix_uint
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
                fbo.auto_clear = False
                self.fbos["gbuffer"] = fbo
            return fbo

    def draw_to_gbuffer(self, mesh, instances):
        if mesh.material.need_env_map or mesh._back_material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.draw_to_gbuffer_program["material"] = mesh.material
        self.draw_to_gbuffer_program["back_material"] = mesh._back_material
        self.draw_to_gbuffer_program["explode_distance"] = mesh.explode_distance
        self.draw_to_gbuffer_program["explode_distance"] = mesh.explode_distance
        self.draw_to_gbuffer_program["is_filled"] = mesh.is_filled
        self.draw_to_gbuffer_program["is_sphere"] = mesh.is_sphere
        self.draw_to_gbuffer_program["mesh_center"] = mesh.center
        mesh.draw(self.draw_to_gbuffer_program, instances)

    def draw_opaque(self):
        self._transparent_meshes.clear()
        none_filled_meshes = {}
        with GLConfig.LocalConfig(clear_color=glm.vec4(0,0,0,0)):
            with self.gbuffer:
                GLConfig.clear_buffers()
                self.draw_to_gbuffer_program["camera"] = self.camera
                self.draw_to_gbuffer_program["use_skydome_map"] = self.scene.skydome.is_completed
                self.draw_to_gbuffer_program["skydome_map"] = self.scene.skydome.skydome_map
                for mesh, instances in self.scene.all_meshes.items():
                    if mesh.is_filled:
                        if mesh.has_opaque:
                            self.draw_to_gbuffer(mesh, instances)
                    else:
                        none_filled_meshes[mesh] = instances

                    if mesh.has_transparent:
                        self._transparent_meshes[mesh] = instances

        resolved = self.gbuffer.resolved

        view_pos_and_alpha_map = resolved.color_attachment(0)
        view_normal_and_emission_r_map = resolved.color_attachment(1)
        ambient_or_arm_and_emission_g_map = resolved.color_attachment(2)
        diffuse_or_base_color_and_emission_b_map = resolved.color_attachment(3)
        specular_or_prelight_and_shininess_map = resolved.color_attachment(4)
        reflection_map = resolved.color_attachment(5)
        env_center_and_refractive_index_map = resolved.color_attachment(6)
        mix_uint_map = resolved.color_attachment(7)

        if self.DOF:
            self.filters["DOF"].view_pos_map = view_pos_and_alpha_map

        self.generate_SSAO(view_pos_and_alpha_map, view_normal_and_emission_r_map)

        with GLConfig.LocalConfig(cull_face=None, polygon_mode=GL.GL_FILL):
            GLConfig.clear_buffers()
            self.deferred_render_program["camera"] = self.camera
            self.deferred_render_program["view_pos_and_alpha_map"] = view_pos_and_alpha_map
            self.deferred_render_program["view_normal_and_emission_r_map"] = view_normal_and_emission_r_map
            self.deferred_render_program["ambient_or_arm_and_emission_g_map"] = ambient_or_arm_and_emission_g_map
            self.deferred_render_program["diffuse_or_base_color_and_emission_b_map"] = diffuse_or_base_color_and_emission_b_map
            self.deferred_render_program["specular_or_prelight_and_shininess_map"] = specular_or_prelight_and_shininess_map
            self.deferred_render_program["reflection_map"] = reflection_map
            self.deferred_render_program["env_center_and_refractive_index_map"] = env_center_and_refractive_index_map
            self.deferred_render_program["mix_uint_map"] = mix_uint_map
            self.deferred_render_program["SSAO_map"] = self._SSAO_map
            self.deferred_render_program["skydome_map"] = self.scene.skydome.skydome_map
            self.deferred_render_program["skybox_map"] = self.scene.skybox.skybox_map
            self.deferred_render_program["fog"] = self.scene.fog
            self.deferred_render_program["use_skybox_map"] = self.scene.skybox.is_completed
            self.deferred_render_program["use_skydome_map"] = self.scene.skydome.is_completed
            self.deferred_render_program.draw_triangles(Frame.vertices, Frame.indices)

        self.gbuffer.draw_to_active(GL.GL_DEPTH_ATTACHMENT)
        
        # points and lines
        if none_filled_meshes:
            self.forward_program["is_opaque_pass"] = True
            self.forward_program["camera"] = self.camera
            self.forward_program["SSAO_map"] = self._SSAO_map
            self.forward_program["use_skybox_map"] = self.scene.skybox.is_completed
            self.forward_program["skybox_map"] = self.scene.skybox.skybox_map
            self.forward_program["use_skydome_map"] = self.scene.skydome.is_completed
            self.forward_program["skydome_map"] = self.scene.skydome.skydome_map
            self.forward_program["fog"] = self.scene.fog
            for mesh, instances in none_filled_meshes.items():
                if mesh.has_opaque:
                    self.forward_draw_mesh(mesh, instances)

        # draw skybox
        if self.scene.skybox.is_completed:
            self.scene.skybox.draw(self.camera)

        # draw skydome
        elif self.scene.skydome.is_completed:
            self.scene.skydome.draw(self.camera)
        
        if self._transparent_meshes:
            if none_filled_meshes:
                with self.gbuffer:
                    self.draw_to_gbuffer_program["camera"] = self.camera
                    self.draw_to_gbuffer_program["use_skydome_map"] = self.scene.skydome.is_completed
                    self.draw_to_gbuffer_program["skydome_map"] = self.scene.skydome.skydome_map
                    for mesh, instances in none_filled_meshes.items():
                        if not mesh.is_filled:
                            self.draw_to_gbuffer(mesh, instances)

            self.gbuffer.draw_to(self.OIT_fbo, GL.GL_DEPTH_ATTACHMENT)

    def generate_SSAO(self, view_pos_alpha_map, view_normal_map):
        self._SSAO_map = None
        if not self._enable_SSAO or GLConfig.polygon_mode != GL.GL_FILL:
            return
        
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
        self._should_update = False
        self.update_dir_lights_depth()
        self.update_point_lights_depth()
        self.update_spot_lights_depth()
        self.draw_opaque()
        self.draw_transparent()
        return self._should_update