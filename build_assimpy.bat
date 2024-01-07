@echo off

for /d %%i in (F:\Python\*) do (
    %%i\python.exe build_assimpy.py
    if %errorlevel% neq 0 exit /b %errorlevel%
)