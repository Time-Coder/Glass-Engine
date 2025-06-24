import os
import subprocess


defines = [
    "USE_DYNAMIC_ENV_MAPPING",
    "USE_DIR_LIGHT",
    "USE_DIR_LIGHT_SHADOW",
    "USE_POINT_LIGHT",
    "USE_POINT_LIGHT_SHADOW",
    "USE_SPOT_LIGHT",
    "USE_SPOT_LIGHT_SHADOW",
    "USE_FOG",
    "USE_SHADING_MODEL_FLAT",
    "USE_SHADING_MODEL_GOURAUD",
    "USE_SHADING_MODEL_PHONG",
    "USE_SHADING_MODEL_PHONG_BLINN",
    "USE_SHADING_MODEL_TOON",
    "USE_SHADING_MODEL_OREN_NAYAR",
    "USE_SHADING_MODEL_MINNAERT",
    "USE_SHADING_MODEL_COOK_TORRANCE",
    "USE_SHADING_MODEL_UNLIT",
    "USE_SHADING_MODEL_FRESNEL",
    "USE_BINDLESS_TEXTURE",
    "USE_SHADER_STORAGE_BLOCK"
]
define_strs = ["-DCSM_LEVELS=5"]
for i in range(len(defines)):
    define_strs.append(f"-D{defines[i]}=1")

self_folder = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(self_folder):
    for file in files:
        ext_name = file.split(".")[-1]
        if ext_name in ["vert", "frag", "geom", "tesc", "tese", "comp"]:
            cmds = ["glslc", "--target-env=opengl", "-fauto-bind-uniforms", "-fauto-map-locations"]
            full_cmds = cmds + define_strs + [f"{root}/{file}", "-c"]
            subprocess.check_call(full_cmds)