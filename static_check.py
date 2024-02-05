import os
import subprocess
import sys


def check_syntax(folder_name):
    for home, dirs, files in os.walk(folder_name):
        for file_name in files:
            if file_name.endswith(".py") and file_name != "__init__.py":
                subprocess.call([sys.executable, "-m", "pyflakes", home + "/" + file_name])


def check_style(folder_name):
    for home, dirs, files in os.walk(folder_name):
        for file_name in files:
            if file_name.endswith(".py"):
                subprocess.call([sys.executable, "-m", "pycodestyle", home + "/" + file_name])


check_syntax("glass")
check_syntax("glass_engine")

check_style("glass")
check_style("glass_engine")
