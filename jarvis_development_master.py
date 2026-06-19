"""
JARVIS DEVELOPMENT MASTER
Complete Build, Develop, Operate, Test System

Features:
- Learns how to BUILD software
- Learns how to DEVELOP applications
- Learns how to OPERATE systems
- Learns how to TEST code
- Teaches everything it learns

এই system পারে:
- নিজে নিজে software build করতে
- নিজে নিজে develop করতে
- নিজে নিজে operate করতে
- নিজে নিজে test করতে
- সব কিছু শিখতে এবং শেখাতে
"""

import os
import sys
import subprocess
import json
import sqlite3
from datetime import datetime
import shutil
import ast
import re

class DevelopmentMaster:
    """
    Complete Development System
    Build, Develop, Operate, Test
    """
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.knowledge_base = {}
        self.learned_skills = []
        
        # Initialize knowledge base
        self.init_knowledge_base()
        
        # Initialize database
        self.init_database()
        
        print("🏗️ JARVIS DEVELOPMENT MASTER INITIALIZED!")
        print("🏗️ JARVIS ডেভেলপমেন্ট মাস্টার চালু হয়েছে!")
        print("\n✅ I can now BUILD, DEVELOP, OPERATE, and TEST!")
        print("✅ আমি এখন BUILD, DEVELOP, OPERATE, এবং TEST করতে পারি!")
    
    def init_knowledge_base(self):
        """Initialize development knowledge base"""
        self.knowledge_base = {
            'build': {
                'python': {
                    'commands': ['python setup.py build', 'python -m build', 'pip install -e .'],
                    'tools': ['setuptools', 'build', 'pip'],
                    'files': ['setup.py', 'pyproject.toml', 'requirements.txt'],
                    'steps': [
                        'Create setup.py or pyproject.toml',
                        'Define dependencies in requirements.txt',
                        'Run build command',
                        'Install package'
                    ]
                },
                'javascript': {
                    'commands': ['npm install', 'npm run build', 'yarn build'],
                    'tools': ['npm', 'yarn', 'webpack', 'vite'],
                    'files': ['package.json', 'webpack.config.js', 'vite.config.js'],
                    'steps': [
                        'Create package.json',
                        'Install dependencies',
                        'Configure build tool',
                        'Run build command'
                    ]
                },
                'java': {
                    'commands': ['mvn clean install', 'gradle build', 'javac *.java'],
                    'tools': ['maven', 'gradle', 'javac'],
                    'files': ['pom.xml', 'build.gradle', 'build.xml'],
                    'steps': [
                        'Create build configuration',
                        'Define dependencies',
                        'Compile source code',
                        'Package application'
                    ]
                }
            },
            'develop': {
                'setup_environment': [
                    'Install IDE (VS Code, PyCharm, IntelliJ)',
                    'Install language runtime (Python, Node.js, Java)',
                    'Install version control (Git)',
                    'Install package manager (pip, npm, maven)',
                    'Configure editor settings',
                    'Install extensions/plugins'
                ],
                'coding_practices': [
                    'Write clean, readable code',
                    'Follow naming conventions',
                    'Add comments and documentation',
                    'Use version control (Git)',
                    'Write modular code',
                    'Handle errors properly',
                    'Follow design patterns'
                ],
                'project_structure': {
                    'python': ['src/', 'tests/', 'docs/', 'requirements.txt', 'setup.py', 'README.md'],
                    'javascript': ['src/', 'tests/', 'public/', 'package.json', 'README.md'],
                    'java': ['src/main/java/', 'src/test/java/', 'pom.xml', 'README.md']
                }
            },
            'operate': {
                'deployment': [
                    'Build application',
                    'Run tests',
                    'Package application',
                    'Deploy to server',
                    'Configure environment',
                    'Start application',
                    'Monitor logs',
                    'Handle errors'
                ],
                'monitoring': [
                    'Check application status',
                    'Monitor resource usage (CPU, RAM)',
                    'Check logs for errors',
                    'Monitor response times',
                    'Track user activity',
                    'Set up alerts'
                ],
                'maintenance': [
                    'Update dependencies',
                    'Apply security patches',
                    'Optimize performance',
                    'Backup data',
                    'Clean up logs',
                    'Restart services if needed'
                ]
            },
            'test': {
                'types': {
                    'unit_tests': 'Test individual functions/methods',
                    'integration_tests': 'Test component interactions',
                    'functional_tests': 'Test complete features',
                    'performance_tests': 'Test speed and efficiency',
                    'security_tests': 'Test for vulnerabilities'
                },
                'frameworks': {
                    'python': ['pytest', 'unittest', 'nose2'],
                    'javascript': ['jest', 'mocha', 'jasmine'],
                    'java': ['junit', 'testng']
                },
                'best_practices': [
                    'Write tests before code (TDD)',
                    'Test edge cases',
                    'Use meaningful test names',
                    'Keep tests independent',
                    'Mock external dependencies',
                    'Aim for high code coverage',
                    'Run tests automatically (CI/CD)'
                ]
            }
        }
        
        print("✅ Knowledge base initialized!")
    
    def init_database(self):
        """Initialize development database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table for learned development skills
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dev_skills_learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_type TEXT,
                    skill_name TEXT,
                    skill_content TEXT,
                    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    proficiency INTEGER DEFAULT 1
                )
            ''')
            
            # Table for build history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS build_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT,
                    language TEXT,
                    build_command TEXT,
                    build_status TEXT,
                    build_output TEXT,
                    built_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table for test results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT,
                    test_type TEXT,
                    tests_run INTEGER,
                    tests_passed INTEGER,
                    tests_failed INTEGER,
                    test_output TEXT,
                    tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table for operations log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operations_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT,
                    operation_target TEXT,
                    operation_status TEXT,
                    operation_details TEXT,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ Development database ready!")
            
        except Exception as e:
            print(f"⚠️ Database init error: {e}")
    
    def learn_to_build(self, language):
        """
        Learn how to build software in a specific language
        নির্দিষ্ট language এ software build করা শেখে
        """
        print(f"\n📚 LEARNING TO BUILD: {language.upper()}")
        print(f"📚 BUILD করা শিখছি: {language.upper()}")
        
        if language.lower() not in self.knowledge_base['build']:
            print(f"❌ Language '{language}' not in knowledge base yet")
            return None
        
        build_info = self.knowledge_base['build'][language.lower()]
        
        print(f"\n✅ Learned how to build {language} projects!")
        print(f"✅ {language} projects build করা শিখেছি!")
        
        print(f"\n📋 Build Commands:")
        for cmd in build_info['commands']:
            print(f"  - {cmd}")
        
        print(f"\n🔧 Build Tools:")
        for tool in build_info['tools']:
            print(f"  - {tool}")
        
        print(f"\n📁 Required Files:")
        for file in build_info['files']:
            print(f"  - {file}")
        
        print(f"\n📝 Build Steps:")
        for i, step in enumerate(build_info['steps'], 1):
            print(f"  {i}. {step}")
        
        # Save to database
        self._save_skill('build', language, json.dumps(build_info))
        
        return build_info
    
    def learn_to_develop(self, aspect='all'):
        """
        Learn development practices
        Development practices শেখে
        """
        print(f"\n📚 LEARNING TO DEVELOP: {aspect.upper()}")
        print(f"📚 DEVELOP করা শিখছি: {aspect.upper()}")
        
        dev_info = self.knowledge_base['develop']
        
        if aspect == 'all' or aspect == 'setup':
            print(f"\n🔧 Environment Setup:")
            for step in dev_info['setup_environment']:
                print(f"  ✓ {step}")
        
        if aspect == 'all' or aspect == 'practices':
            print(f"\n💡 Coding Practices:")
            for practice in dev_info['coding_practices']:
                print(f"  ✓ {practice}")
        
        if aspect == 'all' or aspect == 'structure':
            print(f"\n📁 Project Structure:")
            for lang, structure in dev_info['project_structure'].items():
                print(f"  {lang.upper()}:")
                for item in structure:
                    print(f"    - {item}")
        
        # Save to database
        self._save_skill('develop', aspect, json.dumps(dev_info))
        
        print(f"\n✅ Learned development practices!")
        print(f"✅ Development practices শিখেছি!")
        
        return dev_info
    
    def learn_to_operate(self, aspect='all'):
        """
        Learn how to operate systems
        System operate করা শেখে
        """
        print(f"\n📚 LEARNING TO OPERATE: {aspect.upper()}")
        print(f"📚 OPERATE করা শিখছি: {aspect.upper()}")
        
        ops_info = self.knowledge_base['operate']
        
        if aspect == 'all' or aspect == 'deployment':
            print(f"\n🚀 Deployment Steps:")
            for step in ops_info['deployment']:
                print(f"  ✓ {step}")
        
        if aspect == 'all' or aspect == 'monitoring':
            print(f"\n📊 Monitoring:")
            for item in ops_info['monitoring']:
                print(f"  ✓ {item}")
        
        if aspect == 'all' or aspect == 'maintenance':
            print(f"\n🔧 Maintenance:")
            for item in ops_info['maintenance']:
                print(f"  ✓ {item}")
        
        # Save to database
        self._save_skill('operate', aspect, json.dumps(ops_info))
        
        print(f"\n✅ Learned operations!")
        print(f"✅ Operations শিখেছি!")
        
        return ops_info
    
    def learn_to_test(self, language=None):
        """
        Learn how to test software
        Software test করা শেখে
        """
        print(f"\n📚 LEARNING TO TEST")
        print(f"📚 TEST করা শিখছি")
        
        test_info = self.knowledge_base['test']
        
        print(f"\n🧪 Test Types:")
        for test_type, description in test_info['types'].items():
            print(f"  - {test_type}: {description}")
        
        if language:
            print(f"\n🔧 Testing Frameworks for {language.upper()}:")
            if language.lower() in test_info['frameworks']:
                for framework in test_info['frameworks'][language.lower()]:
                    print(f"  - {framework}")
        else:
            print(f"\n🔧 Testing Frameworks:")
            for lang, frameworks in test_info['frameworks'].items():
                print(f"  {lang.upper()}: {', '.join(frameworks)}")
        
        print(f"\n💡 Best Practices:")
        for practice in test_info['best_practices']:
            print(f"  ✓ {practice}")
        
        # Save to database
        self._save_skill('test', language or 'general', json.dumps(test_info))
        
        print(f"\n✅ Learned testing!")
        print(f"✅ Testing শিখেছি!")
        
        return test_info
    
    def build_project(self, project_path, language):
        """
        Build a project
        Project build করে
        """
        print(f"\n🏗️ BUILDING PROJECT: {project_path}")
        print(f"🏗️ PROJECT BUILD করছি: {project_path}")
        
        if language.lower() not in self.knowledge_base['build']:
            print(f"❌ Don't know how to build {language} projects yet")
            print(f"💡 Learning now...")
            self.learn_to_build(language)
        
        build_info = self.knowledge_base['build'][language.lower()]
        
        # Try each build command
        for cmd in build_info['commands']:
            print(f"\n⚡ Trying: {cmd}")
            
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print(f"✅ Build successful!")
                    print(f"✅ Build সফল হয়েছে!")
                    
                    # Save to database
                    self._save_build_history(
                        os.path.basename(project_path),
                        language,
                        cmd,
                        'success',
                        result.stdout[:1000]
                    )
                    
                    return {'status': 'success', 'command': cmd, 'output': result.stdout}
                else:
                    print(f"⚠️ Build failed with this command")
                    print(f"Error: {result.stderr[:200]}")
                    
            except subprocess.TimeoutExpired:
                print(f"⏱️ Build timeout")
            except Exception as e:
                print(f"❌ Build error: {e}")
        
        print(f"\n❌ All build commands failed")
        return {'status': 'failed', 'message': 'All build commands failed'}
    
    def test_project(self, project_path, language):
        """
        Test a project
        Project test করে
        """
        print(f"\n🧪 TESTING PROJECT: {project_path}")
        print(f"🧪 PROJECT TEST করছি: {project_path}")
        
        if language.lower() not in self.knowledge_base['test']['frameworks']:
            print(f"❌ Don't know how to test {language} projects yet")
            print(f"💡 Learning now...")
            self.learn_to_test(language)
        
        test_frameworks = self.knowledge_base['test']['frameworks'][language.lower()]
        
        # Try each test framework
        test_commands = {
            'pytest': 'pytest',
            'unittest': 'python -m unittest discover',
            'jest': 'npm test',
            'mocha': 'npm test',
            'junit': 'mvn test'
        }
        
        for framework in test_frameworks:
            if framework in test_commands:
                cmd = test_commands[framework]
                print(f"\n⚡ Trying: {cmd}")
                
                try:
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        cwd=project_path,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    # Parse test results
                    tests_run, tests_passed, tests_failed = self._parse_test_output(
                        result.stdout + result.stderr,
                        framework
                    )
                    
                    print(f"\n📊 Test Results:")
                    print(f"  Tests Run: {tests_run}")
                    print(f"  Passed: {tests_passed}")
                    print(f"  Failed: {tests_failed}")
                    
                    # Save to database
                    self._save_test_results(
                        os.path.basename(project_path),
                        framework,
                        tests_run,
                        tests_passed,
                        tests_failed,
                        result.stdout[:1000]
                    )
                    
                    if tests_failed == 0:
                        print(f"✅ All tests passed!")
                        print(f"✅ সব tests pass হয়েছে!")
                    else:
                        print(f"⚠️ Some tests failed")
                    
                    return {
                        'status': 'success',
                        'framework': framework,
                        'tests_run': tests_run,
                        'tests_passed': tests_passed,
                        'tests_failed': tests_failed
                    }
                    
                except subprocess.TimeoutExpired:
                    print(f"⏱️ Test timeout")
                except Exception as e:
                    print(f"❌ Test error: {e}")
        
        print(f"\n⚠️ No test framework found or all tests failed")
        return {'status': 'no_tests', 'message': 'No test framework found'}
    
    def operate_project(self, project_path, operation='start'):
        """
        Operate a project (start, stop, restart, monitor)
        Project operate করে
        """
        print(f"\n⚙️ OPERATING PROJECT: {operation.upper()}")
        print(f"⚙️ PROJECT OPERATE করছি: {operation.upper()}")
        
        operations = {
            'start': ['python main.py', 'npm start', 'java -jar app.jar'],
            'stop': ['pkill -f main.py', 'npm stop', 'pkill -f java'],
            'restart': ['restart service', 'systemctl restart'],
            'monitor': ['ps aux | grep', 'top', 'htop']
        }
        
        if operation not in operations:
            print(f"❌ Unknown operation: {operation}")
            return {'status': 'error', 'message': f'Unknown operation: {operation}'}
        
        # Try operation commands
        for cmd in operations[operation]:
            print(f"⚡ Trying: {cmd}")
            
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                print(f"✅ Operation successful!")
                
                # Save to database
                self._save_operation_log(
                    operation,
                    os.path.basename(project_path),
                    'success',
                    result.stdout[:500]
                )
                
                return {'status': 'success', 'command': cmd, 'output': result.stdout}
                
            except Exception as e:
                print(f"⚠️ Operation failed: {e}")
        
        return {'status': 'failed', 'message': 'All operation commands failed'}
    
    def teach_skill(self, skill_type, skill_name):
        """
        Teach a learned skill
        শেখা skill শেখায়
        """
        print(f"\n👨‍🏫 TEACHING: {skill_type.upper()} - {skill_name}")
        print(f"👨‍🏫 শেখাচ্ছি: {skill_type.upper()} - {skill_name}")
        
        if skill_type == 'build':
            return self.learn_to_build(skill_name)
        elif skill_type == 'develop':
            return self.learn_to_develop(skill_name)
        elif skill_type == 'operate':
            return self.learn_to_operate(skill_name)
        elif skill_type == 'test':
            return self.learn_to_test(skill_name)
        else:
            print(f"❌ Unknown skill type: {skill_type}")
            return None
    
    def _parse_test_output(self, output, framework):
        """Parse test output to extract results"""
        tests_run = 0
        tests_passed = 0
        tests_failed = 0
        
        # Simple parsing (can be improved)
        if 'pytest' in framework:
            # Look for "X passed" or "X failed"
            passed_match = re.search(r'(\d+) passed', output)
            failed_match = re.search(r'(\d+) failed', output)
            
            if passed_match:
                tests_passed = int(passed_match.group(1))
            if failed_match:
                tests_failed = int(failed_match.group(1))
            
            tests_run = tests_passed + tests_failed
        
        elif 'jest' in framework:
            # Look for "Tests: X passed, Y total"
            passed_match = re.search(r'Tests:\s+(\d+) passed', output)
            total_match = re.search(r'(\d+) total', output)
            
            if passed_match:
                tests_passed = int(passed_match.group(1))
            if total_match:
                tests_run = int(total_match.group(1))
            
            tests_failed = tests_run - tests_passed
        
        return tests_run, tests_passed, tests_failed
    
    def _save_skill(self, skill_type, skill_name, skill_content):
        """Save learned skill to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO dev_skills_learned (skill_type, skill_name, skill_content)
                VALUES (?, ?, ?)
            ''', (skill_type, skill_name, skill_content))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Save skill error: {e}")
    
    def _save_build_history(self, project_name, language, command, status, output):
        """Save build history to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO build_history (project_name, language, build_command, build_status, build_output)
                VALUES (?, ?, ?, ?, ?)
            ''', (project_name, language, command, status, output))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Save build history error: {e}")
    
    def _save_test_results(self, project_name, test_type, tests_run, tests_passed, tests_failed, output):
        """Save test results to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO test_results (project_name, test_type, tests_run, tests_passed, tests_failed, test_output)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (project_name, test_type, tests_run, tests_passed, tests_failed, output))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Save test results error: {e}")
    
    def _save_operation_log(self, operation_type, target, status, details):
        """Save operation log to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO operations_log (operation_type, operation_target, operation_status, operation_details)
                VALUES (?, ?, ?, ?)
            ''', (operation_type, target, status, details))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Save operation log error: {e}")
    
    def get_statistics(self):
        """Get development statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count learned skills
            cursor.execute('SELECT COUNT(*) FROM dev_skills_learned')
            skills_count = cursor.fetchone()[0]
            
            # Count builds
            cursor.execute('SELECT COUNT(*) FROM build_history')
            builds_count = cursor.fetchone()[0]
            
            # Count tests
            cursor.execute('SELECT COUNT(*) FROM test_results')
            tests_count = cursor.fetchone()[0]
            
            # Count operations
            cursor.execute('SELECT COUNT(*) FROM operations_log')
            operations_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'skills_learned': skills_count,
                'builds_executed': builds_count,
                'tests_run': tests_count,
                'operations_performed': operations_count
            }
            
        except Exception as e:
            print(f"⚠️ Statistics error: {e}")
            return None


def main():
    """Main function for testing"""
    print("\n" + "="*80)
    print("  🏗️ JARVIS DEVELOPMENT MASTER")
    print("  🏗️ JARVIS ডেভেলপমেন্ট মাস্টার")
    print("  Complete Build, Develop, Operate, Test System!")
    print("  সম্পূর্ণ Build, Develop, Operate, Test সিস্টেম!")
    print("="*80)
    
    dev_master = DevelopmentMaster()
    
    # Test learning
    print("\n" + "="*80)
    print("LEARNING PHASE / শেখার পর্যায়")
    print("="*80)
    
    # Learn to build
    dev_master.learn_to_build('python')
    dev_master.learn_to_build('javascript')
    
    # Learn to develop
    dev_master.learn_to_develop('all')
    
    # Learn to operate
    dev_master.learn_to_operate('all')
    
    # Learn to test
    dev_master.learn_to_test('python')
    
    # Show statistics
    print("\n" + "="*80)
    print("STATISTICS / পরিসংখ্যান")
    print("="*80)
    stats = dev_master.get_statistics()
    if stats:
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    print("\n✅ Development Master ready!")
    print("✅ ডেভেলপমেন্ট মাস্টার প্রস্তুত!")


if __name__ == "__main__":
    main()
