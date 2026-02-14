# App Icon Guide for Emoser APK

## Quick Setup (Automatic)

Run this command to auto-generate icons with the app's pastel colors:

```bash
python create_icon.py
```

This creates properly sized icons in the `images/` folder. Done! ✓

---

## Manual Setup (If Using Custom Icon)

### Step 1: Prepare Your Icon Image

You need a PNG image of at least **512x512 pixels**. Recommended: **1024x1024** or higher.

### Step 2: Create Icons Folder

```bash
mkdir images
```

### Step 3: Copy/Create Icons

Place your icon file as:
- `images/icon-192x192.png` - App launch icon
- `images/icon-512x512.png` - Google Play store icon (optional)

Or use the auto-generator:
```bash
python create_icon.py
```

### Step 4: Verify buildozer.spec

Check that these settings exist in `buildozer.spec`:

```ini
source.include_patterns = assets/*,images/*.png
android.icon = images/icon-192x192.png
```

Both are already set up for you!

---

## Icon Specifications

### Android App Icon Requirements:
- **Format:** PNG with transparency
- **Minimum size:** 192x192 pixels
- **Recommended:** 512x512 or 1024x1024
- **Background:** Transparent or solid color
- **Safe area:** Center 66% will always be visible

### Current Setup:
- Buildozer.spec configured to use `images/icon-192x192.png`
- Auto-generator creates pastel-themed icons matching your app colors
- Icons included in APK automatically

---

## Using Your Own Icon

### Option A: Use Design Tool
1. Create custom icon in Figma, Photoshop, or Canva
2. Export as PNG (512x512 or larger)
3. Save as `images/icon-192x192.png`

### Option B: Use Online Tool
1. Upload your design to:
   - https://www.canva.com (free)
   - https://pixlr.com (free)
   - https://www.photopea.com (free)
2. Export as PNG
3. Save as `images/icon-192x192.png`

### Option C: Use Generated Icon
Run auto-generator to create pastel-themed icon:
```bash
python create_icon.py
```

---

## GitHub Actions Integration

The icon is **automatically included** in the APK when using GitHub build!

### Workflow:
1. Generate/prepare `images/icon-192x192.png`
2. Commit and push to GitHub:
   ```bash
   git add images/icon-192x192.png
   git commit -m "Add app icon"
   git push origin main
   ```
3. GitHub Actions automatically includes it in the APK build

---

## Verify Icon is Included

After downloading APK:

### On Windows/Mac:
1. Rename `.apk` to `.zip`
2. Extract it
3. Look in `res/drawable/` for icon files

### On Android Phone:
Install APK and check app drawer - icon appears automatically

---

## Troubleshooting

### Icon not appearing in APK?
- ✓ Verify `images/icon-192x192.png` exists
- ✓ Check buildozer.spec has `android.icon = images/icon-192x192.png`
- ✓ Rebuild APK

### Icon looks blurry?
- Use higher resolution image (512x512 minimum)
- Rebuild APK

### Icon wrong size?
- Must be square (512x512, not 512x300)
- Padding/margins are OK, but image must be square

---

## What We've Set Up for You

✓ **buildozer.spec** - Icon paths configured
✓ **create_icon.py** - Auto-generator script (pastel colors)
✓ **GitHub Actions** - Automatically includes icons in build

## Next Steps

1. **Generate icon:**
   ```bash
   python create_icon.py
   ```

2. **Or use your own** - place in `images/icon-192x192.png`

3. **Push to GitHub:**
   ```bash
   git add images/
   git commit -m "Add app icons"
   git push origin main
   ```

4. **Build APK** - GitHub Actions will include your icon automatically!

---

## Icon Examples

### Generated Icon (Automatic)
- Pastel background (#FFF5F7)
- Coral circle (#FF6F61)
- Lavender outline (#C1A3E0)
- Minimalist wellness theme

### Custom Icon
- Add your own PNG
- Must be 192x192 or larger
- Transparent background recommended

---

That's it! Your APK will have your custom icon. 🎨
