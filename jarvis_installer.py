"""
JARVIS One-Click Installer
Installs JARVIS with all dependencies automatically

Bengali: JARVIS ওয়ান-ক্লিক ইনস্টলার
সব ডিপেন্ডেন্সি সহ JARVIS স্বয়ংক্রিয়ভাবে ইনস্টল করে
"""

import os
import sys
import subprocess
import shutil
import winreg
from pathlib import Path

class JarvisInstaller:
    def __init__(self):
        self.desktop = Path.home() / "Desktop"
        self.install_dir = self.desktop / "JARVIS"
        self.python_required = "3.8"
        
    def print_header(self):
        print("=" * 80)
        print("  🤖 JARVIS ONE-CLICK INSTALLER")
        print("  🤖 JARVIS ওয়ান-ক্লিক ইনস্টলার")
        print("=" * 80)
        print()
        print("  This will install JARVIS on your Desktop")
        print("  এটি আপনার ডেস্কটপে JARVIS ইনস্টল করবে")
        print()
        print("  Installation includes:")
        print("  ✅ JARVIS Master Algorithm")
        print("  ✅ Complete Database (310+ entries)")
        print("  ✅ All Features (Gaming, 3D, System, etc.)")
        print("  ✅ Desktop Shortcut")
        print("  ✅ Start Menu Entry")
        print("=" * 80)
        print()
    
    def check_python(self):
        """Check if Python is installed"""
        print("[1/8] Checking Python installation...")
        try:
            version = sys.version.split()[0]
            print(f"  ✅ Python {version} found")
            return True
        except Exception as e:

            print(f"⚠️ Error: {e}")
            print("  ❌ Python not found!")
            print("  Please install Python from: https://www.python.org/downloads/")
            return False
    
    def create_install_directory(self):
        """Create installation directory"""
        print("\n[2/8] Creating installation directory...")
        try:
            if self.install_dir.exists():
                print(f"  ⚠️ Directory exists: {self.install_dir}")
                response = input("  Overwrite? (Y/N): ").strip().upper()
                if response == 'Y':
                    shutil.rmtree(self.install_dir)
                    print("  ✅ Old installation removed")
                else:
                    print("  ❌ Installation cancelled")
                    return False
            
            self.install_dir.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {self.install_dir}")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            return False
    
    def copy_files(self):
        """Copy JARVIS files"""
        print("\n[3/8] Copying JARVIS files...")
        try:
            # Get current directory (where installer is running)
            current_dir = Path(__file__).parent
            
            # Files to copy
            files_to_copy = [
                'jarvis_master_algorithm.py',
                'jarvis_memory.db.fixed-20260504-091901',
                'MASTER_ALGORITHM_GUIDE.txt',
                'JARVIS_COMPLETE_CAPABILITIES.md',
                'FINAL_COMPLETE_SUMMARY.txt',
                'DATABASE_README.md'
            ]
            
            copied = 0
            for file in files_to_copy:
                src = current_dir / file
                if src.exists():
                    dst = self.install_dir / file
                    shutil.copy2(src, dst)
                    print(f"  ✅ Copied: {file}")
                    copied += 1
                else:
                    print(f"  ⚠️ Not found: {file}")
            
            print(f"  ✅ Copied {copied} files")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n[4/8] Installing dependencies...")
        try:
            # No external dependencies needed - using built-in modules only
            print("  ✅ All dependencies are built-in (sqlite3, json, datetime)")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            return False
    
    def create_launcher(self):
        """Create launcher script"""
        print("\n[5/8] Creating launcher...")
        try:
            launcher_content = f"""@echo off
title JARVIS AI Assistant
cd /d "{self.install_dir}"
python jarvis_master_algorithm.py
pause
"""
            launcher_path = self.install_dir / "JARVIS.bat"
            with open(launcher_path, 'w') as f:
                f.write(launcher_content)
            print(f"  ✅ Created: JARVIS.bat")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            return False
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        print("\n[6/8] Creating desktop shortcut...")
        try:
            # Create VBS script to create shortcut
            vbs_content = f"""Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{self.desktop}\\JARVIS.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{self.install_dir}\\JARVIS.bat"
oLink.WorkingDirectory = "{self.install_dir}"
oLink.Description = "JARVIS AI Assistant"
oLink.Save
"""
            vbs_path = self.install_dir / "create_shortcut.vbs"
            with open(vbs_path, 'w') as f:
                f.write(vbs_content)
            
            # Execute VBS script
            subprocess.run(['cscript', '//nologo', str(vbs_path)], 
                         check=True, capture_output=True)
            
            # Clean up VBS file
            vbs_path.unlink()
            
            print(f"  ✅ Created: Desktop\\JARVIS.lnk")
            return True
        except Exception as e:
            print(f"  ⚠️ Shortcut creation failed: {e}")
            print("  You can manually run: JARVIS\\JARVIS.bat")
            return True  # Don't fail installation
    
    def create_start_menu_entry(self):
        """Create Start Menu entry"""
        print("\n[7/8] Creating Start Menu entry...")
        try:
            start_menu = Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            jarvis_menu = start_menu / "JARVIS"
            jarvis_menu.mkdir(exist_ok=True)
            
            # Create VBS script for Start Menu shortcut
            vbs_content = f"""Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{jarvis_menu}\\JARVIS.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{self.install_dir}\\JARVIS.bat"
oLink.WorkingDirectory = "{self.install_dir}"
oLink.Description = "JARVIS AI Assistant"
oLink.Save
"""
            vbs_path = self.install_dir / "create_menu.vbs"
            with open(vbs_path, 'w') as f:
                f.write(vbs_content)
            
            # Execute VBS script
            subprocess.run(['cscript', '//nologo', str(vbs_path)], 
                         check=True, capture_output=True)
            
            # Clean up VBS file
            vbs_path.unlink()
            
            print(f"  ✅ Created: Start Menu\\JARVIS")
            return True
        except Exception as e:
            print(f"  ⚠️ Start Menu entry failed: {e}")
            return True  # Don't fail installation
    
    def create_uninstaller(self):
        """Create uninstaller"""
        print("\n[8/8] Creating uninstaller...")
        try:
            uninstaller_content = f"""@echo off
title JARVIS Uninstaller
echo ========================================
echo   JARVIS UNINSTALLER
echo ========================================
echo.
echo This will remove JARVIS from your computer.
echo.
set /p confirm="Are you sure? (Y/N): "
if /i "%confirm%"=="Y" (
    echo.
    echo Removing JARVIS...
    rd /s /q "{self.install_dir}"
    del "%USERPROFILE%\\Desktop\\JARVIS.lnk" 2>nul
    rd /s /q "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\JARVIS" 2>nul
    echo.
    echo ✅ JARVIS has been uninstalled.
    echo.
) else (
    echo.
    echo ❌ Uninstallation cancelled.
    echo.
)
pause
"""
            uninstaller_path = self.install_dir / "Uninstall.bat"
            with open(uninstaller_path, 'w') as f:
                f.write(uninstaller_content)
            print(f"  ✅ Created: Uninstall.bat")
            return True
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            return False
    
    def print_success(self):
        """Print success message"""
        print("\n" + "=" * 80)
        print("  ✅ INSTALLATION COMPLETE!")
        print("  ✅ ইনস্টলেশন সম্পূর্ণ!")
        print("=" * 80)
        print()
        print("  JARVIS has been installed to:")
        print(f"  📁 {self.install_dir}")
        print()
        print("  How to run JARVIS:")
        print("  1. Double-click 'JARVIS' icon on Desktop")
        print("  2. Or search 'JARVIS' in Start Menu")
        print("  3. Or run: Desktop\\JARVIS\\JARVIS.bat")
        print()
        print("  To uninstall:")
        print("  Run: Desktop\\JARVIS\\Uninstall.bat")
        print()
        print("  Features installed:")
        print("  ✅ Master Algorithm (100+ languages)")
        print("  ✅ Complete Database (310+ entries)")
        print("  ✅ Gaming Features")
        print("  ✅ 3D Modeling (Blender-style)")
        print("  ✅ System Management")
        print("  ✅ Download Manager")
        print("  ✅ And much more!")
        print()
        print("=" * 80)
        print()
        input("Press Enter to exit...")
    
    def install(self):
        """Main installation process"""
        self.print_header()
        
        # Installation steps
        if not self.check_python():
            input("Press Enter to exit...")
            return False
        
        if not self.create_install_directory():
            input("Press Enter to exit...")
            return False
        
        if not self.copy_files():
            input("Press Enter to exit...")
            return False
        
        if not self.install_dependencies():
            input("Press Enter to exit...")
            return False
        
        if not self.create_launcher():
            input("Press Enter to exit...")
            return False
        
        self.create_desktop_shortcut()
        self.create_start_menu_entry()
        
        if not self.create_uninstaller():
            input("Press Enter to exit...")
            return False
        
        self.print_success()
        return True

def main():
    installer = JarvisInstaller()
    installer.install()

if __name__ == "__main__":
    main()
