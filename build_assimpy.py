import subprocess
import sys
import os
import shutil
import platform
import glob

if os.path.isdir("build"):
    shutil.rmtree("build")

if os.path.isdir("assimpy.egg-info"):
    shutil.rmtree("assimpy.egg-info")

with open("README_assimpy.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("setup_assimpy.py", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("setup.py", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("MANIFEST.in", "w") as out_file:
    out_file.write(
"""include assimpy/LICENSE
include assimpy/README_PYPI.md
include assimpy/assimpy_ext.h
recursive-include assimpy/assimp *
""")

subprocess.call([sys.executable, "-m", "pip", "install", "pip", "--upgrade", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
subprocess.call([sys.executable, "-m", "build", "--config-setting=-i", "--config-setting=https://pypi.tuna.tsinghua.edu.cn/simple"])

with open("README_glass_engine.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)

if platform.system() == "Linux":
    machine = platform.machine()
    files = glob.glob(f"dist/assimpy-*-linux_{machine}.whl")
    for file in files:
        subprocess.call([sys.executable, "-m", "auditwheel", "repair", file, f"--plat=manylinux_2_35_{machine}", "-w", "dist"])
        os.remove(file)