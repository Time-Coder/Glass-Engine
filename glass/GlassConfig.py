import os
import sys

class GlassConfig:

    def __init__(self):
        self.__cache_folder = os.path.dirname(os.path.abspath(sys.argv[0])) + "/__glcache__"
        self.__debug = True
        self.__print = False
        self.__warning = True

    @property
    def cache_folder(self)->str:
        if not os.path.isdir(self.__cache_folder):
            os.makedirs(self.__cache_folder)

        return self.__cache_folder

    @cache_folder.setter
    def cache_folder(self, folder_path:str):
        self.__cache_folder = folder_path

    @property
    def debug(self):
        return self.__debug
    
    @debug.setter
    def debug(self, flag:bool):
        self.__debug = flag

    @property
    def warning(self):
        return self.__warning
    
    @warning.setter
    def warning(self, flag:bool):
        self.__warning = flag

    @property
    def print(self):
        return self.__print
    
    @print.setter
    def print(self, flag:bool):
        self.__print = flag

GlassConfig = GlassConfig()