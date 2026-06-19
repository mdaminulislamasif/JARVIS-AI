"""
JARVIS Auth Server
==================
A lightweight Flask-based authentication server.
Run this on any machine (local or VPS) to provide:
  - POST /register       — create account
  - POST /login          — email/password login → JWT token
  - POST /logout         — invalidate token
  - GET  /me             — get profile from token
  - POST /key/save       — save Gemini API key to account
  - GET  /key/get        — retrieve saved API keys
  - POST /password/change — change password
  - GET  /health         — server health check
  - POST /oauth/social   — social login (Google/Microsoft/Apple display name sync)

Storage: SQLite (jarvis_users.db) — zero external dependencies beyond Flask + PyJWT
"""

import os
import json
import time
import hashlib
import hmac
import secrets
import sqlite3
import threading
from functools import wraps
from typing import Optional

# ── Try to import Flask; give clear install instructions if missing ────────────
try:
    from flask import Flask, request, jsonify, g
except ImportError:
    raise SystemExit(
        "Flask not installed. Run:  pip install flask pyjwt\n"
        "Then start the server:    python server/auth_server.py"
    )

try:
    import jwt as pyjwt
    # Verify it's actually PyJWT and not the 'jwt' cli/package
    if not hasattr(pyjwt, 'encode'):
        raise ImportError("Installed 'jwt' is not PyJWT.")
except ImportError:
    raise SystemExit(
        "PyJWT not installed or wrong 'jwt' package found.\n"
        "Please run: pip uninstall jwt && pip install pyjwt\n"
    )

# ── Config ────────────────────────────────────────────────────────────────────
SERVER_PORT   = int(os.environ.get("JARVIS_AUTH_PORT", 7700))
SECRET_KEY    = os.environ.get("JARVIS_SECRET", secrets.token_hex(32))
TOKEN_EXPIRY  = 30 * 24 * 3600   # 30 days
DB_PATH       = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_users.db")

app = Flask(__name__)
_db_lock = threading.Lock()

# ── Database ──────────────────────────────────────────────────────────────────

def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    with _db_lock:
        conn = _get_db()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT    UNIQUE NOT NULL,
                display_name  TEXT    NOT NULL DEFAULT '',
                password_hash TEXT    NOT NULL DEFAULT '',
                provider      TEXT    NOT NULL DEFAULT 'email',
                created_at    REAL    NOT NULL DEFAULT ((julianday('now') - 2440587.5) * 86400.0),
                last_login    REAL    DEFAULT NULL
            );

            CREATE TABLE IF NOT EXISTS api_keys (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                api_key    TEXT    NOT NULL,
                label      TEXT    DEFAULT '',
                added_at   REAL    NOT NULL DEFAULT ((julianday('now') - 2440587.5) * 86400.0),
                UNIQUE(user_id, api_key)
            );

            CREATE TABLE IF NOT EXISTS tokens (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                token_hash TEXT    NOT NULL UNIQUE,
                expires_at REAL    NOT NULL,
                created_at REAL    NOT NULL DEFAULT ((julianday('now') - 2440587.5) * 86400.0)
            );
        """)
        conn.commit()
        conn.close()


# ── Password helpers ──────────────────────────────────────────────────────────

def _hash_pw(password: str, salt: str = "") -> str:
    if not salt:
        salt = secrets.token_hex(16)
    h = hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()
    return f"{salt}:{h}"


def _verify_pw(password: str, stored: str) -> bool:
    try:
        salt, _ = stored.split(":", 1)
        return hmac.compare_digest(_hash_pw(password, salt), stored)
    except Exception:
        return False


# ── JWT helpers ───────────────────────────────────────────────────────────────

def _make_token(user_id: int, email: str) -> str:
    payload = {
        "sub":   user_id,
        "email": email,
        "iat":   int(time.time()),
        "exp":   int(time.time()) + TOKEN_EXPIRY,
    }
    token = pyjwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # Store hash in DB for revocation support
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    with _db_lock:
        conn = _get_db()
        conn.execute(
            "INSERT OR REPLACE INTO tokens (user_id, token_hash, expires_at) VALUES (?,?,?)",
            (user_id, token_hash, payload["exp"])
        )
        # Clean up expired tokens
        conn.execute("DELETE FROM tokens WHERE expires_at < ?", (time.time(),))
        conn.commit()
        conn.close()
    return token


def _decode_token(token: str) -> Optional[dict]:
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Check revocation
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        with _db_lock:
            conn = _get_db()
            row = conn.execute(
                "SELECT id FROM tokens WHERE token_hash=? AND expires_at>?",
                (token_hash, time.time())
            ).fetchone()
            conn.close()
        if not row:
            return None
        return payload
    except Exception:
        return None


def _require_auth(f):
    """Decorator: require valid Bearer token."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"ok": False, "error": "Missing token"}), 401
        token = auth[7:]
        payload = _decode_token(token)
        if not payload:
            return jsonify({"ok": False, "error": "Invalid or expired token"}), 401
        g.user_id = payload["sub"]
        g.email   = payload["email"]
        return f(*args, **kwargs)
    return wrapper


# ── CORS helper ───────────────────────────────────────────────────────────────

@app.after_request
def _add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/<path:p>", methods=["OPTIONS"])
def _options(p):
    return "", 204


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "server": "JARVIS Auth Server", "time": time.time()})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email    = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name     = (data.get("display_name") or email.split("@")[0]).strip()

    if not email or "@" not in email:
        return jsonify({"ok": False, "error": "Invalid email"}), 400
    if len(password) < 6:
        return jsonify({"ok": False, "error": "Password must be at least 6 characters"}), 400

    with _db_lock:
        conn = _get_db()
        existing = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            conn.close()
            return jsonify({"ok": False, "error": "Email already registered"}), 409
        conn.execute(
            "INSERT INTO users (email, display_name, password_hash, provider) VALUES (?,?,?,?)",
            (email, name, _hash_pw(password), "email")
        )
        conn.commit()
        user_id = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()["id"]
        conn.close()

    token = _make_token(user_id, email)
    return jsonify({
        "ok": True,
        "token": token,
        "user": {"id": user_id, "email": email, "display_name": name, "provider": "email"},
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email    = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"ok": False, "error": "Email and password required"}), 400

    with _db_lock:
        conn = _get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if not user:
            conn.close()
            return jsonify({"ok": False, "error": "No account found for this email"}), 404
        if not _verify_pw(password, user["password_hash"]):
            conn.close()
            return jsonify({"ok": False, "error": "Incorrect password"}), 401
        # Update last_login
        conn.execute("UPDATE users SET last_login=? WHERE id=?", (time.time(), user["id"]))
        # Get saved API keys
        keys = [r["api_key"] for r in conn.execute(
            "SELECT api_key FROM api_keys WHERE user_id=? ORDER BY added_at DESC LIMIT 10",
            (user["id"],)
        ).fetchall()]
        conn.commit()
        conn.close()

    token = _make_token(user["id"], email)
    return jsonify({
        "ok": True,
        "token": token,
        "user": {
            "id":           user["id"],
            "email":        email,
            "display_name": user["display_name"],
            "provider":     user["provider"],
        },
        "api_keys": keys,
    })


@app.route("/logout", methods=["POST"])
@_require_auth
def logout_route():
    auth = request.headers.get("Authorization", "")[7:]
    token_hash = hashlib.sha256(auth.encode()).hexdigest()
    with _db_lock:
        conn = _get_db()
        conn.execute("DELETE FROM tokens WHERE token_hash=?", (token_hash,))
        conn.commit()
        conn.close()
    return jsonify({"ok": True, "message": "Logged out"})


@app.route("/me", methods=["GET"])
@_require_auth
def me():
    with _db_lock:
        conn = _get_db()
        user = conn.execute("SELECT * FROM users WHERE id=?", (g.user_id,)).fetchone()
        keys = [r["api_key"] for r in conn.execute(
            "SELECT api_key FROM api_keys WHERE user_id=? ORDER BY added_at DESC LIMIT 10",
            (g.user_id,)
        ).fetchall()]
        conn.close()
    if not user:
        return jsonify({"ok": False, "error": "User not found"}), 404
    return jsonify({
        "ok": True,
        "user": {
            "id":           user["id"],
            "email":        user["email"],
            "display_name": user["display_name"],
            "provider":     user["provider"],
            "created_at":   user["created_at"],
            "last_login":   user["last_login"],
        },
        "api_keys": keys,
    })


@app.route("/key/save", methods=["POST"])
@_require_auth
def key_save():
    data    = request.get_json(silent=True) or {}
    api_key = (data.get("api_key") or "").strip()
    label   = (data.get("label") or "").strip()

    if not api_key.startswith("AIza") or len(api_key) < 30:
        return jsonify({"ok": False, "error": "Invalid Gemini API key format"}), 400

    with _db_lock:
        conn = _get_db()
        conn.execute(
            "INSERT OR IGNORE INTO api_keys (user_id, api_key, label) VALUES (?,?,?)",
            (g.user_id, api_key, label)
        )
        conn.commit()
        conn.close()
    return jsonify({"ok": True, "message": "API key saved"})


@app.route("/key/get", methods=["GET"])
@_require_auth
def key_get():
    with _db_lock:
        conn = _get_db()
        rows = conn.execute(
            "SELECT api_key, label, added_at FROM api_keys WHERE user_id=? ORDER BY added_at DESC LIMIT 10",
            (g.user_id,)
        ).fetchall()
        conn.close()
    return jsonify({
        "ok": True,
        "keys": [{"api_key": r["api_key"], "label": r["label"], "added_at": r["added_at"]} for r in rows],
    })


@app.route("/key/delete", methods=["POST"])
@_require_auth
def key_delete():
    data    = request.get_json(silent=True) or {}
    api_key = (data.get("api_key") or "").strip()
    with _db_lock:
        conn = _get_db()
        conn.execute("DELETE FROM api_keys WHERE user_id=? AND api_key=?", (g.user_id, api_key))
        conn.commit()
        conn.close()
    return jsonify({"ok": True})


@app.route("/password/change", methods=["POST"])
@_require_auth
def password_change():
    data   = request.get_json(silent=True) or {}
    old_pw = data.get("old_password") or ""
    new_pw = data.get("new_password") or ""

    if len(new_pw) < 6:
        return jsonify({"ok": False, "error": "New password must be at least 6 characters"}), 400

    with _db_lock:
        conn = _get_db()
        user = conn.execute("SELECT * FROM users WHERE id=?", (g.user_id,)).fetchone()
        if not user:
            conn.close()
            return jsonify({"ok": False, "error": "User not found"}), 404
        if not _verify_pw(old_pw, user["password_hash"]):
            conn.close()
            return jsonify({"ok": False, "error": "Old password incorrect"}), 401
        conn.execute("UPDATE users SET password_hash=? WHERE id=?",
                     (_hash_pw(new_pw), g.user_id))
        conn.commit()
        conn.close()
    return jsonify({"ok": True, "message": "Password changed"})


@app.route("/oauth/social", methods=["POST"])
def oauth_social():
    """
    Social login endpoint.
    Client sends: {provider, email, display_name, social_token (optional)}
    Server creates account if new, returns JWT.
    """
    data     = request.get_json(silent=True) or {}
    provider = (data.get("provider") or "").lower()
    email    = (data.get("email") or "").strip().lower()
    name     = (data.get("display_name") or "").strip()

    if provider not in ("google", "microsoft", "apple"):
        return jsonify({"ok": False, "error": "Unknown provider"}), 400
    if not email:
        # Generate a placeholder email from provider
        email = f"{provider}_{secrets.token_hex(6)}@{provider}.jarvis"
    if not name:
        name = email.split("@")[0]

    with _db_lock:
        conn = _get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if not user:
            conn.execute(
                "INSERT INTO users (email, display_name, password_hash, provider) VALUES (?,?,?,?)",
                (email, name, "", provider)
            )
            conn.commit()
            user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        else:
            # Update display name if provided
            if name and name != user["display_name"]:
                conn.execute("UPDATE users SET display_name=? WHERE id=?", (name, user["id"]))
                conn.commit()
        keys = [r["api_key"] for r in conn.execute(
            "SELECT api_key FROM api_keys WHERE user_id=? ORDER BY added_at DESC LIMIT 10",
            (user["id"],)
        ).fetchall()]
        conn.execute("UPDATE users SET last_login=? WHERE id=?", (time.time(), user["id"]))
        conn.commit()
        conn.close()

    token = _make_token(user["id"], email)
    return jsonify({
        "ok": True,
        "token": token,
        "user": {
            "id":           user["id"],
            "email":        email,
            "display_name": name,
            "provider":     provider,
        },
        "api_keys": keys,
    })


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _init_db()
    print(f"""
    JARVIS AUTH SERVER - ONLINE
    Port  : {SERVER_PORT}
    DB    : {os.path.basename(DB_PATH)}
    Docs  : http://localhost:{SERVER_PORT}/health
    """)
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=False, threaded=True)
