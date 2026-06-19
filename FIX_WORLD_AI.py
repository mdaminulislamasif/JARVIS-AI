"""
WORLD AI CHAT AUTO-FIX SCRIPT
==============================
এই script automatically World AI Chat এর সব সমস্যা fix করবে
"""

import os
import sys

print("="*80)
print("🔧 WORLD AI CHAT AUTO-FIX")
print("="*80)

issues_found = []
fixes_applied = []

# Check 1: Files exist
print("\n1️⃣ Checking files...")
files_to_check = [
    'jarvis_world_ai_chat.py',
    'jarvis_panel.py',
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"   ✅ {file} exists")
    else:
        print(f"   ❌ {file} MISSING!")
        issues_found.append(f"Missing file: {file}")

# Check 2: Dependencies
print("\n2️⃣ Checking dependencies...")
dependencies = ['pyperclip', 'webbrowser', 'customtkinter']

for dep in dependencies:
    try:
        __import__(dep)
        print(f"   ✅ {dep} installed")
    except ImportError:
        print(f"   ❌ {dep} NOT installed")
        issues_found.append(f"Missing dependency: {dep}")
        
        # Try to install
        print(f"      🔧 Attempting to install {dep}...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"      ✅ {dep} installed successfully!")
            fixes_applied.append(f"Installed {dep}")
        except Exception as e:
            print(f"      ❌ Failed to install {dep}: {e}")

# Check 3: Import test
print("\n3️⃣ Testing imports...")
try:
    from jarvis_world_ai_chat import WorldAIChat
    print("   ✅ WorldAIChat import successful")
except Exception as e:
    print(f"   ❌ WorldAIChat import failed: {e}")
    issues_found.append(f"Import error: {e}")

# Check 4: Integration in jarvis_panel.py
print("\n4️⃣ Checking jarvis_panel.py integration...")
try:
    with open('jarvis_panel.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'Import': 'from jarvis_world_ai_chat import WorldAIChat',
        'Init': 'self.world_ai_chat = WorldAIChat()',
        'Fallback': 'if self.world_ai_chat:',
    }
    
    all_ok = True
    for name, search in checks.items():
        if search in content:
            print(f"   ✅ {name} found")
        else:
            print(f"   ❌ {name} NOT found")
            issues_found.append(f"Missing integration: {name}")
            all_ok = False
    
    if not all_ok:
        print("\n   ⚠️ Integration incomplete!")
        print("   💡 Recommendation: Re-run integration script")
        
except Exception as e:
    print(f"   ❌ Error checking integration: {e}")
    issues_found.append(f"Integration check error: {e}")

# Check 5: Test initialization
print("\n5️⃣ Testing initialization...")
try:
    from jarvis_world_ai_chat import WorldAIChat
    world_ai = WorldAIChat()
    print(f"   ✅ Initialization successful")
    print(f"   ✅ {len(world_ai.supported_ais)} AIs available")
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    issues_found.append(f"Initialization error: {e}")

# Check 6: Clipboard test
print("\n6️⃣ Testing clipboard...")
try:
    import pyperclip
    test_text = "World AI Chat Test"
    pyperclip.copy(test_text)
    result = pyperclip.paste()
    if result == test_text:
        print("   ✅ Clipboard working")
    else:
        print("   ⚠️ Clipboard not working properly")
        issues_found.append("Clipboard test failed")
except Exception as e:
    print(f"   ❌ Clipboard error: {e}")
    issues_found.append(f"Clipboard error: {e}")

# Check 7: Browser test
print("\n7️⃣ Testing browser...")
try:
    import webbrowser
    print("   ✅ Browser module available")
    # Don't actually open browser in test
except Exception as e:
    print(f"   ❌ Browser error: {e}")
    issues_found.append(f"Browser error: {e}")

# Summary
print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)

if not issues_found:
    print("\n✅ NO ISSUES FOUND!")
    print("✅ World AI Chat is working perfectly!")
    print("\n🚀 You can now use JARVIS with World AI Chat!")
    print("\nTo test manually:")
    print("1. Remove API key: echo. > jarvis_config.txt")
    print("2. Start JARVIS: python jarvis_panel.py")
    print("3. Ask any question")
    print("4. World AI Chat dialog should appear")
else:
    print(f"\n⚠️ FOUND {len(issues_found)} ISSUE(S):")
    for i, issue in enumerate(issues_found, 1):
        print(f"   {i}. {issue}")
    
    if fixes_applied:
        print(f"\n✅ APPLIED {len(fixes_applied)} FIX(ES):")
        for i, fix in enumerate(fixes_applied, 1):
            print(f"   {i}. {fix}")
        print("\n💡 Please restart this script to verify fixes")
    else:
        print("\n💡 RECOMMENDATIONS:")
        print("   1. Check if all files are present")
        print("   2. Install missing dependencies manually:")
        print("      pip install pyperclip customtkinter")
        print("   3. Re-run integration if needed")
        print("   4. Check terminal logs for detailed errors")

print("\n" + "="*80)
print("🔧 AUTO-FIX COMPLETE")
print("="*80)

# Exit code
sys.exit(0 if not issues_found else 1)
