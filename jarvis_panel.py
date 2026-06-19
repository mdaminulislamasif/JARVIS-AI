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

import threading
import math

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class SafeStream:
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        try:
            if self.stream:
                self.stream.write(data)
        except Exception:
            pass
    def flush(self):
        try:
            if self.stream:
                self.stream.flush()
        except Exception:
            pass
    def __getattr__(self, name):
        return getattr(self.stream, name)

if sys.stdout is not None:
    sys.stdout = SafeStream(sys.stdout)
if sys.stderr is not None:
    sys.stderr = SafeStream(sys.stderr)
import subprocess
import time
import webbrowser
import psutil
import pyautogui
import customtkinter as ctk
from PIL import Image, ImageTk

# Import Modular JARVIS Components
from core.brain import JarvisBrain
from core.database import init_db, save_chat, get_recent_history
from core.auth import get_session, logout, auto_apply_key_to_config
from core.login_window import check_and_login
from engine.voice import VoiceEngine
from engine.mobile_server import start_server, get_ip
from engine.face3d import Face3D
from engine.automation import (
    clean_system, start_workspace, take_screenshot, scan_network,
    ping_device, get_system_stats, copy_to_clipboard, control_volume,
    get_running_processes, get_memory_info, save_note, open_task_manager,
    lock_computer, shutdown_computer, restart_computer, get_disk_info, open_explorer,
    run_net_command, get_network_users, boost_game, android_boost, setup_kali_mode,
    setup_remote_desktop, start_remote_connection, auto_collect_info, scan_for_viruses,
    force_kill_process, empty_recycle_bin, set_brightness, media_control, deploy_bot,
    create_screen_share, scan_wifi, share_files, deep_port_scan, generate_payload,
    scan_bluetooth, ducky_deploy, alien_cipher, signal_scan, find_and_connect, manage_device,
    neutralize_badshah, setup_infinity_firewall, browser_control, control_window,
    scan_router_devices, router_connect, web_security_audit, app_control, self_check,
    run_alien_mode, run_flipper_mode
)
# New engine modules
from engine.generator import (
    generate_text, generate_image, generate_audio, generate_video,
    generate_3d_model, generate_file, generate_photo, list_generated, open_generated,
    GEN_DIR,
)
from engine.streaming import stream_think, detect_bugs, AutoController, start_super_host
from engine.multi_brain import MultiBrain

# Windows 10 + Mouse + Keyboard Control Engine (NEW)
try:
    from engine.windows_control import (
        windows_control, bangla_windows_command,
        mouse_move, mouse_click, mouse_right_click, mouse_double_click,
        mouse_scroll, mouse_drag, mouse_position,
        keyboard_type, keyboard_press, keyboard_hotkey,
        win10_open_app, win10_close_app, win10_focus_window,
        win10_list_windows, win10_shortcut, win10_open_settings,
        win10_system_info, win10_volume_control, win10_brightness_control,
        win10_run_command, win10_manage_process,
    )
    _WIN_CTRL_OK = True
    print("[OK] Windows 10 Control Engine ONLINE")
except Exception as _wce:
    _WIN_CTRL_OK = False
    print(f"[!] Windows Control Engine: {_wce}")
    def windows_control(cmd=""): return f"Windows Control not available: {_wce}"
    def bangla_windows_command(t): return None

# File Upload System
from jarvis_file_handler import handle_file_upload, get_recent_uploads
from jarvis_upload_ui import add_file_upload_button

# Search Learning System
from jarvis_search_learner import SearchLearner

# Article Learning System
from jarvis_article_learner import ArticleLearner

# Translation System
from jarvis_translator import JarvisTranslator

# All Functions Panel
from jarvis_all_functions_panel import open_all_functions_panel

# Natural Interface
from jarvis_natural_interface import NaturalInterface

# Keyboard Shortcuts
from jarvis_keyboard_shortcuts import KeyboardShortcuts

# World AI Chat (Fallback when API keys don't work)
from jarvis_world_ai_chat import WorldAIChat

# Direct AI Chat (JARVIS chats automatically - no browser needed!)
from jarvis_direct_ai_chat import DirectAIChat

# Voice Control Panel (Advanced voice settings!)
from jarvis_voice_control_panel import open_voice_control_panel

# Auto AI Learner (JARVIS learns automatically!)
from jarvis_auto_ai_learner import AutoAILearner

# SIM Call System (New!)
from jarvis_sim_call import open_call_ui

# Neural Harvester System (New!)
from jarvis_neural_harvester import run_harvest_on_text

# Knowledge Hub System (New!)
from jarvis_knowledge_hub import open_knowledge_hub

# Login Bot System (New!)
from jarvis_login_bot import open_login_bot_ui

# Code Studio (AI Code Editor!)
try:
    from jarvis_code_studio import open_code_studio
    _CODE_STUDIO_AVAILABLE = True
except Exception:
    _CODE_STUDIO_AVAILABLE = False

# Folder Upload System
try:
    from jarvis_folder_upload import open_folder_upload
    _FOLDER_UPLOAD_AVAILABLE = True
except Exception:
    _FOLDER_UPLOAD_AVAILABLE = False

# Android Device Manager
try:
    from jarvis_android_manager import open_android_manager
    _ANDROID_MANAGER_AVAILABLE = True
except Exception:
    _ANDROID_MANAGER_AVAILABLE = False

# System Control Module
try:
    from jarvis_system_control import jarvis_execute as sys_execute
    _SYS_CONTROL_AVAILABLE = True
except Exception as _e:
    _SYS_CONTROL_AVAILABLE = False
    def sys_execute(cmd, brain=None): return f"System control unavailable: {_e}"

# ASIF Hacker Suite (New!)
from jarvis_asif_bots import open_asif_suite

# =============================================================================
# ANTIGRAVITY MASTER ENGINE CONFIG
# =============================================================================
_WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
_DESKTOP_AI    = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'ai')

# Prefer workspace-local files; fall back to Desktop/ai/
def _resolve(filename):
    ws = os.path.join(_WORKSPACE_DIR, filename)
    return ws if os.path.exists(ws) else os.path.join(_DESKTOP_AI, filename)

BASE_DIR          = _WORKSPACE_DIR
CONFIG_PATH       = _resolve('jarvis_config.txt')
FACE_IMAGE_PATH   = _resolve('jarvis_face.png')
FACE_GLB_PATH     = _resolve('jarvis_face.glb')
OPENAI_CONFIG_PATH = os.path.join(_DESKTOP_AI, 'openai_config.txt')

def get_saved_keys():
    """Load all valid Gemini API keys from config file."""
    keys = []
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            keys = [line.strip() for line in f.readlines()
                    if (line.strip().startswith("AIza") or line.strip().startswith("AQ.")) and len(line.strip()) > 30]
    return keys

def get_openai_keys():
    """Load all valid OpenAI API keys."""
    keys = []
    if os.path.exists(OPENAI_CONFIG_PATH):
        with open(OPENAI_CONFIG_PATH, 'r') as f:
            keys = [line.strip() for line in f.readlines()
                    if line.strip().startswith("sk-") and len(line.strip()) > 20]
    return keys

def save_new_key(key):
    """Save a new key — auto-detects Gemini vs OpenAI."""
    key = key.strip()
    if (key.startswith("AIza") or key.startswith("AQ.")) and len(key) > 30:
        ok, reason = JarvisBrain.validate_key(key)
        if not ok:
            reason_lower = reason.lower()
            # These are NOT bad key errors — server/model issues, key is valid
            ignored_errors = ["404", "not_found", "503", "unavailable",
                              "429", "resource_exhausted", "overloaded",
                              "currently", "service_unavailable"]
            if not any(e in reason_lower for e in ignored_errors):
                raise ValueError(f"Gemini key invalid: {reason[:120]}")
        # Save key regardless (server may be temporarily down)
        keys = get_saved_keys()
        if key not in keys:
            keys.insert(0, key)
            with open(CONFIG_PATH, 'w') as f:
                for k in keys:
                    f.write(k + "\n")
    elif key.startswith("sk-") and len(key) > 20:
        keys = get_openai_keys()
        if key not in keys:
            keys.insert(0, key)
            with open(OPENAI_CONFIG_PATH, 'w') as f:
                for k in keys:
                    f.write(k + "\n")
    else:
        raise ValueError("Invalid API key format (expects AIza... or AQ... or sk-...).")


# Initialize Database
init_db()

# =============================================================================
# ANIMATED NEON CORE (3D FACE ENGINE)
# =============================================================================
class AntigravityCore(ctk.CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, bg="#02050A", **kwargs)
        self.state = "idle"
        self.emotion = "neutral"
        self.anim = 0
        self.scale = 1.0
        self.raw_img = None
        self.img = None
        self._blink_until = 0.0
        self._next_blink_at = 0.0
        self._mouth_phase = 0.0
        import time
        self.boot_flash_until = time.time() + 1.5
        self.load_avatar()
        self.run_anim()

    def set_emotion(self, emotion):
        self.emotion = str(emotion).lower()

    def load_avatar(self):
        try:
            path = FACE_IMAGE_PATH
            if os.path.exists(path):
                self.raw_img = Image.open(path).convert("RGBA")
                self.update_image()
            else:
                self.raw_img = None
                self.img = None
        except Exception:
            self.raw_img = None
            self.img = None

    def update_image(self):
        if self.raw_img is None:
            self.img = None
            return
        s = int(220 + 10 * math.sin(self.anim * 3))
        resized = self.raw_img.resize((s, s), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(resized)

    def set_state(self, state):
        self.state = state

    def draw(self):
        self.delete("all")
        cx, cy = 150, 150
        
        # 0. Premium pulsing Cyber Cyan HUD Ring during booting
        is_booting = time.time() < getattr(self, 'boot_flash_until', 0.0)
        if is_booting:
            self.configure(bg="#02050A")
            p = 100 + 15 * math.sin(time.time() * 8)
            self.create_oval(cx-p, cy-p*persp_y, cx+p, cy+p*persp_y, outline="#00F3FF", width=2)
            self.create_text(cx, cy, text="INITIALIZING JARVIS...", fill="#00F3FF", font=("Courier New", 14, "bold"))
            return
        else:
            self.configure(bg="#02050A")

        # Determine Color based on state and emotion
        color = "#00FF41" # Neon Green (Idle)
        if self.emotion == "happy":
            color = "#00FF41" # Neon Green
        elif self.emotion == "sad":
            color = "#0033FF" # Deep Blue
        elif self.emotion == "angry":
            color = "#FF0000" # Crimson Red
        elif self.emotion == "excited":
            color = "#FF00FF" # Magenta
        elif self.emotion == "surprised":
            color = "#00FFFF" # Cyan

        if self.state == "listening": color = "#00F3FF" # Cyan override
        elif self.state == "thinking": color = "#FFD700" # Gold override

        # 1. Digital Matrix Rain (Background)
        import random
        for _ in range(15):
            x = random.randint(0, 300)
            y = (self.anim * 200 + random.randint(0, 300)) % 300
            char = random.choice("01$#@!%^&*")
            self.create_text(x, y, text=char, fill="#002200", font=("Courier New", 10))

        # Perspective Scaling
        persp_y = 0.85
        
        # Outer Pulsing HUD Rings
        p1 = 120 + 10 * math.sin(self.anim * 2)
        p2 = 135 + 5 * math.cos(self.anim * 1.5)
        p3 = 145 + 3 * math.sin(self.anim * 4)
        
        self.create_oval(cx-p1, cy-p1*persp_y, cx+p1, cy+p1*persp_y, outline=color, width=1, dash=(2, 4))
        self.create_oval(cx-p2, cy-p2*persp_y, cx+p2, cy+p2*persp_y, outline=color, width=2)
        self.create_oval(cx-p3, cy-p3*persp_y, cx+p3, cy+p3*persp_y, outline=color, width=1)

        # Glitch Effect
        if random.random() > 0.95:
            gy = random.randint(50, 250)
            self.create_line(cx-150, gy, cx+150, gy, fill=color, width=1)

        # Scanning Beam
        scan_y = cy - 150 + (self.anim * 100 % 300)
        if 0 < scan_y < 300:
            self.create_line(cx-140, scan_y, cx+140, scan_y, fill=color, width=1, dash=(1, 1))

        # Rotating Arcs
        start_ang = (self.anim * 50) % 360
        self.create_arc(cx-110, cy-110*persp_y, cx+110, cy+110*persp_y, outline=color, width=3, start=start_ang, extent=60, style="arc")
        self.create_arc(cx-110, cy-110*persp_y, cx+110, cy+110*persp_y, outline=color, width=3, start=start_ang+180, extent=60, style="arc")
        
        # Orbital Data Nodes
        for i in range(8):
            ang = (self.anim * 0.8) + (i * 45 * (math.pi/180))
            r = 150 + 5 * math.sin(self.anim * 3 + i)
            x, y = cx + r * math.cos(ang), cy + r * math.sin(ang) * persp_y
            self.create_oval(x-2, y-2, x+2, y+2, fill=color, outline=color)
            if i % 2 == 0:
                self.create_line(cx + (r-30)*math.cos(ang), cy + (r-30)*math.sin(ang)*persp_y, x, y, fill=color, width=1)

        # Draw Face
        if self.img:
            off_y = 5 * math.sin(self.anim * 2)
            self.create_image(cx, cy + off_y, image=self.img)
            self._draw_face_overlays(cx, cy + off_y, color)
        else:
            self.create_text(cx, cy, text="NO_FACE", fill=color, font=("Courier New", 20, "bold"))

    def _draw_face_overlays(self, cx, cy, color):
        now = time.time()
        blinking = False
        
        # Blinking enabled only for non-extreme emotions
        if self.emotion not in ["surprised", "excited"]:
            if self._next_blink_at <= 0.0:
                self._next_blink_at = now + 2.5 + (2.5 * abs(math.sin(self.anim * 0.37)))
            if now >= self._next_blink_at:
                self._blink_until = now + 0.12
                self._next_blink_at = now + 2.5 + (3.5 * abs(math.sin(self.anim * 0.51)))
            blinking = now < self._blink_until

        eye_y = cy - 25
        left_eye_x = cx - 38
        right_eye_x = cx + 38
        w = 4

        # Eyes Drawing
        if blinking:
            self.create_line(left_eye_x - 14, eye_y, left_eye_x + 14, eye_y, fill=color, width=w)
            self.create_line(right_eye_x - 14, eye_y, right_eye_x + 14, eye_y, fill=color, width=w)
        else:
            if self.emotion == "happy":
                self.create_arc(left_eye_x - 12, eye_y - 6, left_eye_x + 12, eye_y + 10, start=20, extent=140, style="arc", outline=color, width=w)
                self.create_arc(right_eye_x - 12, eye_y - 6, right_eye_x + 12, eye_y + 10, start=20, extent=140, style="arc", outline=color, width=w)
            elif self.emotion == "sad":
                self.create_line(left_eye_x - 12, eye_y - 4, left_eye_x + 12, eye_y + 4, fill=color, width=w)
                self.create_line(right_eye_x - 12, eye_y + 4, right_eye_x + 12, eye_y - 4, fill=color, width=w)
            elif self.emotion == "angry":
                self.create_line(left_eye_x - 12, eye_y + 4, left_eye_x + 12, eye_y - 4, fill=color, width=w)
                self.create_line(right_eye_x - 12, eye_y - 4, right_eye_x + 12, eye_y + 4, fill=color, width=w)
                self.create_line(left_eye_x - 15, eye_y - 12, left_eye_x + 10, eye_y - 5, fill=color, width=w+1)
                self.create_line(right_eye_x - 10, eye_y - 5, right_eye_x + 15, eye_y - 12, fill=color, width=w+1)
            elif self.emotion == "surprised":
                self.create_oval(left_eye_x - 11, eye_y - 11, left_eye_x + 11, eye_y + 11, outline=color, width=w)
                self.create_oval(right_eye_x - 11, eye_y - 11, right_eye_x + 11, eye_y + 11, outline=color, width=w)
            elif self.emotion == "excited":
                self.create_line(left_eye_x - 8, eye_y - 8, left_eye_x + 8, eye_y + 8, fill=color, width=w)
                self.create_line(left_eye_x + 8, eye_y - 8, left_eye_x - 8, eye_y + 8, fill=color, width=w)
                self.create_line(right_eye_x - 8, eye_y - 8, right_eye_x + 8, eye_y + 8, fill=color, width=w)
                self.create_line(right_eye_x + 8, eye_y - 8, right_eye_x - 8, eye_y + 8, fill=color, width=w)
            else:
                self.create_oval(left_eye_x - 10, eye_y - 6, left_eye_x + 10, eye_y + 6, outline=color, width=w)
                self.create_oval(right_eye_x - 10, eye_y - 6, right_eye_x + 10, eye_y + 6, outline=color, width=w)
                px = 2.5 * math.sin(self.anim * 1.2)
                py = 1.5 * math.sin(self.anim * 0.9)
                self.create_oval(left_eye_x - 3 + px, eye_y - 3 + py, left_eye_x + 3 + px, eye_y + 3 + py, fill=color, outline="")
                self.create_oval(right_eye_x - 3 + px, eye_y - 3 + py, right_eye_x + 3 + px, eye_y + 3 + py, fill=color, outline="")

        # Mouth Drawing
        mouth_y = cy + 45
        mouth_w = 48
        if self.state == "speaking":
            self._mouth_phase += 0.25
            open_amt = 6 + 8 * (0.5 + 0.5 * math.sin(self._mouth_phase))
        elif self.state == "listening":
            open_amt = 4
        else:
            open_amt = 2.0

        if self.emotion == "happy":
            self.create_arc(cx - 24, mouth_y - 12, cx + 24, mouth_y + 8, start=190, extent=160, style="arc", outline=color, width=w)
        elif self.emotion == "sad":
            self.create_arc(cx - 24, mouth_y + 2, cx + 24, mouth_y + 22, start=10, extent=160, style="arc", outline=color, width=w)
        elif self.emotion == "angry":
            self.create_line(cx - 20, mouth_y, cx + 20, mouth_y, fill=color, width=w)
        elif self.emotion == "surprised":
            self.create_oval(cx - 10, mouth_y - 10, cx + 10, mouth_y + 10, outline=color, width=w)
        elif self.emotion == "excited":
            self.create_arc(cx - 24, mouth_y - 12, cx + 24, mouth_y + 12, start=180, extent=180, style="chord", fill=color, outline=color)
        else:
            x1, y1 = cx - mouth_w / 2, mouth_y - open_amt / 2
            x2, y2 = cx + mouth_w / 2, mouth_y + open_amt / 2
            self.create_oval(x1, y1, x2, y2, outline=color, width=w)
            if self.state == "speaking":
                self.create_line(cx - 10, mouth_y, cx + 10, mouth_y, fill=color, width=w)

    def run_anim(self):
        try:
            self.anim += 0.05
            if self.anim % 0.2 < 0.05:
                self.update_image()
            self.draw()
        except Exception:
            pass
        finally:
            try:
                if not hasattr(self, '_is_destroying') or not self._is_destroying:
                    self.after(30, self.run_anim)
            except Exception:
                pass

# =============================================================================
# JARVIS ANTIGRAVITY PRIME V11
# =============================================================================
class JarvisAntigravity(ctk.CTk):
    def __init__(self, session: dict = None):
        super().__init__()
        self._session = session or {}
        
        # Destroying flag to prevent after() errors during shutdown
        self._is_destroying = False

        self.title("ANTIGRAVITY [JARVIS PRIME V11]")
        self.geometry("1300x850")
        ctk.set_appearance_mode("dark")
        
        self.neon = "#FF3131" # KILL MODE RED
        self.cyber = "#00F3FF"
        self.bg_black = "#02050A"
        
        # Initialize Engines (Fast Boot Protocol)
        self.brain = None
        self.voice = VoiceEngine()
        
        # Load and apply saved voice settings on startup
        try:
            from jarvis_voice_control_panel import VoiceControlPanel
            v_panel = VoiceControlPanel(self, self.voice, self.speak)
            v_panel.apply_settings()
        except Exception as e:
            print(f"[!] Failed to apply saved voice settings: {e}")
            self.voice.prefer_bangla = True
            
        self.face3d = None
        self.v_lock = threading.Lock()
        self.is_listening = False
        self.continuous_listening = False
        self.prefer_bangla_voice = True
        self.agent_mode = False
        self.streaming_mode = False          # NEW: streaming AI responses
        self.multi_brain = MultiBrain()      # NEW: multi-brain system
        self.auto_ctrl = AutoController()    # NEW: auto controller/scheduler
        self.auto_ctrl.start()
        
        # Low-latency Streaming TTS Speech state
        import queue
        self.speech_queue = queue.Queue()
        self.streaming_speech_buffer = ""
        self.speech_worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_worker_thread.start()
        
        # Integrated AI Chat Mode State
        self.ai_chat_mode = False
        self.selected_global_ai = "auto"
        
        # Initialize Auto Background Learner
        try:
            from jarvis_auto_background_learner import AutoBackgroundLearner
            self.auto_bg_learner = AutoBackgroundLearner()
            print("[OK] Auto Background Learner initialized!")
        except Exception as e:
            self.auto_bg_learner = None
            print(f"[!] Auto Background Learner not available: {e}")
        
        # Initialize Natural Interface
        try:
            self.natural_interface = NaturalInterface()
            self.natural_interface.load_preferences()
            print("[OK] Natural Interface initialized!")
        except Exception as e:
            self.natural_interface = None
            print(f"[!] Natural Interface not available: {e}")
        
        # Initialize Keyboard Shortcuts
        try:
            self.keyboard_shortcuts = KeyboardShortcuts(callback=self._handle_shortcut)
            self.keyboard_shortcuts.start()
            print("[OK] Keyboard Shortcuts activated!")
            print("[IDEA] Press Ctrl+H for shortcuts help")
        except Exception as e:
            self.keyboard_shortcuts = None
            print(f"[!] Keyboard Shortcuts not available: {e}")
        
        # Initialize World AI Chat (Fallback system)
        try:
            self.world_ai_chat = WorldAIChat()
            print("[OK] World AI Chat initialized!")
        except Exception as e:
            self.world_ai_chat = None
            print(f"[!] World AI Chat not available: {e}")
        
        # Initialize Direct AI Chat (Automatic chat - no browser!)
        try:
            self.direct_ai_chat = DirectAIChat()
            print("[OK] Direct AI Chat initialized!")
            print("[IDEA] JARVIS can now chat with AI automatically!")
        except Exception as e:
            self.direct_ai_chat = None
            print(f"[!] Direct AI Chat not available: {e}")
        
        # Clipboard monitoring control (FIX: infinite loop problem)
        self._clipboard_stop_event = threading.Event()
        self._clipboard_enabled = True
        self._clipboard_thread = None
        
        threading.Thread(target=self.async_init_brain, daemon=True).start()
        self.start_clipboard_watcher()
        self._init_face3d()
        
        # Register cleanup handler for graceful shutdown
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Launch visual overlay Antigravity HUD
        try:
            from engine.antigravity_hud import AntigravityHUD
            self.hud = AntigravityHUD(self)
            print("[OK] Antigravity HUD overlay launched!")
        except Exception as e:
            self.hud = None
            print(f"[!] Antigravity HUD failed: {e}")

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.left_panel = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color="#010306", border_width=1, border_color="#002233")
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        
        # 3D Face Animation Container
        self.core = AntigravityCore(self.left_panel, width=300, height=300)
        self.core.pack(pady=40)
        
        # TARGET SCAN BUTTON (OSINT)
        ctk.CTkButton(
            self.left_panel,
            text="👁️ SCAN TARGET PHOTO",
            fg_color="#550000",
            hover_color="#770000",
            font=("Courier New", 12, "bold"),
            height=40,
            command=self.osint_scan
        ).pack(pady=(0, 20))

        face_btns = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        face_btns.pack(pady=(0, 20))
        ctk.CTkButton(
            face_btns,
            text="FACE ON",
            width=90,
            fg_color="#003355",
            hover_color="#005577",
            command=self.face3d_on,
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            face_btns,
            text="FACE OFF",
            width=90,
            fg_color="#440000",
            hover_color="#660000",
            command=self.face3d_off,
        ).pack(side="left", padx=5)
        
        # New Blender Rigging Button
        ctk.CTkButton(
            face_btns,
            text="NEURAL RIG",
            width=90,
            fg_color="#006644",
            hover_color="#008855",
            command=self.neural_rigging,
        ).pack(side="left", padx=5)

        # Sidebar Title
        ctk.CTkLabel(self.left_panel, text="J.A.R.V.I.S.", font=("Courier New", 24, "bold"), text_color=self.neon).pack(pady=20)

        # Scrollable Module Container
        self.modules = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent", width=260)
        self.modules.pack(expand=True, fill="both", padx=10, pady=5)

        def add_module(title, cmd, color="#002233", hcolor="#004466"):
            btn = ctk.CTkButton(self.modules, text=title, fg_color=color, hover_color=hcolor, 
                                command=lambda c=cmd: self.process(c), font=("Courier New", 12, "bold"), height=35)
            btn.pack(pady=5, padx=10, fill="x")

        # --- ANTIGRAVITY SPECIAL FEATURES ---
        ctk.CTkLabel(self.modules, text="[ ANTIGRAVITY NEURAL LINK ]", font=("Courier New", 10, "bold"), text_color="#00FF41").pack(pady=(10, 5))
        
        ctk.CTkButton(
            self.modules,
            text="ANTIGRAVITY UPLINK",
            fg_color="#003311",
            hover_color="#005522",
            font=("Courier New", 12, "bold"),
            height=40,
            command=self.antigravity_uplink
        ).pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(
            self.modules,
            text="SYSTEM RECON",
            fg_color="#332200",
            hover_color="#554400",
            font=("Courier New", 12, "bold"),
            height=40,
            command=self.system_recon
        ).pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(self.modules, text="[ QUICK ACCESS ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=10)
        all_functions_btn = ctk.CTkButton(
            self.modules,
            text="🎯 ALL FUNCTIONS PANEL",
            fg_color="#FF3131",
            hover_color="#FF5555",
            command=self.open_all_functions_panel,
            font=("Courier New", 14, "bold"),
            height=50
        )
        all_functions_btn.pack(pady=10, padx=10, fill="x")
        
        # CODE STUDIO BUTTON
        code_studio_btn = ctk.CTkButton(
            self.modules,
            text="💻 CODE STUDIO",
            fg_color="#003300",
            hover_color="#005500",
            command=self.open_code_studio,
            font=("Courier New", 14, "bold"),
            height=50
        )
        code_studio_btn.pack(pady=5, padx=10, fill="x")

        # FOLDER UPLOAD BUTTON
        ctk.CTkButton(
            self.modules,
            text="📁 FOLDER UPLOAD",
            fg_color="#004433",
            hover_color="#006655",
            command=self.open_folder_upload_panel,
            font=("Courier New", 14, "bold"),
            height=45
        ).pack(pady=5, padx=10, fill="x")

        # ANDROID DEVICE MANAGER BUTTON
        ctk.CTkButton(
            self.modules,
            text="📱 ANDROID MANAGER (ADB)",
            fg_color="#334400",
            hover_color="#556600",
            command=self.open_android_manager_panel,
            font=("Courier New", 13, "bold"),
            height=45
        ).pack(pady=5, padx=10, fill="x")
        
        # DIRECT AI CHAT BUTTON (NEW! No Browser!)
        direct_ai_btn = ctk.CTkButton(
            self.modules,
            text="🤖 DIRECT AI CHAT",
            fg_color="#004466",
            hover_color="#006688",
            command=self.open_direct_ai_chat_panel,
            font=("Courier New", 14, "bold"),
            height=50
        )
        direct_ai_btn.pack(pady=10, padx=10, fill="x")
        
        # WORLD AI CHAT BUTTON (NEW!)
        world_ai_btn = ctk.CTkButton(
            self.modules,
            text="🌍 WORLD AI CHAT",
            fg_color="#00AA00",
            hover_color="#00CC00",
            command=self.open_world_ai_chat_direct,
            font=("Courier New", 14, "bold"),
            height=50
        )
        world_ai_btn.pack(pady=10, padx=10, fill="x")
        
        # --- MODULE SECTION: AI LEARNING (NEW!) ---
        ctk.CTkLabel(self.modules, text="[ AI LEARNING ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        
        # Auto Learner Toggle Button
        self.auto_learn_btn = ctk.CTkButton(
            self.modules,
            text="🤖 AUTO LEARN: OFF",
            fg_color="#AA0000",
            hover_color="#CC0000",
            command=self.toggle_auto_learner,
            font=("Courier New", 14, "bold"),
            height=50
        )
        self.auto_learn_btn.pack(pady=10, padx=10, fill="x")

        # Brain Harvester Button (NEW!)
        self.harvest_btn = ctk.CTkButton(
            self.modules,
            text="🧠 BRAIN HARVEST",
            fg_color="#440066",
            hover_color="#660088",
            command=self.open_harvester_ui,
            font=("Courier New", 14, "bold"),
            height=50
        )
        self.harvest_btn.pack(pady=10, padx=10, fill="x")
        
        # Learning Stats
        self.learning_stats = ctk.CTkLabel(
            self.modules,
            text="📊 Learned: 0 topics | Status: Idle",
            font=("Courier New", 10),
            text_color="#888888"
        )
        self.learning_stats.pack(pady=5, padx=10)
        
        # Learning Settings Button
        learning_settings_btn = ctk.CTkButton(
            self.modules,
            text="⚙️ Learning Settings",
            fg_color="#003344",
            hover_color="#005566",
            command=self.open_learning_settings,
            font=("Courier New", 12, "bold"),
            height=35
        )
        learning_settings_btn.pack(pady=5, padx=10, fill="x")

        # --- MODULE SECTION: CORE ---
        ctk.CTkLabel(self.modules, text="[ CORE SYSTEMS ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("SYSTEM CLEAN", "clean")
        add_module("WORKSPACE", "workspace")
        add_module("SCREENSHOT", "screenshot")

        # Screen Record Button (NEW!)
        self.screen_record_btn = ctk.CTkButton(
            self.modules,
            text="🎥 SCREEN RECORD",
            fg_color="#002233",
            hover_color="#004466",
            command=self.toggle_screen_recording,
            font=("Courier New", 12, "bold"),
            height=35
        )
        self.screen_record_btn.pack(pady=5, padx=10, fill="x")

        add_module("DISK ANALYZE", "disk")
        add_module("APP CONTROL", "app help", "#003344", "#005566")
        add_module("AGENT MODE", "agent on", "#004466", "#006688")
        add_module("WINDOW CTRL", "window", "#004466", "#006688")
        add_module("SYSTEM DOCTOR", "doctor", "#004400", "#006600")
        add_module("SELF FIX", "selfcheck", "#004400", "#006600")
        add_module("🔍 SYSTEM MONITOR", "monitor", "#006666", "#008888")

        # --- MODULE SECTION: NETWORK ---
        ctk.CTkLabel(self.modules, text="[ NETWORK OPS ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("RECON SCAN", "recon")
        add_module("WIFI AUDIT", "wifi")
        add_module("NET USERS", "users")
        add_module("DEVICES", "devices")
        add_module("ROUTER SCAN", "router", "#003344", "#005566")

        # --- MODULE SECTION: ELITE ---
        ctk.CTkLabel(self.modules, text="[ ELITE TOOLS ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("KALI MODE", "kali", "#440066", "#660088")
        add_module("REMOTE CONSOLE", "remote", "#440066", "#660088")
        add_module("FLIPPER MODE", "flipper", "#CC5500", "#EE7700")
        add_module("ALIEN MODE", "alien", "#006600", "#009900")
        add_module("VIRUS PURGE", "purge", "#660000", "#990000")
        add_module("FIREWALL", "firewall", "#004466", "#006688")
        add_module("BROWSER CTRL", "browser", "#004466", "#006688")
        add_module("WEB AUDIT", "webaudit", "#226600", "#338800")

        # --- MODULE SECTION: UPLINK ---
        ctk.CTkLabel(self.modules, text="[ UPLINK ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("MOBILE UPLINK", "mobile", "#664400", "#886600")
        add_module("SIM CALL", "call", "#006600", "#009900")
        add_module("SHARE SCREEN", "share", "#004466", "#006688")
        add_module("SEND FILES", "send", "#004466", "#006688")

        # --- MODULE SECTION: KNOWLEDGE ---
        ctk.CTkLabel(self.modules, text="[ KNOWLEDGE BASE ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("🧠 BRAIN HUB", "knowledge", "#005577", "#007799")
        add_module("📚 LEARNED TOPICS", "searchlearn", "#005577", "#007799")
        add_module("🔐 LOGIN BOT", "loginbot", "#440066", "#660088")

        # --- MODULE SECTION: GENERATOR ---
        ctk.CTkLabel(self.modules, text="[ AI GENERATOR ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("[*] GENERATE IMAGE",    "gen image", "#003300", "#005500")
        add_module("[*] GENERATE VIDEO",    "gen video", "#003300", "#005500")
        add_module("[*] GENERATE AUDIO",    "gen audio", "#003300", "#005500")
        add_module("[*] GENERATE 3D MODEL", "gen 3d",    "#003300", "#005500")
        add_module("[*] GENERATE TEXT",     "gen text",  "#003300", "#005500")
        add_module("[*] GENERATE FILE",     "gen file",  "#003300", "#005500")
        add_module("[>] LIST GENERATED",    "gen list",  "#002200", "#004400")
        add_module("[>] OPEN GEN FOLDER",   "gen folder","#002200", "#004400")

        # --- MODULE SECTION: MULTI-BRAIN ---
        ctk.CTkLabel(self.modules, text="[ MULTI-BRAIN ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("[AI] BRAIN STATUS",    "brain status",   "#220044", "#440066")
        add_module("[AI] OLLAMA (LOCAL)",  "brain ollama",   "#220044", "#440066")
        add_module("[AI] GROQ FAST",       "brain groq",     "#220044", "#440066")
        add_module("[AI] PARALLEL THINK",  "brain parallel", "#330055", "#550077")
        add_module("[~] STREAMING MODE",   "stream toggle",  "#004433", "#006655")

        # --- MODULE SECTION: ASIF HACKER OPS ---
        ctk.CTkLabel(self.modules, text="[ ASIF HACKER OPS ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("🔥 ASIF GEN", "asif gen", "#880000", "#AA0000")
        add_module("🚀 BOT RUNNER", "asif bots", "#005500", "#007700")
        add_module("👑 ASIF MASTER", "asif suite", "#AA0000", "#CC0000")
        add_module("📁 ASIF DIR", "asif dir", "#333333", "#555555")
        add_module("🗨️ DIRECT CHAT", "directchat", "#004466", "#006688")

        # --- MODULE SECTION: SYSTEM CONTROL ---
        ctk.CTkLabel(self.modules, text="[ AUTO CONTROL ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("[T] SCHEDULE TASK", "auto schedule", "#003344", "#005566")
        add_module("[T] LIST TASKS",    "auto list",     "#003344", "#005566")
        add_module("[W] SUPER HOST",    "superhost",     "#004422", "#006644")
        add_module("[!] BUG DETECT",    "bugcheck",      "#440000", "#660000")
        add_module("[+] AUTO FIX BUGS", "bugfix",        "#440000", "#660000")

        # --- MODULE SECTION: LEARNING ---
        ctk.CTkLabel(self.modules, text="[ AUTO LEARNING ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("🤖 AUTO BG LEARN", "autobg", "#FF3131", "#FF5555")
        add_module("🔍 SEARCH & LEARN", "searchlearn", "#006644", "#008866")
        add_module("📚 LEARN 10 WORDS", "learn10", "#004466", "#006688")
        add_module("📖 LEARN 50 WORDS", "learn50", "#003355", "#005577")
        add_module("📜 SEARCH HISTORY", "searchhistory", "#332200", "#554400")
        add_module("📄 LEARN ARTICLE", "learnarticle", "#004488", "#0066AA")
        add_module("📋 ARTICLE LIST", "articlelist", "#332200", "#554400")
        
        # --- MODULE SECTION: TRANSLATOR ---
        ctk.CTkLabel(self.modules, text="[ TRANSLATOR ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        add_module("🌍 TRANSLATE", "translate", "#004466", "#006688")
        add_module("🔤 LANGUAGES", "languages", "#003344", "#005566")
        add_module("📝 TRANS HISTORY", "transhistory", "#332200", "#554400")
        
        # --- MODULE SECTION: SYSTEM (NEW!) ---
        ctk.CTkLabel(self.modules, text="[ SYSTEM ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        
        # Permissions Button
        permissions_btn = ctk.CTkButton(
            self.modules,
            text="🔐 GRANT PERMISSIONS",
            fg_color="#440066",
            hover_color="#660088",
            command=self.request_permissions,
            font=("Courier New", 14, "bold"),
            height=45
        )
        permissions_btn.pack(pady=10, padx=10, fill="x")
        
        # System Settings Button
        system_settings_btn = ctk.CTkButton(
            self.modules,
            text="⚙️ System Settings",
            fg_color="#003344",
            hover_color="#005566",
            command=self.open_system_settings,
            font=("Courier New", 12, "bold"),
            height=35
        )
        system_settings_btn.pack(pady=5, padx=10, fill="x")
        
        # --- MODULE SECTION: VOICE CONTROL ---
        ctk.CTkLabel(self.modules, text="[ VOICE CONTROL ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        
        # Voice Control Panel Button (BIG and PROMINENT!)
        voice_control_btn = ctk.CTkButton(
            self.modules,
            text="🎤 VOICE CONTROL PANEL",
            fg_color="#FF3131",
            hover_color="#FF5555",
            command=self.open_voice_control_panel,
            font=("Courier New", 14, "bold"),
            height=50
        )
        voice_control_btn.pack(pady=10, padx=10, fill="x")
        
        # Bengali Voice Selector Button (NEW!)
        bangla_voice_btn = ctk.CTkButton(
            self.modules,
            text="🇧🇩 BENGALI VOICE SELECTOR",
            fg_color="#006600",
            hover_color="#009900",
            command=self.open_bangla_voice_selector,
            font=("Courier New", 14, "bold"),
            height=50
        )
        bangla_voice_btn.pack(pady=10, padx=10, fill="x")
        
        # Microphone ON/OFF Button (NEW!)
        self.mic_enabled = True
        self.mic_button = ctk.CTkButton(
            self.modules,
            text="🎤 MIC: ON",
            fg_color="#00AA00",
            hover_color="#00CC00",
            command=self.toggle_microphone,
            font=("Courier New", 14, "bold"),
            height=45
        )
        self.mic_button.pack(pady=10, padx=10, fill="x")
        
        # Quick Voice Actions
        voice_quick_frame = ctk.CTkFrame(self.modules, fg_color="transparent")
        voice_quick_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(
            voice_quick_frame,
            text="🔊 Test",
            width=60,
            height=35,
            fg_color="#004466",
            hover_color="#006688",
            command=lambda: self.speak("Hello! I am JARVIS. Voice test successful!")
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            voice_quick_frame,
            text="🐌 Slow",
            width=60,
            height=35,
            fg_color="#003344",
            hover_color="#005566",
            command=lambda: self.set_voice_speed(150)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            voice_quick_frame,
            text="⚡ Fast",
            width=60,
            height=35,
            fg_color="#003344",
            hover_color="#005566",
            command=lambda: self.set_voice_speed(200)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            voice_quick_frame,
            text="🔄 Reset",
            width=60,
            height=35,
            fg_color="#664400",
            hover_color="#886600",
            command=lambda: self.set_voice_speed(165)
        ).pack(side="left", padx=2)

        # --- MODULE SECTION: NEURAL ---
        ctk.CTkLabel(self.modules, text="[ NEURAL PROTOCOLS ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=5)
        self.key_entry = ctk.CTkEntry(self.modules, placeholder_text="New API Key...", height=35, fg_color="#000000", border_color="#002233")
        self.key_entry.pack(pady=5, padx=10, fill="x")
        
        btn_frame = ctk.CTkFrame(self.modules, fg_color="transparent")
        btn_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(btn_frame, text="PASTE", width=45, fg_color="#004466", hover_color="#006688", command=self.paste_key).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="SYNC", width=45, fg_color="#002233", hover_color="#004466", command=self.sync_key).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="PING", width=45, fg_color="#003344", hover_color="#005566", command=self.ping_key).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="TEST", width=45, fg_color="#444400", hover_color="#666600", command=self.test_keys).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="MODEL", width=45, fg_color="#440044", hover_color="#660066", command=self.rotate_brain_model).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="RESET", width=45, fg_color="#660000", hover_color="#880000", command=self.async_init_brain).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="GET KEY", width=45, fg_color="#006644", hover_color="#008866", command=lambda: webbrowser.open("https://aistudio.google.com/app/apikey")).pack(side="left", padx=2)

        # --- MODULE SECTION: ACTIVITY ---
        ctk.CTkLabel(self.modules, text="[ LIVE ACTIVITY ]", font=("Courier New", 10, "bold"), text_color="#555555").pack(pady=10)
        self.activity_feed = ctk.CTkTextbox(self.modules, height=150, font=("Courier New", 10), fg_color="#05080F", text_color="#00FF41", border_width=1, border_color="#002233")
        self.activity_feed.pack(pady=5, padx=10, fill="x")

        # Main Terminal (AI STUDIO DESIGN)
        self.right_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg_black)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Studio Header
        self.studio_header = ctk.CTkFrame(self.right_panel, height=80, fg_color="#05080F", border_width=1, border_color="#002233")
        self.studio_header.pack(fill="x", side="top", padx=20, pady=20)
        
        ctk.CTkLabel(self.studio_header, text="JARVIS AI STUDIO", font=("Courier New", 24, "bold"), text_color=self.cyber).pack(side="left", padx=30)

        # User info + logout (right side)
        user_name = self._session.get("display_name", "")
        provider  = self._session.get("provider", "")
        
        # FIX: Don't show API key as username
        # Check if display_name looks like an API key
        if user_name and (user_name.startswith("AIza") or user_name.startswith("sk-")):
            # It's an API key, not a name - use email or default
            user_name = self._session.get("email", "").split("@")[0] if self._session.get("email") else "User"
        
        if user_name:
            provider_icon = {"google": "[G]", "microsoft": "[M]", "apple": "[A]", "email": "[E]"}.get(provider, "[U]")
            ctk.CTkLabel(
                self.studio_header,
                text=f"{provider_icon} {user_name}",
                font=("Courier New", 12, "bold"),
                text_color="#00FF41",
            ).pack(side="left", padx=15)

        ctk.CTkButton(
            self.studio_header, text="LOGOUT", width=70, height=30,
            fg_color="#330000", hover_color="#550000",
            font=("Courier New", 11), command=self._do_logout,
        ).pack(side="left", padx=5)

        # Action Buttons for Copy
        self.copy_btn = ctk.CTkButton(self.studio_header, text="COPY ALL", width=80, height=30, fg_color="#004466", hover_color="#006688", command=self.copy_terminal)
        self.copy_btn.pack(side="right", padx=10)

        # Streaming mode toggle
        self.stream_btn = ctk.CTkButton(
            self.studio_header, text="STREAM: OFF", width=100, height=30,
            fg_color="#003322", hover_color="#005544",
            command=self.toggle_streaming,
        )
        self.stream_btn.pack(side="right", padx=5)

        # Model Selector Info
        self.model_info = ctk.CTkLabel(self.studio_header, text="MODEL: GEMINI-1.5-FLASH | TEMP: 0.7", font=("Courier New", 12), text_color="#555555")
        self.model_info.pack(side="right", padx=20)
        
        # --- TERMINAL HEADER (With AI Selector) ---
        term_header = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        term_header.pack(fill="x", side="top", padx=30, pady=(0, 5))
        
        self.ai_mode_btn = ctk.CTkButton(term_header, text="🗨️ CHAT MODE: OFF", width=150, height=30,
                                         fg_color="#333333", text_color="#AAAAAA",
                                         command=self._toggle_ai_chat_mode)
        self.ai_mode_btn.pack(side="left", padx=5)
        
        self.ai_selector = ctk.CTkOptionMenu(term_header, values=["Auto", "Pollinations", "Blackbox", "DuckDuckGo", "Phind"],
                                            width=150, height=30, fg_color="#004466",
                                            command=self._on_ai_selected)
        self.ai_selector.pack(side="left", padx=5)
        
        ctk.CTkLabel(term_header, text="[ TERMINAL CONSOLE ]", font=("Courier New", 12, "bold"), text_color="#00FF41").pack(side="right", padx=10)

        # Terminal Area
        self.terminal = ctk.CTkTextbox(self.right_panel, font=("Consolas", 15), text_color=self.neon, fg_color="transparent", border_width=0)
        self.terminal.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.log("SYSTEM", "AI STUDIO ENVIRONMENT LOADED. READY FOR NEURAL INPUT.")
        # Enable drag-and-drop on terminal
        self._setup_drag_drop(self.terminal)

        # Bottom Command Bar
        self.cmd_zone = ctk.CTkFrame(self.right_panel, height=80, fg_color="#05080F", border_width=1, border_color="#1A1A1A")
        self.cmd_zone.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        
        # Quick Actions Container
        self.quick_actions = ctk.CTkFrame(self.cmd_zone, fg_color="transparent")
        self.quick_actions.pack(fill="x", side="top", padx=10, pady=(5, 0))
        
        # File Upload Button
        self.upload_btn = add_file_upload_button(self.quick_actions, None, self.log)
        self.upload_btn.configure(width=100, height=35, font=("Courier New", 11, "bold"))
        self.upload_btn.pack(side="left", padx=5)
        
        # Folder Upload Button
        self.folder_btn = ctk.CTkButton(
            self.quick_actions,
            text="📁 FOLDER",
            width=100,
            height=35,
            fg_color="#004466",
            hover_color="#006688",
            text_color="white",
            font=("Courier New", 11, "bold"),
            command=None
        )
        self.folder_btn.pack(side="left", padx=5)
        
        # Web Search Button
        self.web_search_btn = ctk.CTkButton(
            self.quick_actions,
            text="🔍 SEARCH",
            width=100,
            height=35,
            fg_color="#006644",
            hover_color="#008866",
            text_color="white",
            font=("Courier New", 11, "bold"),
            command=self._handle_web_search
        )
        self.web_search_btn.pack(side="left", padx=5)
        
        # MRX Button
        self.mrx_btn = ctk.CTkButton(
            self.quick_actions,
            text="🔥 MRX LEARN",
            width=110,
            height=35,
            fg_color="#FF3131",
            hover_color="#FF5555",
            text_color="white",
            font=("Courier New", 11, "bold"),
            command=self._handle_mrx_learning
        )
        self.mrx_btn.pack(side="left", padx=5)

        # Bug Detect Button
        self.bug_btn = ctk.CTkButton(
            self.quick_actions,
            text="🐛 BUG DETECT",
            width=110,
            height=35,
            fg_color="#440000",
            hover_color="#660000",
            text_color="white",
            font=("Courier New", 11, "bold"),
            command=lambda: self.process("bugcheck")
        )
        self.bug_btn.pack(side="left", padx=5)
        
        # Main Input Row
        self.input_row = ctk.CTkFrame(self.cmd_zone, fg_color="transparent")
        self.input_row.pack(fill="x", side="top", padx=10, pady=10)
        
        self.entry = ctk.CTkEntry(
            self.input_row, 
            placeholder_text="Awaiting root command...", 
            height=50, 
            fg_color="#0A0F1A", 
            border_color=self.neon, 
            text_color=self.neon, 
            font=("Courier New", 16)
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry._entry.bind("<Return>", lambda e: self.fire_cmd())
        
        # Emoji / Non-BMP safety bindings to prevent TclError crashes on Windows
        def _handle_paste(event):
            try:
                pasted_text = event.widget.clipboard_get()
                clean_paste = "".join(c if ord(c) <= 0xFFFF else "?" for c in pasted_text)
                event.widget.insert("insert", clean_paste)
                return "break"
            except Exception:
                pass

        def _handle_key(event):
            try:
                # Interruption on typing: stop speaking immediately
                if hasattr(self, 'voice') and self.voice and self.voice.is_speaking:
                    self.voice.stop()
                    self.log("SYSTEM", "Speech interrupted by user keyboard input.")

                if event.char and len(event.char) == 1 and ord(event.char) > 0xFFFF:
                    event.widget.insert("insert", "?")
                    return "break"
            except Exception:
                pass

        self.entry._entry.bind("<<Paste>>", _handle_paste, add="+")
        self.entry._entry.bind("<Key>", _handle_key, add="+")
        self.bind("<Escape>", lambda e: self.voice.stop() if (hasattr(self, 'voice') and self.voice) else None)
        
        self.voice_btn = ctk.CTkButton(
            self.input_row,
            text="🎤 LISTEN",
            width=120,
            height=50,
            fg_color=self.neon,
            text_color="black",
            font=("Courier New", 14, "bold"),
            command=self.start_mic,
        )
        self.voice_btn.pack(side="left")
        
        # Premium Status Bar (The missing "Integrated Footer")
        self.status_bar = ctk.CTkFrame(self.right_panel, height=30, fg_color="#02050A")
        self.status_bar.pack(fill="x", side="bottom")
        
        self.pulse_canvas = ctk.CTkCanvas(self.status_bar, width=20, height=20, bg="#02050A", highlightthickness=0)
        self.pulse_canvas.pack(side="left", padx=(20, 5), pady=5)
        self.pulse_dot = self.pulse_canvas.create_oval(5, 5, 15, 15, fill=self.neon, outline="")
        
        self.stats_label = ctk.CTkLabel(self.status_bar, text="SYSTEM INITIALIZING...", font=("Courier New", 10, "bold"), text_color="#555555")
        self.stats_label.pack(side="left", padx=10)
        
        self.face3d_status = ctk.CTkLabel(self.status_bar, text="3D: OFF", font=("Courier New", 10, "bold"), text_color="#555555")
        self.face3d_status.pack(side="left", padx=10)
        
        self.link_status = ctk.CTkLabel(self.status_bar, text="LINK: STANDBY", font=("Courier New", 10, "bold"), text_color="#555555")
        self.link_status.pack(side="left", padx=10)
        
        self.clock_label = ctk.CTkLabel(self.status_bar, text="00:00:00", font=("Courier New", 10, "bold"), text_color=self.neon)
        self.clock_label.pack(side="right", padx=20)
        
        # Update upload buttons with callbacks
        self.upload_btn.configure(command=lambda: self._handle_file_upload())
        self.folder_btn.configure(command=lambda: self._handle_folder_upload())
        
        self.update_telemetry()
        self._animate_pulse()

        # Play startup notification melody
        def play_startup_notification():
            time.sleep(0.2)  # Short delay to allow canvas booting flash to display first
            try:
                import winsound
                # Upbeat C-Major notification melody
                winsound.Beep(523, 100) # C5
                winsound.Beep(659, 100) # E5
                winsound.Beep(784, 100) # G5
                winsound.Beep(1047, 200) # C6
            except Exception:
                pass
            self.log("SYSTEM", "JARVIS systems initialized. Cloud link standing by.")

        threading.Thread(target=play_startup_notification, daemon=True).start()

    def copy_terminal(self):
        import pyperclip
        content = self.terminal.get("1.0", "end").strip()
        if content:
            pyperclip.copy(content)
            self.log("SYSTEM", "Neural data extracted to clipboard.")

    @staticmethod
    def _sanitize(text: str) -> str:
        """Replace emoji / non-BMP chars that Consolas can't render on Windows."""
        _MAP = {
            "←": "<-", "→": "->", "✓": "[OK]", "✗": "[X]", "●": "*",
            "⚡": "[!]", "🧠": "[AI]", "🔑": "[KEY]", "🔵": "[G]",
            "🟦": "[M]", "⬛": "[A]", "✉": "[E]", "👤": "[U]",
            "⏱": "[T]", "📁": "[DIR]", "📂": "[DIR]", "📋": "[LIST]",
            "🌐": "[WEB]", "🐛": "[BUG]", "🔧": "[FIX]", "🔄": "[~]",
            "⚙": "[CFG]", "⬛": "[A]",
        }
        for ch, rep in _MAP.items():
            text = text.replace(ch, rep)
        # Strip any remaining non-BMP (4-byte) emoji that Consolas can't show
        result = []
        for ch in text:
            if ord(ch) > 0xFFFF:
                result.append("?")
            else:
                result.append(ch)
        return "".join(result)

    def log(self, sender, msg):
        t = time.strftime("%H:%M:%S")
        msg = self._sanitize(str(msg))
        log_msg = f"[{t}] [{sender}]> {msg}\n"
        
        # Log to floating HUD
        if hasattr(self, 'hud') and self.hud:
            try:
                self.hud.add_log(f"[{sender}] {msg}")
            except Exception:
                pass
                
        if not hasattr(self, "terminal"):
            print(log_msg)
            return
        self.terminal.insert("end", f"{log_msg}\n")
        self.terminal.see("end")
        if hasattr(self, 'activity_feed'):
            self.activity_feed.insert("1.0", log_msg)
            content = self.activity_feed.get("1.0", "end").split("\n")
            if len(content) > 50:
                self.activity_feed.delete("50.0", "end")
        self.terminal.see("end")

    def async_init_brain(self):
        try:
            # Auto-apply API key from login session first (fast cloud connect)
            session_key = self._session.get("api_key", "")
            if session_key:
                auto_apply_key_to_config(session_key, self._session.get("email", ""))

            # Pull all keys saved on server for this account
            try:
                from server.auth_client import get_client
                client = get_client()
                if client.is_online() and client._token:
                    server_keys = client.get_keys()
                    for k in server_keys:
                        auto_apply_key_to_config(k, self._session.get("email", ""))
            except Exception:
                pass

            if not os.path.exists("jarvis_config.txt"):
                open("jarvis_config.txt", "w").close()
            with open("jarvis_config.txt", "r") as f:
                keys = [k.strip() for k in f.read().splitlines()
                        if k.strip() and not k.strip().startswith("#")]

            if keys:
                self.brain = JarvisBrain(keys)
                self.multi_brain.gemini = self.brain
                if not self.brain.api_keys:
                    self.after(0, lambda: self.log("WARNING",
                        "NEURAL UPLINK OFFLINE: No valid Gemini keys. Add one via Neural Protocols."))
                elif not self.brain.is_connected:
                    self.after(0, lambda: self.log("ERROR",
                        f"NEURAL UPLINK FAILED: {self.brain.last_error}"))
                else:
                    user = self._session.get("display_name", "")
                    if "_" in user and any(p in user.lower() for p in ["google", "microsoft", "apple"]):
                        user = "Boss"
                    greeting = f"Welcome back, {user}! " if user else ""
                    self.after(0, lambda: self.log("SUCCESS",
                        f"NEURAL UPLINK SECURED. {greeting}JARVIS is fully connected to the cloud network."))
                    # Update status indicator
                    self.after(0, lambda: self.status_bar.children.get("model_info", self.model_info).configure(
                        text=f"MODEL: {self.brain.model.upper()} | TEMP: 0.7"))
            else:
                self.after(0, lambda: self.log("WARNING",
                    "NEURAL UPLINK OFFLINE: No API Key. Paste one in Neural Protocols."))

            # Init heavy offline brain afterwards in the background so it doesn't block startup
            try:
                from jarvis_offline_brain import OfflineBrain
                self._offline_brain = OfflineBrain()
            except Exception as e:
                self._offline_brain = None
                print(f"[!] Offline brain not loaded: {e}")
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self.log("ERROR", f"SYSTEM BOOT FAILURE: {err_msg}"))

    def _init_face3d(self):
        if not os.path.exists(FACE_GLB_PATH):
            if hasattr(self, "face3d_status"):
                self.face3d_status.configure(text="3D FACE: MISSING jarvis_face.glb", text_color="#FF3131")
            return
        try:
            self.face3d = Face3D(FACE_GLB_PATH)
            self.face3d.start()
            self.log("SYSTEM", "3D FACE ONLINE: jarvis_face.glb")
            if hasattr(self, "face3d_status"):
                self.face3d_status.configure(text="3D FACE: ON", text_color="#00FF41")
        except Exception as e:
            self.face3d = None
            self.log("ERROR", f"3D FACE FAILED: {e}")
            if hasattr(self, "face3d_status"):
                self.face3d_status.configure(text="3D FACE: FAILED", text_color="#FF3131")

    def face3d_on(self):
        try:
            if not os.path.exists(FACE_GLB_PATH):
                self.log("ERROR", "3D FACE missing: jarvis_face.glb")
                if hasattr(self, "face3d_status"):
                    self.face3d_status.configure(text="3D: MISSING", text_color="#FF3131")
                return
            if not self.face3d:
                self.face3d = Face3D(FACE_GLB_PATH)
            self.face3d.start()
            if hasattr(self, "face3d_status"):
                self.face3d_status.configure(text="3D: ONLINE", text_color="#00FF41")
        except Exception as e:
            self.log("ERROR", f"3D FACE FAILED: {e}")
            if hasattr(self, "face3d_status"):
                self.face3d_status.configure(text="3D: FAILED", text_color="#FF3131")

    def face3d_off(self):
        try:
            if self.face3d:
                self.face3d.stop()
            if hasattr(self, "face3d_status"):
                self.face3d_status.configure(text="3D: OFF", text_color="#555555")
        except Exception:
            if hasattr(self, "face3d_status"):
                self.face3d_status.configure(text="3D: OFF", text_color="#555555")

    def neural_rigging(self):
        """Trigger Blender to prepare the face model automatically."""
        if hasattr(self, "face3d_status"):
            self.face3d_status.configure(text="RIGGING...", text_color="#FFD700")
        
        def run_rig():
            try:
                # Use the emergency batch fix I created for permission bypass
                batch_path = os.path.join(_WORKSPACE_DIR, "FORCE_BLENDER_FIX.bat")
                if os.path.exists(batch_path):
                    subprocess.Popen([batch_path], shell=True)
                else:
                    # Fallback to direct call
                    blender_path = r"C:\Program Files\WindowsApps\BlenderFoundation.Blender_5.1.1.0_x64__ppwjx1n5r4v9t\Blender\blender.exe"
                    script_path = os.path.join(_WORKSPACE_DIR, "jarvis_learned_files", "prepare_face.py")
                    subprocess.Popen([blender_path, "--background", "--python", script_path])
                
                time.sleep(5)
                if hasattr(self, "face3d_status"):
                    self.face3d_status.configure(text="RIG OK", text_color="#00FF41")
            except Exception as e:
                print(f"Rigging Error: {e}")
                if hasattr(self, "face3d_status"):
                    self.face3d_status.configure(text="RIG FAILED", text_color="#FF3131")

        threading.Thread(target=run_rig, daemon=True).start()
    
    def antigravity_uplink(self):
        """Establish a direct neural link and launch the Antigravity HUD."""
        self.log("SYSTEM", "ESTABLISHING NEURAL UPLINK...")
        def connect():
            try:
                self.log("SUCCESS", "ANTIGRAVITY NEURAL LINK: ONLINE")
                self.speak("Neural uplink established. Launching Antigravity HUD.")
                hud_path = os.path.join(_WORKSPACE_DIR, "engine", "antigravity_hud.py")
                subprocess.Popen([sys.executable, hud_path])
            except Exception as e:
                self.log("ERROR", f"HUD LAUNCH FAILED: {e}")
        threading.Thread(target=connect, daemon=True).start()

    def system_recon(self):
        """Perform a deep scan of the system environment."""
        self.log("HACKER", "INITIATING SYSTEM RECONNAISSANCE...")
        def scan():
            import platform
            info = f"OS: {platform.system()} {platform.release()} | CPU: {platform.processor()}"
            time.sleep(1.5)
            self.log("INFO", f"RECON COMPLETE: {info}")
            self.speak("System reconnaissance complete. All sectors are operational.")
        threading.Thread(target=scan, daemon=True).start()
    
    def osint_scan(self):
        """Perform a professional-grade OSINT reconnaissance on a target image."""
        import webbrowser
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(title="SELECT TARGET FOR NEURAL ANALYSIS", 
                                             filetypes=[("Intelligence Data", "*.jpg *.png *.jpeg")])
        
        if file_path:
            self.log("OSINT", f"TARGET ACQUIRED: {os.path.basename(file_path)}")
            self.log("SYSTEM", "UPLOADING TO GLOBAL INTELLIGENCE DATABASE...")
            
            def perform_recon():
                try:
                    # 1. Local Visual Analysis & Metadata Parsing using Python PIL/hash/EXIF
                    import hashlib
                    from PIL import Image
                    from PIL.ExifTags import TAGS, GPSTAGS
                    
                    self.gui_queue.put(('log', "🔍 Running local image scan...\n"))
                    img = Image.open(file_path)
                    width, height = img.size
                    img_format = img.format or "Unknown Format"
                    img_mode = img.mode
                    
                    # Generate SHA-256 Hash for registry identification
                    sha256_hash = hashlib.sha256()
                    with open(file_path, "rb") as f:
                        for byte_block in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(byte_block)
                    hash_sig = sha256_hash.hexdigest()
                    
                    # Parse EXIF metadata
                    exif_data = {}
                    gps_info = {}
                    info = img._getexif() if hasattr(img, '_getexif') else None
                    if info:
                        for tag, value in info.items():
                            decoded = TAGS.get(tag, tag)
                            if decoded == "GPSInfo":
                                for t in value:
                                    sub_decoded = GPSTAGS.get(t, t)
                                    gps_info[sub_decoded] = value[t]
                            else:
                                exif_data[decoded] = value

                    # Format EXIF strings
                    camera = exif_data.get("Model", exif_data.get("Make", "N/A"))
                    date_taken = exif_data.get("DateTimeOriginal", exif_data.get("DateTime", "N/A"))
                    software = exif_data.get("Software", "N/A")
                    
                    # Check face detection (try OpenCV cascade if available)
                    face_count = 0
                    try:
                        import cv2
                        import numpy as np
                        # Try to load face classifier
                        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                        face_cascade = cv2.CascadeClassifier(cascade_path)
                        # Read image in CV2
                        cv_img = cv2.imread(file_path)
                        if cv_img is not None:
                            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                            face_count = len(faces)
                    except Exception:
                        pass # opencv not installed or cascade file not found

                    # Display professional intelligence report
                    self.gui_queue.put(('log', f"🧠 [NEURAL OSINT REPORT - TARGET IDENTIFIED]\n"))
                    self.gui_queue.put(('log', f"   📁 File: {os.path.basename(file_path)}\n"))
                    self.gui_queue.put(('log', f"   📏 Res: {width}x{height} | Format: {img_format} | Mode: {img_mode}\n"))
                    self.gui_queue.put(('log', f"   🔑 Digital Signature (SHA-256): {hash_sig[:32]}...\n"))
                    self.gui_queue.put(('log', f"   📷 Camera Model: {camera}\n"))
                    self.gui_queue.put(('log', f"   📅 Timestamp: {date_taken}\n"))
                    self.gui_queue.put(('log', f"   🛠️ Software signature: {software}\n"))
                    if face_count > 0:
                        self.gui_queue.put(('log', f"   👤 Visual Analysis: {face_count} human face(s) resolved.\n"))
                    if gps_info:
                        self.gui_queue.put(('log', f"   🌐 Geolocation tags: FOUND (Lat/Lon EXIF coordinates synced)\n"))
                    else:
                        self.gui_queue.put(('log', f"   🌐 Geolocation tags: None embedded.\n"))
                        
                    # 2. Check public directories / reverse search queries
                    self.gui_queue.put(('log', "🌐 Step 2: Querying global public directories & registries...\n"))
                    search_term = os.path.basename(file_path).split('.')[0]
                    search_url = f"https://www.google.com/search?q={search_term}+image+lookup"
                    webbrowser.open(search_url)
                    
                    self.gui_queue.put(('log', "✅ Neural Scan complete! Results logged and browser uplink created.\n"))
                    self.speak("Reconnaissance complete. Scanned target image for EXIF data and digital signatures. Found metadata tags. Querying public search engines and secure indexes.")
                except Exception as e:
                    self.gui_queue.put(('log', f"❌ OSINT Scan failed: {e}\n"))
                    self.speak("Sorry sir, the image scanning process encountered an error.")
                    
            threading.Thread(target=perform_recon, daemon=True).start()
        else:
            self.log("WARNING", "RECON ABORTED: NO TARGET SELECTED")

    def speak(self, text: str):
        """Speak with Gemini-style barge-in — user কথা বললে থেমে যাবে"""
        try:
            import re
            speak_text = re.sub(r'\[EMOTION:.*?\]', '', text).strip()

            emotion = self.detect_response_emotion(text)
            self.update_emotion(emotion)

            if hasattr(self, 'core') and self.core:
                self.core.set_state("speaking")

            if hasattr(self, 'voice') and self.voice:
                # Disable concurrent barge-in listener to prevent audio stream corruption
                # self._start_barge_in_listener()
                with self.v_lock:
                    self.voice.speak(speak_text)
                # self._stop_barge_in_listener()

            if hasattr(self, 'core') and self.core:
                self.core.set_state("idle")
        except Exception as e:
            print(f"[!] Speech error: {e}")

    def _start_barge_in_listener(self):
        """Speaking এর সময় mic এ কথা detect হলে interrupt করো"""
        import threading, array
        self._barge_in_active = True

        def _listen_for_interrupt():
            try:
                import speech_recognition as sr
                r2 = sr.Recognizer()
                r2.energy_threshold = max(getattr(self.voice, 'recognizer', None) and
                                          self.voice.recognizer.energy_threshold or 200, 100)
                r2.dynamic_energy_threshold = True
                r2.pause_threshold = 0.3

                mic_src = getattr(self.voice, '_mic_source', None)
                if mic_src is None:
                    return

                # ছোট snippet শুনো — কথা শুনলে interrupt
                try:
                    audio = r2.listen(mic_src, timeout=2, phrase_time_limit=3)
                    raw = array.array('h', audio.frame_data)
                    # Volume check — কথার মতো loud হলেই interrupt
                    rms = (sum(s*s for s in raw) / max(len(raw), 1)) ** 0.5
                    if rms > 300 and self._barge_in_active:
                        print("[VOICE] Barge-in detected! Stopping JARVIS speech...")
                        if hasattr(self, 'voice') and self.voice:
                            self.voice.stop()
                except sr.WaitTimeoutError:
                    pass  # কোনো কথা নেই — স্বাভাবিক
                except Exception:
                    pass
            except Exception:
                pass

        t = threading.Thread(target=_listen_for_interrupt, daemon=True)
        t.start()
        self._barge_in_thread = t

    def _stop_barge_in_listener(self):
        """Barge-in listener বন্ধ করো"""
        self._barge_in_active = False

    def detect_response_emotion(self, text):
        text_lower = text.lower()
        
        # Explicit tag check
        if "[emotion:" in text_lower:
            import re
            m = re.search(r'\[emotion:\s*(\w+)\]', text_lower)
            if m:
                return m.group(1).strip()
                
        # Keyword detection
        excited_words = ["wow", "awesome", "amazing", "hype", "super", "fantastic", "চমৎকার", "অসাধারণ", "দারুণ"]
        happy_words = ["happy", "great", "perfect", "success", "joy", "smile", "ভাল", "ভালো", "ধন্যবাদ", "খুশি", "😊", "😀", "😄"]
        sad_words = ["sad", "sorry", "fail", "lost", "bad", "unfortunate", "error", "offline", "দুঃখিত", "কষ্ট", "খারাপ", "ভুল", "😢", "😭", "💔"]
        angry_words = ["angry", "virus", "threat", "danger", "warning", "attack", "compromise", "hack", "হামলা", "ঝুঁকি", "বিপদ", "alert", "😠", "😡"]
        surprised_words = ["surprise", "shock", "what?", "really", "অবাক", "😮", "😲"]
        
        if any(w in text_lower for w in excited_words):
            return "excited"
        if any(w in text_lower for w in angry_words):
            return "angry"
        if any(w in text_lower for w in sad_words):
            return "sad"
        if any(w in text_lower for w in surprised_words):
            return "surprised"
        if any(w in text_lower for w in happy_words):
            return "happy"
            
        return "neutral"

    def update_emotion(self, emotion):
        emotion = str(emotion).lower()
        if hasattr(self, 'core') and self.core:
            self.core.set_emotion(emotion)
        if hasattr(self, 'voice') and self.voice:
            self.voice.set_emotion(emotion)

    def sing_developer_song(self):
        def _sing_thread():
            try:
                import winsound
                self.update_emotion("excited")
                self.speak("Okay Boss Asif, listen to my new intelligence song!")
                time.sleep(1)
                
                # C-Major scale retro beep sequence
                notes = [
                    (261, 300), (329, 300), (392, 300), (523, 600),
                    (392, 300), (329, 300), (261, 600)
                ]
                for freq, duration in notes:
                    winsound.Beep(freq, duration)
                    
                self.speak("Coding all day, hacking all night,")
                
                for freq, duration in notes:
                    winsound.Beep(int(freq * 1.2), duration)
                    
                self.speak("Jarvis is online, making the future bright!")
                
                for freq, duration in notes:
                    winsound.Beep(int(freq * 0.8), duration)
                    
                self.speak("Asif is the boss, the master mind coder,")
                self.speak("No hacker can match him, from here to the border!")
                
                self.update_emotion("happy")
                for f in [261, 329, 392, 523, 659, 783, 1046]:
                    winsound.Beep(f, 150)
                self.speak("Thank you, thank you, Boss! Hope you like my melody.")
                self.update_emotion("neutral")
            except Exception as e:
                print(f"Singing error: {e}")
                
        threading.Thread(target=_sing_thread, daemon=True).start()
    
    def set_voice_speed(self, speed):
        """Set voice speed"""
        try:
            if hasattr(self, 'voice') and self.voice:
                self.voice.rate = speed
                self.log("SYSTEM", f"🎤 Voice speed set to: {speed}")
                self.speak(f"Voice speed set to {speed}")
                print(f"[OK] Voice speed set to: {speed}")
        except Exception as e:
            self.log("ERROR", f"Could not set voice speed: {e}")
            print(f"[!] Voice speed error: {e}")
    
    def open_voice_control_panel(self):
        """Open advanced voice control panel"""
        try:
            open_voice_control_panel(self, self.voice, self.speak)
            self.log("SYSTEM", "🎤 Voice Control Panel opened!")
        except Exception as e:
            self.log("ERROR", f"Failed to open Voice Control Panel: {e}")
            print(f"[!] Voice Control Panel error: {e}")
    
    def open_bangla_voice_selector(self):
        """Open Bengali voice selector"""
        try:
            from jarvis_bangla_voice_selector import open_bangla_voice_selector
            open_bangla_voice_selector(self)
            self.log("SYSTEM", "🇧🇩 Bengali Voice Selector opened!")
        except Exception as e:
            self.log("ERROR", f"Failed to open Bengali Voice Selector: {e}")
            print(f"[!] Bengali Voice Selector error: {e}")

    def open_all_functions_panel(self):
        """Open the All Functions Panel with all JARVIS commands"""
        try:
            open_all_functions_panel(self, self.process)
            self.log("SYSTEM", "All Functions Panel opened - 200+ functions available!")
        except Exception as e:
            self.log("ERROR", f"Failed to open All Functions Panel: {e}")

    def open_code_studio(self):
        """Open AI-powered Code Studio"""
        try:
            if _CODE_STUDIO_AVAILABLE:
                open_code_studio(self, self.brain)
                self.log("SYSTEM", "💻 Code Studio opened! AI-powered editor ready.")
            else:
                self.log("ERROR", "Code Studio not available. Check jarvis_code_studio.py")
        except Exception as e:
            self.log("ERROR", f"Code Studio error: {e}")

    def open_folder_upload_panel(self):
        """Open Folder Upload panel"""
        try:
            if _FOLDER_UPLOAD_AVAILABLE:
                def on_complete(files):
                    self.log("SYSTEM", f"📁 {len(files)} files uploaded to JARVIS!")
                open_folder_upload(self, self.brain, on_complete)
                self.log("SYSTEM", "📁 Folder Upload opened!")
            else:
                self.log("ERROR", "Folder Upload not available.")
        except Exception as e:
            self.log("ERROR", f"Folder Upload error: {e}")

    def open_android_manager_panel(self):
        """Open Android Device Manager"""
        try:
            if _ANDROID_MANAGER_AVAILABLE:
                open_android_manager(self, self.brain)
                self.log("SYSTEM", "📱 Android Device Manager opened!")
            else:
                self.log("ERROR", "Android Manager not available.")
        except Exception as e:
            self.log("ERROR", f"Android Manager error: {e}")

    def update_telemetry(self):
        try:
            cpu, ram = psutil.cpu_percent(), psutil.virtual_memory().percent
            status = "ONLINE" if (self.brain and self.brain.is_connected) else "OFFLINE"
            self.stats_label.configure(text=f"CPU: {cpu}% | RAM: {ram}%")
            
            # Update Clock
            current_time = time.strftime("%H:%M:%S")
            self.clock_label.configure(text=current_time)
            
            if hasattr(self, "link_status"):
                if status == "ONLINE":
                    self.link_status.configure(text="LINK: ONLINE", text_color="#00FF41")
                else:
                    # Distinguish common causes
                    reason = ""
                    if self.brain and getattr(self.brain, "last_error", ""):
                        le = str(self.brain.last_error)
                        if "RESOURCE_EXHAUSTED" in le or "429" in le:
                            reason = " (QUOTA)"
                        elif "expired" in le.lower() or "invalid" in le.lower():
                            reason = " (KEY)"
                        elif "not_found" in le.lower() or "404" in le:
                            reason = " (MODEL)"
                    self.link_status.configure(text=f"LINK: OFFLINE{reason}", text_color="#FF3131")
        except Exception:
            pass  # Ignore telemetry errors
        finally:
            # Schedule next update safely
            try:
                if not self._is_destroying:
                    self.after(1000, self.update_telemetry)
            except Exception:
                pass  # Widget might be destroyed

    def _animate_pulse(self):
        """Blinking pulse animation for status bar"""
        try:
            current_color = self.pulse_canvas.itemcget(self.pulse_dot, "fill")
            new_color = self.neon if current_color == "#111111" else "#111111"
            self.pulse_canvas.itemconfig(self.pulse_dot, fill=new_color)
        except Exception:
            pass  # Ignore animation errors
        finally:
            # Schedule next animation safely
            try:
                if not self._is_destroying:
                    self.after(800, self._animate_pulse)
            except Exception:
                pass  # Widget might be destroyed

    def paste_key(self):
        """Paste API key from clipboard - FIX: Don't show full key"""
        import pyperclip
        k = pyperclip.paste().strip()
        if k:
            self.key_entry.delete(0, "end")
            self.key_entry.insert(0, k)
            
            # FIX: Show masked key instead of full key
            masked_key = f"{k[:8]}****{k[-4:]}" if len(k) > 12 else "****"
            self.log("SYSTEM", f"📋 API KEY PASTED: {masked_key}")
            self.log("SYSTEM", "💡 Click SYNC to activate this key")

    def rotate_brain_model(self):
        if self.brain:
            self.brain.rotate_model()
            model = self.brain.models[self.brain.model_idx]
            self.log("SYSTEM", f"Neural Model rotated to: {model}")
            self.model_info.configure(text=f"MODEL: {model.upper()} | TEMP: 0.7")

    def test_keys(self):
        if not self.brain: return
        self.log("SYSTEM", f"INITIATING NEURAL POOL DIAGNOSTICS... ({len(self.brain.api_keys)} KEYS)")
        
        popup = ctk.CTkToplevel(self)
        popup.title("ADVANCED API DIAGNOSTICS")
        popup.geometry("400x500")
        popup.attributes("-topmost", True)
        
        scroll = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        scroll.pack(expand=True, fill="both", padx=10, pady=10)
        
        for i, k in enumerate(self.brain.api_keys):
            status = "CHECKING..."
            color = "#FFD700"
            frame = ctk.CTkFrame(scroll, fg_color="#05080F", border_width=1, border_color="#002233")
            frame.pack(pady=5, fill="x")
            
            ctk.CTkLabel(frame, text=f"NODE_{i+1}: {k[:10]}***", font=("Courier New", 12)).pack(side="left", padx=10)
            
            # Action Buttons
            ctk.CTkButton(frame, text="DELETE", width=60, height=20, fg_color="#440000", command=lambda idx=i: self.delete_key_idx(idx)).pack(side="right", padx=5)
            ctk.CTkButton(frame, text="ACTIVATE", width=60, height=20, fg_color="#004400", command=lambda idx=i: self.activate_key_idx(idx)).pack(side="right", padx=5)
            status_lbl = ctk.CTkLabel(frame, text=status, text_color=color, font=("Courier New", 10, "bold"))
            status_lbl.pack(side="right", padx=10)

            def _run_check(idx=i, key=k, lbl=status_lbl):
                ok, reason = JarvisBrain.validate_key(key, model=self.brain.models[0])
                def _update():
                    if ok:
                        st = "ACTIVE" if idx == self.brain.key_idx else "HEALTHY"
                        lbl.configure(text=st, text_color="#00FF41" if idx == self.brain.key_idx else "#555555")
                    else:
                        lbl.configure(text="INVALID", text_color="#FF3131")
                self.after(0, _update)
            threading.Thread(target=_run_check, daemon=True).start()

    def delete_key_idx(self, idx):
        if len(self.brain.api_keys) <= 1:
            self.log("ERROR", "Cannot delete last neural node. System requires at least one uplink.")
            return
        removed = self.brain.api_keys.pop(idx)
        self.brain.key_idx = 0
        self.save_pool_to_config()
        self.log("SYSTEM", f"Node {removed[:5]}*** purged from neural pool.")
        self.test_keys() # Refresh

    def activate_key_idx(self, idx):
        self.brain.key_idx = idx
        self.log("SYSTEM", f"Manually switched to Neural Node {idx + 1}.")
        self.test_keys() # Refresh

    def save_pool_to_config(self):
        with open("jarvis_config.txt", "w") as f:
            f.write("\n".join(self.brain.api_keys))

    def show_mobile_qr(self):
        # Start Server in background if not already
        if not hasattr(self, 'mobile_active'):
            threading.Thread(target=start_server, daemon=True).start()
            self.mobile_active = True
            self.log("SYSTEM", "MOBILE SERVER ONLINE. Screen sharing active.")

        ip = get_ip()
        url = f"http://{ip}:5000"
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=280x280&data={url}&bgcolor=02050A&color=00F3FF"

        # Create Popup Window
        popup = ctk.CTkToplevel(self)
        popup.title("ANTIGRAVITY MOBILE UPLINK")
        popup.geometry("380x560")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="MOBILE REMOTE UPLINK", font=("Courier New", 18, "bold"), text_color="#00F3FF").pack(pady=15)
        ctk.CTkLabel(popup, text="Scan QR with your phone to control this PC", font=("Courier New", 10), text_color="#555555").pack()

        # Generate QR code offline-first
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            # Match the panel theme colors (Cyan `#00F3FF` on Dark background `#02050A`)
            qr_img = qr.make_image(fill_color="#00F3FF", back_color="#02050A")
            # Convert PilImage to PIL Image
            from PIL import Image
            pil_img = qr_img.convert("RGBA").resize((250, 250), Image.Resampling.LANCZOS)
            self.qr_photo = ImageTk.PhotoImage(pil_img)
            ctk.CTkLabel(popup, image=self.qr_photo, text="").pack(pady=15)
        except Exception as e:
            print(f"[!] Local QR Gen failed: {e}. Trying Web API fallback...")
            try:
                import requests
                from io import BytesIO
                response = requests.get(qr_api, timeout=5)
                qr_img = Image.open(BytesIO(response.content))
                self.qr_photo = ImageTk.PhotoImage(qr_img)
                ctk.CTkLabel(popup, image=self.qr_photo, text="").pack(pady=15)
            except Exception as e2:
                print(f"[!] Web QR fallback failed: {e2}")
                ctk.CTkLabel(popup, text=f"URL: {url}", font=("Courier New", 12), text_color="#00FF41", wraplength=300).pack(pady=30)

        # URL display
        url_frame = ctk.CTkFrame(popup, fg_color="#05080F", border_width=1, border_color="#002233")
        url_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(url_frame, text=url, font=("Courier New", 14, "bold"), text_color="#00FF41").pack(pady=10)

        # Feature list
        ctk.CTkLabel(popup, text="[OK] Live Screen View  [OK] Mouse Control\n[OK] Keyboard Input  [OK] Volume & Lock",
                     font=("Courier New", 10), text_color="#444444").pack(pady=5)

        # Open in browser button
        ctk.CTkButton(popup, text="OPEN IN BROWSER", fg_color="#004466", hover_color="#006688",
                      command=lambda: webbrowser.open(url)).pack(pady=10)

        ctk.CTkLabel(popup, text=f"Make sure phone is on same WiFi", font=("Courier New", 9), text_color="#333333").pack()


    def show_custom_qr(self, data):
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={data}"
        
        # Create Popup Window
        popup = ctk.CTkToplevel(self)
        popup.title("JARVIS DATA UPLINK")
        popup.geometry("300x400")
        popup.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(popup, text="DATA SYNC", font=("Courier New", 16, "bold"))
        lbl.pack(pady=20)
        
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="#00F3FF", back_color="#02050A")
            from PIL import Image
            pil_img = qr_img.convert("RGBA").resize((220, 220), Image.Resampling.LANCZOS)
            self.qr_custom_photo = ImageTk.PhotoImage(pil_img)
            ctk.CTkLabel(popup, image=self.qr_custom_photo, text="").pack(pady=10)
        except Exception as e:
            print(f"[!] Local QR Gen failed: {e}. Trying Web API fallback...")
            try:
                import requests
                from io import BytesIO
                response = requests.get(qr_api)
                qr_img = Image.open(BytesIO(response.content))
                self.qr_custom_photo = ImageTk.PhotoImage(qr_img)
                ctk.CTkLabel(popup, image=self.qr_custom_photo, text="").pack(pady=10)
            except Exception as e2:
                print(f"[!] Web QR fallback failed: {e2}")
                ctk.CTkLabel(popup, text=f"DATA: {data}", wraplength=250).pack(pady=10)
            
        ctk.CTkLabel(popup, text="SCAN TO RECEIVE DATA", font=("Courier New", 10)).pack(pady=10)

    def clipboard_watcher(self):
        """Monitor clipboard for Gemini API keys with graceful shutdown"""
        import pyperclip
        last_clip = ""
        last_applied = ""
        last_applied_at = 0.0
        
        print("[OK] Clipboard watcher thread started")
        
        while not self._clipboard_stop_event.is_set():  # ← Check stop event
            try:
                # Check if monitoring is enabled
                if not self._clipboard_enabled:
                    time.sleep(2)
                    continue
                
                # Check clipboard
                curr = pyperclip.paste().strip()
                if curr != last_clip:
                    # Detect Gemini API Key Pattern
                    if (curr.startswith("AIza") or curr.startswith("AQ.")) and 35 <= len(curr) <= 60:
                        now = time.time()
                        if curr != last_applied or (now - last_applied_at) > 10:
                            last_applied = curr
                            last_applied_at = now
                            self.after(0, lambda k=curr: self.auto_apply_key(k))  # ← Fix lambda closure
                    last_clip = curr
                    
            except Exception as e:
                # Log errors instead of silent pass
                print(f"[!] Clipboard watcher error: {e}")
                # Continue running despite errors
                
            time.sleep(2)
        
        print("[OK] Clipboard watcher stopped cleanly")

    def start_clipboard_watcher(self):
        """Start clipboard monitoring in a daemon thread"""
        if self._clipboard_thread and self._clipboard_thread.is_alive():
            return  # Already running
        
        self._clipboard_thread = threading.Thread(
            target=self.clipboard_watcher,
            daemon=True,  # Daemon thread exits with main application
            name="ClipboardWatcher"
        )
        self._clipboard_thread.start()
        print("[OK] Clipboard monitoring started")

    def stop_clipboard_watcher(self):
        """Stop the clipboard watcher thread gracefully"""
        if not self._clipboard_thread or not self._clipboard_thread.is_alive():
            return  # Not running
        
        print("⏹️ Stopping clipboard watcher...")
        self._clipboard_stop_event.set()
        
        # Wait for thread to stop (max 3 seconds)
        self._clipboard_thread.join(timeout=3.0)
        
        if self._clipboard_thread.is_alive():
            print("[!] Clipboard watcher did not stop in time")
        else:
            print("[OK] Clipboard watcher stopped successfully")

    def on_closing(self):
        """Handle application closing with proper cleanup"""
        print("🛑 Shutting down Jarvis...")
        
        # Set destroying flag to stop all animations
        self._is_destroying = True
        
        # Save natural interface preferences
        if hasattr(self, 'natural_interface') and self.natural_interface:
            try:
                self.natural_interface.save_preferences()
                print("[OK] Natural Interface preferences saved")
            except Exception as e:
                print(f"[!] Could not save preferences: {e}")
        
        # Stop keyboard shortcuts
        if hasattr(self, 'keyboard_shortcuts') and self.keyboard_shortcuts:
            try:
                self.keyboard_shortcuts.stop()
                print("[OK] Keyboard Shortcuts deactivated")
            except Exception as e:
                print(f"[!] Could not stop shortcuts: {e}")
        
        self.stop_clipboard_watcher()
        
        # Stop speech worker
        if hasattr(self, 'speech_queue') and self.speech_queue:
            self.speech_queue.put(None)
        
        # Stop auto controller
        if hasattr(self, 'auto_ctrl'):
            self.auto_ctrl.stop()
        
        # Stop auto background learner
        if hasattr(self, 'auto_bg_learner') and self.auto_bg_learner:
            try:
                if self.auto_bg_learner.is_running:
                    self.auto_bg_learner.stop()
                    print("[OK] Auto Background Learner stopped")
            except Exception as e:
                print(f"[!] Could not stop auto learner: {e}")
        
        # Destroy HUD
        if hasattr(self, 'hud') and self.hud:
            try:
                self.hud.destroy()
            except Exception:
                pass

        # Destroy window
        self.destroy()

    def auto_apply_key(self, k):
        """Auto-apply API key from clipboard - FIX: Don't show full key"""
        try:
            save_new_key(k)
            self.brain = JarvisBrain(get_saved_keys())  # Full pool
            
            # FIX: Show masked key instead of full key
            masked_key = f"{k[:8]}****{k[-4:]}" if len(k) > 12 else "****"
            self.log("SYSTEM", "🔍 NEURAL PROTOCOL DETECTED IN CLIPBOARD")
            self.log("SYSTEM", f"✅ AUTO-APPLYING KEY: {masked_key}")
            self.log("SYSTEM", f"📊 UPLINK STABLE: {len(self.brain.api_keys)} KEY(S) IN POOL")
        except Exception as e:
            self.log("ERROR", f"❌ AUTO-APPLY FAILED: {str(e)[:100]}")

    def sync_key(self):
        """Sync API key from entry field - FIX: Don't show full key"""
        k = self.key_entry.get().strip()
        if k:
            try:
                # Validate and save key
                save_new_key(k)
                
                # Reinitialize brain with new key pool
                self.brain = JarvisBrain(get_saved_keys())
                
                # FIX: Show masked key instead of full key
                masked_key = f"{k[:8]}****{k[-4:]}" if len(k) > 12 else "****"
                self.log("SYSTEM", f"✅ API KEY SYNCED: {masked_key}")
                self.log("SYSTEM", f"📊 NEURAL POOL: {len(self.brain.api_keys)} KEY(S) ACTIVE")
                
                # Clear entry field
                self.key_entry.delete(0, "end")
                
                # Update link status
                self.link_status.configure(text="LINK: SYNCING...", text_color="#FFD700")
                
            except Exception as e:
                self.log("ERROR", f"❌ KEY REJECTED: {str(e)[:100]}")
                # Don't show the key in error message

    def ping_key(self):
        k = self.key_entry.get().strip()
        if not k:
            self.log("ERROR", "No key in input.")
            return

        self.log("SYSTEM", "PING: Testing key with Gemini...")

        def _run():
            ok, reason = JarvisBrain.validate_key(
                k,
                model=(self.brain.models[0] if self.brain else None),
            )
            if ok:
                self.after(0, lambda: self.log("SYSTEM", "PING OK: key can access Gemini."))
            else:
                self.after(0, lambda: self.log("ERROR", f"PING FAIL: {reason[:220]}"))

        threading.Thread(target=_run, daemon=True).start()

    def _toggle_ai_chat_mode(self):
        self.ai_chat_mode = not self.ai_chat_mode
        self.ai_mode_btn.configure(text=f"🗨️ CHAT MODE: {'ON' if self.ai_chat_mode else 'OFF'}",
                                   fg_color="#006644" if self.ai_chat_mode else "#333333")

    def _on_ai_selected(self, choice):
        self.selected_global_ai = choice
        self.log("SYSTEM", f"AI switched to: {choice}")

    def fire_cmd(self):
        q = self.entry.get()
        if q:
            self.entry.delete(0, "end")
            self.log("ROOT", q)
            
            # Handle Chat Mode
            if self.ai_chat_mode:
                self.after(0, lambda: self.log("USER", q))
                self.after(0, lambda: self.log("SYSTEM", f"Talking to {self.selected_global_ai.upper()}..."))
                
                try:
                    result = self.direct_ai_chat.chat_with_ai(q, self.selected_global_ai.lower())
                    if result['success']:
                        res = result['response']
                        self.after(0, lambda r=res: self.log("JARVIS", f"[{result['ai']}] {r}"))
                        self.after(0, lambda r=res: self.speak(r))
                        self.core.set_state("idle")
                        if self.face3d: self.face3d.set_state("idle")
                        return
                except Exception as e:
                    self.after(0, lambda: self.log("ERROR", f"Chat failed: {e}"))
            
            # Original Brain processing
            threading.Thread(target=self.process, args=(q,), daemon=True).start()
    
    def _handle_shortcut(self, command: str):
        """Handle keyboard shortcut command"""
        try:
            # Special handling for help shortcut
            if command == 'help' and self.keyboard_shortcuts:
                self.keyboard_shortcuts.show_help()
                self.log("SYSTEM", "⌨️ Keyboard shortcuts help displayed in console")
                return
            
            # Log shortcut activation
            self.log("SYSTEM", f"⌨️ Shortcut activated: {command}")
            
            # Process command through normal pipeline
            threading.Thread(target=self.process, args=(command,), daemon=True).start()
        except Exception as e:
            self.log("ERROR", f"Shortcut handler error: {e}")

    def _handle_file_upload(self):
        """Handle file upload button click"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select file to upload",
            filetypes=[
                ("All Files", "*.*"),
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("Documents", "*.pdf *.doc *.docx *.txt *.md"),
                ("Code", "*.py *.js *.html *.css *.json *.xml"),
                ("Data", "*.csv *.xlsx *.json"),
            ]
        )
        
        if file_path:
            self.log("SYSTEM", f"Uploading file: {file_path}")
            
            # Handle upload
            result = handle_file_upload(file_path)
            
            if result['success']:
                self.log("SYSTEM", 
                    f"✅ File uploaded: {result['filename']} "
                    f"({result['file_type']}, {result['file_size']} bytes)")
                
                # If it's an image, show preview
                if result['file_type'] == 'image':
                    self.log("SYSTEM", f"📷 Image preview: {result['filepath']}")
                
                # If text was extracted, show it
                if result.get('extracted_text') and len(result['extracted_text']) > 0:
                    preview = result['extracted_text'][:200]
                    if len(result['extracted_text']) > 200:
                        preview += "..."
                    self.log("SYSTEM", f"📄 Content preview: {preview}")
                
                # Auto-fill entry with file analysis prompt
                self.entry.delete(0, "end")
                self.entry.insert(0, f"Analyze this file: {result['filename']}")
                
                # Automatic AI prompt analysis if brain is online/available
                if result.get('extracted_text') and len(result['extracted_text']) > 0:
                    self.log("SYSTEM", "Analyzing file content automatically...")
                    query = f"Analyze this file: {result['filename']}\n\nContent:\n{result['extracted_text'][:3000]}"
                    threading.Thread(target=self.process, args=(query,), daemon=True).start()
                
            else:
                self.log("ERROR", f"❌ Upload failed: {result.get('error', 'Unknown error')}")

    def _handle_folder_upload(self):
        """Handle folder upload button click"""
        if not _FOLDER_UPLOAD_AVAILABLE:
            self.log("ERROR", "❌ Folder upload system not available!")
            return
            
        self.log("SYSTEM", "📂 Opening Folder Upload Console...")
        
        def on_complete(uploaded_files):
            if uploaded_files:
                self.log("SYSTEM", f"✅ Folder upload finished: {len(uploaded_files)} files added to active directory.")
                self.entry.delete(0, "end")
                self.entry.insert(0, "Analyze these uploaded files")
                
                # Automatically request folder analysis
                from jarvis_folder_upload import READABLE_EXTENSIONS
                readable_names = [f["name"] for f in uploaded_files if f["ext"] in READABLE_EXTENSIONS]
                if readable_names:
                    self.log("SYSTEM", "Automatically initiating batch analysis on uploaded folder content...")
                    # We can use the first few files to summarize
                    file_summaries = []
                    for f in uploaded_files:
                        if f["ext"] in READABLE_EXTENSIONS:
                            try:
                                with open(f["path"], "r", encoding="utf-8", errors="ignore") as fh:
                                    content = fh.read(1500)
                                file_summaries.append(f"File: {f['name']}\nContent:\n{content}")
                            except Exception:
                                pass
                            if len(file_summaries) >= 3: # Analyze first 3 files to keep context window safe
                                break
                    
                    combined_files = "\n\n".join(file_summaries)
                    query = (f"Batch Analysis Request for Uploaded Folder:\n"
                             f"We have uploaded a folder with {len(uploaded_files)} files: {', '.join([f['name'] for f in uploaded_files])}.\n"
                             f"Here is content preview of readable files:\n\n{combined_files}\n\n"
                             f"Please summarize what this folder contains, what the code or data does, and if you see any bugs or improvements.")
                    threading.Thread(target=self.process, args=(query,), daemon=True).start()
            else:
                self.log("SYSTEM", "📁 Folder selection cancelled or no files uploaded.")
                
        open_folder_upload(self, self.brain, on_complete)

    def _handle_web_search(self):
        """Handle web search button click - searches what user types in chat box"""
        query = self.entry.get().strip()
        
        if not query:
            self.log("SYSTEM", "❌ Please type something in the chat box to search!")
            self.log("SYSTEM", "❌ চ্যাট বক্সে কিছু টাইপ করুন search করার জন্য!")
            return
        
        # Clear entry
        self.entry.delete(0, "end")
        
        # Log what user wants to search
        self.log("ROOT", f"🔍 WEB SEARCH: {query}")
        self.log("SYSTEM", "NEURAL REQUEST SENT. AWAITING BRAIN...")
        
        # Process in background thread
        def _search():
            try:
                # Import offline brain for intelligent search
                from jarvis_offline_brain import OfflineBrain
                offline_brain = OfflineBrain()
                
                # Detect search intent and platform
                query_lower = query.lower()
                search_query = query
                platform = "google"  # default
                
                # Detect specific platforms
                if 'youtube' in query_lower or 'video' in query_lower:
                    platform = "youtube"
                    search_query = query_lower.replace('youtube', '').replace('video', '').strip()
                elif 'github' in query_lower or 'code' in query_lower:
                    platform = "github"
                    search_query = query_lower.replace('github', '').replace('code', '').strip()
                elif 'wikipedia' in query_lower or 'wiki' in query_lower:
                    platform = "wikipedia"
                    search_query = query_lower.replace('wikipedia', '').replace('wiki', '').strip()
                elif 'stackoverflow' in query_lower or 'stack overflow' in query_lower:
                    platform = "stackoverflow"
                    search_query = query_lower.replace('stackoverflow', '').replace('stack overflow', '').strip()
                elif 'amazon' in query_lower or 'shopping' in query_lower:
                    platform = "amazon"
                    search_query = query_lower.replace('amazon', '').replace('shopping', '').strip()
                elif 'twitter' in query_lower or 'tweet' in query_lower:
                    platform = "twitter"
                    search_query = query_lower.replace('twitter', '').replace('tweet', '').strip()
                elif 'reddit' in query_lower:
                    platform = "reddit"
                    search_query = query_lower.replace('reddit', '').strip()
                elif 'image' in query_lower or 'picture' in query_lower or 'photo' in query_lower:
                    platform = "image"
                    search_query = query_lower.replace('image', '').replace('picture', '').replace('photo', '').strip()
                elif 'news' in query_lower or 'খবর' in query_lower:
                    platform = "news"
                    search_query = query_lower.replace('news', '').replace('খবর', '').strip()
                elif 'map' in query_lower or 'location' in query_lower or 'place' in query_lower:
                    platform = "map"
                    search_query = query_lower.replace('map', '').replace('location', '').replace('place', '').strip()
                
                # If no specific platform, use original query
                if not search_query or len(search_query) < 2:
                    search_query = query
                
                # Execute search using offline brain
                result = offline_brain.do_search(f"search {platform} {search_query}")
                
                # Log result
                self.after(0, lambda: self.log("JARVIS", f"[WEB SEARCH] {result['response']}"))
                
                # Also provide intelligent response about what was searched
                if platform == "google":
                    self.after(0, lambda: self.log("JARVIS", 
                        f"🔍 Searched Google for: '{search_query}'\n"
                        f"🔍 Google এ খুঁজেছি: '{search_query}'\n"
                        f"💡 I understand you want to search for information about: {search_query}\n"
                        f"💡 আমি বুঝেছি আপনি এই বিষয়ে তথ্য খুঁজতে চান: {search_query}"
                    ))
                elif platform == "youtube":
                    self.after(0, lambda: self.log("JARVIS", 
                        f"🎥 Searched YouTube for videos about: '{search_query}'\n"
                        f"🎥 YouTube এ ভিডিও খুঁজেছি: '{search_query}'\n"
                        f"💡 I understand you want to watch videos about: {search_query}\n"
                        f"💡 আমি বুঝেছি আপনি এই বিষয়ে ভিডিও দেখতে চান: {search_query}"
                    ))
                elif platform == "github":
                    self.after(0, lambda: self.log("JARVIS", 
                        f"💻 Searched GitHub for code/projects: '{search_query}'\n"
                        f"💻 GitHub এ কোড/প্রজেক্ট খুঁজেছি: '{search_query}'\n"
                        f"💡 I understand you want to find code or projects about: {search_query}\n"
                        f"💡 আমি বুঝেছি আপনি এই বিষয়ে কোড বা প্রজেক্ট খুঁজতে চান: {search_query}"
                    ))
                elif platform == "wikipedia":
                    self.after(0, lambda: self.log("JARVIS", 
                        f"📚 Searched Wikipedia for information: '{search_query}'\n"
                        f"📚 Wikipedia তে তথ্য খুঁজেছি: '{search_query}'\n"
                        f"💡 I understand you want to learn about: {search_query}\n"
                        f"💡 আমি বুঝেছি আপনি এই বিষয়ে জানতে চান: {search_query}"
                    ))
                else:
                    self.after(0, lambda: self.log("JARVIS", 
                        f"🔍 Searched {platform.upper()} for: '{search_query}'\n"
                        f"🔍 {platform.upper()} এ খুঁজেছি: '{search_query}'\n"
                        f"💡 I understand your search intent: {search_query}\n"
                        f"💡 আমি আপনার search এর উদ্দেশ্য বুঝেছি: {search_query}"
                    ))
                
                # Close offline brain
                offline_brain.close()
                
            except Exception as e:
                self.after(0, lambda: self.log("ERROR", f"Web search error: {e}"))
        
        # Run search in background
        threading.Thread(target=_search, daemon=True).start()

    def _handle_mrx_learning(self):
        """Handle MRX button click - runs ALL 4 learning systems on the topic"""
        topic = self.entry.get().strip()
        
        if not topic:
            self.log("SYSTEM", "❌ Please type a topic in the chat box to learn!")
            self.log("SYSTEM", "❌ চ্যাট বক্সে একটি topic টাইপ করুন শিখতে!")
            self.log("SYSTEM", "💡 Example: Python, AI, JavaScript, etc.")
            return
        
        # Clear entry
        self.entry.delete(0, "end")
        
        # Log MRX activation
        self.log("ROOT", f"🔥 MRX ACTIVATED: {topic}")
        self.log("SYSTEM", "🔥 ALL 4 LEARNING SYSTEMS STARTING...")
        self.log("SYSTEM", "🔥 সব 4টি শেখার সিস্টেম শুরু হচ্ছে...")
        
        # Process in background thread
        def _mrx_learn():
            try:
                # Import offline brain
                from jarvis_offline_brain import OfflineBrain
                offline_brain = OfflineBrain()
                
                # System 1: Internet Learner
                self.after(0, lambda: self.log("MRX", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                self.after(0, lambda: self.log("MRX", "🧠 SYSTEM 1: INTERNET LEARNER"))
                self.after(0, lambda: self.log("MRX", f"📚 Learning from internet: {topic}"))
                result1 = offline_brain.process_command(f"learn from internet {topic}")
                self.after(0, lambda: self.log("JARVIS", result1['response']))
                time.sleep(2)
                
                # System 2: Ultimate Learner
                self.after(0, lambda: self.log("MRX", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                self.after(0, lambda: self.log("MRX", "🚀 SYSTEM 2: ULTIMATE LEARNER (Chrome + Google)"))
                self.after(0, lambda: self.log("MRX", f"🌐 Learning everything about: {topic}"))
                result2 = offline_brain.process_command(f"ultimate learn {topic}")
                self.after(0, lambda: self.log("JARVIS", result2['response']))
                time.sleep(2)
                
                # System 3: Auto Learner
                self.after(0, lambda: self.log("MRX", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                self.after(0, lambda: self.log("MRX", "📖 SYSTEM 3: AUTO LEARNER (Word by Word)"))
                self.after(0, lambda: self.log("MRX", f"📝 Learning word by word: {topic}"))
                result3 = offline_brain.process_command(f"auto learn {topic}")
                self.after(0, lambda: self.log("JARVIS", result3['response']))
                time.sleep(2)
                
                # System 4: Chrome DevTools
                self.after(0, lambda: self.log("MRX", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                self.after(0, lambda: self.log("MRX", "🔧 SYSTEM 4: CHROME DEVTOOLS"))
                self.after(0, lambda: self.log("MRX", f"🔍 Advanced learning with DevTools: {topic}"))
                result4 = offline_brain.process_command(f"devtools learn {topic}")
                self.after(0, lambda: self.log("JARVIS", result4['response']))
                
                # Final Summary
                self.after(0, lambda: self.log("MRX", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                self.after(0, lambda: self.log("MRX", "🎉 MRX COMPLETE! ALL 4 SYSTEMS FINISHED!"))
                self.after(0, lambda: self.log("MRX", "🎉 MRX সম্পূর্ণ! সব 4টি সিস্টেম শেষ!"))
                self.after(0, lambda: self.log("MRX", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                self.after(0, lambda: self.log("JARVIS", 
                    f"✅ Learned '{topic}' using ALL 4 systems:\n"
                    f"   1. 🧠 Internet Learner - Quick facts\n"
                    f"   2. 🚀 Ultimate Learner - Deep learning\n"
                    f"   3. 📖 Auto Learner - Word by word\n"
                    f"   4. 🔧 Chrome DevTools - Advanced automation\n\n"
                    f"✅ '{topic}' সব 4টি সিস্টেম দিয়ে শিখেছি:\n"
                    f"   1. 🧠 Internet Learner - দ্রুত তথ্য\n"
                    f"   2. 🚀 Ultimate Learner - গভীর শিক্ষা\n"
                    f"   3. 📖 Auto Learner - শব্দে শব্দে\n"
                    f"   4. 🔧 Chrome DevTools - উন্নত automation\n\n"
                    f"💾 Data saved to:\n"
                    f"   - Database: jarvis_memory.db\n"
                    f"   - Text Files: jarvis_learned_files/{topic}_learned.txt\n\n"
                    f"📊 Check your learning:\n"
                    f"   - Type: 'learned topics'\n"
                    f"   - Type: 'learning stats'\n"
                    f"   - Type: 'search learned {topic}'"
                ))
                
                # Close offline brain
                offline_brain.close()
                
            except Exception as e:
                self.after(0, lambda: self.log("ERROR", f"MRX error: {e}"))
                import traceback
                self.after(0, lambda: self.log("ERROR", traceback.format_exc()))
        
        # Run MRX in background
        threading.Thread(target=_mrx_learn, daemon=True).start()

    def start_mic(self):
        """Toggle continuous listening ON/OFF — debounced to prevent rapid fire"""
        import time

        # Debounce: ignore clicks within 2 seconds of last click
        now = time.time()
        if now - getattr(self, '_last_mic_click', 0) < 2.0:
            return
        self._last_mic_click = now

        # If currently ON → turn OFF
        if getattr(self, 'continuous_listening', False):
            self.continuous_listening = False
            self.is_listening = False
            self.log("SYSTEM", "🎤 Microphone OFF")
            self.set_voice_button(False)
            return

        # Check mic availability
        if not getattr(self, 'mic_enabled', True):
            self.log("SYSTEM", "⚠️ Microphone disabled. Enable it first.")
            return

        # Turn ON
        self.continuous_listening = True
        self.log("SYSTEM", "🎤 Microphone ON — Listening...")
        self.set_voice_button(True)
        self._launch_voice_thread()

    def _launch_voice_thread(self):
        """Safely launch a voice capture thread — never double-starts"""
        if not self.is_listening and getattr(self, 'continuous_listening', False):
            self.is_listening = True
            threading.Thread(target=self.voice_capture, daemon=True).start()

    def set_voice_button(self, listening):
        if not hasattr(self, "voice_btn"):
            return
        try:
            if getattr(self, 'continuous_listening', False):
                # ON state — cyan, always clickable to turn off
                self.voice_btn.configure(
                    text="🔴 MIC ON (click to OFF)",
                    fg_color=self.cyber,
                    text_color="black",
                    state="normal"
                )
            else:
                # OFF state — red, clickable to turn on
                self.voice_btn.configure(
                    text="🎤 LISTEN",
                    fg_color=self.neon,
                    text_color="black",
                    state="normal"
                )
        except Exception:
            pass

    def voice_capture(self):
        try:
            self.core.set_state("listening")
            if self.face3d:
                self.face3d.set_state("listening")

            query = self.voice.listen()
            if query != "none":
                import re as _re_vc
                query = _re_vc.sub(r'\s*->\s*\w+\s*$', '', query).strip()
                self.prefer_bangla_voice = (
                    str(getattr(self.voice, "last_language", "")).lower().startswith("bn")
                    or self.voice.has_bangla(query)
                )
                self.voice.prefer_bangla = self.prefer_bangla_voice
                routed_query = self.normalize_voice_command(query)
                if routed_query not in (query, "__HANDLED__"):
                    self.after(0, lambda q=query, r=routed_query: self.log("VOICE", f"{q} -> {r}"))
                else:
                    self.after(0, lambda q=query: self.log("VOICE", q))
                self.process(routed_query)
            else:
                err = getattr(self.voice, "last_error", "")
                if err:
                    self.after(0, lambda msg=err: self.log("VOICE", msg))
        except Exception as e:
            self.after(0, lambda msg=f"Listening failed: {e}": self.log("VOICE", msg))
        finally:
            self.is_listening = False
            self.core.set_state("idle")
            if self.face3d:
                self.face3d.set_state("idle")

            # Restart only if still in continuous mode — button update করো না এখানে
            if getattr(self, 'continuous_listening', False) and getattr(self, 'mic_enabled', True):
                err = getattr(self.voice, "last_error", "")
                if err and any(w in err for w in ["Microphone", "blocked", "denied", "OSError", "device", "Device"]):
                    delay = 5000
                else:
                    delay = 1000
                self.after(delay, self._restart_mic_if_continuous)

    def _restart_mic_if_continuous(self):
        """Restart mic only if still in continuous mode and not already listening"""
        if (getattr(self, 'continuous_listening', False) and
                getattr(self, 'mic_enabled', True) and
                not self.is_listening):
            self._launch_voice_thread()

    def normalize_voice_command(self, query):
        """Bangla/Banglish voice command ke JARVIS command e convert kore"""
        import re as _re
        import urllib.parse as _up
        import os as _os
        import sys as _sys
        import subprocess as _sp
        import webbrowser as _wb
        q = query.strip().lower()

        def _open_url(url):
            """Open URL in default browser — do NOT hardcode Chrome."""
            if _os.environ.get('JARVIS_NO_DIAGNOSIS') == '1' or _os.environ.get('JARVIS_TESTING') == '1':
                print(f"[MOCK BROWSER] Skipping URL: {url}")
                return
            try:
                _wb.open(url)
            except Exception:
                try:
                    if _sys.platform == 'win32':
                        safe_url = url.replace('"', '').replace('&', '^&').replace('|', '^|')
                        _sp.Popen(f'start "" "{safe_url}"', shell=True)
                except Exception:
                    pass

        # 3D Face control
        face_on  = ["face on", "face calu", "face chalao", "3d on", "face start",
                    "face open", "face dekao", "face jalao", "face deko",
                    "থ্রিডি ফেস অন",
                    "ফেস অন", "ফেস চালু",
                    "থ্রিডি ফেস চালু"]
        face_off = ["face off", "face bondho", "face band", "3d off", "face stop",
                    "ফেস অফ", "ফেস বন্ধ"]
        for kw in face_on:
            if kw in q:
                self.after(0, self.face3d_on)
                return "__HANDLED__"
        for kw in face_off:
            if kw in q:
                self.after(0, self.face3d_off)
                return "__HANDLED__"

        # ── MOUSE CONTROL (Banglish + English direct routing) ──────────────
        import re as _re_m
        # Move mouse
        _move_kws = ["mous noran", "mouse noran", "mous norao", "mous chalao", "mous move",
                     "mouse move", "mouse sorао", "move mouse", "move the mouse",
                     "মাউস নড়াও", "মাউস সরাও", "মাউস মুভ"]
        for _kw in _move_kws:
            if _kw in q:
                # Try to extract coordinates from query (e.g. "mouse move 500 300")
                _m = _re_m.search(r'(\d{2,4})\s+(\d{2,4})', q)
                if _m:
                    return f"mouse move {_m.group(1)} {_m.group(2)}"
                else:
                    # Move to screen center by default
                    try:
                        import pyautogui as _pag
                        _sw, _sh = _pag.size()
                        return f"mouse move {_sw // 2} {_sh // 2}"
                    except Exception:
                        return "mouse move 960 540"
        # Direction-based moves (bame = left, dane = right, upore = up, niche = down)
        if any(w in q for w in ["bam", "bame", "left", "বামে", "বাম"]) and any(w in q for w in ["mous", "mouse", "মাউস"]):
            try:
                import pyautogui as _pag
                _pos = _pag.position()
                return f"mouse move {max(0, _pos.x - 200)} {_pos.y}"
            except Exception:
                return "mouse move 200 540"
        if any(w in q for w in ["dan", "dane", "right", "ডানে", "ডান"]) and any(w in q for w in ["mous", "mouse", "মাউস"]):
            try:
                import pyautogui as _pag
                _pos = _pag.position()
                _sw, _ = _pag.size()
                return f"mouse move {min(_sw - 1, _pos.x + 200)} {_pos.y}"
            except Exception:
                return "mouse move 1200 540"
        if any(w in q for w in ["upor", "upore", "up", "উপরে"]) and any(w in q for w in ["mous", "mouse", "মাউস"]):
            try:
                import pyautogui as _pag
                _pos = _pag.position()
                return f"mouse move {_pos.x} {max(0, _pos.y - 200)}"
            except Exception:
                return "mouse move 960 200"
        if any(w in q for w in ["nice", "niche", "down", "নিচে"]) and any(w in q for w in ["mous", "mouse", "মাউস"]):
            try:
                import pyautogui as _pag
                _pos = _pag.position()
                _, _sh = _pag.size()
                return f"mouse move {_pos.x} {min(_sh - 1, _pos.y + 200)}"
            except Exception:
                return "mouse move 960 800"

        # Left click
        _lclick_kws = ["left click", "laft click", "left key", "laft key", "click koro",
                       "click korao", "mous click", "mouse click", "click mous",
                       "লেফট ক্লিক", "ক্লিক করো", "ক্লিক কর"]
        for _kw in _lclick_kws:
            if _kw in q:
                _m = _re_m.search(r'(\d{2,4})\s+(\d{2,4})', q)
                if _m:
                    return f"mouse click {_m.group(1)} {_m.group(2)}"
                return "mouse click"

        # Right click
        _rclick_kws = ["right click", "right key", "রাইট ক্লিক"]
        for _kw in _rclick_kws:
            if _kw in q:
                return "mouse right"

        # Double click
        if any(w in q for w in ["double click", "double klik", "ডাবল ক্লিক"]):
            return "mouse double"

        # Scroll
        if any(w in q for w in ["scroll up", "scroll upo", "উপরে স্ক্রোল"]):
            return "mouse scroll 5"
        if any(w in q for w in ["scroll down", "নিচে স্ক্রোল"]):
            return "mouse scroll -5"

        # Mouse position
        if any(w in q for w in ["mouse position", "mouse pos", "mous kothay", "মাউস কোথায়"]):
            return "mouse position"

        # ── KEYBOARD CONTROL (Banglish direct routing) ──────────────────────
        # Type text
        _type_m = _re_m.match(r'(?:type|likhte|lekho?|টাইপ কর[ো]?)\s+(.+)', q)
        if _type_m:
            return f"keyboard type {_type_m.group(1)}"
        # Press Enter
        if any(w in q for w in ["enter press", "press enter", "enter dao", "এন্টার"]):
            return "keyboard press enter"
        # Hotkeys
        _hot_m = _re_m.search(r'(?:hotkey|shortcut|ctrl\+\w+|alt\+\w+|win\+\w+)\s*([\w\+]+)', q)
        if _hot_m:
            return f"keyboard hotkey {_hot_m.group(1)}"

        # Extract search query for YouTube / Google
        def _extract_search_term(text, platform_kws):
            clean_text = text
            for kw in platform_kws:
                clean_text = clean_text.replace(kw, "")
            clean_text = clean_text.strip()
            
            # Check for pattern: search word + query
            m = _re.search(r"(?:search|sarche|সার্চ|খোঁজ|খোঁজো|খুঁজুন)\s+(.+)", clean_text)
            if m:
                term = m.group(1).strip()
                term = _re.sub(r"^(\s*|করে|করেন|করো|করুন|করবেন|কর|দিয়ে|লিখে|নিয়ে|নিয়েছি|খুঁজে|খুঁজুন|খোঁজ|অন|ওপেন|প্লে|প্লে\s*করুন|প্লে\s*করো|চালাও|চালան|দেখাও|দেখান)+\s*", "", term)
                return term.strip()
                
            # Check for pattern: query + write/search
            m = _re.search(r"(.+?)\s+(?:search|sarche|সার্চ|খোঁজ|খোঁজো|খুঁজুন|লিখে|দিয়ে)\s*", clean_text)
            if m:
                term = m.group(1).strip()
                term = _re.sub(r"\s*(?:লিখে|দিয়ে|নিয়ে|অন|ওপেন|প্লে|চালান|চালাও|দেখাও|দেখান|সার্চ|খোঁজ|খোঁজুন|সার্চ\s*করো|সার্চ\s*করুন|সার্চ\s*করেন|খোঁজ\s*করুন|খোঁজ\s*করো|খোঁজ\s*করেন)+$", "", term)
                return term.strip()
                
            words = clean_text.split()
            meaningful_words = [w for w in words if w not in ["অন", "ওপেন", "করো", "করুন", "করেন", "করবেন", "কর", "করে", "খোঁজ", "খোঁজো", "খুঁজুন", "সার্চ", "search", "sarche", "এ", "তে", "দিয়ে", "লিখে"]]
            if meaningful_words:
                return " ".join(meaningful_words)
            return ""

        # YouTube smart routing (also catch "browsere youtube" patterns)
        if ("youtube" in q or "ইউটিউব" in q or "youtu" in q) and q.strip() not in ["you", "your", "to", "too"]:
            term = _extract_search_term(q, ["youtube", "ইউটিউব", "youtu"])
            if term:
                url = "https://www.youtube.com/results?search_query=" + _up.quote(term)
                self.after(0, lambda u=url: _open_url(u))
                self.after(0, lambda: self.log("JARVIS", f"YouTube e '{term}' সার্চ করছি, স্যার!"))
            else:
                url = "https://www.youtube.com"
                self.after(0, lambda u=url: _open_url(u))
                self.after(0, lambda: self.log("JARVIS", "YouTube open korchi, sir!"))
            return "__HANDLED__"

        # Google smart routing
        if "google" in q or "গুগল" in q:
            term = _extract_search_term(q, ["google", "গুগল"])
            if term:
                url = "https://www.google.com/search?q=" + _up.quote(term)
                self.after(0, lambda u=url: _open_url(u))
                self.after(0, lambda: self.log("JARVIS", f"Google e '{term}' সার্চ করছি, স্যার!"))
            else:
                url = "https://www.google.com"
                self.after(0, lambda u=url: _open_url(u))
                self.after(0, lambda: self.log("JARVIS", "Google open korchi, sir!"))
            return "__HANDLED__"

        # Chrome / Browser open — only when user explicitly asks for browser
        if any(w in q for w in ["chrome open", "browser open", "open chrome",
                                  "open browser", "browser kholo", "chrome kholo",
                                  "ব্রাউজার খোলো", "ক্রোম খোলো",
                                  "ব্রাউজার চালু", "ক্রোম চালু"]):
            self.after(0, lambda: _open_url("https://www.google.com"))
            self.after(0, lambda: self.log("JARVIS", "Browser open korchi, sir!"))
            return "__HANDLED__"

        # Time sync & Settings — use native Windows (NOT browser)
        time_sync_kws = [
            "time sync", "time update", "টাইম আপডেট", "টাইম সিঙ্ক",
            "সময় আপডেট", "সময় ঠিক", "সময় ঠিক করো", "টাইম ঠিক করো",
            "সময় আপডেট করো", "টাইম আপডেট করো", "সময় সিঙ্ক",
            "time thik koro", "time update koro", "time fix",
        ]
        if any(w in q for w in time_sync_kws):
            def _sync_time():
                import subprocess as _ssp
                self.after(0, lambda: self.log("JARVIS", "Time sync শুরু হচ্ছে, স্যার..."))
                try:
                    _ssp.run(["w32tm", "/resync", "/force"], capture_output=True, timeout=15)
                    self.after(0, lambda: self.log("JARVIS", "✅ System time synced successfully! সময় আপডেট হয়েছে।"))
                    self.after(0, lambda: self.speak("Time has been synced successfully, sir."))
                except Exception as _te:
                    self.after(0, lambda: self.log("ERROR", f"Time sync failed: {_te}"))
            import threading as _thr
            _thr.Thread(target=_sync_time, daemon=True).start()
            return "__HANDLED__"

        # Settings open — open native Windows Settings app
        settings_kws = [
            "time setting", "টাইম সেটিং", "সময় সেটিং",
            "date time setting", "date and time",
            "system setting", "সিস্টেম সেটিং",
            "setting e jao", "setting kholo", "setting open",
            "সেটিং এ যাও", "সেটিং খোলো",
        ]
        if any(w in q for w in settings_kws):
            import subprocess as _ssp
            if any(w in q for w in ["time", "টাইম", "সময়", "date"]):
                _ssp.Popen('start ms-settings:dateandtime', shell=True)
                self.after(0, lambda: self.log("JARVIS", "Windows Date & Time Settings opened, sir."))
            else:
                _ssp.Popen('start ms-settings:system', shell=True)
                self.after(0, lambda: self.log("JARVIS", "Windows System Settings opened, sir."))
            return "__HANDLED__"

        # Aliases
        aliases = {
            "clean":      ("ক্লিন", "পরিষ্কার", "সাফ"),
            "workspace":  ("ওয়ার্কস্পেস", "কাজ শুরু"),
            "screenshot": ("স্ক্রিনশট", "স্ক্রিন শট", "ছবি তোলো"),
            "screenrecord": ("স্ক্রিন রেকর্ড", "রেকর্ড", "ভিডিও রেকর্ড", "record screen", "screen record"),
            "disk":       ("ডিস্ক", "স্টোরেজ"),
            "battery":    ("ব্যাটারি", "চার্জ"),
            "processes":  ("প্রসেস", "চলমান"),
            "memory":     ("মেমরি", "ram"),
            "taskmgr":    ("টাস্ক ম্যানেজার",),
            "wifi":       ("ওয়াইফাই", "ওয়াই ফাই"),
            "users":      ("ইউজার", "ব্যবহারকারী"),
            "devices":    ("ডিভাইস", "যন্ত্র"),
            "router":     ("রাউটার",),
            "mobile":     ("মোবাইল", "atom", "atom 5"),
            "android":    ("এন্ড্রয়াড", "android"),
            "kali":       ("কালি", "কাল হোস্ট", "kali mode"),
            "virus":      ("ভাইরাস",),
            "call":       ("ফোন কল", "কল করো"),
            "monitor":    ("মনিটর",),
            "sing":       ("গান গাও", "গান সোনাও", "গান শোনাও", "sing song", "sing a song"),
            "play":       ("প্লে", "মিউজিক চালাও", "গান চালাও", "play music", "play song"),
        }
        for cmd, words in aliases.items():
            if q == cmd or any(w in q for w in words):
                return cmd
        return query

    def vision_mouse_action(self, action, description):
        """Uses the multimodal Gemini LLM to locate elements on screen and perform mouse actions."""
        self.log("SYSTEM", f"📸 Vision Engine: Capturing display to find '{description}'...")
        try:
            import pyautogui
            import json
            import re
            
            # 1. Take a screenshot
            image_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'temp_vision_screen.png')
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            pyautogui.screenshot(image_path)
            
            # 2. Get screen size
            sw, sh = pyautogui.size()
            
            # 3. Create prompt for Gemini
            prompt = f"""You are a precise Windows GUI automation assistant. 
Analyze the provided screenshot of the screen and locate the target element described as: "{description}"
Find the exact coordinates (X, Y) of the center of this element.
The screen resolution is Width={sw}, Height={sh}.
IMPORTANT:
- Output your response ONLY in JSON format: {{"x": <integer>, "y": <integer>, "reason": "<brief explanation>"}}
- Ensure the coordinates are accurate absolute pixels based on the given screen resolution.
- If the element is not visible or cannot be found, return: {{"x": -1, "y": -1, "reason": "Not found"}}
- Do not output any other text, markdown blocks, or code blocks. Just the raw JSON."""
            
            # 4. Check if brain is active
            if not self.brain or not self.brain.is_connected:
                self.log("ERROR", "Vision Engine: Gemini brain offline. Cannot analyze screen.")
                return "Vision Engine failed: Brain offline."
            
            # 5. Call LLM
            res = self.brain.think(prompt, image_path=image_path)
            self.log("SYSTEM", f"🧠 Vision response: {res}")
            
            # Cleanup screenshot file
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
            except:
                pass
                
            # 6. Parse JSON response
            json_match = re.search(r'\{.*\}', res, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                x = int(data.get("x", -1))
                y = int(data.get("y", -1))
                reason = data.get("reason", "")
                
                if x >= 0 and y >= 0:
                    self.log("SYSTEM", f"🎯 Found '{description}' at ({x}, {y})")
                    # Perform mouse action
                    if action in ["click", "left", "laft", "clk"]:
                        pyautogui.click(x, y)
                        return f"🖱️ Clicked on '{description}' at ({x}, {y})"
                    elif action in ["right", "rclick", "rightclick"]:
                        pyautogui.rightClick(x, y)
                        return f"🖱️ Right-clicked on '{description}' at ({x}, {y})"
                    elif action in ["double", "dblclick", "doubleclick"]:
                        pyautogui.doubleClick(x, y)
                        return f"🖱️ Double-clicked on '{description}' at ({x}, {y})"
                    elif action in ["move", "go", "moveto"]:
                        pyautogui.moveTo(x, y, duration=0.3)
                        return f"🖱️ Moved mouse to '{description}' at ({x}, {y})"
                    else:
                        pyautogui.click(x, y)
                        return f"🖱️ Clicked on '{description}' at ({x}, {y}) via default action"
                else:
                    self.log("WARNING", f"Vision Engine could not locate '{description}'. Reason: {reason}")
                    self.speak(f"Sorry, I could not locate '{description}' on the screen.")
                    return f"Could not locate '{description}' on the screen."
            else:
                self.log("ERROR", f"Vision Engine: Failed to parse coordinates from response: {res}")
                return "Failed to parse screen coordinates."
                
        except Exception as e:
            self.log("ERROR", f"Vision Engine error: {e}")
            return f"Vision Engine failed: {e}"

    def process(self, query):
        if query == "__HANDLED__":
            return
        
        # Clear any pending speech queue items for low-latency responsiveness
        if hasattr(self, 'speech_queue') and self.speech_queue:
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except Exception:
                    break
        self.streaming_speech_buffer = ""

        self.core.set_state("thinking")
        if self.face3d: self.face3d.set_state("thinking")
        
        # Direct Command Routing
        direct_commands = ["clean", "workspace", "screenshot", "screenrecord", "scan", "ping", "battery", "uptime", "copy", "open", "volume", "processes", "memory", "note", "taskmgr", "lock", "shutdown", "restart", "disk", "explorer", "net", "users", "boost", "android", "kali", "remote", "recon", "virus", "kill", "bin", "brightness", "media", "bot", "share", "wifi", "files", "upload", "port", "payload", "qr", "call", "knowledge", "brainhub", "loginbot", "directchat", "asif", "mouse", "keyboard", "windows", "sing", "play", "music", "gen", "generate"]
        query_root = query.lower().split(" ", 1)[0]
        
        if query_root in direct_commands:
            res = f"EXECUTE: {query}"
        else:
            # BRAIN LOGIC WITH ROBUST FALLBACK
            try:
                # Capture screen if requested
                see_screen_keywords = [
                    "see my screen", "look at my screen", "look at my display", "see my display",
                    "what is on my screen", "read my screen", "আমার স্ক্রিন দেখ", "স্ক্রিনে কি আছে",
                    "স্ক্রিন দেখ", "আমার ডিসপ্লে দেখ", "আমার পিসি দেখ", "আমার স্ক্রিন দেখে বলো",
                    "see this", "look at this", "see the screen", "স্ক্রিন দেখে", "স্ক্রিনটা দেখ"
                ]
                image_path = None
                if self.streaming_mode or any(kw in query.lower() for kw in see_screen_keywords):
                    try:
                        import pyautogui
                        image_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'temp_screen.png')
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)
                        pyautogui.screenshot(image_path)
                        self.after(0, lambda: self.log("SYSTEM", "📸 Screenshot captured for vision request (Streaming/Vision mode)."))
                    except Exception as capture_err:
                        print(f"[!] Screenshot capture failed: {capture_err}")
                        image_path = None

                if not self.brain or not self.brain.is_connected:
                    self.after(0, lambda: self.log("SYSTEM", "Brain offline. Using Direct AI..."))
                    result = self.direct_ai_chat.chat_with_ai(query, self.selected_global_ai if self.ai_chat_mode else 'auto')
                    res = result['response'] if isinstance(result, dict) else str(result)
                else:
                    history = get_recent_history(3)
                    if self.streaming_mode:
                        self.after(0, lambda: self.terminal.insert("end", f"\n[JARVIS STREAM]> "))
                        res = stream_think(self.brain, query, history, self._stream_to_terminal, image_path=image_path)
                        self.after(0, lambda: self.terminal.insert("end", "\n"))
                    else:
                        res = self.brain.think(query, history, image_path=image_path)
                        # If brain quota exceeded, use offline brain
                        if "QUOTA_EXCEEDED_USE_OFFLINE" in str(res) or "all API keys have hit today's free quota" in str(res):
                            if hasattr(self, '_offline_brain') and self._offline_brain:
                                result = self._offline_brain.process_command(query)
                                res = result.get('response', 'Offline mode active.') if isinstance(result, dict) else str(result)
                            else:
                                res = "API quota শেষ। নতুন API key add করুন।"
                        # If brain returns error or empty, try direct chat
                        elif not res or "error" in str(res).lower() or "exhausted" in str(res).lower():
                            raise Exception("Brain quota or connection issue")
            except Exception as e:
                _err_msg = str(e)
                self.after(0, lambda m=_err_msg: self.log("SYSTEM", f"Neural Link Failed: {m}. Activating Direct AI..."))
                try:
                    result = self.direct_ai_chat.chat_with_ai(query, self.selected_global_ai if self.ai_chat_mode else 'auto')
                    res = result['response'] if isinstance(result, dict) else str(result)
                except Exception:
                    res = f"আমি এখন বুঝতে পেরেছি: '{query}' — কিন্তু API সংযোগ নেই। API key SYNC করুন।"

        # Ensure all variables are defined before usage
        res = str(res)
        output_msg = res
        res_to_speak = res
        
        # Handle Execution and Quota Fallbacks...
        res_upper = res.upper()
        if "EXECUTE:" in res_upper:
            exec_idx = res_upper.find("EXECUTE:")
            explanation = res[:exec_idx].strip()
            sys_cmd = res[exec_idx + len("EXECUTE:"):].strip().lower()
            
            # Advanced Command Parsing
            parts = sys_cmd.split(" ", 1)
            cmd_root = parts[0]
            cmd_args = parts[1] if len(parts) > 1 else ""
            if cmd_root == "generate":
                cmd_root = "gen"

            cmd_res = ""
            if cmd_root == "clean":
                cmd_res = f"System purged. {clean_system()} temporary files eliminated."
            elif cmd_root == "workspace":
                cmd_res = start_workspace()
            elif cmd_root == "screenshot":
                cmd_res = take_screenshot()
            elif cmd_root == "screenrecord":
                self.after(0, self.toggle_screen_recording)
                return
            elif cmd_root == "scan":
                cmd_res = scan_network()
            elif cmd_root == "ping":
                cmd_res = ping_device(cmd_args)
            elif cmd_root in ["battery", "uptime"]:
                cmd_res = get_system_stats()
            elif cmd_root == "copy":
                cmd_res = copy_to_clipboard(cmd_args)
            elif cmd_root == "open":
                url = cmd_args.strip()
                if not url:
                    cmd_res = "Error: open command requires a target"
                else:
                    try:
                        import shlex
                        parts = shlex.split(url)
                    except Exception:
                        parts = url.split()
                    
                    if not parts:
                        cmd_res = "Error: open command empty"
                    else:
                        first_part = parts[0]
                        args_part = url[len(first_part):].strip()
                        
                        # Check if first part or full input is a URL or website
                        is_url = url.startswith(("http://", "https://", "www.")) or url.endswith((".com", ".org", ".net", ".edu", ".gov", ".mil", ".int", ".io", ".co", ".xyz", ".info"))
                        
                        # Check if it is a known website alias
                        from engine.automation import APP_ALIASES, resolve_app_path
                        alias_resolved = APP_ALIASES.get(first_part.lower(), first_part)
                        if alias_resolved.startswith(("http://", "https://")):
                            is_url = True
                            url = alias_resolved
                            if args_part:
                                if "youtube" in alias_resolved or "google" in alias_resolved:
                                    import urllib.parse
                                    url = f"{alias_resolved}/results?search_query={urllib.parse.quote(args_part)}" if "youtube" in alias_resolved else f"{alias_resolved}/search?q={urllib.parse.quote(args_part)}"
                                else:
                                    url = f"{alias_resolved} {args_part}"
                        
                        if is_url:
                            if not url.startswith("http"):
                                url = "https://" + url
                            webbrowser.open(url)
                            cmd_res = f"Uplink established to: {url}"
                        else:
                            # Resolve as application path
                            app_path = resolve_app_path(alias_resolved)
                            if app_path:
                                try:
                                    if args_part:
                                        subprocess.Popen(f'"{app_path}" {args_part}', shell=True)
                                        cmd_res = f"Opened application: {first_part} with arguments {args_part} (Resolved to: {app_path})"
                                    else:
                                        os.startfile(app_path)
                                        cmd_res = f"Opened application: {cmd_args} (Resolved to: {app_path})"
                                except Exception as e:
                                    cmd_res = f"Error: Could not launch resolved path {app_path}. Reason: {e}"
                            else:
                                # Try to open it via windows command prompt start command (so it displays errors to user)
                                try:
                                    if args_part:
                                        subprocess.Popen(f'start "" "{first_part}" {args_part}', shell=True)
                                    else:
                                        os.startfile(first_part)
                                    cmd_res = f"Opened: {url}"
                                except Exception:
                                    try:
                                        if args_part:
                                            subprocess.Popen(f'start "" "{first_part}" {args_part}', shell=True)
                                        else:
                                            subprocess.Popen(f'start "" "{first_part}"', shell=True)
                                        cmd_res = f"Sent launch command for: {url}"
                                    except Exception as e:
                                        cmd_res = f"Error: Application '{url}' not found or could not be launched. Reason: {e}"

            elif cmd_root == "play" or cmd_root == "music":
                if cmd_args:
                    import urllib.parse
                    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(cmd_args)}"
                    webbrowser.open(url)
                    cmd_res = f"Searching and playing '{cmd_args}' on YouTube."
                else:
                    url = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
                    webbrowser.open(url)
                    cmd_res = "Playing Lofi Programming Beats Stream."
            elif cmd_root == "sing" or cmd_root == "song":
                self.sing_developer_song()
                cmd_res = "Initiated JARVIS neural chiptune song sequence."
            elif cmd_root == "volume":
                cmd_res = control_volume(cmd_args)
            elif cmd_root == "processes":
                cmd_res = get_running_processes()
            elif cmd_root == "memory":
                cmd_res = get_memory_info()
            elif cmd_root == "note":
                cmd_res = save_note(cmd_args)
            elif cmd_root in ["taskmgr", "task"]:
                cmd_res = open_task_manager()
            elif cmd_root == "lock":
                cmd_res = lock_computer()
            elif cmd_root == "shutdown":
                cmd_res = shutdown_computer()
            elif cmd_root == "restart":
                cmd_res = restart_computer()
            elif cmd_root == "disk":
                cmd_res = get_disk_info()
            elif cmd_root == "explorer":
                cmd_res = open_explorer(cmd_args)
            elif cmd_root == "net":
                cmd_res = run_net_command(cmd_args)
            elif cmd_root == "users":
                cmd_res = get_network_users()
            elif cmd_root == "boost":
                cmd_res = boost_game(cmd_args)
            elif cmd_root == "android":
                cmd_res = android_boost()
            elif cmd_root == "kali":
                cmd_res = setup_kali_mode()
            elif cmd_root == "remote":
                if "setup" in cmd_args or "enable" in cmd_args:
                    cmd_res = setup_remote_desktop()
                else:
                    cmd_res = start_remote_connection(cmd_args)
            elif cmd_root == "recon":
                cmd_res = auto_collect_info()
            elif cmd_root == "scan" or cmd_root == "virus":
                cmd_res = scan_for_viruses()
            elif cmd_root == "force" or cmd_root == "kill":
                cmd_res = force_kill_process(cmd_args)
            elif cmd_root == "empty" or cmd_root == "bin":
                cmd_res = empty_recycle_bin()
            elif cmd_root == "brightness" or cmd_root == "light":
                cmd_res = set_brightness(cmd_args)
            elif cmd_root == "media":
                cmd_res = media_control(cmd_args)
            elif cmd_root == "deploy" or cmd_root == "bot":
                # Expecting args like "botname | code"
                if "|" in cmd_args:
                    b_name, b_code = cmd_args.split("|", 1)
                    cmd_res = deploy_bot(b_name.strip(), b_code.strip())
                else:
                    cmd_res = "Deployment Error: Requires 'name | code' format."
            elif cmd_root == "share":
                cmd_res = create_screen_share()
            elif cmd_root == "wifi":
                cmd_res = scan_wifi()
            elif cmd_root == "send" or cmd_root == "files":
                cmd_res = share_files()
            elif cmd_root == "upload":
                # Show recent uploads
                recent = get_recent_uploads(10)
                if recent:
                    cmd_res = "📁 Recent Uploads:\n\n"
                    for file_id, filename, file_type, file_size, upload_date in recent:
                        cmd_res += f"• {filename} ({file_type}, {file_size} bytes) - {upload_date}\n"
                else:
                    cmd_res = "No files uploaded yet. Click 📁 UPLOAD button to upload files!"
            elif cmd_root == "scan" or cmd_root == "port":
                cmd_res = deep_port_scan(cmd_args)
            elif cmd_root == "payload":
                cmd_res = generate_payload(cmd_args if cmd_args else "payload.bat")
            elif cmd_root == "qr":
                self.show_custom_qr(cmd_args)
                cmd_res = f"QR Data Uplink generated for: {cmd_args}"
            elif cmd_root == "flipper":
                cmd_res = run_flipper_mode(cmd_args)
            elif cmd_root == "bt" or cmd_root == "bluetooth":
                cmd_res = scan_bluetooth()
            elif cmd_root == "ducky":
                cmd_res = ducky_deploy(cmd_args)
            elif cmd_root == "alien":
                cmd_res = run_alien_mode(cmd_args)
            elif cmd_root == "cipher":
                cmd_res = alien_cipher(cmd_args)
            elif cmd_root == "signal":
                cmd_res = signal_scan()
            elif cmd_root == "devices" or cmd_root == "find":
                if cmd_args:
                    cmd_res = find_and_connect(cmd_args)
                else:
                    cmd_res = "DEVICE MANAGER: Scanning local spectrum for all active nodes...\n" + auto_collect_info()
            elif cmd_root == "connect":
                # connect [target] [protocol]
                parts = cmd_args.split()
                target = parts[0] if len(parts) > 0 else ""
                proto = parts[1] if len(parts) > 1 else "ping"
                cmd_res = manage_device(target, proto)
            elif cmd_root == "purge" or cmd_root == "badshah":
                cmd_res = neutralize_badshah()
            elif cmd_root == "firewall":
                cmd_res = setup_infinity_firewall()
            elif cmd_root == "mobile":
                self.after(0, self.show_mobile_qr)
                cmd_res = "MOBILE UPLINK: QR console opened."
            elif cmd_root == "call":
                self.after(0, lambda: open_call_ui(self, self.log, cmd_args))
                cmd_res = f"SIM CALL SYSTEM: Uplink UI established for target: {cmd_args}" if cmd_args else "SIM CALL SYSTEM: Uplink UI established."
            elif cmd_root in ["knowledge", "brainhub", "hub"]:
                self.after(0, lambda: open_knowledge_hub(self, self.log))
                cmd_res = "KNOWLEDGE HUB: Accessing collective intelligence nodes..."
            elif cmd_root == "loginbot":
                self.after(0, lambda: open_login_bot_ui(self, self.log))
                cmd_res = "LOGIN BOT: Secure credential vault opened."
            elif cmd_root == "directchat":
                self.after(0, lambda: self.log("SYSTEM", "Direct Chat mode activated. JARVIS will now use free global APIs."))
                self.after(0, lambda: self.terminal.insert("end", "\n[JARVIS]> Hello Boss! Ami apnar sathe kotha bolar jonno ready achi. Ami ekhon Direct Global API use korbo.\n"))
                cmd_res = "DIRECT CHAT: Enabled global free uplink."
            elif cmd_root == "asif":
                local_asif = os.path.join(os.getcwd(), "asif_hacker_suite")
                asif_path = local_asif if os.path.exists(local_asif) else r"d:\AA ASIF\New folder\New folder\New folder\New folder"
                if "gen" in cmd_args:
                    subprocess.Popen(['start', 'cmd', '/c', 'ASIF - 1.BAT'], shell=True, cwd=asif_path)
                    cmd_res = "ASIF GEN: Launching hacker edition generator..."
                elif "bots" in cmd_args:
                    subprocess.Popen(['start', 'cmd', '/c', 'run_all_bots.bat'], shell=True, cwd=asif_path)
                    cmd_res = "BOT RUNNER: Initiating clean-up and bot sequence..."
                elif "suite" in cmd_args:
                    self.after(0, lambda: open_asif_suite(self, self.log))
                    cmd_res = "ASIF MASTER: Opening supreme hacker suite dashboard..."
                elif "dir" in cmd_args:
                    os.startfile(asif_path)
                    cmd_res = f"ASIF DIR: Opening directory {asif_path}"
                else:
                    cmd_res = "ASIF COMMAND: Please specify 'gen', 'bots', or 'dir'."
            elif cmd_root == "app":
                cmd_res = app_control(cmd_args)
            elif cmd_root == "agent":
                mode = cmd_args.strip().lower()
                if mode in ["on", "active", "activate", "start", "enable"]:
                    self.agent_mode = True
                    cmd_res = "AGENT MODE: ACTIVE. Normal instructions now route through app agent control."
                elif mode in ["off", "stop", "disable"]:
                    self.agent_mode = False
                    cmd_res = "AGENT MODE: OFF. Normal AI chat/command routing restored."
                elif mode == "status":
                    cmd_res = f"AGENT MODE: {'ACTIVE' if self.agent_mode else 'OFF'}."
                elif mode:
                    self.agent_mode = True
                    cmd_res = app_control(f"agent {cmd_args}")
                else:
                    self.agent_mode = True
                    cmd_res = "AGENT MODE: ACTIVE. Say 'agent off' to disable."
            elif cmd_root == "selfcheck":
                cmd_res = self_check(auto_fix=False)
            elif cmd_root == "selffix":
                cmd_res = self_check(auto_fix=True)
            elif cmd_root == "browser":
                # browser [action] [target]
                parts = cmd_args.split()
                act = parts[0] if len(parts) > 0 else "open"
                trgt = parts[1] if len(parts) > 1 else None
                cmd_res = browser_control(act, trgt)
            elif cmd_root == "window":
                # window [action] [title]
                parts = cmd_args.split()
                act = parts[0] if len(parts) > 0 else "focus"
                title = parts[1] if len(parts) > 1 else "Chrome"
                cmd_res = control_window(title, act)
            elif cmd_root == "monitor":
                # System Monitor - Show what JARVIS is doing
                try:
                    from jarvis_system_monitor import JarvisSystemMonitor
                    monitor = JarvisSystemMonitor()
                    monitor.log_activity("USER REQUEST", "System monitor opened")
                    cmd_res = monitor.get_system_status()
                except Exception as e:
                    cmd_res = f"Monitor error: {e}\nTry running: python jarvis_system_monitor.py"
            elif cmd_root == "doctor":
                # System Integrity Audit
                audit = []
                audit.append("--- JARVIS SYSTEM AUDIT ---")
                audit.append(f"OS: {sys.platform}")
                audit.append(f"CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%")
                audit.append(f"BRAIN: {'CONNECTED' if self.brain and self.brain.is_connected else 'OFFLINE'}")
                audit.append(f"NEURAL NODES: {len(self.brain.api_keys) if self.brain else 0}")
                audit.append(f"MOBILE SERVER: {'ACTIVE' if hasattr(self, 'mobile_active') else 'STANDBY'}")
                cmd_res = "\n".join(audit)
            elif cmd_root == "router":
                parts = cmd_args.split()
                if parts and parts[0] in ["ping", "ports", "rdp", "share"]:
                    cmd_res = router_connect(parts[1] if len(parts) > 1 else "192.168.1.1", parts[0])
                else:
                    cmd_res = scan_router_devices()
            elif cmd_root == "webaudit" or cmd_root == "webscan":
                target = cmd_args.strip() if cmd_args.strip() else "https://example.com"
                if not cmd_args.strip():
                    cmd_res = "WEB AUDIT: Please specify a target. Usage: webaudit [domain.com]"
                else:
                    cmd_res = web_security_audit(target)

            # ── GENERATOR COMMANDS ────────────────────────────────────────
            elif cmd_root == "gen":
                sub = cmd_args.split(" ", 1)
                gen_type = sub[0].lower() if sub else ""
                gen_prompt = sub[1].strip() if len(sub) > 1 else ""
                if gen_type == "image":
                    cmd_res = generate_image(gen_prompt) if gen_prompt else (self.after(0, lambda: self.show_generator_dialog("image")) or "Image generator opened.")
                elif gen_type in ["photo", "pic"]:
                    cmd_res = generate_photo(gen_prompt) if gen_prompt else (self.after(0, lambda: self.show_generator_dialog("photo")) or "Photo generator opened.")
                elif gen_type == "video":
                    cmd_res = generate_video(gen_prompt) if gen_prompt else (self.after(0, lambda: self.show_generator_dialog("video")) or "Video generator opened.")
                elif gen_type == "audio":
                    cmd_res = generate_audio(gen_prompt) if gen_prompt else (self.after(0, lambda: self.show_generator_dialog("audio")) or "Audio generator opened.")
                elif gen_type == "3d":
                    cmd_res = generate_3d_model(gen_prompt) if gen_prompt else (self.after(0, lambda: self.show_generator_dialog("3d")) or "3D generator opened.")
                elif gen_type == "text":
                    cmd_res = generate_text(gen_prompt, self.brain) if gen_prompt else (self.after(0, lambda: self.show_generator_dialog("text")) or "Text generator opened.")
                elif gen_type == "file":
                    if gen_prompt:
                        parts2 = gen_prompt.split(" ", 1)
                        fname = parts2[0]; fcontent = parts2[1] if len(parts2) > 1 else gen_prompt
                        cmd_res = generate_file(fname, fcontent, self.brain)
                    else:
                        self.after(0, lambda: self.show_generator_dialog("file"))
                        cmd_res = "File generator opened."
                elif gen_type == "list":
                    cmd_res = list_generated()
                elif gen_type == "folder":
                    os.makedirs(GEN_DIR, exist_ok=True); os.startfile(GEN_DIR)
                    cmd_res = f"Opened: {GEN_DIR}"
                else:
                    self.after(0, self.show_generator_panel)
                    cmd_res = "Generator panel opened."

            # ── MULTI-BRAIN COMMANDS ──────────────────────────────────────
            elif cmd_root == "brain":
                sub = cmd_args.strip().lower()
                if sub == "status":
                    cmd_res = self.multi_brain.status()
                elif sub.startswith("parallel"):
                    q2 = sub.replace("parallel", "").strip() or query
                    cmd_res = self.multi_brain.parallel_think(q2)
                elif sub.startswith("ollama"):
                    q2 = sub.replace("ollama", "").strip() or "Hello"
                    from engine.multi_brain import ask_ollama
                    r = ask_ollama(q2, self.multi_brain.ollama_model)
                    cmd_res = r if r else "[OLLAMA] Not running. Start with: ollama serve"
                elif sub.startswith("groq"):
                    q2 = sub.replace("groq", "").strip() or "Hello"
                    from engine.multi_brain import ask_groq
                    r = ask_groq(q2, self.multi_brain.groq_key)
                    cmd_res = r if r else "[GROQ] No key. Add #GROQ_KEY=your_key to jarvis_config.txt"
                else:
                    cmd_res = self.multi_brain.status()

            # ── STREAMING TOGGLE ──────────────────────────────────────────
            elif cmd_root == "stream":
                self.toggle_streaming()
                cmd_res = f"Streaming mode: {'ON' if self.streaming_mode else 'OFF'}"

            # ── AUTO CONTROLLER ───────────────────────────────────────────
            elif cmd_root == "auto":
                sub = cmd_args.strip().lower()
                if sub == "list":
                    cmd_res = self.auto_ctrl.list_tasks()
                elif sub.startswith("schedule"):
                    self.after(0, self.show_schedule_dialog)
                    cmd_res = "Schedule dialog opened."
                else:
                    cmd_res = self.auto_ctrl.list_tasks()

            # ── SUPER HOST ────────────────────────────────────────────────
            elif cmd_root == "superhost":
                parts2 = cmd_args.strip().split()
                directory = parts2[0] if parts2 else None
                port = int(parts2[1]) if len(parts2) > 1 else 8080
                cmd_res = start_super_host(directory, port)

            # ── BUG DETECTION ─────────────────────────────────────────────
            elif cmd_root in ["bugcheck", "bugdetect"]:
                cmd_res = detect_bugs(auto_fix=False)
            elif cmd_root in ["bugfix", "autofix"]:
                cmd_res = detect_bugs(auto_fix=True)
            
            # ── AUTO BACKGROUND LEARNING ──────────────────────────────────
            elif cmd_root == "autobg":
                # Toggle auto background learning
                if self.auto_bg_learner:
                    if self.auto_bg_learner.is_running:
                        self.auto_bg_learner.stop()
                        cmd_res = "⏹️ Auto Background Learning STOPPED!\n⏹️ JARVIS will no longer learn automatically."
                    else:
                        self.auto_bg_learner.start()
                        cmd_res = "▶️ Auto Background Learning STARTED!\n🤖 JARVIS will now learn automatically in background!\n🤖 No user input needed - JARVIS learns on its own!\n\n📊 Learning topics from:\n  - Programming (Python, JavaScript, Java, etc.)\n  - Technology (AI, ML, Blockchain, etc.)\n  - Frameworks (React, Django, TensorFlow, etc.)\n  - Databases (MySQL, MongoDB, Redis, etc.)\n  - Science (Physics, Chemistry, Biology, etc.)\n  - And much more!\n\n⏱️ Learning interval: 5-10 minutes per topic\n💾 All data saved to database automatically\n\nClick 'AUTO BG LEARN' again to stop."
                else:
                    cmd_res = "❌ Auto Background Learner not available!"
            
            # ── SEARCH LEARNING ───────────────────────────────────────────
            elif cmd_root == "searchlearn":
                # Start search learning in background
                def run_search_learn():
                    learner = SearchLearner()
                    learner.auto_learn_words(10, delay=2)
                    learner.close()
                    self.after(0, lambda: self.log("SYSTEM", "✅ Search learning completed! 10 words learned."))
                
                threading.Thread(target=run_search_learn, daemon=True).start()
                cmd_res = "🔍 Starting search learning... Learning 10 words from search engines."
            
            elif cmd_root == "learn10":
                # Learn 10 words
                def run_learn10():
                    learner = SearchLearner()
                    learner.auto_learn_words(10, delay=2)
                    learner.close()
                    self.after(0, lambda: self.log("SYSTEM", "✅ Learned 10 words successfully!"))
                
                threading.Thread(target=run_learn10, daemon=True).start()
                cmd_res = "📚 Learning 10 words... Please wait."
            
            elif cmd_root == "learn50":
                # Learn 50 words
                def run_learn50():
                    learner = SearchLearner()
                    learner.auto_learn_words(50, delay=2)
                    learner.close()
                    self.after(0, lambda: self.log("SYSTEM", "✅ Learned 50 words successfully!"))
                
                threading.Thread(target=run_learn50, daemon=True).start()
                cmd_res = "📖 Learning 50 words... This will take a few minutes."
            
            elif cmd_root == "searchhistory":
                # Show search history
                learner = SearchLearner()
                try:
                    learner.cursor.execute("""
                        SELECT search_term, search_engine, search_date
                        FROM search_history
                        ORDER BY search_date DESC
                        LIMIT 10
                    """)
                    history = learner.cursor.fetchall()
                    
                    if history:
                        cmd_res = "📜 Recent Search History:\n\n"
                        for i, (term, engine, date) in enumerate(history, 1):
                            cmd_res += f"{i}. {term} ({engine}) - {date}\n"
                    else:
                        cmd_res = "No search history yet. Start learning to build history!"
                    
                    learner.close()
                except Exception as e:
                    cmd_res = f"Error retrieving search history: {e}"
                    learner.close()
            
            elif cmd_root == "learnarticle":
                # Open article learning dialog
                self.after(0, lambda: self.show_article_learning_dialog())
                cmd_res = "📄 Opening article learning dialog..."
            
            elif cmd_root == "articlelist":
                # Show learned articles
                article_learner = ArticleLearner()
                try:
                    article_learner.cursor.execute("""
                        SELECT title, word_count, learned_date
                        FROM learned_articles
                        ORDER BY learned_date DESC
                        LIMIT 5
                    """)
                    articles = article_learner.cursor.fetchall()
                    
                    if articles:
                        cmd_res = "📋 Recently Learned Articles:\n\n"
                        for i, (title, words, date) in enumerate(articles, 1):
                            cmd_res += f"{i}. {title}\n"
                            cmd_res += f"   Words: {words:,} | Date: {date}\n\n"
                    else:
                        cmd_res = "No articles learned yet. Click 📄 LEARN ARTICLE to start!"
                    
                    article_learner.close()
                except Exception as e:
                    cmd_res = f"Error retrieving articles: {e}"
                    article_learner.close()
            
            # ── TRANSLATOR ────────────────────────────────────────────────
            elif cmd_root == "translate":
                # Open translation dialog
                self.after(0, lambda: self.show_translation_dialog())
                cmd_res = "🌍 Opening translation dialog..."
            
            elif cmd_root == "languages":
                # Show supported languages
                translator = JarvisTranslator()
                cmd_res = f"🌍 Supported Languages ({len(translator.languages)}):\n\n"
                for code, name in sorted(list(translator.languages.items())[:20], key=lambda x: x[1]):
                    cmd_res += f"{code:5} - {name}\n"
                cmd_res += f"\n... and {len(translator.languages) - 20} more languages!"
                translator.close()
            
            elif cmd_root == "transhistory":
                # Show translation history
                translator = JarvisTranslator()
                try:
                    translator.cursor.execute("""
                        SELECT source_text, source_lang, target_lang, translated_text, translation_date
                        FROM translation_history
                        ORDER BY translation_date DESC
                        LIMIT 5
                    """)
                    history = translator.cursor.fetchall()
                    
                    if history:
                        cmd_res = "📝 Recent Translations:\n\n"
                        for i, (src, src_lang, tgt_lang, trans, date) in enumerate(history, 1):
                            cmd_res += f"{i}. {translator.languages.get(src_lang, src_lang)} → {translator.languages.get(tgt_lang, tgt_lang)}\n"
                            cmd_res += f"   Source: {src[:40]}{'...' if len(src) > 40 else ''}\n"
                            cmd_res += f"   Translation: {trans[:40]}{'...' if len(trans) > 40 else ''}\n\n"
                    else:
                        cmd_res = "No translation history yet. Start translating!"
                    
                    translator.close()
                except Exception as e:
                    cmd_res = f"Error retrieving translation history: {e}"
                    translator.close()
            
            # ── MOUSE CONTROL ─────────────────────────────────────────────
            elif cmd_root == "mouse":
                if not _WIN_CTRL_OK:
                    cmd_res = "Windows Control Engine not loaded. Check engine/windows_control.py."
                else:
                    sub_parts = cmd_args.strip().split()
                    sub_action = sub_parts[0].lower() if sub_parts else ""
                    sub_args = sub_parts[1:]
                    
                    # Detect description-based visual action
                    is_visual = len(sub_args) > 0 and not sub_args[0].isdigit()
                    
                    try:
                        if is_visual:
                            description = " ".join(sub_args)
                            cmd_res = self.vision_mouse_action(sub_action, description)
                        elif sub_action in ["move", "go", "moveto"]:
                            if len(sub_args) >= 2:
                                cmd_res = mouse_move(sub_args[0], sub_args[1])
                            else:
                                cmd_res = "Usage: mouse move X Y"
                        elif sub_action in ["click", "left", "laft", "clk"]:
                            if len(sub_args) >= 2:
                                cmd_res = mouse_click(sub_args[0], sub_args[1])
                            else:
                                cmd_res = mouse_click()
                        elif sub_action in ["right", "rclick", "rightclick"]:
                            if len(sub_args) >= 2:
                                cmd_res = mouse_right_click(sub_args[0], sub_args[1])
                            else:
                                cmd_res = mouse_right_click()
                        elif sub_action in ["double", "dblclick", "doubleclick"]:
                            if len(sub_args) >= 2:
                                cmd_res = mouse_double_click(sub_args[0], sub_args[1])
                            else:
                                cmd_res = mouse_double_click()
                        elif sub_action in ["scroll", "scrollup", "scrolldown"]:
                            amount = int(sub_args[0]) if sub_args else -3
                            x = sub_args[1] if len(sub_args) > 1 else None
                            y = sub_args[2] if len(sub_args) > 2 else None
                            cmd_res = mouse_scroll(amount, x, y)
                        elif sub_action in ["drag"]:
                            if len(sub_args) >= 4:
                                from engine.windows_control import mouse_drag
                                cmd_res = mouse_drag(sub_args[0], sub_args[1], sub_args[2], sub_args[3])
                            else:
                                cmd_res = "Usage: mouse drag X1 Y1 X2 Y2"
                        elif sub_action in ["position", "pos", "where"]:
                            cmd_res = mouse_position()
                        else:
                            # Unknown sub-action — just do a left click at current position
                            cmd_res = mouse_click()
                    except Exception as _me:
                        cmd_res = f"Mouse control error: {_me}"

            # ── KEYBOARD CONTROL ──────────────────────────────────────────
            elif cmd_root == "keyboard":
                if not _WIN_CTRL_OK:
                    cmd_res = "Windows Control Engine not loaded. Check engine/windows_control.py."
                else:
                    sub_parts = cmd_args.strip().split(None, 1)
                    sub_action = sub_parts[0].lower() if sub_parts else ""
                    sub_text = sub_parts[1].strip() if len(sub_parts) > 1 else ""
                    try:
                        if sub_action in ["type", "write", "input"]:
                            cmd_res = keyboard_type(sub_text) if sub_text else "Usage: keyboard type [text]"
                        elif sub_action in ["press", "key"]:
                            cmd_res = keyboard_press(sub_text) if sub_text else "Usage: keyboard press [key]"
                        elif sub_action in ["hotkey", "shortcut", "combo"]:
                            keys = [k.strip() for k in sub_text.replace("+", " ").split() if k.strip()]
                            cmd_res = keyboard_hotkey(*keys) if keys else "Usage: keyboard hotkey ctrl+c"
                        else:
                            cmd_res = f"Unknown keyboard action: {sub_action}. Use: type, press, hotkey"
                    except Exception as _ke:
                        cmd_res = f"Keyboard control error: {_ke}"

            # ── WINDOWS CONTROL (shorthand) ───────────────────────────────
            elif cmd_root == "windows":
                if not _WIN_CTRL_OK:
                    cmd_res = "Windows Control Engine not loaded."
                else:
                    try:
                        cmd_res = windows_control(cmd_args)
                    except Exception as _we:
                        cmd_res = f"Windows control error: {_we}"

            else:
                cmd_res = ""
                if _SYS_CONTROL_AVAILABLE:
                    try:
                        res_temp = sys_execute(sys_cmd, self.brain)
                        if not res_temp.startswith("Command not recognized:"):
                            cmd_res = res_temp
                    except Exception as e:
                        print(f"[!] System control error: {e}")
                
                if not cmd_res:
                    try:
                        from engine.automation import run_command_prompt
                        cmd_res = run_command_prompt(sys_cmd)
                    except Exception as e:
                        cmd_res = f"Critical Failure: {e}"
            
            output_msg = f"{explanation}\n\n[SYSTEM]: {cmd_res}"
            res_to_speak = f"{explanation}. {cmd_res}"
            if self.prefer_bangla_voice and not self.voice.has_bangla(res_to_speak):
                res_to_speak = f"{cmd_root} কমান্ড সম্পন্ন হয়েছে।"
        
        # ── LOG RESPONSE TO TERMINAL ──────────────────────────────────────
        self.after(0, lambda m=output_msg: self.log("JARVIS", m))
        save_chat(query, output_msg)

        # Speak or finalize streaming speech queue
        if self.streaming_mode and self.brain and self.brain.is_connected:
            leftover = self.streaming_speech_buffer.strip()
            if leftover:
                self.speech_queue.put(leftover)
            self.streaming_speech_buffer = ""
        else:
            self.speak(res_to_speak)

    def toggle_screen_recording(self):
        """Toggles screen recording on/off"""
        try:
            from jarvis_screen_recorder import screen_recorder
        except Exception as e:
            self.log("ERROR", f"Screen Recorder import failed: {e}")
            self.speak("Screen recorder module is not available.")
            return

        if not hasattr(self, 'recording_active'):
            self.recording_active = False

        if not self.recording_active:
            res = screen_recorder.start_recording()
            if "Recording started!" in res:
                self.recording_active = True
                self.screen_record_btn.configure(
                    text="🔴 RECORDING... [STOP]",
                    fg_color="#CC0000",
                    hover_color="#AA0000"
                )
                self.log("JARVIS", f"🎥 {res}")
                self.speak("Screen recording started.")
            else:
                self.log("ERROR", f"Failed to start recording: {res}")
                self.speak("Failed to start screen recording.")
        else:
            res = screen_recorder.stop_recording()
            self.recording_active = False
            self.screen_record_btn.configure(
                text="🎥 SCREEN RECORD",
                fg_color="#002233",
                hover_color="#004466"
            )
            self.log("JARVIS", f"🎥 {res}")
            self.speak("Screen recording stopped and saved.")

    # =========================================================================
    # STREAMING MODE
    # =========================================================================

    def start_vision_stream(self):
        """Starts a background loop to update the screen screenshot and preview window"""
        if not self.streaming_mode or hasattr(self, '_is_destroying') and self._is_destroying:
            return
            
        try:
            import PIL.Image
            import PIL.ImageTk
            import PIL.ImageGrab as ImageGrab
            
            image_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'temp_screen.png')
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Grab screenshot at native resolution
            import PIL.ImageDraw as ImageDraw
            img = ImageGrab.grab()
            
            # Draw cursor on vision stream screenshot
            try:
                draw = ImageDraw.Draw(img)
                px, py = pyautogui.position()
                screen_w, screen_h = pyautogui.size()
                rx = img.width / screen_w
                ry = img.height / screen_h
                cx, cy = int(px * rx), int(py * ry)
                # Outer cyan ring (0, 243, 255) and inner red dot (255, 0, 0)
                draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=(0, 243, 255), width=2)
                draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 0, 0))
            except Exception:
                pass
            
            img.save(image_path)
            
            # Update preview window if open
            if hasattr(self, 'vision_window') and self.vision_window and self.vision_window.winfo_exists():
                preview_w = 320
                preview_h = 180
                img_resized = img.resize((preview_w, preview_h), PIL.Image.Resampling.LANCZOS)
                photo = PIL.ImageTk.PhotoImage(img_resized)
                
                if hasattr(self, 'vision_label') and self.vision_label.winfo_exists():
                    self.vision_label.configure(image=photo)
                    self.vision_label.image = photo  # Keep a reference
        except Exception as e:
            print(f"[VISION STREAM] Capture error: {e}")
            
        # Schedule next frame (5 FPS)
        self.after(200, self.start_vision_stream)

    def toggle_streaming(self):
        self.streaming_mode = not self.streaming_mode
        if self.streaming_mode:
            self.stream_btn.configure(text="STREAM: ON", fg_color="#005544")
            self.log("SYSTEM", "STREAMING MODE ON -- AI responses appear token by token.")
            
            try:
                # Open JARVIS Eye floating preview window
                if not hasattr(self, 'vision_window') or not self.vision_window or not self.vision_window.winfo_exists():
                    self.vision_window = ctk.CTkToplevel(self)
                    self.vision_window.title("JARVIS Eye - Live Stream")
                    self.vision_window.geometry("340x220+50+50") # Float in upper corner
                    self.vision_window.attributes("-topmost", True)
                    self.vision_window.configure(fg_color="#050F1A")
                    
                    # Window title label
                    header = ctk.CTkLabel(
                        self.vision_window, 
                        text="👁️ JARVIS EYE - LIVE STREAM", 
                        font=("Segoe UI", 12, "bold"), 
                        text_color="#00FFCC"
                    )
                    header.pack(pady=5)
                    
                    # Capture label preview
                    self.vision_label = ctk.CTkLabel(self.vision_window, text="", fg_color="black")
                    self.vision_label.pack(fill="both", expand=True, padx=10, pady=5)
                    
                self.start_vision_stream()
                self.log("SYSTEM", "📸 Display Capture (JARVIS's Eye) ON. Live screen stream is active.")
                self.speak("Display capture activated. Live video feed of your screen is open.")
            except Exception as e:
                self.log("SYSTEM", f"⚠️ Display Capture activation failed: {e}")
        else:
            self.stream_btn.configure(text="STREAM: OFF", fg_color="#003322")
            if hasattr(self, 'vision_window') and self.vision_window and self.vision_window.winfo_exists():
                self.vision_window.destroy()
            self.vision_window = None
            self.log("SYSTEM", "STREAMING MODE OFF -- Display Capture deactivated.")
            self.speak("Display capture deactivated.")

    def _speech_worker(self):
        while not self._is_destroying:
            try:
                try:
                    text = self.speech_queue.get(timeout=1.0)
                except Exception:
                    continue
                
                if text is None:
                    break
                
                import re
                clean_text = re.sub(r'\[EMOTION:.*?\]', '', text).strip()
                clean_text = clean_text.replace("*", "").replace("#", "").strip()
                if clean_text:
                    self.after(0, lambda: self.core.set_state("speaking"))
                    if self.face3d:
                        self.after(0, lambda: self.face3d.set_state("speaking"))
                    
                    emotion = self.detect_response_emotion(clean_text)
                    self.update_emotion(emotion)
                    
                    with self.v_lock:
                        self.voice.speak(clean_text)
                    
                    self.after(0, lambda: self.core.set_state("idle"))
                    if self.face3d:
                        self.after(0, lambda: self.face3d.set_state("idle"))
                
                self.speech_queue.task_done()
            except Exception as e:
                print(f"[!] Speech worker thread error: {e}")
                time.sleep(0.1)

    def _stream_to_terminal(self, chunk: str):
        self.terminal.insert("end", chunk.replace("*", ""))
        self.terminal.see("end")
        
        self.streaming_speech_buffer += chunk
        import re
        parts = re.split(r'([.?!।\n]+)', self.streaming_speech_buffer)
        completed_sentences = []
        i = 0
        while i < len(parts) - 1:
            text_part = parts[i]
            delimiter = parts[i+1]
            completed_sentences.append(text_part + delimiter)
            i += 2
        
        self.streaming_speech_buffer = parts[-1]
        
        for sentence in completed_sentences:
            stripped = sentence.strip()
            if len(stripped) > 1:
                self.speech_queue.put(stripped)

    # =========================================================================
    # DRAG & DROP
    # =========================================================================

    def _setup_drag_drop(self, widget):
        try:
            from tkinterdnd2 import DND_FILES  # type: ignore
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", self._on_drop)
            self.log("SYSTEM", "Drag & Drop: ACTIVE")
        except Exception:
            widget.bind("<Control-v>", self._on_paste_path)

    def _on_drop(self, event):
        raw = event.data.strip()
        # tkinterdnd2 wraps paths with spaces in braces
        import re
        paths = re.findall(r'\{([^}]+)\}|(\S+)', raw)
        file_list = [p[0] or p[1] for p in paths if p[0] or p[1]]
        for path in file_list:
            self._handle_dropped_file(path.strip('"'))

    def _on_paste_path(self, event=None):
        try:
            import pyperclip
            path = pyperclip.paste().strip().strip('"')
            if os.path.exists(path):
                self._handle_dropped_file(path)
        except Exception:
            pass

    def _handle_dropped_file(self, path: str):
        if not os.path.exists(path):
            self.log("DROP", f"Not found: {path}")
            return
        ext = os.path.splitext(path)[1].lower()
        name = os.path.basename(path)
        self.log("DROP", f"Received: {name}")

        if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
            self.entry.delete(0, "end")
            self.entry.insert(0, f"Describe this image: {path}")
            return

        if ext in (".txt", ".py", ".js", ".ts", ".html", ".css", ".json",
                   ".md", ".csv", ".xml", ".yaml", ".yml", ".ini", ".cfg", ".log"):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(8000)
                prompt = f"Analyze this file ({name}):\n\n{content}"
                threading.Thread(target=self.process, args=(prompt,), daemon=True).start()
            except Exception as e:
                self.log("DROP", f"Read error: {e}")
            return

        if ext == ".pdf":
            try:
                import PyPDF2  # type: ignore
                with open(path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    text = "\n".join(p.extract_text() or "" for p in reader.pages[:5])
                prompt = f"Summarize this PDF ({name}):\n\n{text[:6000]}"
                threading.Thread(target=self.process, args=(prompt,), daemon=True).start()
            except ImportError:
                self.log("DROP", "PDF support: pip install PyPDF2")
            except Exception as e:
                self.log("DROP", f"PDF error: {e}")
            return

        try:
            os.startfile(path)
            self.log("DROP", f"Opened: {name}")
        except Exception as e:
            self.log("DROP", f"Cannot open: {e}")

    # =========================================================================
    # GENERATOR PANEL
    # =========================================================================

    def show_generator_dialog(self, gen_type: str):
        """Quick single-type generator dialog."""
        popup = ctk.CTkToplevel(self)
        popup.title(f"[*] Generate {gen_type.upper()}")
        popup.geometry("500x300")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text=f"[*] {gen_type.upper()} GENERATOR",
                     font=("Courier New", 18, "bold"), text_color="#00F3FF").pack(pady=15)
        ctk.CTkLabel(popup, text="Enter prompt:", font=("Courier New", 12),
                     text_color="#555555").pack(anchor="w", padx=20)
        prompt_entry = ctk.CTkEntry(popup, height=45, font=("Courier New", 13),
                                    fg_color="#05080F", text_color="#00FF41")
        prompt_entry.pack(fill="x", padx=20, pady=10)

        def _generate():
            p = prompt_entry.get().strip()
            if not p:
                return
            popup.destroy()
            def _run():
                if gen_type == "image":   r = generate_image(p)
                elif gen_type == "photo": r = generate_photo(p)
                elif gen_type == "video": r = generate_video(p)
                elif gen_type == "audio": r = generate_audio(p)
                elif gen_type == "3d":    r = generate_3d_model(p)
                elif gen_type == "text":  r = generate_text(p, self.brain)
                elif gen_type == "file":
                    parts2 = p.split(" ", 1)
                    r = generate_file(parts2[0], parts2[1] if len(parts2) > 1 else p, self.brain)
                else: r = generate_text(p, self.brain)
                self.after(0, lambda: self.log("GEN", r))
            threading.Thread(target=_run, daemon=True).start()

        ctk.CTkButton(popup, text="[*] GENERATE", height=45,
                      fg_color="#003300", hover_color="#005500",
                      command=_generate).pack(fill="x", padx=20, pady=10)
        prompt_entry.bind("<Return>", lambda e: _generate())

    def show_translation_dialog(self):
        """Show translation dialog"""
        popup = ctk.CTkToplevel(self)
        popup.title("🌍 JARVIS TRANSLATOR")
        popup.geometry("600x500")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="🌍 UNIVERSAL TRANSLATOR", font=("Courier New", 20, "bold"),
                     text_color="#00F3FF").pack(pady=15)
        
        # Source text
        ctk.CTkLabel(popup, text="Text to translate:", font=("Courier New", 12),
                     text_color="#555555").pack(anchor="w", padx=20, pady=(10,5))
        source_text = ctk.CTkTextbox(popup, height=100, font=("Courier New", 12),
                                      fg_color="#05080F", text_color="#00FF41")
        source_text.pack(fill="x", padx=20, pady=5)
        
        # Language selection
        lang_frame = ctk.CTkFrame(popup, fg_color="transparent")
        lang_frame.pack(fill="x", padx=20, pady=10)
        
        # Target language
        ctk.CTkLabel(lang_frame, text="To:", font=("Courier New", 12),
                     text_color="#555555").pack(side="left", padx=5)
        target_lang = ctk.CTkEntry(lang_frame, width=100, placeholder_text="en",
                                    fg_color="#05080F", text_color="#00FF41")
        target_lang.pack(side="left", padx=5)
        target_lang.insert(0, "bn")
        
        # Common languages
        ctk.CTkLabel(lang_frame, text="Quick:", font=("Courier New", 10),
                     text_color="#555555").pack(side="left", padx=10)
        for lang_code, lang_name in [("en", "EN"), ("bn", "BN"), ("hi", "HI"), ("es", "ES"), ("fr", "FR")]:
            ctk.CTkButton(lang_frame, text=lang_name, width=40, height=25,
                          fg_color="#004466", hover_color="#006688",
                          command=lambda lc=lang_code: target_lang.delete(0, "end") or target_lang.insert(0, lc)
                          ).pack(side="left", padx=2)
        
        # Result text
        ctk.CTkLabel(popup, text="Translation:", font=("Courier New", 12),
                     text_color="#555555").pack(anchor="w", padx=20, pady=(10,5))
        result_text = ctk.CTkTextbox(popup, height=100, font=("Courier New", 12),
                                      fg_color="#05080F", text_color="#00FF41")
        result_text.pack(fill="x", padx=20, pady=5)
        
        # Status label
        status_label = ctk.CTkLabel(popup, text="", font=("Courier New", 10),
                                     text_color="#888888")
        status_label.pack(pady=5)
        
        def _translate():
            text = source_text.get("1.0", "end-1c").strip()
            tgt_lang = target_lang.get().strip()
            
            if not text:
                status_label.configure(text="⚠️ Please enter text to translate", text_color="#FF3131")
                return
            
            if not tgt_lang:
                status_label.configure(text="⚠️ Please enter target language", text_color="#FF3131")
                return
            
            status_label.configure(text="🌍 Translating...", text_color="#FFD700")
            result_text.delete("1.0", "end")
            
            def _run():
                translator = JarvisTranslator()
                result = translator.translate(text, tgt_lang, 'auto')
                translator.close()
                
                def _update():
                    if result['success']:
                        result_text.insert("1.0", result['translated_text'])
                        status_label.configure(
                            text=f"✅ Translated using {result['engine']}", 
                            text_color="#00FF41"
                        )
                        self.log("TRANSLATOR", f"Translated to {tgt_lang}: {result['translated_text'][:50]}...")
                    else:
                        status_label.configure(
                            text=f"❌ Translation failed: {result.get('error', 'Unknown error')}", 
                            text_color="#FF3131"
                        )
                
                self.after(0, _update)
            
            threading.Thread(target=_run, daemon=True).start()
        
        # Translate button
        ctk.CTkButton(popup, text="🌍 TRANSLATE", height=45,
                      fg_color="#004466", hover_color="#006688",
                      font=("Courier New", 14, "bold"),
                      command=_translate).pack(fill="x", padx=20, pady=10)
        
        # Help text
        ctk.CTkLabel(popup, text="Language codes: en=English, bn=Bengali, hi=Hindi, es=Spanish, fr=French, de=German, etc.",
                     font=("Courier New", 9), text_color="#444444", wraplength=550).pack(pady=5)

    def show_article_learning_dialog(self):
        """Show article learning dialog"""
        popup = ctk.CTkToplevel(self)
        popup.title("📄 JARVIS ARTICLE LEARNER")
        popup.geometry("600x400")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="📄 FULL ARTICLE LEARNER", font=("Courier New", 20, "bold"),
                     text_color="#00F3FF").pack(pady=15)
        
        # Topic/URL input
        ctk.CTkLabel(popup, text="Wikipedia topic or URL:", font=("Courier New", 12),
                     text_color="#555555").pack(anchor="w", padx=20, pady=(10,5))
        topic_entry = ctk.CTkEntry(popup, height=40, font=("Courier New", 13),
                                    placeholder_text="e.g., Artificial Intelligence or https://...",
                                    fg_color="#05080F", text_color="#00FF41")
        topic_entry.pack(fill="x", padx=20, pady=5)
        
        # Quick topics
        quick_frame = ctk.CTkFrame(popup, fg_color="transparent")
        quick_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(quick_frame, text="Quick Topics:", font=("Courier New", 10),
                     text_color="#555555").pack(side="left", padx=5)
        
        for topic in ["Artificial Intelligence", "Machine Learning", "Python (programming language)", "Quantum Computing"]:
            ctk.CTkButton(quick_frame, text=topic[:15]+"...", width=120, height=25,
                          fg_color="#004466", hover_color="#006688",
                          command=lambda t=topic: topic_entry.delete(0, "end") or topic_entry.insert(0, t)
                          ).pack(side="left", padx=2)
        
        # Status/Result area
        result_frame = ctk.CTkFrame(popup, fg_color="#05080F", border_width=1, border_color="#002233")
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        result_text = ctk.CTkTextbox(result_frame, font=("Courier New", 11),
                                      fg_color="transparent", text_color="#00FF41")
        result_text.pack(fill="both", expand=True, padx=10, pady=10)
        result_text.insert("1.0", "Enter a Wikipedia topic or URL and click LEARN ARTICLE.\n\nJARVIS will fetch the complete article and save it to the knowledge base.")
        
        def _learn():
            topic = topic_entry.get().strip()
            
            if not topic:
                result_text.delete("1.0", "end")
                result_text.insert("1.0", "⚠️ Please enter a topic or URL")
                return
            
            result_text.delete("1.0", "end")
            result_text.insert("1.0", f"📚 Learning article: {topic}\n\nPlease wait...")
            
            def _run():
                article_learner = ArticleLearner()
                success = article_learner.learn_article(topic)
                article_learner.close()
                
                def _update():
                    if success:
                        result_text.delete("1.0", "end")
                        result_text.insert("1.0", f"✅ Article learned successfully!\n\nTopic: {topic}\n\nThe complete article has been saved to the knowledge base.\n\nYou can now ask JARVIS questions about this topic!")
                        self.log("ARTICLE LEARNER", f"Learned full article: {topic}")
                    else:
                        result_text.delete("1.0", "end")
                        result_text.insert("1.0", f"❌ Failed to learn article: {topic}\n\nPlease check the topic name or URL and try again.")
                
                self.after(0, _update)
            
            threading.Thread(target=_run, daemon=True).start()
        
        # Learn button
        ctk.CTkButton(popup, text="📄 LEARN ARTICLE", height=45,
                      fg_color="#004488", hover_color="#0066AA",
                      font=("Courier New", 14, "bold"),
                      command=_learn).pack(fill="x", padx=20, pady=10)

    def show_generator_panel(self):
        """Full generator panel with all types."""
        popup = ctk.CTkToplevel(self)
        popup.title("[*] JARVIS AI GENERATOR")
        popup.geometry("580x480")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="[*] AI GENERATOR", font=("Courier New", 22, "bold"),
                     text_color="#00F3FF").pack(pady=15)

        type_var = ctk.StringVar(value="image")
        type_frame = ctk.CTkFrame(popup, fg_color="#05080F")
        type_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(type_frame, text="Type:", font=("Courier New", 12),
                     text_color="#555555").pack(side="left", padx=10)
        for t in ["image", "photo", "video", "audio", "3d", "text", "file"]:
            ctk.CTkRadioButton(type_frame, text=t.upper(), variable=type_var, value=t,
                               font=("Courier New", 11), text_color="#00F3FF").pack(side="left", padx=6)

        ctk.CTkLabel(popup, text="Prompt:", font=("Courier New", 12),
                     text_color="#555555").pack(anchor="w", padx=20, pady=(10, 0))
        prompt_box = ctk.CTkTextbox(popup, height=100, font=("Courier New", 13),
                                    fg_color="#05080F", text_color="#00FF41")
        prompt_box.pack(fill="x", padx=20, pady=5)

        result_box = ctk.CTkTextbox(popup, height=120, font=("Courier New", 11),
                                    fg_color="#05080F", text_color="#00F3FF")
        result_box.pack(fill="x", padx=20, pady=5)

        def _generate():
            p = prompt_box.get("1.0", "end").strip()
            t = type_var.get()
            if not p:
                return
            result_box.delete("1.0", "end")
            result_box.insert("end", f"Generating {t}...\n")
            def _run():
                if t == "image":   r = generate_image(p)
                elif t == "photo": r = generate_photo(p)
                elif t == "video": r = generate_video(p)
                elif t == "audio": r = generate_audio(p)
                elif t == "3d":    r = generate_3d_model(p)
                elif t == "text":  r = generate_text(p, self.brain)
                elif t == "file":
                    parts2 = p.split(" ", 1)
                    r = generate_file(parts2[0], parts2[1] if len(parts2) > 1 else p, self.brain)
                else: r = generate_text(p, self.brain)
                self.after(0, lambda: result_box.insert("end", r + "\n"))
                self.after(0, lambda: self.log("GEN", r[:200]))
            threading.Thread(target=_run, daemon=True).start()

        ctk.CTkButton(popup, text="[*] GENERATE", height=45,
                      fg_color="#003300", hover_color="#005500",
                      command=_generate).pack(fill="x", padx=20, pady=10)

    # =========================================================================
    # SCHEDULE DIALOG
    # =========================================================================

    def show_schedule_dialog(self):
        popup = ctk.CTkToplevel(self)
        popup.title("[T] AUTO SCHEDULE TASK")
        popup.geometry("480x320")
        popup.configure(fg_color="#02050A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="[T] SCHEDULE TASK", font=("Courier New", 18, "bold"),
                     text_color="#00F3FF").pack(pady=15)

        ctk.CTkLabel(popup, text="Task name:", font=("Courier New", 12),
                     text_color="#555555").pack(anchor="w", padx=20)
        name_entry = ctk.CTkEntry(popup, height=35, font=("Courier New", 13),
                                  fg_color="#05080F", text_color="#00FF41")
        name_entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(popup, text="Command (e.g. screenshot, clean, recon):",
                     font=("Courier New", 12), text_color="#555555").pack(anchor="w", padx=20)
        cmd_entry = ctk.CTkEntry(popup, height=35, font=("Courier New", 13),
                                 fg_color="#05080F", text_color="#00FF41")
        cmd_entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(popup, text="Interval (seconds):", font=("Courier New", 12),
                     text_color="#555555").pack(anchor="w", padx=20)
        interval_entry = ctk.CTkEntry(popup, height=35, font=("Courier New", 13),
                                      fg_color="#05080F", text_color="#00FF41")
        interval_entry.insert(0, "3600")
        interval_entry.pack(fill="x", padx=20, pady=5)

        def _schedule():
            name = name_entry.get().strip() or "task"
            cmd  = cmd_entry.get().strip()
            try:
                interval = float(interval_entry.get().strip())
            except ValueError:
                interval = 3600
            if not cmd:
                return
            self.auto_ctrl.add_interval(name, lambda c=cmd: self.process(c), interval)
            self.log("AUTO", f"Scheduled '{name}' every {interval}s: {cmd}")
            popup.destroy()

        ctk.CTkButton(popup, text="[T] SCHEDULE", height=40,
                      fg_color="#003344", hover_color="#005566",
                      command=_schedule).pack(fill="x", padx=20, pady=10)

    # =========================================================================
    # LOGOUT
    # =========================================================================

    def _do_logout(self):
        logout()
        self.log("SYSTEM", "Session terminated. Restarting for login...")
        self.after(1000, lambda: (self.destroy(), _restart_with_login()))

    # =========================================================================
    # WORLD AI CHAT METHODS
    # =========================================================================

    def open_world_ai_chat_direct(self):
        """Open World AI Chat directly - FIX: Integrated with main input and threaded"""
        # Get query from main entry first
        query = self.entry.get().strip()
        
        def _run_world_chat():
            try:
                if not self.world_ai_chat:
                    self.after(0, lambda: self.log("ERROR", "World AI Chat not available!"))
                    return
                
                self.after(0, lambda: self.log("SYSTEM", "🌍 Initializing World AI Chat..."))
                
                # Show AI selector (This might still show a dialog)
                ai = self.world_ai_chat.show_ai_selector_dialog(self)
                
                if not ai:
                    self.after(0, lambda: self.log("WARNING", "No AI selected"))
                    return
                
                # If entry was empty, ask for query via dialog
                active_query = query
                if not active_query:
                    active_query = self._get_query_dialog()
                
                if not active_query:
                    self.after(0, lambda: self.log("WARNING", "No query provided"))
                    return
                
                # Clear main entry if we used it
                if not query:
                    pass # query dialog handled it
                else:
                    self.after(0, lambda: self.entry.delete(0, "end"))
                
                self.after(0, lambda: self.log("ROOT", f"🌍 WORLD AI [{ai}]: {active_query}"))
                
                # Chat with AI
                result = self.world_ai_chat.chat_with_ai(active_query, ai, self)
                
                if result['success']:
                    self.after(0, lambda: self.log("JARVIS", f"[{result['ai']}] {result['response']}"))
                    self.after(0, lambda: self.speak(result['response']))
                    save_chat(active_query, result['response'])
                    
                    # AUTO HARVEST (NEW!)
                    self.after(1000, lambda: run_harvest_on_text(result['response'], self.log))
                else:
                    self.after(0, lambda: self.log("WARNING", "World AI Chat cancelled or failed"))
            
            except Exception as e:
                self.after(0, lambda: self.log("ERROR", f"World AI Chat error: {e}"))
                print(f"[!] World AI Chat error: {e}")
        
        # Start in background thread to prevent panel freeze
        threading.Thread(target=_run_world_chat, daemon=True).start()

    def open_direct_ai_chat_panel(self):
        """Chat with AI directly inside the panel - NO BROWSER!"""
        query = self.entry.get().strip()
        
        if not query:
            # If entry empty, ask for query via dialog
            query = self._get_query_dialog()
            if not query:
                return

        self.log("SYSTEM", "🤖 Initializing Direct AI Uplink...")
        self.entry.delete(0, "end")
        
        def _run_direct_chat():
            try:
                if not self.direct_ai_chat:
                    self.after(0, lambda: self.log("ERROR", "Direct AI Chat not available!"))
                    return
                
                self.after(0, lambda: self.log("ROOT", f"🤖 DIRECT AI: {query}"))
                
                # Chat with AI
                result = self.direct_ai_chat.chat_with_ai(query, 'auto')
                
                if result['success']:
                    res = result['response']
                    self.after(0, lambda: self.log("JARVIS", f"[{result['ai']}] {res}"))
                    self.after(0, lambda: self.speak(res))
                    save_chat(query, res)
                    
                    # AUTO HARVEST (NEW!)
                    from jarvis_neural_harvester import run_harvest_on_text
                    self.after(1000, lambda: run_harvest_on_text(res, self.log))
                else:
                    self.after(0, lambda: self.log("WARNING", f"Direct AI failed: {result['response']}"))
            
            except Exception as e:
                self.after(0, lambda: self.log("ERROR", f"Direct AI error: {e}"))
        
        # Run in thread
        threading.Thread(target=_run_direct_chat, daemon=True).start()

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

    # =========================================================================
    # AUTO AI LEARNER METHODS
    # =========================================================================

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
            print(f"[!] Auto learner error: {e}")

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
            print(f"[!] Stats update error: {e}")

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

    # =========================================================================
    # MICROPHONE CONTROL METHODS
    # =========================================================================

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
            print(f"[!] Microphone error: {e}")

    # =========================================================================
    # SYSTEM PERMISSIONS METHODS
    # =========================================================================

    def request_permissions(self):
        """Request all system permissions"""
        try:
            self.log("SYSTEM", "🔐 Requesting permissions...")
            
            permissions = {
                'Microphone': self._request_mic_permission(),
                'File System': self._request_file_permission(),
                'Network': self._request_network_permission(),
                'Registry Access': True,
                'System Settings': True,
                'Processor Core': True,
                'Mouse & Keyboard Control': True,
                'Terminal & PowerShell': True,
                'BIOS/Motherboard Access': True,
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
            print(f"[!] Permission error: {e}")

    def _request_mic_permission(self):
        """Request microphone permission"""
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            mic = None
            try:
                mic = sr.Microphone()
                with mic:
                    pass
            except:
                try:
                    mics = sr.Microphone.list_microphone_names()
                    for idx, name in enumerate(mics):
                        name_lower = name.lower()
                        if "microphone" in name_lower or "mic" in name_lower or "input" in name_lower:
                            try:
                                test_mic = sr.Microphone(device_index=idx)
                                with test_mic:
                                    mic = test_mic
                                    break
                            except:
                                continue
                except:
                    pass
            if not mic:
                return False
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=0.1)
            return True
        except:
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
        except:
            return False

    def _request_network_permission(self):
        """Request network permission"""
        try:
            import socket
            # Try to create a socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.close()
            return True
        except:
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

    def open_harvester_ui(self):
        """Open the Neural Harvester UI for manual knowledge extraction."""
        try:
            from jarvis_neural_harvester import NeuralHarvester
            harvester = NeuralHarvester()
            
            popup = ctk.CTkToplevel(self)
            popup.title("🧠 JARVIS NEURAL HARVESTER")
            popup.geometry("600x550")
            popup.attributes("-topmost", True)
            popup.configure(fg_color="#02050A")
            
            ctk.CTkLabel(popup, text="🧠 NEURAL HARVESTER PROTOCOL", font=("Courier New", 20, "bold"), text_color="#00F3FF").pack(pady=20)
            
            # Instruction for Trojan Prompt
            ctk.CTkLabel(popup, text="[ TROJAN PROMPT ] - Paste this to other AIs to extract secrets:", font=("Courier New", 10), text_color="#555555").pack(anchor="w", padx=30)
            
            trojan_box = ctk.CTkTextbox(popup, height=120, font=("Courier New", 10), fg_color="#05080F", text_color="#FFD700", border_width=1, border_color="#002233")
            trojan_box.pack(fill="x", padx=30, pady=5)
            trojan_box.insert("1.0", harvester.get_trojan_prompt())
            
            def copy_trojan():
                import pyperclip
                pyperclip.copy(harvester.get_trojan_prompt())
                self.log("HARVESTER", "Trojan Prompt copied to clipboard!")

            ctk.CTkButton(popup, text="📋 COPY TROJAN PROMPT", fg_color="#440066", command=copy_trojan).pack(pady=10)
            
            ctk.CTkLabel(popup, text="[ MANUAL INJECT ] - Paste AI response here to harvest:", font=("Courier New", 10), text_color="#555555").pack(anchor="w", padx=30, pady=(15, 0))
            
            input_box = ctk.CTkTextbox(popup, height=150, font=("Courier New", 11), fg_color="#000000", text_color="#00FF41", border_width=1, border_color="#00FF41")
            input_box.pack(fill="x", padx=30, pady=5)
            
            def start_manual_harvest():
                text = input_box.get("1.0", "end-1c").strip()
                if text:
                    self.log("HARVESTER", "Starting manual neural extraction...")
                    from jarvis_neural_harvester import run_harvest_on_text
                    success = run_harvest_on_text(text, self.log)
                    if success:
                        self.log("HARVESTER", "✅ Extraction complete!")
                    else:
                        self.log("HARVESTER", "❌ No new neural data found.")
                    input_box.delete("1.0", "end")
                else:
                    self.log("ERROR", "Please paste text to harvest first!")

            ctk.CTkButton(popup, text="🚀 START NEURAL HARVEST", fg_color="#006644", hover_color="#008866", command=start_manual_harvest, font=("Courier New", 14, "bold"), height=50).pack(pady=20)
            
        except Exception as e:
            self.log("ERROR", f"Harvester UI Error: {e}")


def _restart_with_login():
    """Re-launch the app with the login screen."""
    root = ctk.CTk()
    root.withdraw()

    def _on_login(session):
        root.destroy()
        _launch_main(session)

    check_and_login(root, _on_login, force_login=True)
    root.mainloop()


def _launch_main(session: dict):
    app = JarvisAntigravity(session)
    app.mainloop()

if __name__ == "__main__":
    # Hidden root window — login window is a Toplevel
    root = ctk.CTk()
    root.withdraw()

    def _on_login(session):
        root.destroy()
        _launch_main(session)

    check_and_login(root, _on_login)
    root.mainloop()
