@echo off
title MoCapAnything V2 - One-Click Installer (PixelArtistry)
cd /d "%~dp0"

echo ============================================================
echo  MoCapAnything V2 - One-Click Installer by PixelArtistry
echo  Needs: Windows 10/11, NVIDIA GPU recommended, ~20 GB free disk
echo ============================================================
echo.

where uv >nul 2>nul
if errorlevel 1 (
    echo Installing uv ^(Python package manager^)...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

uv run --python 3.11 --no-project install_mocapanything.py
if errorlevel 1 (
    echo.
    echo Installation failed - scroll up for the error.
    pause
    exit /b 1
)

echo.
echo Installation finished. Double-click Run_MoCapAnything.bat to start.
pause
