"""
JARVIS - WORKING VERSION
Real AI Assistant that Actually Works!

This version can:
- Execute real commands
- Open applications
- Manage files
- Search the web
- And much more!
"""

import os
import sys
import subprocess
import webbrowser
import sqlite3
import json
from datetime import datetime
import platform

class WorkingJARVIS:
    """JARVIS that actually works!"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.system = platform.system()
        print(f"✅ JARVIS initialized on {self.system}")
    
    def speak(self, text):
        """Speak text (print for now, can add TTS later)"""
        print(f"\n🤖 JARVIS: {text}")
    
    def execute_command(self, user_input):
        """Execute actual commands based on user input"""
        user_input = user_input.lower().strip()
        
        # ===== WEB BROWSER =====
        if any(word in user_input for word in ['open chrome', 'open browser', 'browse', 'google']):
            if 'youtube' in user_input:
                self.speak("Opening YouTube...")
                webbrowser.open('https://www.youtube.com')
            elif 'facebook' in user_input:
                self.speak("Opening Facebook...")
                webbrowser.open('https://www.facebook.com')
            elif 'gmail' in user_input or 'email' in user_input:
                self.speak("Opening Gmail...")
                webbrowser.open('https://mail.google.com')
            else:
                self.speak("Opening web browser...")
                webbrowser.open('https://www.google.com')
            return True
        
        # ===== SEARCH =====
        if 'search' in user_input or 'find' in user_input or 'khoj' in user_input:
            # Extract search query
            query = user_input.replace('search', '').replace('find', '').replace('khoj', '').strip()
            if query:
                self.speak(f"Searching for: {query}")
                webbrowser.open(f'https://www.google.com/search?q={query}')
            else:
                self.speak("What would you like to search for?")
            return True
        
        # ===== OPEN APPLICATIONS =====
        if 'open' in user_input:
            if 'notepad' in user_input:
                self.speak("Opening Notepad...")
                if self.system == 'Windows':
                    subprocess.Popen(['notepad.exe'])
                return True
            
            elif 'calculator' in user_input or 'calc' in user_input:
                self.speak("Opening Calculator...")
                if self.system == 'Windows':
                    subprocess.Popen(['calc.exe'])
                return True
            
            elif 'paint' in user_input:
                self.speak("Opening Paint...")
                if self.system == 'Windows':
                    subprocess.Popen(['mspaint.exe'])
                return True
            
            elif 'cmd' in user_input or 'command prompt' in user_input:
                self.speak("Opening Command Prompt...")
                if self.system == 'Windows':
                    subprocess.Popen(['cmd.exe'])
                return True
            
            elif 'powershell' in user_input:
                self.speak("Opening PowerShell...")
                if self.system == 'Windows':
                    subprocess.Popen(['powershell.exe'])
                return True
            
            elif 'explorer' in user_input or 'file explorer' in user_input:
                self.speak("Opening File Explorer...")
                if self.system == 'Windows':
                    subprocess.Popen(['explorer.exe'])
                return True
        
        # ===== FILE OPERATIONS =====
        if 'create file' in user_input or 'make file' in user_input:
            self.speak("Creating a new file...")
            filename = 'jarvis_test_file.txt'
            with open(filename, 'w') as f:
                f.write('This file was created by JARVIS!\n')
                f.write(f'Created at: {datetime.now()}\n')
            self.speak(f"File created: {filename}")
            return True
        
        if 'create folder' in user_input or 'make folder' in user_input:
            self.speak("Creating a new folder...")
            foldername = 'JARVIS_Folder'
            os.makedirs(foldername, exist_ok=True)
            self.speak(f"Folder created: {foldername}")
            return True
        
        if 'list files' in user_input or 'show files' in user_input:
            self.speak("Listing files in current directory...")
            files = os.listdir('.')
            print("\nFiles:")
            for i, file in enumerate(files[:20], 1):  # Show first 20
                print(f"  {i}. {file}")
            return True
        
        # ===== SYSTEM INFO =====
        if 'system info' in user_input or 'computer info' in user_input:
            self.speak("Getting system information...")
            print(f"\n  System: {platform.system()}")
            print(f"  Release: {platform.release()}")
            print(f"  Version: {platform.version()}")
            print(f"  Machine: {platform.machine()}")
            print(f"  Processor: {platform.processor()}")
            return True
        
        # ===== TIME & DATE =====
        if 'time' in user_input or 'date' in user_input:
            now = datetime.now()
            if 'time' in user_input:
                self.speak(f"Current time is {now.strftime('%I:%M %p')}")
            if 'date' in user_input:
                self.speak(f"Today's date is {now.strftime('%B %d, %Y')}")
            return True
        
        # ===== CALCULATIONS =====
        if 'calculate' in user_input or 'math' in user_input or '+' in user_input or '-' in user_input:
            try:
                # Extract numbers and operation
                import re
                numbers = re.findall(r'\d+', user_input)
                if len(numbers) >= 2:
                    a, b = int(numbers[0]), int(numbers[1])
                    if '+' in user_input or 'plus' in user_input or 'add' in user_input:
                        result = a + b
                        self.speak(f"{a} + {b} = {result}")
                    elif '-' in user_input or 'minus' in user_input or 'subtract' in user_input:
                        result = a - b
                        self.speak(f"{a} - {b} = {result}")
                    elif '*' in user_input or 'multiply' in user_input or 'times' in user_input:
                        result = a * b
                        self.speak(f"{a} × {b} = {result}")
                    elif '/' in user_input or 'divide' in user_input:
                        result = a / b
                        self.speak(f"{a} ÷ {b} = {result}")
                    return True
            except Exception as e:

                print(f"⚠️ Error: {e}")
                pass
        
        # ===== HELP =====
        if 'help' in user_input or 'what can you do' in user_input:
            self.speak("Here's what I can do:")
            print("\n  🌐 Web & Search:")
            print("    - 'open chrome' / 'open browser'")
            print("    - 'open youtube' / 'open facebook' / 'open gmail'")
            print("    - 'search [query]' / 'find [query]'")
            print("\n  📱 Applications:")
            print("    - 'open notepad' / 'open calculator' / 'open paint'")
            print("    - 'open cmd' / 'open powershell' / 'open explorer'")
            print("\n  📁 Files & Folders:")
            print("    - 'create file' / 'create folder'")
            print("    - 'list files' / 'show files'")
            print("\n  💻 System:")
            print("    - 'system info' / 'computer info'")
            print("    - 'time' / 'date'")
            print("\n  🔢 Math:")
            print("    - 'calculate 5 + 3' / '10 - 2' / '4 * 5' / '20 / 4'")
            print("\n  ℹ️ Other:")
            print("    - 'help' - Show this help")
            print("    - 'exit' / 'quit' - Exit JARVIS")
            return True
        
        # ===== EXIT =====
        if user_input in ['exit', 'quit', 'bye', 'goodbye']:
            self.speak("Goodbye! Have a great day!")
            return 'exit'
        
        # ===== DEFAULT =====
        self.speak(f"I heard: '{user_input}'")
        self.speak("I'm still learning this command. Try 'help' to see what I can do!")
        return False
    
    def run(self):
        """Run JARVIS in interactive mode"""
        print("\n" + "=" * 80)
        print("  🤖 JARVIS - WORKING VERSION")
        print("  🤖 JARVIS - কার্যকর সংস্করণ")
        print("=" * 80)
        print("\n  I'm ready to help! Try these commands:")
        print("  - 'open chrome' - Open web browser")
        print("  - 'search Python' - Search on Google")
        print("  - 'open notepad' - Open Notepad")
        print("  - 'create file' - Create a test file")
        print("  - 'help' - See all commands")
        print("  - 'exit' - Exit JARVIS")
        print("\n" + "=" * 80)
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                result = self.execute_command(user_input)
                
                if result == 'exit':
                    break
                
            except KeyboardInterrupt:
                print("\n\n🤖 JARVIS: Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                self.speak("Sorry, something went wrong. Please try again.")


def main():
    """Main function"""
    jarvis = WorkingJARVIS()
    
    # Check if command provided as argument
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        jarvis.execute_command(command)
    else:
        jarvis.run()


if __name__ == "__main__":
    main()
