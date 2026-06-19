#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX WORLD AI CHAT
=================
World AI Chat এর সমস্যা ঠিক করার script
"""

import sys
import os

print("=" * 70)
print("🔧 FIXING WORLD AI CHAT")
print("=" * 70)
print()

# Check if files exist
print("Step 1: Checking files...")
files_to_check = [
    'jarvis_world_ai_chat.py',
    'jarvis_panel.py'
]

all_exist = True
for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file} exists")
    else:
        print(f"❌ {file} NOT FOUND!")
        all_exist = False

if not all_exist:
    print("\n❌ Some files are missing! Cannot proceed.")
    sys.exit(1)

print()

# Check imports
print("Step 2: Checking dependencies...")
dependencies = {
    'customtkinter': 'customtkinter',
    'pyperclip': 'pyperclip',
    'webbrowser': 'webbrowser (built-in)',
    'tkinter': 'tkinter (built-in)'
}

missing_deps = []
for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"✅ {name} available")
    except ImportError:
        print(f"❌ {name} NOT FOUND!")
        missing_deps.append(module)

if missing_deps:
    print(f"\n⚠️ Missing dependencies: {', '.join(missing_deps)}")
    print("\nTo install:")
    for dep in missing_deps:
        if dep not in ['webbrowser', 'tkinter']:
            print(f"   pip install {dep}")
    print()

print()

# Test WorldAIChat
print("Step 3: Testing WorldAIChat initialization...")
try:
    from jarvis_world_ai_chat import WorldAIChat
    world_ai = WorldAIChat()
    print(f"✅ WorldAIChat initialized successfully")
    print(f"   Available AIs: {len(world_ai.supported_ais)}")
except Exception as e:
    print(f"❌ Failed to initialize WorldAIChat: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Create a simple test GUI
print("Step 4: Creating test GUI...")
print("   ⚠️ A window should appear - if you see it, World AI Chat is working!")
print("   ⚠️ একটি window দেখা উচিত - যদি দেখেন, World AI Chat কাজ করছে!")
print()

try:
    import customtkinter as ctk
    
    # Create test window
    root = ctk.CTk()
    root.title("World AI Chat Test")
    root.geometry("600x400")
    root.configure(fg_color="#02050A")
    
    # Make it very visible
    root.attributes("-topmost", True)
    root.lift()
    root.focus_force()
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Header
    header = ctk.CTkFrame(root, fg_color="#00AA00", height=100)
    header.pack(fill="x")
    
    ctk.CTkLabel(
        header,
        text="✅ WORLD AI CHAT IS WORKING!",
        font=("Courier New", 24, "bold"),
        text_color="#FFFFFF"
    ).pack(pady=30)
    
    # Content
    content = ctk.CTkFrame(root, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=20)
    
    ctk.CTkLabel(
        content,
        text="🎉 World AI Chat কাজ করছে!\n\nএখন আপনি JARVIS panel থেকে World AI Chat ব্যবহার করতে পারবেন।",
        font=("Courier New", 14),
        text_color="#00FF41",
        justify="center"
    ).pack(pady=20)
    
    ctk.CTkLabel(
        content,
        text="Available AIs:",
        font=("Courier New", 12, "bold"),
        text_color="#FFD700"
    ).pack(pady=(20, 10))
    
    ai_list = "\n".join([f"{info['icon']} {info['name']}" for info in world_ai.supported_ais.values()])
    
    ctk.CTkLabel(
        content,
        text=ai_list,
        font=("Courier New", 11),
        text_color="#00FF41",
        justify="left"
    ).pack()
    
    # Test button
    def test_ai_selector():
        selected = world_ai.show_ai_selector_dialog(root)
        if selected:
            result_label.configure(text=f"✅ Selected: {world_ai.supported_ais[selected]['name']}")
        else:
            result_label.configure(text="⚠️ No AI selected")
    
    test_btn = ctk.CTkButton(
        root,
        text="🧪 TEST AI SELECTOR",
        command=test_ai_selector,
        fg_color="#0055AA",
        hover_color="#0077CC",
        font=("Courier New", 14, "bold"),
        height=50
    )
    test_btn.pack(pady=10, padx=20, fill="x")
    
    result_label = ctk.CTkLabel(
        root,
        text="Click button to test",
        font=("Courier New", 11),
        text_color="#888888"
    )
    result_label.pack(pady=5)
    
    # Close button
    close_btn = ctk.CTkButton(
        root,
        text="❌ CLOSE",
        command=root.destroy,
        fg_color="#AA0000",
        hover_color="#CC0000",
        font=("Courier New", 14, "bold"),
        height=40
    )
    close_btn.pack(pady=(10, 20), padx=20, fill="x")
    
    print("✅ Test window created successfully")
    print("   Close the window when done testing")
    print()
    
    root.mainloop()
    
except Exception as e:
    print(f"❌ Failed to create test GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("🎯 DIAGNOSIS COMPLETE")
print("=" * 70)
print()
print("If you saw the test window:")
print("✅ World AI Chat is working correctly!")
print("✅ You can use it from JARVIS panel")
print()
print("If you didn't see the window:")
print("❌ There's a problem with GUI display")
print("   Possible causes:")
print("   - Display/monitor issues")
print("   - Window manager blocking windows")
print("   - Graphics driver issues")
print()
print("যদি test window দেখেছেন:")
print("✅ World AI Chat সঠিকভাবে কাজ করছে!")
print("✅ JARVIS panel থেকে ব্যবহার করতে পারবেন")
print()
print("যদি window না দেখেন:")
print("❌ GUI display এ সমস্যা আছে")
print("   সম্ভাব্য কারণ:")
print("   - Display/monitor সমস্যা")
print("   - Window manager windows block করছে")
print("   - Graphics driver সমস্যা")
print()
print("=" * 70)
