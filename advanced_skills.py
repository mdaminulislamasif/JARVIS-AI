import pyautogui
import socket
import os

class AdvancedSkills:
    def __init__(self, brain_module):
        self.brain = brain_module

    def take_screenshot(self):
        self.brain.speak("Taking screenshot...")
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        self.brain.speak("Screenshot saved as screenshot.png")

    def get_network_info(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.brain.speak(f"Hostname: {hostname}. IP Address: {ip_address}.")

    def write_and_execute_code(self, task):
        self.brain.speak(f"Generating code for: {task}")
        # Use brain to generate code logic would go here
        self.brain.speak("Code generation and execution requires advanced privileges.")
