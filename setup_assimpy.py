import setuptools
import platform
import zipfile
import subprocess
import shutil

zip_file = zipfile.ZipFile("assimpy/assimp-5.4.0.zip")
zip_file.extractall("assimpy")
zip_file.close()

zip_file = zipfile.ZipFile("assimpy/pybind11-2.12.0.zip")
zip_file.extractall("assimpy")
zip_file.close()

if platform.system() == "Windows":
    extra_flags = []
    library_dirs = [
        "build/assimp-5.4.0/lib/MinSizeRel",
        "build/assimp-5.4.0/contrib/zlib/MinSizeRel"
    ]
elif shutil.which("ninja") is not None:
    extra_flags = ["-G", "Ninja"]
    library_dirs = [
        "build/assimp-5.4.0/lib",
        "build/assimp-5.4.0/contrib/zlib"
    ]

subprocess.check_call(
    [
        "cmake", "assimpy/assimp-5.4.0",
        "-B", "build/assimp-5.4.0",
        "-DCMAKE_CONFIGURATION_TYPES=MinSizeRel",
        "-DBUILD_SHARED_LIBS=OFF",
        "-DASSIMP_BUILD_TESTS=OFF",
        "-DASSIMP_INJECT_DEBUG_POSTFIX=OFF",
        "-DASSIMP_INSTALL=OFF",
        "-DASSIMP_INSTALL_PDB=OFF",
        "-DASSIMP_WARNINGS_AS_ERRORS=OFF",
        "-DLIBRARY_SUFFIX="
    ] + extra_flags
)
subprocess.check_call(
    [
        "cmake", "--build", f"build/assimp-5.4.0", "--config", "MinSizeRel", "--parallel"
    ]
)

ext = setuptools.Extension(
    "assimpy_ext",
    sources=[
        "assimpy/assimpy_ext.cpp",
        "assimpy/module.cpp"
    ],
    include_dirs=[
        "assimpy",
        "assimpy/pybind11-2.12.0/include",
        "assimpy/assimp-5.4.0/include",
        "build/assimp-5.4.0/include"
    ],
    libraries=[
        "assimp",
        "zlibstatic"
    ],
    library_dirs=library_dirs
)

if platform.system() != "Windows":
    ext.extra_compile_args = ["-std=c++11"]

ext_modules = [ext]
extra_files = ["LICENSE", "__pyinstaller/assimp/LICENSE", "__pyinstaller/pybind11/LICENSE"]

with open("assimpy/README_PYPI.md", "r", encoding='utf-8') as in_file:
    long_description = in_file.read()

setuptools.setup(
    name="assimpy",
    version="5.4.0",
    author="王炳辉 (BingHui-WANG)",
    author_email="binghui.wang@foxmail.com",
    description="3D model loader for Glass-Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Time-Coder/Glass-Engine",
    include_package_data=False,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    packages=["assimpy", "assimpy/__pyinstaller"],
    package_data={
        'assimpy': extra_files,
    },
    ext_modules=ext_modules,
    entry_points={'pyinstaller40': ['hook-dirs = assimpy.__pyinstaller:get_hook_dirs']}
)