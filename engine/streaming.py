"""
JARVIS Streaming Engine
- Streaming AI responses (token-by-token output to UI)
- Auto-control: scheduled tasks, event triggers, watchdog
- Online/Offline bug detection
"""
import os
import sys
import time
import threading
import subprocess
import importlib
import urllib.request
import socket
from typing import Callable, Optional

# ── STREAMING BRAIN RESPONSE ─────────────────────────────────────────────────
def stream_think(brain, query: str, history_str: str = "", callback: Callable[[str], None] = None, image_path: str = None) -> str:
    """
    Stream AI response token by token.
    On 503/overload, falls back to non-streaming brain.think().
    callback(chunk) is called for each new chunk of text.
    Returns the full response string.
    """
    if not brain or not brain.is_connected:
        msg = "[STREAM] Brain offline."
        if callback:
            callback(msg)
        return msg

    full_response = []
    prompt = f"History:\n{history_str}\n\nUser: {query}" if history_str else query

    contents = []
    if image_path and os.path.exists(image_path):
        try:
            from PIL import Image
            img = Image.open(image_path)
            contents.append(img)
            print(f"[STREAM] Loaded image for streaming vision: {image_path}")
        except Exception as e:
            print(f"[STREAM] Image load error: {e}")
    contents.append(prompt)

    try:
        import google.genai as genai_new
        USE_NEW = hasattr(genai_new, "Client")
    except ImportError:
        USE_NEW = False

    try:
        if USE_NEW:
            import google.genai as genai
            client = genai.Client(api_key=brain.api_keys[brain.key_idx])
            model_name = brain.models[brain.model_idx]
            for chunk in client.models.generate_content_stream(
                model=model_name,
                contents=contents,
            ):
                text = getattr(chunk, "text", "") or ""
                if text:
                    full_response.append(text)
                    if callback:
                        callback(text)
        else:
            import google.generativeai as genai
            genai.configure(api_key=brain.api_keys[brain.key_idx])
            model = genai.GenerativeModel(model_name=brain.models[brain.model_idx])
            for chunk in model.generate_content(contents, stream=True):
                text = getattr(chunk, "text", "") or ""
                if text:
                    full_response.append(text)
                    if callback:
                        callback(text)

    except Exception as e:
        err_str = str(e)
        # 503 / overload — fallback to non-streaming brain.think()
        if any(x in err_str for x in ["503", "UNAVAILABLE", "overloaded", "high demand", "429", "RESOURCE_EXHAUSTED"]):
            if callback:
                callback("\n[Switching to fallback mode...]\n")
            try:
                fallback = brain.think(query, history_str, image_path=image_path)
                if fallback and "[STREAM" not in fallback:
                    if callback:
                        callback(fallback)
                    return fallback
            except Exception as e2:
                pass
            # Try next key/model
            try:
                old_idx = brain.key_idx
                brain.key_idx = (brain.key_idx + 1) % max(1, len(brain.api_keys))
                fallback2 = brain.think(query, history_str, image_path=image_path)
                brain.key_idx = old_idx
                if fallback2:
                    if callback:
                        callback(fallback2)
                    return fallback2
            except Exception:
                pass
        else:
            err = f"\n[STREAM ERROR] {e}"
            full_response.append(err)
            if callback:
                callback(err)

    return "".join(full_response)


# ── ONLINE / OFFLINE BUG DETECTOR ────────────────────────────────────────────
REQUIRED_PACKAGES = [
    "customtkinter", "PIL", "pyttsx3", "speech_recognition",
    "psutil", "pyautogui", "pyperclip",
]

OPTIONAL_PACKAGES = {
    "edge_tts":   "edge-tts",
    "panda3d":    "panda3d",
    "requests":   "requests",
    "gtts":       "gtts",
}

ONLINE_HOSTS = [
    ("8.8.8.8", 53),
    ("1.1.1.1", 53),
    ("generativelanguage.googleapis.com", 443),
]


def check_internet() -> "tuple[bool, str]":
    """Check if internet is reachable."""
    for host, port in ONLINE_HOSTS:
        try:
            s = socket.create_connection((host, port), timeout=3)
            s.close()
            return True, f"Online via {host}"
        except OSError:
            continue
    return False, "All internet checks failed"


def detect_bugs(auto_fix: bool = False) -> str:
    """
    Scan for missing packages, broken imports, and connectivity issues.
    If auto_fix=True, attempts pip install for missing packages.
    """
    report = ["═══ JARVIS BUG DETECTION REPORT ═══", ""]

    # 1. Internet check
    online, net_msg = check_internet()
    report.append(f"[NET] {'✓ ONLINE' if online else '✗ OFFLINE'}: {net_msg}")

    # 2. Required packages
    report.append("\n[REQUIRED PACKAGES]")
    missing_required = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
            report.append(f"  ✓ {pkg}")
        except ImportError:
            report.append(f"  ✗ {pkg} — MISSING")
            missing_required.append(pkg)

    # 3. Optional packages
    report.append("\n[OPTIONAL PACKAGES]")
    missing_optional = []
    for mod, pip_name in OPTIONAL_PACKAGES.items():
        try:
            importlib.import_module(mod)
            report.append(f"  ✓ {mod}")
        except ImportError:
            report.append(f"  ~ {mod} ({pip_name}) — not installed")
            missing_optional.append(pip_name)

    # 4. Config files
    report.append("\n[CONFIG FILES]")
    _base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    checks = {
        "jarvis_config.txt": os.path.join(_base, "jarvis_config.txt"),
        "jarvis_memory.db":  os.path.join(_base, "jarvis_memory.db"),
        "jarvis_face.glb":   os.path.join(_base, "jarvis_face.glb"),
        "jarvis_face.png":   os.path.join(_base, "jarvis_face.png"),
    }
    for name, path in checks.items():
        exists = os.path.exists(path)
        report.append(f"  {'✓' if exists else '✗'} {name}")

    # 5. DB integrity
    report.append("\n[DATABASE]")
    try:
        import sqlite3
        db_path = os.path.join(_base, "jarvis_memory.db")
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path, timeout=3)
            conn.execute("PRAGMA quick_check").fetchall()
            conn.close()
            report.append("  ✓ jarvis_memory.db — healthy")
        else:
            report.append("  ~ jarvis_memory.db — will be created on first use")
    except Exception as e:
        report.append(f"  ✗ jarvis_memory.db — CORRUPT: {e}")

    # 6. Auto-fix
    if auto_fix and missing_required:
        report.append("\n[AUTO-FIX] Installing missing required packages...")
        for pkg in missing_required:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                    check=True, capture_output=True
                )
                report.append(f"  ✓ Installed: {pkg}")
            except Exception as e:
                report.append(f"  ✗ Failed: {pkg} — {e}")

    report.append("\n═══ END OF REPORT ═══")
    return "\n".join(report)


# ── AUTO CONTROL / SCHEDULER ─────────────────────────────────────────────────
class AutoController:
    """
    Lightweight task scheduler for JARVIS.
    Supports: interval tasks, one-shot delayed tasks, watchdog.
    """
    def __init__(self):
        self._tasks: list[dict] = []
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def add_interval(self, name: str, func: Callable, interval_sec: float):
        """Run func every interval_sec seconds."""
        with self._lock:
            self._tasks.append({
                "name": name, "func": func,
                "type": "interval", "interval": interval_sec,
                "next_run": time.time() + interval_sec,
            })

    def add_once(self, name: str, func: Callable, delay_sec: float):
        """Run func once after delay_sec seconds."""
        with self._lock:
            self._tasks.append({
                "name": name, "func": func,
                "type": "once", "interval": 0,
                "next_run": time.time() + delay_sec,
            })

    def remove(self, name: str):
        with self._lock:
            self._tasks = [t for t in self._tasks if t["name"] != name]

    def list_tasks(self) -> str:
        with self._lock:
            if not self._tasks:
                return "No scheduled tasks."
            lines = ["--- AUTO CONTROLLER TASKS ---"]
            for t in self._tasks:
                eta = max(0, t["next_run"] - time.time())
                lines.append(f"  [{t['type'].upper()}] {t['name']} — next in {eta:.0f}s")
            return "\n".join(lines)

    def _loop(self):
        while self._running:
            now = time.time()
            with self._lock:
                tasks_copy = list(self._tasks)
            to_remove = []
            for task in tasks_copy:
                if now >= task["next_run"]:
                    try:
                        task["func"]()
                    except Exception as e:
                        print(f"[AUTO] Task '{task['name']}' error: {e}")
                    if task["type"] == "once":
                        to_remove.append(task["name"])
                    else:
                        task["next_run"] = now + task["interval"]
            if to_remove:
                with self._lock:
                    self._tasks = [t for t in self._tasks if t["name"] not in to_remove]
            time.sleep(0.5)


# ── SUPER HOST (local HTTP host for sharing files/pages) ─────────────────────
_super_host_thread: Optional[threading.Thread] = None
_super_host_port = 8080


def start_super_host(directory: str = None, port: int = 8080) -> str:
    """
    Start a local HTTP file server to share files over LAN.
    """
    global _super_host_thread, _super_host_port
    if directory is None:
        directory = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    if not os.path.isdir(directory):
        return f"[SUPER HOST] Directory not found: {directory}"

    _super_host_port = port

    def _serve():
        import http.server
        import socketserver
        os.chdir(directory)
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"[SUPER HOST] Serving {directory} on port {port}")
            httpd.serve_forever()

    _super_host_thread = threading.Thread(target=_serve, daemon=True)
    _super_host_thread.start()

    # Get local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 1))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "127.0.0.1"

    url = f"http://{ip}:{port}"
    return (
        f"[SUPER HOST ONLINE]\n"
        f"Directory: {directory}\n"
        f"URL: {url}\n"
        f"Share this URL with anyone on your network to browse files."
    )
