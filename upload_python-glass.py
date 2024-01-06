import subprocess
import sys

subprocess.call([sys.executable, "-m", "twine", "upload", "dist/python-glass-*.tar.gz", "dist/python_glass-*.whl", "--verbose"])
