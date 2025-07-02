@echo off

REM Locate real Python executable directory using py launcher
for /f "delims=" %%P in ('py -c "import os, sys; print(os.path.dirname(sys.executable))"') do set PYTHON_DIR=%%P

REM Get current system PATH
for /f "usebackq tokens=*" %%A in (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| findstr /i Path`) do set "SYS_PATH=%%A"
set "SYS_PATH=%SYS_PATH:~33%"

REM Append Python and Scripts to system PATH
setx /M PATH "%SYS_PATH%;%PYTHON_DIR%;%PYTHON_DIR%\Scripts%"
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Python and Scripts directories have been added to the system PATH.
    echo Please restart your terminal or computer for changes to take effect.
) else (
    echo [ERROR] Failed to update the system PATH. Please run this script as administrator.
)

pause