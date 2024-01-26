#!/bin/bash

set -e

python_versions=("3.7.9" "3.8.10" "3.9.13" "3.10.11" "3.11.7" "3.12.1")
for version in ${python_versions[@]};
do
    pyenv install $version
    pyenv local $version
    python build_assimpy.py
done;