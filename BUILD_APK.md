# Emoser APK Build Guide

This guide provides multiple methods to build the Emoser APK on Windows.

## Quick Reference
- **buildozer.spec** - Configuration for all build methods
- **Dockerfile** - For Docker-based builds
- **.github/workflows/build.yml** - For GitHub Actions cloud builds

---

## Method 1: GitHub Actions (EASIEST - Cloud Build) ⭐ Recommended

**Requirements:**
- GitHub account (free)
- Git installed on your computer

**Steps:**

1. Initialize a git repository:
```bash
cd c:\Users\Koushik\projectFiles\emoser
git init
git add .
git commit -m "Initial commit"
```

2. Create a GitHub repository and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/emoser.git
git branch -M main
git push -u origin main
```

3. The APK will build automatically in GitHub Actions:
   - Go to your repository on GitHub.com
   - Click "Actions" tab
   - Wait for "Build APK" workflow to complete
   - Download the APK from "Artifacts"

**Advantages:**
- ✅ No local setup required
- ✅ Automatic builds on every push
- ✅ Free for public repositories
- ✅ Builds in the cloud

---

## Method 2: Docker (Local Build) 

**Requirements:**
- Docker Desktop for Windows installed ([Download](https://www.docker.com/products/docker-desktop))
- ~10-15 GB disk space for Android SDK

**Steps:**

1. Create an output directory:
```bash
mkdir c:\Users\Koushik\projectFiles\emoser\output
```

2. Build the Docker image:
```bash
cd c:\Users\Koushik\projectFiles\emoser
docker build -t emoser-builder .
```

3. Run the builder:
```bash
docker run -v "%cd%\output":/output emoser-builder
```

4. The APK will be in the `output` folder:
```bash
dir output
```

**Advantages:**
- ✅ Self-contained environment
- ✅ No conflicts with system Python
- ✅ Consistent builds
- ⚠️ Slower first run (downloads ~10GB)
- ⚠️ Requires Docker Desktop

---

## Method 3: WSL2 (Windows Subsystem for Linux)

**Requirements:**
- Windows 10/11 Pro or higher
- Enable Hyper-V

**Quick Setup:**

1. Install WSL2:
```powershell
wsl --install -d Ubuntu-22.04
```

2. Set up in WSL2:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip openjdk-11-jdk android-sdk
pip3 install buildozer cython kivy
cd /mnt/c/Users/Koushik/projectFiles/emoser
buildozer android debug
```

3. APK will be in `bin/` folder

**Advantages:**
- ✅ Native Linux build environment
- ✅ Faster than Docker
- ⚠️ Requires specific Windows versions
- ⚠️ Steeper learning curve

---

## Method 4: Buildozer on Windows (Direct - Not Recommended)

Buildozer is designed for Linux. While it might partially work with manual Android SDK setup, it's not officially supported on Windows.

---

## Troubleshooting

### APK build fails
1. Check buildozer.spec is in the project root
2. Ensure main.py is in the project root
3. Check all required Python modules in requirements

### Docker build is slow
- First run downloads ~10GB of Android SDK
- Subsequent builds are faster
- You can use `docker images` to see existing images

### Need to modify app name or version
Edit `buildozer.spec`:
```ini
title = Emoser - Emotion Wellness
package.name = emoser
package.domain = org.emoser
version = 0.1
```

---

## Recommended Path

**For fastest results (cloud build):**
1. Use Method 1: GitHub Actions
2. Takes ~5-10 minutes first time
3. Automatic for future updates

**For local development:**
1. Use Method 3: WSL2 (if you have Win 10/11 Pro)
2. Or use Method 2: Docker (more reliable)

---

## Files Included

- `buildozer.spec` - All build configurations
- `Dockerfile` - Docker build instructions
- `.github/workflows/build.yml` - GitHub Actions workflow

All configurations are ready to use!
