from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import os
import shutil
import sys
import platform

python_version = ''.join(map(str, sys.version_info[:2]))
python_requires = f">={sys.version_info[0]}.{sys.version_info[1]}, <{sys.version_info[0]}.{sys.version_info[1]+1}"
bits, _ = platform.architecture()
platform_postfix = "win_amd64" if bits == "64bit" else "win32"

def modify_time(file_name):
    if not os.path.isfile(file_name):
        return 0
    
    return os.path.getmtime(file_name)

def compile_folder(folder_name):
    compiler_directives = {"language_level": "3", "annotation_typing": False}
    postfix = f".cp{python_version}-{platform_postfix}.pyd"
    for home, dirs, files in os.walk(folder_name):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                if not os.path.isdir(postfix + "/" + home):
                    os.makedirs(postfix + "/" + home)

                base_name = filename.split(".")[0]
                if modify_time(home + "/" + base_name + ".c") < modify_time(home + "/" + filename) or \
                   modify_time(home + "/" + filename) > modify_time(postfix + "/" + home + "/" + base_name + postfix):
                    extension = Extension(
                        base_name, [home + "/" + filename],
                        extra_compile_args=["/Ox"]
                    )
                    ext_modules = cythonize(extension, compiler_directives=compiler_directives)
                    setup(name=base_name, python_requires=python_requires, ext_modules=ext_modules)

                src_file_name = base_name + postfix
                dest_file_name = postfix + "/" + home + "/" + src_file_name
                if modify_time(src_file_name) > modify_time(dest_file_name):
                    if os.path.isfile(dest_file_name):
                        os.remove(dest_file_name)

                    shutil.move(src_file_name, postfix + "/" + home)

            if filename == "__init__.py":
                src_file_name = home + "/" + filename
                dest_file_name = postfix + "/" + home + "/" + filename
                if modify_time(src_file_name) > modify_time(dest_file_name):
                    if os.path.isfile(dest_file_name):
                        os.remove(dest_file_name)

                    shutil.copy(src_file_name, postfix + "/" + home)

compile_folder("glass")
compile_folder("glass_engine")
