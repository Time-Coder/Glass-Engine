#!/bin/bash

set -e

python_versions=("3.7.9" "3.8.10" "3.9.13" "3.10.11" "3.11.7" "3.12.1")
for version in ${python_versions[@]};
do
    pyenv local $version
    $(pyenv which pip) config set global.index-url https://mirrors.aliyun.com/pypi/simple
    $(pyenv which python) build_assimpy.py
done;