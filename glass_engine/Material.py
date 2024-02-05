from glass.utils import checktype
from glass import sampler2D
from glass.ImageLoader import ImageLoader
from glass.WeakSet import WeakSet
from glass.MetaInstancesRecorder import MetaInstancesRecorder
from .callback_vec import callback_vec3, callback_vec4
from .GlassEngineConfig import GlassEngineConfig

import glm
from enum import Enum
import numpy as np
import math
from functools import wraps


def param_setter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        value = args[1]

        should_test_transparent = False
        if (
            func.__name__
            in [
                "ambient_map",
                "specular_map",
                "emission_map",
                "reflection_map",
                "refractive_index",
                "base_color_map",
            ]
            and not self._opacity_user_set
            and self._opacity == 0
        ):
            self._opacity = 1
            should_test_transparent = True

            for mesh in self._parent_meshes:
                colors = None
                if mesh.material is self:
                    if "color" in mesh.vertices:
                        colors = mesh.vertices["color"].ndarray
                elif mesh._back_material is self:
                    if "back_color" in mesh.vertices:
                        colors = mesh.vertices["back_color"].ndarray

                if colors is not None and (
                    len(colors.shape) != 2 or colors.shape[1] != 4
                ):
                    colors = colors.reshape(-1, 4)

                if (
                    colors is not None
                    and colors.size > 0
                    and np.all(colors == colors[0, :])
                ):
                    used_color = glm.vec3(colors[0, 0], colors[0, 1], colors[0, 2])

                    old_should_callback = self._should_callback
                    self._should_callback = False
                    self.base_color = used_color
                    self._should_callback = old_should_callback

                break

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

        self._update_all_env_maps()
        if func.__name__ == "generate_shadows":
            self._update_all_depth_maps()

        if should_test_transparent:
            self._test_transparent()

        return return_value

    return wrapper


class Material(metaclass=MetaInstancesRecorder):

    class ShadingModel(Enum):
        Flat = 0x1
        Gouraud = 0x2
        Phong = 0x3
        PhongBlinn = 0x4
        Toon = 0x5
        OrenNayar = 0x6
        Minnaert = 0x7
        CookTorrance = 0x8
        NoShading = 0x9
        Unlit = 0x9
        Fresnel = 0xA
        PBR = 0xB

    class Type(Enum):
        Emerald = "翡翠"
        Jade = "玉"
        Obsidian = "黑曜石"
        Pearl = "珍珠"
        Ruby = "红宝石"
        Turquoise = "绿松石"
        Brass = "黄铜"
        Bronze = "青铜"
        Chrome = "铬"
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

    @MetaInstancesRecorder.init
    def __init__(self, name: str = ""):
        self._name: str = name
        self._shading_model: Material.ShadingModel = Material.ShadingModel.PhongBlinn

        self._ambient: callback_vec3 = callback_vec3(
            0, 0, 0, self._color_change_callback
        )
        self._base_color: callback_vec3 = callback_vec3(
            0.396, 0.74151, 0.69102, self._color_change_callback
        )
        self._specular: callback_vec3 = callback_vec3(
            0.3, 0.3, 0.3, self._color_change_callback
        )
        self._shininess: float = 0.6 * 128
        self._shininess_strength: float = 1
        self._emission: callback_vec3 = callback_vec3(
            0, 0, 0, self._color_change_callback
        )
        self._emission_strength: float = 1
        self._opacity: float = 0
        self._height_scale: float = 0.05
        self._metallic: float = 0.5
        self._roughness: float = 0
        self._recv_shadows: bool = True
        self._cast_shadows: bool = True
        self._diffuse_bands: int = 2
        self._specular_bands: int = 2
        self._diffuse_softness: float = 0.05
        self._specular_softness: float = 0.02
        self._rim_power: float = 0.3
        self._fog: bool = True
        self._reflection: callback_vec4 = callback_vec4(
            1, 1, 1, 0, self._color_change_callback
        )
        self._refractive_index: float = 0
        self._env_mix_diffuse: bool = True
        self._env_max_bake_times: int = 2
        self._dynamic_env_mapping: bool = False
        self._auto_update_env_map: bool = False

        self._ambient_map: sampler2D = None
        self._specular_map: sampler2D = None
        self._shininess_map: sampler2D = None
        self._emission_map: sampler2D = None
        self._normal_map: sampler2D = None
        self._height_map: sampler2D = None
        self._opacity_map: sampler2D = None
        self._ao_map: sampler2D = None
        self._reflection_map: sampler2D = None
        self._base_color_map: sampler2D = None
        self._metallic_map: sampler2D = None
        self._roughness_map: sampler2D = None
        self._arm_map: sampler2D = None

        self.arm_use_a: bool = True
        self._opacity_user_set: bool = False
        self._reflection_user_set: bool = False
        self._has_transparent: bool = True
        self._has_opaque: bool = False
        self._parent_meshes: WeakSet = WeakSet()
        self._should_callback: bool = True
        self._prop_name: str = ""

        GlassEngineConfig._update_cast_shadows(self._cast_shadows)
        GlassEngineConfig._update_recv_shadows(self._recv_shadows)
        GlassEngineConfig._update_recv_fog(self._fog)
        GlassEngineConfig._update_dynamic_env(self._dynamic_env_mapping)
        GlassEngineConfig._update_shading_model()

    @MetaInstancesRecorder.delete
    def __del__(self):
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def _color_change_callback(self):
        if not self._should_callback:
            return

        old_should_callback = self._should_callback
        self._should_callback = False

        if self._prop_name == "reflection":
            self._reflection_user_set = True

        if self._prop_name == "ambient":
            if glm.length(self._ambient) < 1e-6:
                self.ambient = glm.vec3(1e-6)

        if not self._opacity_user_set and self._opacity == 0:
            self._opacity = 1
            for mesh in self._parent_meshes:
                colors = None
                if mesh.material is self:
                    if "color" in mesh.vertices:
                        colors = mesh.vertices["color"].ndarray
                elif mesh._back_material is self:
                    if "back_color" in mesh.vertices:
                        colors = mesh.vertices["back_color"].ndarray

                if colors is not None and (
                    len(colors.shape) != 2 or colors.shape[1] != 4
                ):
                    colors = colors.reshape(-1, 4)

                if (
                    colors is not None
                    and colors.size > 0
                    and np.all(colors == colors[0, :])
                ):
                    used_color = glm.vec3(colors[0, 0], colors[0, 1], colors[0, 2])
                    if self._prop_name != "base_color":
                        self.base_color = used_color

                break

        self._update_all_env_maps()
        self._test_transparent()

        self._should_callback = old_should_callback

    @property
    def fog(self) -> bool:
        return self._fog

    @fog.setter
    @param_setter
    def fog(self, fog: bool):
        self._fog = fog
        GlassEngineConfig._update_recv_fog(fog)

    @property
    def diffuse_bands(self) -> int:
        return self._diffuse_bands

    @diffuse_bands.setter
    @param_setter
    def diffuse_bands(self, bands: int):
        self._diffuse_bands = bands

    @property
    def specular_bands(self) -> int:
        return self._specular_bands

    @specular_bands.setter
    @param_setter
    def specular_bands(self, bands: int):
        self._specular_bands = bands

    @property
    def diffuse_softness(self) -> float:
        return self._diffuse_softness

    @diffuse_softness.setter
    @param_setter
    def diffuse_softness(self, softness: float):
        self._diffuse_softness = max(softness, 1e-5)

    @property
    def specular_softness(self) -> float:
        return self._specular_softness

    @specular_softness.setter
    @param_setter
    def specular_softness(self, softness: float):
        self._specular_softness = max(softness, 1e-5)

    @property
    def rim_power(self) -> float:
        return self._rim_power

    @rim_power.setter
    @param_setter
    def rim_power(self, p: float):
        self._rim_power = p

    @property
    def recv_shadows(self):
        return self._recv_shadows

    @recv_shadows.setter
    @param_setter
    def recv_shadows(self, flag: bool):
        self._recv_shadows = flag
        GlassEngineConfig._update_recv_shadows(flag)

    @property
    def cast_shadows(self):
        return self._cast_shadows

    @cast_shadows.setter
    @param_setter
    def cast_shadows(self, flag: bool):
        self._cast_shadows = flag
        GlassEngineConfig._update_cast_shadows(flag)

    @property
    def has_transparent(self):
        return self._has_transparent

    @property
    def has_opaque(self):
        return self._has_opaque

    @property
    def need_env_map(self):
        if self._env_max_bake_times <= 0 or not self._dynamic_env_mapping:
            return False

        has_reflection = False
        if self._reflection_map is None:
            has_reflection = (
                glm.length(self._reflection.rgb * self._reflection.a) > 1e-6
            )
        else:
            has_reflection = True

        if has_reflection:
            return True

    @property
    def auto_update_env_map(self):
        return self._auto_update_env_map

    @auto_update_env_map.setter
    @param_setter
    def auto_update_env_map(self, flag: bool):
        self._auto_update_env_map = flag

    def update_env_map(self):
        for mesh in self._parent_meshes:
            for scene in mesh.scenes:
                for instance in scene._all_meshes[mesh].values():
                    instance.user_data["env_bake_times", scene] = 0

    @property
    def dynamic_env_mapping(self):
        return self._dynamic_env_mapping

    @dynamic_env_mapping.setter
    @param_setter
    def dynamic_env_mapping(self, flag: bool):
        self._dynamic_env_mapping = flag
        GlassEngineConfig._update_dynamic_env(flag)

    @property
    def env_max_bake_times(self):
        return self._env_max_bake_times

    @env_max_bake_times.setter
    @param_setter
    def env_max_bake_times(self, times: int):
        self._env_max_bake_times = times

    @property
    def shading_model(self):
        return self._shading_model

    @shading_model.setter
    @param_setter
    def shading_model(self, shading_model: (ShadingModel, None)):
        if shading_model is None:
            shading_model = Material.ShadingModel.Unlit

        self._shading_model = shading_model
        GlassEngineConfig._update_shading_model()

    @property
    def ambient(self) -> callback_vec3:
        self._prop_name = "ambient"

        return self._ambient

    @ambient.setter
    def ambient(self, ambient: glm.vec3) -> None:
        self._prop_name = "ambient"

        if glm.length(ambient) < 1e-6:
            ambient = glm.vec3(1e-6)

        old_should_callback = self._should_callback
        self._should_callback = False
        self._ambient.r = ambient.r
        self._ambient.g = ambient.g
        self._should_callback = old_should_callback

        self._ambient.b = ambient.b

    @property
    def diffuse(self) -> callback_vec3:
        return self.base_color

    @diffuse.setter
    def diffuse(self, diffuse: glm.vec3) -> None:
        self.base_color = diffuse

    @property
    def specular(self) -> callback_vec3:
        self._prop_name = "specular"

        return self._specular

    @specular.setter
    def specular(self, specular: glm.vec3) -> None:
        self._prop_name = "specular"

        old_should_callback = self._should_callback
        self._should_callback = False
        self._specular.r = specular.r
        self._specular.g = specular.g
        self._should_callback = old_should_callback

        self._specular.b = specular.b

    @property
    def glossiness(self):
        return math.sqrt(self._shininess)

    @glossiness.setter
    @param_setter
    def glossiness(self, glossiness: float):
        self._shininess = glossiness * glossiness

    @property
    def shininess(self):
        return self._shininess

    @shininess.setter
    @param_setter
    def shininess(self, shininess: float):
        self._shininess = shininess

    @property
    def emission_strength(self) -> float:
        return self._emission_strength

    @emission_strength.setter
    @param_setter
    def emission_strength(self, emission_strength: float) -> None:
        self._emission_strength = emission_strength

    @property
    def shininess_strength(self):
        return self._shininess_strength

    @shininess_strength.setter
    @param_setter
    def shininess_strength(self, shininess_strength: float):
        self._shininess_strength = shininess_strength

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    @param_setter
    def opacity(self, opacity: float):
        self._opacity = opacity
        self._opacity_user_set = True

        self._test_transparent()

    @property
    def emission(self) -> callback_vec3:
        self._prop_name = "emission"

        return self._emission

    @emission.setter
    def emission(self, emission: glm.vec3) -> None:
        self._prop_name = "emission"

        old_should_callback = self._should_callback
        self._should_callback = False
        self._emission.r = emission.r
        self._emission.g = emission.g
        self._should_callback = old_should_callback

        self._emission.b = emission.b

    @property
    def env_mix_diffuse(self):
        return self._env_mix_diffuse

    @env_mix_diffuse.setter
    @param_setter
    def env_mix_diffuse(self, flag: bool):
        self._env_mix_diffuse = flag

    @property
    def reflection(self) -> callback_vec4:
        self._prop_name = "reflection"
        return self._reflection

    @reflection.setter
    def reflection(self, reflection: (glm.vec4, glm.vec3, float)) -> None:
        if isinstance(reflection, glm.vec3):
            reflection = glm.vec4(reflection, 1)
        if isinstance(reflection, (float, int)):
            reflection = glm.vec4(1, 1, 1, reflection)

        self._prop_name = "reflection"
        self._reflection_user_set = True

        old_should_callback = self._should_callback
        self._should_callback = False
        self._reflection.r = reflection.r
        self._reflection.g = reflection.g
        self._reflection.b = reflection.b
        self._should_callback = old_should_callback

        self._reflection.a = reflection.a

    @property
    def refractive_index(self):
        return self._refractive_index

    @refractive_index.setter
    @param_setter
    def refractive_index(self, refractive_index: float):
        self._refractive_index = refractive_index

        if not self._reflection_user_set:
            self._reflection = glm.vec4(1, 1, 1, 1)

    @property
    def height_scale(self):
        return self._height_scale

    @height_scale.setter
    @param_setter
    def height_scale(self, distance: float):
        self._height_scale = distance

    @property
    def base_color(self) -> callback_vec3:
        self._prop_name = "base_color"
        return self._base_color

    @base_color.setter
    def base_color(self, base_color: glm.vec3) -> None:
        self._prop_name = "base_color"

        old_should_callback = self._should_callback
        self._should_callback = False
        self._base_color.r = base_color.r
        self._base_color.g = base_color.g
        self._should_callback = old_should_callback

        self._base_color.b = base_color.b

    @property
    def roughness(self):
        return self._roughness

    @roughness.setter
    @param_setter
    def roughness(self, roughness: float):
        self._roughness = roughness

    @property
    def metallic(self):
        return self._metallic

    @metallic.setter
    @param_setter
    def metallic(self, metallic: float):
        self._metallic = metallic

    @property
    def ambient_map(self):
        return self._ambient_map

    @ambient_map.setter
    @param_setter
    def ambient_map(self, ambient_map: (sampler2D, str, np.ndarray)):
        if isinstance(ambient_map, sampler2D) or ambient_map is None:
            self._ambient_map = ambient_map
        elif isinstance(ambient_map, (str, np.ndarray)):
            if isinstance(ambient_map, str):
                ambient_map = ImageLoader.load(ambient_map)
            threshold = 0.5
            image_dtype = ambient_map.dtype
            if "int" in str(image_dtype):
                threshold = 127
            if ambient_map.max() > threshold:
                ambient_map = (0.2 * ambient_map).astype(image_dtype)
            self._ambient_map = sampler2D(ambient_map)

    @property
    def diffuse_map(self):
        return self.base_color_map

    @diffuse_map.setter
    def diffuse_map(self, diffuse_map: (sampler2D, str, np.ndarray)):
        self.base_color_map = diffuse_map

    @property
    def specular_map(self):
        return self._specular_map

    @specular_map.setter
    @param_setter
    def specular_map(self, specular_map: (sampler2D, str, np.ndarray)):
        if isinstance(specular_map, sampler2D) or specular_map is None:
            self._specular_map = specular_map
        elif isinstance(specular_map, (str, np.ndarray)):
            if self._specular_map is None:
                self._specular_map = sampler2D(specular_map)
            else:
                self._specular_map.image = specular_map

    @property
    def shininess_map(self):
        return self._shininess_map

    @shininess_map.setter
    @param_setter
    def shininess_map(self, shininess_map: (sampler2D, str, np.ndarray)):
        if isinstance(shininess_map, sampler2D) or shininess_map is None:
            self._shininess_map = shininess_map
        elif isinstance(shininess_map, (str, np.ndarray)):
            if self._shininess_map is None:
                self._shininess_map = sampler2D(shininess_map)
            else:
                self._shininess_map.image = shininess_map

    @property
    def emission_map(self):
        return self._emission_map

    @emission_map.setter
    @param_setter
    def emission_map(self, emission_map: (sampler2D, str, np.ndarray)):
        if isinstance(emission_map, sampler2D) or emission_map is None:
            self._emission_map = emission_map
        elif isinstance(emission_map, (str, np.ndarray)):
            if self._emission_map is None:
                self._emission_map = sampler2D(emission_map)
            else:
                self._emission_map.image = emission_map

    @property
    def normal_map(self):
        return self._normal_map

    @normal_map.setter
    @param_setter
    def normal_map(self, normal_map: (sampler2D, str, np.ndarray)):
        if isinstance(normal_map, sampler2D) or normal_map is None:
            self._normal_map = normal_map
        elif isinstance(normal_map, (str, np.ndarray)):
            if self._normal_map is None:
                self._normal_map = sampler2D(normal_map)
            else:
                self._normal_map.image = normal_map

    @property
    def height_map(self):
        return self._height_map

    @height_map.setter
    @param_setter
    def height_map(self, height_map: (sampler2D, str, np.ndarray)):
        if isinstance(height_map, sampler2D) or height_map is None:
            self._height_map = height_map
        elif isinstance(height_map, (str, np.ndarray)):
            if self._height_map is None:
                self._height_map = sampler2D(height_map)
            else:
                self._height_map.image = height_map

    @property
    def opacity_map(self):
        return self._opacity_map

    @opacity_map.setter
    @param_setter
    def opacity_map(self, opacity_map: (sampler2D, str, np.ndarray)):
        if isinstance(opacity_map, sampler2D) or opacity_map is None:
            self._opacity_map = opacity_map
        elif isinstance(opacity_map, (str, np.ndarray)):
            if self._opacity_map is None:
                self._opacity_map = sampler2D(opacity_map)
            else:
                self._opacity_map.image = opacity_map

        self._opacity_user_set = True
        self._test_transparent()

    @property
    def ao_map(self):
        return self._ao_map

    @ao_map.setter
    @param_setter
    def ao_map(self, ao_map: (sampler2D, str, np.ndarray)):
        if isinstance(ao_map, sampler2D) or ao_map is None:
            self._ao_map = ao_map
        elif isinstance(ao_map, (str, np.ndarray)):
            if self._ao_map is None:
                self._ao_map = sampler2D(ao_map)
            else:
                self._ao_map.image = ao_map

    @property
    def arm_map(self):
        return self._arm_map

    @arm_map.setter
    @param_setter
    def arm_map(self, arm_map: (sampler2D, str, np.ndarray)):
        if isinstance(arm_map, sampler2D) or arm_map is None:
            self._arm_map = arm_map
        elif isinstance(arm_map, (str, np.ndarray)):
            if self._arm_map is None:
                self._arm_map = sampler2D(arm_map)
            else:
                self._arm_map.image = arm_map

    @property
    def reflection_map(self):
        return self._reflection_map

    @reflection_map.setter
    @param_setter
    def reflection_map(self, reflection_map: (sampler2D, str, np.ndarray)):
        if isinstance(reflection_map, sampler2D) or reflection_map is None:
            self._reflection_map = reflection_map
        elif isinstance(reflection_map, (str, np.ndarray)):
            if self._reflection_map is None:
                self._reflection_map = sampler2D(reflection_map)
            else:
                self._reflection_map.image = reflection_map

        self._reflection_user_set = True

    @property
    def base_color_map(self):
        return self._base_color_map

    @base_color_map.setter
    @param_setter
    def base_color_map(self, base_color_map: (sampler2D, str, np.ndarray)):
        if isinstance(base_color_map, sampler2D) or base_color_map is None:
            self._base_color_map = base_color_map
        elif isinstance(base_color_map, (str, np.ndarray)):
            if self._base_color_map is None:
                self._base_color_map = sampler2D(base_color_map)
            else:
                self._base_color_map.image = base_color_map

    @property
    def metallic_map(self):
        return self._metallic_map

    @metallic_map.setter
    @param_setter
    def metallic_map(self, metallic_map: (sampler2D, str, np.ndarray)):
        if isinstance(metallic_map, sampler2D) or metallic_map is None:
            self._metallic_map = metallic_map
        elif isinstance(metallic_map, (str, np.ndarray)):
            if self._metallic_map is None:
                self._metallic_map = sampler2D(metallic_map)
            else:
                self._metallic_map.image = metallic_map

    @property
    def roughness_map(self):
        return self._roughness_map

    @roughness_map.setter
    @param_setter
    def roughness_map(self, roughness_map: (sampler2D, str, np.ndarray)):
        if isinstance(roughness_map, sampler2D) or roughness_map is None:
            self._roughness_map = roughness_map
        elif isinstance(roughness_map, (str, np.ndarray)):
            if self._roughness_map is None:
                self._roughness_map = sampler2D(roughness_map)
            else:
                self._roughness_map.image = roughness_map

    @checktype
    def set_as(self, type: Type):
        if type == Material.Type.Emerald:
            self.ambient = glm.vec3(0.0215, 0.1745, 0.0215)
            self.diffuse = glm.vec3(0.07568, 0.61424, 0.07568)
            self.specular = glm.vec3(0.633, 0.727811, 0.633)
            self.shininess = 0.6 * 128
        elif type == Material.Type.Jade:
            self.ambient = glm.vec3(0.135, 0.2225, 0.1575)
            self.diffuse = glm.vec3(0.54, 0.89, 0.63)
            self.specular = glm.vec3(0.316228, 0.316228, 0.316228)
            self.shininess = 0.1 * 128
        elif type == Material.Type.Obsidian:
            self.ambient = glm.vec3(0.05375, 0.05, 0.06625)
            self.diffuse = glm.vec3(0.18275, 0.17, 0.22525)
            self.specular = glm.vec3(0.332741, 0.328634, 0.346435)
            self.shininess = 0.3 * 128
        elif type == Material.Type.Pearl:
            self.ambient = glm.vec3(0.25, 0.20725, 0.20725)
            self.diffuse = glm.vec3(1, 0.829, 0.829)
            self.specular = glm.vec3(0.296648, 0.296648, 0.296648)
            self.shininess = 0.088 * 128
        elif type == Material.Type.Ruby:
            self.ambient = glm.vec3(0.1745, 0.01175, 0.01175)
            self.diffuse = glm.vec3(0.61424, 0.04136, 0.04136)
            self.specular = glm.vec3(0.727811, 0.626959, 0.626959)
            self.shininess = 0.6 * 128
        elif type == Material.Type.Turquoise:
            self.ambient = glm.vec3(0.1, 0.18725, 0.1745)
            self.diffuse = glm.vec3(0.396, 0.74151, 0.69102)
            self.specular = glm.vec3(0.297254, 0.30829, 0.306678)
            self.shininess = 0.1 * 128
        elif type == Material.Type.Brass:
            self.ambient = glm.vec3(0.329412, 0.223529, 0.027451)
            self.diffuse = glm.vec3(0.780392, 0.568627, 0.113725)
            self.specular = glm.vec3(0.992157, 0.941176, 0.807843)
            self.shininess = 0.21794872 * 128
        elif type == Material.Type.Bronze:
            self.ambient = glm.vec3(0.2125, 0.1275, 0.054)
            self.diffuse = glm.vec3(0.714, 0.4284, 0.18144)
            self.specular = glm.vec3(0.393548, 0.271906, 0.166721)
            self.shininess = 0.2 * 128
        elif type == Material.Type.Chrome:
            self.ambient = glm.vec3(0.25, 0.25, 0.25)
            self.diffuse = glm.vec3(0.4, 0.4, 0.4)
            self.specular = glm.vec3(0.774597, 0.774597, 0.774597)
            self.shininess = 0.6 * 128
        elif type == Material.Type.Copper:
            self.ambient = glm.vec3(0.19125, 0.0735, 0.0225)
            self.diffuse = glm.vec3(0.7038, 0.27048, 0.0828)
            self.specular = glm.vec3(0.256777, 0.137622, 0.086014)
            self.shininess = 0.1 * 128
        elif type == Material.Type.Gold:
            self.ambient = glm.vec3(0.24725, 0.1995, 0.0745)
            self.diffuse = glm.vec3(0.75164, 0.60648, 0.22648)
            self.specular = glm.vec3(0.628281, 0.555802, 0.366065)
            self.shininess = 0.4 * 128
        elif type == Material.Type.Silver:
            self.ambient = glm.vec3(0.19225, 0.19225, 0.19225)
            self.diffuse = glm.vec3(0.50754, 0.50754, 0.50754)
            self.specular = glm.vec3(0.508273, 0.508273, 0.508273)
            self.shininess = 0.4 * 128
        elif type == Material.Type.BlackPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.01, 0.01, 0.01)
            self.specular = glm.vec3(0.50, 0.50, 0.50)
            self.shininess = 0.25 * 128
        elif type == Material.Type.CyanPlastic:
            self.ambient = glm.vec3(0.0, 0.1, 0.06)
            self.diffuse = glm.vec3(0.0, 0.50980392, 0.50980392)
            self.specular = glm.vec3(0.50196078, 0.50196078, 0.50196078)
            self.shininess = 0.25 * 128
        elif type == Material.Type.GreenPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.1, 0.35, 0.1)
            self.specular = glm.vec3(0.45, 0.55, 0.45)
            self.shininess = 0.25 * 128
        elif type == Material.Type.RedPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.5, 0.0, 0.0)
            self.specular = glm.vec3(0.7, 0.6, 0.6)
            self.shininess = 0.25 * 128
        elif type == Material.Type.WhitePlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.55, 0.55, 0.55)
            self.specular = glm.vec3(0.70, 0.70, 0.70)
            self.shininess = 0.25 * 128
        elif type == Material.Type.YellowPlastic:
            self.ambient = glm.vec3(0.0, 0.0, 0.0)
            self.diffuse = glm.vec3(0.5, 0.5, 0.0)
            self.specular = glm.vec3(0.60, 0.60, 0.50)
            self.shininess = 0.25 * 128
        elif type == Material.Type.BlackRubber:
            self.ambient = glm.vec3(0.02, 0.02, 0.02)
            self.diffuse = glm.vec3(0.01, 0.01, 0.01)
            self.specular = glm.vec3(0.4, 0.4, 0.4)
            self.shininess = 0.078125 * 128
        elif type == Material.Type.CyanRubber:
            self.ambient = glm.vec3(0.0, 0.05, 0.05)
            self.diffuse = glm.vec3(0.4, 0.5, 0.5)
            self.specular = glm.vec3(0.04, 0.7, 0.7)
            self.shininess = 0.078125 * 128
        elif type == Material.Type.GreenRubber:
            self.ambient = glm.vec3(0.0, 0.05, 0.0)
            self.diffuse = glm.vec3(0.4, 0.5, 0.4)
            self.specular = glm.vec3(0.04, 0.7, 0.04)
            self.shininess = 0.078125 * 128
        elif type == Material.Type.RedRubber:
            self.ambient = glm.vec3(0.05, 0.0, 0.0)
            self.diffuse = glm.vec3(0.5, 0.4, 0.4)
            self.specular = glm.vec3(0.7, 0.04, 0.04)
            self.shininess = 0.078125 * 128
        elif type == Material.Type.WhiteRubber:
            self.ambient = glm.vec3(0.05, 0.05, 0.05)
            self.diffuse = glm.vec3(0.5, 0.5, 0.5)
            self.specular = glm.vec3(0.7, 0.7, 0.7)
            self.shininess = 0.078125 * 128
        elif type == Material.Type.YellowRubber:
            self.ambient = glm.vec3(0.05, 0.05, 0.0)
            self.diffuse = glm.vec3(0.5, 0.5, 0.4)
            self.specular = glm.vec3(0.7, 0.7, 0.04)
            self.shininess = 0.078125 * 128

    def _update_all_depth_maps(self):
        for mesh in self._parent_meshes:
            for scene in mesh.scenes:
                scene._should_update_depth_maps = True

    def _update_all_env_maps(self):
        for mesh in self._parent_meshes:
            for scene in mesh.scenes:
                scene._should_update_env_maps = True

    def _test_transparent(self):
        self._has_transparent = False
        self._has_opaque = False
        if self.opacity_map is not None:
            image = self.opacity_map.image
            if image is None:
                self._has_transparent = True
                self._has_opaque = True
            else:
                if "int" in str(image.dtype):
                    self._has_transparent = np.any(image < 255)
                    self._has_opaque = np.any(image >= 255)
                else:
                    self._has_transparent = np.any(image < 1 - 1e-6)
                    self._has_opaque = np.any(image >= 1 - 1e-6)
        else:
            self._has_transparent = self.opacity < 1 - 1e-6
            self._has_opaque = self.opacity >= 1 - 1e-6

        if self.diffuse_map is not None:
            image = self.diffuse_map.image
            if image is None:
                self._has_transparent = True
                self._has_opaque = True
            elif len(image.shape) > 2 and image.shape[2] > 3:
                if "int" in str(image.dtype):
                    self._has_transparent = (
                        np.any(image[:, :, 3] < 255) or self._has_transparent
                    )
                    self._has_opaque = (
                        np.any(image[:, :, 3] >= 255) and self._has_opaque
                    )
                else:
                    self._has_transparent = (
                        np.any(image[:, :, 3] < 1 - 1e-6) or self._has_transparent
                    )
                    self._has_opaque = (
                        np.any(image[:, :, 3] >= 1 - 1e-6) and self._has_opaque
                    )

        for mesh in self._parent_meshes:
            mesh._test_transparent()
