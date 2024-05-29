import subprocess
import sys
import os
import platform
import glob

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
include assimpy/assimp-5.4.1.zip
include assimpy/pybind11-2.12.0.zip
include assimpy/__pyinstaller/assimp/LICENSE
include assimpy/__pyinstaller/pybind11/LICENSE
""")

subprocess.check_call([sys.executable, "setup.py", "sdist", "bdist_wheel"])

with open("README_glass_engine.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)

if platform.system() == "Linux":
    machine = platform.machine()
    files = glob.glob(f"dist/assimpy-*-linux_{machine}.whl")
    for file in files:
        subprocess.call([sys.executable, "-m", "auditwheel", "repair", file, f"--plat=manylinux2014_{machine}", "-w", "dist"])
        os.remove(file)
