import subprocess
import sys
import os
import shutil

if os.path.isdir("build"):
    shutil.rmtree("build")

if os.path.isdir("python_glass.egg-info"):
    shutil.rmtree("python_glass.egg-info")

with open("README_glass.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("setup_glass.py", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("setup.py", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("MANIFEST.in", "w", encoding="utf-8") as out_file:
    out_file.write(
"""include glass/README_PYPI.md
include glass/LICENSE
include glass/ShaderParser_/pcpp/LICENSE
""")

subprocess.call([sys.executable, "setup.py", "sdist", "bdist_wheel"])

with open("README_glass_engine.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)