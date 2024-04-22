import os
import platform


def find_files(directory):
    file_list = []
    abs_directory = (
        os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..").replace(
            "\\", "/"
        )
        + "/"
        + directory
    )
    for root, _, files in os.walk(abs_directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file)).replace("\\", "/")
            if not os.path.isfile(file_path):
                continue

            target_path = (
                "glass/"
                + directory
                + file_path[
                    len(abs_directory) : (-len(os.path.basename(file_path)) - 1)
                ]
            )
            if "__glcache__" not in file_path:
                file_list.append((file_path.replace("\\", "/"), target_path))
    return file_list

self_folder = os.path.dirname(os.path.abspath(__file__))
datas = find_files("glsl")
datas += find_files("ShaderParser_/tree-sitter-glsl")
datas.extend(
    [
        (
            os.path.abspath(self_folder + "/../LICENSE").replace("\\", "/"),
            "glass",
        ),
        (
            os.path.abspath(self_folder + "/../ShaderParser_/pcpp/LICENSE").replace("\\", "/"),
            "glass/ShaderParser_/pcpp",
        )
    ]
)
if platform.system() == "Linux":
    hiddenimports = ["OpenGL.platform.egl"]
