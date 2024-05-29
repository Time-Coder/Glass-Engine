import platform
import zipfile
import subprocess
import shutil
import sys
import os

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def public_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        return response.json().get("origin")
    except:
        return "127.0.0.1"

def is_China_ip(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json/")
        data = response.json()
        return data['country'] == 'CN'
    except Exception as e:
        return True

_is_China_user = None
def is_China_user():
    global _is_China_user
    if _is_China_user is None:
        _is_China_user = is_China_ip(public_ip())

    return _is_China_user

def pip_install(package):
    if is_China_user():
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import setuptools
except ImportError:
    pip_install("setuptools")
    import setuptools

zip_file = zipfile.ZipFile("assimpy/assimp-5.4.1.zip")
zip_file.extractall("assimpy")
zip_file.close()

zip_file = zipfile.ZipFile("assimpy/pybind11-2.12.0.zip")
zip_file.extractall("assimpy")
zip_file.close()

extra_flags = []
if platform.system() == "Windows":
    library_dirs = [
        "build/assimp-5.4.1/lib/MinSizeRel",
        "build/assimp-5.4.1/contrib/zlib/MinSizeRel"
    ]
else:
    library_dirs = [
        "build/assimp-5.4.1/lib",
        "build/assimp-5.4.1/contrib/zlib"
    ]
    if shutil.which("ninja") is not None:
        extra_flags = ["-G", "Ninja"]

if shutil.which("cmake") is None:
    pip_install("cmake")

if (
    (
        not os.path.isfile(library_dirs[0] + "/assimp.lib") and
        not os.path.isfile(library_dirs[0] + "/assimp.a") and
        not os.path.isfile(library_dirs[0] + "/libassimp.lib") and
        not os.path.isfile(library_dirs[0] + "/libassimp.a")
    ) or (
        not os.path.isfile(library_dirs[1] + "/zlibstatic.lib") and
        not os.path.isfile(library_dirs[1] + "/zlibstatic.a") and
        not os.path.isfile(library_dirs[1] + "/libzlibstatic.lib") and
        not os.path.isfile(library_dirs[1] + "/libzlibstatic.a")
    )
):
    subprocess.check_call(
        [
            "cmake", "assimpy/assimp-5.4.1",
            "-B", "build/assimp-5.4.1",
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
            "cmake", "--build", f"build/assimp-5.4.1", "--config", "MinSizeRel", "--parallel"
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
        "assimpy/assimp-5.4.1/include",
        "build/assimp-5.4.1/include"
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
    version="5.4.1",
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