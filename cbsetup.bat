@echo off

:: Check if script is running as administrator
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo Script is running as administrator.
) ELSE (
    echo Script is not running as administrator.
    echo Attempting to elevate privileges...
    powershell -Command "Start-Process '%comspec%' -ArgumentList '/c \"%~0\"' -Verb RunAs"
    exit /B
)

:: The rest of the script runs with administrative privileges
:: Install Chocolatey
echo Installing Chocolatey...
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "(iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))) >$null 2>&1"
echo Chocolatey installed successfully!

:: Install Python using Chocolatey
echo Installing Python with Chocolatey...
choco install -y python
echo Python installed successfully!

:: Install additional tools
echo Installing additional tools (curl, wget, openssl)...
choco install -y curl
choco install -y wget
choco install -y openssl
echo Additional tools installed successfully!

:: Pause script
pause
