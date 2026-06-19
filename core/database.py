import os
import sqlite3
import time

# Resolve DB path: prefer the workspace-local file, fall back to Desktop/ai/
_WORKSPACE_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'jarvis_memory.db')
_DESKTOP_DB   = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'ai', 'jarvis_memory.db')

if os.path.exists(os.path.dirname(_WORKSPACE_DB)):
    DB_PATH = _WORKSPACE_DB
else:
    DB_PATH = _WORKSPACE_DB if os.path.exists(_WORKSPACE_DB) else _DESKTOP_DB

def _ensure_sqlite_db(path: str) -> str:
    """
    Returns a usable SQLite DB path.
    If the existing file is corrupted, it tries to rename it aside and recreate.
    If the file is locked (Windows), it handles it gracefully using busy timeouts.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    def _create_schema(conn: sqlite3.Connection) -> None:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            jarvis_msg TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        conn.commit()

    try:
        conn = sqlite3.connect(path, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA quick_check").fetchall()
        _create_schema(conn)
        conn.close()
        return path
    except sqlite3.OperationalError as e:
        err_msg = str(e).lower()
        if "lock" in err_msg or "busy" in err_msg or "permission" in err_msg:
            print(f"[DB] Database is busy/locked: {e}. Re-using the main DB path.")
            return path
        # Fall back to session only if we absolutely cannot write/open the directory
        ts = time.strftime("%Y%m%d-%H%M%S")
        fallback = f"{path}.session-{ts}"
        try:
            conn = sqlite3.connect(fallback, timeout=10)
            conn.execute("PRAGMA journal_mode=WAL;")
            _create_schema(conn)
            conn.close()
            print(f"[DB] Operational error: {e}. Falling back to session: {os.path.basename(fallback)}")
            return fallback
        except Exception:
            return path
    except sqlite3.DatabaseError as e:
        ts = time.strftime("%Y%m%d-%H%M%S")
        corrupt_path = f"{path}.corrupt-{ts}"
        try:
            if os.path.exists(path):
                os.replace(path, corrupt_path)
            conn = sqlite3.connect(path, timeout=10)
            conn.execute("PRAGMA journal_mode=WAL;")
            _create_schema(conn)
            conn.close()
            print(f"[DB] Corrupt DB renamed to {os.path.basename(corrupt_path)}, fresh DB created.")
            return path
        except PermissionError:
            fallback = f"{path}.session-{ts}"
            try:
                conn = sqlite3.connect(fallback, timeout=10)
                conn.execute("PRAGMA journal_mode=WAL;")
                _create_schema(conn)
                conn.close()
                print(f"[DB] DB corrupt and locked, using session fallback: {os.path.basename(fallback)}")
                return fallback
            except Exception:
                return path

def init_db():
    global DB_PATH
    DB_PATH = _ensure_sqlite_db(DB_PATH)

def save_chat(user, jarvis):
    global DB_PATH
    DB_PATH = _ensure_sqlite_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.execute(
        "INSERT INTO chat_history (user_msg, jarvis_msg) VALUES (?, ?)",
        (user, jarvis),
    )
    conn.commit()
    conn.close()

def get_recent_history(limit=5):
    try:
        global DB_PATH
        DB_PATH = _ensure_sqlite_db(DB_PATH)
        conn = sqlite3.connect(DB_PATH, timeout=5)
        history = conn.execute(
            "SELECT user_msg, jarvis_msg FROM chat_history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        return "\n".join([f"User: {h[0]}\nJarvis: {h[1]}" for h in reversed(history)])
    except Exception:
        return ""
