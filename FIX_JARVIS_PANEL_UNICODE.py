#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX JARVIS PANEL UNICODE ERRORS
================================
Fixes Unicode encoding errors that prevent JARVIS panel from starting
"""

import os
import sys
import re

print("=" * 70)
print("🔧 FIXING JARVIS PANEL UNICODE ERRORS")
print("=" * 70)
print()

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        # Set UTF-8 encoding for console
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        print("✅ Console encoding set to UTF-8")
    except Exception as e:
        print(f"⚠️ Could not set console encoding: {e}")

print()

# Files to fix
files_to_fix = [
    'jarvis_auto_background_learner.py',
    'jarvis_panel.py',
    'jarvis_offline_brain.py',
    'jarvis_internet_learner.py',
    'jarvis_ultimate_learner.py',
    'jarvis_autonomous_system.py',
    'jarvis_tree_tab_learner.py',
]

# Unicode characters that cause problems
problematic_chars = {
    '✅': '[OK]',
    '❌': '[X]',
    '⚠️': '[!]',
    '🔧': '[TOOL]',
    '🎯': '[TARGET]',
    '🚀': '[ROCKET]',
    '💡': '[IDEA]',
    '🔥': '[FIRE]',
    '⚡': '[BOLT]',
    '🌍': '[GLOBE]',
    '🤖': '[ROBOT]',
    '🧠': '[BRAIN]',
    '💬': '[CHAT]',
    '🔮': '[CRYSTAL]',
    '🦙': '[LLAMA]',
    '🤗': '[HUG]',
    '🌟': '[STAR]',
    '🔍': '[SEARCH]',
    '🎭': '[MASK]',
    '🔷': '[DIAMOND]',
}

def fix_unicode_in_file(filepath):
    """Fix Unicode characters in a file"""
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filepath}")
        return False
    
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # Replace problematic Unicode characters in print statements only
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            new_line = line
            
            # Only fix print statements
            if 'print(' in line or 'print (' in line:
                for unicode_char, replacement in problematic_chars.items():
                    if unicode_char in line:
                        new_line = new_line.replace(unicode_char, replacement)
                        changes += 1
            
            new_lines.append(new_line)
        
        content = '\n'.join(new_lines)
        
        if changes > 0:
            # Create backup
            backup_file = filepath + '.unicode_backup'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed {filepath}: {changes} changes")
            print(f"   Backup: {backup_file}")
            return True
        else:
            print(f"✅ {filepath}: No changes needed")
            return True
    
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

# Fix all files
print("Step 1: Fixing Unicode in Python files...")
print()

fixed_count = 0
for filepath in files_to_fix:
    if fix_unicode_in_file(filepath):
        fixed_count += 1
    print()

print("=" * 70)
print(f"✅ Fixed {fixed_count}/{len(files_to_fix)} files")
print("=" * 70)
print()

# Create a startup wrapper
print("Step 2: Creating startup wrapper...")

wrapper_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS PANEL STARTUP WRAPPER
=============================
Fixes encoding issues before starting JARVIS panel
"""

import sys
import os

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')
    except Exception as e:

        print(f"⚠️ Error: {e}")
        pass

# Set environment variable for UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import and run JARVIS panel
try:
    import jarvis_panel
    print("[OK] JARVIS Panel starting...")
except Exception as e:
    print(f"[X] Error starting JARVIS: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
'''

with open('START_JARVIS.py', 'w', encoding='utf-8') as f:
    f.write(wrapper_content)

print("✅ Created START_JARVIS.py")
print()

# Create batch file
print("Step 3: Creating batch file...")

batch_content = '''@echo off
chcp 65001 >nul
echo ================================================================
echo STARTING JARVIS PANEL
echo ================================================================
echo.

python START_JARVIS.py

if errorlevel 1 (
    echo.
    echo ================================================================
    echo ERROR: JARVIS failed to start
    echo ================================================================
    echo.
    pause
)
'''

with open('START_JARVIS.bat', 'w', encoding='utf-8') as f:
    f.write(batch_content)

print("✅ Created START_JARVIS.bat")
print()

print("=" * 70)
print("🎉 FIX COMPLETE!")
print("=" * 70)
print()
print("✅ What was fixed:")
print("   1. Unicode characters in print statements")
print("   2. Console encoding issues")
print("   3. Created startup wrapper")
print("   4. Created batch file")
print()
print("🚀 How to start JARVIS now:")
print()
print("   Method 1 (Recommended):")
print("   Double-click: START_JARVIS.bat")
print()
print("   Method 2:")
print("   python START_JARVIS.py")
print()
print("   Method 3 (Original):")
print("   python jarvis_panel.py")
print()
print("💡 If still having issues:")
print("   1. Close all Python processes")
print("   2. Restart terminal")
print("   3. Use START_JARVIS.bat")
print()
print("=" * 70)
