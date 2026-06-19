#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS PANEL STARTUP WRAPPER
=============================
Fixes encoding issues before starting JARVIS panel
"""

import sys
import os

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
    except Exception as e:
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

# Set environment variable for UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import and run JARVIS panel
try:
    import jarvis_panel
    print("[OK] JARVIS Panel starting...")
except Exception as e:
    print(f"[X] Error starting JARVIS: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
