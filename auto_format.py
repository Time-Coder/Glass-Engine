import subprocess
import sys


def auto_format(folder_name):
    subprocess.call([sys.executable, "-m", "black", folder_name])


auto_format("glass")
auto_format("glass_engine")
