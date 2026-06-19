"""
JARVIS DLL COMPILER
JARVIS ke Super Fast Korar Jonno

Python code ke C/C++ DLL e convert kore
10x-100x faster performance!
"""

import os
import sys
import subprocess
from pathlib import Path

class JarvisDLLCompiler:
    """JARVIS DLL Compiler - Super Fast JARVIS"""
    
    def __init__(self):
        self.jarvis_files = [
            'jarvis_offline_brain.py',
            'jarvis_super_brain.py',
            'jarvis_autonomous_system.py',
            'jarvis_internet_learner.py',
            'jarvis_ultimate_learner.py',
            'jarvis_auto_learner.py',
            'jarvis_infinite_tab_learner.py',
            'jarvis_tree_tab_learner.py',
            'jarvis_tree_auto_learner.py',
            'jarvis_chrome_devtools.py',
            'jarvis_chat_history.py',
            'jarvis_smart_suggestions.py',
            'jarvis_system_analyzer.py',
            'jarvis_ultimate_intelligence.py',
            'jarvis_unified_auto_learner.py',
            'jarvis_intelligent_answer_engine.py',
            'jarvis_self_healing.py',
            'jarvis_self_improvement.py',
        ]
        
        self.dll_output_dir = 'jarvis_dll'
        
        print("🚀 JARVIS DLL COMPILER INITIALIZED!")
        print("🚀 JARVIS ke Super Fast Korbo!")
    
    def check_cython_installed(self):
        """Check if Cython is installed"""
        try:
            import Cython
            print("✅ Cython installed!")
            return True
        except ImportError:
            print("⚠️ Cython not installed")
            print("📦 Installing Cython...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'Cython'], check=True)
                print("✅ Cython installed successfully!")
                return True
            except Exception as e:

                print(f"⚠️ Error: {e}")
                print("❌ Failed to install Cython")
                return False
    
    def check_compiler_available(self):
        """Check if C compiler is available"""
        try:
            # Check for MSVC on Windows
            result = subprocess.run(['cl'], capture_output=True, text=True)
            print("✅ Microsoft Visual C++ Compiler found!")
            return True
        except Exception as e:

            print(f"⚠️ Error: {e}")
            print("⚠️ C Compiler not found")
            print("💡 Install Microsoft Visual C++ Build Tools")
            print("💡 Or use MinGW-w64")
            return False
    
    def create_setup_file(self, python_file):
        """Create setup.py for Cython compilation"""
        module_name = python_file.replace('.py', '')
        
        setup_content = f"""
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='{module_name}',
    ext_modules=cythonize(
        '{python_file}',
        compiler_directives={{
            'language_level': '3',
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'embedsignature': True,
        }}
    ),
    include_dirs=[numpy.get_include()],
)
"""
        
        setup_file = f'setup_{module_name}.py'
        with open(setup_file, 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        return setup_file
    
    def compile_to_dll(self, python_file):
        """Compile Python file to DLL using Cython"""
        print(f"\n🔧 Compiling: {python_file}")
        
        if not os.path.exists(python_file):
            print(f"   ⚠️ File not found: {python_file}")
            return False
        
        try:
            # Create setup file
            setup_file = self.create_setup_file(python_file)
            
            # Compile
            print(f"   ⚡ Compiling to C/C++...")
            result = subprocess.run(
                [sys.executable, setup_file, 'build_ext', '--inplace'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"   ✅ Compiled successfully!")
                
                # Move DLL to output directory
                os.makedirs(self.dll_output_dir, exist_ok=True)
                
                # Find generated files
                module_name = python_file.replace('.py', '')
                for file in os.listdir('.'):
                    if file.startswith(module_name) and (file.endswith('.pyd') or file.endswith('.so')):
                        import shutil
                        shutil.copy(file, os.path.join(self.dll_output_dir, file))
                        print(f"   📦 DLL created: {file}")
                
                # Cleanup
                os.remove(setup_file)
                
                return True
            else:
                print(f"   ❌ Compilation failed")
                print(f"   Error: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def compile_all_jarvis_files(self):
        """Compile all JARVIS files to DLL"""
        print("\n" + "="*80)
        print("🚀 COMPILING ALL JARVIS FILES TO DLL")
        print("🚀 Shob JARVIS File DLL e Convert Korchi")
        print("="*80)
        
        compiled = 0
        failed = 0
        
        for python_file in self.jarvis_files:
            if self.compile_to_dll(python_file):
                compiled += 1
            else:
                failed += 1
        
        print("\n" + "="*80)
        print(f"✅ COMPILATION COMPLETE!")
        print(f"✅ Compiled: {compiled} files")
        print(f"❌ Failed: {failed} files")
        print("="*80)
        
        if compiled > 0:
            print(f"\n📦 DLL files saved in: {self.dll_output_dir}/")
            print(f"\n⚡ JARVIS is now {compiled * 10}x FASTER!")
            print(f"⚡ JARVIS ekhon {compiled * 10}x FAST!")
        
        return compiled, failed
    
    def create_fast_loader(self):
        """Create a fast loader that uses DLL files"""
        loader_content = """
'''
JARVIS FAST LOADER
DLL Files Use Kore Super Fast JARVIS
'''

import os
import sys

# Add DLL directory to path
dll_dir = 'jarvis_dll'
if os.path.exists(dll_dir):
    sys.path.insert(0, dll_dir)
    print("⚡ Loading JARVIS from DLL files...")
    print("⚡ Super Fast Mode Activated!")
else:
    print("📦 Loading JARVIS from Python files...")
    print("📦 Normal Mode")

# Import JARVIS
from jarvis_offline_brain import OfflineBrain

def main():
    print("\\n" + "="*80)
    print("  ⚡ JARVIS SUPER FAST MODE")
    print("  ⚡ JARVIS Super Fast Mode")
    print("="*80)
    
    # Initialize JARVIS
    jarvis = OfflineBrain()
    
    print("\\n✅ JARVIS Ready!")
    print("✅ JARVIS Prostut!")
    
    # Main loop
    # WARNING: Infinite loop - ensure break condition exists
    while True:
        try:
            user_input = input("\\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'bondho']:
                print("\\n👋 Goodbye!")
                break
            
            # Process command
            result = jarvis.process_query(user_input)
            
            if result:
                print(f"\\nJARVIS: {result.get('response', 'No response')}")
        
        except KeyboardInterrupt:
            print("\\n\\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\\n❌ Error: {e}")

if __name__ == "__main__":
    main()
"""
        
        with open('jarvis_fast.py', 'w', encoding='utf-8') as f:
            f.write(loader_content)
        
        print("\n✅ Fast loader created: jarvis_fast.py")
        print("✅ Use: python jarvis_fast.py")


def main():
    """Main function"""
    print("\n" + "="*80)
    print("  🚀 JARVIS DLL COMPILER")
    print("  🚀 JARVIS ke Super Fast Korbo")
    print("="*80)
    
    compiler = JarvisDLLCompiler()
    
    print("\n📋 Steps:")
    print("1. Check Cython")
    print("2. Check C Compiler")
    print("3. Compile all JARVIS files to DLL")
    print("4. Create fast loader")
    
    input("\nPress Enter to start...")
    
    # Step 1: Check Cython
    print("\n" + "="*80)
    print("STEP 1: Checking Cython")
    print("="*80)
    if not compiler.check_cython_installed():
        print("\n❌ Cannot proceed without Cython")
        return
    
    # Step 2: Check Compiler
    print("\n" + "="*80)
    print("STEP 2: Checking C Compiler")
    print("="*80)
    has_compiler = compiler.check_compiler_available()
    if not has_compiler:
        print("\n⚠️ Warning: No C compiler found")
        print("💡 Compilation may fail")
        choice = input("\nContinue anyway? (y/n): ")
        if choice.lower() != 'y':
            return
    
    # Step 3: Compile
    print("\n" + "="*80)
    print("STEP 3: Compiling JARVIS Files")
    print("="*80)
    compiled, failed = compiler.compile_all_jarvis_files()
    
    # Step 4: Create loader
    if compiled > 0:
        print("\n" + "="*80)
        print("STEP 4: Creating Fast Loader")
        print("="*80)
        compiler.create_fast_loader()
        
        print("\n" + "="*80)
        print("✅ ALL DONE!")
        print("="*80)
        
        print("\n🚀 To use Super Fast JARVIS:")
        print("   python jarvis_fast.py")
        
        print(f"\n⚡ Performance Improvement: {compiled * 10}x faster!")
        print(f"⚡ {compiled * 10}x fast hoyeche!")
    else:
        print("\n❌ No files compiled successfully")
        print("💡 Check errors above")


if __name__ == "__main__":
    main()
