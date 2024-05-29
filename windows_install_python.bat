@echo off

set python_versions=3.7.9 3.7.9-win32 3.8.10 3.8.10-win32 3.9.13 3.9.13-win32 3.10.11 3.10.11-win32 3.11.7 3.11.7-win32 3.12.1 3.12.1-win32

for %%v in (%python_versions%) do (
    pyenv install %%v
    pyenv local %%v
    python -m pip install pip --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
    @REM python -m pip install -r requirements.txt --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple
)
