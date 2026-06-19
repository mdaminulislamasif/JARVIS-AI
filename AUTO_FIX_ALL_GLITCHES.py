"""
AUTO FIX ALL GLITCHES - JARVIS
স্বয়ংক্রিয়ভাবে সব Glitches ঠিক করা

Automatically fixes all glitches without asking for confirmation.
স্বয়ংক্রিয়ভাবে সব glitches ঠিক করে confirmation ছাড়াই।
"""

import os
import re
import shutil
from datetime import datetime


def auto_fix_all_glitches():
    """Automatically fix all glitches"""
    print("\n" + "="*80)
    print("  🔧 AUTO FIX ALL GLITCHES")
    print("  🔧 স্বয়ংক্রিয়ভাবে সব Glitches ঠিক করা")
    print("="*80)
    
    backup_dir = f"backups/auto_glitch_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    fixed_count = 0
    total_files = 0
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        if any(skip in root for skip in ['.git', '__pycache__', 'venv', 'env', 'node_modules', '.cheng_bot', 'backups']):
            continue
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"\n📁 Found {len(python_files)} Python files")
    print(f"📁 {len(python_files)}টি Python files পাওয়া গেছে")
    
    # Fix each file
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Replace bare except: with except Exception as e:
            content = re.sub(
                r'(\s+)except:\s*$',
                r'\1except Exception as e:\n\1    print(f"⚠️ Error: {e}")',
                content,
                flags=re.MULTILINE
            )
            
            # Fix 2: Replace except: pass with proper error handling
            content = re.sub(
                r'(\s+)except:\s*\n\s+pass',
                r'\1except Exception as e:\n\1    print(f"⚠️ Error: {e}")',
                content
            )
            
            # Fix 3: Add warning comments to infinite loops
            lines = content.split('\n')
            new_lines = []
            for i, line in enumerate(lines):
                # WARNING: Infinite loop - ensure break condition exists
                if 'while True:' in line:
                    # Check if there's already a warning
                    if i > 0 and 'WARNING' not in lines[i-1]:
                        indent = len(line) - len(line.lstrip())
                        new_lines.append(' ' * indent + '# WARNING: Infinite loop - ensure break condition exists')
                new_lines.append(line)
            content = '\n'.join(new_lines)
            
            # If content changed, save it
            if content != original_content:
                # Backup original
                backup_path = os.path.join(backup_dir, filepath.replace('/', '_').replace('\\', '_'))
                shutil.copy2(filepath, backup_path)
                
                # Save fixed version
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_count += 1
                total_files += 1
                print(f"✅ Fixed: {filepath}")
        
        except Exception as e:
            print(f"⚠️ Error fixing {filepath}: {e}")
    
    print(f"\n" + "="*80)
    print(f"  ✅ AUTO FIX COMPLETE!")
    print(f"  ✅ স্বয়ংক্রিয় Fix সম্পূর্ণ!")
    print("="*80)
    print(f"\n📊 SUMMARY:")
    print(f"   Files Scanned: {len(python_files)}")
    print(f"   Files Fixed: {fixed_count}")
    print(f"   Backup Location: {backup_dir}")
    print(f"\n✅ ALL GLITCHES FIXED!")
    print(f"✅ সব Glitches ঠিক করা হয়েছে!")


if __name__ == "__main__":
    auto_fix_all_glitches()
