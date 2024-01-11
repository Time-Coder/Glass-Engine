import subprocess
import sys
import os
import shutil
import platform
from tree_sitter import Language
import glob

if os.path.isdir("build"):
    shutil.rmtree("build")

if os.path.isdir("python_glass.egg-info"):
    shutil.rmtree("python_glass.egg-info")

self_folder = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
platform_system = platform.system()
if platform_system == "Linux":
    dll_suffix = ".so"
elif platform_system == "Darwin":
    dll_suffix = ".dylib"
else:
    dll_suffix = ".dll"
    
dll_file = self_folder + "/glass/glsl/glsl" + dll_suffix
if not os.path.isfile(dll_file):
    Language.build_library(dll_file, [self_folder + "/glass/tree-sitter-glsl"])
    trash_files = glob.glob(self_folder + "/glass/glsl/glsl.*")
    for trash_file in trash_files:
        if os.path.abspath(trash_file) != os.path.abspath(dll_file):
            os.remove(trash_file)

with open("README_glass.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("setup_glass.py", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("setup.py", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("MANIFEST.in", "w", encoding="utf-8") as out_file:
    out_file.write(
"""include glass/README_PYPI.md
""")

subprocess.call([sys.executable, "-m", "build", "--config-setting=-i", "--config-setting=https://pypi.tuna.tsinghua.edu.cn/simple"])

with open("README_glass_engine.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)