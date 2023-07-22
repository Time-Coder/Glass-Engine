from .Renderer import Renderer
from .FlatCamera import FlatCamera
from ..Filters import GaussFilter, DOFFilter, FXAAFilter, BloomFilter, HDRFilter
from ..Frame import Frame

from glass import \
    ShaderProgram, GLConfig, FBO, RBO, sampler2D, sampler2DMS, ACBO, uimage2D, image2D, samplerCube, GLInfo
from glass.DictList import DictList
from glass.utils import checktype

from OpenGL import GL
import glm

class CommonRenderer(Renderer):

    def __init__(self):
        Renderer.__init__(self)

        self.camera = None
        self.scene = None

        self._enable_SSAO = False
        self._SSAO_map = None
        self._SSAO_samples = 64
        self._SSAO_radius = 0.2
        self._SSAO_power = 2.2
        self._SSAO_blur_filter = GaussFilter(15)
        self._envFXAA = True
        self._should_update = False

        self._DOF = False
        self._transparent_meshes = {}

        self._flat_cameras = DictList()
        self._flat_cameras["right"] = FlatCamera("right")
        self._flat_cameras["left"] = FlatCamera("left")
        self._flat_cameras["bottom"] = FlatCamera("bottom")
        self._flat_cameras["top"] = FlatCamera("top")
        self._flat_cameras["front"] = FlatCamera("front")
        self._flat_cameras["back"] = FlatCamera("back")

        self.filters["bloom"] = BloomFilter()
        self.filters["DOF"] = DOFFilter()
        self.filters["HDR"] = HDRFilter()
        self.filters["FXAA"] = FXAAFilter(internal_format=GL.GL_RGB8)

        self.filters["bloom"].enabled = False
        self.filters["DOF"].enabled = False
        self.filters["HDR"].enabled = False
        self.filters["FXAA"].enabled = False

    @property
    def bloom(self):
        return self.filters["bloom"].enabled
    
    @bloom.setter
    @checktype
    def bloom(self, flag:bool):
        self.filters["bloom"].enabled = flag

    @property
    def HDR(self):
        return self.filters["HDR"].enabled
    
    @HDR.setter
    @checktype
    def HDR(self, flag:bool):
        self.filters["HDR"].enabled = flag

    @property
    def DOF(self):
        return self.filters["DOF"].enabled
    
    @DOF.setter
    @checktype
    def DOF(self, flag:bool):
        self.filters["DOF"].enabled = flag

    @property
    def FXAA(self):
        return self.filters["FXAA"].enabled
    
    @FXAA.setter
    def FXAA(self, flag:bool):
        self.filters["FXAA"].enabled = flag

    @property
    def envFXAA(self):
        return self._envFXAA
    
    @envFXAA.setter
    def envFXAA(self, flag:bool):
        if self._envFXAA == flag:
            return
        
        self._envFXAA = flag
        if self.scene is None:
            return
        
        if flag:
            self.camera.screen.makeCurrent()
            for mesh, instances in self.scene.all_meshes.items():
                if not mesh.material.need_env_map:
                    continue

                for inst in instances:
                    if "env_bake_state" not in inst.user_data or \
                       inst.user_data["env_bake_state"] != "baked":
                        continue

                    env_OIT_blend_fbo = self.env_OIT_blend_fbo(inst)
                    env_map = env_OIT_blend_fbo.color_attachment(0)
                    env_FXAA_fbo = self.env_FXAA_fbo(inst)
                    with env_FXAA_fbo:
                        FXAAFilter.program["screen_image"] = env_map
                        FXAAFilter.program.draw_triangles(Frame.vertices, Frame.indices)
                    env_map = env_FXAA_fbo.color_attachment(0)
                    inst.env_map_index = env_map.index
                    inst.user_data["env_bake_state"] = "filtered"
        else:
            for mesh, instances in self.scene.all_meshes.items():
                if not mesh.material.need_env_map:
                    continue

                for inst in instances:
                    if "env_bake_state" not in inst.user_data or \
                       inst.user_data["env_bake_state"] != "filtered":
                        continue

                    env_OIT_blend_fbo = self.env_OIT_blend_fbo(inst)
                    inst.env_map_index = env_OIT_blend_fbo.color_attachment(0).index

    @property
    def programs(self):
        if not hasattr(self, "_programs"):
            self._programs = {}
            
        return self._programs
    
    @property
    def fbos(self):
        if not hasattr(self, "_fbos"):
            self._fbos = {}

        return self._fbos

    @property
    def SSAO(self):
        return self._enable_SSAO
    
    @SSAO.setter
    @checktype
    def SSAO(self, flag:bool):
        self._enable_SSAO = flag

    @property
    def SSAO_radius(self):
        return self._SSAO_radius
    
    @SSAO_radius.setter
    @checktype
    def SSAO_radius(self, radius:float):
        self._SSAO_radius = radius

    @property
    def SSAO_samples(self):
        return self._SSAO_samples
    
    @SSAO_samples.setter
    @checktype
    def SSAO_samples(self, samples:int):
        self._SSAO_samples = samples

    @property
    def SSAO_power(self):
        return self._SSAO_power
    
    @SSAO_power.setter
    @checktype
    def SSAO_power(self, power:float):
        self._SSAO_power = power

    def startup(self, camera, scene):
        self.camera = camera
        self.scene = scene
        self.filters["DOF"].camera = camera
        self.filters["HDR"].camera = camera

        return False
    
    @property
    def forward_program(self):
        if "forward" in self.programs:
            return self.programs["forward"]
        
        program = ShaderProgram()
        program.compile("../glsl/Pipelines/forward_rendering/forward_rendering.vs")
        program.compile("../glsl/Pipelines/forward_rendering/forward_rendering.gs")
        program.compile("../glsl/Pipelines/forward_rendering/forward_rendering.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)
        program["BindlessSampler2Ds"].bind(sampler2D.BindlessSampler2Ds)

        self.programs["forward"] = program

        return program

    @property
    def OIT_blend_program(self):
        if "OIT_blend" in self.programs:
            return self.programs["OIT_blend"]
        
        program = ShaderProgram()
        program.compile("../glsl/Pipelines/draw_frame.vs")
        program.compile("../glsl/Pipelines/OIT_blend.fs")
        self.programs["OIT_blend"] = program
        return program
    
    @property
    def OIT_fbo(self):
        fbo = None
        screen_size = GLConfig.screen_size

        samples = self.camera.screen.samples
        if samples > 1:
            if "OIT_ms" in self.fbos:
                fbo = self.fbos["OIT_ms"]
                fbo.resize(screen_size.x, screen_size.y, samples)
            else:
                fbo = FBO(screen_size.x, screen_size.y, samples)
                fbo.attach(0, sampler2DMS, GL.GL_RGBA32F)
                fbo.attach(1, sampler2DMS, GL.GL_RGBA32F)
                fbo.attach(2, sampler2DMS, GL.GL_R32F)
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
                fbo.auto_clear = False
                self.fbos["OIT_ms"] = fbo
            return fbo
        else:
            if "OIT" in self.fbos:
                fbo = self.fbos["OIT"]
                fbo.resize(screen_size.x, screen_size.y)
            else:
                fbo = FBO(screen_size.x, screen_size.y)
                fbo.attach(0, sampler2D, GL.GL_RGBA32F)
                fbo.attach(1, sampler2D, GL.GL_RGBA32F)
                fbo.attach(2, sampler2D, GL.GL_R32F)
                fbo.attach(GL.GL_DEPTH_ATTACHMENT, RBO)
                fbo.auto_clear = False
                self.fbos["OIT"] = fbo
            return fbo

    def env_OIT_blend_fbo(self, instance):
        current_context = GLConfig.buffered_current_context
        key = ("env_OIT_blend_fbo", current_context)
        if key in instance.user_data:
            return instance.user_data[key]
        
        fbo = FBO(2048, 1024)
        fbo.attach(0, sampler2D, GL.GL_RGBA32F)
        fbo.color_attachment(0).filter_mipmap = GL.GL_LINEAR
        instance.user_data[key] = fbo
        return fbo

    def env_FXAA_fbo(self, instance):
        current_context = GLConfig.buffered_current_context
        key = ("env_FXAA_fbo", current_context)
        if key in instance.user_data:
            return instance.user_data[key]
        
        FXAA_fbo = FBO(2048, 1024)
        FXAA_fbo.attach(0, sampler2D)
        FXAA_fbo.color_attachment(0).filter_mipmap = GL.GL_LINEAR
        instance.user_data[key] = FXAA_fbo

        return FXAA_fbo

    @property
    def gen_env_map_program(self):
        if "gen_env_map" not in self.programs:
            program = ShaderProgram()
            program.compile("../glsl/Pipelines/env_mapping/gen_env_map.vs")
            program.compile("../glsl/Pipelines/env_mapping/gen_env_map.gs")
            program.compile("../glsl/Pipelines/env_mapping/gen_env_map.fs")
            program["DirLights"].bind(self.scene.dir_lights)
            program["PointLights"].bind(self.scene.point_lights)
            program["SpotLights"].bind(self.scene.spot_lights)
            program["BindlessSampler2Ds"].bind(sampler2D.BindlessSampler2Ds)
            
            self.programs["gen_env_map"] = program

        return self.programs["gen_env_map"]

    @property
    def ssao_generate_program(self):
        if "ssao_generate" in self.programs:
            return self.programs["ssao_generate"]
        
        program = ShaderProgram()
        program.compile("../glsl/Pipelines/draw_frame.vs")
        program.compile("../glsl/Pipelines/SSAO/ssao_generate.fs")
        self.programs["ssao_generate"] = program
        
        return program
    
    @property
    def ssao_fbo(self):
        half_screen_size = GLConfig.screen_size/2
        if "ssao" in self.fbos:
            self.fbos["ssao"].resize(half_screen_size.x, half_screen_size.y)
        else:
            fbo = FBO(half_screen_size.x, half_screen_size.y)
            fbo.attach(0, sampler2D)
            self.fbos["ssao"] = fbo

        return self.fbos["ssao"]
    
    def env_map_fbo(self, instance):
        current_context = GLConfig.buffered_current_context
        key = ("env_map_fbo", current_context)
        if key in instance.user_data:
            return instance.user_data[key]
        
        env_map_fbo = FBO(1024, 1024)
        env_map_fbo.attach(0, samplerCube)
        env_map_fbo.attach(1, samplerCube)
        env_map_fbo.attach(2, samplerCube)
        env_map_fbo.attach(GL.GL_DEPTH_ATTACHMENT, samplerCube)
        env_map_fbo.auto_clear = False
        instance.user_data[key] = env_map_fbo
        
        return env_map_fbo

    def env_bake_times(self, instance):
        key = ("env_bake_times", self.scene)
        if key in instance.user_data:
            return instance.user_data[key]
        
        return 0
    
    def increase_bake_times(self, instance):
        key = ("env_bake_times", self.scene)
        if key not in instance.user_data:
            instance.user_data[key] = 0

        instance.user_data[key] += 1

    def gen_env_map(self, mesh, instances):
        max_bake_times = max(mesh.material.env_max_bake_times, mesh._back_material.env_max_bake_times)
        mesh_center = mesh.center
        for instance in instances:
            if instance.visible == 0:
                continue

            if self.env_bake_times(instance) >= max_bake_times:
                continue

            camera_pos = mesh_center + instance.abs_position
            for camera in self._flat_cameras:
                camera.abs_position = camera_pos

            instance.visible = 0
            env_map_fbo = self.env_map_fbo(instance)
            env_transparent_meshes = {}
            with GLConfig.LocalConfig(depth_test=True, depth_write=True, blend=False):
                with env_map_fbo:
                    GLConfig.clear_buffers()

                    self.gen_env_map_program["cameras"] = self._flat_cameras
                    self.gen_env_map_program["is_opaque_pass"] = True
                    self.gen_env_map_program["use_skybox_map"] = self.scene.skybox.is_completed
                    self.gen_env_map_program["skybox_map"] = self.scene.skybox.skybox_map
                    self.gen_env_map_program["use_skydome_map"] = self.scene.skydome.is_completed
                    self.gen_env_map_program["skydome_map"] = self.scene.skydome.skydome_map
                    self.gen_env_map_program["SSAO_map"] = None
                    for other_mesh, other_instances in self.scene.all_meshes.items():
                        if other_mesh.has_opaque:
                            self.gen_env_map_program["explode_distance"] = other_mesh.explode_distance
                            self.gen_env_map_program["material"] = other_mesh.material
                            self.gen_env_map_program["back_material"] = other_mesh._back_material
                            self.gen_env_map_program["is_filled"] = other_mesh.is_filled
                            self.gen_env_map_program["is_sphere"] = other_mesh.is_sphere
                            other_mesh.draw(self.gen_env_map_program, other_instances)
                        if other_mesh.has_transparent:
                            env_transparent_meshes[other_mesh] = other_instances

            opaque_color_map = env_map_fbo.color_attachment(0)
            accum_map = None
            reveal_map = None
            if env_transparent_meshes:
                with GLConfig.LocalConfig(
                    depth_test=True, depth_write=False, blend=True,
                    blend_src_rgb=GL.GL_ONE, blend_dest_rgb=GL.GL_ONE,
                    blend_src_alpha=GL.GL_ONE, blend_dest_alpha=GL.GL_ONE):
                    GLConfig.blend_src_rgbi[1] = GL.GL_ONE
                    GLConfig.blend_dest_rgbi[1] = GL.GL_ONE
                    GLConfig.blend_src_rgbi[2] = GL.GL_ONE
                    GLConfig.blend_dest_rgbi[2] = GL.GL_ONE
                    with env_map_fbo:
                        GLConfig.clear_buffer(1, glm.vec4(0, 0, 0, 0))
                        GLConfig.clear_buffer(2, glm.vec4(0, 0, 0, 0))

                        self.gen_env_map_program["cameras"] = self._flat_cameras
                        self.gen_env_map_program["is_opaque_pass"] = False
                        self.gen_env_map_program["use_skybox_map"] = self.scene.skybox.is_completed
                        self.gen_env_map_program["skybox_map"] = self.scene.skybox.skybox_map
                        self.gen_env_map_program["use_skydome_map"] = self.scene.skydome.is_completed
                        self.gen_env_map_program["skydome_map"] = self.scene.skydome.skydome_map
                        self.gen_env_map_program["SSAO_map"] = None
                        for other_mesh, other_instances in env_transparent_meshes.items():
                            self.gen_env_map_program["explode_distance"] = other_mesh.explode_distance
                            self.gen_env_map_program["material"] = other_mesh.material
                            self.gen_env_map_program["back_material"] = other_mesh._back_material
                            self.gen_env_map_program["is_filled"] = other_mesh.is_filled
                            self.gen_env_map_program["is_sphere"] = other_mesh.is_sphere
                            other_mesh.draw(self.gen_env_map_program, other_instances)

                    # 取出 OIT 信息
                    accum_map = env_map_fbo.color_attachment(1)
                    reveal_map = env_map_fbo.color_attachment(2)

            env_OIT_blend_fbo = self.env_OIT_blend_fbo(instance)
            with GLConfig.LocalConfig(
                polygon_mode=GL.GL_FILL,
                cull_face=None,
                depth_func=GL.GL_ALWAYS
            ):
                with env_OIT_blend_fbo:
                    self.env_OIT_blend_program["opaque_color_map"] = opaque_color_map
                    self.env_OIT_blend_program["accum_map"] = accum_map
                    self.env_OIT_blend_program["reveal_map"] = reveal_map
                    self.env_OIT_blend_program.draw_triangles(Frame.vertices, Frame.indices)

            env_map = env_OIT_blend_fbo.color_attachment(0)
            instance.user_data["env_bake_state"] = "baked"
            if self._envFXAA:
                env_FXAA_fbo = self.env_FXAA_fbo(instance)
                with env_FXAA_fbo:
                    FXAAFilter.program["screen_image"] = env_map
                    FXAAFilter.program.draw_triangles(Frame.vertices, Frame.indices)
                env_map = env_FXAA_fbo.color_attachment(0)
                instance.user_data["env_bake_state"] = "filtered"
            instance.env_map_index = env_map.index
            instance.visible = 1
            self.increase_bake_times(instance)

            if self.env_bake_times(instance) <= max_bake_times:
                self._should_update = True

    def forward_draw_mesh(self, mesh, instances):
        if mesh.material.need_env_map or mesh._back_material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.forward_program["material"] = mesh.material
        self.forward_program["back_material"] = mesh._back_material
        self.forward_program["explode_distance"] = mesh.explode_distance
        self.forward_program["is_filled"] = mesh.is_filled
        self.forward_program["is_sphere"] = mesh.is_sphere
        mesh.draw(self.forward_program, instances)

    def draw_tangent(self, mesh, instances):
        if mesh.tangent_scale != 0:
            with GLConfig.LocalConfig(line_width=mesh.tangent_line_width):
                self.draw_tangent_program["tangent_scale"] = mesh.tangent_scale
                self.draw_tangent_program["color"] = mesh.tangent_color
                self.draw_tangent_program["explode_distance"] = mesh.explode_distance
                mesh.draw(self.draw_tangent_program, instances)

    def draw_bitangent(self, mesh, instances):
        if mesh.bitangent_scale != 0:
            with GLConfig.LocalConfig(line_width=mesh.bitangent_line_width):
                self.draw_bitangent_program["bitangent_scale"] = mesh.bitangent_scale
                self.draw_bitangent_program["color"] = mesh.bitangent_color
                self.draw_bitangent_program["explode_distance"] = mesh.explode_distance
                mesh.draw(self.draw_bitangent_program, instances)

    def draw_normal(self, mesh, instances):
        if mesh.normal_scale != 0:
            with GLConfig.LocalConfig(line_width=mesh.normal_line_width):
                self.draw_normal_program["normal_scale"] = mesh.normal_scale
                self.draw_normal_program["color"] = mesh.normal_color
                self.draw_normal_program["explode_distance"] = mesh.explode_distance
                mesh.draw(self.draw_normal_program, instances)

    def draw_TBN(self, mesh, instances):
        self.draw_tangent(mesh, instances)
        self.draw_bitangent(mesh, instances)
        self.draw_normal(mesh, instances)

    @property
    def env_OIT_blend_program(self):
        if "env_OIT_blend" in self.programs:
            return self.programs["env_OIT_blend"]
        
        program = ShaderProgram()
        program.compile("../glsl/Pipelines/draw_frame.vs")
        program.compile("../glsl/Pipelines/env_mapping/env_OIT_blend.fs")
        self.programs["env_OIT_blend"] = program

        return program

    def draw_transparent(self):
        if not self._transparent_meshes:
            return
        
        with GLConfig.LocalConfig(depth_test=True, depth_write=False, blend=True):
            GLConfig.blend_src_rgbi[1] = GL.GL_ONE
            GLConfig.blend_dest_rgbi[1] = GL.GL_ONE
            GLConfig.blend_src_rgbi[2] = GL.GL_ONE
            GLConfig.blend_dest_rgbi[2] = GL.GL_ONE
            with self.OIT_fbo:
                GLConfig.clear_buffer(1, glm.vec4(0, 0, 0, 0))
                GLConfig.clear_buffer(2, glm.vec4(0, 0, 0, 0))

                self.forward_program["camera"] = self.camera
                self.forward_program["is_opaque_pass"] = False
                self.forward_program["SSAO_map"] = self._SSAO_map
                self.forward_program["use_skybox_map"] = self.scene.skybox.is_completed
                self.forward_program["skybox_map"] = self.scene.skybox.skybox_map
                self.forward_program["use_skydome_map"] = self.scene.skydome.is_completed
                self.forward_program["skydome_map"] = self.scene.skydome.skydome_map
                for mesh, instances in self._transparent_meshes.items():
                    self.forward_draw_mesh(mesh, instances)

        # 取出 OIT 信息
        resolved = self.OIT_fbo.resolved
        accum_map = resolved.color_attachment(1)
        reveal_map = resolved.color_attachment(2)

        with GLConfig.LocalConfig(
            polygon_mode=GL.GL_FILL,
            cull_face=None,
            depth_func=GL.GL_ALWAYS,
            blend=True,
            blend_func=(GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_SRC_ALPHA)
        ):
            self.OIT_blend_program["accum_map"] = accum_map
            self.OIT_blend_program["reveal_map"] = reveal_map
            self.OIT_blend_program.draw_triangles(Frame.vertices, Frame.indices)
