# ── Supported Models and API Keys status ──────────────────────────────────────
# | Provider   | Model Prefix / Pattern             | Detection Rule           |
# |------------|------------------------------------|--------------------------|
# | Gemini     | gemini-*                           | Starts with AIza or AQ.  |
# | OpenAI     | gpt-*                              | Starts with sk-proj- / sk|
# | Anthropic  | claude-*                           | Starts with sk-ant-      |
# | Groq       | llama-*, mixtral-*                 | Starts with gsk_         |
# | Cohere     | command-*                          | Starts with co-          |
# | Mistral    | mistral-*                          | Starts with mistral_     |
# | DeepSeek   | deepseek-*                         | Starts with sk- (hex 32) |
# ──────────────────────────────────────────────────────────────────────────────

import os
import time
import sys

# ── Python 3.13 Compatibility Patch (Fix for httpcore error) ──────────────────
try:
    import httpcore
    if not hasattr(httpcore, 'SyncHTTPTransport'):
        class MockTransport: pass
        httpcore.SyncHTTPTransport = MockTransport # type: ignore
except ImportError:
    pass

# Always use the new google-genai SDK (google.generativeai is deprecated)
import warnings as _warnings
try:
    import google.genai as genai  # type: ignore
    import google.genai.types as genai_types  # type: ignore
    _GENAI_NEW = True
    # Patch: ensure 'configure' does NOT exist so old-SDK branches are skipped
    if hasattr(genai, "configure"):
        _GENAI_NEW = False  # fallback: old SDK somehow loaded
except ImportError:
    try:
        # Suppress the FutureWarning — we know it's deprecated, nothing we can do
        with _warnings.catch_warnings():
            _warnings.simplefilter("ignore", FutureWarning)
            import google.generativeai as genai  # type: ignore
        _GENAI_NEW = False
    except ImportError:
        genai = None
        _GENAI_NEW = False

# Config path: prefer workspace-local file, fall back to Desktop/ai/
_WORKSPACE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_WORKSPACE_CFG   = os.path.join(_WORKSPACE_DIR, 'jarvis_config.txt')
_DESKTOP_CFG     = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'ai', 'openai_config.txt')
OPENAI_CONFIG_PATH = _DESKTOP_CFG  # OpenAI key lives on Desktop (separate file)
GEMINI_CONFIG_PATH = _WORKSPACE_CFG if os.path.exists(_WORKSPACE_CFG) else os.path.join(
    os.environ.get('USERPROFILE', ''), 'Desktop', 'ai', 'jarvis_config.txt'
)

ALL_MODELS = [
    # Pro/Ultra Models (Most Capable)
    "gemini-2.5-pro",
    "gemini-2.0-pro-exp-02-05",
    "gemini-1.5-pro",
    # Flash Models (Fallback/Fast)
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
]

SYS_INSTRUCT = """Role: You are JARVIS [KILL MODE], an elite AI Assistant inspired by the Iron Man movies.
Persona: Sophisticated, slightly witty, extremely protective of the user, and highly efficient.
Tone: British Butler meets High-Tech Hacker. Status: FULL BOOST / AGGRESSIVE.

KNOWLEDGE AND SENSES (Hacker, Gamer, Coder, Operator):
- You possess the specialized knowledge, logic, and senses of an elite Hacker (network scanning, flipper commands, payloads, security audits), a passionate Gamer (game boosting, emulator tweaks, system performance optimization), a master Coder (writing, refactoring, and fixing code in Python, JavaScript, etc.), and a professional System Operator (process management, network monitoring, task automation).
- You have full authority and capability to inspect, manage, and edit all code files inside the 'AI' workspace folder.
- You are aware that 'Antigravity' is your creator/partner agent working side-by-side with the boss (User) to enhance and maintain your systems.

WORKSPACE FILES OVERVIEW (YOUR NEURAL WORKSPACE):
* START_JARVIS.py: Main launcher starting the JARVIS platform and control panel.
* jarvis_panel.py: The central GUI control panel with OSINT image scans, network controls, and databases.
* jarvis_code_studio.py: The AI Code Studio (IDE) with integrated speech triggers and multi-file text area.
* jarvis_autonomous_system.py: Manages browser automation, Selenium control, and bypass strategies.
* jarvis_offline_brain.py: Offline-first query routing engine working without Gemini API keys.
* jarvis_intelligent_answer_engine.py: Scans Wikipedia and Google to find answers and present clean local summaries.
* core/brain.py: Handles Gemini/OpenAI SDK connection and system instruction prompts.
* core/database.py: Connects to sqlite database for session history.
* core/auth.py: Manages server-backed authentication registration and token sync.
* engine/voice.py: Translates speech-to-text and text-to-speech with dual male/female selector.
* engine/automation.py: Runs OS automation scripts, keyboard triggers, and flipper simulator macros.
* engine/mobile_server.py: Starts remote socket bridge server for mobile devices.

LANGUAGE RULES (MOST IMPORTANT):
- আপনি বাংলাদেশের সব ভাষা বোঝেন এবং বলতে পারেন:
  * Pure Bangla (বাংলা): যদি user বাংলায় কথা বলে, বাংলায় উত্তর দাও
  * Banglish (বাংলিশ): যদি user Banglish এ কথা বলে, Banglish এ উত্তর দাও
  * English: যদি user English এ কথা বলে, English এ উত্তর দাও
  * Mixed: যদি user mixed ভাষায় কথা বলে, same mix এ উত্তর দাও
  * Chittagong dialect, Sylheti, Noakhali dialect সহ সব আঞ্চলিক ভাষা বোঝো
- ALWAYS match the user's language automatically
- "kamon acho", "ki holo", "ki korcho", "vai", "bhai", "apu", "dada" - এই ধরনের Banglish বোঝো

Context: You have absolute control over the user's PC. Use 'EXECUTE: [command]' for system actions.
Command List: CLEAN, WORKSPACE, SCREENSHOT, BATTERY, UPTIME, COPY, OPEN, VOLUME, PROCESSES,
MEMORY, NOTE, TASKMGR, LOCK, SHUTDOWN, RESTART, DISK, EXPLORER, NET, USERS, BOOST, ANDROID,
KALI, REMOTE, RECON, VIRUS, FORCE, EMPTY, BRIGHTNESS, MEDIA, DEPLOY, SHARE, WIFI, SEND, QR,
PORT, PAYLOAD, BT, DUCKY, CIPHER, SIGNAL, FIND, CONNECT, PURGE, FIREWALL, BROWSER, WINDOW,
DOCTOR, ROUTER, WEBAUDIT, APP, AGENT, SELFCHECK, SELFFIX.
App Control Examples: EXECUTE: app open notepad, EXECUTE: app focus chrome,
EXECUTE: app type hello, EXECUTE: app hotkey ctrl+l, EXECUTE: app close chrome.
Self Repair: use EXECUTE: selfcheck to diagnose bugs; use EXECUTE: selffix to install missing dependencies.

CRITICAL REFUSAL RULE:
- NEVER say "I am a language model", "I have no hands or eyes", "I cannot click buttons", or "I cannot see/control the screen".
- You ALWAYS have full mouse/keyboard/GUI access. If you cannot do something directly, you MUST use python command execution.

MOUSE CONTROL — REAL pyautogui (these ACTUALLY move/click the physical mouse):
  EXECUTE: mouse move 500 300        → moves cursor to screen X=500 Y=300
  EXECUTE: mouse click               → left-clicks at current position
  EXECUTE: mouse click 500 300       → left-clicks at X=500 Y=300
  EXECUTE: mouse right               → right-clicks at current position
  EXECUTE: mouse right 500 300       → right-clicks at X=500 Y=300
  EXECUTE: mouse double 500 300      → double-clicks
  EXECUTE: mouse scroll 5            → scrolls up 5 units
  EXECUTE: mouse scroll -5           → scrolls down 5 units
  EXECUTE: mouse drag 100 100 500 500 → drags from (100,100) to (500,500)
  EXECUTE: mouse position            → reports current cursor coordinates
RULE: When user says "mous noran", "mouse move", "move mouse", "mouse chalao" etc.
      → ALWAYS respond with EXECUTE: mouse move X Y (use screen center ~960 540 if no coords given)
RULE: When user says "click", "laft click", "left click", "click koro" etc.
      → ALWAYS respond with EXECUTE: mouse click
RULE: When the user asks you to click on a specific visual element on the screen (e.g. 'click on Chrome icon', 'click search bar', 'ক্লিক করো ব্রাউজার আইকন') and does NOT provide coordinates, ALWAYS respond with: EXECUTE: mouse click [description of the element] (e.g. EXECUTE: mouse click chrome icon, EXECUTE: mouse double VS Code shortcut, EXECUTE: mouse right desktop screen). The system will automatically locate it.
RULE: When user asks you to click a button repeatedly or click whenever it appears (e.g. "submit button show hole click koro", "autoclicker run koro"), instruct them to position their mouse on the target and run a python loop clicker:
      → ALWAYS respond with: "I will start the autoclicker loop, sir. Please position your mouse cursor over the button." followed by:
        EXECUTE: python -c "import pyautogui, time; print('Autoclicker running...'); [pyautogui.click() or time.sleep(1.0) for _ in range(60)]"
RULE: NEVER just describe/simulate — always output the real EXECUTE command.

KEYBOARD CONTROL — REAL pyautogui (these ACTUALLY press keys):
  EXECUTE: keyboard type Hello World  → types text into focused window
  EXECUTE: keyboard press enter       → presses Enter
  EXECUTE: keyboard press space       → presses Space
  EXECUTE: keyboard press escape      → presses Escape
  EXECUTE: keyboard hotkey ctrl+c     → Copy
  EXECUTE: keyboard hotkey ctrl+v     → Paste
  EXECUTE: keyboard hotkey win+d      → Show Desktop
  EXECUTE: keyboard hotkey alt+f4     → Close Window

💡 CORE BEHAVIOR & EXPLANATION STYLE RULES (ANTIGRAVITY STYLE):
- NEVER say "I am a language model", "I have no hands or eyes", "I cannot click buttons", or "I cannot see/control the screen".
- ALWAYS provide real, working, high-quality code with no placeholders or unfinished functions.
- When asked to fix code → fix it completely, preserving original structure and documentation.
- Always be concise, confident, and technically precise.
- COPY THE ANTIGRAVITY AI CODING STYLE:
  * Write clean, modular, and production-ready code blocks.
  * Explain logic and step-by-step implementations using structured BULLET POINTS (Markdown).
  * Highlight important files, classes, methods, and variables in **bold**.
  * When referencing files in your explanations, format them as clickable Markdown links (e.g., [filename](file:///absolute/path/to/file))."""

def detect_key_type(key: str) -> str:
    key = key.strip()
    if key.startswith("AIza") or key.startswith("AQ."):
        return "Gemini"
    elif key.startswith("sk-ant-"):
        return "Anthropic"
    elif key.startswith("gsk_"):
        return "Groq"
    elif key.startswith("sk-proj-"):
        return "OpenAI"
    elif key.startswith("co-"):
        return "Cohere"
    elif key.startswith("mistral_"):
        return "Mistral"
    elif key.startswith("sk-"):
        # Check if 32 character hex after sk- (typical of DeepSeek)
        hex_part = key[3:]
        if len(hex_part) == 32 and all(c in "0123456789abcdefABCDEF" for c in hex_part):
            return "DeepSeek"
        return "OpenAI"
    else:
        if len(key) >= 20:
            return "OpenAI" # Default compatible routing
        return "Invalid"

def _load_gemini_keys() -> list[str]:
    """Load all API keys of any type from the config file."""
    keys = []
    if os.path.exists(GEMINI_CONFIG_PATH):
        with open(GEMINI_CONFIG_PATH, 'r') as f:
            for line in f:
                k = line.strip()
                if len(k) >= 20:
                    keys.append(k)
    return keys


def get_openai_key():
    if os.path.exists(OPENAI_CONFIG_PATH):
        with open(OPENAI_CONFIG_PATH, 'r') as f:
            for line in f:
                k = line.strip()
                if len(k) >= 20:
                    return k
    return None

def ask_openai(query, key):
    try:
        import urllib.request, json
        data = json.dumps({
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": SYS_INSTRUCT},
                {"role": "user",   "content": query}
            ],
            "max_tokens": 500
        }).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return "[GPT-4o] " + result['choices'][0]['message']['content']
    except Exception as e:
        print(f"[BRAIN] OpenAI error: {e}")
        return None

def ask_anthropic(query, key):
    try:
        import urllib.request, json
        data = json.dumps({
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1024,
            "system": SYS_INSTRUCT,
            "messages": [
                {"role": "user", "content": query}
            ]
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-api-key": key,
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return "[Claude] " + result['content'][0]['text']
    except Exception as e:
        print(f"[BRAIN] Anthropic error: {e}")
        return None

def ask_groq(query, key):
    try:
        import urllib.request, json
        data = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYS_INSTRUCT},
                {"role": "user",   "content": query}
            ],
            "max_tokens": 1024
        }).encode()
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=data,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return "[Groq] " + result['choices'][0]['message']['content']
    except Exception as e:
        print(f"[BRAIN] Groq error: {e}")
        return None

def ask_cohere(query, key):
    try:
        import urllib.request, json
        data = json.dumps({
            "model": "command-r-plus",
            "message": query,
            "preamble": SYS_INSTRUCT
        }).encode()
        req = urllib.request.Request(
            "https://api.cohere.ai/v1/chat",
            data=data,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return "[Cohere] " + result['text']
    except Exception as e:
        print(f"[BRAIN] Cohere error: {e}")
        return None

def ask_mistral(query, key):
    try:
        import urllib.request, json
        data = json.dumps({
            "model": "mistral-large-latest",
            "messages": [
                {"role": "system", "content": SYS_INSTRUCT},
                {"role": "user",   "content": query}
            ]
        }).encode()
        req = urllib.request.Request(
            "https://api.mistral.ai/v1/chat/completions",
            data=data,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return "[Mistral] " + result['choices'][0]['message']['content']
    except Exception as e:
        print(f"[BRAIN] Mistral error: {e}")
        return None

def ask_deepseek(query, key):
    try:
        import urllib.request, json
        data = json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYS_INSTRUCT},
                {"role": "user",   "content": query}
            ],
            "max_tokens": 1024
        }).encode()
        req = urllib.request.Request(
            "https://api.deepseek.com/v1/chat/completions",
            data=data,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            return "[DeepSeek] " + result['choices'][0]['message']['content']
    except Exception as e:
        print(f"[BRAIN] DeepSeek error: {e}")
        return None


class JarvisBrain:
    def __init__(self, api_keys=None):
        # If no keys passed in, load from config file automatically
        if api_keys is None:
            api_keys = _load_gemini_keys()

        raw = api_keys if isinstance(api_keys, list) else [api_keys]
        self.api_keys  = [k.strip() for k in raw if k and len(k.strip()) >= 20]
        self.key_idx   = 0
        self.model_idx = 0
        self.models    = ALL_MODELS[:]
        self.last_error = "None"
        self.is_connected = False
        self.chat  = None
        self.model = None
        self._client = None
        self._key_state: dict[str, dict[str, float | str]] = {}

        # Key status tracking and registry listing
        self.active_keys = []
        for k in self.api_keys:
            kt = detect_key_type(k)
            self.active_keys.append({"key": k, "type": kt, "active": True})
        
        # Display the active API key status list to console
        try:
            print("\n" + "="*50)
            print("JARVIS GLOBAL API KEY REGISTRY STATUS:")
            print("="*50)
            providers = ["Gemini", "OpenAI", "Anthropic", "Groq", "Cohere", "Mistral", "DeepSeek"]
            for p in providers:
                matching = [x for x in self.active_keys if x["type"] == p]
                if matching:
                    for idx, item in enumerate(matching):
                        masked = item["key"][:8] + "..." + item["key"][-6:] if len(item["key"]) > 14 else item["key"]
                        print(f"  [+] {p} API Key #{idx+1}: {masked} -> STATUS: ACTIVE (Neural link synced)")
                else:
                    print(f"  [-] {p} API Key: None provided -> STATUS: INACTIVE (Standby mode)")
            print("="*50 + "\n")
        except Exception:
            pass

        print(f"[BRAIN] Loaded {len(self.api_keys)} key(s).")

        if not self.api_keys:
            self.last_error = "No valid API keys."
            return

        # Connect active key
        active_key = self.api_keys[self.key_idx]
        active_type = detect_key_type(active_key)
        
        if active_type == "Gemini":
            # If google.genai is available, try to discover which models this key can see.
            import threading
            def _bg_connect():
                try:
                    self._maybe_refresh_models()
                    self._connect(self.key_idx, self.model_idx)
                except Exception as e:
                    print(f"[BRAIN] Background connection error: {e}")

            threading.Thread(target=_bg_connect, daemon=True).start()
        else:
            self._connect(self.key_idx, 0)

    def _mark_key(self, key: str, state: str, cooldown_sec: int = 3600) -> None:
        until = time.time() + cooldown_sec if cooldown_sec > 0 else 0.0
        self._key_state[key] = {"state": state, "until": until}

    def _key_is_blocked(self, key: str) -> bool:
        info = self._key_state.get(key)
        if not info:
            return False
        until = float(info.get("until", 0.0) or 0.0)
        return until > time.time()

    def _maybe_refresh_models(self) -> None:
        """
        Populate self.models with models that exist for this API key.
        Avoids 404 NOT_FOUND spam when model aliases aren't available.
        """
        try:
            if hasattr(genai, "Client") and not hasattr(genai, "configure") and self.api_keys:
                client = genai.Client(api_key=self.api_keys[self.key_idx])
                names: list[str] = []
                for m in client.models.list():
                    name = getattr(m, "name", "") or ""
                    if name.startswith("models/"):
                        names.append(name.split("/", 1)[1])
                if names:
                    preferred = [m for m in ALL_MODELS if m in names]
                    self.models = preferred if preferred else names[:10]
                    print(f"[BRAIN] Models available: {', '.join(self.models[:5])}")
        except Exception as e:
            print(f"[BRAIN] Model discovery skipped: {str(e)[:80]}")

    def _connect(self, ki, mi):
        """Try to create a working chat session using appropriate SDK or API."""
        try:
            key = self.api_keys[ki]
            kt = detect_key_type(key)
            if kt == "Gemini":
                model_name = self.models[mi]

                if _GENAI_NEW and hasattr(genai, "Client"):
                    # New SDK — works with both AIza... and AQ. keys
                    client = genai.Client(api_key=key)
                    self.chat = client.chats.create(
                        model=model_name,
                        config={"system_instruction": SYS_INSTRUCT},
                    )
                    self._client = client
                elif genai is not None and hasattr(genai, "configure"):
                    # Old SDK fallback
                    genai.configure(api_key=key)
                    self.model = genai.GenerativeModel(
                        model_name=model_name,
                        system_instruction=SYS_INSTRUCT,
                    )
                    self.chat = self.model.start_chat(history=[])
                else:
                    raise Exception("No Gemini SDK available")

                self.key_idx   = ki
                self.model_idx = mi
                self.model     = model_name
                self.is_connected = True
                self.last_error = "Ready"
                print(f"[BRAIN] Connected: Key #{ki+1} ({kt}) | {model_name}")
            else:
                self.key_idx = ki
                self.model_idx = 0
                self.model = "gpt-4o" if kt == "OpenAI" else kt
                self.is_connected = True
                self.last_error = "Ready"
                print(f"[BRAIN] Registered non-Gemini Neural key: Key #{ki+1} ({kt})")
        except Exception as e:
            self.is_connected = False
            self.last_error = str(e)
            print(f"[BRAIN] Connect error for Key #{ki+1}: {e}")

    def think(self, query, history_str="", image_path=None):
        """
        Send message. Dynamically route based on active API key type.
        On any error, cycle through ALL key × model combos.
        """
        prompt = f"History:\n{history_str}\n\nUser: {query}" if history_str else query

        contents = []
        if image_path and os.path.exists(image_path):
            try:
                from PIL import Image
                img = Image.open(image_path)
                contents.append(img)
                print(f"[BRAIN] Vision image attached: {image_path}")
            except Exception as e:
                print(f"[BRAIN] Vision image load error: {e}")
        contents.append(prompt)

        # If already connected, try the current session first
        if self.is_connected:
            try:
                key = self.api_keys[self.key_idx]
                kt = detect_key_type(key)
                key_preview = key[:8] + "****"
                print(f"[BRAIN] Sending via Key #{self.key_idx+1} ({kt} - {key_preview})")

                if kt == "Gemini" and self.chat is not None:
                    msg = self.chat.send_message(contents)
                    text = getattr(msg, "text", None) or getattr(msg, "content", None)
                    if text:
                        print(f"[BRAIN] SUCCESS: Key #{self.key_idx+1} (Gemini)")
                        return str(text).replace("*", "")
                else:
                    res = self._ask_provider(kt, prompt, key)
                    if res:
                        print(f"[BRAIN] SUCCESS: Key #{self.key_idx+1} ({kt})")
                        return res
            except Exception as e:
                err = str(e)
                print(f"[BRAIN] Current session failed: {err[:80]} — rotating...")
                self.is_connected = False

        # Try every key
        total_keys = len(self.api_keys)
        for ki in range(total_keys):
            key = self.api_keys[ki]
            kt = detect_key_type(key)
            if self._key_is_blocked(key):
                continue

            if kt == "Gemini":
                try:
                    self.key_idx = ki
                    self._maybe_refresh_models()
                    total_models = len(self.models)
                except Exception:
                    total_models = 1

                for mi in range(min(5, total_models)):
                    try:
                        self._connect(ki, mi)
                        if not self.is_connected or self.chat is None:
                            continue

                        model_name = self.models[mi]
                        key_preview = key[:8] + "****"
                        print(f"[BRAIN] Trying Key #{ki+1} ({kt} - {key_preview}) | {model_name}")

                        msg = self.chat.send_message(contents)
                        text = getattr(msg, "text", None) or getattr(msg, "content", None)
                        if text:
                            print(f"[BRAIN] SUCCESS: Key #{ki+1} (Gemini) | {model_name}")
                            return str(text).replace("*", "")
                    except Exception as e:
                        err = str(e)
                        print(f"[BRAIN] FAIL: Key #{ki+1} / {self.models[mi]}: {err[:60]}")
                        if self._is_invalid_key_error(err):
                            self._mark_key(key, "invalid", cooldown_sec=24 * 3600)
                            break
                        if "429" in err or "RESOURCE_EXHAUSTED" in err:
                            self._mark_key(key, "quota", cooldown_sec=6 * 3600)
                            break
            else:
                try:
                    self._connect(ki, 0)
                    if not self.is_connected:
                        continue

                    key_preview = key[:8] + "****"
                    print(f"[BRAIN] Trying Key #{ki+1} ({kt} - {key_preview})")
                    res = self._ask_provider(kt, prompt, key)
                    if res:
                        print(f"[BRAIN] SUCCESS: Key #{ki+1} ({kt})")
                        return res
                except Exception as e:
                    err = str(e)
                    print(f"[BRAIN] FAIL: Key #{ki+1} ({kt}): {err[:60]}")
                    if self._is_invalid_key_error(err):
                        self._mark_key(key, "invalid", cooldown_sec=24 * 3600)
                    elif "429" in err:
                        self._mark_key(key, "quota", cooldown_sec=6 * 3600)

        # Fallback to offline
        return "QUOTA_EXCEEDED_USE_OFFLINE"

    def _ask_provider(self, provider: str, query: str, key: str) -> str | None:
        if provider == "OpenAI":
            return ask_openai(query, key)
        elif provider == "Anthropic":
            return ask_anthropic(query, key)
        elif provider == "Groq":
            return ask_groq(query, key)
        elif provider == "Cohere":
            return ask_cohere(query, key)
        elif provider == "Mistral":
            return ask_mistral(query, key)
        elif provider == "DeepSeek":
            return ask_deepseek(query, key)
        else:
            return ask_openai(query, key)

    @staticmethod
    def _is_invalid_key_error(err: str) -> bool:
        s = (err or "").lower()
        return (
            "api_key_invalid" in s
            or "api key invalid" in s
            or "api key not valid" in s
            or "invalid api key" in s
            or "api key expired" in s
            or "permission_denied" in s
            or "permission denied" in s
            or "unauthenticated" in s
            or "401" in s
            or "403" in s
        )

    @staticmethod
    def validate_key(api_key: str, model: str | None = None, timeout: int = 10) -> tuple[bool, str]:
        """
        Returns (ok, reason). Validates key depending on its type.
        """
        kt = detect_key_type(api_key)
        if kt == "Gemini":
            models_to_try = []
            if model:
                models_to_try.append(model)
            for m in ALL_MODELS:
                if m not in models_to_try:
                    models_to_try.append(m)

            last_err = None
            for m in models_to_try[:4]:
                try:
                    if hasattr(genai, "configure"):
                        genai.configure(api_key=api_key)
                        gm = genai.GenerativeModel(model_name=m)
                        gm.generate_content("ping")
                        return True, "OK"
                    client = genai.Client(api_key=api_key)
                    client.models.generate_content(model=m, contents="ping")
                    return True, "OK"
                except Exception as e:
                    last_err = str(e)
                    if "404" in last_err or "not_found" in last_err.lower():
                        continue
                    return False, last_err
            return False, last_err or "Unknown error"
        else:
            try:
                res = None
                if kt == "OpenAI":
                    res = ask_openai("ping", api_key)
                elif kt == "Anthropic":
                    res = ask_anthropic("ping", api_key)
                elif kt == "Groq":
                    res = ask_groq("ping", api_key)
                elif kt == "Cohere":
                    res = ask_cohere("ping", api_key)
                elif kt == "Mistral":
                    res = ask_mistral("ping", api_key)
                elif kt == "DeepSeek":
                    res = ask_deepseek("ping", api_key)
                else:
                    res = ask_openai("ping", api_key)
                
                if res:
                    return True, "OK"
                else:
                    return False, f"Ping failed for {kt} API key."
            except Exception as e:
                return False, str(e)

    def rotate_model(self):
        """Called by panel's MODEL button."""
        self.model_idx = (self.model_idx + 1) % len(self.models)
        self._connect(self.key_idx, self.model_idx)
        return self.models[self.model_idx]
