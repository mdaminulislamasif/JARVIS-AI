"""
COMPREHENSIVE FIX VERIFICATION
Tests all fixes for API quota problem
"""

import os
import sys

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

print("\n" + "="*80)
print("  🔍 VERIFYING ALL FIXES FOR API QUOTA PROBLEM")
print("  🔍 API QUOTA সমস্যার সব FIX যাচাই করা হচ্ছে")
print("="*80)

# Test 1: Check core/brain.py returns special code
print("\n[TEST 1] Checking core/brain.py...")
try:
    with open('core/brain.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'return "QUOTA_EXCEEDED_USE_OFFLINE"' in content:
            print("✅ core/brain.py: Returns special code QUOTA_EXCEEDED_USE_OFFLINE")
        else:
            print("❌ core/brain.py: Does NOT return special code")
            print("   Expected: return \"QUOTA_EXCEEDED_USE_OFFLINE\"")
except Exception as e:
    print(f"❌ Error reading core/brain.py: {e}")

# Test 2: Check jarvis_panel.py has offline brain fallback AFTER brain.think()
print("\n[TEST 2] Checking jarvis_panel.py...")
try:
    with open('jarvis_panel.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Check for the new fallback code after brain.think()
        if 'if "QUOTA_EXCEEDED_USE_OFFLINE" in str(res) or "all API keys have hit today\'s free quota" in str(res):' in content:
            print("✅ jarvis_panel.py: Has offline brain fallback AFTER brain.think()")
        else:
            print("❌ jarvis_panel.py: Missing offline brain fallback after brain.think()")
        
        # Check for offline brain import
        if 'from jarvis_offline_brain import OfflineBrain' in content:
            print("✅ jarvis_panel.py: Imports OfflineBrain")
        else:
            print("❌ jarvis_panel.py: Does NOT import OfflineBrain")
except Exception as e:
    print(f"❌ Error reading jarvis_panel.py: {e}")

# Test 3: Check engine/multi_brain.py returns special code
print("\n[TEST 3] Checking engine/multi_brain.py...")
try:
    with open('engine/multi_brain.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'return "QUOTA_EXCEEDED_USE_OFFLINE"' in content:
            print("✅ engine/multi_brain.py: Returns special code")
        else:
            print("❌ engine/multi_brain.py: Does NOT return special code")
except Exception as e:
    print(f"❌ Error reading engine/multi_brain.py: {e}")

# Test 4: Check jarvis_offline_brain.py exists and has process_query method
print("\n[TEST 4] Checking jarvis_offline_brain.py...")
try:
    if os.path.exists('jarvis_offline_brain.py'):
        print("✅ jarvis_offline_brain.py: File exists")
        
        with open('jarvis_offline_brain.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'def process_query(self, user_input):' in content:
                print("✅ jarvis_offline_brain.py: Has process_query() method")
            else:
                print("❌ jarvis_offline_brain.py: Missing process_query() method")
            
            if 'class OfflineBrain:' in content:
                print("✅ jarvis_offline_brain.py: Has OfflineBrain class")
            else:
                print("❌ jarvis_offline_brain.py: Missing OfflineBrain class")
    else:
        print("❌ jarvis_offline_brain.py: File does NOT exist")
except Exception as e:
    print(f"❌ Error checking jarvis_offline_brain.py: {e}")

# Test 5: Try importing and using offline brain
print("\n[TEST 5] Testing offline brain functionality...")
try:
    os.environ['JARVIS_NO_DIAGNOSIS'] = '1'
    from jarvis_offline_brain import OfflineBrain
    print("✅ Successfully imported OfflineBrain")
    
    brain = OfflineBrain()
    print("✅ Successfully created OfflineBrain instance")
    
    # Test a simple query
    result = brain.process_query("2+2")
    if result and result.get('status') == 'success':
        print(f"✅ Offline brain works! Response: {result.get('response', '')[:50]}")
    else:
        print(f"⚠️ Offline brain returned: {result}")
except Exception as e:
    print(f"❌ Error testing offline brain: {e}")

# Test 6: Check backup files exist
print("\n[TEST 6] Checking backup files...")
backup_files = [
    'jarvis_panel.py.backup_20260506_002033',
    'engine/multi_brain.py.backup_20260506_002033'
]
for backup in backup_files:
    if os.path.exists(backup):
        print(f"✅ Backup exists: {backup}")
    else:
        print(f"⚠️ Backup not found: {backup}")

# Summary
print("\n" + "="*80)
print("  📊 VERIFICATION SUMMARY")
print("="*80)
print("""
✅ = Fix is in place
❌ = Fix is missing or broken
⚠️ = Warning (not critical)

If all tests show ✅, the fix should work!
If you see ❌, please run this script again or contact support.

NEXT STEPS:
1. Close JARVIS if it's running
2. Run JARVIS.bat or START_JARVIS.bat
3. Type "HELLO" or any command
4. You should see "[OFFLINE]" response instead of quota error

যদি সব টেস্ট ✅ দেখায়, তাহলে FIX কাজ করবে!
যদি ❌ দেখেন, তাহলে আবার চালান বা সাপোর্টে যোগাযোগ করুন।
""")
print("="*80)
