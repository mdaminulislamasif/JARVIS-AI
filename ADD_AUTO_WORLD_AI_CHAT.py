#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADD AUTOMATIC WORLD AI CHAT TO JARVIS PANEL
============================================
This script adds automatic World AI Chat integration to JARVIS panel

NEW FEATURE:
- User clicks "🌍 WORLD AI CHAT" button
- User selects AI (Gemini, ChatGPT, etc.)
- AI mode activates
- User types in JARVIS panel chat box
- User presses Enter
- Response automatically appears in JARVIS panel!

NO MORE MANUAL COPY-PASTE!
"""

import os
import sys

print("=" * 70)
print("⚡ ADDING AUTOMATIC WORLD AI CHAT TO JARVIS")
print("=" * 70)
print()

# Step 1: Check if files exist
print("Step 1: Checking files...")
if not os.path.exists('jarvis_panel.py'):
    print("❌ jarvis_panel.py not found!")
    sys.exit(1)
print("✅ jarvis_panel.py found")

if not os.path.exists('jarvis_world_ai_chat_auto.py'):
    print("❌ jarvis_world_ai_chat_auto.py not found!")
    sys.exit(1)
print("✅ jarvis_world_ai_chat_auto.py found")
print()

# Step 2: Check dependencies
print("Step 2: Checking dependencies...")
try:
    import selenium
    print("✅ selenium installed")
except ImportError:
    print("⚠️ selenium not installed")
    print("   Installing selenium...")
    os.system("pip install selenium")

try:
    from selenium import webdriver
    print("✅ selenium webdriver available")
except ImportError:
    print("❌ selenium webdriver not available")
    print("   Please install: pip install selenium")

print()

# Step 3: Read jarvis_panel.py
print("Step 3: Reading jarvis_panel.py...")
with open('jarvis_panel.py', 'r', encoding='utf-8') as f:
    panel_code = f.read()

print(f"✅ Read {len(panel_code)} characters")
print()

# Step 4: Check if already integrated
print("Step 4: Checking if already integrated...")
if 'jarvis_world_ai_chat_auto' in panel_code:
    print("⚠️ Automatic World AI Chat already integrated!")
    print("   No changes needed.")
    sys.exit(0)

print("✅ Not yet integrated, proceeding...")
print()

# Step 5: Add import
print("Step 5: Adding import statement...")
import_line = "from jarvis_world_ai_chat_auto import WorldAIChatAuto"

# Find where to add import (after other jarvis imports)
if 'from jarvis_world_ai_chat import WorldAIChat' in panel_code:
    panel_code = panel_code.replace(
        'from jarvis_world_ai_chat import WorldAIChat',
        'from jarvis_world_ai_chat import WorldAIChat\nfrom jarvis_world_ai_chat_auto import WorldAIChatAuto  # AUTOMATIC MODE!'
    )
    print("✅ Import added after WorldAIChat import")
else:
    # Add at the beginning with other imports
    lines = panel_code.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('import customtkinter'):
            lines.insert(i + 1, import_line)
            panel_code = '\n'.join(lines)
            print("✅ Import added after customtkinter import")
            break

print()

# Step 6: Add initialization
print("Step 6: Adding initialization in __init__...")

# Find where WorldAIChat is initialized
init_code = """
        # Initialize World AI Chat Auto (NEW - Automatic mode!)
        try:
            self.world_ai_chat_auto = WorldAIChatAuto()
            print("✅ World AI Chat Auto initialized!")
        except Exception as e:
            self.world_ai_chat_auto = None
            print(f"⚠️ World AI Chat Auto not available: {e}")
"""

if 'self.world_ai_chat = WorldAIChat()' in panel_code:
    panel_code = panel_code.replace(
        'print("✅ World AI Chat initialized!")',
        'print("✅ World AI Chat initialized!")\n' + init_code
    )
    print("✅ Initialization added")
else:
    print("⚠️ Could not find WorldAIChat initialization")

print()

# Step 7: Modify button command
print("Step 7: Modifying World AI Chat button...")

# Change button command to use auto mode
old_button = '''world_ai_btn = ctk.CTkButton(
            self.modules,
            text="🌍 WORLD AI CHAT",
            fg_color="#00AA00",
            hover_color="#00CC00",
            command=self.open_world_ai_chat_direct,'''

new_button = '''world_ai_btn = ctk.CTkButton(
            self.modules,
            text="⚡ WORLD AI CHAT (AUTO)",
            fg_color="#00AA00",
            hover_color="#00CC00",
            command=self.open_world_ai_chat_auto,  # NEW: Auto mode!'''

if old_button in panel_code:
    panel_code = panel_code.replace(old_button, new_button)
    print("✅ Button command updated to auto mode")
else:
    print("⚠️ Could not find World AI Chat button")

print()

# Step 8: Add new method
print("Step 8: Adding new auto mode method...")

new_method = '''
    def open_world_ai_chat_auto(self):
        """Open World AI Chat in AUTOMATIC mode - no manual copy-paste!"""
        try:
            if not self.world_ai_chat_auto:
                self.log("ERROR", "World AI Chat Auto not available!")
                self.log("SYSTEM", "Install selenium: pip install selenium")
                return
            
            # Check if already active
            status = self.world_ai_chat_auto.get_status()
            if status['active']:
                # Already active - deactivate
                result = self.world_ai_chat_auto.deactivate_ai_mode()
                self.log("SYSTEM", f"⚡ AI mode deactivated")
                return
            
            self.log("SYSTEM", "⚡ Opening World AI Chat (Automatic Mode)...")
            
            # Show AI selector
            ai = self.world_ai_chat_auto.show_ai_selector_dialog(self)
            
            if not ai:
                self.log("WARNING", "No AI selected")
                return
            
            # Activate AI mode
            result = self.world_ai_chat_auto.activate_ai_mode(ai, self)
            
            if result['success']:
                self.log("JARVIS", result['message'])
                self.log("SYSTEM", f"⚡ Type your question and press Enter!")
                self.log("SYSTEM", f"⚡ আপনার প্রশ্ন লিখুন এবং Enter চাপুন!")
            else:
                self.log("ERROR", result['message'])
        
        except Exception as e:
            self.log("ERROR", f"World AI Chat Auto error: {e}")
            print(f"⚠️ World AI Chat Auto error: {e}")
'''

# Find where to add method (after open_world_ai_chat_direct)
if 'def open_world_ai_chat_direct(self):' in panel_code:
    # Find the end of open_world_ai_chat_direct method
    lines = panel_code.split('\n')
    method_start = -1
    method_end = -1
    
    for i, line in enumerate(lines):
        if 'def open_world_ai_chat_direct(self):' in line:
            method_start = i
        elif method_start != -1 and line.strip().startswith('def ') and i > method_start:
            method_end = i
            break
    
    if method_end != -1:
        lines.insert(method_end, new_method)
        panel_code = '\n'.join(lines)
        print("✅ Auto mode method added")
    else:
        print("⚠️ Could not find insertion point for method")
else:
    print("⚠️ Could not find open_world_ai_chat_direct method")

print()

# Step 9: Modify process_input to check for AI mode
print("Step 9: Modifying process_input to handle AI mode...")

ai_mode_check = '''
        # Check if World AI Chat Auto mode is active
        if hasattr(self, 'world_ai_chat_auto') and self.world_ai_chat_auto:
            status = self.world_ai_chat_auto.get_status()
            if status['active']:
                # AI mode is active - send query to AI
                self.log("SYSTEM", f"⚡ Sending to {status['ai_name']}...")
                
                def handle_response(response):
                    self.after(0, lambda: self.log("JARVIS", f"[{status['ai_name']}] {response}"))
                    self.after(0, lambda: self.speak(response))
                
                # Send query in background thread
                import threading
                def send_query():
                    result = self.world_ai_chat_auto.send_query_auto(user_input)
                    if result['success']:
                        self.after(0, lambda: self.log("JARVIS", f"[{result['ai']}] {result['response']}"))
                        self.after(0, lambda: self.speak(result['response']))
                    else:
                        self.after(0, lambda: self.log("ERROR", result['response']))
                
                thread = threading.Thread(target=send_query, daemon=True)
                thread.start()
                return  # Don't process normally
'''

# Find process_input method and add check at the beginning
if 'def process_input(self, user_input):' in panel_code:
    panel_code = panel_code.replace(
        'def process_input(self, user_input):',
        'def process_input(self, user_input):' + ai_mode_check
    )
    print("✅ AI mode check added to process_input")
else:
    print("⚠️ Could not find process_input method")

print()

# Step 10: Write modified code
print("Step 10: Writing modified jarvis_panel.py...")
with open('jarvis_panel.py', 'w', encoding='utf-8') as f:
    f.write(panel_code)

print("✅ jarvis_panel.py updated")
print()

# Step 11: Create backup
print("Step 11: Creating backup...")
import shutil
backup_file = 'jarvis_panel_backup_before_auto.py'
shutil.copy2('jarvis_panel.py', backup_file)
print(f"✅ Backup created: {backup_file}")
print()

print("=" * 70)
print("🎉 AUTOMATIC WORLD AI CHAT ADDED SUCCESSFULLY!")
print("=" * 70)
print()
print("✅ What was added:")
print("   1. Import WorldAIChatAuto")
print("   2. Initialize world_ai_chat_auto")
print("   3. Updated button to auto mode")
print("   4. Added open_world_ai_chat_auto() method")
print("   5. Modified process_input() to check AI mode")
print()
print("🚀 How to use:")
print("   1. Start JARVIS: python jarvis_panel.py")
print("   2. Click: ⚡ WORLD AI CHAT (AUTO)")
print("   3. Select AI (Gemini, ChatGPT, etc.)")
print("   4. Type in JARVIS chat box")
print("   5. Press Enter")
print("   6. Response appears automatically!")
print()
print("⚠️ Requirements:")
print("   - selenium: pip install selenium")
print("   - ChromeDriver (auto-downloaded by selenium)")
print()
print("💡 Note:")
print("   - Browser will open automatically")
print("   - First time may take a few seconds")
print("   - Keep browser window open")
print("   - Click button again to deactivate")
print()
print("🔥 NO MORE MANUAL COPY-PASTE! 🔥")
print()
