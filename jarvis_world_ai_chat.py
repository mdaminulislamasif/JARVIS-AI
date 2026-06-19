"""
JARVIS WORLD AI CHAT
When API keys don't work, chat with world AIs (Gemini, ChatGPT, Claude, etc.)

Features:
- Opens AI website in browser
- Copies user query to clipboard
- User pastes and gets AI response
- Copies AI response back
- JARVIS learns from response
- Shows output to user
"""

import webbrowser
import pyperclip
import time
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk


class WorldAIChat:
    """Chat with world AIs when API keys don't work"""
    
    def __init__(self):
        self.supported_ais = {
            'gemini': {
                'name': 'Google Gemini',
                'url': 'https://gemini.google.com/app',
                'icon': '🔷'
            },
            'chatgpt': {
                'name': 'ChatGPT (OpenAI)',
                'url': 'https://chatgpt.com',
                'icon': '🤖'
            },
            'claude': {
                'name': 'Claude AI (Anthropic)',
                'url': 'https://claude.ai/new',
                'icon': '🧠'
            },
            'copilot': {
                'name': 'Microsoft Copilot',
                'url': 'https://copilot.microsoft.com',
                'icon': '💬'
            },
            'perplexity': {
                'name': 'Perplexity AI',
                'url': 'https://www.perplexity.ai',
                'icon': '🔮'
            },
            'meta': {
                'name': 'Meta AI (Llama)',
                'url': 'https://www.meta.ai',
                'icon': '🦙'
            },
            'huggingface': {
                'name': 'HuggingChat',
                'url': 'https://huggingface.co/chat',
                'icon': '🤗'
            },
            'you': {
                'name': 'You.com AI',
                'url': 'https://you.com',
                'icon': '🌟'
            },
            'phind': {
                'name': 'Phind AI',
                'url': 'https://www.phind.com',
                'icon': '🔍'
            },
            'poe': {
                'name': 'Poe (Multiple AIs)',
                'url': 'https://poe.com',
                'icon': '🎭'
            },
        }
        
        self.last_query = ""
        self.last_response = ""
    
    def chat_with_ai(self, query, ai_name='gemini', parent_window=None):
        """
        Chat with a world AI
        
        Args:
            query: User's question
            ai_name: Which AI to use (gemini, chatgpt, claude, etc.)
            parent_window: Parent tkinter window for dialog
        
        Returns:
            dict: {'success': bool, 'response': str, 'ai': str}
        """
        if ai_name not in self.supported_ais:
            return {
                'success': False,
                'response': f"AI '{ai_name}' not supported. Available: {', '.join(self.supported_ais.keys())}",
                'ai': None
            }
        
        ai_info = self.supported_ais[ai_name]
        self.last_query = query
        
        # Step 1: Copy query to clipboard
        pyperclip.copy(query)
        
        # Step 2: Open AI website
        webbrowser.open(ai_info['url'])
        
        # Step 3: Show instruction dialog
        result = self._show_instruction_dialog(query, ai_info, parent_window)
        
        if result['success']:
            self.last_response = result['response']
            return result
        else:
            return {
                'success': False,
                'response': 'User cancelled or no response provided',
                'ai': ai_name
            }
    
    def _show_instruction_dialog(self, query, ai_info, parent_window):
        """Show dialog with instructions for user"""
        
        # Create dialog window
        if parent_window:
            dialog = ctk.CTkToplevel(parent_window)
        else:
            dialog = ctk.CTk()
        
        dialog.title(f"Chat with {ai_info['name']}")
        dialog.geometry("650x550")
        dialog.configure(fg_color="#02050A")
        
        # Make it VERY visible - always on top and grab focus
        dialog.attributes("-topmost", True)
        dialog.lift()
        dialog.focus_force()
        # dialog.grab_set()  # REMOVED TO PREVENT PANEL FREEZING
        
        # Center the window on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header with animation
        header = ctk.CTkFrame(dialog, fg_color="#FF3131", height=100)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header,
            text=f"🌍 WORLD AI CHAT",
            font=("Courier New", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            header,
            text=f"{ai_info['icon']} {ai_info['name']}",
            font=("Courier New", 20, "bold"),
            text_color="#FFFF00"
        ).pack(pady=(0, 15))
        
        # Instructions with better formatting
        instructions_frame = ctk.CTkFrame(dialog, fg_color="#05080F", border_width=2, border_color="#00FF41")
        instructions_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        instructions = f"""
🎯 SIMPLE STEPS (সহজ ধাপ):

✅ STEP 1: Browser এ {ai_info['name']} খুলেছে
✅ STEP 2: আপনার প্রশ্ন clipboard এ আছে

📝 STEP 3: {ai_info['name']} এ paste করুন (Ctrl+V)
⏳ STEP 4: AI response এর জন্য wait করুন
📋 STEP 5: Response copy করুন (Ctrl+C)
✅ STEP 6: নিচের box এ paste করুন এবং SUBMIT click করুন

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Your Question:
{query[:200]}{"..." if len(query) > 200 else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIP: Question already copied! Just paste in {ai_info['name']}!
        """
        
        instructions_label = ctk.CTkLabel(
            instructions_frame,
            text=instructions.strip(),
            font=("Courier New", 11),
            text_color="#00FF41",
            justify="left"
        )
        instructions_label.pack(padx=20, pady=20, anchor="w")
        
        # Response input with better label
        response_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        response_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        response_label = ctk.CTkLabel(
            response_frame,
            text="📋 PASTE AI RESPONSE HERE (AI এর response এখানে paste করুন):",
            font=("Courier New", 13, "bold"),
            text_color="#FFD700"
        )
        response_label.pack(anchor="w", pady=(0, 5))
        
        response_text = ctk.CTkTextbox(
            dialog,
            height=120,
            font=("Courier New", 12),
            fg_color="#001100",
            text_color="#00FF41",
            border_width=2,
            border_color="#00FF41"
        )
        response_text.pack(fill="x", padx=20, pady=(0, 15))
        response_text.focus_set()  # Focus on text box
        
        # Result storage
        result = {'success': False, 'response': '', 'ai': ai_info['name']}
        
        def on_submit():
            response = response_text.get("1.0", "end-1c").strip()
            if response and len(response) > 10:  # At least 10 characters
                result['success'] = True
                result['response'] = response
                dialog.grab_release()
                dialog.destroy()
            else:
                # Show warning with sound
                dialog.bell()
                messagebox.showwarning(
                    "Empty Response", 
                    "⚠️ Please paste the AI response first!\n\nআগে AI এর response paste করুন!",
                    parent=dialog
                )
                response_text.focus_set()
        
        def on_cancel():
            result['success'] = False
            dialog.grab_release()
            dialog.destroy()
        
        # Buttons with better styling
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        submit_btn = ctk.CTkButton(
            button_frame,
            text="✅ SUBMIT (জমা দিন)",
            command=on_submit,
            fg_color="#00AA00",
            hover_color="#00FF00",
            font=("Courier New", 16, "bold"),
            height=50,
            border_width=2,
            border_color="#00FF00"
        )
        submit_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ CANCEL (বাতিল)",
            command=on_cancel,
            fg_color="#AA0000",
            hover_color="#FF0000",
            font=("Courier New", 16, "bold"),
            height=50,
            border_width=2,
            border_color="#FF0000"
        )
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(10, 0))
        
        # Bind Enter key to submit
        response_text.bind("<Control-Return>", lambda e: on_submit())
        
        # Flash window to get attention
        try:
            dialog.attributes('-alpha', 0.0)
            dialog.after(50, lambda: dialog.attributes('-alpha', 1.0))
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result
    
    def learn_from_response(self, query, response, learning_systems=None):
        """
        Learn from AI response using available learning systems
        
        Args:
            query: Original question
            response: AI's response
            learning_systems: Dict of available learning systems
                {
                    'auto_learner': AutoLearner instance,
                    'tree_learner': TreeLearner instance,
                    'ultimate_learner': UltimateLearner instance,
                }
        
        Returns:
            dict: Learning results
        """
        results = {
            'success': True,
            'learned_from': [],
            'errors': []
        }
        
        if not learning_systems:
            results['success'] = False
            results['errors'].append("No learning systems provided")
            return results
        
        # Try each learning system
        for system_name, system in learning_systems.items():
            try:
                if system_name == 'auto_learner' and hasattr(system, 'learn_text'):
                    system.learn_text(response)
                    results['learned_from'].append(system_name)
                
                elif system_name == 'tree_learner' and hasattr(system, 'learn'):
                    system.learn(query, response)
                    results['learned_from'].append(system_name)
                
                elif system_name == 'ultimate_learner' and hasattr(system, 'learn'):
                    system.learn(response)
                    results['learned_from'].append(system_name)
                
            except Exception as e:
                results['errors'].append(f"{system_name}: {str(e)}")
        
        return results
    
    def show_ai_selector_dialog(self, parent_window=None):
        """Show dialog to select which AI to use"""
        
        if parent_window:
            dialog = ctk.CTkToplevel(parent_window)
        else:
            dialog = ctk.CTk()
        
        dialog.title("Select AI")
        dialog.geometry("550x700")
        dialog.configure(fg_color="#02050A")
        
        # Make it VERY visible
        dialog.attributes("-topmost", True)
        dialog.lift()
        dialog.focus_force()
        # dialog.grab_set()  # REMOVED TO PREVENT PANEL FREEZING
        
        # Center the window
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header with better styling
        header = ctk.CTkFrame(dialog, fg_color="#FF3131", height=120)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            header,
            text="🌍 SELECT WORLD AI",
            font=("Courier New", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            header,
            text="Choose which AI to chat with:",
            font=("Courier New", 14),
            text_color="#FFFF00"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            header,
            text="কোন AI এর সাথে chat করবেন select করুন:",
            font=("Courier New", 12),
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
                text=f"{ai_info['icon']} {ai_info['name']}",
                command=make_callback(ai_key),
                fg_color=fg_color,
                hover_color=hover_color,
                font=("Courier New", 18, "bold"),
                height=70,
                border_width=2,
                border_color=hover_color
            )
            btn.pack(fill="x", pady=10)
        
        # Info label
        info_label = ctk.CTkLabel(
            dialog,
            text="💡 Click any AI to open it in browser",
            font=("Courier New", 11),
            text_color="#888888"
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
        
        # Flash window to get attention
        try:
            dialog.attributes('-alpha', 0.0)
            dialog.after(50, lambda: dialog.attributes('-alpha', 1.0))
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
        
        dialog.wait_window()
        
        return selected_ai['name']


# Test function
if __name__ == "__main__":
    world_ai = WorldAIChat()
    
    # Test with a simple query
    result = world_ai.chat_with_ai("What is Python programming?", ai_name='gemini')
    
    if result['success']:
        print(f"✅ Success!")
        print(f"AI: {result['ai']}")
        print(f"Response: {result['response'][:200]}...")
    else:
        print(f"❌ Failed: {result['response']}")
