@echo off
REM Emoser APK Build Script for Windows
REM This script provides multiple build options

setlocal enabledelayedexpansion
color 0A
title Emoser APK Builder

echo.
echo ========================================
echo   EMOSER APK BUILD OPTIONS
echo ========================================
echo.
echo Choose a build method:
echo.
echo 1. GitHub Actions (Cloud - RECOMMENDED)
echo    - Builds in the cloud automatically
echo    - Requires GitHub account
echo.
echo 2. Docker (Local Build)
echo    - Builds locally in a container
echo    - Requires Docker Desktop
echo.
echo 3. WSL2 (Windows Subsystem for Linux)
echo    - Native Linux build
echo    - Requires Windows 10/11 Pro
echo.
echo 0. Show detailed instructions
echo.
set /p choice="Enter your choice (0-3): "

if "%choice%"=="1" goto github_actions
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto wsl2
if "%choice%"=="0" goto instructions
goto end

:github_actions
echo.
echo GITHUB ACTIONS BUILD (Cloud Build)
echo ===================================
echo.
echo This will build your APK in the cloud at no cost.
echo.
echo Requirements:
echo - GitHub account (https://github.com)
echo - Git installed
echo.
echo Steps:
echo 1. Go to https://github.com/new and create a new repository
echo 2. Run these commands:
echo.
echo    cd /d "c:\Users\Koushik\projectFiles\emoser"
echo    git init
echo    git add .
echo    git commit -m "Initial Emoser commit"
echo    git remote add origin https://github.com/YOUR_USERNAME/emoser.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. After push completes, go to your GitHub repository
echo 4. Click the "Actions" tab
echo 5. Wait for the "Build APK" workflow to complete (~10 minutes)
echo 6. Click on the completed workflow and download the APK from "Artifacts"
echo.
echo The APK will be available as android-debug.apk
echo.
pause
goto end

:docker
echo.
echo DOCKER BUILD (Local)
echo ====================
echo.
echo Requirements:
echo - Docker Desktop for Windows installed
echo   Download from: https://www.docker.com/products/docker-desktop
echo.
echo Steps:
echo 1. Start Docker Desktop
echo 2. Run these commands:
echo.
echo    cd /d "c:\Users\Koushik\projectFiles\emoser"
echo    mkdir output
echo    docker build -t emoser-builder .
echo    docker run -v "%%cd%%\output":/output emoser-builder
echo.
echo 3. Wait for build to complete (~15-20 minutes)
echo 4. Check "output" folder for the APK
echo.
pause
goto end

:wsl2
echo.
echo WSL2 BUILD (Windows Subsystem for Linux)
echo =========================================
echo.
echo Requirements:
echo - Windows 10/11 Pro with Hyper-V enabled
echo.
echo Steps:
echo 1. Run in PowerShell (as Administrator):
echo    wsl --install -d Ubuntu-22.04
echo.
echo 2. Restart your computer
echo.
echo 3. Run these commands in WSL terminal:
echo.
echo    sudo apt-get update
echo    sudo apt-get install -y python3-pip openjdk-11-jdk android-sdk
echo    pip3 install buildozer cython kivy
echo    cd /mnt/c/Users/Koushik/projectFiles/emoser
echo    buildozer android debug
echo.
echo 4. APK will be in: bin/
echo.
pause
goto end

:instructions
cls
echo Detailed instructions saved in: BUILD_APK.md
echo Please read that file for comprehensive information.
echo.
type BUILD_APK.md
pause
goto end

:end
echo.
echo Done!
pause
