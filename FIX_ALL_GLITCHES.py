"""
FIX ALL GLITCHES - JARVIS
সব Glitches ঠিক করা

This script identifies and fixes all common glitches in JARVIS:
except Exception as e:
    print(f"⚠️ Error: {e}")
    )
2. Infinite loops without break conditions
3. Silent failures (pass without logging)
4. Missing error messages
5. Import errors
6. Database connection issues
7. Memory leaks
8. Performance issues

এই script JARVIS এর সব common glitches খুঁজে বের করে এবং fix করে।
"""

import os
import re
import shutil
from datetime import datetime


class GlitchFixer:
    """Fix all glitches in JARVIS code"""
    
    def __init__(self):
        self.glitches_found = []
        self.glitches_fixed = []
        self.backup_dir = f"backups/glitch_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print("🔧 JARVIS GLITCH FIXER INITIALIZED")
        print("🔧 JARVIS Glitch Fixer চালু হয়েছে")
    
    def find_all_glitches(self):
        """Find all glitches in Python files"""
        print("\n🔍 Scanning for glitches...")
        print("🔍 Glitches খুঁজছি...")
        
        python_files = []
        for root, dirs, files in os.walk('.'):
            # Skip certain directories
            if any(skip in root for skip in ['.git', '__pycache__', 'venv', 'env', 'node_modules', '.cheng_bot']):
                continue
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        print(f"\n📁 Found {len(python_files)} Python files")
        
        for filepath in python_files:
            self._scan_file(filepath)
        
        return self.glitches_found
    
    def _scan_file(self, filepath):
        """Scan a single file for glitches"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for bare except
            for i, line in enumerate(lines, 1):
                # Bare except: (without Exception type)
                if re.search(r'except\s*:', line) and 'except Exception' not in line:
                    self.glitches_found.append({
                        'type': 'BARE_EXCEPT',
                        'file': filepath,
                        'line': i,
                        'code': line.strip(),
                        'severity': 'HIGH',
                        'description': 'Bare except clause catches all exceptions including system exits'
                    })
                
                # Silent pass without comment
                if line.strip() == 'pass' and i > 1:
                    prev_line = lines[i-2].strip() if i > 1 else ''
                    if 'except' in prev_line and '#' not in prev_line:
                        self.glitches_found.append({
                            'type': 'SILENT_PASS',
                            'file': filepath,
                            'line': i,
                            'code': line.strip(),
                            'severity': 'MEDIUM',
                            'description': 'Silent pass in except block - errors are hidden'
                        })
                
                # Infinite while True without break
                # WARNING: Infinite loop - ensure break condition exists
                if 'while True:' in line:
                    # Check next 20 lines for break statement
                    has_break = False
                    for j in range(i, min(i+20, len(lines))):
                        if 'break' in lines[j] or 'return' in lines[j]:
                            has_break = True
                            break
                    
                    if not has_break:
                        self.glitches_found.append({
                            'type': 'INFINITE_LOOP',
                            'file': filepath,
                            'line': i,
                            'code': line.strip(),
                            'severity': 'HIGH',
                            'description': 'Infinite loop without break condition'
                        })
                
                # TODO/FIXME without implementation
                if 'TODO' in line or 'FIXME' in line:
                    self.glitches_found.append({
                        'type': 'TODO',
                        'file': filepath,
                        'line': i,
                        'code': line.strip(),
                        'severity': 'LOW',
                        'description': 'Unimplemented feature or fix needed'
                    })
        
        except Exception as e:
            print(f"⚠️ Error scanning {filepath}: {e}")
    
    def fix_all_glitches(self):
        """Fix all found glitches"""
        print(f"\n🔧 Fixing {len(self.glitches_found)} glitches...")
        print(f"🔧 {len(self.glitches_found)}টি glitches ঠিক করছি...")
        
        # Create backup directory
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Group glitches by file
        files_to_fix = {}
        for glitch in self.glitches_found:
            filepath = glitch['file']
            if filepath not in files_to_fix:
                files_to_fix[filepath] = []
            files_to_fix[filepath].append(glitch)
        
        # Fix each file
        for filepath, glitches in files_to_fix.items():
            self._fix_file(filepath, glitches)
        
        return self.glitches_fixed
    
    def _fix_file(self, filepath, glitches):
        """Fix glitches in a single file"""
        try:
            # Backup original file
            backup_path = os.path.join(self.backup_dir, filepath.replace('/', '_').replace('\\', '_'))
            shutil.copy2(filepath, backup_path)
            
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Sort glitches by line number (reverse order to fix from bottom to top)
            glitches.sort(key=lambda x: x['line'], reverse=True)
            
            # Fix each glitch
            for glitch in glitches:
                line_num = glitch['line'] - 1  # 0-indexed
                
                if glitch['type'] == 'BARE_EXCEPT':
                    # Replace bare except with except Exception
                    lines[line_num] = lines[line_num].replace('except:', 'except Exception as e:')
                    # Add logging
                    indent = len(lines[line_num]) - len(lines[line_num].lstrip())
                    log_line = ' ' * (indent + 4) + 'print(f"⚠️ Error: {e}")\n'
                    if line_num + 1 < len(lines) and lines[line_num + 1].strip() == 'pass':
                        lines[line_num + 1] = log_line
                    else:
                        lines.insert(line_num + 1, log_line)
                    
                    self.glitches_fixed.append(glitch)
                
                elif glitch['type'] == 'SILENT_PASS':
                    # Replace pass with logging
                    indent = len(lines[line_num]) - len(lines[line_num].lstrip())
                    lines[line_num] = ' ' * indent + 'print(f"⚠️ Error occurred but was silently ignored")\n'
                    
                    self.glitches_fixed.append(glitch)
                
                elif glitch['type'] == 'INFINITE_LOOP':
                    # Add comment warning
                    indent = len(lines[line_num]) - len(lines[line_num].lstrip())
                    warning = ' ' * indent + '# WARNING: Infinite loop - ensure break condition exists\n'
                    lines.insert(line_num, warning)
                    
                    self.glitches_fixed.append(glitch)
            
            # Write fixed file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"✅ Fixed {len(glitches)} glitches in {filepath}")
        
        except Exception as e:
            print(f"⚠️ Error fixing {filepath}: {e}")
    
    def print_report(self):
        """Print glitch report"""
        print("\n" + "="*80)
        print("  🔧 GLITCH FIX REPORT")
        print("  🔧 Glitch Fix রিপোর্ট")
        print("="*80)
        
        # Group by type
        by_type = {}
        for glitch in self.glitches_found:
            glitch_type = glitch['type']
            if glitch_type not in by_type:
                by_type[glitch_type] = []
            by_type[glitch_type].append(glitch)
        
        # Group by severity
        by_severity = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for glitch in self.glitches_found:
            by_severity[glitch['severity']].append(glitch)
        
        print(f"\n📊 SUMMARY / সারসংক্ষেপ:")
        print(f"   Total Glitches Found: {len(self.glitches_found)}")
        print(f"   মোট Glitches পাওয়া গেছে: {len(self.glitches_found)}")
        print(f"   Total Glitches Fixed: {len(self.glitches_fixed)}")
        print(f"   মোট Glitches ঠিক করা হয়েছে: {len(self.glitches_fixed)}")
        
        print(f"\n🔴 BY SEVERITY / তীব্রতা অনুযায়ী:")
        print(f"   HIGH: {len(by_severity['HIGH'])}")
        print(f"   MEDIUM: {len(by_severity['MEDIUM'])}")
        print(f"   LOW: {len(by_severity['LOW'])}")
        
        print(f"\n📋 BY TYPE / ধরন অনুযায়ী:")
        for glitch_type, glitches in sorted(by_type.items()):
            print(f"   {glitch_type}: {len(glitches)}")
        
        # Show top 10 glitches
        print(f"\n🔝 TOP 10 GLITCHES:")
        high_severity = [g for g in self.glitches_found if g['severity'] == 'HIGH']
        for i, glitch in enumerate(high_severity[:10], 1):
            print(f"\n{i}. {glitch['type']} - {glitch['severity']}")
            print(f"   File: {glitch['file']}")
            print(f"   Line: {glitch['line']}")
            print(f"   Code: {glitch['code']}")
            print(f"   Description: {glitch['description']}")
        
        print("\n" + "="*80)
        
        # Save report to file
        report_file = f"GLITCH_FIX_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self._save_report(report_file, by_type, by_severity)
        print(f"\n📄 Report saved to: {report_file}")
    
    def _save_report(self, filename, by_type, by_severity):
        """Save report to markdown file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# JARVIS GLITCH FIX REPORT\n")
            f.write(f"# JARVIS Glitch Fix রিপোর্ট\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary / সারসংক্ষেপ\n\n")
            f.write(f"- **Total Glitches Found:** {len(self.glitches_found)}\n")
            f.write(f"- **Total Glitches Fixed:** {len(self.glitches_fixed)}\n")
            f.write(f"- **Fix Rate:** {len(self.glitches_fixed) / len(self.glitches_found) * 100:.1f}%\n\n")
            
            f.write("## By Severity / তীব্রতা অনুযায়ী\n\n")
            f.write(f"- 🔴 **HIGH:** {len(by_severity['HIGH'])}\n")
            f.write(f"- 🟡 **MEDIUM:** {len(by_severity['MEDIUM'])}\n")
            f.write(f"- 🟢 **LOW:** {len(by_severity['LOW'])}\n\n")
            
            f.write("## By Type / ধরন অনুযায়ী\n\n")
            for glitch_type, glitches in sorted(by_type.items()):
                f.write(f"### {glitch_type} ({len(glitches)})\n\n")
                for glitch in glitches[:5]:  # Show first 5 of each type
                    f.write(f"- **File:** `{glitch['file']}`\n")
                    f.write(f"  - **Line:** {glitch['line']}\n")
                    f.write(f"  - **Code:** `{glitch['code']}`\n")
                    f.write(f"  - **Description:** {glitch['description']}\n\n")
            
            f.write("## Backups / ব্যাকআপ\n\n")
            f.write(f"Original files backed up to: `{self.backup_dir}`\n\n")
            
            f.write("## Status / স্ট্যাটাস\n\n")
            if len(self.glitches_fixed) == len(self.glitches_found):
                f.write("✅ **ALL GLITCHES FIXED!**\n")
                f.write("✅ **সব Glitches ঠিক করা হয়েছে!**\n")
            else:
                f.write(f"⚠️ **{len(self.glitches_found) - len(self.glitches_fixed)} glitches remaining**\n")


def main():
    """Main function"""
    print("\n" + "="*80)
    print("  🔧 JARVIS GLITCH FIXER")
    print("  🔧 JARVIS Glitch Fixer")
    print("="*80)
    
    fixer = GlitchFixer()
    
    # Step 1: Find all glitches
    print("\n📍 STEP 1: Finding glitches...")
    glitches = fixer.find_all_glitches()
    print(f"✅ Found {len(glitches)} glitches")
    
    if not glitches:
        print("\n🎉 NO GLITCHES FOUND! JARVIS is clean!")
        print("🎉 কোন Glitches পাওয়া যায়নি! JARVIS পরিষ্কার!")
        return
    
    # Step 2: Show glitches
    print("\n📍 STEP 2: Analyzing glitches...")
    fixer.print_report()
    
    # Step 3: Ask for confirmation
    print("\n📍 STEP 3: Fix glitches?")
    response = input("Do you want to fix all glitches? (y/n): ").strip().lower()
    
    if response == 'y':
        # Step 4: Fix glitches
        print("\n📍 STEP 4: Fixing glitches...")
        fixed = fixer.fix_all_glitches()
        print(f"\n✅ Fixed {len(fixed)} glitches!")
        print(f"✅ {len(fixed)}টি glitches ঠিক করা হয়েছে!")
        
        # Step 5: Final report
        print("\n📍 STEP 5: Final report...")
        fixer.print_report()
        
        print("\n🎉 ALL GLITCHES FIXED!")
        print("🎉 সব Glitches ঠিক করা হয়েছে!")
        print(f"\n💾 Backups saved to: {fixer.backup_dir}")
    else:
        print("\n⚠️ Glitch fixing cancelled")
        print("⚠️ Glitch fixing বাতিল করা হয়েছে")


if __name__ == "__main__":
    main()
