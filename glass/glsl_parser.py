import platform
from tree_sitter import Language, Parser
import os
import glob

glsl_parser = None
def create_glsl_parser():
    global glsl_parser
    if glsl_parser is not None:
        return
    
    self_folder = os.path.dirname(os.path.abspath(__file__))
    platform_system = platform.system()
    if platform_system == "Linux":
        dll_suffix = ".so"
    elif platform_system == "Darwin":
        dll_suffix = ".dylib"
    else:
        dll_suffix = ".dll"

    if platform.architecture()[0] == "64bit":
        plat = "x64"
    else:
        plat = "x86"
        
    dll_file = self_folder + "/glsl/glsl-" + plat + dll_suffix
    if not os.path.isfile(dll_file):
        Language.build_library(dll_file, [self_folder + "/tree-sitter-glsl"])
        trash_files = glob.glob(self_folder + f"/glsl/glsl-{plat}.*")
        for trash_file in trash_files:
            if os.path.abspath(trash_file) != os.path.abspath(dll_file):
                os.remove(trash_file)

    GLSL_LANGUAGE = Language(dll_file, 'glsl')
    glsl_parser = Parser()
    glsl_parser.set_language(GLSL_LANGUAGE)

def get_glsl_parser():
    global glsl_parser
    if glsl_parser is None:
        create_glsl_parser()

    return glsl_parser