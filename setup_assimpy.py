from setuptools import setup
import os

import platform

try:
    import pybind11
except:
    import sys
    import subprocess
    subprocess.call([sys.executable, "-m", "pip", "install", "pybind11"])
    import pybind11

from pybind11.setup_helpers import Pybind11Extension

def find_files(module, directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)[(len(module) + 1) :]
            if "__glcache__" not in file_path:
                file_list.append(file_path.replace("\\", "/"))
    return file_list

plat = "x64" if platform.architecture()[0] == "64bit" else "win32"
ext_modules = [
    Pybind11Extension(
        name="assimpy",
        sources=sorted(["assimpy/assimpy.cpp", "assimpy/module.cpp"]),  # Sort source files for reproducibility
        include_dirs=[
            os.path.dirname(os.path.abspath(pybind11.__file__)).replace("\\", "/") + "/include",
            "assimpy/assimp/include"
        ],
        library_dirs=[
            "assimpy/assimp/lib"
        ],
        libraries=[
            f"assimp-{plat}",
            f"zlibstatic-{plat}"
        ]
    ),
]

with open("assimpy/README_PYPI.md", "r", encoding='utf-8') as in_file:
    long_description = in_file.read()

setup(
    name="assimpy",
    version="5.3.1.1",
    author="王炳辉 (BingHui-WANG)",
    author_email="binghui.wang@foxmail.com",
    description="3D model loader for Glass-Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Time-Coder/Glass-Engine",
    include_package_data=False,
    platforms=["win_amd64", "win32"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    ext_modules=ext_modules
)