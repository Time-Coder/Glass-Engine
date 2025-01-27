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
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-i", "https://mirrors.aliyun.com/pypi/simple"])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def vspaths():
    result = {
        "x86_PATH": [],
        "x64_PATH": [],
        "INCLUDE": [],
        "x86_LIB": [],
        "x64_LIB": [],
    }

    cl_path = shutil.which("cl.exe")
    if cl_path is None:
        raise RuntimeError("cl.exe is not in your PATH")
    
    cl_path = os.path.dirname(cl_path)
    vs_home = os.path.abspath(os.path.join(cl_path, "..", "..", ".."))
    
    result["x86_PATH"].append(vs_home + "\\bin\\Hostx86\\x86")
    result["x64_PATH"].append(vs_home + "\\bin\\Hostx86\\x64")
    
    rc_path = shutil.which("rc.exe")
    if cl_path is None:
        raise RuntimeError("rc.exe is not in your PATH")
    
    rc_path = os.path.dirname(rc_path)
    sdk_home = os.path.abspath(os.path.join(rc_path, ".."))
    sdk_version = os.path.basename(sdk_home)
    sdk_home = os.path.abspath(os.path.join(sdk_home, "..", ".."))
    
    result["x86_PATH"].append(f"{sdk_home}\\bin\\{sdk_version}\\x86")
    result["x64_PATH"].append(f"{sdk_home}\\bin\\{sdk_version}\\x64")

    result["INCLUDE"].append(f"{vs_home}\\include")
    result["INCLUDE"].append(f"{sdk_home}\\Include\\{sdk_version}\\cppwinrt")
    result["INCLUDE"].append(f"{sdk_home}\\Include\\{sdk_version}\\shared")
    result["INCLUDE"].append(f"{sdk_home}\\Include\\{sdk_version}\\ucrt")
    result["INCLUDE"].append(f"{sdk_home}\\Include\\{sdk_version}\\um")
    result["INCLUDE"].append(f"{sdk_home}\\Include\\{sdk_version}\\winrt")

    result["x86_LIB"].append(f"{vs_home}\\lib\\x86")
    result["x86_LIB"].append(f"{sdk_home}\\Lib\\{sdk_version}\\ucrt\\x86")
    result["x86_LIB"].append(f"{sdk_home}\\Lib\\{sdk_version}\\um\\x86")

    result["x64_LIB"].append(f"{vs_home}\\lib\\x64")
    result["x64_LIB"].append(f"{sdk_home}\\Lib\\{sdk_version}\\ucrt\\x64")
    result["x64_LIB"].append(f"{sdk_home}\\Lib\\{sdk_version}\\um\\x64")

    return result

try:
    import setuptools
except ImportError:
    pip_install("setuptools")
    import setuptools

bits = platform.architecture()[0]
if bits == "64bit":
    bits = "x64"
else:
    bits = "x86"

extra_flags = []
library_dirs = [
    f"build/assimp-5.4.3/{bits}/lib",
    f"build/assimp-5.4.3/{bits}/contrib/zlib",
    f"build/assimp-5.4.3/{bits}/lib/MinSizeRel",
    f"build/assimp-5.4.3/{bits}/contrib/zlib/MinSizeRel"
]

if (
    (
        not os.path.isfile(library_dirs[0] + "/assimp.lib") and
        not os.path.isfile(library_dirs[0] + "/assimp.a") and
        not os.path.isfile(library_dirs[0] + "/libassimp.lib") and
        not os.path.isfile(library_dirs[0] + "/libassimp.a") and
        not os.path.isfile(library_dirs[2] + "/assimp.lib") and
        not os.path.isfile(library_dirs[2] + "/assimp.a") and
        not os.path.isfile(library_dirs[2] + "/libassimp.lib") and
        not os.path.isfile(library_dirs[2] + "/libassimp.a")
    ) or (
        not os.path.isfile(library_dirs[1] + "/zlibstatic.lib") and
        not os.path.isfile(library_dirs[1] + "/zlibstatic.a") and
        not os.path.isfile(library_dirs[1] + "/libzlibstatic.lib") and
        not os.path.isfile(library_dirs[1] + "/libzlibstatic.a") and
        not os.path.isfile(library_dirs[3] + "/zlibstatic.lib") and
        not os.path.isfile(library_dirs[3] + "/zlibstatic.a") and
        not os.path.isfile(library_dirs[3] + "/libzlibstatic.lib") and
        not os.path.isfile(library_dirs[3] + "/libzlibstatic.a")
    )
):
    zip_file = zipfile.ZipFile("assimpy/assimp-5.4.3.zip")
    zip_file.extractall("assimpy")
    zip_file.close()

    zip_file = zipfile.ZipFile("assimpy/pybind11-2.13.6.zip")
    zip_file.extractall("assimpy")
    zip_file.close()

    if shutil.which("cmake") is None:
        pip_install("cmake")

    if shutil.which("ninja") is None:
        pip_install("ninja")

    if shutil.which("ninja") is not None:
        extra_flags = ["-G", "Ninja"]

    if platform.system() == "Windows":
        vs_paths = vspaths()
        os.environ["INCLUDE"] = ";".join(vs_paths["INCLUDE"])
        if bits == "x64":
            os.environ["LIB"] = ";".join(vs_paths["x64_LIB"])
            os.environ["PATH"] = ";".join(vs_paths["x64_PATH"]) + ";" + os.environ["PATH"]
        else:
            os.environ["LIB"] = ";".join(vs_paths["x86_LIB"])
            os.environ["PATH"] = ";".join(vs_paths["x86_PATH"]) + ";" + os.environ["PATH"]

    subprocess.check_call(
        [
            "cmake", "assimpy/assimp-5.4.3",
            "-B", f"build/assimp-5.4.3/{bits}",
            "-DCMAKE_BUILD_TYPE=MinSizeRel",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DASSIMP_BUILD_TESTS=OFF",
            "-DASSIMP_INJECT_DEBUG_POSTFIX=OFF",
            "-DASSIMP_INSTALL=OFF",
            "-DASSIMP_INSTALL_PDB=OFF",
            "-DASSIMP_WARNINGS_AS_ERRORS=OFF",
            "-DLIBRARY_SUFFIX=",
            "-DCMAKE_DEPFILE_FLAGS_C=",
            "-DCMAKE_DEPFILE_FLAGS_CXX="
        ] + extra_flags
    )
    subprocess.check_call(
        [
            "cmake", "--build", f"build/assimp-5.4.3/{bits}", "--config", "MinSizeRel", "--parallel"
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
        "assimpy/pybind11-2.13.6/include",
        "assimpy/assimp-5.4.3/include",
        f"build/assimp-5.4.3/{bits}/include"
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
    version="5.4.3",
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