
import pyautogui
import time
import os
import pyperclip
import pygetwindow as gw

def extreme_automation():
    print("Executing Extreme Automation...")
    
    # 1. Find and Focus Blender
    blender_windows = [w for w in gw.getWindowsWithTitle('Blender') if 'Blender' in w.title]
    if not blender_windows:
        print("Blender not found!")
        return
    
    blender_win = blender_windows[0]
    blender_win.restore()
    blender_win.activate()
    time.sleep(2)
    
    # 2. Go to Text Editor area
    # Use Search to find Run Script
    pyautogui.press('f3')
    time.sleep(1)
    pyautogui.write('Run Script')
    time.sleep(1)
    pyautogui.press('enter')
    
    print("Script triggered via Search Menu.")
    time.sleep(5)
    
    # 3. Export via Menu (The most reliable way)
    print("Attempting Export via Menu...")
    pyautogui.hotkey('f3')
    time.sleep(1)
    pyautogui.write('Export glTF 2.0')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    
    # Type the path
    target_path = r"c:\Users\PHP\Desktop\ai\jarvis_learned_files\jarvis_face.glb"
    pyautogui.write(target_path)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter') # Confirm overwrite
    
    print("Export sequence complete.")

if __name__ == "__main__":
    extreme_automation()
