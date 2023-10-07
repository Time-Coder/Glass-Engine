import os
from glass.utils import pip_install

os.environ["INCLUDE"] = "G:/Python-workspace/glass_engine/glass_engine/OpenEXR_dist/include/OpenEXR;G:/Python-workspace/glass_engine/glass_engine/OpenEXR_dist/include/Imath;" + os.environ["INCLUDE"]
os.environ["LIB"] = "G:/Python-workspace/glass_engine/glass_engine/OpenEXR_dist/lib;" + os.environ["LIB"]
os.environ["PATH"] = "G:/Python-workspace/glass_engine/glass_engine/OpenEXR_dist/bin;" + os.environ["PATH"]
pip_install("OpenEXR")