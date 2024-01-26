import os
import platform

def find_files(directory):
    file_list = []
    abs_directory = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..").replace("\\", "/") + "/" + directory
    for root, _, files in os.walk(abs_directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file)).replace("\\", "/")
            if not os.path.isfile(file_path):
                continue

            target_path = "glass/" + directory + file_path[len(abs_directory):(-len(os.path.basename(file_path))-1)]
            if "__glcache__" not in file_path:
                file_list.append((file_path.replace("\\", "/"), target_path))
    return file_list

datas = find_files('glsl')
datas += find_files("tree-sitter-glsl")
datas.append((os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../LICENSE").replace("\\", "/"), "glass"))
if platform.system() == "Linux":
    hiddenimports = ["OpenGL.platform.egl"]
