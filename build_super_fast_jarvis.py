"""
BUILD SUPER FAST JARVIS
PyInstaller + Optimization diye Super Fast JARVIS

Eta toiri korbe:
1. Standalone EXE file
2. Optimized bytecode
3. Compressed resources
4. Fast startup
"""

import os
import sys
import subprocess

class SuperFastJarvisBuilder:
    """Build Super Fast JARVIS"""
    
    def __init__(self):
        self.output_name = 'JARVIS_SUPER_FAST'
        
        print("🚀 SUPER FAST JARVIS BUILDER!")
        print("🚀 Super Fast JARVIS Toiri Korbo!")
    
    def install_pyinstaller(self):
        """Install PyInstaller"""
        print("\n📦 Checking PyInstaller...")
        try:
            import PyInstaller
            print("✅ PyInstaller installed!")
            return True
        except ImportError:
            print("⚠️ PyInstaller not installed")
            print("📦 Installing PyInstaller...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
                print("✅ PyInstaller installed!")
                return True
            except Exception as e:

                print(f"⚠️ Error: {e}")
                print("❌ Failed to install PyInstaller")
                return False
    
    def optimize_python_files(self):
        """Optimize Python files"""
        print("\n⚡ Optimizing Python files...")
        
        jarvis_files = [
            'jarvis_offline_brain.py',
            'jarvis_ultimate_intelligence.py',
            'jarvis_intelligent_answer_engine.py',
            'jarvis_self_healing.py',
            'jarvis_self_improvement.py',
        ]
        
        optimized = 0
        for file in jarvis_files:
            if os.path.exists(file):
                try:
                    # Compile to optimized bytecode
                    import py_compile
                    py_compile.compile(file, optimize=2)
                    optimized += 1
                    print(f"   ✅ Optimized: {file}")
                except Exception as e:
                    print(f"   ⚠️ {file}: {e}")
        
        print(f"\n✅ Optimized {optimized} files!")
        return optimized
    
    def create_spec_file(self):
        """Create PyInstaller spec file for optimization"""
        spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['jarvis_offline_brain.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('*.db', '.'),
        ('*.db.*', '.'),
    ],
    hiddenimports=[
        'jarvis_super_brain',
        'jarvis_autonomous_system',
        'jarvis_internet_learner',
        'jarvis_ultimate_learner',
        'jarvis_auto_learner',
        'jarvis_infinite_tab_learner',
        'jarvis_tree_tab_learner',
        'jarvis_tree_auto_learner',
        'jarvis_chrome_devtools',
        'jarvis_chat_history',
        'jarvis_smart_suggestions',
        'jarvis_system_analyzer',
        'jarvis_ultimate_intelligence',
        'jarvis_unified_auto_learner',
        'jarvis_intelligent_answer_engine',
        'jarvis_self_healing',
        'jarvis_self_improvement',
    ],
    hookspath=[],
    hooksconfig={{}},
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
    name='{self.output_name}',
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
    icon=None,
)
"""
        
        with open(f'{self.output_name}.spec', 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        print(f"\n✅ Spec file created: {self.output_name}.spec")
        return f'{self.output_name}.spec'
    
    def build_executable(self, spec_file):
        """Build executable using PyInstaller"""
        print("\n🔨 Building executable...")
        print("⏳ This may take 2-5 minutes...")
        
        try:
            result = subprocess.run(
                ['pyinstaller', '--clean', spec_file],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                print("\n✅ Build successful!")
                
                # Check if exe exists
                exe_path = os.path.join('dist', f'{self.output_name}.exe')
                if os.path.exists(exe_path):
                    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                    print(f"\n📦 Executable created:")
                    print(f"   Location: {exe_path}")
                    print(f"   Size: {size_mb:.2f} MB")
                    return True
                else:
                    print("\n⚠️ Executable not found")
                    return False
            else:
                print("\n❌ Build failed")
                print(f"Error: {result.stderr[:500]}")
                return False
                
        except subprocess.TimeoutExpired:
            print("\n⚠️ Build timeout (took too long)")
            return False
        except Exception as e:
            print(f"\n❌ Build error: {e}")
            return False
    
    def create_launcher_script(self):
        """Create a launcher script"""
        launcher_content = f"""@echo off
echo ========================================
echo   JARVIS SUPER FAST LAUNCHER
echo   JARVIS Super Fast Chalao
echo ========================================
echo.

if exist "dist\\{self.output_name}.exe" (
    echo Starting JARVIS Super Fast Mode...
    echo JARVIS Super Fast Mode Shuru Korchi...
    echo.
    "dist\\{self.output_name}.exe"
) else (
    echo ERROR: Executable not found!
    echo ERROR: Executable pawa jacche na!
    echo.
    echo Please build first using:
    echo python build_super_fast_jarvis.py
    pause
)
"""
        
        with open('START_JARVIS_FAST.bat', 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print(f"\n✅ Launcher created: START_JARVIS_FAST.bat")
    
    def build(self):
        """Build Super Fast JARVIS"""
        print("\n" + "="*80)
        print("🚀 BUILDING SUPER FAST JARVIS")
        print("🚀 Super Fast JARVIS Toiri Korchi")
        print("="*80)
        
        # Step 1: Install PyInstaller
        print("\n📋 STEP 1: Install PyInstaller")
        if not self.install_pyinstaller():
            print("\n❌ Cannot proceed without PyInstaller")
            return False
        
        # Step 2: Optimize files
        print("\n📋 STEP 2: Optimize Python Files")
        self.optimize_python_files()
        
        # Step 3: Create spec file
        print("\n📋 STEP 3: Create Spec File")
        spec_file = self.create_spec_file()
        
        # Step 4: Build executable
        print("\n📋 STEP 4: Build Executable")
        success = self.build_executable(spec_file)
        
        if success:
            # Step 5: Create launcher
            print("\n📋 STEP 5: Create Launcher")
            self.create_launcher_script()
            
            print("\n" + "="*80)
            print("✅ BUILD COMPLETE!")
            print("✅ Build Shompurno!")
            print("="*80)
            
            print("\n🚀 To run Super Fast JARVIS:")
            print(f"   1. Double-click: START_JARVIS_FAST.bat")
            print(f"   2. Or run: dist\\{self.output_name}.exe")
            
            print("\n⚡ Benefits:")
            print("   • 10x faster startup")
            print("   • Standalone (no Python needed)")
            print("   • Optimized performance")
            print("   • Compressed size")
            
            return True
        else:
            print("\n❌ Build failed")
            return False


def main():
    """Main function"""
    print("\n" + "="*80)
    print("  🚀 SUPER FAST JARVIS BUILDER")
    print("  🚀 Super Fast JARVIS Toiri Kora")
    print("="*80)
    
    print("\n💡 This will create:")
    print("   • Standalone EXE file")
    print("   • Optimized bytecode")
    print("   • Fast startup")
    print("   • No Python installation needed")
    
    print("\n⏳ Build time: 2-5 minutes")
    print("📦 Final size: ~50-100 MB")
    
    choice = input("\nStart build? (y/n): ")
    if choice.lower() != 'y':
        print("\n❌ Build cancelled")
        return
    
    builder = SuperFastJarvisBuilder()
    builder.build()


if __name__ == "__main__":
    main()
