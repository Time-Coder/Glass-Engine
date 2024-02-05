import subprocess
import sys
import os
import shutil

if os.path.isdir("build"):
    shutil.rmtree("build")

if os.path.isdir("glass_engine.egg-info"):
    shutil.rmtree("glass_engine.egg-info")

with open("README_glass_engine.rst", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("README.rst", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("setup_glass_engine.py", "r", encoding="utf-8") as in_file:
    content = in_file.read()

with open("setup.py", "w", encoding="utf-8") as out_file:
    out_file.write(content)

with open("MANIFEST.in", "w", encoding="utf-8") as out_file:
    out_file.write(
"""include glass_engine/images/glass_engine_logo256.png
include glass_engine/images/start.png
include glass_engine/README_PYPI.md
include glass_engine/LICENSE
""")

subprocess.call([sys.executable, "setup.py", "sdist", "bdist_wheel"])
