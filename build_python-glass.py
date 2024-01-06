import subprocess
import sys

subprocess.call([sys.executable, "setup_python-glass.py", "sdist", "bdist_wheel"])
