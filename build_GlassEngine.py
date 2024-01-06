import subprocess
import sys

subprocess.call([sys.executable, "setup_GlassEngine.py", "sdist", "bdist_wheel"])
