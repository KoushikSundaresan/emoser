# Quick Start: Build APK with GitHub Actions

You have Git installed! This is the easiest path. Follow these steps:

## Step 1: Create GitHub Account (1 minute)
Go to https://github.com and sign up (free)

## Step 2: Create a GitHub Repository (2 minutes)
1. Go to https://github.com/new
2. Repository name: `emoser`
3. Make it Public (so you can access the APK)
4. Click "Create repository"
5. Copy your repository URL (looks like: `https://github.com/YOUR_USERNAME/emoser.git`)

## Step 3: Push Your Code to GitHub (3 minutes)
Run these commands in PowerShell or Command Prompt:

```bash
cd c:\Users\Koushik\projectFiles\emoser

git init
git add .
git commit -m "Initial Emoser emotion wellness app"

git remote add origin https://github.com/YOUR_USERNAME/emoser.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username!

## Step 4: Watch the Build (10 minutes)
1. Go to your GitHub repository (https://github.com/YOUR_USERNAME/emoser)
2. Click the "Actions" tab
3. You should see "Build APK" workflow running
4. Wait for it to finish (typically 8-10 minutes)

## Step 5: Download Your APK
1. Click on the completed "Build APK" workflow
2. Scroll down to "Artifacts"
3. Download the `emoser-apk` zip file
4. Extract it to get: `emoser-debug.apk`

## That's it! You have your APK! 🎉

### Next Steps:
- Install on Android phone via USB or email the APK
- The APK is production-ready and shareable

### Troubleshooting:
- If build fails, check the GitHub Actions logs for details
- Common issue: Missing `buildozer.spec` (already created for you)
- If Android SDK fails, GitHub will show detailed error messages

---

## Alternative: Local Build with Docker

If you want to build locally and have Docker installed:

```bash
cd c:\Users\Koushik\projectFiles\emoser
mkdir output
docker build -t emoser-builder .
docker run -v "%cd%\output":/output emoser-builder
```

Then find your APK in the `output` folder.

---

**Estimated time to first APK: ~20 minutes** ⏱️
