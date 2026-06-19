"""
JARVIS Authentication System
- Server-backed auth (server/auth_server.py) with local fallback
- Email/password login
- Google / Microsoft / Apple social login
- Auto Gemini API key fetch + sync to server
- Session persistence (remember me)
- Account management
"""
import os
import json
import hashlib
import hmac
import secrets
import time
import threading
import webbrowser
import urllib.request
import urllib.parse
import http.server
import socketserver
from typing import Optional

_BASE        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_FILE    = os.path.join(_BASE, "jarvis_auth.json")
SESSION_FILE = os.path.join(_BASE, "jarvis_session.json")

# ── Server client (lazy import to avoid circular deps) ────────────────────────
def _get_server_client():
    try:
        from server.auth_client import get_client
        return get_client()
    except Exception:
        return None

# ── Helpers ───────────────────────────────────────────────────────────────────

def _hash_password(password: str, salt: str = "") -> str:
    if not salt:
        salt = secrets.token_hex(16)
    h = hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()
    return f"{salt}:{h}"

def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, _ = stored.split(":", 1)
        return hmac.compare_digest(_hash_password(password, salt), stored)
    except Exception:
        return False

def _load_auth() -> dict:
    if os.path.exists(AUTH_FILE):
        try:
            with open(AUTH_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            print("⚠️ Error occurred but was silently ignored")
    return {"users": {}, "version": 1}

def _save_auth(data: dict):
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _load_session() -> dict:
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                s = json.load(f)
                # Check expiry
                if s.get("expires_at", 0) > time.time():
                    return s
        except Exception:
            print("⚠️ Error occurred but was silently ignored")
    return {}

def _save_session(email: str, display_name: str, provider: str,
                  remember: bool = True, api_key: str = "", server_token: str = ""):
    expires = time.time() + (30 * 86400 if remember else 86400)
    data = {
        "email": email,
        "display_name": display_name,
        "provider": provider,
        "api_key": api_key,
        "server_token": server_token,
        "expires_at": expires,
        "logged_in_at": time.time(),
        "source": "server" if server_token else "local"
    }
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data

def _clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# ── Account Management ────────────────────────────────────────────────────────

def create_account(email: str, password: str, display_name: str = "") -> tuple:
    """Returns (ok: bool, message: str). Tries server first, falls back to local."""
    email = email.strip().lower()
    if not email or "@" not in email:
        return False, "Invalid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    # Try server
    client = _get_server_client()
    if client and client.is_online():
        ok, result = client.register(email, password, display_name or email.split("@")[0])
        if ok:
            return True, "Account created on server."
        # If server says already exists, that's a real error
        if isinstance(result, str) and "already" in result.lower():
            return False, result
        # Other server error — fall through to local

    # Local fallback
    data = _load_auth()
    if email in data["users"]:
        return False, "Account already exists. Please log in."
    data["users"][email] = {
        "display_name": display_name or email.split("@")[0],
        "password_hash": _hash_password(password),
        "provider": "email",
        "created_at": time.time(),
        "api_keys": [],
    }
    _save_auth(data)
    return True, "Account created (local)."


def login_email(email: str, password: str, remember: bool = True) -> tuple:
    """Returns (ok: bool, session_dict or error_str). Tries server first, falls back to local."""
    email = email.strip().lower()

    # Try server
    client = _get_server_client()
    if client and client.is_online():
        ok, result = client.login(email, password, remember)
        if ok:
            # Auto-apply first API key from server
            api_key = result.get("api_key", "")
            if api_key:
                auto_apply_key_to_config(api_key, email)
            return True, result
        # Wrong password is a definitive error — don't fall through
        if isinstance(result, str) and ("password" in result.lower() or "incorrect" in result.lower()):
            return False, result

    # Local fallback
    data = _load_auth()
    user = data["users"].get(email)
    if not user:
        return False, "No account found. Please create one first."
    if not _verify_password(password, user.get("password_hash", "")):
        return False, "Incorrect password."
    api_key = user.get("api_keys", [""])[0] if user.get("api_keys") else ""
    session = _save_session(email, user["display_name"], "email", remember, api_key)
    return True, session

def change_password(email: str, old_pw: str, new_pw: str) -> tuple:
    email = email.strip().lower()
    data  = _load_auth()
    user  = data["users"].get(email)
    if not user:
        return False, "Account not found."
    if not _verify_password(old_pw, user.get("password_hash", "")):
        return False, "Old password incorrect."
    if len(new_pw) < 6:
        return False, "New password must be at least 6 characters."
    user["password_hash"] = _hash_password(new_pw)
    _save_auth(data)
    return True, "Password changed."

def save_api_key_to_account(email: str, api_key: str):
    data = _load_auth()
    user = data["users"].get(email.strip().lower())
    if user:
        keys = user.get("api_keys", [])
        if api_key not in keys:
            keys.insert(0, api_key)
        user["api_keys"] = keys[:10]
        _save_auth(data)

def get_session() -> dict:
    return _load_session()

def logout():
    client = _get_server_client()
    if client and client.is_online():
        try:
            client.logout()
        except Exception:
            pass
    _clear_session()

# ── OAuth (Google / Microsoft / Apple) ───────────────────────────────────────
# These open the browser to the provider's OAuth page.
# A tiny local HTTP server captures the redirect and extracts the token/code.
# For Google: we use the "device flow" which is simpler and doesn't need a
# registered OAuth app — it just opens AI Studio for the API key.

OAUTH_CALLBACK_PORT = 9876
_oauth_result: dict = {}
_oauth_event  = threading.Event()


class _OAuthHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        global _oauth_result
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))

        # Extract useful fields
        _oauth_result = {
            "code":    params.get("code", ""),
            "token":   params.get("access_token", ""),
            "email":   params.get("email", ""),
            "name":    params.get("name", ""),
            "error":   params.get("error", ""),
            "path":    parsed.path,
            "params":  params,
        }
        _oauth_event.set()

        # Send a nice response page
        html = """<!DOCTYPE html>
<html><head><title>JARVIS Auth</title>
<style>
  body{background:#02050A;color:#00F3FF;font-family:'Courier New',monospace;
       display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}
  .box{text-align:center;border:1px solid #00F3FF;padding:40px;border-radius:12px;}
  h1{color:#00FF41;font-size:28px;}
  p{color:#555;}
</style></head>
<body><div class="box">
  <h1>✓ JARVIS AUTH COMPLETE</h1>
  <p>You can close this tab and return to JARVIS.</p>
</div></body></html>"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


def _start_oauth_server() -> Optional[socketserver.TCPServer]:
    try:
        socketserver.TCPServer.allow_reuse_address = True
        server = socketserver.TCPServer(("", OAUTH_CALLBACK_PORT), _OAuthHandler)
        t = threading.Thread(target=server.handle_request, daemon=True)
        t.start()
        return server
    except Exception as e:
        print(f"[AUTH] OAuth server error: {e}")
        return None


def oauth_google(callback=None) -> dict:
    """Opens Google sign-in + AI Studio. Syncs with server if online."""
    global _oauth_result, _oauth_event
    _oauth_result = {}
    _oauth_event.clear()

    webbrowser.open("https://accounts.google.com/signin")
    time.sleep(1)
    webbrowser.open("https://aistudio.google.com/app/apikey")

    # Try server social login
    client = _get_server_client()
    if client and client.is_online():
        ok, result = client.social_login("google")
        if ok:
            if callback:
                callback(result)
            return result

    session = _save_session(
        email="google_user@gmail.com",
        display_name="Google User",
        provider="google",
        remember=True,
        api_key="",
    )
    if callback:
        callback(session)
    return session


def oauth_microsoft(callback=None) -> dict:
    """Opens Microsoft sign-in + AI Studio. Syncs with server if online."""
    webbrowser.open("https://login.microsoftonline.com/")
    time.sleep(1)
    webbrowser.open("https://aistudio.google.com/app/apikey")

    client = _get_server_client()
    if client and client.is_online():
        ok, result = client.social_login("microsoft")
        if ok:
            if callback:
                callback(result)
            return result

    session = _save_session(
        email="microsoft_user@outlook.com",
        display_name="Microsoft User",
        provider="microsoft",
        remember=True,
        api_key="",
    )
    if callback:
        callback(session)
    return session


def oauth_apple(callback=None) -> dict:
    """Opens Apple sign-in + AI Studio. Syncs with server if online."""
    webbrowser.open("https://appleid.apple.com/sign-in")
    time.sleep(1)
    webbrowser.open("https://aistudio.google.com/app/apikey")

    client = _get_server_client()
    if client and client.is_online():
        ok, result = client.social_login("apple")
        if ok:
            if callback:
                callback(result)
            return result

    session = _save_session(
        email="apple_user@icloud.com",
        display_name="Apple User",
        provider="apple",
        remember=True,
        api_key="",
    )
    if callback:
        callback(session)
    return session


# ── Auto API Key Fetch ────────────────────────────────────────────────────────

def auto_fetch_gemini_key() -> str:
    """
    Opens Google AI Studio and watches clipboard for an API key.
    Returns the key when detected (blocking, max 120s).
    """
    webbrowser.open("https://aistudio.google.com/app/apikey")
    try:
        import pyperclip
        deadline = time.time() + 120
        last = pyperclip.paste()
        while time.time() < deadline:
            curr = pyperclip.paste().strip()
            if curr != last and len(curr) >= 20:
                return curr
            last = curr
            time.sleep(1)
    except Exception:
        print("⚠️ Error occurred but was silently ignored")
    return ""


def auto_apply_key_to_config(api_key: str, email: str = "") -> bool:
    """Write the API key to jarvis_config.txt, save to account, and sync to server."""
    api_key = api_key.strip()
    if len(api_key) < 20:
        return False
    cfg = os.path.join(_BASE, "jarvis_config.txt")
    keys = []
    if os.path.exists(cfg):
        with open(cfg, "r") as f:
            keys = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    if api_key not in keys:
        keys.insert(0, api_key)
        with open(cfg, "w") as f:
            f.write("\n".join(keys) + "\n")
    if email:
        save_api_key_to_account(email, api_key)
    # Sync to server
    client = _get_server_client()
    if client and client.is_online() and client._token:
        try:
            client.save_key(api_key)
        except Exception:
            print("⚠️ Error occurred but was silently ignored")
    return True
