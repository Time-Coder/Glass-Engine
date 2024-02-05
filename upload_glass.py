import subprocess
import sys

subprocess.call([sys.executable, "-m", "twine", "upload", "dist/python_glass-*.tar.gz", "dist/python_glass-*.whl", "--verbose"])
