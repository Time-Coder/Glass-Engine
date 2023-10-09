import setuptools
import os
import shutil
import sys
import platform
import subprocess

# install PyGLM
if "-d" in sys.argv:
    plat = "x64" if platform.architecture()[0] == "64bit" else "win32"
    version = ".".join(platform.python_version().split(".")[:2])
    if int(version.split(".")[1]) < 12:
        subprocess.call(sys.executable, "-m", "pip", "install", "PyGLM")
    else:
        gitee_url = ""
        github_url = ""
        
        if plat == "x64":
            gitee_url = ""
            github_url = ""
        else:
            gitee_url = ""
            github_url = ""

        return_code = subprocess.call(sys.executable, "-m", "pip", "install", gitee_url)
        if return_code != 0:
            subprocess.call(sys.executable, "-m", "pip", "install", github_url)

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
    "images/glass_engine_logo64.png",
    "images/glass_engine_logo256.png",
    "images/start.png",
    "README_PYPI.md"
]
glass_engine_extra_files.extend(find_files("glass_engine", "glass_engine/glsl"))
glass_extra_files = find_files("glass", "glass/glsl")

setuptools.setup(
    name="glass_engine",
    version="0.1.10",
    author="王炳辉 (BingHui-WANG)",
    author_email="binghui.wang@foxmail.com",
    description="An easy-to-use 3D rendering engine for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Time-Coder/Glass-Engine",
    packages=setuptools.find_packages(),
    package_data={
        'glass_engine': glass_engine_extra_files,
        'glass': glass_extra_files
    },
    platforms=["win_amd64", "win32"],
    python_requires=">=3.7",
    install_requires=[
        "PyOpenGL",
        "PyOpenGL_accelerate",
        "MarkupSafe==2.0.1",
        "qt-material",
        "numpy",
        "opencv-python",
        "Pillow",
        "pyroexr",
        "maxminddb-geolite2",
        "wget",
        "requests",
        "chardet"
    ],
    classifiers=[
        f"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
