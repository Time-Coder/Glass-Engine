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

with open("glass_engine/README_PYPI.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

extra_files = ["images/glass_engine_logo64.png", "LICENSE"]
extra_files += find_files("glass_engine", "glass_engine/glsl")

setuptools.setup(
    name="glass_engine",
    version="0.1.51",
    author="王炳辉 (BingHui-WANG)",
    author_email="binghui.wang@foxmail.com",
    description="An easy-to-use 3D rendering engine for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Time-Coder/Glass-Engine",
    packages=setuptools.find_packages(include=['glass_engine*']),
    package_data={
        'glass_engine': extra_files,
    },
    include_package_data=False,
    python_requires=">=3.7",
    install_requires=[
        "python-glass>=0.1.51",
        "assimpy>=5.3.1.3",
        "pytweening"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    entry_points={'pyinstaller40': ['hook-dirs = glass_engine.__pyinstaller:get_hook_dirs']}
)
