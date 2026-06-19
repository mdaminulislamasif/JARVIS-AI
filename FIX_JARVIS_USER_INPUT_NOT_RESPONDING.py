"""
FIX: JARVIS Not Responding to User Input
JARVIS talks to other AIs but doesn't reply to user commands
"""

import os
import sys

print("=" * 80)
print("🔧 FIXING JARVIS USER INPUT RESPONSE")
print("=" * 80)
print()

print("সমস্যা: JARVIS দুনিয়ার সব AI এর সাথে কথা বলতে পারে কিন্তু")
print("        আপনার কথার reply দিচ্ছে না")
print()
print("Problem: JARVIS can talk to all AIs in the world but")
print("         doesn't reply to your commands")
print()
print("=" * 80)
print()

# Check 1: Duplicate binding
print("CHECK 1: Entry Widget Binding")
print("-" * 80)

with open("jarvis_panel.py", "r", encoding="utf-8") as f:
    content = f.read()

# Count how many times entry.bind is called
bind_count = content.count('self.entry.bind("<Return>"')
print(f"Found {bind_count} entry.bind('<Return>') calls")

if bind_count > 1:
    print("❌ PROBLEM: Duplicate binding found!")
    print("   This can cause the Enter key to not work properly")
    print()
    print("🔧 FIX: Remove duplicate binding")
    print()
else:
    print("✅ No duplicate binding")
    print()

# Check 2: fire_cmd method
print("CHECK 2: fire_cmd() Method")
print("-" * 80)

if "def fire_cmd(self):" in content:
    print("✅ fire_cmd() method exists")
    
    # Check if it calls process()
    fire_cmd_start = content.find("def fire_cmd(self):")
    fire_cmd_section = content[fire_cmd_start:fire_cmd_start + 1500]
    
    if "self.process" in fire_cmd_section:
        print("✅ fire_cmd() calls self.process()")
    else:
        print("❌ fire_cmd() does NOT call self.process()")
    
    if "self.log" in fire_cmd_section:
        print("✅ fire_cmd() logs user input")
    else:
        print("❌ fire_cmd() does NOT log user input")
    
    print()
else:
    print("❌ fire_cmd() method NOT FOUND")
    print()

# Check 3: Natural Interface errors
print("CHECK 3: Natural Interface")
print("-" * 80)

if "self.natural_interface" in content:
    print("✅ Natural Interface is used")
    
    # Check if there's error handling
    if "Natural Interface error" in content:
        print("✅ Has error handling for Natural Interface")
        print("   If Natural Interface fails, falls back to direct processing")
    else:
        print("⚠️ No error handling for Natural Interface")
    
    print()
else:
    print("⚠️ Natural Interface not used")
    print()

# Check 4: process() method
print("CHECK 4: process() Method")
print("-" * 80)

if "def process(self, query):" in content:
    print("✅ process() method exists")
    
    process_start = content.find("def process(self, query):")
    process_section = content[process_start:process_start + 2000]
    
    checks = {
        "Sets thinking state": "self.core.set_state" in process_section,
        "Has greeting detection": "greeting_keywords" in process_section,
        "Has offline brain fallback": "OfflineBrain" in process_section,
        "Speaks response": "self.speak" in process_section or "voice.speak" in process_section,
        "Logs response": "self.log" in process_section,
    }
    
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
    
    print()
else:
    print("❌ process() method NOT FOUND")
    print()

# Check 5: Entry widget creation
print("CHECK 5: Entry Widget")
print("-" * 80)

if "self.entry = ctk.CTkEntry" in content:
    print("✅ Entry widget created")
    
    # Find entry widget section
    entry_start = content.find("self.entry = ctk.CTkEntry")
    entry_section = content[entry_start:entry_start + 500]
    
    if ".pack(" in entry_section:
        print("✅ Entry widget packed (visible)")
    else:
        print("❌ Entry widget might not be visible")
    
    print()
else:
    print("❌ Entry widget NOT FOUND")
    print()

print("=" * 80)
print("DIAGNOSIS")
print("=" * 80)
print()

# Diagnosis
issues_found = []

if bind_count > 1:
    issues_found.append("Duplicate entry binding")

if "Natural Interface error" not in content:
    issues_found.append("No Natural Interface error handling")

if issues_found:
    print("❌ ISSUES FOUND:")
    for i, issue in enumerate(issues_found, 1):
        print(f"  {i}. {issue}")
    print()
else:
    print("✅ No obvious code issues found")
    print()
    print("The problem might be:")
    print("  1. Natural Interface is throwing errors")
    print("  2. process() method is not being called")
    print("  3. Threading issue preventing execution")
    print("  4. Entry widget focus issue")
    print()

print("=" * 80)
print("SOLUTIONS")
print("=" * 80)
print()

print("SOLUTION 1: Remove Duplicate Binding")
print("-" * 80)
print("If duplicate binding found, keep only one:")
print()
print("# REMOVE THIS LINE (duplicate):")
print('self.entry.bind("<Return>", lambda e: self.fire_cmd())')
print()
print("# KEEP ONLY ONE:")
print('self.entry.bind("<Return>", lambda e: self.fire_cmd())')
print()

print("SOLUTION 2: Add Debug Logging")
print("-" * 80)
print("Add debug prints to see where it stops:")
print()
print("def fire_cmd(self):")
print('    print("🔍 DEBUG: fire_cmd() called")')
print("    q = self.entry.get()")
print('    print(f"🔍 DEBUG: User input: {q}")')
print("    if q:")
print('        print("🔍 DEBUG: Processing input...")')
print("        self.entry.delete(0, 'end')")
print('        self.log("ROOT", q)')
print('        print("🔍 DEBUG: Calling process()...")')
print("        threading.Thread(target=self.process, args=(q,), daemon=True).start()")
print('        print("🔍 DEBUG: Thread started")')
print()

print("SOLUTION 3: Bypass Natural Interface")
print("-" * 80)
print("Temporarily disable Natural Interface to test:")
print()
print("def fire_cmd(self):")
print("    q = self.entry.get()")
print("    if q:")
print("        self.entry.delete(0, 'end')")
print('        self.log("ROOT", q)')
print("        # Direct processing (bypass Natural Interface)")
print("        threading.Thread(target=self.process, args=(q,), daemon=True).start()")
print()

print("SOLUTION 4: Test Entry Widget")
print("-" * 80)
print("Check if entry widget is receiving input:")
print()
print("1. Click in the entry box")
print("2. Type something")
print("3. Press Enter")
print("4. Check terminal for debug messages")
print()

print("=" * 80)
print("QUICK FIX")
print("=" * 80)
print()
print("Try these steps in order:")
print()
print("1. Click in the chat input box at the bottom")
print("2. Type: hello")
print("3. Press Enter")
print("4. Wait 2-3 seconds")
print("5. Check terminal output")
print()
print("If you see:")
print('  [ROOT]> hello')
print("  But no [JARVIS]> response")
print()
print("Then the problem is in process() method, not fire_cmd()")
print()
print("If you DON'T see [ROOT]> hello")
print("Then fire_cmd() is not being called")
print()
print("=" * 80)
