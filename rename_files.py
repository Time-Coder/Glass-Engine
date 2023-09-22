import os
import sys

version = sys.argv[1]
versions = version.split(".")
plat = sys.argv[2]
plat_postfix = ("_amd64" if plat == "x64" else "32")

postfix = f"py3.{versions[1]}-win{plat_postfix}"

target_filename = f"dist/glass_engine-0.0.1-{postfix}.tar.gz"

if os.path.isfile(target_filename):
    os.remove(target_filename)

os.rename("dist/glass_engine-0.0.1.tar.gz", target_filename)