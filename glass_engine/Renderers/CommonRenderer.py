from .Renderer import Renderer
from ..Filters import GaussFilter, KernelFilter, BloomFilter, DOFFilter, HDRFilter, FXAAFilter
from ..Frame import Frame

from glass import ShaderProgram, GLConfig, FBO, RBO, sampler2D, sampler2DMS, samplerCube, sampler2DArray, GlassConfig, GLInfo
from glass.utils import checktype, cat, modify_time

from OpenGL import GL
import glm
import os
import numpy as np

class CommonRenderer(Renderer):

    __dir_light_depth_geo_shader_template = None
    __dir_light_depth_lines_geo_shader_template = None
    __dir_light_depth_points_geo_shader_template = None

    def __init__(self):
        Renderer.__init__(self)

        self._enable_SSAO = False
        self._SSAO_map = None
        self._SSAO_samples = 64
        self._SSAO_radius = 0.2
        self._SSAO_power = 2.2
        self._SSAO_filter = GaussFilter(15)
        self._envFXAA = True
        self._should_update = False

        self._DOF = False
        self._all_meshes = []
        self._all_lines = []
        self._all_points = []
        self._opaque_meshes = []
        self._opaque_lines = []
        self._opaque_points = []
        self._transparent_meshes = []
        self._transparent_points = []
        self._transparent_lines = []
        self._meshes_cast_shadows = []
        self._lines_cast_shadows = []
        self._points_cast_shadows = []

        self._depth_filter_kernel = KernelFilter.Kernel(np.ones((5, 5))/25)

        self.filters["bloom"] = BloomFilter()
        self.filters["DOF"] = DOFFilter()
        self.filters["HDR"] = HDRFilter()
        self.filters["FXAA"] = FXAAFilter(internal_format=GL.GL_RGBA8)

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
                if not mesh.material.need_env_map and \
                   not mesh._back_material.need_env_map:
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
                    inst.env_map_handle = env_map.handle
                    inst.user_data["env_bake_state"] = "filtered"
        else:
            for mesh, instances in self.scene.all_meshes.items():
                if not mesh.material.need_env_map and \
                   not mesh._back_material.need_env_map:
                    continue

                for inst in instances:
                    if "env_bake_state" not in inst.user_data or \
                       inst.user_data["env_bake_state"] != "filtered":
                        continue

                    env_OIT_blend_fbo = self.env_OIT_blend_fbo(inst)
                    inst.env_map_handle = env_OIT_blend_fbo.color_attachment(0).handle

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

    def startup(self):
        self.filters["DOF"].camera = self.camera
        self.filters["HDR"].camera = self.camera

        return False
    
    @property
    def dir_light_depth_geo_shader_path(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        target_filename = GlassConfig.cache_folder + f"/DirLight_depth{self.camera.CSM_levels}.gs"
        template_filename = self_folder + "/../glsl/Pipelines/DirLight_depth/DirLight_depth.gs"
        if not os.path.isfile(target_filename) or modify_time(template_filename) > modify_time(target_filename):
            if CommonRenderer.__dir_light_depth_geo_shader_template is None:
                CommonRenderer.__dir_light_depth_geo_shader_template = cat(template_filename)

            content = CommonRenderer.__dir_light_depth_geo_shader_template.replace("{CSM_levels}", str(self.camera.CSM_levels))
            out_file = open(target_filename, "w")
            out_file.write(content)
            out_file.close()

        return target_filename
    
    @property
    def dir_light_depth_lines_geo_shader_path(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        target_filename = GlassConfig.cache_folder + f"/DirLight_depth_lines{self.camera.CSM_levels}.gs"
        template_filename = self_folder + "/../glsl/Pipelines/DirLight_depth/DirLight_depth_lines.gs"
        if not os.path.isfile(target_filename) or modify_time(template_filename) > modify_time(target_filename):
            if CommonRenderer.__dir_light_depth_lines_geo_shader_template is None:
                CommonRenderer.__dir_light_depth_lines_geo_shader_template = cat(template_filename)

            content = CommonRenderer.__dir_light_depth_lines_geo_shader_template.replace("{CSM_levels}", str(self.camera.CSM_levels))
            out_file = open(target_filename, "w")
            out_file.write(content)
            out_file.close()

        return target_filename

    @property
    def dir_light_depth_points_geo_shader_path(self):
        self_folder = os.path.dirname(os.path.abspath(__file__))
        target_filename = GlassConfig.cache_folder + f"/DirLight_depth_points{self.camera.CSM_levels}.gs"
        template_filename = self_folder + "/../glsl/Pipelines/DirLight_depth/DirLight_depth_points.gs"
        if not os.path.isfile(target_filename) or modify_time(template_filename) > modify_time(target_filename):
            if CommonRenderer.__dir_light_depth_points_geo_shader_template is None:
                CommonRenderer.__dir_light_depth_points_geo_shader_template = cat(template_filename)

            content = CommonRenderer.__dir_light_depth_points_geo_shader_template.replace("{CSM_levels}", str(self.camera.CSM_levels))
            out_file = open(target_filename, "w")
            out_file.write(content)
            out_file.close()

        return target_filename

    @property
    def dir_light_depth_program(self):
        key = f"dir_light_depth{self.camera.CSM_levels}"
        if key in self.programs:
            return self.programs[key]
        
        program = ShaderProgram()
        program.add_include_path(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/DirLight_depth")
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/DirLight_depth/DirLight_depth.vs")
        program.compile(self.dir_light_depth_geo_shader_path)
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/DirLight_depth/DirLight_depth.fs")

        self.programs[key] = program

        return program
    
    @property
    def dir_light_depth_lines_program(self):
        key = f"dir_light_depth_lines{self.camera.CSM_levels}"
        if key in self.programs:
            return self.programs[key]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.add_include_path(self_folder + "/../glsl/Pipelines/DirLight_depth")
        program.compile(self_folder + "/../glsl/Pipelines/DirLight_depth/DirLight_depth.vs")
        program.compile(self.dir_light_depth_lines_geo_shader_path)
        program.compile(self_folder + "/../glsl/Pipelines/DirLight_depth/DirLight_depth.fs")

        self.programs[key] = program

        return program

    @property
    def dir_light_depth_points_program(self):
        key = f"dir_light_depth_points{self.camera.CSM_levels}"
        if key in self.programs:
            return self.programs[key]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.add_include_path(self_folder + "/../glsl/Pipelines/DirLight_depth")
        program.compile(self_folder + "/../glsl/Pipelines/DirLight_depth/DirLight_depth.vs")
        program.compile(self.dir_light_depth_points_geo_shader_path)
        program.compile(self_folder + "/../glsl/Pipelines/DirLight_depth/DirLight_depth.fs")

        self.programs[key] = program

        return program
    
    @property
    def point_light_depth_program(self):
        if "point_light_depth" in self.programs:
            return self.programs["point_light_depth"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.vs")
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.gs")
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.fs")

        self.programs["point_light_depth"] = program

        return program
    
    @property
    def point_light_depth_lines_program(self):
        if "point_light_depth_lines" in self.programs:
            return self.programs["point_light_depth_lines"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.vs")
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth_lines.gs")
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.fs")

        self.programs["point_light_depth_lines"] = program

        return program

    @property
    def point_light_depth_points_program(self):
        if "point_light_depth_points" in self.programs:
            return self.programs["point_light_depth_points"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.vs")
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth_points.gs")
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.fs")

        self.programs["point_light_depth_points"] = program

        return program
    
    @property
    def spot_light_depth_program(self):
        if "spot_light_depth" in self.programs:
            return self.programs["spot_light_depth"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.vs")
        program.compile(self_folder + "/../glsl/Pipelines/SpotLight_depth/SpotLight_depth.gs")
        program.compile(self_folder + "/../glsl/Pipelines/SpotLight_depth/SpotLight_depth.fs")

        self.programs["spot_light_depth"] = program

        return program
    
    @property
    def spot_light_depth_lines_program(self):
        if "spot_light_depth_lines" in self.programs:
            return self.programs["spot_light_depth_lines"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.vs")
        program.compile(self_folder + "/../glsl/Pipelines/SpotLight_depth/SpotLight_depth_lines.gs")
        program.compile(self_folder + "/../glsl/Pipelines/SpotLight_depth/SpotLight_depth.fs")

        self.programs["spot_light_depth_lines"] = program

        return program

    @property
    def spot_light_depth_points_program(self):
        if "spot_light_depth_points" in self.programs:
            return self.programs["spot_light_depth_points"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/PointLight_depth/PointLight_depth.vs")
        program.compile(self_folder + "/../glsl/Pipelines/SpotLight_depth/SpotLight_depth_points.gs")
        program.compile(self_folder + "/../glsl/Pipelines/SpotLight_depth/SpotLight_depth.fs")

        self.programs["spot_light_depth_points"] = program

        return program
    
    def classify_meshes(self):
        self._all_meshes.clear()
        self._all_lines.clear()
        self._all_points.clear()
        self._opaque_meshes.clear()
        self._opaque_lines.clear()
        self._opaque_points.clear()
        self._transparent_meshes.clear()
        self._transparent_lines.clear()
        self._transparent_points.clear()
        self._meshes_cast_shadows.clear()
        self._lines_cast_shadows.clear()
        self._points_cast_shadows.clear()

        for mesh_tuple in self.scene.all_meshes.items():
            mesh = mesh_tuple[0]
            if mesh.primitive in GLInfo.triangle_types:
                self._all_meshes.append(mesh_tuple)
                
                if mesh.material.cast_shadows:
                    self._meshes_cast_shadows.append(mesh_tuple)

                if mesh.has_transparent:
                    self._transparent_meshes.append(mesh_tuple)

                if mesh.has_opaque:
                    self._opaque_meshes.append(mesh_tuple)

            elif mesh.primitive in GLInfo.line_types:
                self._all_lines.append(mesh_tuple)
                
                if mesh.material.cast_shadows:
                    self._lines_cast_shadows.append(mesh_tuple)

                if mesh.has_transparent:
                    self._transparent_lines.append(mesh_tuple)

                if mesh.has_opaque:
                    self._opaque_lines.append(mesh_tuple)

            elif mesh.primitive == GL.GL_POINTS:
                self._all_points.append(mesh_tuple)
                
                if mesh.material.cast_shadows:
                    self._points_cast_shadows.append(mesh_tuple)

                if mesh.has_transparent:
                    self._transparent_points.append(mesh_tuple)

                if mesh.has_opaque:
                    self._opaque_points.append(mesh_tuple)

    def update_spot_lights_depth(self):
        if not self._meshes_cast_shadows and \
           not self._lines_cast_shadows and \
           not self._points_cast_shadows:
            return

        for spot_light in self.scene.spot_lights:
            if not spot_light.generate_shadows or \
               not spot_light.need_update_depth_map:
                continue

            if spot_light.depth_fbo is None:
                spot_light.depth_fbo = FBO(1024, 1024)
                spot_light.depth_fbo.attach(GL.GL_DEPTH_ATTACHMENT, samplerCube)
                spot_light.depth_fbo.depth_attachment.wrap = GL.GL_CLAMP_TO_EDGE
            
            with GLConfig.LocalConfig(depth_test=True, blend=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with spot_light.depth_fbo:
                    if self._meshes_cast_shadows:
                        self.spot_light_depth_program["spot_light"] = spot_light
                        for mesh, instances in self._meshes_cast_shadows:
                            self.spot_light_depth_program["explode_distance"] = mesh.explode_distance
                            mesh.draw(self.spot_light_depth_program, instances)

                    if self._lines_cast_shadows:
                        self.spot_light_depth_lines_program["spot_light"] = spot_light
                        for mesh, instances in self._lines_cast_shadows:
                            mesh.draw(self.spot_light_depth_lines_program, instances)

                    if self._points_cast_shadows:
                        self.spot_light_depth_points_program["spot_light"] = spot_light
                        for mesh, instances in self._points_cast_shadows:
                            mesh.draw(self.spot_light_depth_points_program, instances)

            new_handle = spot_light.depth_fbo.depth_attachment.handle
            if spot_light.depth_map_handle != new_handle:
                spot_light.depth_map_handle = new_handle
                self.scene.spot_lights.dirty = True

            spot_light.need_update_depth_map = False

    def update_point_lights_depth(self):
        if not self._meshes_cast_shadows and \
           not self._lines_cast_shadows and \
           not self._points_cast_shadows:
            return
        
        for point_light in self.scene.point_lights:
            if not point_light.generate_shadows or \
               not point_light.need_update_depth_map:
                continue

            if point_light.depth_fbo is None:
                point_light.depth_fbo = FBO(1024, 1024)
                point_light.depth_fbo.attach(GL.GL_DEPTH_ATTACHMENT, samplerCube)
                point_light.depth_fbo.depth_attachment.wrap = GL.GL_CLAMP_TO_EDGE
            
            with GLConfig.LocalConfig(depth_test=True, blend=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with point_light.depth_fbo:
                    if self._meshes_cast_shadows:
                        self.point_light_depth_program["point_light"] = point_light
                        for mesh, instances in self._meshes_cast_shadows:
                            self.point_light_depth_program["explode_distance"] = mesh.explode_distance
                            mesh.draw(self.point_light_depth_program, instances)

                    if self._lines_cast_shadows:
                        self.point_light_depth_lines_program["point_light"] = point_light
                        for mesh, instances in self._lines_cast_shadows:
                            mesh.draw(self.point_light_depth_lines_program, instances)

                    if self._points_cast_shadows:
                        self.point_light_depth_points_program["point_light"] = point_light
                        for mesh, instances in self._points_cast_shadows:
                            mesh.draw(self.point_light_depth_points_program, instances)

            new_handle = point_light.depth_fbo.depth_attachment.handle
            if point_light.depth_map_handle != new_handle:
                point_light.depth_map_handle = new_handle
                self.scene.point_lights.dirty = True

            point_light.need_update_depth_map = False

    def update_dir_lights_depth(self):
        if not self._meshes_cast_shadows and \
           not self._lines_cast_shadows and \
           not self._points_cast_shadows:
            return
        
        for dir_light in self.scene.dir_lights:
            if not dir_light.generate_shadows:
                continue

            dir_light.max_back_offset = 0

        for mesh, instances in self.scene.all_meshes.items():
            if not mesh.material.cast_shadows:
                continue

            original_center = mesh.center
            original_corner = glm.vec3()
            original_corner.x = original_center.x + (mesh.x_max - mesh.x_min)/2
            original_corner.y = original_center.y + (mesh.y_max - mesh.y_min)/2
            original_corner.z = original_center.z + (mesh.z_max - mesh.z_min)/2
            for instance in instances:
                center = instance.apply(original_center)
                corner = instance.apply(original_corner)
                radius = glm.length(corner - center)

                for dir_light in self.scene.dir_lights:
                    if not dir_light.generate_shadows:
                        continue

                    current_offset = radius + glm.dot(center, -dir_light.direction)
                    if current_offset > dir_light.max_back_offset:
                        dir_light.max_back_offset = current_offset

        for dir_light in self.scene.dir_lights:
            if not dir_light.generate_shadows:
                continue

            if dir_light.depth_fbo is None:
                dir_light.depth_fbo = FBO(1024, 1024, layers=self.camera.CSM_levels)
                dir_light.depth_fbo.attach(GL.GL_DEPTH_ATTACHMENT, sampler2DArray)

                dir_light.depth_fbo.depth_attachment.wrap_s = GL.GL_CLAMP_TO_BORDER
                dir_light.depth_fbo.depth_attachment.wrap_t = GL.GL_CLAMP_TO_BORDER
                dir_light.depth_fbo.depth_attachment.border_color = glm.vec4(1, 1, 1, 1)

                dir_light.depth_filter = GaussFilter(5)
            
            with GLConfig.LocalConfig(clear_color=glm.vec4(1,1,1,1), depth_test=True, blend=False, cull_face=None, polygon_mode=GL.GL_FILL):
                with dir_light.depth_fbo:
                    if self._meshes_cast_shadows:
                        self.dir_light_depth_program["dir_light"] = dir_light
                        self.dir_light_depth_program["camera"] = self.camera
                        for mesh, instances in self._meshes_cast_shadows:
                            self.dir_light_depth_program["explode_distance"] = mesh.explode_distance
                            mesh.draw(self.dir_light_depth_program, instances)

                    if self._lines_cast_shadows:
                        self.dir_light_depth_lines_program["dir_light"] = dir_light
                        self.dir_light_depth_lines_program["camera"] = self.camera
                        for mesh, instances in self._lines_cast_shadows:
                            mesh.draw(self.dir_light_depth_lines_program, instances)

                    if self._points_cast_shadows:
                        self.dir_light_depth_points_program["dir_light"] = dir_light
                        self.dir_light_depth_points_program["camera"] = self.camera
                        for mesh, instances in self._points_cast_shadows:
                            mesh.draw(self.dir_light_depth_points_program, instances)

            new_handle = dir_light.depth_fbo.depth_attachment.handle
            if dir_light.depth_map_handle != new_handle:
                dir_light.depth_map_handle = new_handle
                self.scene.dir_lights.dirty = True
                self._should_update = True

    @property
    def forward_program(self):
        if "forward" in self.programs:
            return self.programs["forward"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_rendering.vs")
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_rendering.gs")
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_rendering.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)

        self.programs["forward"] = program

        return program
    
    @property
    def forward_lines_program(self):
        if "forward_lines" in self.programs:
            return self.programs["forward_lines"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_draw_lines.vs")
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_draw_points.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)

        self.programs["forward_lines"] = program

        return program

    @property
    def forward_points_program(self):
        if "forward_points" in self.programs:
            return self.programs["forward_points"]
        
        self_folder = os.path.dirname(os.path.abspath(__file__))
        program = ShaderProgram()
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_draw_points.vs")
        program.compile(self_folder + "/../glsl/Pipelines/forward_rendering/forward_draw_points.fs")

        program["PointLights"].bind(self.scene.point_lights)
        program["DirLights"].bind(self.scene.dir_lights)
        program["SpotLights"].bind(self.scene.spot_lights)

        self.programs["forward_points"] = program

        return program

    @property
    def OIT_blend_program(self):
        if "OIT_blend" in self.programs:
            return self.programs["OIT_blend"]
        
        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/OIT_blend.fs")
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
            self_folder = os.path.dirname(os.path.abspath(__file__))
            program = ShaderProgram()
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map.vs")
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map.gs")
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map.fs")
            program["DirLights"].bind(self.scene.dir_lights)
            program["PointLights"].bind(self.scene.point_lights)
            program["SpotLights"].bind(self.scene.spot_lights)
            
            self.programs["gen_env_map"] = program

        return self.programs["gen_env_map"]
    
    @property
    def gen_env_map_lines_program(self):
        if "gen_env_map_lines" not in self.programs:
            self_folder = os.path.dirname(os.path.abspath(__file__))
            program = ShaderProgram()
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map_points.vs")
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map_lines.gs")
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map_points.fs")
            program["DirLights"].bind(self.scene.dir_lights)
            program["PointLights"].bind(self.scene.point_lights)
            program["SpotLights"].bind(self.scene.spot_lights)
            
            self.programs["gen_env_map_lines"] = program

        return self.programs["gen_env_map_lines"]

    @property
    def gen_env_map_points_program(self):
        if "gen_env_map_points" not in self.programs:
            self_folder = os.path.dirname(os.path.abspath(__file__))
            program = ShaderProgram()
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map_points.vs")
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map_points.gs")
            program.compile(self_folder + "/../glsl/Pipelines/env_mapping/gen_env_map_points.fs")
            program["DirLights"].bind(self.scene.dir_lights)
            program["PointLights"].bind(self.scene.point_lights)
            program["SpotLights"].bind(self.scene.spot_lights)
            
            self.programs["gen_env_map_points"] = program

        return self.programs["gen_env_map_points"]

    @property
    def generate_ssao_program(self):
        if "generate_ssao" in self.programs:
            return self.programs["generate_ssao"]
        
        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/SSAO/generate_ssao.fs")
        self.programs["generate_ssao"] = program
        
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
        key = ("env_map_fbo", GLConfig.buffered_current_context)
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

    def prepare_gen_env_map_draw_mesh(self, view_center:glm.vec3, is_opaque_pass:bool):
        self.gen_env_map_program["CSM_camera"] = self.camera
        self.gen_env_map_program["view_center"] = view_center
        self.gen_env_map_program["is_opaque_pass"] = is_opaque_pass
        self.gen_env_map_program["use_skybox_map"] = self.scene.skybox.is_completed
        self.gen_env_map_program["skybox_map"] = self.scene.skybox.skybox_map
        self.gen_env_map_program["use_skydome_map"] = self.scene.skydome.is_completed
        self.gen_env_map_program["skydome_map"] = self.scene.skydome.skydome_map
        self.gen_env_map_program["fog"] = self.scene.fog
        self.gen_env_map_program["SSAO_map"] = None

    def gen_env_map_draw_mesh(self, mesh, instances):
        self.gen_env_map_program["explode_distance"] = mesh.explode_distance
        self.gen_env_map_program["material"] = mesh.material
        self.gen_env_map_program["back_material"] = mesh._back_material
        self.gen_env_map_program["is_sphere"] = mesh.is_sphere
        self.gen_env_map_program["mesh_center"] = mesh.center
        mesh.draw(self.gen_env_map_program, instances)

    def prepare_gen_env_map_draw_lines(self, view_center:glm.vec3, is_opaque_pass:bool):
        self.gen_env_map_lines_program["CSM_camera"] = self.camera
        self.gen_env_map_lines_program["view_center"] = view_center
        self.gen_env_map_lines_program["is_opaque_pass"] = is_opaque_pass
        self.gen_env_map_lines_program["use_skybox_map"] = self.scene.skybox.is_completed
        self.gen_env_map_lines_program["skybox_map"] = self.scene.skybox.skybox_map
        self.gen_env_map_lines_program["use_skydome_map"] = self.scene.skydome.is_completed
        self.gen_env_map_lines_program["skydome_map"] = self.scene.skydome.skydome_map
        self.gen_env_map_lines_program["fog"] = self.scene.fog
        self.gen_env_map_lines_program["SSAO_map"] = None

    def gen_env_map_draw_lines(self, mesh, instances):
        self.gen_env_map_lines_program["material"] = mesh.material
        self.gen_env_map_lines_program["mesh_center"] = mesh.center
        mesh.draw(self.gen_env_map_lines_program, instances)

    def prepare_gen_env_map_draw_points(self, view_center:glm.vec3, is_opaque_pass:bool):
        self.gen_env_map_points_program["CSM_camera"] = self.camera
        self.gen_env_map_points_program["view_center"] = view_center
        self.gen_env_map_points_program["is_opaque_pass"] = is_opaque_pass
        self.gen_env_map_points_program["use_skybox_map"] = self.scene.skybox.is_completed
        self.gen_env_map_points_program["skybox_map"] = self.scene.skybox.skybox_map
        self.gen_env_map_points_program["use_skydome_map"] = self.scene.skydome.is_completed
        self.gen_env_map_points_program["skydome_map"] = self.scene.skydome.skydome_map
        self.gen_env_map_points_program["fog"] = self.scene.fog
        self.gen_env_map_points_program["SSAO_map"] = None

    def gen_env_map_draw_points(self, mesh, instances):
        self.gen_env_map_points_program["material"] = mesh.material
        self.gen_env_map_points_program["mesh_center"] = mesh.center
        mesh.draw(self.gen_env_map_points_program, instances)

    def gen_env_map(self, mesh, instances):
        max_bake_times = max(mesh.material.env_max_bake_times, mesh._back_material.env_max_bake_times)
        mesh_center = mesh.center
        for instance in instances:
            if instance.visible == 0:
                continue

            if self.env_bake_times(instance) >= max_bake_times:
                continue
            
            view_center = instance.apply(mesh_center)

            instance.visible = 0
            env_map_fbo = self.env_map_fbo(instance)

            with GLConfig.LocalConfig(depth_test=True, depth_write=True, blend=False):
                with env_map_fbo:
                    GLConfig.clear_buffers()

                    if self._opaque_meshes:
                        self.prepare_gen_env_map_draw_mesh(view_center, True)
                        for other_mesh, other_instances in self._opaque_meshes:
                            self.gen_env_map_draw_mesh(other_mesh, other_instances)

                    if self._opaque_lines:
                        self.prepare_gen_env_map_draw_lines(view_center, True)
                        for other_mesh, other_instances in self._opaque_lines:
                            self.gen_env_map_draw_lines(other_mesh, other_instances)

                    if self._opaque_points:
                        self.prepare_gen_env_map_draw_points(view_center, True)
                        for other_mesh, other_instances in self._opaque_points:
                            self.gen_env_map_draw_points(other_mesh, other_instances)

            opaque_color_map = env_map_fbo.color_attachment(0)
            accum_map = None
            reveal_map = None
            if self._transparent_meshes or self._transparent_points or self._transparent_lines:
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

                        if self._transparent_meshes:
                            self.prepare_gen_env_map_draw_mesh(view_center, False)
                            for other_mesh, other_instances in self._transparent_meshes:
                                self.gen_env_map_draw_mesh(other_mesh, other_instances)

                        if self._transparent_lines:
                            self.prepare_gen_env_map_draw_lines(view_center, False)
                            for other_mesh, other_instances in self._transparent_lines:
                                self.gen_env_map_draw_lines(other_mesh, other_instances)

                        if self._transparent_points:
                            self.prepare_gen_env_map_draw_points(view_center, False)
                            for other_mesh, other_instances in self._transparent_points:
                                self.gen_env_map_draw_points(other_mesh, other_instances)

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
            instance.env_map_handle = env_map.handle
            instance.visible = 1
            self.increase_bake_times(instance)

            if self.env_bake_times(instance) <= max_bake_times:
                self._should_update = True

    def prepare_forward_draw_mesh(self, is_opaque_pass:bool):
        self.forward_program["camera"] = self.camera
        self.forward_program["is_opaque_pass"] = is_opaque_pass
        self.forward_program["SSAO_map"] = self._SSAO_map
        self.forward_program["use_skybox_map"] = self.scene.skybox.is_completed
        self.forward_program["skybox_map"] = self.scene.skybox.skybox_map
        self.forward_program["use_skydome_map"] = self.scene.skydome.is_completed
        self.forward_program["skydome_map"] = self.scene.skydome.skydome_map
        self.forward_program["fog"] = self.scene.fog

    def forward_draw_mesh(self, mesh, instances):
        if mesh.material.need_env_map or mesh._back_material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.forward_program["material"] = mesh.material
        self.forward_program["back_material"] = mesh._back_material
        self.forward_program["explode_distance"] = mesh.explode_distance
        self.forward_program["is_sphere"] = mesh.is_sphere
        self.forward_program["mesh_center"] = mesh.center
        mesh.draw(self.forward_program, instances)

    def prepare_forward_draw_lines(self, is_opaque_pass:bool):
        self.forward_lines_program["camera"] = self.camera
        self.forward_lines_program["is_opaque_pass"] = is_opaque_pass
        self.forward_lines_program["SSAO_map"] = self._SSAO_map
        self.forward_lines_program["use_skybox_map"] = self.scene.skybox.is_completed
        self.forward_lines_program["skybox_map"] = self.scene.skybox.skybox_map
        self.forward_lines_program["use_skydome_map"] = self.scene.skydome.is_completed
        self.forward_lines_program["skydome_map"] = self.scene.skydome.skydome_map
        self.forward_lines_program["fog"] = self.scene.fog

    def forward_draw_lines(self, mesh, instances):
        if mesh.material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.forward_lines_program["material"] = mesh.material
        self.forward_lines_program["mesh_center"] = mesh.center
        mesh.draw(self.forward_lines_program, instances)

    def prepare_forward_draw_points(self, is_opaque_pass:bool):
        self.forward_points_program["camera"] = self.camera
        self.forward_points_program["is_opaque_pass"] = is_opaque_pass
        self.forward_points_program["SSAO_map"] = self._SSAO_map
        self.forward_points_program["use_skybox_map"] = self.scene.skybox.is_completed
        self.forward_points_program["skybox_map"] = self.scene.skybox.skybox_map
        self.forward_points_program["use_skydome_map"] = self.scene.skydome.is_completed
        self.forward_points_program["skydome_map"] = self.scene.skydome.skydome_map
        self.forward_points_program["fog"] = self.scene.fog

    def forward_draw_points(self, mesh, instances):
        if mesh.material.need_env_map:
            self.gen_env_map(mesh, instances)

        self.forward_points_program["material"] = mesh.material
        self.forward_points_program["mesh_center"] = mesh.center
        mesh.draw(self.forward_points_program, instances)

    @property
    def env_OIT_blend_program(self):
        if "env_OIT_blend" in self.programs:
            return self.programs["env_OIT_blend"]
        
        program = ShaderProgram()
        program.compile(Frame.draw_frame_vs)
        program.compile(os.path.dirname(os.path.abspath(__file__)) + "/../glsl/Pipelines/env_mapping/env_OIT_blend.fs")
        self.programs["env_OIT_blend"] = program

        return program

    def draw_transparent(self):
        if not self._transparent_meshes and \
           not self._transparent_points and \
           not self._transparent_lines:
            return
        
        with GLConfig.LocalConfig(depth_test=True, depth_write=False, blend=True):
            GLConfig.blend_src_rgbi[1] = GL.GL_ONE
            GLConfig.blend_dest_rgbi[1] = GL.GL_ONE
            GLConfig.blend_src_rgbi[2] = GL.GL_ONE
            GLConfig.blend_dest_rgbi[2] = GL.GL_ONE
            with self.OIT_fbo:
                GLConfig.clear_buffer(1, glm.vec4(0, 0, 0, 0))
                GLConfig.clear_buffer(2, glm.vec4(0, 0, 0, 0))

                if self._transparent_meshes:
                    self.prepare_forward_draw_mesh(False)
                    for mesh, instances in self._transparent_meshes:
                        self.forward_draw_mesh(mesh, instances)

                if self._transparent_lines:
                    self.prepare_forward_draw_lines(False)
                    for mesh, instances in self._transparent_lines:
                        self.forward_draw_lines(mesh, instances)

                if self._transparent_points:
                    self.prepare_forward_draw_points(False)
                    for mesh, instances in self._transparent_points:
                        self.forward_draw_points(mesh, instances)

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
