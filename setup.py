import sys
import setuptools
import os
import shutil
import platform

versions = platform.python_version().split(".")
version = ".".join(versions[:2])
plat = ("x64" if platform.architecture()[0] == "64bit" else "win32")
if len(sys.argv) == 4 and sys.argv[3] in ["x64", "win32"]:
    version = sys.argv[2]
    versions = version.split(".")
    plat = sys.argv[3]
    sys.argv = sys.argv[:2]

python_requires = f">=3.{versions[1]}, <3.{int(versions[1])+1}"

openexr_urls = \
{
    ("3.6", "win32"): "https://download.lfd.uci.edu/pythonlibs/archived/cp36/OpenEXR-1.3.2-cp36-cp36m-win32.whl",
    ("3.6", "x64"): "https://download.lfd.uci.edu/pythonlibs/archived/cp36/OpenEXR-1.3.2-cp36-cp36m-win_amd64.whl",
    ("3.7", "win32"): "https://download.lfd.uci.edu/pythonlibs/archived/cp37/OpenEXR-1.3.7-cp37-cp37m-win32.whl",
    ("3.7", "x64"): "https://download.lfd.uci.edu/pythonlibs/archived/cp37/OpenEXR-1.3.7-cp37-cp37m-win_amd64.whl",
    ("3.8", "win32"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp38-cp38-win32.whl",
    ("3.8", "x64"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp38-cp38-win_amd64.whl",
    ("3.9", "win32"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp39-cp39-win32.whl",
    ("3.9", "x64"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp39-cp39-win_amd64.whl",
    ("3.10", "win32"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp310-cp310-win32.whl",
    ("3.10", "x64"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp310-cp310-win_amd64.whl",
    ("3.11", "win32"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp311-cp311-win32.whl",
    ("3.11", "x64"): "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp311-cp311-win_amd64.whl"
}
openexr_url = openexr_urls[(version, plat)]

postfix = ("_amd64" if plat == "x64" else "32")
assimp_loader_name = f"AssimpModelLoader/AssimpModelLoader.cp3{versions[1]}-win{postfix}.pyd"
assimp_dll_name = "AssimpModelLoader/assimp-vc143-mt.dll"

def find_files(module, directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)[(len(module) + 1) :]
            if "__glcache__" not in file_path:
                file_list.append(file_path.replace("\\", "/"))
    return file_list

if os.path.isdir(f"glass_engine/AssimpModelLoader_{plat}"):
    if plat == "win32":
        os.rename("glass_engine/AssimpModelLoader", "glass_engine/AssimpModelLoader_x64")
    else:
        os.rename("glass_engine/AssimpModelLoader", "glass_engine/AssimpModelLoader_win32")

    os.rename(f"glass_engine/AssimpModelLoader_{plat}", "glass_engine/AssimpModelLoader")

if os.path.isdir("build"):
    shutil.rmtree("build")

if os.path.isdir("glass_engine.egg-info"):
    shutil.rmtree("glass_engine.egg-info")

with open("glass_engine/README_PYPI.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

glass_engine_extra_files = \
[
    assimp_loader_name,
    assimp_dll_name,
    "glass_engine_logo64.png",
    "glass_engine_logo256.png",
    "glass_engine_logo411.png",
    "Demos/assets/models/jet/11805_airplane_v2_L2.mtl",
    "Demos/assets/models/jet/11805_airplane_v2_L2.obj",
    "Demos/assets/models/jet/airplane_body_diffuse_v1.jpg",
    "Demos/assets/models/jet/airplane_wings_diffuse_v1.jpg",
    "Demos/assets/skydomes/puresky.exr",
    "README_PYPI.md"
]
glass_engine_extra_files.extend(find_files("glass_engine", "glass_engine/glsl"))
glass_extra_files = find_files("glass", "glass/glsl")

setuptools.setup(
    name="glass_engine",
    version="0.0.1",
    author="王炳辉 (BingHui-WANG)",
    author_email="binghui.wang@foxmail.com",
    description="A very user-friendly 3D rendering engine for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Time-Coder/Glass-Engine",
    packages=setuptools.find_packages(),
    package_data={
        'glass_engine': glass_engine_extra_files,
        'glass': glass_extra_files
    },
    platforms=[("win_amd64" if plat == "x64" else "win32")],
    python_requires=python_requires,
    install_requires=[
        "PyOpenGL",
        "PyOpenGL_accelerate",
        "PyQt6",
        "qt-material",
        "PyGLM",
        "numpy",
        "opencv-python",
        "Pillow",
        f"OpenEXR @ {openexr_url}"
    ],
    classifiers=[
        f"Programming Language :: Python :: {version}",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
