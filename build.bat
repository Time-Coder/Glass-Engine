@echo off

@REM python static_check.py
@REM if %errorlevel% neq 0 goto end

set PYTHON_HOME=F:\Python\31011
set PATH=%PYTHON_HOME%;%PATH%

python compile.py build_ext --inplace
if %errorlevel% neq 0 goto end

@REM cd pyd
@REM if %errorlevel% neq 0 goto end

@REM python setup.py sdist bdist_wheel
@REM if %errorlevel% neq 0 goto end

@REM cd dist
@REM if %errorlevel% neq 0 goto end

@REM pip uninstall glass_engine
@REM if %errorlevel% neq 0 goto end

@REM pip install glass_engine-0.0.1-py3-none-any.whl
@REM if %errorlevel% neq 0 goto end

@REM python smoke_test.py
@REM if %errorlevel% neq 0 goto end

:end
cmd /k