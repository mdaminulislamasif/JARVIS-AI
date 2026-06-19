"""
JARVIS Auth Server Launcher
Run this file to start the auth server:
    python server/start_server.py

Or with a custom port:
    set JARVIS_AUTH_PORT=8800 && python server/start_server.py

Auto-installs Flask and PyJWT if missing.
"""
import subprocess
import sys
import os

def _ensure_deps():
    missing = []
    for pkg, imp in [("flask", "flask"), ("pyjwt", "jwt")]:
        try:
            __import__(imp)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"[SETUP] Missing dependencies: {', '.join(missing)}")
        try:
            print(f"[SETUP] Attempting auto-install...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install"] + missing + ["--quiet"],
                check=True
            )
            print("[SETUP] Success. Starting JARVIS server...")
        except Exception as e:
            print(f"[!] SETUP FAILED: {e}")
            print(f"[!] Please run manually: pip install {' '.join(missing)}")
            sys.exit(1)

if __name__ == "__main__":
    _ensure_deps()
    # Add project root to path and normalize for Windows
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)
    
    try:
        from server.auth_server import app, _init_db, SERVER_PORT, DB_PATH
        _init_db()
        print(f"""
    JARVIS AUTH SERVER - ONLINE
    ---------------------------
    Port  : {SERVER_PORT}
    DB    : {os.path.abspath(DB_PATH)}
    URL   : http://localhost:{SERVER_PORT}
    
    Status: Listening for neural requests...
    Press Ctrl+C to stop.
    """)
        app.run(host="0.0.0.0", port=SERVER_PORT, debug=False, threaded=True)
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:
            print(f"[!] PORT {SERVER_PORT} IS ALREADY IN USE.")
            print(f"[!] Please close the other JARVIS instance or change port in auth_server.py")
        else:
            print(f"[!] SERVER ERROR: {e}")
    except Exception as e:
        print(f"[!] CRITICAL FAILURE: {e}")
