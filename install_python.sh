#!/bin/bash

set -e

sudo apt -y install libssl-dev libreadline-dev libbz2-dev liblzma-dev libsqlite3-dev

python_versions=("3.7.9" "3.8.10" "3.9.13" "3.10.11" "3.11.7" "3.12.1")
for version in ${python_versions[@]};
do
    wget --no-check-certificate https://npm.taobao.org/mirrors/python/$version/Python-$version.tar.xz -P ~/.pyenv/cache/
    pyenv install $version
done;
