"""
NEW METHODS FOR JARVIS PANEL
=============================
Add these methods to JarvisAntigravity class in jarvis_panel.py

Copy and paste these methods into the class.
"""

# ============================================================================
# WORLD AI CHAT METHODS
# ============================================================================

def open_world_ai_chat_direct(self):
    """Open World AI Chat directly"""
    try:
        if not self.world_ai_chat:
            self.log("ERROR", "World AI Chat not available!")
            return
        
        self.log("SYSTEM", "🌍 Opening World AI Chat...")
        
        # Show AI selector
        ai = self.world_ai_chat.show_ai_selector_dialog(self)
        
        if not ai:
            self.log("WARNING", "No AI selected")
            return
        
        # Get query from user
        query = self._get_query_dialog()
        
        if not query:
            self.log("WARNING", "No query provided")
            return
        
        # Chat with AI
        result = self.world_ai_chat.chat_with_ai(query, ai, self)
        
        if result['success']:
            self.log("JARVIS", f"[{result['ai']}] {result['response']}")
            self.speak(result['response'])
        else:
            self.log("WARNING", "World AI Chat cancelled or failed")
    
    except Exception as e:
        self.log("ERROR", f"World AI Chat error: {e}")
        print(f"⚠️ World AI Chat error: {e}")

def _get_query_dialog(self):
    """Show dialog to get query from user"""
    import customtkinter as ctk
    from tkinter import messagebox
    
    dialog = ctk.CTkToplevel(self)
    dialog.title("Enter Query")
    dialog.geometry("500x300")
    dialog.configure(fg_color="#02050A")
    dialog.attributes("-topmost", True)
    dialog.grab_set()
    
    # Center dialog
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Header
    ctk.CTkLabel(
        dialog,
        text="📝 Enter Your Question",
        font=("Courier New", 20, "bold"),
        text_color="#00F3FF"
    ).pack(pady=20)
    
    # Text box
    text_box = ctk.CTkTextbox(
        dialog,
        height=100,
        font=("Courier New", 12),
        fg_color="#05080F",
        text_color="#00FF41"
    )
    text_box.pack(fill="both", expand=True, padx=20, pady=10)
    text_box.focus_set()
    
    result = {'query': None}
    
    def on_submit():
        query = text_box.get("1.0", "end-1c").strip()
        if query:
            result['query'] = query
            dialog.grab_release()
            dialog.destroy()
        else:
            messagebox.showwarning("Empty Query", "Please enter a question!")
    
    def on_cancel():
        dialog.grab_release()
        dialog.destroy()
    
    # Buttons
    btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    btn_frame.pack(fill="x", padx=20, pady=20)
    
    ctk.CTkButton(
        btn_frame,
        text="✅ SUBMIT",
        command=on_submit,
        fg_color="#00AA00",
        hover_color="#00CC00",
        font=("Courier New", 14, "bold"),
        height=45
    ).pack(side="left", expand=True, fill="x", padx=(0, 10))
    
    ctk.CTkButton(
        btn_frame,
        text="❌ CANCEL",
        command=on_cancel,
        fg_color="#AA0000",
        hover_color="#CC0000",
        font=("Courier New", 14, "bold"),
        height=45
    ).pack(side="left", expand=True, fill="x", padx=(10, 0))
    
    dialog.wait_window()
    return result['query']


# ============================================================================
# AUTO AI LEARNER METHODS
# ============================================================================

def toggle_auto_learner(self):
    """Toggle auto AI learner ON/OFF"""
    try:
        # Initialize auto learner if not exists
        if not hasattr(self, 'auto_learner'):
            from jarvis_auto_ai_learner import AutoAILearner
            self.auto_learner = AutoAILearner(self)
            self.log("SYSTEM", "🤖 Auto AI Learner initialized!")
        
        # Toggle state
        if self.auto_learner.is_running:
            # Stop learning
            self.auto_learner.stop()
            self.auto_learn_btn.configure(
                text="🤖 AUTO LEARN: OFF",
                fg_color="#AA0000",
                hover_color="#CC0000"
            )
            self.log("SYSTEM", "🤖 Auto AI Learner stopped")
            self._update_learning_stats()
        else:
            # Start learning
            self.auto_learner.start()
            self.auto_learn_btn.configure(
                text="🤖 AUTO LEARN: ON",
                fg_color="#00AA00",
                hover_color="#00CC00"
            )
            self.log("SYSTEM", "🤖 Auto AI Learner started!")
            self._start_learning_stats_update()
    
    except Exception as e:
        self.log("ERROR", f"Auto learner error: {e}")
        print(f"⚠️ Auto learner error: {e}")

def _update_learning_stats(self):
    """Update learning statistics display"""
    try:
        if hasattr(self, 'auto_learner'):
            stats = self.auto_learner.get_stats()
            status = "Learning..." if stats['is_running'] else "Idle"
            self.learning_stats.configure(
                text=f"📊 Learned: {stats['learned_count']} topics | Status: {status}"
            )
    except Exception as e:
        print(f"⚠️ Stats update error: {e}")

def _start_learning_stats_update(self):
    """Start periodic stats update"""
    def update_loop():
        if hasattr(self, 'auto_learner') and self.auto_learner.is_running:
            self._update_learning_stats()
            self.after(5000, update_loop)  # Update every 5 seconds
    
    update_loop()

def open_learning_settings(self):
    """Open learning settings dialog"""
    try:
        self.log("SYSTEM", "⚙️ Opening learning settings...")
        # TODO: Implement settings dialog
        from tkinter import messagebox
        messagebox.showinfo(
            "Learning Settings",
            "Learning Settings:\n\n"
            "• Auto-learning interval: 30-60 seconds\n"
            "• Topics: 60+ categories\n"
            "• Learning method: Direct AI Chat\n"
            "• Storage: Offline Brain knowledge base\n\n"
            "More settings coming soon!"
        )
    except Exception as e:
        self.log("ERROR", f"Settings error: {e}")


# ============================================================================
# MICROPHONE CONTROL METHODS
# ============================================================================

def toggle_microphone(self):
    """Toggle microphone ON/OFF"""
    try:
        self.mic_enabled = not self.mic_enabled
        
        if self.mic_enabled:
            self.mic_button.configure(
                text="🎤 MIC: ON",
                fg_color="#00AA00",
                hover_color="#00CC00"
            )
            self.log("SYSTEM", "🎤 Microphone enabled")
        else:
            self.mic_button.configure(
                text="🎤 MIC: OFF",
                fg_color="#AA0000",
                hover_color="#CC0000"
            )
            self.log("SYSTEM", "🎤 Microphone disabled")
    
    except Exception as e:
        self.log("ERROR", f"Microphone toggle error: {e}")
        print(f"⚠️ Microphone error: {e}")


# ============================================================================
# SYSTEM PERMISSIONS METHODS
# ============================================================================

def request_permissions(self):
    """Request all system permissions"""
    try:
        self.log("SYSTEM", "🔐 Requesting permissions...")
        
        permissions = {
            'Microphone': self._request_mic_permission(),
            'File System': self._request_file_permission(),
            'Network': self._request_network_permission(),
        }
        
        granted = sum(permissions.values())
        total = len(permissions)
        
        # Show results
        result_text = "Permission Results:\n\n"
        for perm, status in permissions.items():
            icon = "✅" if status else "❌"
            result_text += f"{icon} {perm}: {'Granted' if status else 'Denied'}\n"
        
        result_text += f"\n📊 Total: {granted}/{total} granted"
        
        from tkinter import messagebox
        messagebox.showinfo("Permissions", result_text)
        
        self.log("SYSTEM", f"🔐 Permissions: {granted}/{total} granted")
    
    except Exception as e:
        self.log("ERROR", f"Permission request error: {e}")
        print(f"⚠️ Permission error: {e}")

def _request_mic_permission(self):
    """Request microphone permission"""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.1)
        return True
    except Exception as e:

        print(f"⚠️ Error: {e}")
        return False

def _request_file_permission(self):
    """Request file system permission"""
    try:
        import os
        import tempfile
        # Try to create a temp file
        fd, path = tempfile.mkstemp()
        os.close(fd)
        os.remove(path)
        return True
    except Exception as e:

        print(f"⚠️ Error: {e}")
        return False

def _request_network_permission(self):
    """Request network permission"""
    try:
        import socket
        # Try to create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.close()
        return True
    except Exception as e:

        print(f"⚠️ Error: {e}")
        return False

def open_system_settings(self):
    """Open system settings dialog"""
    try:
        self.log("SYSTEM", "⚙️ Opening system settings...")
        # TODO: Implement settings dialog
        from tkinter import messagebox
        messagebox.showinfo(
            "System Settings",
            "System Settings:\n\n"
            "• Microphone: Enabled\n"
            "• Voice: Enabled\n"
            "• Auto-learning: Configurable\n"
            "• Permissions: Manageable\n\n"
            "More settings coming soon!"
        )
    except Exception as e:
        self.log("ERROR", f"Settings error: {e}")


# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

"""
TO ADD THESE METHODS TO JARVIS:

1. Open jarvis_panel.py
2. Find the JarvisAntigravity class
3. Add these methods inside the class (after existing methods)
4. Save the file
5. Run JARVIS

All new buttons will work automatically!
"""
