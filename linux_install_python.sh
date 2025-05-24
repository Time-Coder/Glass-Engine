#!/bin/bash

set -e

# sudo aptitude install libreadline-dev libbz2-dev liblzma-dev libsqlite3-dev tk-dev libffi-dev libgdbm-dev uuid-dev

python_versions=("3.7.17" "3.8.20" "3.9.22" "3.10.17" "3.11.12" "3.12.10" "3.13.3")
for version in ${python_versions[@]};
do
    # wget --no-check-certificate https://npm.taobao.org/mirrors/python/$version/Python-$version.tar.xz -P ~/.pyenv/cache/
    pyenv install -v $version
    # pyenv local $version
    # $(pyenv which python) -m pip install pip --upgrade -i https://mirrors.aliyun.com/pypi/simple
    # $(pyenv which python) -m pip install -r requirements.txt --upgrade -i https://mirrors.aliyun.com/pypi/simple
done;
