import subprocess
import sys

subprocess.call([sys.executable, "setup_assimpy.py", "sdist", "bdist_wheel"])