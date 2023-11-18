import os
import shutil

class GlassConfig:

    def __init__(self):
        self_folder = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
        glass_engine_glsl_folder = self_folder + "/../glass_engine/glsl"
        glass_glsl_folder = self_folder + "/glsl"
        if os.path.isdir(glass_engine_glsl_folder):
            self.__cache_folder = glass_engine_glsl_folder + "/__glcache__"
        else:
            self.__cache_folder = glass_glsl_folder + "/__glcache__"

        self.debug:bool = False
        self.print:bool = True
        self.warning:bool = True
        self.recompile:bool = False

    @property
    def cache_folder(self)->str:
        if not os.path.isdir(self.__cache_folder):
            os.makedirs(self.__cache_folder)

        return self.__cache_folder

    @cache_folder.setter
    def cache_folder(self, folder_path:str):
        self.__cache_folder = folder_path

    def clear_cache(self):
        if os.path.isdir(self.__cache_folder):
            shutil.rmtree(self.__cache_folder)

GlassConfig = GlassConfig()