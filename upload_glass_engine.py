import subprocess
import sys

subprocess.call([sys.executable, "-m", "twine", "upload", "dist/glass_engine-*.tar.gz", "dist/glass_engine-*.whl", "--verbose"])
