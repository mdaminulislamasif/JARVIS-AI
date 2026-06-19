"""
Create Portable JARVIS.exe
Creates a standalone executable that can be copied to any Windows computer
and run without installation.

Bengali: Ekta portable JARVIS.exe toiri korbe jeta kono computer e copy kore
run kora jabe, kono installation lagbe na.
"""
import os
import sys
import subprocess

print("=" * 80)
print("  PORTABLE JARVIS.EXE CREATOR")
print("  পোর্টেবল JARVIS.exe তৈরি করুন")
print("=" * 80)
print()

# Check if PyInstaller is installed
print("[1/6] Checking PyInstaller...")
try:
    import PyInstaller
    print("    ✅ PyInstaller installed")
except ImportError:
    print("    ❌ PyInstaller not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("    ✅ PyInstaller installed successfully")

# Create main JARVIS launcher script
print("\n[2/6] Creating JARVIS launcher script...")
launcher_code = '''"""
JARVIS - Portable AI Assistant
Can be copied and run on any Windows computer
"""
import os
import sys
import subprocess
import sqlite3
from pathlib import Path

# Get the directory where the exe is located
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up paths
DB_PATH = os.path.join(BASE_DIR, 'jarvis_memory.db')
CONFIG_PATH = os.path.join(BASE_DIR, 'jarvis_config.txt')

def check_database():
    """Check if database exists and is valid"""
    if not os.path.exists(DB_PATH):
        print("⚠️  Database not found. Creating new database...")
        create_database()
        return True
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        conn.execute("PRAGMA quick_check").fetchall()
        conn.close()
        return True
    except Exception as e:

        print(f"⚠️ Error: {e}")
        print("⚠️  Database corrupted. Creating new database...")
        os.rename(DB_PATH, DB_PATH + '.backup')
        create_database()
        return True

def create_database():
    """Create a fresh database with basic schema"""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            jarvis_msg TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            category TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT,
            source TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE NOT NULL,
            preference_value TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add basic system info
    import platform
    cursor.execute("INSERT OR REPLACE INTO system_info (key, value, category) VALUES (?, ?, ?)",
                   ('os_name', platform.system(), 'system'))
    cursor.execute("INSERT OR REPLACE INTO system_info (key, value, category) VALUES (?, ?, ?)",
                   ('hostname', platform.node(), 'system'))
    cursor.execute("INSERT OR REPLACE INTO system_info (key, value, category) VALUES (?, ?, ?)",
                   ('jarvis_version', '2.0 Portable', 'software'))
    
    conn.commit()
    conn.close()
    print("✅ Database created successfully")

def check_config():
    """Check if config file exists"""
    if not os.path.exists(CONFIG_PATH):
        print("⚠️  Config file not found. Creating default config...")
        with open(CONFIG_PATH, 'w') as f:
            f.write("# JARVIS Configuration\\n")
            f.write("# Add your API keys here (one per line)\\n")
            f.write("# Example: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\\n")
        print("✅ Config file created. Please add your API keys.")
        return False
    return True

def main():
    """Main JARVIS launcher"""
    print("=" * 70)
    print("  JARVIS - Portable AI Assistant")
    print("  পোর্টেবল AI সহায়ক")
    print("=" * 70)
    print(f"\\nRunning from: {BASE_DIR}")
    print(f"Database: {DB_PATH}")
    print(f"Config: {CONFIG_PATH}\\n")
    
    # Check database
    print("[1/3] Checking database...")
    check_database()
    
    # Check config
    print("\\n[2/3] Checking configuration...")
    if not check_config():
        print("\\n⚠️  Please edit jarvis_config.txt and add your API keys")
        print("    Then run JARVIS again.\\n")
        input("Press Enter to exit...")
        return
    
    # Check if main JARVIS script exists
    print("\\n[3/3] Starting JARVIS...")
    
    # Try to import and run JARVIS
    try:
        # Add current directory to path
        sys.path.insert(0, BASE_DIR)
        
        # Check if core modules exist
        core_path = os.path.join(BASE_DIR, 'core')
        if os.path.exists(core_path):
            print("✅ Core modules found")
            
            # Import and run JARVIS
            try:
                from core import brain
                print("\\n" + "=" * 70)
                print("  JARVIS STARTED SUCCESSFULLY!")
                print("  JARVIS সফলভাবে চালু হয়েছে!")
                print("=" * 70)
                print("\\nType 'exit' or 'quit' to stop JARVIS\\n")
                
                # Simple chat loop
                # WARNING: Infinite loop - ensure break condition exists
                while True:
                    user_input = input("You: ")
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        print("\\nJARVIS: Goodbye! আবার দেখা হবে!\\n")
                        break
                    
                    # Process with JARVIS brain
                    response = brain.process_query(user_input)
                    print(f"JARVIS: {response}\\n")
                    
            except ImportError as e:
                print(f"❌ Error importing JARVIS modules: {e}")
                print("\\nPlease ensure all JARVIS files are in the same folder as the .exe")
        else:
            print("❌ Core modules not found")
            print("\\nPlease ensure the 'core' folder is in the same directory as JARVIS.exe")
            print("\\nRequired structure:")
            print("  JARVIS.exe")
            print("  jarvis_memory.db")
            print("  jarvis_config.txt")
            print("  core/")
            print("    brain.py")
            print("    database.py")
            print("    auth.py")
            print("  engine/")
            print("    (other modules)")
    
    except Exception as e:
        print(f"\\n❌ Error starting JARVIS: {e}")
        import traceback
        traceback.print_exc()
    
    print("\\n" + "=" * 70)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''

with open('jarvis_launcher.py', 'w', encoding='utf-8') as f:
    f.write(launcher_code)

print("    ✅ Launcher script created: jarvis_launcher.py")

# Create PyInstaller spec file
print("\n[3/6] Creating PyInstaller configuration...")
spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['jarvis_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('core', 'core'),
        ('engine', 'engine'),
        ('jarvis_memory.db.fixed-*', '.'),
        ('jarvis_config.txt', '.'),
    ],
    hiddenimports=[
        'sqlite3',
        'google.genai',
        'google.generativeai',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JARVIS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='jarvis_icon.ico' if os.path.exists('jarvis_icon.ico') else None,
)
'''

with open('jarvis.spec', 'w', encoding='utf-8') as f:
    f.write(spec_content)

print("    ✅ PyInstaller spec created: jarvis.spec")

# Create build script
print("\n[4/6] Creating build script...")
build_script = '''@echo off
echo ================================================================================
echo   BUILDING PORTABLE JARVIS.EXE
echo   পোর্টেবল JARVIS.exe তৈরি করা হচ্ছে
echo ================================================================================
echo.

echo [1/3] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo     Done

echo.
echo [2/3] Building JARVIS.exe with PyInstaller...
pyinstaller --clean --onefile --console jarvis_launcher.py --name JARVIS
echo     Done

echo.
echo [3/3] Creating portable package...
if not exist "JARVIS_Portable" mkdir "JARVIS_Portable"
copy dist\\JARVIS.exe "JARVIS_Portable\\"
xcopy /E /I /Y core "JARVIS_Portable\\core"
xcopy /E /I /Y engine "JARVIS_Portable\\engine"
copy jarvis_memory.db.fixed-* "JARVIS_Portable\\jarvis_memory.db" 2>nul
copy jarvis_config.txt "JARVIS_Portable\\" 2>nul
echo     Done

echo.
echo ================================================================================
echo   BUILD COMPLETE!
echo   তৈরি সম্পন্ন!
echo ================================================================================
echo.
echo Portable JARVIS created in: JARVIS_Portable\\
echo.
echo You can now:
echo   1. Copy the entire JARVIS_Portable folder to any Windows computer
echo   2. Run JARVIS.exe
echo   3. No installation needed!
echo.
echo আপনি এখন:
echo   1. JARVIS_Portable ফোল্ডারটি যেকোনো Windows কম্পিউটারে কপি করুন
echo   2. JARVIS.exe চালান
echo   3. কোনো ইনস্টলেশন লাগবে না!
echo.
pause
'''

with open('build_jarvis.bat', 'w', encoding='utf-8') as f:
    f.write(build_script)

print("    ✅ Build script created: build_jarvis.bat")

# Create README for portable version
print("\n[5/6] Creating README for portable version...")
readme_content = '''# JARVIS Portable - পোর্টেবল JARVIS

## What is this? / এটা কি?

This is a portable version of JARVIS that can be copied to any Windows computer and run without installation.

এটি JARVIS এর একটি পোর্টেবল সংস্করণ যা যেকোনো Windows কম্পিউটারে কপি করে ইনস্টলেশন ছাড়াই চালানো যায়।

## How to Use / কিভাবে ব্যবহার করবেন

### English:
1. Copy the entire `JARVIS_Portable` folder to any Windows computer
2. Open the folder
3. Double-click `JARVIS.exe`
4. JARVIS will start automatically!

### বাংলা:
1. সম্পূর্ণ `JARVIS_Portable` ফোল্ডারটি যেকোনো Windows কম্পিউটারে কপি করুন
2. ফোল্ডারটি খুলুন
3. `JARVIS.exe` তে ডাবল ক্লিক করুন
4. JARVIS স্বয়ংক্রিয়ভাবে চালু হবে!

## Folder Structure / ফোল্ডার গঠন

```
JARVIS_Portable/
├── JARVIS.exe              (Main executable / মূল এক্সিকিউটেবল)
├── jarvis_memory.db        (Database / ডাটাবেস)
├── jarvis_config.txt       (Configuration / কনফিগারেশন)
├── core/                   (Core modules / মূল মডিউল)
│   ├── brain.py
│   ├── database.py
│   └── ...
└── engine/                 (Engine modules / ইঞ্জিন মডিউল)
    ├── voice.py
    └── ...
```

## Requirements / প্রয়োজনীয়তা

- Windows 7 or higher / Windows 7 বা তার উপরে
- No Python installation needed! / Python ইনস্টলেশন লাগবে না!
- No internet required for basic functions / মৌলিক কাজের জন্য ইন্টারনেট লাগবে না

## Features / বৈশিষ্ট্য

✅ Fully portable - no installation needed
✅ Works on any Windows computer
✅ Includes complete database with:
   - Windows 10 Pro information
   - Flipper Zero knowledge
   - Cyber attack encyclopedia
✅ All data stored locally
✅ Can be run from USB drive

✅ সম্পূর্ণ পোর্টেবল - ইনস্টলেশন লাগবে না
✅ যেকোনো Windows কম্পিউটারে কাজ করে
✅ সম্পূর্ণ ডাটাবেস অন্তর্ভুক্ত:
   - Windows 10 Pro তথ্য
   - Flipper Zero জ্ঞান
   - সাইবার আক্রমণ এনসাইক্লোপিডিয়া
✅ সব ডেটা স্থানীয়ভাবে সংরক্ষিত
✅ USB ড্রাইভ থেকে চালানো যায়

## Configuration / কনফিগারেশন

Edit `jarvis_config.txt` to add your API keys:

আপনার API কী যোগ করতে `jarvis_config.txt` সম্পাদনা করুন:

```
# Add your Google API keys here
AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Troubleshooting / সমস্যা সমাধান

### English:
- **JARVIS won't start**: Make sure all files are in the same folder
- **Database error**: Delete `jarvis_memory.db` and restart (will create new database)
- **Missing modules**: Ensure `core` and `engine` folders are present

### বাংলা:
- **JARVIS চালু হচ্ছে না**: নিশ্চিত করুন সব ফাইল একই ফোল্ডারে আছে
- **ডাটাবেস ত্রুটি**: `jarvis_memory.db` মুছে দিন এবং পুনরায় চালু করুন (নতুন ডাটাবেস তৈরি হবে)
- **মডিউল নেই**: নিশ্চিত করুন `core` এবং `engine` ফোল্ডার আছে

## Support / সহায়তা

For help, check the documentation files:
- DATABASE_README.md
- CYBER_ATTACKS_REFERENCE.md
- FLIPPER_ZERO_REFERENCE.md

সাহায্যের জন্য, ডকুমেন্টেশন ফাইল দেখুন:
- DATABASE_README.md
- CYBER_ATTACKS_REFERENCE.md
- FLIPPER_ZERO_REFERENCE.md

## Version / সংস্করণ

JARVIS Portable v2.0
Created: May 4, 2026
'''

with open('PORTABLE_README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("    ✅ README created: PORTABLE_README.md")

# Create instructions
print("\n[6/6] Creating build instructions...")
instructions = """
================================================================================
  HOW TO BUILD PORTABLE JARVIS.EXE
  পোর্টেবল JARVIS.exe কিভাবে তৈরি করবেন
================================================================================

STEP 1: Install PyInstaller (if not already installed)
        PyInstaller ইনস্টল করুন (যদি ইতিমধ্যে না থাকে)
        
        Command: pip install pyinstaller

STEP 2: Run the build script
        বিল্ড স্ক্রিপ্ট চালান
        
        Command: build_jarvis.bat
        
        Or manually: pyinstaller --clean --onefile --console jarvis_launcher.py --name JARVIS

STEP 3: Find your portable JARVIS
        আপনার পোর্টেবল JARVIS খুঁজুন
        
        Location: JARVIS_Portable folder
        স্থান: JARVIS_Portable ফোল্ডার

STEP 4: Copy to any computer
        যেকোনো কম্পিউটারে কপি করুন
        
        - Copy the entire JARVIS_Portable folder
        - সম্পূর্ণ JARVIS_Portable ফোল্ডার কপি করুন
        
        - Can be copied to:
          - USB drive
          - External hard drive
          - Network share
          - Cloud storage
          
        - কপি করা যায়:
          - USB ড্রাইভে
          - এক্সটার্নাল হার্ড ড্রাইভে
          - নেটওয়ার্ক শেয়ারে
          - ক্লাউড স্টোরেজে

STEP 5: Run on any Windows computer
        যেকোনো Windows কম্পিউটারে চালান
        
        - No installation needed!
        - Just double-click JARVIS.exe
        
        - কোনো ইনস্টলেশন লাগবে না!
        - শুধু JARVIS.exe তে ডাবল ক্লিক করুন

================================================================================
  WHAT WILL BE INCLUDED
  কি অন্তর্ভুক্ত থাকবে
================================================================================

✅ JARVIS.exe (standalone executable)
✅ jarvis_memory.db (complete database with 100 entries)
✅ jarvis_config.txt (configuration file)
✅ core/ folder (all core modules)
✅ engine/ folder (all engine modules)
✅ All documentation files

✅ JARVIS.exe (স্বতন্ত্র এক্সিকিউটেবল)
✅ jarvis_memory.db (100 এন্ট্রি সহ সম্পূর্ণ ডাটাবেস)
✅ jarvis_config.txt (কনফিগারেশন ফাইল)
✅ core/ ফোল্ডার (সব মূল মডিউল)
✅ engine/ ফোল্ডার (সব ইঞ্জিন মডিউল)
✅ সব ডকুমেন্টেশন ফাইল

================================================================================
  ADVANTAGES
  সুবিধা
================================================================================

✅ No Python installation required on target computer
✅ No dependency installation needed
✅ Works offline (except for AI features)
✅ Can run from USB drive
✅ Complete database included
✅ Easy to share with others
✅ No registry modifications
✅ No admin rights needed

✅ টার্গেট কম্পিউটারে Python ইনস্টলেশন লাগবে না
✅ কোনো ডিপেন্ডেন্সি ইনস্টলেশন লাগবে না
✅ অফলাইনে কাজ করে (AI ফিচার ছাড়া)
✅ USB ড্রাইভ থেকে চালানো যায়
✅ সম্পূর্ণ ডাটাবেস অন্তর্ভুক্ত
✅ অন্যদের সাথে শেয়ার করা সহজ
✅ কোনো রেজিস্ট্রি পরিবর্তন নেই
✅ অ্যাডমিন অধিকার লাগবে না

================================================================================
  FILE SIZE
  ফাইল সাইজ
================================================================================

Approximate size: 50-100 MB (depending on included modules)
আনুমানিক সাইজ: 50-100 MB (অন্তর্ভুক্ত মডিউলের উপর নির্ভর করে)

================================================================================
"""

with open('BUILD_INSTRUCTIONS.txt', 'w', encoding='utf-8') as f:
    f.write(instructions)

print("    ✅ Instructions created: BUILD_INSTRUCTIONS.txt")

# Final summary
print("\n" + "=" * 80)
print("  SETUP COMPLETE!")
print("  সেটআপ সম্পন্ন!")
print("=" * 80)
print("\nFiles created:")
print("  ✅ jarvis_launcher.py - Main launcher script")
print("  ✅ jarvis.spec - PyInstaller configuration")
print("  ✅ build_jarvis.bat - Automated build script")
print("  ✅ PORTABLE_README.md - User instructions")
print("  ✅ BUILD_INSTRUCTIONS.txt - Build instructions")
print("\nNext steps:")
print("  1. Run: build_jarvis.bat")
print("  2. Wait for build to complete")
print("  3. Find JARVIS.exe in JARVIS_Portable folder")
print("  4. Copy folder to any computer and run!")
print("\nপরবর্তী পদক্ষেপ:")
print("  1. চালান: build_jarvis.bat")
print("  2. বিল্ড সম্পন্ন হওয়ার জন্য অপেক্ষা করুন")
print("  3. JARVIS_Portable ফোল্ডারে JARVIS.exe খুঁজুন")
print("  4. ফোল্ডারটি যেকোনো কম্পিউটারে কপি করে চালান!")
print("=" * 80)
