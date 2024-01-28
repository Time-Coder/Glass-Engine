import setuptools
import os

def find_files(module, directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)[(len(module) + 1) :]
            abs_file_path = os.path.abspath(os.path.join(root, file)).replace("\\", "/")
            if not os.path.isfile(abs_file_path):
                continue

            if "__glcache__" not in file_path:
                file_list.append(file_path.replace("\\", "/"))
    return file_list

extra_files = ["LICENSE"]
extra_files += find_files("glass", "glass/glsl")
extra_files += find_files("glass", "glass/tree-sitter-glsl")

with open("glass/README_PYPI.md", "r", encoding='utf-8') as in_file:
    long_description = in_file.read()

setuptools.setup(
    name="python_glass",
    version="0.1.51",
    author="王炳辉 (BingHui-WANG)",
    author_email="binghui.wang@foxmail.com",
    description="OpenGL wrapper for Glass-Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Time-Coder/Glass-Engine",
    packages=setuptools.find_packages(exclude=['*glass_engine*', '*assimpy*']),
    package_data={
        'glass': extra_files
    },
    include_package_data=False,
    python_requires=">=3.7",
    install_requires=[
        "PyOpenGL",
        "PyGLM",
        "numpy",
        "opencv-python",
        "maxminddb-geolite2",
        "wget",
        "requests",
        "chardet",
        "tree-sitter",
        "freetype-py"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    entry_points={'pyinstaller40': ['hook-dirs = glass.__pyinstaller:get_hook_dirs']}
)
