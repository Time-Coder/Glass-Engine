import os
import subprocess
import sys


def check_syntax(folder_name):
    subprocess.call([sys.executable, "-m", "pyflakes", folder_name])


def check_style(folder_name):
    subprocess.call([sys.executable, "-m", "pycodestyle", folder_name])


check_syntax("glass")
check_syntax("glass_engine")

# check_style("glass")
# check_style("glass_engine")
