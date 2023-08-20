from glass.utils import checktype
from glass import sampler2D

import glm
from enum import Enum
import numpy as np
from functools import wraps

class Material():

    class ShadingModel(Enum):
        Flat = 0x1
        Gouraud = 0x2
        Phong = 0x3
        PhongBlinn = 0x4
        Toon = 0x5 # undefined
        OrenNayar = 0x6 # undefined
        Minnaert = 0x7 # undefined
        CookTorrance = 0x8
        NoShading = 0x9
        Unlit = 0x9
        Fresnel = 0xa # undefined
        PBR = 0xb

    class Type(Enum):
        Emerald = "翡翠"
        Jade = "玉"
        Obsidian = "黑曜石"
        Pearl = "珍珠"
        Ruby = "红宝石"
        Turquoise = "绿松石"
        Brass = "黄铜"
        Bronze = "青铜"
        Chrome = "铬合金"
        Copper = "铜"
        Gold = "金"
        Silver = "银"
        BlackPlastic = "黑色塑料"
        CyanPlastic = "青色塑料"
        GreenPlastic = "绿色塑料"
        RedPlastic = "红色塑料"
        WhitePlastic = "白色塑料"
        YellowPlastic = "黄色塑料"
        BlackRubber = "黑色橡胶"
        CyanRubber = "青色橡胶"
        GreenRubber = "绿色橡胶"
        RedRubber = "红色橡胶"
        WhiteRubber = "白色橡胶"
        YellowRubber = "黄色橡胶"
        
        def __init__(self, ch_name):
            self.ch_name = ch_name

    def __init__(self):
        self.__ambient = glm.vec3(0.1, 0.1, 0.1)
        self.__diffuse = glm.vec3(0.5, 0.5, 0.5)
        self.__specular = glm.vec3(0.3, 0.3, 0.3)
        self.__shininess = 0.6
        self.__emission = glm.vec3(0, 0, 0)
        self.__reflection = glm.vec4(0, 0, 0, 0)
        self.__refraction = glm.vec4(0, 0, 0, 0)
        self.__refractive_index = 0
        self._opacity = 0
        self.__height_scale = 0.05
        self.__env_mix_diffuse = True
        self.__albedo = glm.vec3(0.5, 0.5, 0.5)
        self.__metallic = 0.5
        self.__roughness = 0.5
        self.__recv_shadows = True
        self.__cast_shadows = True

        self.__ambient_map = None
        self.__diffuse_map = None
        self.__specular_map = None
        self.__shininess_map = None
        self.__emission_map = None
        self.__normal_map = None
        self.__height_map = None
        self._opacity_map = None
        self.__ambient_occlusion_map = None
        self.__reflection_map = None
        self.__refraction_map = None
        self.__refractive_index_map = None
        self.__albedo_map = None
        self.__metallic_map = None
        self.__roughness_map = None

        self.__shading_model = Material.ShadingModel.PhongBlinn

        self._opacity_user_set = False
        self.__reflection_user_set = False
        self.__refraction_user_set = False
        self.__refractive_index_user_set = False
        self.__env_max_bake_times = 2
        self.__dynamic_env_mapping = False
        self.__auto_update_env_map = False
        self.__has_transparent = True
        self.__has_opaque = False

        self._parent_meshes = set()

    @staticmethod
    def param_setter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            value = args[1]

            if not self._opacity_user_set:
                if self._opacity != 1:
                    self._opacity = 1
                    self._test_transparent()

            equal = False
            try:
                lvalue = getattr(self, func.__name__)
                if type(lvalue) != type(value):
                    equal = False
                else:
                    equal = bool(getattr(self, func.__name__) == value)
            except:
                equal = False

            if equal:
                return

            safe_func = checktype(func)
            return_value = safe_func(*args, **kwargs)

            return return_value

        return wrapper

    @property
    def recv_shadows(self):
        return self.__recv_shadows
    
    @recv_shadows.setter
    @param_setter
    def recv_shadows(self, flag:bool):
        self.__recv_shadows = flag

    @property
    def cast_shadows(self):
        return self.__cast_shadows
    
    @cast_shadows.setter
    @param_setter
    def cast_shadows(self, flag:bool):
        self.__cast_shadows = flag

    @property
    def has_transparent(self):
        return self.__has_transparent
    
    @property
    def has_opaque(self):
        return self.__has_opaque

    @property
    def need_env_map(self):
        if self.__env_max_bake_times <= 0 or not self.__dynamic_env_mapping:
            return False

        has_reflection = False
        if self.__reflection_map is None:
            has_reflection = (glm.length(self.__reflection) > 0)
        else:
            has_reflection = True

        if has_reflection:
            return True

        if self.__refraction_map is None:
            return (glm.length(self.__refraction) > 0)
        else:
            return True
    
    @property
    def auto_update_env_map(self):
        return self.__auto_update_env_map
    
    @auto_update_env_map.setter
    @param_setter
    def auto_update_env_map(self, flag:bool):
        self.__auto_update_env_map = flag
    
    def update_env_map(self):
        for mesh in self._parent_meshes:
            for scene in mesh.scenes:
                for instance in scene._all_meshes[mesh].values():
                    instance.user_data["env_bake_times", scene] = 0

    @property
    def dynamic_env_mapping(self):
        return self.__dynamic_env_mapping
    
    @dynamic_env_mapping.setter
    @param_setter
    def dynamic_env_mapping(self, flag:bool):
        self.__dynamic_env_mapping = flag

    @property
    def env_max_bake_times(self):
        return self.__env_max_bake_times
    
    @env_max_bake_times.setter
    @param_setter
    def env_max_bake_times(self, times:int):
        self.__env_max_bake_times = times

    @property
    def shading_model(self):
        return self.__shading_model
    
    @shading_model.setter
    @param_setter
    def shading_model(self, shading_model:ShadingModel):
        self.__shading_model = shading_model

    @property
    def ambient(self):
        return self.__ambient
    
    @ambient.setter
    @param_setter
    def ambient(self, ambient:(glm.vec3,float)):
        if isinstance(ambient, glm.vec3):
            self.__ambient = ambient
        elif isinstance(ambient, (float,int)):
            self.__ambient = glm.vec3(ambient, ambient, ambient)

    @property
    def diffuse(self):
        return self.__diffuse
    
    @diffuse.setter
    @param_setter
    def diffuse(self, diffuse:(glm.vec3,float)):
        if isinstance(diffuse, glm.vec3):
            self.__diffuse = diffuse
        elif isinstance(diffuse, (float,int)):
            self.__diffuse = glm.vec3(diffuse, diffuse, diffuse)

    @property
    def specular(self):
        return self.__specular
    
    @specular.setter
    @param_setter
    def specular(self, specular:(glm.vec3,float)):
        if isinstance(specular, glm.vec3):
            self.__specular = specular
        elif isinstance(specular, (float,int)):
            self.__specular = glm.vec3(specular, specular, specular)

    @property
    def shininess(self):
        return self.__shininess
    
    @shininess.setter
    @param_setter
    def shininess(self, shininess:float):
        self.__shininess = shininess

    @property
    def opacity_user_set(self):
        return self._opacity_user_set

    @property
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    @param_setter
    def opacity(self, opacity:float):
        self._opacity = opacity
        self._opacity_user_set = True

        self._test_transparent()

    @property
    def emission(self):
        return self.__emission
    
    @emission.setter
    @param_setter
    def emission(self, emission:glm.vec3):
        self.__emission = emission

    @property
    def env_mix_diffuse(self):
        return self.__env_mix_diffuse
    
    @env_mix_diffuse.setter
    @param_setter
    def env_mix_diffuse(self, flag:bool):
        self.__env_mix_diffuse = flag

    @property
    def reflection(self):
        return self.__reflection
    
    @reflection.setter
    @param_setter
    def reflection(self, reflection:(glm.vec4,glm.vec3,float)):
        if isinstance(reflection, glm.vec3):
            reflection = glm.vec4(reflection, 1)
        if isinstance(reflection, (float,int)):
            reflection = glm.vec4(1,1,1,reflection)

        self.__reflection = reflection
        self.__reflection_user_set = True

    @property
    def refraction(self):
        return self.__refraction
    
    @refraction.setter
    @param_setter
    def refraction(self, refraction:(glm.vec4,glm.vec3,float)):
        if isinstance(refraction, glm.vec3):
            refraction = glm.vec4(refraction, 1)
        if isinstance(refraction, (float,int)):
            refraction = glm.vec4(1, 1, 1, refraction)

        self.__refraction = refraction

        if not self.__reflection_user_set:
            self.__reflection = self.__refraction

        if not self.__refractive_index_user_set:
            self.__refractive_index = 1.5

        self.__refraction_user_set = True

    @property
    def refractive_index(self):
        return self.__refractive_index
    
    @refractive_index.setter
    @param_setter
    def refractive_index(self, refractive_index:float):
        self.__refractive_index = refractive_index

        if not self.__reflection_user_set:
            self.__reflection = glm.vec4(1, 1, 1, 1)

        if not self.__refraction_user_set:
            self.__refraction = glm.vec4(1, 1, 1, 1)

        self.__refractive_index_user_set = True

    @property
    def height_scale(self):
        return self.__height_scale
    
    @height_scale.setter
    @param_setter
    def height_scale(self, distance:float):
        self.__height_scale = distance

    @property
    def albedo(self):
        return self.__albedo
    
    @albedo.setter
    @param_setter
    def albedo(self, albedo:glm.vec3):
        self.__albedo = albedo

    @property
    def roughness(self):
        return self.__roughness
    
    @roughness.setter
    @param_setter
    def roughness(self, roughness:float):
        self.__roughness = roughness

    @property
    def metallic(self):
        return self.__metallic
    
    @metallic.setter
    @param_setter
    def metallic(self, metallic:float):
        self.__metallic = metallic

    @property
    def ambient_map(self):
        return self.__ambient_map
    
    @ambient_map.setter
    @param_setter
    def ambient_map(self, ambient_map:(sampler2D,str)):
        if isinstance(ambient_map, sampler2D) or ambient_map is None:
            self.__ambient_map = ambient_map
        elif isinstance(ambient_map, str):
            if self.__ambient_map is None:
                self.__ambient_map = sampler2D(ambient_map)
            else:
                self.__ambient_map.image = ambient_map

    @property
    def diffuse_map(self):
        return self.__diffuse_map
    
    @diffuse_map.setter
    @param_setter
    def diffuse_map(self, diffuse_map:(sampler2D,str,np.ndarray)):
        if isinstance(diffuse_map, sampler2D) or diffuse_map is None:
            self.__diffuse_map = diffuse_map
        elif isinstance(diffuse_map, (str,np.ndarray)):
            if self.__diffuse_map is None:
                self.__diffuse_map = sampler2D(diffuse_map)
            else:
                self.__diffuse_map.image = diffuse_map

        self._test_transparent()

    @property
    def specular_map(self):
        return self.__specular_map
    
    @specular_map.setter
    @param_setter
    def specular_map(self, specular_map:(sampler2D,str,np.ndarray)):
        if isinstance(specular_map, sampler2D) or specular_map is None:
            self.__specular_map = specular_map
        elif isinstance(specular_map, (str,np.ndarray)):
            if self.__specular_map is None:
                self.__specular_map = sampler2D(specular_map)
            else:
                self.__specular_map.image = specular_map

    @property
    def shininess_map(self):
        return self.__shininess_map
    
    @shininess_map.setter
    @param_setter
    def shininess_map(self, shininess_map:(sampler2D,str,np.ndarray)):
        if isinstance(shininess_map, sampler2D) or shininess_map is None:
            self.__shininess_map = shininess_map
        elif isinstance(shininess_map, (str,np.ndarray)):
            if self.__shininess_map is None:
                self.__shininess_map = sampler2D(shininess_map)
            else:
                self.__shininess_map.image = shininess_map

    @property
    def emission_map(self):
        return self.__emission_map
    
    @emission_map.setter
    @param_setter
    def emission_map(self, emission_map:(sampler2D,str,np.ndarray)):
        if isinstance(emission_map, sampler2D) or emission_map is None:
            self.__emission_map = emission_map
        elif isinstance(emission_map, (str,np.ndarray)):
            if self.__emission_map is None:
                self.__emission_map = sampler2D(emission_map)
            else:
                self.__emission_map.image = emission_map

    @property
    def normal_map(self):
        return self.__normal_map

    @normal_map.setter
    @param_setter
    def normal_map(self, normal_map:(sampler2D,str,np.ndarray)):
        if isinstance(normal_map, sampler2D) or normal_map is None:
            self.__normal_map = normal_map
        elif isinstance(normal_map, (str,np.ndarray)):
            if self.__normal_map is None:
                self.__normal_map = sampler2D(normal_map)
            else:
                self.__normal_map.image = normal_map

    @property
    def height_map(self):
        return self.__height_map
    
    @height_map.setter
    @param_setter
    def height_map(self, height_map:(sampler2D,str,np.ndarray)):
        if isinstance(height_map, sampler2D) or height_map is None:
            self.__height_map = height_map
        elif isinstance(height_map, (str,np.ndarray)):
            if self.__height_map is None:
                self.__height_map = sampler2D(height_map)
            else:
                self.__height_map.image = height_map

    @property
    def opacity_map(self):
        return self._opacity_map
    
    @opacity_map.setter
    @param_setter
    def opacity_map(self, opacity_map:(sampler2D,str,np.ndarray)):
        if isinstance(opacity_map, sampler2D) or opacity_map is None:
            self._opacity_map = opacity_map
        elif isinstance(opacity_map, (str,np.ndarray)):
            if self._opacity_map is None:
                self._opacity_map = sampler2D(opacity_map)
            else:
                self._opacity_map.image = opacity_map

        self._opacity_user_set = True
        self._test_transparent()

    @property
    def ambient_occlusion_map(self):
        return self.__ambient_occlusion_map
    
    @ambient_occlusion_map.setter
    @param_setter
    def ambient_occlusion_map(self, ambient_occlusion_map:(sampler2D,str,np.ndarray)):
        if isinstance(ambient_occlusion_map, sampler2D) or ambient_occlusion_map is None:
            self.__ambient_occlusion_map = ambient_occlusion_map
        elif isinstance(ambient_occlusion_map, (str,np.ndarray)):
            if self.__ambient_occlusion_map is None:
                self.__ambient_occlusion_map = sampler2D(ambient_occlusion_map)
            else:
                self.__ambient_occlusion_map.image = ambient_occlusion_map

    @property
    def reflection_map(self):
        return self.__reflection_map
    
    @reflection_map.setter
    @param_setter
    def reflection_map(self, reflection_map:(sampler2D,str,np.ndarray)):
        if isinstance(reflection_map, sampler2D) or reflection_map is None:
            self.__reflection_map = reflection_map
        elif isinstance(reflection_map, (str,np.ndarray)):
            if self.__reflection_map is None:
                self.__reflection_map = sampler2D(reflection_map)
            else:
                self.__reflection_map.image = reflection_map

        self.__reflection_user_set = True

    @property
    def refraction_map(self):
        return self.__refraction_map
    
    @refraction_map.setter
    @param_setter
    def refraction_map(self, refraction_map:(sampler2D,str,np.ndarray)):
        if isinstance(refraction_map, sampler2D) or refraction_map is None:
            self.__refraction_map = refraction_map
        elif isinstance(refraction_map, (str,np.ndarray)):
            if self.__refraction_map is None:
                self.__refraction_map = sampler2D(refraction_map)
            else:
                self.__refraction_map.image = refraction_map

        if not self.__reflection_user_set:
            self.__reflection = glm.vec4(1, 1, 1, 1)

        if not self.__refractive_index_user_set:
            self.__refractive_index = 1.5

        self.__refraction_user_set = True

    @property
    def refractive_index_map(self):
        return self.__refractive_index_map
    
    @refractive_index_map.setter
    @param_setter
    def refractive_index_map(self, refractive_index_map:(sampler2D,str,np.ndarray)):
        if isinstance(refractive_index_map, sampler2D) or refractive_index_map is None:
            self.__refractive_index_map = refractive_index_map
        elif isinstance(refractive_index_map, (str,np.ndarray)):
            if self.__refractive_index_map is None:
                self.__refractive_index_map = sampler2D(refractive_index_map)
            else:
                self.__refractive_index_map.image = refractive_index_map

        if not self.__reflection_user_set:
            self.__reflection = glm.vec4(1, 1, 1, 1)

        if not self.__refraction_user_set:
            self.__refraction = glm.vec4(1, 1, 1, 1)

        self.__refractive_index_user_set = True

    @property
    def albedo_map(self):
        return self.__albedo_map
    
    @albedo_map.setter
    @param_setter
    def albedo_map(self, albedo_map:(sampler2D,str,np.ndarray)):
        if isinstance(albedo_map, sampler2D) or albedo_map is None:
            self.__albedo_map = albedo_map
        elif isinstance(albedo_map, (str,np.ndarray)):
            if self.__albedo_map is None:
                self.__albedo_map = sampler2D(albedo_map)
            else:
                self.__albedo_map.image = albedo_map

    @property
    def metallic_map(self):
        return self.__metallic_map
    
    @metallic_map.setter
    @param_setter
    def metallic_map(self, metallic_map:(sampler2D,str,np.ndarray)):
        if isinstance(metallic_map, sampler2D) or metallic_map is None:
            self.__metallic_map = metallic_map
        elif isinstance(metallic_map, (str,np.ndarray)):
            if self.__metallic_map is None:
                self.__metallic_map = sampler2D(metallic_map)
            else:
                self.__metallic_map.image = metallic_map

    @property
    def roughness_map(self):
        return self.__roughness_map
    
    @roughness_map.setter
    @param_setter
    def roughness_map(self, roughness_map:(sampler2D,str,np.ndarray)):
        if isinstance(roughness_map, sampler2D) or roughness_map is None:
            self.__roughness_map = roughness_map
        elif isinstance(roughness_map, (str,np.ndarray)):
            if self.__roughness_map is None:
                self.__roughness_map = sampler2D(roughness_map)
            else:
                self.__roughness_map.image = roughness_map

    @property
    def use_ambient_map(self):
        return (self.__ambient_map is not None)

    @property
    def use_diffuse_map(self):
        return (self.__diffuse_map is not None)

    @property
    def use_specular_map(self):
        return (self.__specular_map is not None)

    @property
    def use_shininess_map(self):
        return (self.__shininess_map is not None)

    @property
    def use_emission_map(self):
        return (self.__emission_map is not None)

    @property
    def use_normal_map(self):
        return (self.__normal_map is not None)

    @property
    def use_height_map(self):
        return (self.__height_map is not None)

    @property
    def use_opacity_map(self):
        return (self._opacity_map is not None)

    @property
    def use_ambient_occlusion_map(self):
        return (self.__ambient_occlusion_map is not None)

    @property
    def use_reflection_map(self):
        return (self.__reflection_map is not None)

    @property
    def use_refraction_map(self):
        return (self.__refraction_map is not None)

    @property
    def use_refractive_index_map(self):
        return (self.__refractive_index_map is not None)
    
    @property
    def use_albedo_map(self):
        return (self.__albedo_map is not None)
    
    @property
    def use_metallic_map(self):
        return (self.__metallic_map is not None)
    
    @property
    def use_roughness_map(self):
        return (self.__roughness_map is not None)

    @checktype
    def set_as(self, type:Type):
        if type == Material.Type.Emerald:
            self.ambient = glm.vec3(0.0215, 0.1745, 0.0215)
            self.diffuse = glm.vec3(0.07568, 0.61424, 0.07568)
            self.specular = glm.vec3(0.633, 0.727811, 0.633)
            self.shininess = 0.6
        elif type == Material.Type.Jade:
            self.ambient = glm.vec3(0.135, 0.2225, 0.1575)
            self.diffuse = glm.vec3(0.54, 0.89, 0.63)
            self.specular = glm.vec3(0.316228, 0.316228, 0.316228)
            self.shininess = 0.1
        elif type == Material.Type.Obsidian:
            self.ambient = glm.vec3(0.05375, 0.05, 0.06625)
            self.diffuse = glm.vec3(0.18275, 0.17, 0.22525)
            self.specular = glm.vec3(0.332741, 0.328634, 0.346435)
            self.shininess = 0.3
        elif type == Material.Type.Pearl:
            self.ambient = glm.vec3(0.25, 0.20725, 0.20725)
            self.diffuse = glm.vec3(1, 0.829, 0.829)
            self.specular = glm.vec3(0.296648, 0.296648, 0.296648)
            self.shininess = 0.088
        elif type == Material.Type.Ruby:
            self.ambient = glm.vec3(0.1745, 0.01175, 0.01175)
            self.diffuse = glm.vec3(0.61424, 0.04136, 0.04136)
            self.specular = glm.vec3(0.727811, 0.626959, 0.626959)
            self.shininess = 0.6
        elif type == Material.Type.Turquoise:
            self.ambient = glm.vec3(0.1, 0.18725, 0.1745)
            self.diffuse = glm.vec3(0.396, 0.74151, 0.69102)
            self.specular = glm.vec3(0.297254, 0.30829, 0.306678)
            self.shininess = 0.1
        elif type == Material.Type.Brass:
            self.ambient = glm.vec3(0.329412, 0.223529, 0.027451)
            self.diffuse = glm.vec3(0.780392, 0.568627, 0.113725)
            self.specular = glm.vec3(0.992157, 0.941176, 0.807843)
            self.shininess = 0.21794872
        elif type == Material.Type.Bronze:
            self.ambient = glm.vec3(0.2125, 0.1275, 0.054)
            self.diffuse = glm.vec3(0.714, 0.4284, 0.18144)
            self.specular = glm.vec3(0.393548, 0.271906, 0.166721)
            self.shininess = 0.2
        elif type == Material.Type.Chrome:
            self.ambient = glm.vec3(0.25, 0.25, 0.25)
            self.diffuse = glm.vec3(0.4, 0.4, 0.4)
            self.specular = glm.vec3(0.774597, 0.774597, 0.774597)
            self.shininess = 0.6
        elif type == Material.Type.Copper:
            self.ambient = glm.vec3(0.19125, 0.0735, 0.0225)
            self.diffuse = glm.vec3(0.7038, 0.27048, 0.0828)
            self.specular = glm.vec3(0.256777, 0.137622, 0.086014)
            self.shininess = 0.1
        elif type == Material.Type.Gold:
            self.ambient = glm.vec3(0.24725, 0.1995, 0.0745)
            self.diffuse = glm.vec3(0.75164, 0.60648, 0.22648)
            self.specular = glm.vec3(0.628281, 0.555802, 0.366065)
            self.shininess = 0.4
        elif type == Material.Type.Silver:
            self.ambient = glm.vec3(0.19225, 0.19225, 0.19225)
            self.diffuse = glm.vec3(0.50754, 0.50754, 0.50754)
            self.specular = glm.vec3(0.508273, 0.508273, 0.508273)
            self.shininess = 0.4
        elif type == Material.Type.BlackPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.01, 0.01, 0.01)
            self.specular = glm.vec3(0.50, 0.50, 0.50)
            self.shininess = 0.25
        elif type == Material.Type.CyanPlastic:
            self.ambient = glm.vec3(0.0, 0.1, 0.06)
            self.diffuse = glm.vec3(0.0, 0.50980392, 0.50980392)
            self.specular = glm.vec3(0.50196078, 0.50196078, 0.50196078)
            self.shininess = 0.25
        elif type == Material.Type.GreenPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.1, 0.35, 0.1)
            self.specular = glm.vec3(0.45, 0.55, 0.45)
            self.shininess = 0.25
        elif type == Material.Type.RedPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.5, 0.0, 0.0)
            self.specular = glm.vec3(0.7, 0.6, 0.6)
            self.shininess = 0.25
        elif type == Material.Type.WhitePlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.55, 0.55, 0.55)
            self.specular = glm.vec3(0.70, 0.70, 0.70)
            self.shininess = 0.25
        elif type == Material.Type.YellowPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.5, 0.5, 0.0)
            self.specular = glm.vec3(0.60, 0.60, 0.50)
            self.shininess = 0.25
        elif type == Material.Type.BlackRubber:
            self.ambient = glm.vec3(0.02, 0.02, 0.02)
            self.diffuse = glm.vec3(0.01, 0.01, 0.01)
            self.specular = glm.vec3(0.4, 0.4, 0.4)
            self.shininess = 0.078125
        elif type == Material.Type.CyanRubber:
            self.ambient = glm.vec3(0.0, 0.05, 0.05)
            self.diffuse = glm.vec3(0.4, 0.5, 0.5)
            self.specular = glm.vec3(0.04, 0.7, 0.7)
            self.shininess = 0.078125
        elif type == Material.Type.GreenRubber:
            self.ambient = glm.vec3(0.0, 0.05, 0.0)
            self.diffuse = glm.vec3(0.4, 0.5, 0.4)
            self.specular = glm.vec3(0.04, 0.7, 0.04)
            self.shininess = 0.078125
        elif type == Material.Type.RedRubber:
            self.ambient = glm.vec3(0.05, 0.0, 0.0)
            self.diffuse = glm.vec3(0.5, 0.4, 0.4)
            self.specular = glm.vec3(0.7, 0.04, 0.04)
            self.shininess = 0.078125
        elif type == Material.Type.WhiteRubber:
            self.ambient = glm.vec3(0.05, 0.05, 0.05)
            self.diffuse = glm.vec3(0.5, 0.5, 0.5)
            self.specular = glm.vec3(0.7, 0.7, 0.7)
            self.shininess = 0.078125
        elif type == Material.Type.YellowRubber:
            self.ambient = glm.vec3(0.05, 0.05, 0.0)
            self.diffuse = glm.vec3(0.5, 0.5, 0.4)
            self.specular = glm.vec3(0.7, 0.7, 0.04)
            self.shininess = 0.078125

    @staticmethod
    @checktype
    def create(type:Type):
        material = Material()
        material.set_as(type)
        return material
    
    def _test_transparent(self):
        self.__has_transparent = False
        self.__has_opaque = False
        if self.use_opacity_map:
            image = self.opacity_map.image
            if "int" in image.dtype.__name__:
                self.__has_transparent = np.any(image < 255)
                self.__has_opaque = np.any(image >= 255)
            else:
                self.__has_transparent = np.any(image < 1-1E-6)
                self.__has_opaque = np.any(image >= 1-1E-6)
        else:
            self.__has_transparent = self.opacity < 1-1E-6
            self.__has_opaque = self.opacity >= 1-1E-6

        if self.use_diffuse_map:
            image = self.diffuse_map.image
            if len(image.shape) == 2:
                return
            
            if image.shape[2] < 4:
                return
            
            if "int" in image.dtype.__name__:
                self.__has_transparent = np.any(image[:,:,3] < 255) or self.__has_transparent
                self.__has_opaque = np.any(image[:,:,3] >= 255) and self.__has_opaque
            else:
                self.__has_transparent = np.any(image[:,:,3] < 1-1E-6) or self.__has_transparent
                self.__has_opaque = np.any(image[:,:,3] >= 1-1E-6) and self.__has_opaque

        for mesh in self._parent_meshes:
            mesh._test_transparent()
