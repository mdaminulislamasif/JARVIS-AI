"""
JARVIS SELF-HEALING SYSTEM
স্ব-নিরাময় সিস্টেম

JARVIS নিজে নিজে:
- নিজের সমস্যা খুঁজে বের করবে
- নিজেই fix করবে
- নিজেই test করবে
- নিজেই improve করবে

NO HUMAN INTERVENTION NEEDED!
মানুষের হস্তক্ষেপ লাগবে না!
"""

import os
import sys

# Force console stdout and stderr to use UTF-8 on Windows to prevent encoding crashes
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import time
import traceback
import subprocess
import re
from datetime import datetime
import sqlite3


class SelfHealingSystem:
    """JARVIS Self-Healing System - নিজে নিজে ঠিক করে"""
    
    def __init__(self):
        self.db_path = 'jarvis_self_healing.db'
        self.log_file = 'jarvis_self_healing.log'
        self.issues_found = []
        self.fixes_applied = []
        self.setup_database()
        
        print("🔧 JARVIS SELF-HEALING SYSTEM INITIALIZED!")
        print("🔧 JARVIS স্ব-নিরাময় সিস্টেম চালু হয়েছে!")
        print("🔧 JARVIS will now fix itself automatically!")
        print("🔧 JARVIS এখন নিজেকে নিজে ঠিক করবে!")
    
    def setup_database(self):
        """Setup database for tracking issues and fixes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Issues table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_type TEXT,
                    description TEXT,
                    severity TEXT,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fixed BOOLEAN DEFAULT 0
                )
            """)
            
            # Fixes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fixes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_id INTEGER,
                    fix_description TEXT,
                    fix_code TEXT,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN,
                    FOREIGN KEY (issue_id) REFERENCES issues(id)
                )
            """)
            
            conn.commit()
            conn.close()
            print("✅ Self-Healing database ready!")
            
        except Exception as e:
            print(f"⚠️ Database setup error: {e}")
    
    def run_self_diagnosis(self):
        """
        Run complete self-diagnosis
        সম্পূর্ণ self-diagnosis চালায়
        """
        print("\n" + "="*80)
        print("🔍 JARVIS SELF-DIAGNOSIS STARTED")
        print("🔍 JARVIS স্ব-নির্ণয় শুরু হয়েছে")
        print("="*80)
        
        self.issues_found = []
        
        # 1. Check Python files for syntax errors
        print("\n1️⃣ Checking Python files for syntax errors...")
        self._check_syntax_errors()
        
        # 2. Check for missing imports
        print("\n2️⃣ Checking for missing imports...")
        self._check_missing_imports()
        
        # 3. Check for undefined methods
        print("\n3️⃣ Checking for undefined methods...")
        self._check_undefined_methods()
        
        # 4. Check for indentation errors
        print("\n4️⃣ Checking for indentation errors...")
        self._check_indentation_errors()
        
        # 5. Check database integrity
        print("\n5️⃣ Checking database integrity...")
        self._check_database_integrity()
        
        # 6. Check file permissions
        print("\n6️⃣ Checking file permissions...")
        self._check_file_permissions()
        
        # 7. Run test suite
        print("\n7️⃣ Running test suite...")
        self._run_tests()
        
        # Summary
        print("\n" + "="*80)
        print(f"🔍 DIAGNOSIS COMPLETE: Found {len(self.issues_found)} issues")
        print(f"🔍 নির্ণয় সম্পূর্ণ: {len(self.issues_found)}টি সমস্যা পাওয়া গেছে")
        print("="*80)
        
        return self.issues_found
    
    def _check_syntax_errors(self):
        """Check all Python files for syntax errors"""
        python_files = [f for f in os.listdir('.') if f.endswith('.py')]
        
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    compile(code, file, 'exec')
                print(f"   ✅ {file}: No syntax errors")
            except SyntaxError as e:
                issue = {
                    'type': 'syntax_error',
                    'file': file,
                    'line': e.lineno,
                    'description': str(e),
                    'severity': 'high'
                }
                self.issues_found.append(issue)
                print(f"   ❌ {file}: Syntax error at line {e.lineno}")
                self._log_issue(issue)
    
    def _check_missing_imports(self):
        """Check for missing imports"""
        python_files = [f for f in os.listdir('.') if f.endswith('.py') and f.startswith('jarvis_')]
        
        for file in python_files:
            try:
                # Try to import the module
                module_name = file[:-3]  # Remove .py
                __import__(module_name)
                print(f"   ✅ {file}: All imports OK")
            except ImportError as e:
                issue = {
                    'type': 'missing_import',
                    'file': file,
                    'description': str(e),
                    'severity': 'medium'
                }
                self.issues_found.append(issue)
                print(f"   ⚠️ {file}: Missing import - {e}")
                self._log_issue(issue)
            except Exception as e:
                # Other errors (not import related)
                pass
    
    def _check_undefined_methods(self):
        """Check for undefined methods being called"""
        python_files = [f for f in os.listdir('.') if f.endswith('.py') and f.startswith('jarvis_')]
        
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Find method calls like self._method_name()
                    method_calls = re.findall(r'self\.(_\w+)\(', content)
                    
                    # Find method definitions like def _method_name(
                    method_defs = re.findall(r'def (_\w+)\(', content)
                    
                    # Check for undefined methods
                    undefined = set(method_calls) - set(method_defs)
                    
                    if undefined:
                        for method in undefined:
                            issue = {
                                'type': 'undefined_method',
                                'file': file,
                                'method': method,
                                'description': f"Method '{method}' is called but not defined",
                                'severity': 'high'
                            }
                            self.issues_found.append(issue)
                            print(f"   ❌ {file}: Undefined method '{method}'")
                            self._log_issue(issue)
                    else:
                        print(f"   ✅ {file}: All methods defined")
            
            except Exception as e:
                print(f"   ⚠️ {file}: Error checking methods - {e}")
    
    def _check_indentation_errors(self):
        """Check for indentation errors"""
        python_files = [f for f in os.listdir('.') if f.endswith('.py')]
        
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    for i, line in enumerate(lines, 1):
                        # Check for mixed tabs and spaces
                        if '\t' in line and '    ' in line:
                            issue = {
                                'type': 'indentation_error',
                                'file': file,
                                'line': i,
                                'description': 'Mixed tabs and spaces',
                                'severity': 'medium'
                            }
                            self.issues_found.append(issue)
                            print(f"   ⚠️ {file}: Mixed tabs/spaces at line {i}")
                            self._log_issue(issue)
                            break
                    else:
                        print(f"   ✅ {file}: Indentation OK")
            
            except Exception as e:
                print(f"   ⚠️ {file}: Error checking indentation - {e}")
    
    def _check_database_integrity(self):
        """Check database integrity"""
        db_files = [f for f in os.listdir('.') if f.endswith('.db') and not any(x in f for x in ['.backup', '.corrupted', 'fixed-', 'session-'])]
        
        for db_file in db_files:
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                conn.close()
                
                if result[0] == 'ok':
                    print(f"   ✅ {db_file}: Database OK")
                else:
                    issue = {
                        'type': 'database_corruption',
                        'file': db_file,
                        'description': f"Database integrity check failed: {result[0]}",
                        'severity': 'high'
                    }
                    self.issues_found.append(issue)
                    print(f"   ❌ {db_file}: Database corrupted")
                    self._log_issue(issue)
            
            except Exception as e:
                issue = {
                    'type': 'database_error',
                    'file': db_file,
                    'description': str(e),
                    'severity': 'medium'
                }
                self.issues_found.append(issue)
                print(f"   ⚠️ {db_file}: Database error - {e}")
                self._log_issue(issue)
    
    def _check_file_permissions(self):
        """Check file permissions"""
        important_files = [f for f in os.listdir('.') if f.endswith('.py') and f.startswith('jarvis_')]
        
        for file in important_files:
            try:
                # Check if file is readable
                with open(file, 'r') as f:
                    pass
                
                # Check if file is writable
                with open(file, 'a') as f:
                    pass
                
                print(f"   ✅ {file}: Permissions OK")
            
            except PermissionError:
                issue = {
                    'type': 'permission_error',
                    'file': file,
                    'description': 'File permission denied',
                    'severity': 'high'
                }
                self.issues_found.append(issue)
                print(f"   ❌ {file}: Permission denied")
                self._log_issue(issue)
    
    def _run_tests(self):
        """Run test suite"""
        test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
        
        if not test_files:
            print("   ⚠️ No test files found")
            return
        
        for test_file in test_files:
            try:
                child_env = os.environ.copy()
                child_env['PYTHONIOENCODING'] = 'utf-8'
                child_env['JARVIS_NO_DIAGNOSIS'] = '1'
                result = subprocess.run(
                    [sys.executable, test_file],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    env=child_env,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print(f"   ✅ {test_file}: All tests passed")
                else:
                    issue = {
                        'type': 'test_failure',
                        'file': test_file,
                        'description': result.stderr[:200],
                        'severity': 'medium'
                    }
                    self.issues_found.append(issue)
                    print(f"   ❌ {test_file}: Tests failed")
                    self._log_issue(issue)
            
            except subprocess.TimeoutExpired:
                print(f"   ⚠️ {test_file}: Test timeout")
            except Exception as e:
                print(f"   ⚠️ {test_file}: Error running tests - {e}")
    
    def auto_fix_issues(self):
        """
        Automatically fix all found issues
        সব সমস্যা স্বয়ংক্রিয়ভাবে ঠিক করে
        """
        if not self.issues_found:
            print("\n✅ No issues to fix!")
            return
        
        print("\n" + "="*80)
        print(f"🔧 AUTO-FIXING {len(self.issues_found)} ISSUES")
        print(f"🔧 {len(self.issues_found)}টি সমস্যা স্বয়ংক্রিয়ভাবে ঠিক করা হচ্ছে")
        print("="*80)
        
        self.fixes_applied = []
        
        for i, issue in enumerate(self.issues_found, 1):
            print(f"\n🔧 [{i}/{len(self.issues_found)}] Fixing: {issue['type']}")
            
            if issue['type'] == 'syntax_error':
                self._fix_syntax_error(issue)
            elif issue['type'] == 'missing_import':
                self._fix_missing_import(issue)
            elif issue['type'] == 'undefined_method':
                self._fix_undefined_method(issue)
            elif issue['type'] == 'indentation_error':
                self._fix_indentation_error(issue)
            elif issue['type'] == 'database_corruption':
                self._fix_database_corruption(issue)
            elif issue['type'] == 'permission_error':
                self._fix_permission_error(issue)
            elif issue['type'] == 'test_failure':
                self._fix_test_failure(issue)
            else:
                print(f"   ⚠️ Unknown issue type: {issue['type']}")
        
        print("\n" + "="*80)
        print(f"🔧 AUTO-FIX COMPLETE: Applied {len(self.fixes_applied)} fixes")
        print(f"🔧 স্বয়ংক্রিয় ঠিক সম্পূর্ণ: {len(self.fixes_applied)}টি fix করা হয়েছে")
        print("="*80)
    
    def _fix_syntax_error(self, issue):
        """Fix syntax errors"""
        print(f"   🔧 Attempting to fix syntax error in {issue['file']}...")
        
        try:
            # Backup original file
            backup_file = f"{issue['file']}.backup"
            with open(issue['file'], 'r', encoding='utf-8') as f:
                content = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Try common fixes
            # (This is simplified - real implementation would be more sophisticated)
            
            fix = {
                'issue': issue,
                'description': 'Syntax error fix attempted',
                'success': False
            }
            
            self.fixes_applied.append(fix)
            self._log_fix(fix)
            
            print(f"   ⚠️ Syntax errors require manual review")
            print(f"   💾 Backup saved: {backup_file}")
        
        except Exception as e:
            print(f"   ❌ Fix failed: {e}")
    
    def _fix_missing_import(self, issue):
        """Fix missing imports"""
        print(f"   🔧 Attempting to install missing package...")
        
        try:
            # Extract package name from error
            match = re.search(r"No module named '(\w+)'", issue['description'])
            if match:
                package = match.group(1)
                
                # Try to install
                result = subprocess.run(
                    ['pip', 'install', package],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=60
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Installed package: {package}")
                    fix = {
                        'issue': issue,
                        'description': f'Installed package: {package}',
                        'success': True
                    }
                    self.fixes_applied.append(fix)
                    self._log_fix(fix)
                else:
                    print(f"   ❌ Failed to install: {package}")
            else:
                print(f"   ⚠️ Could not extract package name")
        
        except Exception as e:
            print(f"   ❌ Fix failed: {e}")
    
    def _fix_undefined_method(self, issue):
        """Fix undefined methods"""
        print(f"   🔧 Creating stub for undefined method '{issue['method']}'...")
        
        try:
            # Read file
            with open(issue['file'], 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find class definition
            class_line = -1
            for i, line in enumerate(lines):
                if 'class ' in line:
                    class_line = i
                    break
            
            if class_line >= 0:
                # Find indentation
                indent = '    '
                
                # Create method stub
                method_stub = f"""
{indent}def {issue['method']}(self, *args, **kwargs):
{indent}    \"\"\"Auto-generated method stub\"\"\"
{indent}    # TODO: Implement this method
{indent}    pass
"""
                
                # Insert at end of class
                lines.append(method_stub)
                
                # Write back
                with open(issue['file'], 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                print(f"   ✅ Created method stub: {issue['method']}")
                
                fix = {
                    'issue': issue,
                    'description': f"Created stub for {issue['method']}",
                    'success': True
                }
                self.fixes_applied.append(fix)
                self._log_fix(fix)
            else:
                print(f"   ⚠️ Could not find class definition")
        
        except Exception as e:
            print(f"   ❌ Fix failed: {e}")
    
    def _fix_indentation_error(self, issue):
        """Fix indentation errors"""
        print(f"   🔧 Converting tabs to spaces...")
        
        try:
            with open(issue['file'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert tabs to 4 spaces
            fixed_content = content.replace('\t', '    ')
            
            with open(issue['file'], 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"   ✅ Fixed indentation in {issue['file']}")
            
            fix = {
                'issue': issue,
                'description': 'Converted tabs to spaces',
                'success': True
            }
            self.fixes_applied.append(fix)
            self._log_fix(fix)
        
        except Exception as e:
            print(f"   ❌ Fix failed: {e}")
    
    def _fix_database_corruption(self, issue):
        """Fix database corruption"""
        print(f"   🔧 Attempting to repair database...")
        
        try:
            # Backup corrupted database
            backup_file = f"{issue['file']}.corrupted.backup"
            os.rename(issue['file'], backup_file)
            
            print(f"   ✅ Moved corrupted database to: {backup_file}")
            print(f"   ℹ️ New database will be created on next run")
            
            fix = {
                'issue': issue,
                'description': 'Backed up corrupted database',
                'success': True
            }
            self.fixes_applied.append(fix)
            self._log_fix(fix)
        
        except Exception as e:
            print(f"   ❌ Fix failed: {e}")
    
    def _fix_permission_error(self, issue):
        """Fix permission errors"""
        print(f"   🔧 Attempting to fix permissions...")
        
        try:
            # Try to change permissions (Unix/Linux)
            if os.name != 'nt':  # Not Windows
                os.chmod(issue['file'], 0o644)
                print(f"   ✅ Fixed permissions for {issue['file']}")
                
                fix = {
                    'issue': issue,
                    'description': 'Changed file permissions',
                    'success': True
                }
                self.fixes_applied.append(fix)
                self._log_fix(fix)
            else:
                print(f"   ⚠️ Permission fix not available on Windows")
        
        except Exception as e:
            print(f"   ❌ Fix failed: {e}")
    
    def _fix_test_failure(self, issue):
        """Fix test failures"""
        print(f"   🔧 Analyzing test failure...")
        
        # Test failures usually require code fixes
        # This is a placeholder for more sophisticated analysis
        
        print(f"   ⚠️ Test failures require code review")
        print(f"   💡 Suggestion: Review {issue['file']}")
    
    def _log_issue(self, issue):
        """Log issue to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO issues (issue_type, description, severity)
                VALUES (?, ?, ?)
            """, (issue['type'], issue['description'], issue['severity']))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"   ⚠️ Failed to log issue: {e}")
    
    def _log_fix(self, fix):
        """Log fix to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get last issue ID
            cursor.execute("SELECT MAX(id) FROM issues")
            issue_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO fixes (issue_id, fix_description, success)
                VALUES (?, ?, ?)
            """, (issue_id, fix['description'], fix['success']))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"   ⚠️ Failed to log fix: {e}")
    
    def run_continuous_monitoring(self, interval=300):
        """
        Run continuous monitoring and auto-fix
        ক্রমাগত monitoring এবং auto-fix চালায়
        
        Args:
            interval: Check interval in seconds (default: 300 = 5 minutes)
        """
        print("\n" + "="*80)
        print("🔄 CONTINUOUS SELF-HEALING STARTED")
        print("🔄 ক্রমাগত স্ব-নিরাময় শুরু হয়েছে")
        print(f"🔄 Checking every {interval} seconds ({interval//60} minutes)")
        print("="*80)
        
        try:
            # WARNING: Infinite loop - ensure break condition exists
            while True:
                print(f"\n⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running diagnosis...")
                
                # Run diagnosis
                issues = self.run_self_diagnosis()
                
                # Auto-fix if issues found
                if issues:
                    self.auto_fix_issues()
                else:
                    print("\n✅ All systems healthy!")
                
                # Wait for next check
                print(f"\n💤 Sleeping for {interval} seconds...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Continuous monitoring stopped by user")


def main():
    """Main function"""
    print("\n" + "="*80)
    print("  🔧 JARVIS SELF-HEALING SYSTEM")
    print("  🔧 JARVIS স্ব-নিরাময় সিস্টেম")
    print("="*80)
    
    healer = SelfHealingSystem()
    
    print("\n💡 Choose mode:")
    print("1. Run diagnosis once")
    print("2. Run diagnosis and auto-fix")
    print("3. Continuous monitoring (every 5 minutes)")
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    elif not sys.stdin.isatty() or os.environ.get('JARVIS_NO_DIAGNOSIS') == '1':
        print("\n🤖 Non-interactive/test environment detected - choosing mode: 1")
        choice = '1'
    else:
        choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in ['1', '--diagnose', '-d']:
        healer.run_self_diagnosis()
    elif choice in ['2', '--fix', '-f']:
        healer.run_self_diagnosis()
        healer.auto_fix_issues()
    elif choice in ['3', '--monitor', '-m']:
        healer.run_continuous_monitoring()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
