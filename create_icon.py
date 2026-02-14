#!/usr/bin/env python3
"""
Simple icon generator for Emoser APK
Creates a basic app icon with pastel colors
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_emoser_icon():
    """Create an Emoser icon with pastel colors"""
    
    # Icon sizes needed for Android
    sizes = {
        'icon-192x192.png': 192,
        'icon-512x512.png': 512,
    }
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Pastel colors from the app
    bg_color = (255, 245, 247)  # #FFF5F7 soft pastel
    coral = (255, 111, 97)       # #FF6F61 warm coral
    lavender = (193, 163, 224)   # #C1A3E0 muted lavender
    
    for filename, size in sizes.items():
        # Create image with pastel background
        img = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw a circle for the main visual
        margin = size // 8
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=coral,
            outline=lavender,
            width=max(1, size // 64)
        )
        
        # Draw inner circle (heart-like shape for wellness)
        inner_margin = size // 4
        draw.ellipse(
            [inner_margin, inner_margin, size - inner_margin, size - inner_margin],
            fill=bg_color
        )
        
        # Save the icon
        img.save(os.path.join('images', filename))
        print(f"✓ Created {filename}")
    
    print("\n✓ Icons created in images/ folder")
    print("  - icon-192x192.png (for adaptive icon)")
    print("  - icon-512x512.png (for app store)")

if __name__ == '__main__':
    try:
        create_emoser_icon()
    except ImportError:
        print("PIL (Pillow) not installed. Installing...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'Pillow'])
        create_emoser_icon()
