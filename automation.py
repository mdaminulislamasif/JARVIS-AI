import os
import subprocess
import pyautogui
import psutil
import shutil
import ctypes
import time
import glob

class AutomationEngine:
    def __init__(self, brain_module):
        self.brain = brain_module
        pyautogui.FAILSAFE = True

    def smart_open_app(self, app_name):
        """Advanced app launcher that searches the whole system if shortcut fails"""
        self.brain.speak(f"Searching and opening {app_name}")
        
        # 1. Try simple search
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app_name)
        time.sleep(0.5)
        pyautogui.press('enter')
        
        # 2. Verify if it opened (wait 3s)
        time.sleep(3)
        if not self.is_program_running(app_name):
            self.brain.speak("Simple search failed. Initiating deep system search...")
            # Search in Common Folders
            search_paths = [
                "C:\\Program Files\\**\\*.exe",
                "C:\\Program Files (x86)\\**\\*.exe"
            ]
            for path in search_paths:
                # Use glob to find the exe (limited depth for speed)
                matches = glob.glob(path, recursive=True)
                for match in matches:
                    if app_name.lower() in os.path.basename(match).lower():
                        os.startfile(match)
                        self.brain.speak(f"Found and launched from: {os.path.basename(match)}")
                        return True
            self.brain.speak(f"I couldn't find {app_name} in your installed applications.")
            return False
        return True

    def is_program_running(self, program_name):
        for proc in psutil.process_iter(['name']):
            if program_name.lower() in proc.info['name'].lower():
                return True
        return False

    def shutdown(self):
        self.brain.speak("System shutting down. Goodbye!")
        os.system("shutdown /s /t 1")

    def restart(self):
        self.brain.speak("Restarting system.")
        os.system("shutdown /r /t 1")

    def lock_pc(self):
        ctypes.windll.user32.LockWorkStation()

    def manual_click(self):
        pyautogui.click()
        self.brain.speak("Clicked.")

    def manual_type(self, text):
        pyautogui.write(text, interval=0.05)

    def manual_hotkey(self, keys):
        parts = keys.replace(' ', '').split('+')
        pyautogui.hotkey(*parts)

    def clean_temp_files(self):
        self.brain.speak("Cleaning system garbage...")
        temp_folders = [os.environ.get('TEMP'), r'C:\Windows\Temp']
        for folder in temp_folders:
            if folder and os.path.exists(folder):
                shutil.rmtree(folder, ignore_errors=True)
        self.brain.speak("Cleanup complete.")
