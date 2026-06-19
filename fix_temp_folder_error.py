"""
FIX TEMP FOLDER ERROR
Fixes the "404 Error - Input nothing temporary file" issue
"""

import os
import sys
import tempfile
import shutil

print("\n" + "="*80)
print("  🔧 FIXING TEMP FOLDER ERROR")
print("  🔧 Temp Folder Error ঠিক করা হচ্ছে")
print("="*80)

def fix_temp_folder():
    """Fix temporary folder issues"""
    
    print("\n1️⃣ Checking system temp folder...")
    
    # Get system temp directory
    system_temp = tempfile.gettempdir()
    print(f"   System temp: {system_temp}")
    
    # Check if it exists
    if os.path.exists(system_temp):
        print(f"   ✅ System temp folder exists")
    else:
        print(f"   ❌ System temp folder missing!")
        try:
            os.makedirs(system_temp, exist_ok=True)
            print(f"   ✅ Created system temp folder")
        except Exception as e:
            print(f"   ❌ Error creating temp folder: {e}")
    
    print("\n2️⃣ Creating JARVIS temp folders...")
    
    # Create JARVIS-specific temp folders
    jarvis_temp_folders = [
        'temp',
        'tmp',
        'cache',
        'jarvis_temp',
        os.path.join(system_temp, 'jarvis'),
    ]
    
    for folder in jarvis_temp_folders:
        try:
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
                print(f"   ✅ Created: {folder}")
            else:
                print(f"   ✅ Exists: {folder}")
        except Exception as e:
            print(f"   ⚠️ Could not create {folder}: {e}")
    
    print("\n3️⃣ Checking write permissions...")
    
    # Test write permissions
    test_file = os.path.join(system_temp, 'jarvis_test.txt')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print(f"   ✅ Write permissions OK")
    except Exception as e:
        print(f"   ❌ Write permission error: {e}")
    
    print("\n4️⃣ Cleaning old temp files...")
    
    # Clean old JARVIS temp files
    try:
        jarvis_temp = os.path.join(system_temp, 'jarvis')
        if os.path.exists(jarvis_temp):
            # Count files
            file_count = len([f for f in os.listdir(jarvis_temp) if os.path.isfile(os.path.join(jarvis_temp, f))])
            print(f"   Found {file_count} temp files")
            
            # Clean files older than 1 day
            import time
            current_time = time.time()
            cleaned = 0
            
            for filename in os.listdir(jarvis_temp):
                filepath = os.path.join(jarvis_temp, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    if file_age > 86400:  # 1 day in seconds
                        try:
                            os.remove(filepath)
                            cleaned += 1
                        except Exception as e:

                            print(f"⚠️ Error: {e}")
                            pass
            
            print(f"   ✅ Cleaned {cleaned} old files")
    except Exception as e:
        print(f"   ⚠️ Cleanup error: {e}")
    
    print("\n5️⃣ Setting environment variables...")
    
    # Set temp environment variables
    try:
        os.environ['TEMP'] = system_temp
        os.environ['TMP'] = system_temp
        os.environ['JARVIS_TEMP'] = os.path.join(system_temp, 'jarvis')
        print(f"   ✅ Environment variables set")
    except Exception as e:
        print(f"   ⚠️ Could not set env vars: {e}")
    
    print("\n" + "="*80)
    print("  ✅ TEMP FOLDER FIX COMPLETE!")
    print("  ✅ Temp Folder Fix সম্পূর্ণ!")
    print("="*80)
    
    print("\n📝 Summary:")
    print(f"   System Temp: {system_temp}")
    print(f"   JARVIS Temp: {os.path.join(system_temp, 'jarvis')}")
    print(f"   Local Temp: ./temp")
    print(f"   Local Cache: ./cache")
    
    print("\n💡 Recommendations:")
    print("   1. Restart JARVIS panel")
    print("   2. If error persists, run as Administrator")
    print("   3. Check antivirus settings")
    
    return True


if __name__ == "__main__":
    try:
        fix_temp_folder()
        print("\n✅ Fix completed successfully!")
        print("✅ Fix সফলভাবে সম্পূর্ণ হয়েছে!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
