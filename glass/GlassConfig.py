import os
import shutil
import re

from .GLConfig import GLConfig


class GlassConfig:

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
        glass_engine_glsl_folder = os.path.abspath(
            self_folder + "/../glass_engine/glsl"
        ).replace("\\", "/")
        glass_glsl_folder = self_folder + "/glsl"
        if os.path.isdir(glass_engine_glsl_folder):
            self.__cache_folder = glass_engine_glsl_folder + "/__glcache__"
        else:
            self.__cache_folder = glass_glsl_folder + "/__glcache__"

        self.debug: bool = False
        self.print: bool = True
        self.warning: bool = True
        self.recompile: bool = False

    @property
    def cache_folder(self) -> str:
        if not os.path.isdir(self.__cache_folder):
            os.makedirs(self.__cache_folder)

        return self.__cache_folder

    @cache_folder.setter
    def cache_folder(self, folder_path: str):
        self.__cache_folder = folder_path

    @property
    def renderer_folder(self) -> str:
        santified_renderer = re.sub(r'[\\/:*?"<>|]', " ", GLConfig.renderer)
        renderer_folder = f"{self.__cache_folder}/{santified_renderer}"
        if not os.path.isdir(renderer_folder):
            os.makedirs(renderer_folder)

        return renderer_folder

    def clear_cache(self):
        if os.path.isdir(self.__cache_folder):
            shutil.rmtree(self.__cache_folder)


GlassConfig = GlassConfig()
