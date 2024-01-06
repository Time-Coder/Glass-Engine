import setuptools
import os
import shutil

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

if os.path.isdir("python-glass.egg-info"):
    shutil.rmtree("python-glass.egg-info")

extra_files = \
[
    "tree-sitter-glsl/glsl.dll"
]
extra_files.extend(find_files("glass", "glass/glsl"))

setuptools.setup(
    name="python-glass",
    version="0.1.31",
    author="王炳辉 (BingHui-WANG)",
    author_email="binghui.wang@foxmail.com",
    description="OpenGL wrapper for Glass-Engine",
    long_description="OpenGL wrapper for Glass-Engine",
    long_description_content_type="text/plain",
    packages=['glass'],
    package_data={
        'glass': extra_files
    },
    platforms=["win_amd64", "win32"],
    python_requires=">=3.7",
    install_requires=[
        "PyOpenGL",
        "PyOpenGL_accelerate",
        "moderngl",
        "PyGLM",
        "numpy",
        "opencv-python",
        "Pillow",
        "maxminddb-geolite2",
        "wget",
        "requests",
        "chardet",
        "tree-sitter"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
