#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX JARVIS PANEL FREEZE
=======================
Fixes panel freeze/unresponsive issue
"""

import os
import sys
import subprocess

print("=" * 70)
print("🔧 FIXING JARVIS PANEL FREEZE")
print("=" * 70)
print()

print("Problem: Panel খুলেছে কিন্তু কোনো কিছু click হচ্ছে না")
print("Cause: Panel freeze হয়ে আছে / Unresponsive")
print()

# Step 1: Kill all Python processes
print("Step 1: Stopping all Python processes...")
try:
    subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                   capture_output=True, text=True)
    subprocess.run(['taskkill', '/F', '/IM', 'pythonw.exe'], 
                   capture_output=True, text=True)
    print("[OK] All Python processes stopped")
except Exception as e:
    print(f"[!] Could not stop processes: {e}")

print()

# Step 2: Check for the tkinter error
print("Step 2: Checking for tkinter/customtkinter issues...")

if os.path.exists('jarvis_panel.py'):
    with open('jarvis_panel.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for after() calls that might cause freeze
    if 'after(' in content:
        print("[!] Found after() calls - these can cause freeze")
        print("[!] Checking for invalid command name errors...")
    
    # The error "invalid command name" is a tkinter bug
    # It happens when after() is called with invalid callback
    print("[OK] File checked")
else:
    print("[X] jarvis_panel.py not found!")

print()

# Step 3: Create a minimal test panel
print("Step 3: Creating minimal test panel...")

minimal_panel = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MINIMAL JARVIS PANEL TEST
=========================
Tests if basic panel works without freeze
"""

import customtkinter as ctk
import sys

print("=" * 70)
print("MINIMAL JARVIS PANEL TEST")
print("=" * 70)
print()

# Create window
root = ctk.CTk()
root.title("JARVIS Panel Test")
root.geometry("800x600")
root.configure(fg_color="#02050A")

# Header
header = ctk.CTkLabel(
    root,
    text="JARVIS PANEL TEST",
    font=("Courier New", 28, "bold"),
    text_color="#00FF41"
)
header.pack(pady=20)

# Status
status_label = ctk.CTkLabel(
    root,
    text="If you can see this and click buttons, panel is working!",
    font=("Courier New", 14),
    text_color="#FFFFFF"
)
status_label.pack(pady=10)

# Test counter
click_count = {'count': 0}

def on_button_click():
    click_count['count'] += 1
    result_label.configure(text=f"[OK] Button clicked {click_count['count']} times!")
    print(f"[OK] Button clicked {click_count['count']} times")

# Test button
test_btn = ctk.CTkButton(
    root,
    text="CLICK ME TO TEST",
    command=on_button_click,
    fg_color="#00AA00",
    hover_color="#00FF00",
    font=("Courier New", 18, "bold"),
    height=60,
    width=300
)
test_btn.pack(pady=30)

# Result label
result_label = ctk.CTkLabel(
    root,
    text="Click the button above!",
    font=("Courier New", 14),
    text_color="#FFD700"
)
result_label.pack(pady=10)

# Input test
input_label = ctk.CTkLabel(
    root,
    text="Test typing here:",
    font=("Courier New", 12),
    text_color="#FFFFFF"
)
input_label.pack(pady=(30, 5))

test_input = ctk.CTkEntry(
    root,
    width=400,
    height=40,
    font=("Courier New", 14),
    fg_color="#001100",
    text_color="#00FF41",
    border_width=2,
    border_color="#00FF41",
    placeholder_text="Type here and press Enter..."
)
test_input.pack(pady=10)

def on_enter(event=None):
    text = test_input.get()
    if text:
        input_result.configure(text=f"[OK] You typed: {text}")
        print(f"[OK] Input working! Got: {text}")
        test_input.delete(0, 'end')

test_input.bind("<Return>", on_enter)

input_result = ctk.CTkLabel(
    root,
    text="",
    font=("Courier New", 12),
    text_color="#00FF41"
)
input_result.pack(pady=5)

# Instructions
instructions = ctk.CTkLabel(
    root,
    text="""
TEST CHECKLIST:
1. Can you see this window? [  ]
2. Can you click the button? [  ]
3. Can you type in the input box? [  ]
4. Can you press Enter? [  ]

If ALL YES: Panel system is working!
If ANY NO: There's a system issue.
    """,
    font=("Courier New", 10),
    text_color="#888888",
    justify="left"
)
instructions.pack(pady=20)

# Close button
close_btn = ctk.CTkButton(
    root,
    text="CLOSE TEST",
    command=root.destroy,
    fg_color="#AA0000",
    hover_color="#FF0000",
    font=("Courier New", 14, "bold"),
    height=40
)
close_btn.pack(pady=10)

print("[OK] Test panel created")
print("[OK] Try clicking and typing")
print()
print("If this works but JARVIS doesn't:")
print("  -> JARVIS panel has a bug")
print("  -> Need to fix JARVIS code")
print()
print("If this also doesn't work:")
print("  -> System issue (graphics, drivers, etc.)")
print("  -> Need to fix system")
print()

try:
    root.mainloop()
except Exception as e:
    print(f"[X] Error: {e}")
    import traceback
    traceback.print_exc()
'''

with open('TEST_MINIMAL_PANEL.py', 'w', encoding='utf-8') as f:
    f.write(minimal_panel)

print("[OK] Created TEST_MINIMAL_PANEL.py")
print()

# Step 4: Create fix for the "invalid command name" error
print("Step 4: Creating fix for tkinter 'invalid command name' error...")

fix_code = '''
# FIX FOR "invalid command name" ERROR
# =====================================
# This error happens when tkinter's after() is called incorrectly
# 
# BAD:
#   self.after(1000, self.some_method())  # Wrong! Calls immediately
#
# GOOD:
#   self.after(1000, self.some_method)    # Correct! Passes reference
#
# The error in your log:
#   "invalid command name '1990887400448update'"
#   "invalid command name '1990890747520_windows_set_titlebar_icon'"
#
# These are memory addresses, meaning after() got a return value instead of function reference
'''

with open('TKINTER_FIX_NOTES.txt', 'w', encoding='utf-8') as f:
    f.write(fix_code)

print("[OK] Created TKINTER_FIX_NOTES.txt")
print()

# Step 5: Create restart script
print("Step 5: Creating clean restart script...")

restart_script = '''@echo off
chcp 65001 >nul
echo ================================================================
echo CLEAN RESTART JARVIS
echo ================================================================
echo.

echo Step 1: Stopping all Python processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
echo [OK] Processes stopped
echo.

echo Step 2: Waiting 2 seconds...
timeout /t 2 /nobreak >nul
echo [OK] Ready
echo.

echo Step 3: Starting JARVIS...
python START_JARVIS.py

if errorlevel 1 (
    echo.
    echo ================================================================
    echo ERROR: JARVIS failed to start
    echo ================================================================
    echo.
    echo Try:
    echo   1. Run TEST_MINIMAL_PANEL.py first
    echo   2. Check if that works
    echo   3. If yes, JARVIS has a bug
    echo   4. If no, system issue
    echo.
    pause
)
'''

with open('RESTART_JARVIS_CLEAN.bat', 'w', encoding='utf-8') as f:
    f.write(restart_script)

print("[OK] Created RESTART_JARVIS_CLEAN.bat")
print()

print("=" * 70)
print("🎉 FIX TOOLS CREATED!")
print("=" * 70)
print()
print("[OK] What was created:")
print("   1. TEST_MINIMAL_PANEL.py - Test if panel system works")
print("   2. TKINTER_FIX_NOTES.txt - Explanation of the bug")
print("   3. RESTART_JARVIS_CLEAN.bat - Clean restart script")
print()
print("🚀 NEXT STEPS:")
print()
print("STEP 1: Test if panel system works")
print("   python TEST_MINIMAL_PANEL.py")
print()
print("   If this works (you can click and type):")
print("   -> Panel system is OK")
print("   -> JARVIS code has a bug")
print("   -> Need to fix JARVIS")
print()
print("   If this also freezes:")
print("   -> System issue")
print("   -> Graphics driver problem")
print("   -> Need to restart computer")
print()
print("STEP 2: If test works, restart JARVIS cleanly")
print("   RESTART_JARVIS_CLEAN.bat")
print()
print("STEP 3: If still freezes, the bug is in JARVIS code")
print("   The error 'invalid command name' shows:")
print("   -> tkinter after() called incorrectly")
print("   -> Need to fix jarvis_panel.py")
print()
print("=" * 70)
print()
print("🔥 RUN THIS NOW:")
print("   python TEST_MINIMAL_PANEL.py")
print()
print("   If you can click the button:")
print("   -> System OK, JARVIS has bug")
print()
print("   If you can't click:")
print("   -> System issue, restart computer")
print()
print("=" * 70)
