@echo off

python setup.py sdist 3.11 x64
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.11 x64
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.10 x64
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.10 x64
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.9 x64
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.9 x64
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.8 x64
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.8 x64
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.7 x64
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.7 x64
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.6 x64
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.6 x64
if %errorlevel% neq 0 (
    goto end
)





python setup.py sdist 3.11 win32
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.11 win32
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.10 win32
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.10 win32
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.9 win32
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.9 win32
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.8 win32
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.8 win32
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.7 win32
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.7 win32
if %errorlevel% neq 0 (
    goto end
)

python setup.py sdist 3.6 win32
if %errorlevel% neq 0 (
    goto end
)
python rename_files.py 3.6 win32
if %errorlevel% neq 0 (
    goto end
)

:end
