"""
JARVIS ALL FUNCTIONS PANEL
সব Functions এর Buttons

Complete button panel with ALL JARVIS functions organized by category.
সব JARVIS functions এর জন্য complete button panel।
"""

import customtkinter as ctk
from tkinter import messagebox
import threading


class AllFunctionsPanel(ctk.CTkToplevel):
    """Panel with ALL JARVIS functions as buttons"""
    
    def __init__(self, parent, process_callback):
        super().__init__(parent)
        
        self.process_callback = process_callback
        
        self.title("JARVIS - ALL FUNCTIONS")
        self.geometry("1400x900")
        
        # Colors
        self.bg_color = "#02050A"
        self.fg_color = "#05080F"
        self.accent_color = "#00F3FF"
        self.button_color = "#003355"
        self.hover_color = "#005577"
        
        self.configure(fg_color=self.bg_color)
        
        # Header
        header = ctk.CTkFrame(self, fg_color=self.fg_color, height=80)
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header,
            text="🤖 JARVIS - ALL FUNCTIONS PANEL",
            font=("Courier New", 28, "bold"),
            text_color=self.accent_color
        ).pack(pady=20)
        
        # Main container with scrollable frame
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.bg_color,
            scrollbar_button_color=self.button_color,
            scrollbar_button_hover_color=self.hover_color
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create all function categories
        self._create_all_categories(main_container)
    
    def _create_all_categories(self, container):
        """Create all function categories with buttons"""
        
        # Category 1: CORE SYSTEMS
        self._add_category(container, "🔧 CORE SYSTEMS", [
            ("System Clean", "clean", "#003355"),
            ("Workspace", "workspace", "#003355"),
            ("Screenshot", "screenshot", "#003355"),
            ("Disk Analyze", "disk", "#003355"),
            ("System Info", "system info", "#003355"),
            ("System Stats", "stats", "#003355"),
            ("Memory Info", "memory", "#003355"),
            ("Disk Info", "disk info", "#003355"),
            ("Running Processes", "processes", "#003355"),
            ("Task Manager", "task manager", "#003355"),
            ("Lock Computer", "lock", "#660000"),
            ("Shutdown", "shutdown", "#660000"),
            ("Restart", "restart", "#660000"),
            ("Empty Recycle Bin", "empty bin", "#003355"),
            ("Set Brightness", "brightness", "#003355"),
            ("Control Volume", "volume", "#003355"),
            ("Media Control", "media", "#003355"),
        ])
        
        # Category 2: NETWORK OPERATIONS
        self._add_category(container, "🌐 NETWORK OPERATIONS", [
            ("Network Scan", "recon", "#004466"),
            ("WiFi Scan", "wifi", "#004466"),
            ("Network Users", "users", "#004466"),
            ("Devices", "devices", "#004466"),
            ("Router Scan", "router", "#004466"),
            ("Ping Device", "ping", "#004466"),
            ("Deep Port Scan", "portscan", "#004466"),
            ("Scan Router Devices", "router devices", "#004466"),
            ("Router Connect", "router connect", "#004466"),
            ("Scan Bluetooth", "bluetooth", "#004466"),
            ("Signal Scan", "signal", "#004466"),
            ("Find and Connect", "findconnect", "#004466"),
        ])
        
        # Category 3: LEARNING SYSTEMS
        self._add_category(container, "📚 LEARNING SYSTEMS", [
            ("Auto Background Learn", "autobg", "#006644"),
            ("Start Auto Learning", "start auto learning", "#006644"),
            ("Stop Auto Learning", "stop auto learning", "#006644"),
            ("Auto Learning Stats", "auto learning stats", "#006644"),
            ("Search & Learn", "searchlearn", "#006644"),
            ("Learn 10 Words", "learn10", "#006644"),
            ("Learn 50 Words", "learn50", "#006644"),
            ("Learn Article", "learnarticle", "#006644"),
            ("Article List", "articlelist", "#006644"),
            ("Search History", "searchhistory", "#006644"),
            ("Internet Learn", "learn from internet", "#006644"),
            ("Ultimate Learn", "ultimate learn", "#006644"),
            ("Auto Learn", "auto learn", "#006644"),
            ("Tree Learn", "tree learn", "#006644"),
            ("Tree Auto Learn", "tree auto", "#006644"),
            ("Infinite Learn", "infinite learn", "#006644"),
        ])
        
        # Category 4: INTELLIGENCE SYSTEMS
        self._add_category(container, "🧠 INTELLIGENCE SYSTEMS", [
            ("Brain Status", "brain status", "#440066"),
            ("Ollama (Local)", "brain ollama", "#440066"),
            ("Groq Fast", "brain groq", "#440066"),
            ("Parallel Think", "brain parallel", "#440066"),
            ("Multi-Brain", "multibrain", "#440066"),
            ("Ultimate Intelligence", "ultimate intelligence", "#440066"),
            ("Human Brain", "human brain", "#440066"),
            ("Emotional State", "emotional state", "#440066"),
            ("Smart Suggestions", "suggest", "#440066"),
            ("Chat History", "chat history", "#440066"),
        ])
        
        # Category 5: GENERATOR
        self._add_category(container, "🎨 AI GENERATOR", [
            ("Generate Image", "gen image", "#003300"),
            ("Generate Video", "gen video", "#003300"),
            ("Generate Audio", "gen audio", "#003300"),
            ("Generate 3D Model", "gen 3d", "#003300"),
            ("Generate Text", "gen text", "#003300"),
            ("Generate File", "gen file", "#003300"),
            ("Generate Photo", "gen photo", "#003300"),
            ("List Generated", "gen list", "#003300"),
            ("Open Gen Folder", "gen folder", "#003300"),
        ])
        
        # Category 6: TRANSLATOR
        self._add_category(container, "🌍 TRANSLATOR", [
            ("Translate", "translate", "#004466"),
            ("Languages", "languages", "#004466"),
            ("Translation History", "transhistory", "#004466"),
        ])
        
        # Category 7: ELITE TOOLS
        self._add_category(container, "⚡ ELITE TOOLS", [
            ("Kali Mode", "kali", "#660088"),
            ("Remote Console", "remote", "#660088"),
            ("Flipper Mode", "flipper", "#EE7700"),
            ("Alien Mode", "alien", "#009900"),
            ("Virus Purge", "purge", "#990000"),
            ("Firewall", "firewall", "#006688"),
            ("Browser Control", "browser", "#006688"),
            ("Web Audit", "webaudit", "#338800"),
            ("Web Security Audit", "web security", "#338800"),
            ("Ducky Deploy", "ducky", "#EE7700"),
            ("Alien Cipher", "cipher", "#009900"),
            ("Neutralize Badshah", "neutralize", "#990000"),
            ("Infinity Firewall", "infinity firewall", "#006688"),
        ])
        
        # Category 8: AUTOMATION
        self._add_category(container, "🤖 AUTOMATION", [
            ("Agent Mode ON", "agent on", "#006688"),
            ("Agent Mode OFF", "agent off", "#006688"),
            ("Schedule Task", "auto schedule", "#005566"),
            ("List Tasks", "auto list", "#005566"),
            ("Super Host", "superhost", "#006644"),
            ("Auto Controller", "auto controller", "#005566"),
            ("Auto Collect Info", "autocollect", "#005566"),
            ("Deploy Bot", "deploy bot", "#005566"),
        ])
        
        # Category 9: WINDOW & APP CONTROL
        self._add_category(container, "🪟 WINDOW & APP CONTROL", [
            ("Window Control", "window", "#004466"),
            ("App Control", "app help", "#004466"),
            ("Control Window", "control window", "#004466"),
            ("Manage Device", "manage device", "#004466"),
            ("Open Explorer", "explorer", "#004466"),
        ])
        
        # Category 10: UPLINK & SHARING
        self._add_category(container, "📡 UPLINK & SHARING", [
            ("Mobile Uplink", "mobile", "#886600"),
            ("Share Screen", "share", "#006688"),
            ("Send Files", "send", "#006688"),
            ("Share Files", "share files", "#006688"),
            ("Create Screen Share", "screen share", "#006688"),
        ])
        
        # Category 11: GAMING & BOOST
        self._add_category(container, "🎮 GAMING & BOOST", [
            ("Boost Game", "boost game", "#660066"),
            ("Android Boost", "android boost", "#660066"),
        ])
        
        # Category 12: SELF-SYSTEMS
        self._add_category(container, "🔧 SELF-SYSTEMS", [
            ("Self Check", "selfcheck", "#006600"),
            ("System Doctor", "doctor", "#006600"),
            ("Self Heal", "self heal", "#006600"),
            ("Self Diagnosis", "diagnose", "#006600"),
            ("Self Improve", "improve yourself", "#006600"),
            ("Build Yourself", "build yourself", "#006600"),
            ("Healing Stats", "healing stats", "#006600"),
            ("Improvement Stats", "improvement stats", "#006600"),
        ])
        
        # Category 13: DEBUGGING & TESTING
        self._add_category(container, "🐛 DEBUGGING & TESTING", [
            ("Bug Detect", "bugcheck", "#660000"),
            ("Auto Fix Bugs", "bugfix", "#660000"),
            ("Detect Bugs", "detect bugs", "#660000"),
            ("Scan for Viruses", "scan virus", "#660000"),
            ("Force Kill Process", "force kill", "#660000"),
        ])
        
        # Category 14: STREAMING & MONITORING
        self._add_category(container, "📊 STREAMING & MONITORING", [
            ("Streaming Mode", "stream toggle", "#006655"),
            ("System Monitor", "monitor", "#008888"),
            ("Performance Monitor", "performance", "#008888"),
        ])
        
        # Category 15: CLIPBOARD & NOTES
        self._add_category(container, "📋 CLIPBOARD & NOTES", [
            ("Copy to Clipboard", "copy", "#004466"),
            ("Save Note", "note", "#004466"),
        ])
        
        # Category 16: PAYLOAD & SECURITY
        self._add_category(container, "🔐 PAYLOAD & SECURITY", [
            ("Generate Payload", "payload", "#660000"),
        ])
        
        # Category 17: VOICE & SPEECH
        self._add_category(container, "🎤 VOICE & SPEECH", [
            ("Listen", "listen", "#FF3131"),
            ("Speak", "speak", "#FF3131"),
            ("Voice Browser", "voice browser", "#FF3131"),
        ])
        
        # Category 18: FILE OPERATIONS
        self._add_category(container, "📁 FILE OPERATIONS", [
            ("Upload File", "upload", "#004466"),
            ("Recent Uploads", "recent uploads", "#004466"),
        ])
        
        # Category 19: SEARCH & WEB
        self._add_category(container, "🔍 SEARCH & WEB", [
            ("Web Search", "web search", "#006644"),
            ("Google Search", "google", "#006644"),
            ("Search Engine", "search", "#006644"),
        ])
        
        # Category 20: ADVANCED FEATURES
        self._add_category(container, "🚀 ADVANCED FEATURES", [
            ("Ultra Fast Tree Learn", "ultra fast tree", "#FF3131"),
            ("Advanced Cache", "cache", "#FF3131"),
            ("Performance Monitor", "perf monitor", "#FF3131"),
            ("Intelligent Answer", "intelligent answer", "#FF3131"),
            ("Unified Auto Learner", "unified auto", "#FF3131"),
        ])
    
    def _add_category(self, container, title, buttons):
        """Add a category with buttons"""
        # Category frame
        category_frame = ctk.CTkFrame(container, fg_color=self.fg_color)
        category_frame.pack(fill="x", padx=10, pady=10)
        
        # Category title
        ctk.CTkLabel(
            category_frame,
            text=title,
            font=("Courier New", 18, "bold"),
            text_color=self.accent_color
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Buttons grid
        buttons_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Create buttons in grid (4 columns)
        for i, (text, command, color) in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=lambda cmd=command: self._execute_command(cmd),
                fg_color=color,
                hover_color=self._lighten_color(color),
                font=("Courier New", 12, "bold"),
                height=40,
                width=200
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Configure grid columns to expand equally
        for col in range(4):
            buttons_frame.grid_columnconfigure(col, weight=1)
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        # Simple lightening by adding to each RGB component
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, r + 40)
        g = min(255, g + 40)
        b = min(255, b + 40)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _execute_command(self, command):
        """Execute a command"""
        try:
            # Call the parent's process callback
            if self.process_callback:
                threading.Thread(
                    target=self.process_callback,
                    args=(command,),
                    daemon=True
                ).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute command: {e}")


def open_all_functions_panel(parent, process_callback):
    """Open the all functions panel"""
    panel = AllFunctionsPanel(parent, process_callback)
    panel.focus()
    return panel


# Test
if __name__ == "__main__":
    def test_callback(cmd):
        print(f"Executing: {cmd}")
    
    app = ctk.CTk()
    app.title("Test")
    app.geometry("400x300")
    
    ctk.CTkButton(
        app,
        text="Open All Functions Panel",
        command=lambda: open_all_functions_panel(app, test_callback)
    ).pack(expand=True)
    
    app.mainloop()
