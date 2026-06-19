"""
QUICK TEST - Self-Builder Integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_offline_brain import OfflineBrain

print("\n" + "="*80)
print("  QUICK SELF-BUILDER TEST")
print("="*80)

# Initialize JARVIS
print("\n1. Initializing JARVIS...")
jarvis = OfflineBrain()

# Check if Self-Builder is available
print("\n2. Checking Self-Builder...")
if hasattr(jarvis, 'self_builder') and jarvis.self_builder is not None:
    print("[OK] Self-Builder available!")
else:
    print("[FAIL] Self-Builder NOT available!")
    sys.exit(1)

# Test commands
commands = [
    "suggest features",
    "analyze yourself",
    "feature status"
]

print("\n3. Testing commands...")
for cmd in commands:
    print(f"\n{'='*80}")
    print(f"  Testing: {cmd}")
    print(f"{'='*80}")
    
    try:
        result = jarvis.process_command(cmd)
        print(f"\nStatus: {result.get('status')}")
        print(f"Type: {result.get('type')}")
        print(f"\nResponse (first 500 chars):")
        print(result.get('response', 'No response')[:500])
        
        if result.get('status') == 'success':
            print(f"\n[PASS] {cmd}")
        else:
            print(f"\n[FAIL] {cmd}")
    except Exception as e:
        print(f"\n[ERROR] {e}")

print("\n" + "="*80)
print("  TEST COMPLETE!")
print("="*80)
