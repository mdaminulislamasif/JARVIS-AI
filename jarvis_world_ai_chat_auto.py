#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS WORLD AI CHAT - AUTOMATIC VERSION
=========================================
Automatically chat with world AIs directly from JARVIS panel!

NEW FEATURES:
- Type in JARVIS panel
- Press Enter
- AI response appears automatically in JARVIS
- No manual copy-paste needed!

How it works:
1. User clicks "🌍 WORLD AI CHAT" button
2. User selects AI (Gemini, ChatGPT, etc.)
3. AI mode activates in JARVIS panel
4. User types in JARVIS chat box
5. User presses Enter
6. JARVIS automatically:
   - Opens AI website
   - Sends query
   - Gets response
   - Shows in panel
"""

import webbrowser
import pyperclip
import time
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading


class WorldAIChatAuto:
    """Automatic chat with world AIs - no manual copy-paste!"""
    
    def __init__(self):
        self.supported_ais = {
            'gemini': {
                'name': 'Google Gemini',
                'url': 'https://gemini.google.com/app',
                'icon': '🔷',
                'input_selector': 'textarea[aria-label="Enter a prompt here"]',
                'output_selector': '.model-response-text',
                'send_method': 'enter'  # or 'button'
            },
            'chatgpt': {
                'name': 'ChatGPT (OpenAI)',
                'url': 'https://chatgpt.com',
                'icon': '🤖',
                'input_selector': '#prompt-textarea',
                'output_selector': '.markdown',
                'send_method': 'enter'
            },
            'claude': {
                'name': 'Claude AI (Anthropic)',
                'url': 'https://claude.ai/new',
                'icon': '🧠',
                'input_selector': 'div[contenteditable="true"]',
                'output_selector': '.font-claude-message',
                'send_method': 'enter'
            },
            'copilot': {
                'name': 'Microsoft Copilot',
                'url': 'https://copilot.microsoft.com',
                'icon': '💬',
                'input_selector': 'textarea[aria-label="Ask me anything..."]',
                'output_selector': '.response-message',
                'send_method': 'button'
            },
            'perplexity': {
                'name': 'Perplexity AI',
                'url': 'https://www.perplexity.ai',
                'icon': '🔮',
                'input_selector': 'textarea[placeholder="Ask anything..."]',
                'output_selector': '.prose',
                'send_method': 'enter'
            },
            'meta': {
                'name': 'Meta AI (Llama)',
                'url': 'https://www.meta.ai',
                'icon': '🦙',
                'input_selector': 'textarea',
                'output_selector': '.message-content',
                'send_method': 'enter'
            },
            'huggingface': {
                'name': 'HuggingChat',
                'url': 'https://huggingface.co/chat',
                'icon': '🤗',
                'input_selector': 'textarea[placeholder="Ask anything"]',
                'output_selector': '.prose',
                'send_method': 'enter'
            },
            'you': {
                'name': 'You.com AI',
                'url': 'https://you.com',
                'icon': '🌟',
                'input_selector': 'textarea[name="query"]',
                'output_selector': '.answer',
                'send_method': 'enter'
            },
            'phind': {
                'name': 'Phind AI',
                'url': 'https://www.phind.com',
                'icon': '🔍',
                'input_selector': 'textarea',
                'output_selector': '.answer-content',
                'send_method': 'enter'
            },
            'poe': {
                'name': 'Poe (Multiple AIs)',
                'url': 'https://poe.com',
                'icon': '🎭',
                'input_selector': 'textarea[placeholder="Talk to"]',
                'output_selector': '.Message_botMessageBubble',
                'send_method': 'enter'
            },
        }
        
        self.active_ai = None
        self.active_mode = False
        self.driver = None
        self.last_query = ""
        self.last_response = ""
    
    def activate_ai_mode(self, ai_name, parent_window=None):
        """
        Activate AI mode - JARVIS panel will send queries to selected AI
        
        Args:
            ai_name: Which AI to use (gemini, chatgpt, etc.)
            parent_window: Parent window for dialogs
        
        Returns:
            dict: {'success': bool, 'message': str, 'ai': str}
        """
        if ai_name not in self.supported_ais:
            return {
                'success': False,
                'message': f"AI '{ai_name}' not supported",
                'ai': None
            }
        
        self.active_ai = ai_name
        self.active_mode = True
        ai_info = self.supported_ais[ai_name]
        
        # Initialize browser in background
        try:
            self._init_browser(ai_name)
            return {
                'success': True,
                'message': f"✅ {ai_info['name']} mode activated! Type in JARVIS panel and press Enter.",
                'ai': ai_name
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Failed to activate {ai_info['name']}: {str(e)}",
                'ai': None
            }
    
    def deactivate_ai_mode(self):
        """Deactivate AI mode and close browser"""
        self.active_mode = False
        self.active_ai = None
        
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:

                print(f"⚠️ Error: {e}")
                pass
            self.driver = None
        
        return {
            'success': True,
            'message': "✅ AI mode deactivated"
        }
    
    def _init_browser(self, ai_name):
        """Initialize browser with AI website"""
        ai_info = self.supported_ais[ai_name]
        
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Open AI website
        self.driver.get(ai_info['url'])
        
        # Wait for page to load
        time.sleep(3)
    
    def send_query_auto(self, query, callback=None):
        """
        Automatically send query to AI and get response
        
        Args:
            query: User's question
            callback: Function to call with response (for async)
        
        Returns:
            dict: {'success': bool, 'response': str, 'ai': str}
        """
        if not self.active_mode or not self.active_ai:
            return {
                'success': False,
                'response': 'AI mode not activated. Click "🌍 WORLD AI CHAT" first.',
                'ai': None
            }
        
        if not self.driver:
            return {
                'success': False,
                'response': 'Browser not initialized. Please restart AI mode.',
                'ai': self.active_ai
            }
        
        ai_info = self.supported_ais[self.active_ai]
        self.last_query = query
        
        try:
            # Find input field
            wait = WebDriverWait(self.driver, 10)
            input_field = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ai_info['input_selector']))
            )
            
            # Clear and type query
            input_field.clear()
            input_field.send_keys(query)
            
            # Send query
            if ai_info['send_method'] == 'enter':
                input_field.send_keys(Keys.RETURN)
            else:
                # Find and click send button
                send_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                send_button.click()
            
            # Wait for response
            time.sleep(2)  # Initial wait
            
            # Get response (with retry)
            response_text = self._get_response_with_retry(ai_info['output_selector'])
            
            if response_text:
                self.last_response = response_text
                
                if callback:
                    callback(response_text)
                
                return {
                    'success': True,
                    'response': response_text,
                    'ai': self.active_ai
                }
            else:
                return {
                    'success': False,
                    'response': '⚠️ Could not get AI response. Please check browser window.',
                    'ai': self.active_ai
                }
        
        except Exception as e:
            return {
                'success': False,
                'response': f'❌ Error: {str(e)}',
                'ai': self.active_ai
            }
    
    def _get_response_with_retry(self, selector, max_retries=10, wait_time=2):
        """Get AI response with retry logic"""
        for i in range(max_retries):
            try:
                # Find all response elements
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    # Get last response (most recent)
                    last_element = elements[-1]
                    text = last_element.text.strip()
                    
                    if text and len(text) > 10:  # Valid response
                        return text
                
                # Wait and retry
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"Retry {i+1}/{max_retries}: {e}")
                time.sleep(wait_time)
        
        return None
    
    def show_ai_selector_dialog(self, parent_window=None):
        """Show dialog to select which AI to use (same as before)"""
        
        if parent_window:
            dialog = ctk.CTkToplevel(parent_window)
        else:
            dialog = ctk.CTk()
        
        dialog.title("Select AI for Auto Mode")
        dialog.geometry("550x750")
        dialog.configure(fg_color="#02050A")
        
        # Make it VERY visible
        dialog.attributes("-topmost", True)
        dialog.lift()
        dialog.focus_force()
        dialog.grab_set()
        
        # Center the window
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header = ctk.CTkFrame(dialog, fg_color="#FF3131", height=140)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header,
            text="🌍 WORLD AI CHAT",
            font=("Courier New", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            header,
            text="⚡ AUTOMATIC MODE ⚡",
            font=("Courier New", 18, "bold"),
            text_color="#00FF00"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            header,
            text="Type in JARVIS → Press Enter → Get Response!",
            font=("Courier New", 12),
            text_color="#FFFF00"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            header,
            text="JARVIS এ লিখুন → Enter চাপুন → Response পাবেন!",
            font=("Courier New", 11),
            text_color="#FFFF00"
        ).pack(pady=(0, 20))
        
        # Scrollable frame for AI buttons
        ai_frame = ctk.CTkScrollableFrame(
            dialog,
            fg_color="transparent",
            height=400
        )
        ai_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # AI buttons
        selected_ai = {'name': None}
        
        colors = [
            ("#003355", "#0055AA"),  # Blue
            ("#335500", "#55AA00"),  # Green
            ("#553300", "#AA5500"),  # Orange
            ("#330055", "#5500AA"),  # Purple
            ("#005533", "#00AA55"),  # Teal
        ]
        
        for idx, (ai_key, ai_info) in enumerate(self.supported_ais.items()):
            def make_callback(key):
                def callback():
                    selected_ai.update({'name': key})
                    dialog.grab_release()
                    dialog.destroy()
                return callback
            
            color_idx = idx % len(colors)
            fg_color, hover_color = colors[color_idx]
            
            btn = ctk.CTkButton(
                ai_frame,
                text=f"{ai_info['icon']} {ai_info['name']} ⚡",
                command=make_callback(ai_key),
                fg_color=fg_color,
                hover_color=hover_color,
                font=("Courier New", 16, "bold"),
                height=70,
                border_width=2,
                border_color=hover_color
            )
            btn.pack(fill="x", pady=10)
        
        # Info label
        info_label = ctk.CTkLabel(
            dialog,
            text="💡 Select AI for automatic mode\n⚡ No manual copy-paste needed!",
            font=("Courier New", 11),
            text_color="#00FF00",
            justify="center"
        )
        info_label.pack(pady=(0, 10))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            dialog,
            text="❌ CANCEL (বাতিল)",
            command=lambda: (selected_ai.update({'name': None}), dialog.grab_release(), dialog.destroy()),
            fg_color="#660000",
            hover_color="#AA0000",
            font=("Courier New", 16, "bold"),
            height=50,
            border_width=2,
            border_color="#AA0000"
        )
        cancel_btn.pack(fill="x", padx=40, pady=(0, 20))
        
        dialog.wait_window()
        
        return selected_ai['name']
    
    def get_status(self):
        """Get current status"""
        if self.active_mode and self.active_ai:
            ai_info = self.supported_ais[self.active_ai]
            return {
                'active': True,
                'ai': self.active_ai,
                'ai_name': ai_info['name'],
                'icon': ai_info['icon'],
                'message': f"⚡ {ai_info['icon']} {ai_info['name']} mode active"
            }
        else:
            return {
                'active': False,
                'ai': None,
                'ai_name': None,
                'icon': None,
                'message': "AI mode not active"
            }


# Test function
if __name__ == "__main__":
    print("=" * 70)
    print("🌍 WORLD AI CHAT - AUTOMATIC MODE TEST")
    print("=" * 70)
    print()
    
    world_ai = WorldAIChatAuto()
    
    print("Available AIs:")
    for ai_key, ai_info in world_ai.supported_ais.items():
        print(f"  {ai_info['icon']} {ai_info['name']}")
    
    print()
    print("⚠️ This is automatic mode - requires Selenium and ChromeDriver")
    print("⚠️ Install: pip install selenium")
    print()
    print("To use:")
    print("1. Select AI from JARVIS panel")
    print("2. Type in JARVIS chat box")
    print("3. Press Enter")
    print("4. Response appears automatically!")
    print()
