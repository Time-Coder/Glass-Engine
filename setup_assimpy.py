import setuptools

import platform
import zipfile

zip_file = zipfile.ZipFile("assimpy/assimp.zip")
zip_file.extractall("assimpy/assimp")

zip_file = zipfile.ZipFile("assimpy/pybind11.zip")
zip_file.extractall("assimpy/pybind11")

machine = platform.machine()
plat_sys = platform.system()
bits = platform.architecture()[0]

ext = setuptools.Extension(
    name="assimpy_ext",
    sources=sorted(["assimpy/assimpy_ext.cpp", "assimpy/module.cpp"]),
    include_dirs=["assimpy/assimp/include", "assimpy/pybind11/include"],
    library_dirs=[f"assimpy/assimp/lib/{machine}/{plat_sys}/{bits}"],
    libraries=["assimp", "zlibstatic"],
    package_dir={'assimpy': 'assimpy'}
)

if plat_sys != "Windows":
    ext.extra_compile_args = ["-std=c++11"]

ext_modules = [ext]
extra_files = ["LICENSE"]

with open("assimpy/README_PYPI.md", "r", encoding='utf-8') as in_file:
    long_description = in_file.read()

setuptools.setup(
    name="assimpy",
    version="5.3.1.3",
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
