from glass import GLConfig, ShaderProgram
import importlib

DirLight = None
PointLight = None
SpotLight = None
Material = None
Fog = None

def import_DirLight():
    global DirLight
    if DirLight is None:
        DirLight = importlib.import_module(".Lights.DirLight", "glass_engine").DirLight

def import_PointLight():
    global PointLight
    if PointLight is None:
        PointLight = importlib.import_module(".Lights.PointLight", "glass_engine").PointLight

def import_SpotLight():
    global SpotLight
    if SpotLight is None:
        SpotLight = importlib.import_module(".Lights.SpotLight", "glass_engine").SpotLight

def import_Material():
    global Material
    if Material is None:
        Material = importlib.import_module(".Material", "glass_engine").Material

def import_Fog():
    global Fog
    if Fog is None:
        Fog = importlib.import_module(".Fog", "glass_engine").Fog

class GlassEngineConfig:

    def __init__(self):
        self._has_material_recv_shadows:bool = False
        self._has_material_cast_shadows:bool = False
        self._has_material_recv_fog:bool = False

        self._has_dir_lights:bool = False
        self._has_point_lights:bool = False
        self._has_spot_lights:bool = False

        self._has_dir_lights_generate_shadows:bool = False
        self._has_point_lights_generate_shadows:bool = False
        self._has_spot_lights_generate_shadows:bool = False

        self._has_fog:bool = False

        self._dict = {}
        self._dict["USE_DYNAMIC_ENV_MAPPING"] = False
        self._dict["USE_DIR_LIGHT"] = False
        self._dict["USE_DIR_LIGHT_SHADOW"] = False
        self._dict["USE_POINT_LIGHT"] = False
        self._dict["USE_POINT_LIGHT_SHADOW"] = False
        self._dict["USE_SPOT_LIGHT"] = False
        self._dict["USE_SPOT_LIGHT_SHADOW"] = False
        self._dict["USE_FOG"] = False
        self._dict["USE_SHADING_MODEL_FLAT"] = False
        self._dict["USE_SHADING_MODEL_GOURAUD"] = False
        self._dict["USE_SHADING_MODEL_PHONG"] = False
        self._dict["USE_SHADING_MODEL_PHONG_BLINN"] = False
        self._dict["USE_SHADING_MODEL_TOON"] = False
        self._dict["USE_SHADING_MODEL_OREN_NAYAR"] = False
        self._dict["USE_SHADING_MODEL_MINNAERT"] = False
        self._dict["USE_SHADING_MODEL_COOK_TORRANCE"] = False
        self._dict["USE_SHADING_MODEL_UNLIT"] = False
        self._dict["USE_SHADING_MODEL_FRESNEL"] = False
        self._dict["USE_BINDLESS_TEXTURE"] = False

    def __getitem__(self, name:str):
        return self._dict[name]
    
    def __setitem__(self, name:str, value:bool):
        if name not in self._dict:
            return

        if self._dict[name] == value:
            return
        
        if not value:
            for program in ShaderProgram.all_instances:
                if self.__has_macro(program):
                    return
            self._dict[name] = value
        else:
            self._dict[name] = value
            for program in ShaderProgram.all_instances:
                self.__reload_program(program)
    
    def define_for_program(self, program):
        has_bindless_extension = ("GL_ARB_bindless_texture" in GLConfig.available_extensions)
        for name in self._dict:
            if name in ["USE_DYNAMIC_ENV_MAPPING", "USE_DIR_LIGHT_SHADOW", "USE_POINT_LIGHT_SHADOW", "USE_SPOT_LIGHT_SHADOW"] and \
               not has_bindless_extension:
                program.undef(name)
                continue

            if name == "USE_BINDLESS_TEXTURE":
                if has_bindless_extension:
                    program.define(name, 1)
                else:
                    program.undef(name)
                continue

            if self._dict[name]:
                program.define(name, 1)
            else:
                program.undef(name)

    def __has_macro(self, program):
        for name in program.defines:
            if name in self._dict:
                return True

        return False

    def __reload_program(self, program):
        has_macro = self.__has_macro(program)

        if not has_macro:
            return
        
        self.define_for_program(program)
        program.reload()

    def _update_dynamic_env(self, flag:bool):
        import_Material()

        has_dynamic_env_mapping = flag
        if not flag:
            for material in Material.all_instances:
                if material.dynamic_env_mapping:
                    has_dynamic_env_mapping = True
                    break
        
        self["USE_DYNAMIC_ENV_MAPPING"] = has_dynamic_env_mapping

    def _update_recv_shadows(self, flag:bool):
        import_Material()

        has_material_recv_shadows = flag
        if not flag:
            for material in Material.all_instances:
                if material.recv_shadows:
                    has_material_recv_shadows = True
                    break
        
        if self._has_material_recv_shadows == has_material_recv_shadows:
            return

        self._has_material_recv_shadows = has_material_recv_shadows
        if self._has_material_recv_shadows:
            if self._has_material_cast_shadows:
                if self._has_dir_lights_generate_shadows:
                    self["USE_DIR_LIGHT_SHADOW"] = True
                if self._has_point_lights_generate_shadows:
                    self["USE_POINT_LIGHT_SHADOW"] = True
                if self._has_spot_lights_generate_shadows:
                    self["USE_SPOT_LIGHT_SHADOW"] = True
        else:
            self["USE_DIR_LIGHT_SHADOW"] = False
            self["USE_POINT_LIGHT_SHADOW"] = False
            self["USE_SPOT_LIGHT_SHADOW"] = False

    def _update_cast_shadows(self, flag:bool):
        import_Material()

        has_material_cast_shadows = flag
        if not flag:
            for material in Material.all_instances:
                if material.cast_shadows:
                    has_material_cast_shadows = True
                    break
        
        if self._has_material_cast_shadows == has_material_cast_shadows:
            return

        self._has_material_cast_shadows = has_material_cast_shadows
        if self._has_material_cast_shadows:
            if self._has_material_recv_shadows:
                if self._has_dir_lights_generate_shadows:
                    self["USE_DIR_LIGHT_SHADOW"] = True
                if self._has_point_lights_generate_shadows:
                    self["USE_POINT_LIGHT_SHADOW"] = True
                if self._has_spot_lights_generate_shadows:
                    self["USE_SPOT_LIGHT_SHADOW"] = True
        else:
            self["USE_DIR_LIGHT_SHADOW"] = False
            self["USE_POINT_LIGHT_SHADOW"] = False
            self["UES_SPOT_LIGHT_SHADOW"] = False

    def _update_recv_fog(self, flag:bool):
        import_Material()

        has_material_recv_fog = flag
        if not flag:
            for material in Material.all_instances:
                if material.fog:
                    has_material_recv_fog = True
                    break
        
        if self._has_material_recv_fog == has_material_recv_fog:
            return

        self._has_material_recv_fog = has_material_recv_fog
        if self._has_material_recv_fog:
            if self._has_fog:
                self["USE_FOG"] = True
        else:
            self["USE_FOG"] = False

    def _update_fog(self):
        import_Fog()

        has_fog = False
        for fog in Fog.all_instances:
            if fog.extinction_density > 1E-6 and \
               fog.inscattering_density > 1E-6:
                has_fog = True
                break

        if self._has_fog == has_fog:
            return

        self._has_fog = has_fog
        if self._has_fog:
            if self._has_material_recv_fog:
                self["USE_FOG"] = True
        else:
            self["USE_FOG"] = False

    def _update_dir_lights(self):
        import_DirLight()

        self["USE_DIR_LIGHT"] = bool(DirLight.all_instances)

    def _update_point_lights(self):
        import_PointLight()

        self["USE_POINT_LIGHT"] = bool(PointLight.all_instances)

    def _update_spot_lights(self):
        import_SpotLight()

        self["USE_SPOT_LIGHT"] = bool(SpotLight.all_instances)

    def _update_dir_lights_generate_shadows(self, flag:bool):
        import_DirLight()

        has_dir_lights_generate_shadows = flag
        if not flag:
            for dir_light in DirLight.all_instances:
                if dir_light.generate_shadows:
                    has_dir_lights_generate_shadows = True
                    break

        if self._has_dir_lights_generate_shadows == has_dir_lights_generate_shadows:
            return

        self._has_dir_lights_generate_shadows = has_dir_lights_generate_shadows
        if self._has_dir_lights_generate_shadows:
            if self._has_material_recv_shadows and self._has_material_cast_shadows:
                self["USE_DIR_LIGHT_SHADOW"] = True
        else:
            self["USE_DIR_LIGHT_SHADOW"] = False

    def _update_point_lights_generate_shadows(self, flag:bool):
        import_PointLight()

        has_point_lights_generate_shadows = flag
        if not flag:
            for point_light in DirLight.all_instances:
                if point_light.generate_shadows:
                    has_point_lights_generate_shadows = True
                    break

        if self._has_point_lights_generate_shadows == has_point_lights_generate_shadows:
            return

        self._has_point_lights_generate_shadows = has_point_lights_generate_shadows
        if self._has_point_lights_generate_shadows:
            if self._has_material_recv_shadows and self._has_material_cast_shadows:
                self["USE_POINT_LIGHT_SHADOW"] = True
        else:
            self["USE_POINT_LIGHT_SHADOW"] = False

    def _update_spot_lights_generate_shadows(self, flag:bool):
        import_SpotLight()

        has_spot_lights_generate_shadows = flag
        if not flag:
            for spot_light in DirLight.all_instances:
                if spot_light.generate_shadows:
                    has_spot_lights_generate_shadows = True
                    break

        if self._has_spot_lights_generate_shadows == has_spot_lights_generate_shadows:
            return

        self._has_spot_lights_generate_shadows = has_spot_lights_generate_shadows
        if self._has_spot_lights_generate_shadows:
            if self._has_material_recv_shadows and self._has_material_cast_shadows:
                self["USE_SPOT_LIGHT_SHADOW"] = True
        else:
            self["USE_SPOT_LIGHT_SHADOW"] = False

    def _update_shading_model(self):
        import_Material()

        has_Flat = False
        has_Gouraud = False
        has_Phong = False
        has_PhongBlinn = False
        has_Toon = False
        has_OrenNayar = False
        has_Minnaert = False
        has_CookTorrance = False
        has_Unlit = False
        has_Fresnel = False
        for material in Material.all_instances:
            if material.shading_model == Material.ShadingModel.Flat:
                has_Flat = True

            elif material.shading_model == Material.ShadingModel.Gouraud:
                has_Gouraud = True

            elif material.shading_model == Material.ShadingModel.Phong:
                has_Phong = True

            elif material.shading_model == Material.ShadingModel.PhongBlinn:
                has_PhongBlinn = True

            elif material.shading_model == Material.ShadingModel.Toon:
                has_Toon = True

            elif material.shading_model == Material.ShadingModel.OrenNayar:
                has_OrenNayar = True

            elif material.shading_model == Material.ShadingModel.Minnaert:
                has_Minnaert = True

            elif material.shading_model in [Material.ShadingModel.CookTorrance, Material.ShadingModel.PBR]:
                has_CookTorrance = True

            elif material.shading_model in [Material.ShadingModel.NoShading, Material.ShadingModel.Unlit]:
                has_Unlit = True

            elif material.shading_model == Material.ShadingModel.Fresnel:
                has_Fresnel = True

        self["USE_SHADING_MODEL_FLAT"] = has_Flat
        self["USE_SHADING_MODEL_GOURAUD"] = has_Gouraud
        self["USE_SHADING_MODEL_PHONG"] = has_Phong
        self["USE_SHADING_MODEL_PHONG_BLINN"] = has_PhongBlinn
        self["USE_SHADING_MODEL_TOON"] = has_Toon
        self["USE_SHADING_MODEL_OREN_NAYAR"] = has_OrenNayar
        self["USE_SHADING_MODEL_MINNAERT"] = has_Minnaert
        self["USE_SHADING_MODEL_COOK_TORRANCE"] = has_CookTorrance
        self["USE_SHADING_MODEL_UNLIT"] = has_Unlit
        self["USE_SHADING_MODEL_FRESNEL"] = has_Fresnel

GlassEngineConfig = GlassEngineConfig()