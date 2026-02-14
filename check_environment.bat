@echo off
REM Check what APK build tools are available on this system

setlocal enabledelayedexpansion
color 0F
title Emoser Build Environment Checker
cls

echo.
echo ========================================
echo   EMOSER BUILD ENVIRONMENT CHECK
echo ========================================
echo.

set "has_git=0"
set "has_docker=0"
set "has_wsl2=0"
set "buildozer_installed=0"

echo Checking system environment...
echo.

REM Check Git
git --version >nul 2>&1
if %errorlevel% equ 0 (
    set "has_git=1"
    echo [✓] Git is installed
    git --version
) else (
    echo [✗] Git is NOT installed
)
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    set "has_docker=1"
    echo [✓] Docker is installed
    docker --version
) else (
    echo [✗] Docker is NOT installed
)
echo.

REM Check WSL2
wsl --list >nul 2>&1
if %errorlevel% equ 0 (
    set "has_wsl2=1"
    echo [✓] WSL2 is available
    wsl --list
) else (
    echo [✗] WSL2 is NOT installed
)
echo.

REM Check Python and Buildozer
python -c "import buildozer" >nul 2>&1
if %errorlevel% equ 0 (
    set "buildozer_installed=1"
    echo [✓] Buildozer Python package is installed
) else (
    echo [✗] Buildozer Python package is NOT installed
)
echo.

REM Check if buildozer.spec exists
if exist buildozer.spec (
    echo [✓] buildozer.spec configuration file found
) else (
    echo [✗] buildozer.spec NOT found in current directory
)
echo.

REM Summary
echo ========================================
echo   AVAILABLE BUILD OPTIONS
echo ========================================
echo.

if %has_git% equ 1 (
    echo ✓ GitHub Actions (Cloud Build) - AVAILABLE
    echo   Fastest and easiest method! No local setup needed.
    echo   https://github.com/features/actions
) else (
    echo ✗ GitHub Actions - Git required
    echo   Download Git: https://git-scm.com/download/win
)
echo.

if %has_docker% equ 1 (
    echo ✓ Docker Build - AVAILABLE
    echo   Build locally in a container
) else (
    echo ✗ Docker Build - Docker Desktop required
    echo   Download: https://www.docker.com/products/docker-desktop
)
echo.

if %has_wsl2% equ 1 (
    echo ✓ WSL2 Build - AVAILABLE
    echo   Build using Windows Subsystem for Linux
) else (
    echo ✗ WSL2 Build - WSL2 not installed
    echo   Run: wsl --install -d Ubuntu-22.04
)
echo.

REM Recommendations
echo ========================================
echo   RECOMMENDATIONS
echo ========================================
echo.

if %has_git% equ 1 (
    echo 1. Use GitHub Actions (simplest, cloud-based)
    echo    Run: build_apk.bat
    echo    Then choose option 1
) else if %has_docker% equ 1 (
    echo 1. Install Git first, then use GitHub Actions
    echo    Otherwise, use Docker locally
) else if %has_wsl2% equ 1 (
    echo 1. Use WSL2 Build (good native Linux option)
    echo    Run: build_apk.bat
    echo    Then choose option 3
) else (
    echo 1. Install Git and use GitHub Actions (no local setup needed)
    echo    Download: https://git-scm.com/download/win
)
echo.

echo ========================================
echo.
echo For detailed instructions, see: BUILD_APK.md
echo To start build, run: build_apk.bat
echo.
pause
