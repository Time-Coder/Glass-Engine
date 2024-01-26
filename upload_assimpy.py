import subprocess
import sys

subprocess.call([sys.executable, "-m", "twine", "upload", "dist/assimpy-*.whl", "--verbose"])