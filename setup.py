import setuptools
import os
import shutil
import platform
import sys
import subprocess

if "-d" in sys.argv:
    version = ".".join(platform.python_version().split(".")[:2])
    openexr_urls = \
    {
        "3.7": "https://download.lfd.uci.edu/pythonlibs/archived/cp37/OpenEXR-1.3.7-cp37-cp37m-win_amd64.whl",
        "3.8": "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp38-cp38-win_amd64.whl",
        "3.9": "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp39-cp39-win_amd64.whl",
        "3.10": "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp310-cp310-win_amd64.whl",
        "3.11": "https://download.lfd.uci.edu/pythonlibs/archived/OpenEXR-1.3.8-cp311-cp311-win_amd64.whl"
    }
    
    install_cmd = [sys.executable, "-m", "pip", "install", openexr_urls[version]]
    subprocess.call(install_cmd)

def find_files(module, directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)[(len(module) + 1) :]
            if "__glcache__" not in file_path:
                file_list.append(file_path.replace("\\", "/"))
    return file_list

if os.path.isdir("build"):
    shutil.rmtree("build")

if os.path.isdir("glass_engine.egg-info"):
    shutil.rmtree("glass_engine.egg-info")

with open("glass_engine/README_PYPI.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

glass_engine_extra_files = \
[
    "AssimpModelLoader/assimp-vc143-mt.dll",
    "AssimpModelLoader/AssimpModelLoader.cp37-win_amd64.pyd",
    "AssimpModelLoader/AssimpModelLoader.cp38-win_amd64.pyd",
    "AssimpModelLoader/AssimpModelLoader.cp39-win_amd64.pyd",
    "AssimpModelLoader/AssimpModelLoader.cp310-win_amd64.pyd",
    "AssimpModelLoader/AssimpModelLoader.cp311-win_amd64.pyd",
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
    platforms=["win_amd64"],
    python_requires=">=3.7, <3.12",
    install_requires=[
        "PyOpenGL",
        "PyOpenGL_accelerate",
        "PyQt6",
        "MarkupSafe==2.0.1",
        "qt-material",
        "PyGLM",
        "numpy",
        "opencv-python",
        "Pillow"
    ],
    classifiers=[
        f"Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
