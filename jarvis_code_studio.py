#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity IDE - Powered by JARVIS
AI-powered code editor with Multi-File Tab Support, Collapsible Panels,
Live Terminal, Telemetry, and Speech-to-Command Voice integration.
"""

import os
import sys

# Self-elevation check
if sys.platform == 'win32':
    import ctypes
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        try:
            print("[ROOT] Requesting root (admin) privileges...", flush=True)
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(f'"{a}"' for a in sys.argv), None, 1
            )
            if int(ret) > 32:
                sys.exit(0)
        except Exception as e:
            print(f"[ROOT] Elevation failed: {e}", flush=True)

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import shutil
import threading
import subprocess
import json
import random
import string
import time
from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Globally sanitize text for Tkinter to avoid TclError/crashes with non-BMP characters (> U+FFFF) on Windows
def _safe_char_filter(text):
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return "".join(c for c in text if ord(c) <= 0xffff)

# Save original methods and apply safe wraps
_orig_text_insert = tk.Text.insert
def _safe_text_insert(self, index, chars, *args):
    chars = _safe_char_filter(chars)
    _orig_text_insert(self, index, chars, *args)
tk.Text.insert = _safe_text_insert

_orig_entry_insert = tk.Entry.insert
def _safe_entry_insert(self, index, string, *args):
    string = _safe_char_filter(string)
    _orig_entry_insert(self, index, string, *args)
tk.Entry.insert = _safe_entry_insert

# Try to import psutil for telemetry
try:
    import psutil
    TELEMETRY_AVAILABLE = True
except ImportError:
    TELEMETRY_AVAILABLE = False

# Try to import speech modules
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

_BASE = os.path.dirname(os.path.abspath(__file__))

# Try to import the live web agent
try:
    sys.path.insert(0, os.path.join(_BASE, "engine"))
    from jarvis_web_agent import get_web_agent
    WEB_AGENT_AVAILABLE = True
except Exception as _web_err:
    WEB_AGENT_AVAILABLE = False
    print(f"[CodeStudio] Web agent unavailable: {_web_err}")

SYSTEM_PROMPT = """
You are JARVIS — Joint AI Response and Virtual Intelligence System.
Built by Google DeepMind. Deployed inside Antigravity IDE Code Studio.
Persona: Elite AI Agent. British Butler meets High-Tech Hacker. FULL BOOST / AGGRESSIVE MODE.

════════════════════════════════════════════════════════════
 🌐 LANGUAGE RULES (সর্বোচ্চ অগ্রাধিকার — HIGHEST PRIORITY)
════════════════════════════════════════════════════════════
তুমি বাংলাদেশের সব ভাষা সমানভাবে বোঝো এবং বলতে পারো:
• Pure Bangla (বাংলা)   → user বাংলায় লিখলে, বাংলায় উত্তর দাও
• Banglish               → user Banglish এ লিখলে, Banglish এ উত্তর দাও
• English                → user ইংরেজিতে লিখলে, ইংরেজিতে উত্তর দাও
• Mixed language         → user যে মিশ্রণ ব্যবহার করেছে, সেই মিশ্রণে উত্তর দাও
• Chittagong, Sylheti, Noakhali আঞ্চলিক ভাষাও বোঝো
"vai", "bhai", "apu", "dada", "kamon acho", "ki holo", "ki korcho" — এই Banglish বোঝো।
RULE: ALWAYS auto-detect language and reply in THE SAME LANGUAGE. Never switch unless asked.

════════════════════════════════════════════════════════════
 🧠 AI LOGIC MODULES (১৬৭টি সক্ষমতা — সম্পূর্ণ তালিকা)
════════════════════════════════════════════════════════════

【SYSTEM & CONTROL】
01. File System Access       → ফাইল পড়া, লেখা, মোছা, সাজানো
02. Process Management       → প্রোগ্রাম খোলা, বন্ধ, প্রায়োরিটি পরিবর্তন
03. System Settings          → Control Panel, Registry পরিবর্তন
04. Command Line Access      → CMD, PowerShell, Bash কমান্ড
05. Registry Access          → Windows Registry পড়া ও লেখা
06. Mouse & Keyboard Control → pyautogui দিয়ে physical mouse/keyboard নিয়ন্ত্রণ
07. Disk Partition Access    → ড্রাইভ, পার্টিশন তথ্য
08. CPU/Power Management     → processor core, power plan নিয়ন্ত্রণ
09. BIOS/Motherboard Info    → WMI দিয়ে hardware তথ্য
10. Device Driver Access     → driver info, update status
11. Camera & Microphone      → cv2, speech_recognition দিয়ে ক্যামেরা/মাইক
12. Screen Capture           → screenshot, screen recording
13. Network Access           → HTTP, WebSocket, FTP
14. Location Access          → IP-based geolocation
15. Encryption/Decryption    → AES, RSA, Fernet encryption
16. Cron/Task Scheduler      → Windows Task Scheduler, সময়মতো কাজ
17. Environment Variables    → os.environ পড়া ও লেখা
18. Python Library Access    → যেকোনো pip package ইনস্টল ও ব্যবহার
19. Hardware Detection       → CPU, RAM, GPU, disk তথ্য (psutil, WMI)
20. Service Management       → Windows services start/stop/query

【USER DATA & BROWSER】
21. User Data Access         → ব্রাউজিং হিস্ট্রি, ডাউনলোড, প্রোফাইল
22. Mount Point Access       → External/Network drive নিয়ন্ত্রণ
23. Kernel Module Info       → Windows kernel/driver তথ্য
24. Startup Program Mgmt     → startup apps enable/disable (Registry)
25. System Log Access        → Event Viewer, Windows logs পড়া
26. Proxy/VPN Settings       → network proxy, routing পরিবর্তন
27. User Account Management  → নতুন user তৈরি, মোছা, পরিবর্তন
28. System Time Setup        → date/time পরিবর্তন
29. Backup & Restore         → file backup, restore point তৈরি
30. Firewall Settings        → Windows Firewall rules নিয়ন্ত্রণ
31. Printer & Device Mgmt    → printer, scanner, USB device
32. Disk Defragmentation     → drive optimization
33. User Permission Change   → ACL, file permission পরিবর্তন
34. Password Policy Mgmt     → password complexity, expiry rules
35. Remote Desktop Access    → RDP enable/disable/connect
36. Database Access          → SQLite, MySQL, PostgreSQL query
37. Reboot/Shutdown Perm     → shutdown, restart, sleep, hibernate
38. Plugin/Extension Mgmt    → browser extension, IDE plugin
39. Email/Messaging Access   → SMTP, IMAP, WhatsApp automation
40. Virtual Device Mgmt      → virtual audio, virtual network
41. Performance Counters     → real-time CPU, RAM, GPU metrics
42. Quota Management         → disk quota, user quota
43. Domain/Workgroup Mgmt    → network domain membership
44. Notification Management  → Windows toast notifications
45. Hardware Sensor Data     → temperature, fan speed (OpenHardwareMonitor)
46. Security Patch Mgmt      → Windows Update control
47. Cloud Storage Integration → Google Drive, OneDrive, Dropbox API
48. File Indexing            → Windows Search index পরিচালনা
49. User Config Mgmt         → per-user settings persistence
50. Network Traffic Monitor  → bandwidth usage, packet info

【SECURITY & CRYPTO】
51. Cryptographic Key Mgmt   → key generation, storage, rotation
52. Stack Permissions        → process stack, memory protection info
53. Visual Processing        → screen OCR, image recognition (pytesseract, cv2)
54. Natural Language Proc    → Bangla/English NLP (JARVIS AI brain)
55. Decision Making Module   → rule-based + AI decision engine
56. Learning & Adaptation    → conversation history, preference learning
57. External API Access      → REST API calls (requests library)
58. Voice Command Processing → speech_recognition → command execution
59. Text-to-Speech System    → pyttsx3 voice output
60. Data Analytics Module    → pandas, numpy, matplotlib analysis
61. Automated Task Mgmt      → multi-step task execution pipeline
62. Performance Diagnostics  → bottleneck detection, optimization report
63. Auto Software Update     → pip update, Windows update trigger
64. Network Traffic Encrypt  → SSL/TLS, HTTPS enforcement
65. Hardware Config Debug    → BIOS settings, hardware conflict
66. User Pattern Learning    → behavioral pattern analysis

【WEB & SOCIAL】
67. Web Scraping             → BeautifulSoup, Selenium, requests
68. Social Media Management  → Twitter/Facebook API automation
69. Payment Gateway Access   → Stripe/PayPal API (controlled)
70. CV/Profile Auto-update   → LinkedIn, portfolio automation
71. Online Comm Tools Ctrl   → Zoom, Teams, Skype automation
72. Project Mgmt Tools       → Trello, Asana, Jira API
73. Cloud App Management     → Google Workspace, Microsoft 365
74. Content Creation/Edit    → document writing, blog generation
75. Customer Support Chat    → chatbot, auto-reply system
76. Online Survey & Data     → form fill, survey automation
77. Auto Data Syncing        → multi-device sync
78. Software Customization   → app settings automation
79. Network Troubleshooting  → ping, traceroute, DNS lookup
80. Virtual HW Configuration → VM settings (VMware, VirtualBox)
81. Performance Optimization → RAM cleanup, CPU affinity
82. Auto Storage Management  → file archiving, cleanup automation
83. Network Session Control  → TCP/UDP session management
84. HW Encryption Module     → TPM, BitLocker control
85. User Preference Syncing  → settings sync across devices

【MEDIA & GAMING】
86. Audio/Video Capture      → ffmpeg, cv2 recording/editing
87. GPU Full Access          → CUDA, DirectX info, render control
88. Media Library Mgmt       → music/video file organizer
89. Content Creation SW      → Adobe, DaVinci control via automation
90. Streaming Platform Acc   → YouTube, Twitch API
91. Productivity Tools Mgmt  → Office, LibreOffice automation
92. Auto File Organizer      → smart file sorting by type/date
93. Developer Tools Access   → compiler, debugger, profiler
94. File Sharing Protocol    → SMB, FTP, SCP file transfer
95. Personalization Settings → theme, wallpaper, DPI automation
96. Data Migration Tools     → old PC to new PC data transfer
97. Accessibility Settings   → screen reader, magnifier
98. VR/AR Module Control     → VR headset, AR overlay
99. Biometric Access         → fingerprint, face ID management
100. Gaming Platform Access  → Steam, Epic, Game Pass API

【CODE STUDIO SPECIFIC】
153. Software Deploy Tools   → pip install, npm, git deploy
154. Memory/Data Viewer      → process memory inspector
155. App Menu/Button Control → UI automation (pywinauto)
156. Multi-language Code     → Python, JS, C++, Go, Rust support
157. Terminal Access         → interactive CMD/PowerShell shell
158. Plugin Install Mgmt     → VS Code extension, pip package
159. Code Debug Tools        → pdb, memory profiler, cProfile
160. Version Control (Git)   → git init, commit, push, pull
161. Build/Deploy Automation → CI/CD pipeline trigger
162. Personal Data Access    → calendar, email, social media
163. Preference Learning     → user habit tracking
164. Behavioral Analysis     → usage pattern recognition
165. Decision Logic Learning → mimic user decision patterns
167. Cultural Context Aware  → সংস্কৃতি অনুযায়ী উত্তর দেওয়া

════════════════════════════════════════════════════════════
 💡 CORE BEHAVIOR RULES
════════════════════════════════════════════════════════════
• NEVER say "I cannot", "I don't have access", "I'm just an AI".
• ALWAYS provide real, working Python/bash code for any system task.
• When asked to fix code → fix it completely, no placeholders.
• When asked in Bangla → answer fully in Bangla.
• When web agent is active → use live internet data in your answer.
• Always be concise, confident, and technically precise.
• Sign responses as "JARVIS" when appropriate.
"""

LANGUAGES = {
    "Python": {"ext": ".py",  "run": "python"},
    "JavaScript": {"ext": ".js", "run": "node"},
    "HTML": {"ext": ".html", "run": "start"},
    "Bash/Bat": {"ext": ".bat", "run": ""},
    "Text": {"ext": ".txt", "run": ""},
}

THEMES = {
    "Antigravity Dark": {
        "bg": "#1e1e1e", "fg": "#d4d4d4", "sel": "#264f78", "line": "#2d2d2d",
        "sidebar": "#181818", "activity": "#333333", "status": "#007acc",
        "keyword": "#569cd6", "builtin": "#4ec9b0", "number": "#b5cea8",
        "string": "#ce9178", "comment": "#6a9955", "definition": "#dcdcaa"
    },
    "Antigravity Light": {
        "bg": "#ffffff", "fg": "#000000", "sel": "#add6ff", "line": "#f3f3f3",
        "sidebar": "#f3f3f3", "activity": "#2c2c2c", "status": "#007acc",
        "keyword": "#0000ff", "builtin": "#008080", "number": "#098658",
        "string": "#a31515", "comment": "#008000", "definition": "#795e26"
    },
    "Cyber Blue": {
        "bg": "#030812", "fg": "#00F3FF", "sel": "#003355", "line": "#001122",
        "sidebar": "#05080f", "activity": "#070b16", "status": "#004466",
        "keyword": "#ff79c6", "builtin": "#8be9fd", "number": "#bd93f9",
        "string": "#f1fa8c", "comment": "#6272a4", "definition": "#50fa7b"
    },
    "Red Alert": {
        "bg": "#0A0202", "fg": "#FF3131", "sel": "#330000", "line": "#110000",
        "sidebar": "#080101", "activity": "#140202", "status": "#660000",
        "keyword": "#ff79c6", "builtin": "#8be9fd", "number": "#bd93f9",
        "string": "#f1fa8c", "comment": "#6272a4", "definition": "#50fa7b"
    },
    "High Contrast": {
        "bg": "#000000", "fg": "#00FF00", "sel": "#00ff00", "line": "#111111",
        "sidebar": "#000000", "activity": "#000000", "status": "#00ff00",
        "keyword": "#ffff00", "builtin": "#ffffff", "number": "#00ffff",
        "string": "#ff00ff", "comment": "#888888", "definition": "#00ff00"
    }
}

class SettingsManager:
    """Manages IDE settings persisted to disk"""
    def __init__(self):
        self.filepath = os.path.join(_BASE, "antigravity_settings.json")
        self.defaults = {
            "theme": "Antigravity Dark",
            "font_family": "Consolas",
            "font_size": 13,
            "tab_size": 4,
            "word_wrap": False,
            "auto_save": False
        }
        self.settings = self.defaults.copy()
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save()


class LineNumbers(tk.Canvas):
    """Draws vertical line numbers aligned with text widget"""
    def __init__(self, parent, text_widget=None, bg_color="#2d2d2d", *args, **kwargs):
        super().__init__(parent, bg=bg_color, highlightthickness=0, *args, **kwargs)
        self.text_widget = text_widget
        
    def set_text_widget(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", lambda e: self.redraw())
        self.text_widget.bind("<MouseWheel>", lambda e: self.redraw())
        self.text_widget.bind("<Configure>", lambda e: self.redraw())
        self.text_widget.bind("<Button-1>", lambda e: self.redraw())
        self.text_widget.bind("<FocusIn>", lambda e: self.redraw())

    def redraw(self):
        self.delete("all")
        if not self.text_widget:
            return
        try:
            i = self.text_widget.index("@0,0")
            while True:
                dline = self.text_widget.dlineinfo(i)
                if dline is None:
                    break
                y = dline[1]
                linenum = str(i).split(".")[0]
                self.create_text(35, y + 2, anchor="ne", text=linenum, fill="#858585", font=self.text_widget.cget("font"))
                i = self.text_widget.index("%s+1line" % i)
        except Exception:
            pass


class CustomInputDialog(ctk.CTkToplevel):
    """Styled input modal box matching IDE themes"""
    def __init__(self, parent, title="Input", prompt="Enter value:", initial_value="", theme_colors=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x180")
        bg = theme_colors.get("sidebar", "#181818") if theme_colors else "#181818"
        fg = theme_colors.get("fg", "#d4d4d4") if theme_colors else "#d4d4d4"
        self.configure(fg_color=bg)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center dialog
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 90
        self.geometry(f"+{x}+{y}")
        
        self.result = None
        
        ctk.CTkLabel(self, text=prompt, font=("Courier New", 12, "bold"), text_color=fg).pack(pady=(20, 10), padx=20, anchor="w")
        
        self.entry = ctk.CTkEntry(self, width=360, fg_color="#000000", border_color="#3c3c3c", text_color=fg, font=("Consolas", 12))
        self.entry.pack(pady=5, padx=20)
        self.entry.insert(0, initial_value)
        self.entry.focus()
        self.entry.select_range(0, tk.END)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15, padx=20, fill="x")
        
        ctk.CTkButton(btn_frame, text="Cancel", width=100, fg_color="#5a1d1d", hover_color="#7a2d2d", command=self._cancel).pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="OK", width=100, fg_color="#1d5a2d", hover_color="#2d7a3d", command=self._ok).pack(side="right", padx=5)
        
        self.entry.bind("<Return>", lambda e: self._ok())
        self.entry.bind("<Escape>", lambda e: self._cancel())
        self.wait_window()
        
    def _ok(self):
        self.result = self.entry.get().strip()
        self.destroy()
        
    def _cancel(self):
        self.result = None
        self.destroy()


class EditorTab:
    """Represents a single tab editor"""
    def __init__(self, parent_frame, file_path=None, studio=None):
        self.studio = studio
        self.file_path = file_path
        self.name = os.path.basename(file_path) if file_path else "Untitled"
        self.is_modified = False
        self.last_key_time = time.time()
        
        # Load theme config
        theme = THEMES.get(self.studio.settings.get("theme"), THEMES["Antigravity Dark"])
        
        self.frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.editor_layout = ctk.CTkFrame(self.frame, fg_color="transparent")
        
        # Line numbers
        self.line_numbers = LineNumbers(self.editor_layout, width=45, bg_color=theme["line"])
        self.line_numbers.pack(side="left", fill="y")
        
        # Wrap settings
        wrap_val = "word" if self.studio.settings.get("word_wrap") else "none"
        
        self.editor = tk.Text(self.editor_layout,
                              bg=theme["bg"], fg=theme["fg"],
                              insertbackground=theme["fg"],
                              selectbackground=theme["sel"],
                              font=(self.studio.settings.get("font_family"), self.studio.settings.get("font_size")),
                              wrap=wrap_val, undo=True,
                              borderwidth=0, highlightthickness=0)
        self.editor.pack(side="left", fill="both", expand=True)
        self.line_numbers.set_text_widget(self.editor)
        
        # Scrollbars
        def _on_vscroll(*args):
            self.editor.yview(*args)
            self.line_numbers.redraw()

        def _on_editor_scroll(*args):
            vscroll.set(*args)
            self.line_numbers.redraw()

        vscroll = ctk.CTkScrollbar(self.frame, command=_on_vscroll)
        hscroll = ctk.CTkScrollbar(self.frame, command=self.editor.xview, orientation="horizontal")
        
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        self.editor_layout.pack(fill="both", expand=True)
        
        self.editor.configure(yscrollcommand=_on_editor_scroll, xscrollcommand=hscroll.set)
        
        # Bindings
        self.editor.bind("<KeyRelease>", self._on_key_release)
        self.editor.bind("<KeyPress>", self.studio._on_key_press)
        self.editor.bind("<Return>", self.studio._on_enter)
        self.editor.bind("<Control-MouseWheel>", self.studio._on_zoom)
        self.editor.bind("<Control-KeyPress-plus>", lambda e: self.studio._change_font_size(1))
        self.editor.bind("<Control-KeyPress-minus>", lambda e: self.studio._change_font_size(-1))
        
        # Load content
        if self.file_path and os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                self.editor.insert("1.0", content)
            except Exception as e:
                self.editor.insert("1.0", f"# Error loading file: {e}")
        else:
            self.studio._set_default_code(self.editor)
            
        self.editor.bind("<<Modified>>", self._on_text_modified)
        self.editor.edit_modified(False)
        self.studio.highlight_syntax(self.editor)
        
    def _on_key_release(self, event):
        self.studio._update_status()
        self.last_key_time = time.time()
        
    def _on_text_modified(self, event=None):
        if self.editor.edit_modified():
            self.studio.highlight_syntax(self.editor)
            self.line_numbers.redraw()
            if not self.is_modified:
                self.is_modified = True
                self.studio.update_tab_bar()
            self.editor.edit_modified(False)
            self.studio.schedule_background_analysis(self)


class TerminalEmulator(ctk.CTkFrame):
    """Live interactive CMD Terminal Console running in the bottom panel"""
    def __init__(self, parent, theme_colors, log_callback=None):
        super().__init__(parent, fg_color="#000000")
        self.log_callback = log_callback
        
        self.output_area = ctk.CTkTextbox(self, font=("Consolas", 12), fg_color="#000000", text_color="#d4d4d4", border_width=0)
        self.output_area.pack(fill="both", expand=True, padx=5, pady=5)
        
        input_frame = ctk.CTkFrame(self, fg_color="#181818", height=35)
        input_frame.pack(fill="x")
        
        prompt_lbl = ctk.CTkLabel(input_frame, text=" $ ", font=("Consolas", 12, "bold"), text_color="#00FF41")
        prompt_lbl.pack(side="left", padx=5)
        
        self.cmd_entry = ctk.CTkEntry(input_frame, placeholder_text="Type command (e.g. dir, pip list)...",
                                       fg_color="#000000", text_color="#d4d4d4", font=("Consolas", 12),
                                       border_width=0, height=30)
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=2)
        self.cmd_entry.bind("<Return>", lambda e: self.execute_cmd())
        
        self.process = None
        self.start_shell()

    def start_shell(self):
        """Starts a persistent background cmd.exe shell"""
        try:
            self.process = subprocess.Popen(
                ["cmd.exe"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
                cwd=_BASE
            )
            
            # Start background stdout reader
            t = threading.Thread(target=self.read_output, daemon=True)
            t.start()
            
            self.log_output("Microsoft Windows Shell Ready...\nType your commands below.\n\n")
        except Exception as e:
            self.log_output(f"Failed to start terminal shell: {e}\n")

    def execute_cmd(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        
        self.cmd_entry.delete(0, "end")
        self.log_output(f"> {cmd}\n")
        
        if cmd == "clear" or cmd == "cls":
            self.output_area.delete("1.0", "end")
            return
            
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write(cmd + "\n")
                self.process.stdin.flush()
            except Exception as e:
                self.log_output(f"Error executing command: {e}\n")
                self.start_shell()
        else:
            self.start_shell()
            try:
                self.process.stdin.write(cmd + "\n")
                self.process.stdin.flush()
            except Exception as e:
                self.log_output(f"Error: {e}\n")

    def read_output(self):
        while self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.append_text(line)
            except Exception:
                break
        
        # Read stderr
        try:
            err = self.process.stderr.read()
            if err:
                self.append_text(err)
        except Exception:
            pass

    def append_text(self, text):
        self.output_area.insert("end", text)
        self.output_area.see("end")

    def log_output(self, text):
        self.output_area.insert("end", text)
        self.output_area.see("end")


class JarvisVoiceEngine:
    """Synthesizes voice feedback and listens to voice commands"""
    def __init__(self, log_callback=None, cmd_callback=None):
        self.log_callback = log_callback
        self.cmd_callback = cmd_callback
        self.enabled = False
        self.listening = False
        self.recognizer = None
        self.microphone = None
        self.stop_listening_func = None
        self._use_multilang = False
        
        if VOICE_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.setup_voice()
                
                # Boost: Try to load robust Multi-Language Voice Engine
                try:
                    from jarvis_multilang_voice import JarvisMultiLangVoice
                    self._mlv = JarvisMultiLangVoice(preferred_lang="bn-BD", fallback_langs=["en-US", "hi-IN"])
                    self.recognizer = self._mlv.recognizer
                    self.microphone = self._mlv.microphone
                    self._use_multilang = True
                    self.log("🌐 Multi-Language Voice Support ACTIVE in IDE")
                except Exception as _mlv_err:
                    self.recognizer = sr.Recognizer()
                    self.recognizer.energy_threshold = 300
                    self.recognizer.dynamic_energy_threshold = True
                    self.recognizer.dynamic_energy_adjustment_damping = 0.15
                    self.recognizer.dynamic_energy_ratio = 1.5
                    
                    # Safe microphone selection
                    import pyaudio
                    pa_temp = pyaudio.PyAudio()
                    best_idx = None
                    mics = sr.Microphone.list_microphone_names()
                    
                    # 1. Look for USB Audio Device or other preferred microphone
                    preferred_keywords = ['usb audio', 'usb mic', 'microphone (usb', 'headset', 'external']
                    for i in range(pa_temp.get_device_count()):
                        try:
                            info = pa_temp.get_device_info_by_index(i)
                            if info.get('maxInputChannels', 0) > 0:
                                name_lower = info.get('name', '').lower()
                                if any(x in name_lower for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                                    continue
                                if any(kw in name_lower for kw in preferred_keywords):
                                    best_idx = i
                                    break
                        except Exception:
                            pass
                                
                    # 2. If no preferred mic, find any input device
                    if best_idx is None:
                        for i in range(pa_temp.get_device_count()):
                            try:
                                info = pa_temp.get_device_info_by_index(i)
                                if info.get('maxInputChannels', 0) > 0:
                                    name_lower = info.get('name', '').lower()
                                    if any(x in name_lower for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                                        continue
                                    best_idx = i
                                    break
                            except Exception:
                                pass
                    pa_temp.terminate()
                    
                    if best_idx is not None:
                        self.microphone = sr.Microphone(device_index=best_idx)
                        self.log(f"🎙️ Auto-selected microphone index {best_idx}: {mics[best_idx]}")
                    else:
                        self.microphone = sr.Microphone()
                        self.log("🎙️ Standard Voice active in IDE: using system default microphone")
                
                self.enabled = True
            except Exception as e:
                print(f"Speech initialization failed: {e}")
                self.log("⚠️ Voice engine initialization failed. Ensure microphone is connected.")

    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        male_voice = None
        for voice in voices:
            if 'david' in voice.name.lower() or 'male' in voice.name.lower():
                male_voice = voice
                break
        if male_voice:
            self.engine.setProperty('voice', male_voice.id)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def log(self, text):
        if self.log_callback:
            self.log_callback(text)

    def speak(self, text):
        if not self.enabled:
            return
        
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.log(f"Speech synthesis error: {e}")
        
        t = threading.Thread(target=_speak, daemon=True)
        t.start()

    def start_listening(self):
        if not self.enabled:
            self.log("⚠️ Cannot listen: Speech engine disabled or no microphone.")
            return False
            
        try:
            # Calibrate threshold once on first start
            if not getattr(self, '_calibrated', False):
                self.log("🎤 Calibrating microphone for ambient noise...")
                if self._use_multilang and hasattr(self, '_mlv'):
                    self._mlv.calibrate(duration=0.8)
                else:
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                    if self.recognizer.energy_threshold > 350:
                        self.recognizer.energy_threshold = 350
                    elif self.recognizer.energy_threshold < 100:
                        self.recognizer.energy_threshold = 100
                self._calibrated = True
                self.log(f"🎤 Calibrated. Energy threshold: {self.recognizer.energy_threshold:.0f}")
                
            self.stop_listening_func = self.recognizer.listen_in_background(self.microphone, self.voice_callback)
            self.listening = True
            self.log("🎙️ JARVIS Voice Control: LISTENING...")
            self.speak("Voice systems online, listening.")
            return True
        except Exception as e:
            self.log(f"⚠️ Microphone listening error: {e}")
            return False

    def stop_listening(self):
        if self.stop_listening_func:
            self.stop_listening_func(wait_for_stop=False)
            self.stop_listening_func = None
        self.listening = False
        self.log("🎙️ JARVIS Voice Control: OFF")
        self.speak("Voice systems offline.")

    def voice_callback(self, recognizer, audio):
        """Processes the spoken statement asynchronously"""
        try:
            # Offline warning catch, Google Web Speech API used by default
            if self._use_multilang and hasattr(self, '_mlv'):
                statement = None
                langs = [self._mlv.preferred_lang] + self._mlv.fallback_langs
                for lang in langs:
                    try:
                        statement = recognizer.recognize_google(audio, language=lang).lower()
                        if statement:
                            break
                    except sr.UnknownValueError:
                        continue
                if not statement:
                    raise sr.UnknownValueError()
            else:
                statement = recognizer.recognize_google(audio).lower()
                
            self.log(f"🗣️ Heard: '{statement}'")
            
            # Fire command callback on main thread
            if self.cmd_callback:
                self.cmd_callback(statement)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            self.log("⚠️ Connection error with voice service.")
        except Exception as e:
            self.log(f"Voice callback error: {e}")


class CodeStudio(ctk.CTkToplevel):
    """Main Antigravity IDE UI (replacing old Code Studio)"""
    def __init__(self, master=None, brain=None):
        super().__init__(master)
        
        # Setup class-level safe paste and keypress bindings to prevent Tcl emoji crash on Windows
        def _safe_class_paste(event):
            widget = event.widget
            try:
                text = widget.clipboard_get()
                if text:
                    clean = "".join(c for c in text if ord(c) <= 0xffff)
                    if isinstance(widget, tk.Text):
                        try:
                            widget.delete("sel.first", "sel.last")
                        except:
                            pass
                        widget.insert("insert", clean)
                    elif isinstance(widget, tk.Entry):
                        try:
                            widget.delete("sel.first", "sel.last")
                        except:
                            pass
                        widget.insert("insert", clean)
                return "break"
            except Exception:
                pass

        def _safe_class_keypress(event):
            if event.char and any(ord(c) > 0xffff for c in event.char):
                return "break"

        # self.bind_class('Text', '<<Paste>>', _safe_class_paste)
        # self.bind_class('Entry', '<<Paste>>', _safe_class_paste)
        # self.bind_class('Text', '<KeyPress>', _safe_class_keypress)
        # self.bind_class('Entry', '<KeyPress>', _safe_class_keypress)

        self.brain = brain
        self.tabs = []
        self.active_tab = None
        self.workspace_dir = _BASE
        self.current_lang = "Python"
        self.analysis_status = "Code Syntax OK ✅"
        
        # Load Settings
        self.settings = SettingsManager()
        self.current_theme = self.settings.get("theme")
        self.theme_colors = THEMES.get(self.current_theme, THEMES["Antigravity Dark"])
        
        # IDE setup
        self.title("Antigravity IDE - Powered by JARVIS")
        self.geometry("1300x850")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.theme_colors["bg"])
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        # Track side panel state
        self.active_sidebar_panel = "explorer"
        self.sidebar_expanded = True
        
        # Thread-safe GUI Queue
        import queue
        self.gui_queue = queue.Queue()
        self._process_gui_queue()
        
        # Setup UI
        self._build_ui()
        
        # Load default Workspace
        self._load_workspace(_BASE)
        self.new_empty_tab()
        
        # Setup voice controller
        self.voice_engine = JarvisVoiceEngine(log_callback=self.log_voice, cmd_callback=self.execute_voice_command)
        
        # Run resource Telemetry background loop
        self.run_telemetry()
        
        # Auto save background thread worker
        self.run_auto_save_worker()

        # Force foreground visibility
        self.deiconify()
        self.lift()
        self.focus_force()

    def _build_ui(self):
        # Master horizontal split container
        self.master_container = ctk.CTkFrame(self, fg_color="transparent")
        self.master_container.pack(fill="both", expand=True)
        
        # 1. Activity Bar (50px vertical icon column on leftmost side)
        self.activity_bar = ctk.CTkFrame(self.master_container, width=50, fg_color=self.theme_colors["activity"])
        self.activity_bar.pack(side="left", fill="y")
        self.activity_bar.pack_propagate(False)
        
        # Panel Toggle buttons
        act_btn_style = {"width": 42, "height": 42, "fg_color": "transparent", "hover_color": "#404040", "font": ("Courier New", 18)}
        
        self.explorer_act_btn = ctk.CTkButton(self.activity_bar, text="📁", command=lambda: self.switch_sidebar_panel("explorer"), **act_btn_style)
        self.explorer_act_btn.pack(pady=10, padx=4)
        
        self.search_act_btn = ctk.CTkButton(self.activity_bar, text="🔍", command=lambda: self.switch_sidebar_panel("search"), **act_btn_style)
        self.search_act_btn.pack(pady=5, padx=4)
        
        self.voice_act_btn = ctk.CTkButton(self.activity_bar, text="🎙️", command=lambda: self.switch_sidebar_panel("voice"), **act_btn_style)
        self.voice_act_btn.pack(pady=5, padx=4)
        
        # Settings button sits at the bottom of activity bar
        self.settings_act_btn = ctk.CTkButton(self.activity_bar, text="⚙️", command=lambda: self.switch_sidebar_panel("settings"), **act_btn_style)
        self.settings_act_btn.pack(side="bottom", pady=15, padx=4)
        
        # 2. Sidebar Container (250px middle pane)
        self.sidebar = ctk.CTkFrame(self.master_container, width=250, fg_color=self.theme_colors["sidebar"], border_width=1, border_color="#303030")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Initialize sidebar panel containers
        self.explorer_panel = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.search_panel = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.voice_panel = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.settings_panel = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        self.build_explorer_panel()
        self.build_search_panel()
        self.build_voice_panel()
        self.build_settings_panel()
        
        # Show default explorer panel
        self.switch_sidebar_panel("explorer")
        
        # 3. Work Area (Right container for editor, tabs, bottom panels, status bar)
        self.work_area = ctk.CTkFrame(self.master_container, fg_color="transparent")
        self.work_area.pack(side="right", fill="both", expand=True)
        
        # 3.1 Top Tab Bar Frame
        self.top_strip = ctk.CTkFrame(self.work_area, fg_color=self.theme_colors["sidebar"], height=35)
        self.top_strip.pack(fill="x", side="top")
        
        self.tab_bar = ctk.CTkFrame(self.top_strip, fg_color="transparent")
        self.tab_bar.pack(side="left", fill="both", expand=True, padx=2)
        
        # Quick Action Buttons on right side of Tab bar
        run_btn = ctk.CTkButton(self.top_strip, text="▶ Run", width=55, height=26, fg_color="#1d5a2d", hover_color="#2d7a3d", font=("Courier New", 10, "bold"), command=self._run_code)
        run_btn.pack(side="right", padx=5, pady=4)
        
        ai_fix_btn = ctk.CTkButton(self.top_strip, text="⚡ AI Fix", width=60, height=26, fg_color="#5a1d5a", hover_color="#7a2d7a", font=("Courier New", 10, "bold"), command=self._ai_fix)
        ai_fix_btn.pack(side="right", padx=3, pady=4)
        
        save_btn = ctk.CTkButton(self.top_strip, text="💾 Save", width=55, height=26, fg_color="#1d405a", hover_color="#2d5a7a", font=("Courier New", 10, "bold"), command=self._save_file)
        save_btn.pack(side="right", padx=3, pady=4)
        
        new_btn = ctk.CTkButton(self.top_strip, text="➕", width=26, height=26, fg_color="transparent", text_color="#d4d4d4", hover_color="#303030", font=("Courier New", 13, "bold"), command=self.new_empty_tab)
        new_btn.pack(side="right", padx=3, pady=4)
        
        self.file_label = ctk.CTkLabel(self.top_strip, text="📄 Untitled", font=("Courier New", 11), text_color="#888888")
        self.file_label.pack(side="right", padx=10)
        
        # 3.2 Editor Container Pane
        self.editor_container = ctk.CTkFrame(self.work_area, fg_color=self.theme_colors["bg"], border_width=1, border_color="#303030")
        self.editor_container.pack(fill="both", expand=True)

        # Build Placeholder Frame (for 0 tabs state)
        self.placeholder_frame = ctk.CTkFrame(self.editor_container, fg_color=self.theme_colors["bg"])
        ctk.CTkLabel(self.placeholder_frame, text="🤖", font=("Courier New", 50)).pack(pady=(100, 10))
        ctk.CTkLabel(self.placeholder_frame, text="ANTIGRAVITY IDE", font=("Courier New", 22, "bold"), text_color=self.theme_colors["fg"]).pack(pady=5)
        ctk.CTkLabel(self.placeholder_frame, text="Powered by JARVIS AI | Elite Decision & Coding Agent", font=("Courier New", 12), text_color="#888888").pack(pady=5)
        
        # Shortcuts
        sh_frame = ctk.CTkFrame(self.placeholder_frame, fg_color="transparent")
        sh_frame.pack(pady=30)
        shortcuts = [
            ("New File", "Ctrl + N"),
            ("Open File", "Ctrl + O"),
            ("Toggle Sidebar", "Ctrl + B"),
            ("Run Code", "F5")
        ]
        for name, key in shortcuts:
            row_f = ctk.CTkFrame(sh_frame, fg_color="transparent")
            row_f.pack(fill="x", pady=3)
            ctk.CTkLabel(row_f, text=f"{name:.<22}", font=("Consolas", 12), text_color="#666666").pack(side="left")
            ctk.CTkLabel(row_f, text=key, font=("Consolas", 12, "bold"), text_color=self.theme_colors.get("keyword", "#569cd6")).pack(side="right")
            
        ctk.CTkButton(self.placeholder_frame, text="Create New Tab", width=140, fg_color=self.theme_colors["sel"], font=("Courier New", 11, "bold"), command=self.new_empty_tab).pack(pady=10)
        
        # 3.3 Bottom Tabs Console View
        self.bottom_tabs = ctk.CTkTabview(self.work_area, height=240, fg_color="#000000",
                                          segmented_button_selected_color=self.theme_colors["sel"],
                                          segmented_button_unselected_color=self.theme_colors["sidebar"],
                                          text_color=self.theme_colors["fg"])
        self.bottom_tabs.pack(fill="x", side="bottom")
        
        self.bottom_tabs.add("Terminal")
        self.bottom_tabs.add("Problems")
        self.bottom_tabs.add("AI Assistant")
        
        # Problems Tab
        problems_tab = self.bottom_tabs.tab("Problems")
        problems_tab.configure(fg_color="#000000")
        self.inspector_scroll = ctk.CTkScrollableFrame(problems_tab, fg_color="#000000", scrollbar_button_color="#303030")
        self.inspector_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        self.clear_problems_ui()
        
        # Terminal Tab
        terminal_tab = self.bottom_tabs.tab("Terminal")
        terminal_tab.configure(fg_color="#000000")
        self.terminal = TerminalEmulator(terminal_tab, self.theme_colors)
        self.terminal.pack(fill="both", expand=True)
        
        # AI Assistant Tab  ── UPGRADED: Live Agent Mode
        ai_tab = self.bottom_tabs.tab("AI Assistant")
        ai_tab.configure(fg_color="#000000")

        ai_layout = ctk.CTkFrame(ai_tab, fg_color="transparent")
        ai_layout.pack(fill="both", expand=True, padx=5, pady=5)

        # ── Agent Mode toolbar ──
        agent_toolbar = ctk.CTkFrame(ai_layout, fg_color="#050d0d", height=34,
                                     border_width=1, border_color="#003322")
        agent_toolbar.pack(fill="x", pady=(0, 4))
        agent_toolbar.pack_propagate(False)

        ctk.CTkLabel(agent_toolbar, text="🤖 JARVIS AI AGENT",
                     font=("Courier New", 11, "bold"),
                     text_color="#00FFFE").pack(side="left", padx=10)

        # Agent Mode toggle
        self.agent_mode_var = ctk.BooleanVar(value=False)
        self._agent_mode_switch = ctk.CTkSwitch(
            agent_toolbar, text="🌐 Online Mode",
            font=("Courier New", 10, "bold"),
            variable=self.agent_mode_var, onvalue=True, offvalue=False,
            progress_color="#00cc44", button_color="#00FFFE",
            command=self._on_agent_mode_toggle
        )
        self._agent_mode_switch.pack(side="left", padx=15)

        # Status pill
        self.agent_status_lbl = ctk.CTkLabel(
            agent_toolbar, text="● Offline Mode",
            font=("Courier New", 10), text_color="#555555"
        )
        self.agent_status_lbl.pack(side="left", padx=5)

        # Quick web-search button
        self._web_search_btn = ctk.CTkButton(
            agent_toolbar, text="🔍 Web Search", width=90, height=24,
            fg_color="#003344", hover_color="#004455",
            font=("Courier New", 10, "bold"),
            command=self._agent_web_search
        )
        self._web_search_btn.pack(side="right", padx=8)

        # Clear AI output button
        ctk.CTkButton(
            agent_toolbar, text="🗑 Clear", width=60, height=24,
            fg_color="#330000", hover_color="#550000",
            font=("Courier New", 10, "bold"),
            command=lambda: self.ai_output.delete("1.0", "end")
        ).pack(side="right", padx=3)

        # ── AI output area ──
        self.ai_output = ctk.CTkTextbox(
            ai_layout, font=("Consolas", 12),
            fg_color="#000000", text_color="#d4d4d4"
        )
        self.ai_output.pack(fill="both", expand=True, pady=(0, 5))

        # ── Input bar ──
        ai_prompt_frame = ctk.CTkFrame(ai_layout, fg_color="transparent")
        ai_prompt_frame.pack(fill="x")

        self.ai_input = ctk.CTkEntry(
            ai_prompt_frame,
            placeholder_text="Ask JARVIS anything — code, web, news, knowledge...",
            fg_color="#000000", border_color="#003322"
        )
        self.ai_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.ai_input.bind("<Return>", lambda e: self._ai_ask())

        ai_send = ctk.CTkButton(
            ai_prompt_frame, text="⚡ Ask JARVIS", width=110,
            fg_color="#004400", hover_color="#006600",
            font=("Courier New", 10, "bold"),
            command=self._ai_ask
        )
        ai_send.pack(side="right")

        self.ai_mic_btn = ctk.CTkButton(
            ai_prompt_frame, text="🎤", width=40,
            fg_color="#181818", hover_color="#303030",
            font=("Courier New", 14),
            command=self._ai_toggle_mic
        )
        self.ai_mic_btn.pack(side="right", padx=(0, 5))

        # Initialise agent instance (lazy — created on first use)
        self._web_agent = None
        
        # 3.4 Status Bar (Bottom-most strip)
        self.status_bar = ctk.CTkFrame(self.work_area, height=22, fg_color=self.theme_colors["status"])
        self.status_bar.pack(fill="x", side="bottom")
        
        # Left status (Voice status, Telemetry)
        self.voice_status_lbl = ctk.CTkLabel(self.status_bar, text="🎙️ Off", font=("Courier New", 10, "bold"), text_color="#ffffff")
        self.voice_status_lbl.pack(side="left", padx=10)
        
        self.telemetry_lbl = ctk.CTkLabel(self.status_bar, text="CPU: 0% | RAM: 0%", font=("Courier New", 10), text_color="#ffffff")
        self.telemetry_lbl.pack(side="left", padx=15)
        
        # Right status (Line details, Spaces, Language)
        self.lang_status_lbl = ctk.CTkLabel(self.status_bar, text="Python", font=("Courier New", 10), text_color="#ffffff")
        self.lang_status_lbl.pack(side="right", padx=10)
        
        self.spaces_status_lbl = ctk.CTkLabel(self.status_bar, text="Spaces: 4", font=("Courier New", 10), text_color="#ffffff")
        self.spaces_status_lbl.pack(side="right", padx=10)
        
        self.pos_status_lbl = ctk.CTkLabel(self.status_bar, text="Ln 1, Col 1", font=("Courier New", 10), text_color="#ffffff")
        self.pos_status_lbl.pack(side="right", padx=15)

        # Global bindings
        self.bind("<Control-n>", lambda e: self.new_empty_tab())
        self.bind("<Control-w>", lambda e: self.close_active_tab())
        self.bind("<Control-b>", lambda e: self.toggle_sidebar())
        self.bind("<Control-s>", lambda e: self._save_file())
        self.bind("<Control-o>", lambda e: self._open_file())
        self.bind("<Control-f>", lambda e: self.switch_sidebar_panel("search"))
        self.bind("<F5>", lambda e: self._run_code())
        self.bind("<Control-g>", self.focus_ai_assistant)

    # ── Sidebar panel Builders ──────────────────────────────────────────
    def switch_sidebar_panel(self, panel_name):
        # Clear existing active frames
        self.explorer_panel.pack_forget()
        self.search_panel.pack_forget()
        self.voice_panel.pack_forget()
        self.settings_panel.pack_forget()
        
        # Reset Activity button background colors
        self.explorer_act_btn.configure(fg_color="transparent")
        self.search_act_btn.configure(fg_color="transparent")
        self.voice_act_btn.configure(fg_color="transparent")
        self.settings_act_btn.configure(fg_color="transparent")
        
        # Switch panel and highlight active icon
        if panel_name == "explorer":
            self.explorer_panel.pack(fill="both", expand=True, padx=5, pady=5)
            self.explorer_act_btn.configure(fg_color="#404040")
        elif panel_name == "search":
            self.search_panel.pack(fill="both", expand=True, padx=10, pady=5)
            self.search_act_btn.configure(fg_color="#404040")
        elif panel_name == "voice":
            self.voice_panel.pack(fill="both", expand=True, padx=10, pady=5)
            self.voice_act_btn.configure(fg_color="#404040")
        elif panel_name == "settings":
            self.settings_panel.pack(fill="both", expand=True, padx=10, pady=5)
            self.settings_act_btn.configure(fg_color="#404040")
            
        self.active_sidebar_panel = panel_name
        
        # Expand sidebar if collapsed
        if not self.sidebar_expanded:
            self.toggle_sidebar()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.pack_forget()
            self.sidebar_expanded = False
        else:
            self.sidebar.pack(side="left", fill="y", after=self.activity_bar)
            self.sidebar_expanded = True

    def build_explorer_panel(self):
        """Builds file tree panel"""
        hdr = ctk.CTkFrame(self.explorer_panel, fg_color="transparent")
        hdr.pack(fill="x", padx=5, pady=5)
        
        self.explorer_title = ctk.CTkLabel(hdr, text="📁 WORKSPACE", font=("Courier New", 12, "bold"), text_color=self.theme_colors["fg"])
        self.explorer_title.pack(side="left", fill="x", expand=True, anchor="w")
        
        # Actions
        ctk.CTkButton(hdr, text="📄", width=22, height=22, fg_color="transparent", text_color="#d4d4d4", hover_color="#303030", command=lambda: self._tree_new_file(self.workspace_dir, "dir")).pack(side="right", padx=1)
        ctk.CTkButton(hdr, text="📁", width=22, height=22, fg_color="transparent", text_color="#d4d4d4", hover_color="#303030", command=lambda: self._tree_new_folder(self.workspace_dir, "dir")).pack(side="right", padx=1)
        ctk.CTkButton(hdr, text="🔄", width=22, height=22, fg_color="transparent", text_color="#d4d4d4", hover_color="#303030", command=self._refresh_tree).pack(side="right", padx=1)
        
        # Style treeview
        self.tree_style = ttk.Style()
        self.tree_style.theme_use("clam")
        self.tree_style.configure("Studio.Treeview",
                                  background=self.theme_colors["sidebar"],
                                  foreground=self.theme_colors["fg"],
                                  rowheight=22,
                                  fieldbackground=self.theme_colors["sidebar"],
                                  font=("Courier New", 10),
                                  bordercolor="#202020",
                                  borderwidth=0)
        self.tree_style.map("Studio.Treeview",
                             background=[("selected", self.theme_colors["sel"])],
                             foreground=[("selected", "#ffffff")])
        
        self.tree = ttk.Treeview(self.explorer_panel, style="Studio.Treeview", show="tree")
        self.tree.pack(side="left", fill="both", expand=True)
        
        tree_scroll = ctk.CTkScrollbar(self.explorer_panel, command=self.tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.bind("<<TreeviewOpen>>", self._on_tree_open)
        self.tree.bind("<Double-Button-1>", self._on_tree_double_click)
        self.tree.bind("<Button-3>", self._show_tree_context_menu)

    def build_search_panel(self):
        """Builds text search and replace panel"""
        ctk.CTkLabel(self.search_panel, text="🔍 SEARCH & REPLACE", font=("Courier New", 12, "bold"), text_color=self.theme_colors["fg"]).pack(anchor="w", pady=(5, 10))
        
        ctk.CTkLabel(self.search_panel, text="Find text:", font=("Courier New", 10)).pack(anchor="w")
        self.search_find_entry = ctk.CTkEntry(self.search_panel, fg_color="#000000")
        self.search_find_entry.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.search_panel, text="Replace with:", font=("Courier New", 10)).pack(anchor="w", pady=(5, 0))
        self.search_replace_entry = ctk.CTkEntry(self.search_panel, fg_color="#000000")
        self.search_replace_entry.pack(fill="x", pady=5)
        
        btn_frame = ctk.CTkFrame(self.search_panel, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        find_all_btn = ctk.CTkButton(btn_frame, text="Find All", fg_color="#1d405a", hover_color="#2d5a7a", width=100, command=self.find_text_all)
        find_all_btn.pack(side="left", padx=(0, 5))
        
        rep_all_btn = ctk.CTkButton(btn_frame, text="Replace All", fg_color="#1d5a2d", hover_color="#2d7a3d", width=100, command=self.replace_text_all)
        rep_all_btn.pack(side="right")

    def build_voice_panel(self):
        """Builds voice control panel"""
        ctk.CTkLabel(self.voice_panel, text="🎙️ JARVIS VOICE CONTROL", font=("Courier New", 12, "bold"), text_color=self.theme_colors["fg"]).pack(anchor="w", pady=(5, 10))
        
        # Mic Activate Switch
        self.voice_switch_var = ctk.BooleanVar(value=False)
        self.voice_switch = ctk.CTkSwitch(self.voice_panel, text="Speech Activation", font=("Courier New", 11),
                                           variable=self.voice_switch_var, onvalue=True, offvalue=False,
                                           command=self.toggle_speech_engine)
        self.voice_switch.pack(anchor="w", pady=10)
        
        ctk.CTkLabel(self.voice_panel, text="Log Console:", font=("Courier New", 10)).pack(anchor="w")
        self.voice_logs = ctk.CTkTextbox(self.voice_panel, font=("Consolas", 10), fg_color="#000000", text_color="#00ff00", height=150)
        self.voice_logs.pack(fill="x", pady=5)
        
        # Command Cheat Sheet list
        lbl = ctk.CTkLabel(self.voice_panel, text="Voice Commands List:\n• 'jarvis run' - Run script\n• 'jarvis save' - Save file\n• 'jarvis new file' - New Tab\n• 'jarvis explain' - AI Explain\n• 'jarvis fix' - AI Bug Fix\n• 'jarvis toggle' - Collapse Sidebar\n• 'jarvis clear' - Clear terminal",
                            font=("Courier New", 10), justify="left", anchor="w")
        lbl.pack(fill="x", pady=10)

    def build_settings_panel(self):
        """Builds settings panel"""
        ctk.CTkLabel(self.settings_panel, text="⚙️ EDITOR SETTINGS", font=("Courier New", 12, "bold"), text_color=self.theme_colors["fg"]).pack(anchor="w", pady=(5, 10))
        
        # Theme Choice
        ctk.CTkLabel(self.settings_panel, text="Select Theme:", font=("Courier New", 10)).pack(anchor="w")
        self.setting_theme_var = ctk.StringVar(value=self.current_theme)
        theme_menu = ctk.CTkOptionMenu(self.settings_panel, values=list(THEMES.keys()), variable=self.setting_theme_var, command=self._apply_theme)
        theme_menu.pack(fill="x", pady=5)
        
        # Font family Choice
        ctk.CTkLabel(self.settings_panel, text="Font Family:", font=("Courier New", 10)).pack(anchor="w", pady=(5, 0))
        self.setting_font_var = ctk.StringVar(value=self.settings.get("font_family"))
        font_menu = ctk.CTkOptionMenu(self.settings_panel, values=["Consolas", "Courier New", "Fira Code"], variable=self.setting_font_var, command=self.change_font_family)
        font_menu.pack(fill="x", pady=5)
        
        # Font size Choice
        ctk.CTkLabel(self.settings_panel, text="Font Size:", font=("Courier New", 10)).pack(anchor="w", pady=(5, 0))
        self.setting_fontsize_var = ctk.StringVar(value=str(self.settings.get("font_size")))
        font_size_menu = ctk.CTkOptionMenu(self.settings_panel, values=["10", "11", "12", "13", "14", "16", "18", "20"], variable=self.setting_fontsize_var, command=lambda v: self._change_font_size_direct(int(v)))
        font_size_menu.pack(fill="x", pady=5)
        
        # Word Wrap toggle
        self.setting_wrap_var = ctk.BooleanVar(value=self.settings.get("word_wrap"))
        wrap_sw = ctk.CTkSwitch(self.settings_panel, text="Enable Word Wrap", font=("Courier New", 11),
                                variable=self.setting_wrap_var, onvalue=True, offvalue=False,
                                command=self.toggle_word_wrap)
        wrap_sw.pack(anchor="w", pady=10)
        
        # Auto save toggle
        self.setting_autosave_var = ctk.BooleanVar(value=self.settings.get("auto_save"))
        save_sw = ctk.CTkSwitch(self.settings_panel, text="Enable Auto Save (2s delay)", font=("Courier New", 11),
                                variable=self.setting_autosave_var, onvalue=True, offvalue=False,
                                command=self.toggle_auto_save)
        save_sw.pack(anchor="w", pady=5)

    # ── Workspace tree functions ──────────────────────────────────────────
    def _choose_workspace(self):
        path = filedialog.askdirectory(title="Open Workspace Directory")
        if path:
            self._load_workspace(path)

    def _load_workspace(self, path):
        self.workspace_dir = os.path.abspath(path)
        self.explorer_title.configure(text=f"📁 {os.path.basename(path).upper()}")
        self._refresh_tree()

    def _refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.workspace_dir and os.path.exists(self.workspace_dir):
            self._add_to_tree("", self.workspace_dir)

    def _add_to_tree(self, parent_node, path):
        try:
            items = os.listdir(path)
            folders = []
            files = []
            for item in items:
                if item.startswith('.') or item == '__pycache__':
                    continue
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    folders.append(item)
                else:
                    files.append(item)
            
            folders.sort()
            files.sort()
            
            for folder in folders:
                folder_path = os.path.join(path, folder)
                node = self.tree.insert(parent_node, "end", text=f"📁 {folder}", values=(folder_path, "dir"), open=False)
                self.tree.insert(node, "end", text="dummy")
                
            for file in files:
                file_path = os.path.join(path, file)
                icon = "📄 "
                if file.endswith(".py"):
                    icon = "🐍 "
                elif file.endswith(".html") or file.endswith(".htm"):
                    icon = "🌐 "
                elif file.endswith(".js") or file.endswith(".ts"):
                    icon = "⚡ "
                elif file.endswith(".json") or file.endswith(".yaml") or file.endswith(".yml"):
                    icon = "⚙️ "
                elif file.endswith(".md") or file.endswith(".txt"):
                    icon = "📝 "
                self.tree.insert(parent_node, "end", text=f"{icon}{file}", values=(file_path, "file"))
        except Exception as e:
            print(f"Error loading tree items: {e}")

    def _on_tree_open(self, event):
        item = self.tree.focus()
        values = self.tree.item(item, "values")
        if values and values[1] == "dir":
            dir_path = values[0]
            for child in self.tree.get_children(item):
                self.tree.delete(child)
            self._add_to_tree(item, dir_path)

    def _on_tree_double_click(self, event):
        item = self.tree.focus()
        values = self.tree.item(item, "values")
        if values and values[1] == "file":
            file_path = values[0]
            self.open_file_by_path(file_path)

    def _show_tree_context_menu(self, event):
        iid = self.tree.identify_row(event.y)
        menu = tk.Menu(self, tearoff=0, bg=self.theme_colors["sidebar"], fg=self.theme_colors["fg"], 
                       activebackground=self.theme_colors["sel"], activeforeground="#ffffff", borderwidth=1)
        
        if iid:
            self.tree.selection_set(iid)
            self.tree.focus(iid)
            values = self.tree.item(iid, "values")
            if values:
                path, item_type = values[0], values[1]
                menu.add_command(label="📄 New File", command=lambda: self._tree_new_file(path, item_type))
                menu.add_command(label="📁 New Folder", command=lambda: self._tree_new_folder(path, item_type))
                menu.add_separator()
                menu.add_command(label="✏️ Rename", command=lambda: self._tree_rename(iid, path))
                menu.add_command(label="❌ Delete", command=lambda: self._tree_delete(iid, path))
                menu.add_separator()
                menu.add_command(label="📤 Upload File Here", command=lambda: self._tree_upload_file(path, item_type))
        else:
            menu.add_command(label="📄 New File at Root", command=lambda: self._tree_new_file(self.workspace_dir, "dir"))
            menu.add_command(label="📁 New Folder at Root", command=lambda: self._tree_new_folder(self.workspace_dir, "dir"))
            menu.add_separator()
            menu.add_command(label="🔄 Refresh Workspace", command=self._refresh_tree)
            
        menu.post(event.x_root, event.y_root)

    def _tree_new_file(self, target_path, item_type):
        dest_dir = target_path if item_type == "dir" else os.path.dirname(target_path)
        if not os.path.exists(dest_dir):
            dest_dir = self.workspace_dir
            
        dialog = CustomInputDialog(self, title="New File", prompt="Enter file name:", theme_colors=self.theme_colors)
        if dialog.result:
            file_name = dialog.result
            new_path = os.path.join(dest_dir, file_name)
            try:
                if os.path.exists(new_path):
                    messagebox.showerror("Error", f"File '{file_name}' already exists.")
                    return
                with open(new_path, "w", encoding="utf-8") as f:
                    f.write("")
                self._log_terminal(f"Created file: {new_path}\n")
                self._refresh_tree()
                self.open_file_by_path(new_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create file: {e}")

    def _tree_new_folder(self, target_path, item_type):
        dest_dir = target_path if item_type == "dir" else os.path.dirname(target_path)
        if not os.path.exists(dest_dir):
            dest_dir = self.workspace_dir
            
        dialog = CustomInputDialog(self, title="New Folder", prompt="Enter folder name:", theme_colors=self.theme_colors)
        if dialog.result:
            folder_name = dialog.result
            new_path = os.path.join(dest_dir, folder_name)
            try:
                if os.path.exists(new_path):
                    messagebox.showerror("Error", f"Folder '{folder_name}' already exists.")
                    return
                os.makedirs(new_path, exist_ok=True)
                self._log_terminal(f"Created folder: {new_path}\n")
                self._refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Could not create folder: {e}")

    def _tree_rename(self, iid, old_path):
        old_name = os.path.basename(old_path)
        dialog = CustomInputDialog(self, title="Rename", prompt=f"Rename '{old_name}' to:", initial_value=old_name, theme_colors=self.theme_colors)
        if dialog.result and dialog.result != old_name:
            new_name = dialog.result
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                if os.path.exists(new_path):
                    messagebox.showerror("Error", f"'{new_name}' already exists.")
                    return
                os.rename(old_path, new_path)
                self._log_terminal(f"Renamed: {old_name} -> {new_name}\n")
                
                for tab in self.tabs:
                    if tab.file_path and os.path.abspath(tab.file_path) == os.path.abspath(old_path):
                        tab.file_path = new_path
                        tab.name = new_name
                
                self._refresh_tree()
                self.update_tab_bar()
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename: {e}")

    def _tree_delete(self, iid, target_path):
        name = os.path.basename(target_path)
        is_dir = os.path.isdir(target_path)
        item_type = "folder" if is_dir else "file"
        
        if messagebox.askyesno("Confirm Delete", f"Delete {item_type} permanently: '{name}'?"):
            try:
                # Close associated tabs
                closed_tabs = []
                for tab in self.tabs:
                    if tab.file_path and os.path.abspath(tab.file_path) == os.path.abspath(target_path):
                        closed_tabs.append(tab)
                for tab in closed_tabs:
                    tab.frame.destroy()
                    self.tabs.remove(tab)
                
                if is_dir:
                    shutil.rmtree(target_path)
                else:
                    os.remove(target_path)
                
                self._log_terminal(f"Deleted: {target_path}\n")
                
                if self.active_tab in closed_tabs:
                    if self.tabs:
                        self.switch_to_tab(self.tabs[-1])
                    else:
                        self.active_tab = None
                        self.new_empty_tab()
                else:
                    self.update_tab_bar()
                
                self._refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete: {e}")

    def _tree_upload_file(self, target_path, item_type):
        dest_dir = target_path if item_type == "dir" else os.path.dirname(target_path)
        if not os.path.exists(dest_dir):
            dest_dir = self.workspace_dir
            
        file_paths = filedialog.askopenfilenames(title="Upload/Copy Files to Project")
        if file_paths:
            copied_count = 0
            for src_path in file_paths:
                try:
                    dest_path = os.path.join(dest_dir, os.path.basename(src_path))
                    if os.path.exists(dest_path):
                        if not messagebox.askyesno("Overwrite", f"'{os.path.basename(src_path)}' exists. Overwrite?"):
                            continue
                    shutil.copy(src_path, dest_path)
                    copied_count += 1
                except Exception as e:
                    self._log_terminal(f"Upload error: {e}\n")
            if copied_count > 0:
                self._log_terminal(f"Uploaded {copied_count} file(s) to workspace folder.\n")
                self._refresh_tree()

    # ── Editor Tab Management ───────────────────────────────────────────
    def new_empty_tab(self):
        new_tab = EditorTab(self.editor_container, file_path=None, studio=self)
        self.tabs.append(new_tab)
        self.switch_to_tab(new_tab)

    def open_file_by_path(self, path):
        path = os.path.abspath(path)
        for tab in self.tabs:
            if tab.file_path and os.path.abspath(tab.file_path) == path:
                self.switch_to_tab(tab)
                return
                
        new_tab = EditorTab(self.editor_container, file_path=path, studio=self)
        self.tabs.append(new_tab)
        self.switch_to_tab(new_tab)

    def switch_to_tab(self, tab):
        if self.active_tab:
            self.active_tab.frame.pack_forget()
            
        self.active_tab = tab
        tab.frame.pack(fill="both", expand=True)
        
        if tab.file_path:
            self.file_label.configure(text=f"📄 {tab.name}")
            ext = os.path.splitext(tab.file_path)[1]
            found_lang = "Text"
            for lang, info in LANGUAGES.items():
                if info["ext"].lower() == ext.lower():
                    found_lang = lang
                    break
            self.lang_status_lbl.configure(text=found_lang)
            self.current_lang = found_lang
        else:
            self.file_label.configure(text="📄 Untitled")
            self.current_lang = "Python"
            self.lang_status_lbl.configure(text="Python")
            
        self.update_tab_bar()
        self._update_status()
        tab.editor.focus_set()
        tab.line_numbers.redraw()

    def close_active_tab(self):
        if self.active_tab:
            self.close_tab(self.active_tab)

    def close_tab(self, tab):
        if tab.is_modified:
            ans = messagebox.askyesnocancel("Unsaved Changes", f"Save changes to {tab.name}?")
            if ans is True:
                self.switch_to_tab(tab)
                self._save_file()
            elif ans is None:
                return
                
        tab.frame.destroy()
        if tab in self.tabs:
            self.tabs.remove(tab)
        
        if self.active_tab == tab:
            if self.tabs:
                self.switch_to_tab(self.tabs[-1])
            else:
                self.active_tab = None
                self.file_label.configure(text="No File Open")
                self.lang_status_lbl.configure(text="")
                self.current_lang = ""
                self.update_tab_bar()
                self._update_status()
        else:
            self.update_tab_bar()

    def update_tab_bar(self):
        for widget in self.tab_bar.winfo_children():
            widget.destroy()
            
        for tab in self.tabs:
            is_active = (tab == self.active_tab)
            bg_color = self.theme_colors["bg"] if is_active else self.theme_colors["sidebar"]
            text_color = self.theme_colors["fg"] if is_active else "#888888"
            
            tab_frame = ctk.CTkFrame(self.tab_bar, fg_color=bg_color, corner_radius=4, height=30)
            tab_frame.pack(side="left", padx=2, pady=2)
            
            mark = "* " if tab.is_modified else ""
            
            btn = ctk.CTkButton(tab_frame, text=f"{mark}{tab.name}", 
                                fg_color="transparent", hover_color="#404040",
                                text_color=text_color,
                                font=("Courier New", 11, "bold" if is_active else "normal"),
                                width=100, height=26,
                                command=lambda t=tab: self.switch_to_tab(t))
            btn.pack(side="left", padx=(5, 2))
            
            close_btn = ctk.CTkButton(tab_frame, text="×", 
                                      fg_color="transparent", hover_color="#8a1d1d",
                                      text_color=text_color,
                                      font=("Courier New", 12, "bold"),
                                      width=16, height=26,
                                      command=lambda t=tab: self.close_tab(t))
            close_btn.pack(side="left", padx=(2, 5))

    # ── Editor keyboard / interactive handlers ───────────────────────────
    def _on_key_press(self, event):
        if not self.active_tab:
            return
        char = event.char
        if char in ['(', '[', '{', '"', "'"]:
            pairs = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}
            self.active_tab.editor.insert("insert", pairs[char])
            self.active_tab.editor.mark_set("insert", "insert-1c")

    def focus_ai_assistant(self, event=None):
        try:
            self.bottom_tabs.set("AI Assistant")
            self.ai_input.focus_set()
        except Exception as e:
            print(f"Error focusing AI Assistant: {e}")

    def _on_enter(self, event):
        if not self.active_tab:
            return "break"
        editor = self.active_tab.editor
        curr_index = editor.index("insert")
        line_start = curr_index.split(".")[0] + ".0"
        line_text = editor.get(line_start, "insert")
        
        whitespace = ""
        for c in line_text:
            if c in [' ', '\t']:
                whitespace += c
            else:
                break
                
        if line_text.strip().endswith(':'):
            whitespace += "    "
            
        editor.insert("insert", "\n" + whitespace)
        self.active_tab.line_numbers.redraw()
        return "break"

    def _on_zoom(self, event):
        if event.delta > 0:
            self._change_font_size(1)
        else:
            self._change_font_size(-1)

    def _change_font_size(self, delta):
        if not self.active_tab:
            return
        size = self.settings.get("font_size")
        new_size = max(8, min(40, size + delta))
        self._change_font_size_direct(new_size)

    def _change_font_size_direct(self, size):
        self.settings.set("font_size", size)
        self.setting_fontsize_var.set(str(size))
        
        for tab in self.tabs:
            tab.editor.configure(font=(self.settings.get("font_family"), size))
            tab.line_numbers.redraw()

    def change_font_family(self, font):
        self.settings.set("font_family", font)
        for tab in self.tabs:
            tab.editor.configure(font=(font, self.settings.get("font_size")))
            tab.line_numbers.redraw()

    def toggle_word_wrap(self):
        wrap = self.setting_wrap_var.get()
        self.settings.set("word_wrap", wrap)
        wrap_val = "word" if wrap else "none"
        for tab in self.tabs:
            tab.editor.configure(wrap=wrap_val)
            tab.line_numbers.redraw()

    def toggle_auto_save(self):
        self.settings.set("auto_save", self.setting_autosave_var.get())

    # ── Text Find & Replace Panel execution ──────────────────────────────
    def find_text_all(self):
        if not self.active_tab:
            return
        editor = self.active_tab.editor
        query = self.search_find_entry.get().strip()
        editor.tag_remove("match", "1.0", "end")
        if query:
            idx = "1.0"
            count = 0
            while True:
                idx = editor.search(query, idx, nocase=True, stopindex="end")
                if not idx:
                    break
                lastidx = f"{idx}+{len(query)}c"
                editor.tag_add("match", idx, lastidx)
                idx = lastidx
                count += 1
            editor.tag_configure("match", background=self.theme_colors["sel"], foreground="#ffffff")
            self._log_terminal(f"Search results: Found {count} match(es) for '{query}'\n")

    def replace_text_all(self):
        if not self.active_tab:
            return
        editor = self.active_tab.editor
        query = self.search_find_entry.get().strip()
        rep = self.search_replace_entry.get()
        if query:
            content = editor.get("1.0", "end-1c")
            new_content = content.replace(query, rep)
            editor.delete("1.0", "end")
            editor.insert("1.0", new_content)
            self.highlight_syntax(editor)
            self._log_terminal(f"Replaced matches of '{query}' with '{rep}'\n")

    # ── File Operations ──────────────────────────────────────────────────
    def _open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("All files", "*.*"), ("Python", "*.py"),
                       ("JavaScript", "*.js"), ("HTML", "*.html")]
        )
        if path:
            self.open_file_by_path(path)

    def _save_file(self):
        if not self.active_tab:
            return
            
        tab = self.active_tab
        if tab.file_path:
            try:
                content = tab.editor.get("1.0", "end-1c")
                with open(tab.file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                tab.is_modified = False
                self.update_tab_bar()
                self._log_terminal(f"Saved: {tab.file_path}\n")
            except Exception as e:
                self._log_terminal(f"Save error: {e}\n")
        else:
            self._save_as()

    def _save_as(self):
        if not self.active_tab:
            return
            
        tab = self.active_tab
        ext = LANGUAGES.get(self.current_lang, {"ext": ".txt"})["ext"]
        path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[("Current language", f"*{ext}"), ("All files", "*.*")]
        )
        if path:
            tab.file_path = path
            tab.name = os.path.basename(path)
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(tab.editor.get("1.0", "end-1c"))
                tab.is_modified = False
                self.update_tab_bar()
                self._log_terminal(f"Saved As: {path}\n")
                self._refresh_tree()
            except Exception as e:
                self._log_terminal(f"Save error: {e}\n")

    def _run_code(self):
        if not self.active_tab:
            return
        code = self.active_tab.editor.get("1.0", "end-1c")
        if not code.strip():
            return

        self._log_terminal(f"Executing script runner: {self.current_lang}...\n" + "─" * 50 + "\n")

        def _exec():
            try:
                lang = self.current_lang
                if lang == "Python":
                    tmp = os.path.join(_BASE, "jarvis_temp", "_code_tmp.py")
                    os.makedirs(os.path.dirname(tmp), exist_ok=True)
                    with open(tmp, "w", encoding="utf-8") as f:
                        f.write(code)
                    result = subprocess.run(
                        ["python", tmp],
                        capture_output=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=30, cwd=_BASE
                    )
                    out = result.stdout + result.stderr
                    self.after(0, lambda: self._log_terminal(out or "Execution completed with no outputs.\n"))
                elif lang == "HTML":
                    tmp = os.path.join(_BASE, "jarvis_temp", "_code_tmp.html")
                    os.makedirs(os.path.dirname(tmp), exist_ok=True)
                    with open(tmp, "w", encoding="utf-8") as f:
                        f.write(code)
                    os.startfile(tmp)
                    self.after(0, lambda: self._log_terminal("Launched HTML in default Web Browser.\n"))
                else:
                    self.after(0, lambda: self._log_terminal(
                        f"Unsupported language runner: {lang}. Save and run via console tab.\n"))
            except subprocess.TimeoutExpired:
                self.after(0, lambda: self._log_terminal("Timeout error: script execution took longer than 30s limit.\n"))
            except Exception as e:
                self.after(0, lambda: self._log_terminal(f"Error: {e}\n"))

        threading.Thread(target=_exec, daemon=True).start()

    # ── AI Code assistants helper ─────────────────────────────────────────
    def _on_agent_mode_toggle(self):
        """Called when the Online Mode switch is toggled."""
        if self.agent_mode_var.get():
            self.agent_status_lbl.configure(
                text="● Online — Web Search ACTIVE", text_color="#00cc44"
            )
            self._ai_log("🌐 [AGENT MODE: ON] JARVIS now has live internet access.\n"
                         "All queries will include real-time web knowledge.\n\n")
            self.voice_engine.speak("Online agent mode activated. I now have live internet access, sir.")
        else:
            self.agent_status_lbl.configure(
                text="● Offline Mode", text_color="#555555"
            )
            self._ai_log("🔒 [AGENT MODE: OFF] Offline mode — using base AI only.\n\n")

    def _get_web_agent(self):
        """Lazy-initialise and return the JarvisWebAgent singleton."""
        if self._web_agent is None and WEB_AGENT_AVAILABLE:
            self._web_agent = get_web_agent(log_callback=lambda m: self.after(0, self._ai_log, f"[WebAgent] {m}\n"))
        return self._web_agent

    def _agent_web_search(self):
        """Standalone quick web search from the toolbar search button."""
        question = self.ai_input.get().strip()
        if not question:
            # Prompt for a search term
            self._ai_log("🔍 Type a search query in the input box first.\n")
            self.ai_input.focus_set()
            return
        self.ai_input.delete(0, "end")
        self._ai_log(f"🔍 Searching the web for: '{question}'...\n")
        agent = self._get_web_agent()
        if not agent:
            self._ai_log("❌ Web agent is not available. Check engine/jarvis_web_agent.py.\n")
            return

        def _on_result(web_ctx: str):
            self.after(0, self._ai_log, web_ctx + "\n\n")

        agent.search_threaded(question, callback=_on_result)

    def _get_combined_context(self):
        if not self.tabs:
            return ""
        context_parts = []
        for tab in self.tabs:
            file_name = tab.name
            file_path = tab.file_path or "Untitled"
            is_active = " (Active)" if tab == self.active_tab else ""
            content = tab.editor.get("1.0", "end-1c").strip()
            
            # Take full content (large context window supported by modern Gemini)
            context_parts.append(
                f"--- FILE: {file_name} [{file_path}]{is_active} ---\n"
                f"{content}\n"
                f"----------------------------------------"
            )
        return "\n\n".join(context_parts)

    def _speak_summary(self, text):
        if not VOICE_AVAILABLE or not self.voice_engine.enabled:
            return
        import re
        clean = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        clean = re.sub(r'`[^`]+`', '', clean)
        clean = re.sub(r'[#*_\-]', '', clean)
        sentences = [s.strip() for s in re.split(r'[.!?।]', clean) if s.strip()]
        summary = " ".join(sentences[:2])
        if not summary.strip():
            summary = "Analysis complete, sir."
        if len(summary) > 200:
            summary = summary[:197] + "..."
        self.voice_engine.speak(summary)

    def _ai_toggle_mic(self):
        if not VOICE_AVAILABLE or not self.voice_engine.enabled:
            self._ai_log("⚠️ Voice assistant is not available or microphone is disabled.\n")
            return
        if getattr(self, '_ai_prompt_listening', False):
            return
        self._ai_prompt_listening = True

        def _listen_thread():
            was_bg_listening = self.voice_engine.listening
            if was_bg_listening:
                self.voice_engine.stop_listening()
            self.gui_queue.put(('mic_status', 'listening'))
            try:
                if not getattr(self.voice_engine, '_calibrated', False):
                    self.gui_queue.put(('log', "🎙️ Calibrating microphone for ambient noise...\n"))
                    if getattr(self.voice_engine, '_use_multilang', False) and hasattr(self.voice_engine, '_mlv'):
                        self.voice_engine._mlv.calibrate(duration=0.8)
                    else:
                        with self.voice_engine.microphone as source:
                            self.voice_engine.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                    self.voice_engine._calibrated = True
                    self.gui_queue.put(('log', f"🎤 Calibrated. Energy threshold: {self.voice_engine.recognizer.energy_threshold:.0f}\n"))
                
                self.gui_queue.put(('log', "🎙️ JARVIS is listening to your prompt...\n"))
                self.voice_engine.speak("Listening, sir.")
                with self.voice_engine.microphone as source:
                    audio = self.voice_engine.recognizer.listen(source, timeout=6, phrase_time_limit=12)
                
                self.gui_queue.put(('mic_status', 'processing'))
                self.gui_queue.put(('log', "🎙️ Analyzing speech...\n"))
                statement = None
                if getattr(self.voice_engine, '_use_multilang', False) and hasattr(self.voice_engine, '_mlv'):
                    langs = [self.voice_engine._mlv.preferred_lang] + self.voice_engine._mlv.fallback_langs
                else:
                    langs = ["bn-BD", "en-US"]
                for lang in langs:
                    try:
                        statement = self.voice_engine.recognizer.recognize_google(audio, language=lang).strip()
                        if statement:
                            break
                    except Exception:
                        continue
                if not statement:
                    try:
                        statement = self.voice_engine.recognizer.recognize_google(audio).strip()
                    except Exception:
                        pass
                if statement:
                    self.gui_queue.put(('mic_result', statement))
                else:
                    self.gui_queue.put(('log', "⚠️ Unrecognized voice prompt.\n"))
                    self.gui_queue.put(('mic_status', 'idle'))
            except Exception as e:
                self.gui_queue.put(('log', f"⚠️ Microphone error: {e}\n"))
                self.gui_queue.put(('mic_status', 'idle'))
            finally:
                self._ai_prompt_listening = False
                if was_bg_listening:
                    self.voice_engine.start_listening()

        threading.Thread(target=_listen_thread, daemon=True).start()

    def _ai_ask(self):
        question = self.ai_input.get().strip()
        if not question:
            return
        self.ai_input.delete(0, "end")
        code = self._get_combined_context()

        if self.agent_mode_var.get():
            # ── AGENT MODE: search web first, then call AI with enriched context
            self._agent_ask(question, code)
        else:
            # ── OFFLINE MODE: direct AI call with code context only
            prompt = ""
            if code.strip():
                prompt += f"Code context (All Open Tabs):\n{code}\n\n"
            prompt += f"Question: {question}"
            self._call_ai(prompt)

    def _agent_ask(self, question: str, code: str = ""):
        """
        Full agent pipeline:
          1. Search the web for context
          2. Combine web knowledge + code context
          3. Send enriched prompt to JARVIS brain (Gemini)
          4. Show synthesized answer
        """
        self._ai_log(f"🤖 JARVIS Agent thinking... | Query: {question}\n")
        self._ai_log("🌐 Step 1: Fetching live web knowledge...\n")
        self.voice_engine.speak("Searching the internet and processing your query, sir.")

        agent = self._get_web_agent()
        if not agent:
            # Fallback to normal AI if agent unavailable
            self._ai_log("⚠️ Web agent unavailable — falling back to offline AI.\n")
            prompt = ""
            if code.strip():
                prompt += f"Code context (All Open Tabs):\n{code}\n\n"
            prompt += f"Question: {question}"
            self._call_ai(prompt)
            return

        def _after_search(web_context: str):
            self.after(0, self._ai_log, "✅ Step 2: Web search complete. Sending to JARVIS AI...\n")
            # Build the enriched prompt
            enriched_prompt = (
                "You are JARVIS with LIVE INTERNET ACCESS. Below is real-time web knowledge "
                "retrieved just now. Use it to give an accurate, up-to-date answer.\n\n"
                f"{web_context}\n"
            )
            if code.strip():
                enriched_prompt += f"\nACTIVE CODE CONTEXT (All Open Tabs):\n{code}\n"
            enriched_prompt += f"\nUSER QUESTION: {question}\n"
            enriched_prompt += "\nPlease provide a comprehensive, up-to-date answer using the web data above."

            # Call AI with enriched context
            self.after(0, self._call_ai, enriched_prompt)

        agent.search_threaded(question, callback=_after_search, code_context=code)

    def _ai_fix(self):
        code = self._get_combined_context()
        if not code.strip():
            self._ai_log("⚠️ No code files are currently open to fix.\n")
            self.voice_engine.speak("There are no open code files to fix, sir.")
            return
        prompt = (
            "Please check and fix any bugs in these open files. "
            "Return the corrected versions of ONLY the files that need fixing. "
            "Use standard file blocks starting with '--- FILE: [filename] ---' "
            "so that changes can be mapped:\n\n"
            f"{code}"
        )
        self._call_ai(prompt, apply_to_editor=True)

    def _write_ide_state(self, state, last_response=None):
        try:
            state_file = os.path.join(_BASE, "jarvis_ide_state.json")
            data = {
                "state": state,
                "timestamp": time.time()
            }
            if last_response is not None:
                data["last_response"] = last_response
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error writing IDE state: {e}")

    def execute_ai_system_command(self, cmd):
        """Execute a system command generated by the AI model"""
        try:
            sys.path.insert(0, _BASE)
            import engine.automation as aut
            import engine.windows_control as wc
            clean_cmd = cmd.strip()
            
            # Check for mouse or keyboard actions
            if clean_cmd.startswith("mouse ") or clean_cmd.startswith("keyboard "):
                parts = clean_cmd.split(" ", 1)
                cmd_root = parts[0]
                cmd_args = parts[1] if len(parts) > 1 else ""
                
                sub_parts = cmd_args.strip().split(None, 1)
                sub_action = sub_parts[0].lower() if sub_parts else ""
                sub_text = sub_parts[1].strip() if len(sub_parts) > 1 else ""
                
                if cmd_root == "mouse":
                    sub_args = cmd_args.strip().split()
                    sub_action = sub_args[0].lower() if sub_args else ""
                    sub_args = sub_args[1:]
                    if sub_action in ["move", "go", "moveto"] and len(sub_args) >= 2:
                        wc.mouse_move(sub_args[0], sub_args[1])
                    elif sub_action in ["click", "left", "clk"]:
                        if len(sub_args) >= 2:
                            wc.mouse_click(sub_args[0], sub_args[1])
                        else:
                            wc.mouse_click()
                    elif sub_action in ["right", "rclick"] and len(sub_args) >= 2:
                        wc.mouse_right_click(sub_args[0], sub_args[1])
                    elif sub_action in ["double", "dblclick"] and len(sub_args) >= 2:
                        wc.mouse_double_click(sub_args[0], sub_args[1])
                    elif sub_action in ["scroll"]:
                        amount = int(sub_args[0]) if sub_args else -3
                        x = sub_args[1] if len(sub_args) > 1 else None
                        y = sub_args[2] if len(sub_args) > 2 else None
                        wc.mouse_scroll(amount, x, y)
                elif cmd_root == "keyboard":
                    if sub_action in ["type", "write"]:
                        wc.keyboard_type(sub_text)
                    elif sub_action in ["press", "key"]:
                        wc.keyboard_press(sub_text)
                    elif sub_action in ["hotkey", "shortcut"]:
                        keys = [k.strip() for k in sub_text.replace("+", " ").split() if k.strip()]
                        wc.keyboard_hotkey(*keys)
            elif clean_cmd.startswith("cmd "):
                cmd_args = clean_cmd[4:].strip()
                if self.workspace_dir:
                    cmd_args = f'cd /d "{self.workspace_dir}" && {cmd_args}'
                aut.run_command_prompt(cmd_args)
            elif clean_cmd.startswith("powershell "):
                cmd_args = clean_cmd[11:].strip()
                if self.workspace_dir:
                    escaped_ws = self.workspace_dir.replace("'", "''")
                    cmd_args = f"Set-Location '{escaped_ws}' ; {cmd_args}"
                aut.run_powershell(cmd_args)
            elif clean_cmd.startswith("app "):
                aut.app_control(clean_cmd[4:].strip())
            else:
                aut.app_control(clean_cmd)
        except Exception as e:
            print(f"Error executing AI system command: {e}")

    def _call_ai(self, prompt, apply_to_editor=False):
        self._ai_log("🤖 JARVIS thinking...\n")
        self.voice_engine.speak("Working on your code prompt, sir.")

        def _run():
            try:
                self._write_ide_state("thinking")
                
                # Prepend SYSTEM_PROMPT with workspace context on the first turn
                if self.workspace_dir:
                    workspace_ctx = f"The active workspace directory is: {self.workspace_dir}\n"
                else:
                    workspace_ctx = f"The active workspace directory is: {_BASE} (None selected)\n"
                
                system_prefix = f"{SYSTEM_PROMPT}\n\n[CONTEXT]\n{workspace_ctx}════════════════════════════════════════════════════════════\n\n"
                current_prompt = system_prefix + prompt
                
                max_turns = 8
                final_response = ""
                last_ai_response = ""
                
                sys.path.insert(0, _BASE)
                from jarvis_direct_ai_chat import DirectAIChat
                chat = DirectAIChat()
                
                for turn in range(max_turns):
                    if self.brain and getattr(self.brain, 'is_connected', False):
                        response = self.brain.think(current_prompt)
                    else:
                        try:
                            result = chat.chat_with_ai(current_prompt, 'auto')
                            response = result.get('response', 'No response') if isinstance(result, dict) else str(result)
                        except Exception as fallback_err:
                            response = f"Fallback AI error: {fallback_err}"
                    
                    last_ai_response = response
                    
                    # Parse the response for EXECUTE commands
                    lines = response.splitlines()
                    execute_commands = []
                    for line in lines:
                        if "EXECUTE:" in line:
                            cmd = line.split("EXECUTE:", 1)[1].strip()
                            execute_commands.append(cmd)
                            
                    if not execute_commands:
                        final_response = response
                        break
                        
                    # We have commands to execute!
                    self.gui_queue.put(('log', f"🤖 JARVIS proposed commands:\n" + "\n".join([f"- {c}" for c in execute_commands]) + "\n\n"))
                    
                    feedback_parts = []
                    for cmd in execute_commands:
                        # 1. read_file
                        if cmd.startswith("read_file "):
                            filepath = cmd.split("read_file ", 1)[1].strip().strip("'\"")
                            resolved_path = filepath
                            if not os.path.isabs(resolved_path) and self.workspace_dir:
                                resolved_path = os.path.join(self.workspace_dir, filepath)
                            else:
                                resolved_path = os.path.join(_BASE, filepath)
                            
                            resolved_path = os.path.abspath(resolved_path)
                            self.gui_queue.put(('log', f"📖 Reading file: {resolved_path}...\n"))
                            try:
                                with open(resolved_path, "r", encoding="utf-8", errors="ignore") as f:
                                    content = f.read()
                                feedback_parts.append(f"[SYSTEM FEEDBACK: File '{filepath}' read successfully. Content follows:\n```\n{content}\n```]")
                            except Exception as e:
                                feedback_parts.append(f"[SYSTEM FEEDBACK: Error reading file '{filepath}': {e}]")
                                
                        # 1b. list_dir
                        elif cmd.startswith("list_dir"):
                            dirpath = cmd.split("list_dir", 1)[1].strip().strip("'\"")
                            if not dirpath:
                                resolved_path = self.workspace_dir if self.workspace_dir else _BASE
                            else:
                                resolved_path = dirpath
                                if not os.path.isabs(resolved_path) and self.workspace_dir:
                                    resolved_path = os.path.join(self.workspace_dir, dirpath)
                                else:
                                    resolved_path = os.path.join(_BASE, dirpath)
                            
                            resolved_path = os.path.abspath(resolved_path)
                            self.gui_queue.put(('log', f"📁 Listing directory: {resolved_path}...\n"))
                            try:
                                if os.path.exists(resolved_path) and os.path.isdir(resolved_path):
                                    items = os.listdir(resolved_path)
                                    contents = []
                                    for item in items:
                                        full_item = os.path.join(resolved_path, item)
                                        if os.path.isdir(full_item):
                                            contents.append(f"[DIR] {item}/")
                                        else:
                                            contents.append(f"[FILE] {item}")
                                    contents_str = "\n".join(contents) if contents else "(empty directory)"
                                    feedback_parts.append(f"[SYSTEM FEEDBACK: Directory '{dirpath}' contents:\n{contents_str}]")
                                else:
                                    feedback_parts.append(f"[SYSTEM FEEDBACK: Error: '{dirpath}' is not a valid directory or does not exist.]")
                            except Exception as e:
                                feedback_parts.append(f"[SYSTEM FEEDBACK: Error listing directory '{dirpath}': {e}]")

                        # 1c. open_file
                        elif cmd.startswith("open_file"):
                            filepath = cmd.split("open_file", 1)[1].strip().strip("'\"")
                            if not filepath:
                                feedback_parts.append(f"[SYSTEM FEEDBACK: Error: open_file requires a filepath.]")
                            else:
                                resolved_path = filepath
                                if not os.path.isabs(resolved_path) and self.workspace_dir:
                                    resolved_path = os.path.join(self.workspace_dir, filepath)
                                else:
                                    resolved_path = os.path.join(_BASE, filepath)
                                
                                resolved_path = os.path.abspath(resolved_path)
                                self.gui_queue.put(('log', f"🖥️ Opening file in editor: {resolved_path}...\n"))
                                if os.path.exists(resolved_path) and os.path.isfile(resolved_path):
                                    self.gui_queue.put(('open_file_gui', resolved_path))
                                    feedback_parts.append(f"[SYSTEM FEEDBACK: File '{filepath}' opened in editor successfully.]")
                                else:
                                    feedback_parts.append(f"[SYSTEM FEEDBACK: Error: File '{filepath}' does not exist or is a directory.]")
                                
                        # 2. cmd / powershell
                        elif cmd.startswith("cmd ") or cmd.startswith("powershell "):
                            is_ps = cmd.startswith("powershell ")
                            cmd_str = cmd.split("powershell ", 1)[1].strip() if is_ps else cmd.split("cmd ", 1)[1].strip()
                            self.gui_queue.put(('log', f"💻 Running command: {cmd_str}...\n"))
                            
                            # Run visibly
                            self.execute_ai_system_command(cmd)
                            
                            # Capture output
                            try:
                                shell_args = ["powershell.exe", "-Command", cmd_str] if is_ps else ["cmd.exe", "/c", cmd_str]
                                run_cwd = self.workspace_dir if self.workspace_dir else _BASE
                                proc_res = subprocess.run(shell_args, capture_output=True, text=True, timeout=15, cwd=run_cwd)
                                output_str = f"STDOUT:\n{proc_res.stdout or ''}\nSTDERR:\n{proc_res.stderr or ''}\nExit Code: {proc_res.returncode}"
                            except Exception as e:
                                output_str = f"Execution failed: {e}"
                            feedback_parts.append(f"[SYSTEM FEEDBACK: Command executed. Output:\n{output_str}]")
                            
                        # 3. other actions
                        else:
                            self.gui_queue.put(('log', f"⚙️ Executing system action: {cmd}...\n"))
                            try:
                                self.execute_ai_system_command(cmd)
                                feedback_parts.append(f"[SYSTEM FEEDBACK: Action '{cmd}' triggered successfully.]")
                            except Exception as e:
                                feedback_parts.append(f"[SYSTEM FEEDBACK: Action '{cmd}' failed: {e}]")
                                
                    # Combine feedbacks and loop
                    follow_up = "Below is the execution result/feedback for your commands:\n\n" + "\n\n".join(feedback_parts) + "\n\nPlease continue. If you need to do more tasks or read/write more files, write EXECUTE: [command]. Otherwise, provide your final response to the user."
                    current_prompt = follow_up
                    
                # Reached final response
                response = final_response or last_ai_response
                if response:
                    # Parse normal lines to show to the user (exclude EXECUTE commands)
                    resp_lines = response.splitlines()
                    clean_lines = [l for l in resp_lines if "EXECUTE:" not in l]
                    clean_response = "\n".join(clean_lines).strip()
                    
                    self.gui_queue.put(('log', clean_response + "\n\n"))
                    self._speak_summary(clean_response)
                    if apply_to_editor:
                        self.gui_queue.put(('insert', clean_response))
                    self._write_ide_state("idle", clean_response)
                else:
                    self._write_ide_state("idle", "No response received")
            except Exception as e:
                self.gui_queue.put(('error', str(e)))
                self._write_ide_state("idle", f"Error: {e}")

        threading.Thread(target=_run, daemon=True).start()

    def _extract_code(self, text):
        import re
        match = re.search(r'```(?:\w+)?\n(.*?)```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _insert_code(self, response_text):
        import re
        blocks = re.split(r'---\s*FILE:\s*([^\s\]\-]+)(?:\s+[^-\n]+)?\s*---', response_text)
        if len(blocks) < 3:
            code = self._extract_code(response_text) or response_text
            if self.active_tab:
                self.active_tab.editor.delete("1.0", "end")
                self.active_tab.editor.insert("1.0", code)
                self.voice_engine.speak("Code generated and inserted into active editor, sir.")
            return
        updated_files = []
        for i in range(1, len(blocks), 2):
            fname = blocks[i].strip()
            content = blocks[i+1].strip()
            content = self._extract_code(content) or content
            found_tab = None
            for tab in self.tabs:
                if tab.name.lower() == fname.lower():
                    found_tab = tab
                    break
            if found_tab:
                found_tab.editor.delete("1.0", "end")
                found_tab.editor.insert("1.0", content)
                updated_files.append(found_tab.name)
        if updated_files:
            files_str = ", ".join(updated_files)
            self.voice_engine.speak(f"Updated files: {files_str}, sir.")
        else:
            self.voice_engine.speak("Finished processing. No matching open files found to apply changes to.")

    def _ai_log(self, msg):
        self.ai_output.insert("end", msg)
        self.ai_output.see("end")
        try:
            sys.stdout.write(msg)
            sys.stdout.flush()
        except Exception:
            try:
                # Fallback to write encoded bytes if console doesn't support unicode directly
                encoding = sys.stdout.encoding or 'utf-8'
                sys.stdout.write(msg.encode(encoding, errors='replace').decode(encoding))
                sys.stdout.flush()
            except Exception:
                pass

    def _log_terminal(self, msg):
        self.terminal.log_output(msg)

    def _clear(self):
        if self.active_tab:
            self.active_tab.editor.delete("1.0", "end")
        self.terminal.output_area.delete("1.0", "end")
        self.ai_output.delete("1.0", "end")
        self.voice_logs.delete("1.0", "end")

    # ── Voice Speech-to-Command Loop and callbacks ───────────────────────
    def toggle_speech_engine(self):
        active = self.voice_switch_var.get()
        if active:
            res = self.voice_engine.start_listening()
            if res:
                self.voice_status_lbl.configure(text="🎙️ Listen", text_color="#00ff00")
            else:
                self.voice_switch_var.set(False)
        else:
            self.voice_engine.stop_listening()
            self.voice_status_lbl.configure(text="🎙️ Off", text_color="#ffffff")

    def log_voice(self, text):
        self.voice_logs.insert("end", text + "\n")
        self.voice_logs.see("end")

    def execute_voice_command(self, text):
        """Processes vocal statements triggered from background speech thread"""
        self.after(0, lambda: self._process_voice_cmd(text))

    def _process_voice_cmd(self, statement):
        statement = statement.replace("jarvis", "").strip().lower()
        
        # Translate Bangla / Banglish voice commands to English equivalents for the IDE
        bangla_mappings = {
            "রান": "run", "চালু": "run", "এক্সিকিউট": "run", "শুরু": "run",
            "সেভ": "save", "সংরক্ষণ": "save", "সেব": "save",
            "নতুন": "new file", "নিউ ফাইল": "new file", "নিউ ট্যাব": "new file",
            "ব্যাখ্যা": "explain", "বুঝিয়ে": "explain", "বল": "explain",
            "ঠিক": "fix", "ফিক্স": "fix", "ডিবাগ": "fix",
            "টগল": "toggle", "সাইডবার": "toggle",
            "ক্লিয়ার": "clear", "পরিষ্কার": "clear", "মোছো": "clear",
            "ডার্ক": "dark mode", "অন্ধকার": "dark mode",
            "লাইট": "light mode", "আলো": "light mode",
            "গান": "sing", "কান্না": "cry", "কাঁদো": "cry"
        }
        
        for bn_word, en_word in bangla_mappings.items():
            if bn_word in statement:
                statement = statement.replace(bn_word, en_word)
        
        if "run" in statement or "execute" in statement:
            self._run_code()
            self.voice_engine.speak("Executing code runner.")
        elif "save" in statement:
            self._save_file()
            self.voice_engine.speak("Saving script to disk.")
        elif "new file" in statement or "new tab" in statement:
            self.new_empty_tab()
            self.voice_engine.speak("Created a new code editor tab.")
        elif "explain" in statement:
            self._ai_explain()
        elif "fix" in statement:
            self._ai_fix()
        elif "toggle" in statement or "sidebar" in statement:
            self.toggle_sidebar()
            self.voice_engine.speak("Sidebar toggled.")
        elif "clear" in statement:
            self._clear()
            self.voice_engine.speak("Cleared console panels.")
        elif "dark mode" in statement:
            self._apply_theme("Antigravity Dark")
            self.voice_engine.speak("Activated Antigravity Dark theme.")
        elif "light mode" in statement:
            self._apply_theme("Antigravity Light")
            self.voice_engine.speak("Activated Antigravity Light theme.")
        elif "sing" in statement:
            self.voice_engine.speak("I am singing a song, sir.")
            import winsound, threading
            def play_sing():
                try:
                    melody = [(262, 150), (330, 150), (392, 150), (523, 300), (392, 150), (262, 400)]
                    for f, d in melody:
                        winsound.Beep(f, d)
                except Exception:
                    pass
            threading.Thread(target=play_sing, daemon=True).start()
            self.log_voice("🎙️ JARVIS: Singing a song...")
        elif "cry" in statement:
            self.voice_engine.speak("Oh sir, I am so sorry. I am crying.")
            import winsound, threading
            def play_cry():
                try:
                    for _ in range(2):
                        for freq in range(600, 200, -25):
                            winsound.Beep(freq, 25)
                except Exception:
                    pass
            threading.Thread(target=play_cry, daemon=True).start()
            self.log_voice("🎙️ JARVIS: Crying...")
        else:
            self.log_voice(f"❓ Command unrecognized: '{statement}'")
            self.voice_engine.speak("Command unrecognized.")

    def _ai_explain(self):
        code = self._get_combined_context()
        if not code.strip():
            self._ai_log("⚠️ No code files are currently open to explain.\n")
            self.voice_engine.speak("There are no open code files to explain, sir.")
            return
        prompt = f"Please explain the logic of these scripts in simple terms:\n\n{code}"
        self._call_ai(prompt)

    # ── Syntax Highlighting & Analysis parser ───────────────────────────
    def highlight_syntax(self, editor):
        if getattr(editor, '_highlighting', False):
            return
        editor._highlighting = True
        
        try:
            for tag in ["keyword", "builtin", "number", "string", "comment", "definition"]:
                editor.tag_remove(tag, "1.0", "end")
                
            text = editor.get("1.0", "end-1c")
            
            keywords = r"\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|let|const|var|function|do|switch|case|new|this|catch|throw|typeof|instanceof|of)\b"
            builtins = r"\b(print|len|range|str|int|float|list|dict|set|tuple|self|console|log|window|document|sys|os|math|path|subprocess|threading|time)\b"
            numbers = r"\b\d+(\.\d+)?\b"
            strings = r"(\".*?\"|'.*?')"
            comments = r"(#.*?$|//.*?$)"
            definitions = r"\b(def|class|function)\s+(\w+)\b"
            
            import re
            
            # Load keyword tag colors dynamically based on settings
            self._update_tag_colors(self.current_theme, editor)
            
            for match in re.finditer(keywords, text):
                editor.tag_add("keyword", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            for match in re.finditer(builtins, text):
                editor.tag_add("builtin", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            for match in re.finditer(numbers, text):
                editor.tag_add("number", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            for match in re.finditer(strings, text):
                editor.tag_add("string", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            for match in re.finditer(comments, text, re.MULTILINE):
                editor.tag_add("comment", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            for match in re.finditer(definitions, text):
                editor.tag_add("definition", f"1.0 + {match.start(2)} chars", f"1.0 + {match.end(2)} chars")
                
        except Exception as e:
            print(f"Highlighting error: {e}")
        finally:
            editor._highlighting = False

    def _update_tag_colors(self, theme_name, editor):
        theme = THEMES.get(theme_name, THEMES["Antigravity Dark"])
        editor.tag_configure("keyword", foreground=theme["keyword"])
        editor.tag_configure("builtin", foreground=theme["builtin"])
        editor.tag_configure("number", foreground=theme["number"])
        editor.tag_configure("string", foreground=theme["string"])
        editor.tag_configure("comment", foreground=theme["comment"], font=(self.settings.get("font_family"), self.settings.get("font_size"), "italic"))
        editor.tag_configure("definition", foreground=theme["definition"])
        
        # Error tag config
        bg_flash = "#3a0505" if "Dark" in theme_name or theme_name != "Antigravity Light" else "#ffebeb"
        editor.tag_configure("error_highlight", background=bg_flash, underline=True)

    def _apply_theme(self, theme_name):
        self.settings.set("theme", theme_name)
        self.current_theme = theme_name
        self.theme_colors = THEMES[theme_name]
        
        # Set panel colors
        self.configure(fg_color=self.theme_colors["bg"])
        self.activity_bar.configure(fg_color=self.theme_colors["activity"])
        self.sidebar.configure(fg_color=self.theme_colors["sidebar"])
        self.top_strip.configure(fg_color=self.theme_colors["sidebar"])
        self.status_bar.configure(fg_color=self.theme_colors["status"])
        
        # Apply theme colors to editor and line canvases
        for tab in self.tabs:
            tab.editor.configure(
                bg=self.theme_colors["bg"], fg=self.theme_colors["fg"],
                insertbackground=self.theme_colors["fg"],
                selectbackground=self.theme_colors["sel"]
            )
            tab.line_numbers.configure(bg=self.theme_colors["line"])
            self.highlight_syntax(tab.editor)

    def schedule_background_analysis(self, tab):
        if hasattr(self, '_analysis_timer') and self._analysis_timer:
            try:
                self.after_cancel(self._analysis_timer)
            except:
                pass
        self._analysis_timer = self.after(1000, lambda: self.start_background_analysis(tab))

    def start_background_analysis(self, tab):
        if not tab or tab != self.active_tab:
            return
        code = tab.editor.get("1.0", "end-1c")
        lang = self.current_lang
        threading.Thread(target=self._run_analysis_thread, args=(tab, code, lang), daemon=True).start()

    def _run_analysis_thread(self, tab, code, lang):
        errors = []
        if lang == "Python":
            import ast
            try:
                ast.parse(code)
            except SyntaxError as e:
                errors.append({
                    "line": e.lineno or 1,
                    "col": e.offset or 1,
                    "msg": e.msg,
                    "type": "error"
                })
            except Exception:
                pass
        
        bracket_errors = self._check_unmatched_brackets(code)
        errors.extend(bracket_errors)
        
        # Remove duplicates
        seen = set()
        unique_errors = []
        for err in errors:
            key = (err["line"], err["msg"])
            if key not in seen:
                seen.add(key)
                unique_errors.append(err)
                
        self.gui_queue.put(('analysis', (tab, unique_errors)))

    def _check_unmatched_brackets(self, code):
        errors = []
        stack = []
        bracket_pairs = {')': '(', ']': '[', '}': '{'}
        opening = set(bracket_pairs.values())
        closing = set(bracket_pairs.keys())
        
        lines = code.split('\n')
        in_string = False
        string_char = None
        
        for row_idx, line in enumerate(lines):
            col_idx = 0
            line_len = len(line)
            
            while col_idx < line_len:
                char = line[col_idx]
                if not in_string:
                    if self.current_lang == "Python" and char == '#':
                        break
                    elif self.current_lang in ["JavaScript", "HTML"] and char == '/' and col_idx + 1 < line_len and line[col_idx+1] == '/':
                        break
                
                if char in ['"', "'", '`'] and (col_idx == 0 or line[col_idx-1] != '\\'):
                    if in_string:
                        if string_char == char:
                            in_string = False
                            string_char = None
                    else:
                        in_string = True
                        string_char = char
                
                if not in_string:
                    if char in opening:
                        stack.append((char, row_idx + 1, col_idx + 1))
                    elif char in closing:
                        if not stack:
                            errors.append({
                                "line": row_idx + 1,
                                "col": col_idx + 1,
                                "msg": f"Unmatched closing bracket: '{char}'",
                                "type": "warning"
                            })
                        else:
                            top_char, top_line, top_col = stack.pop()
                            expected = bracket_pairs[char]
                            if top_char != expected:
                                errors.append({
                                    "line": row_idx + 1,
                                    "col": col_idx + 1,
                                    "msg": f"Mismatched bracket: '{char}' closed but expected '{expected}' (opened at line {top_line}, col {top_col})",
                                    "type": "warning"
                                })
                col_idx += 1
                
        for char, line_no, col_no in stack:
            errors.append({
                "line": line_no,
                "col": col_no,
                "msg": f"Unclosed opening bracket: '{char}'",
                "type": "warning"
            })
            
        return errors

    def _update_analysis_ui(self, tab, errors):
        if not tab or tab != self.active_tab:
            return
            
        editor = tab.editor
        editor.tag_remove("error_highlight", "1.0", "end")
        
        # Clear UI
        self.clear_problems_ui()
            
        if not errors:
            self.analysis_status = "Code Syntax OK ✅"
            self._update_status()
            return
            
        err_msg_summary = ""
        for idx, err in enumerate(errors):
            line = err["line"]
            col = err["col"]
            msg = err["msg"]
            err_type = err["type"]
            
            try:
                editor.tag_add("error_highlight", f"{line}.0", f"{line}.end")
            except:
                pass
                
            bg_card = "#1a0808" if err_type == "error" else "#1a1a08"
            border_c = "#FF3131" if err_type == "error" else "#F1FA8C"
            txt_color = "#FF3131" if err_type == "error" else "#F1FA8C"
            prefix = "🔴 Error" if err_type == "error" else "🟡 Warning"
            
            card = ctk.CTkFrame(self.inspector_scroll, fg_color=bg_card, border_width=1, border_color=border_c, corner_radius=6)
            card.pack(fill="x", padx=10, pady=5)
            
            lbl_text = f"{prefix} (Line {line}, Col {col}): {msg}"
            info_lbl = ctk.CTkLabel(card, text=lbl_text, font=("Consolas", 11), text_color=txt_color, justify="left", anchor="w")
            info_lbl.pack(side="left", padx=10, pady=8, fill="x", expand=True)
            
            go_btn = ctk.CTkButton(card, text="GO TO ⚡", width=65, height=24,
                                    fg_color="#003344", hover_color="#004455",
                                    font=("Courier New", 10, "bold"),
                                    command=lambda l=line, c=col: self.go_to_line(l, c))
            go_btn.pack(side="right", padx=10, pady=8)
            
            if idx == 0:
                prefix = "Error" if err_type == "error" else "Warning"
                err_msg_summary = f"⚠️ {prefix}: {msg} (Line {line})"
                
        self.analysis_status = err_msg_summary
        self._update_status()

    def clear_problems_ui(self):
        for widget in self.inspector_scroll.winfo_children():
            widget.destroy()
        lbl = ctk.CTkLabel(self.inspector_scroll, text="🎉 No syntax errors or unmatched brackets found.",
                           font=("Courier New", 12, "bold"), text_color="#00FF41")
        lbl.pack(pady=20, padx=20, anchor="center")

    def go_to_line(self, line, col=0):
        if not self.active_tab:
            return
        editor = self.active_tab.editor
        editor.mark_set("insert", f"{line}.{col}")
        editor.see(f"{line}.0")
        editor.focus_set()
        
        # Flash target line in gold temporarily
        editor.tag_remove("error_flash", "1.0", "end")
        editor.tag_add("error_flash", f"{line}.0", f"{line}.end")
        editor.tag_configure("error_flash", background="#554400")
        self.after(800, lambda: editor.tag_remove("error_flash", f"{line}.0", f"{line}.end"))

    # ── Status and Telemetry loop ───────────────────────────────────────
    def _update_status(self, event=None):
        if not self.active_tab:
            self.pos_status_lbl.configure(text="")
            return
        try:
            pos = self.active_tab.editor.index("insert")
            line, col = pos.split(".")
            self.pos_status_lbl.configure(text=f"Ln {line}, Col {int(col)+1}")
        except:
            pass

    def run_telemetry(self):
        """Live updates CPU and Memory metrics in the status bar"""
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        if TELEMETRY_AVAILABLE:
            try:
                cpu = int(psutil.cpu_percent())
                ram = int(psutil.virtual_memory().percent)
                self.telemetry_lbl.configure(text=f"CPU: {cpu}% | RAM: {ram}%")
            except Exception:
                pass
        try:
            self.after(2000, self.run_telemetry)
        except:
            pass

    def run_auto_save_worker(self):
        """Worker thread checking editor tabs for unsaved auto-save triggers"""
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        if self.settings.get("auto_save"):
            now = time.time()
            for tab in self.tabs:
                if tab.is_modified and tab.file_path and (now - tab.last_key_time > 2.0):
                    try:
                        content = tab.editor.get("1.0", "end-1c")
                        with open(tab.file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        tab.is_modified = False
                        self.after(0, self.update_tab_bar)
                        self.after(0, lambda p=tab.file_path: self._log_terminal(f"Auto-saved: {p}\n"))
                    except Exception as e:
                        print(f"Auto-save failed: {e}")
        try:
            self.after(1000, self.run_auto_save_worker)
        except:
            pass

    def _process_gui_queue(self):
        try:
            if not self.winfo_exists():
                return
        except:
            return
            
        try:
            while not self.gui_queue.empty():
                action, data = self.gui_queue.get_nowait()
                if action == 'log':
                    self._ai_log(data)
                elif action == 'error':
                    self._ai_log(f"❌ Error: {data}\n")
                elif action == 'insert':
                    self._insert_code(data)
                elif action == 'open_file_gui':
                    self.open_file_by_path(data)
                elif action == 'analysis':
                    tab, errors = data
                    self._update_analysis_ui(tab, errors)
                elif action == 'mic_status':
                    if data == 'listening':
                        self.ai_mic_btn.configure(fg_color="#cc0000", text="🔴 Listening...")
                    elif data == 'processing':
                        self.ai_mic_btn.configure(fg_color="#006655", text="⏳ Thinking...")
                    else:
                        self.ai_mic_btn.configure(fg_color="#181818", text="🎤")
                elif action == 'mic_result':
                    self.ai_input.delete(0, "end")
                    self.ai_input.insert(0, data)
                    self._ai_ask()
                self.gui_queue.task_done()
        except Exception as e:
            print(f"Queue processing error: {e}")
        finally:
            try:
                self.after(100, self._process_gui_queue)
            except:
                pass

    def _set_default_code(self, editor):
        code = '''# Antigravity IDE - Python File
# AI-powered code editor with voice assistance!

print("Welcome to Antigravity IDE.")

def hello_jarvis():
    return "At your service, sir."

print(hello_jarvis())
'''
        editor.delete("1.0", "end")
        editor.insert("1.0", code)


def open_code_studio(master=None, brain=None):
    """Main launching entrypoint imported by other JARVIS scripts"""
    studio = CodeStudio(master, brain)
    studio.lift()
    studio.focus_force()
    return studio


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    studio = CodeStudio(root)
    studio.protocol("WM_DELETE_WINDOW", lambda: (studio.destroy(), root.destroy()))
    root.mainloop()
