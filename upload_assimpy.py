import subprocess
import sys

subprocess.call([sys.executable, "-m", "twine", "upload", "dist/assimpy-*.tar.gz", "dist/assimpy-*.whl", "--verbose"])