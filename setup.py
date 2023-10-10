import setuptools
import os
import shutil
import sys
import platform
import subprocess
import warnings

# install PyGLM
if "-d" in sys.argv:
    plat = "x64" if platform.architecture()[0] == "64bit" else "win32"
    version = ".".join(platform.python_version().split(".")[:2])
    if int(version.split(".")[1]) < 12:
        subprocess.call([sys.executable, "-m", "pip", "install", "PyGLM"])
    else:
        temp_folder = os.path.dirname(os.path.abspath(__file__))

        target_file = ""
        gitee_url = ""
        github_url = ""
        
        if plat == "x64":
            gitee_url = "https://gitee.com/time-coder/Glass-Engine/raw/main/PyGLM/PyGLM-2.7.0-cp312-cp312-win_amd64.whl"
            github_url = "https://raw.githubusercontent.com/Time-Coder/Glass-Engine/main/PyGLM/PyGLM-2.7.0-cp312-cp312-win_amd64.whl"
            target_file = temp_folder + "/PyGLM-2.7.0-cp312-cp312-win_amd64.whl"
        else:
            gitee_url = "https://gitee.com/time-coder/Glass-Engine/raw/main/PyGLM/PyGLM-2.7.0-cp312-cp312-win32.whl"
            github_url = "https://raw.githubusercontent.com/Time-Coder/Glass-Engine/main/PyGLM/PyGLM-2.7.0-cp312-cp312-win32.whl"
            target_file = temp_folder + "/PyGLM-2.7.0-cp312-cp312-win32.whl"

        subprocess.call([sys.executable, "-m", "pip", "install", "wget"])
        import wget

        try:
            wget.download(gitee_url, target_file)
        except:
            wget.download(github_url, target_file)

        return_code = subprocess.call([sys.executable, "-m", "pip", "install", target_file])
        if return_code != 0:
            warnings.warn("Failed to install PyGLM, Please install it manually.")

def find_files(module, directory):
    file_list = []
    for root, _, files in os.walk(directory):
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
    version="0.1.17",
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
    python_requires=">=3.6",
    install_requires=[
        "PyOpenGL",
        "PyOpenGL_accelerate",
        "moderngl",
        "MarkupSafe==2.0.1",
        "qt-material",
        "numpy",
        "opencv-python",
        "Pillow",
        "maxminddb-geolite2",
        "wget",
        "requests",
        "chardet"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
