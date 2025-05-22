#!/bin/bash

set -e

python_versions=("3.7.17" "3.8.19" "3.9.19" "3.10.14" "3.11.9" "3.12.3" "3.13.0b1")
for version in ${python_versions[@]};
do
    pyenv local $version
    $(pyenv which pip) config set global.index-url https://mirrors.aliyun.com/pypi/simple
    $(pyenv which python) build_assimpy.py
done;
