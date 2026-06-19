"""
JARVIS Auth Client
==================
Talks to the JARVIS Auth Server (server/auth_server.py).
Falls back to local auth (core/auth.py) if server is unreachable.

Usage:
    from server.auth_client import AuthClient
    client = AuthClient("http://localhost:7700")
    ok, result = client.login("user@example.com", "password")
"""
import os
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional

_BASE        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SERVER_CFG  = os.path.join(_BASE, "jarvis_server.json")
SESSION_FILE = os.path.join(_BASE, "jarvis_session.json")

DEFAULT_SERVER = "http://localhost:7700"


def _load_server_url() -> str:
    if os.path.exists(_SERVER_CFG):
        try:
            with open(_SERVER_CFG) as f:
                return json.load(f).get("url", DEFAULT_SERVER).rstrip("/")
        except Exception:
            print("⚠️ Error occurred but was silently ignored")
    return DEFAULT_SERVER


def _save_server_url(url: str):
    with open(_SERVER_CFG, "w") as f:
        json.dump({"url": url.rstrip("/")}, f)


def _load_token() -> str:
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE) as f:
                s = json.load(f)
                if s.get("expires_at", 0) > time.time():
                    return s.get("server_token", "")
        except Exception:
            print("⚠️ Error occurred but was silently ignored")
    return ""


def _save_session(data: dict, token: str, remember: bool = True):
    expires = time.time() + (30 * 86400 if remember else 86400)
    session = {
        "email":        data.get("email", ""),
        "display_name": data.get("display_name", ""),
        "provider":     data.get("provider", "email"),
        "api_key":      (data.get("api_keys") or [""])[0],
        "api_keys":     data.get("api_keys", []),
        "server_token": token,
        "expires_at":   expires,
        "logged_in_at": time.time(),
        "source":       "server",
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f, indent=2)
    return session


class AuthClient:
    """
    HTTP client for the JARVIS Auth Server.
    All methods return (ok: bool, data: dict | str).
    """

    def __init__(self, server_url: str = None):
        self.server_url = (server_url or _load_server_url()).rstrip("/")
        self._token     = _load_token()
        self.online     = False
        self._check_health()

    # ── Internal HTTP ─────────────────────────────────────────────────────────

    def _request(self, method: str, path: str, body: dict = None,
                 auth: bool = False, timeout: int = 8) -> tuple:
        url = f"{self.server_url}{path}"
        headers = {"Content-Type": "application/json"}
        if auth and self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        data = json.dumps(body).encode() if body else None
        req  = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                result = json.loads(r.read())
                self.online = True
                return True, result
        except urllib.error.HTTPError as e:
            try:
                result = json.loads(e.read())
                return False, result.get("error", str(e))
            except Exception:
                return False, f"HTTP {e.code}: {e.reason}"
        except Exception as e:
            self.online = False
            return False, f"Server unreachable: {e}"

    # ── Health ────────────────────────────────────────────────────────────────

    def _check_health(self):
        ok, _ = self._request("GET", "/health", timeout=3)
        self.online = ok

    def is_online(self) -> bool:
        self._check_health()
        return self.online

    # ── Auth ──────────────────────────────────────────────────────────────────

    def register(self, email: str, password: str, display_name: str = "",
                 remember: bool = True) -> tuple:
        ok, result = self._request("POST", "/register", {
            "email": email, "password": password, "display_name": display_name
        })
        if ok and result.get("ok"):
            self._token = result["token"]
            session = _save_session(result["user"], self._token, remember)
            return True, session
        return False, result if isinstance(result, str) else result.get("error", "Registration failed")

    def login(self, email: str, password: str, remember: bool = True) -> tuple:
        ok, result = self._request("POST", "/login", {
            "email": email, "password": password
        })
        if ok and result.get("ok"):
            self._token = result["token"]
            user_data   = result["user"]
            user_data["api_keys"] = result.get("api_keys", [])
            session = _save_session(user_data, self._token, remember)
            return True, session
        return False, result if isinstance(result, str) else result.get("error", "Login failed")

    def logout(self) -> tuple:
        ok, result = self._request("POST", "/logout", auth=True)
        self._token = ""
        # Clear local session
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        return ok, result

    def get_profile(self) -> tuple:
        ok, result = self._request("GET", "/me", auth=True)
        if ok and result.get("ok"):
            return True, result
        return False, result if isinstance(result, str) else result.get("error", "Failed")

    def social_login(self, provider: str, email: str = "", display_name: str = "",
                     remember: bool = True) -> tuple:
        ok, result = self._request("POST", "/oauth/social", {
            "provider": provider, "email": email, "display_name": display_name
        })
        if ok and result.get("ok"):
            self._token = result["token"]
            user_data   = result["user"]
            user_data["api_keys"] = result.get("api_keys", [])
            session = _save_session(user_data, self._token, remember)
            return True, session
        return False, result if isinstance(result, str) else result.get("error", "Social login failed")

    # ── API Keys ──────────────────────────────────────────────────────────────

    def save_key(self, api_key: str, label: str = "") -> tuple:
        ok, result = self._request("POST", "/key/save",
                                   {"api_key": api_key, "label": label}, auth=True)
        return ok, result

    def get_keys(self) -> list:
        ok, result = self._request("GET", "/key/get", auth=True)
        if ok and result.get("ok"):
            return [k["api_key"] for k in result.get("keys", [])]
        return []

    def delete_key(self, api_key: str) -> tuple:
        return self._request("POST", "/key/delete", {"api_key": api_key}, auth=True)

    # ── Password ──────────────────────────────────────────────────────────────

    def change_password(self, old_pw: str, new_pw: str) -> tuple:
        ok, result = self._request("POST", "/password/change",
                                   {"old_password": old_pw, "new_password": new_pw}, auth=True)
        return ok, result

    # ── Server config ─────────────────────────────────────────────────────────

    def set_server_url(self, url: str):
        self.server_url = url.rstrip("/")
        _save_server_url(url)
        self._check_health()

    def get_server_url(self) -> str:
        return self.server_url


# ── Singleton ─────────────────────────────────────────────────────────────────
_client: Optional[AuthClient] = None

def get_client() -> AuthClient:
    global _client
    if _client is None:
        _client = AuthClient()
    return _client
