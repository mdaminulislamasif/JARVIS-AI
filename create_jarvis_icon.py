"""
Create JARVIS Icon for Installer and EXE
JARVIS আইকন তৈরি করুন ইনস্টলার এবং EXE এর জন্য
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_jarvis_icon():
    """Create a professional JARVIS icon"""
    
    print("Creating JARVIS icon...")
    print("JARVIS আইকন তৈরি করা হচ্ছে...")
    
    # Create multiple sizes for Windows icon
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Create image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        bg_color = (0, 150, 255, 255)  # Blue
        circle_color = (255, 255, 255, 255)  # White
        text_color = (255, 255, 255, 255)  # White
        
        # Draw outer circle (blue background)
        margin = size // 10
        draw.ellipse([margin, margin, size-margin, size-margin], 
                     fill=bg_color, outline=circle_color, width=max(1, size//32))
        
        # Draw "J" for JARVIS
        try:
            # Try to use a nice font
            font_size = size // 2
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception as e:

            print(f"⚠️ Error: {e}")
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Draw "J" in center
        text = "J"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - size // 10
        
        draw.text((x, y), text, fill=text_color, font=font)
        
        images.append(img)
        print(f"  ✅ Created {size}x{size} icon")
    
    # Save as ICO file
    images[0].save('jarvis_icon.ico', format='ICO', 
                   sizes=[(img.width, img.height) for img in images])
    
    print("\n✅ Icon created: jarvis_icon.ico")
    print("✅ আইকন তৈরি হয়েছে: jarvis_icon.ico")
    
    return 'jarvis_icon.ico'

def update_spec_with_icon():
    """Update PyInstaller spec files to include icon"""
    
    print("\nUpdating spec files with icon...")
    print("আইকন সহ spec ফাইল আপডেট করা হচ্ছে...")
    
    # Update jarvis.spec
    try:
        with open('jarvis.spec', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add icon parameter
        if 'icon=None' in content:
            content = content.replace('icon=None', "icon='jarvis_icon.ico'")
            
            with open('jarvis.spec', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  ✅ Updated jarvis.spec")
    except Exception as e:

        print(f"⚠️ Error: {e}")
        print("  ⚠️ jarvis.spec not found")
    
    # Update jarvis_installer.spec
    try:
        with open('jarvis_installer.spec', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add icon parameter
        if 'icon=None' in content:
            content = content.replace('icon=None', "icon='jarvis_icon.ico'")
            
            with open('jarvis_installer.spec', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  ✅ Updated jarvis_installer.spec")
    except Exception as e:

        print(f"⚠️ Error: {e}")
        print("  ⚠️ jarvis_installer.spec not found")
    
    print("\n✅ Spec files updated!")
    print("✅ Spec ফাইল আপডেট হয়েছে!")

def create_rebuild_script():
    """Create script to rebuild with icon"""
    
    script = '''@echo off
title Rebuilding JARVIS with Icon
echo ================================================================================
echo   REBUILDING JARVIS WITH ICON
echo   আইকন সহ JARVIS পুনর্নির্মাণ করা হচ্ছে
echo ================================================================================
echo.

echo [1/2] Rebuilding JARVIS Installer with icon...
pyinstaller --clean --noconfirm jarvis_installer.spec
if errorlevel 1 (
    echo   ❌ Installer build failed
    pause
    exit /b 1
)
echo   ✅ Installer built with icon
echo.

echo [2/2] Copying to Desktop...
if exist "dist\\JARVIS_Installer.exe" (
    copy /Y "dist\\JARVIS_Installer.exe" "C:\\Users\\PHP\\Desktop\\JARVIS_Installer.exe"
    echo   ✅ Copied to Desktop
) else (
    echo   ❌ Installer not found
)
echo.

echo ================================================================================
echo   ✅ DONE!
echo ================================================================================
echo.
echo   New installer with icon: C:\\Users\\PHP\\Desktop\\JARVIS_Installer.exe
echo   আইকন সহ নতুন ইনস্টলার: C:\\Users\\PHP\\Desktop\\JARVIS_Installer.exe
echo.
pause
'''
    
    with open('rebuild_with_icon.bat', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("\n✅ Created rebuild_with_icon.bat")
    print("✅ rebuild_with_icon.bat তৈরি হয়েছে")

def main():
    print("\n" + "=" * 80)
    print("  🎨 JARVIS ICON CREATOR")
    print("  🎨 JARVIS আইকন তৈরিকারী")
    print("=" * 80)
    print()
    
    # Check if PIL is available
    try:
        from PIL import Image
        print("✅ PIL/Pillow is available")
    except ImportError:
        print("❌ PIL/Pillow not found!")
        print("Installing Pillow...")
        import subprocess
        subprocess.run(['pip', 'install', 'pillow'], check=True)
        print("✅ Pillow installed")
    
    # Create icon
    icon_path = create_jarvis_icon()
    
    # Update spec files
    update_spec_with_icon()
    
    # Create rebuild script
    create_rebuild_script()
    
    print("\n" + "=" * 80)
    print("  ✅ ICON READY!")
    print("  ✅ আইকন প্রস্তুত!")
    print("=" * 80)
    print()
    print("  Files created:")
    print("  ✅ jarvis_icon.ico (Icon file)")
    print("  ✅ rebuild_with_icon.bat (Rebuild script)")
    print()
    print("  Next steps:")
    print("  1. Run: rebuild_with_icon.bat")
    print("  2. Wait for rebuild")
    print("  3. New installer with icon will be on Desktop!")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
