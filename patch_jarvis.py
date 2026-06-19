#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch jarvis_panel.py to fix normalize_voice_command"""

import re

path = r"C:\Users\asifg\OneDrive\Desktop\ai\jarvis_panel.py"

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Find and replace the normalize_voice_command method
old_start = "    def normalize_voice_command(self, query):"
old_end   = "    def process(self, query):"

new_method = '''    def normalize_voice_command(self, query):
        """Bangla/Banglish voice command ke JARVIS command e convert kore"""
        import re as _re
        import webbrowser as _wb
        import urllib.parse as _up
        q = query.strip().lower()

        # 3D Face control
        face_on  = ["face on", "face calu", "face chalao", "3d on", "face start",
                    "face open", "face dekao", "face jalao", "face deko",
                    "\u09a5\u09cd\u09b0\u09bf\u09a1\u09bf \u09ab\u09c7\u09b8 \u0985\u09a8",
                    "\u09ab\u09c7\u09b8 \u0985\u09a8", "\u09ab\u09c7\u09b8 \u099a\u09be\u09b2\u09c1",
                    "\u09a5\u09cd\u09b0\u09bf\u09a1\u09bf \u09ab\u09c7\u09b8 \u099a\u09be\u09b2\u09c1"]
        face_off = ["face off", "face bondho", "face band", "3d off", "face stop",
                    "\u09ab\u09c7\u09b8 \u0985\u09ab", "\u09ab\u09c7\u09b8 \u09ac\u09a8\u09cd\u09a7"]
        for kw in face_on:
            if kw in q:
                self.after(0, self.face3d_on)
                return "__HANDLED__"
        for kw in face_off:
            if kw in q:
                self.after(0, self.face3d_off)
                return "__HANDLED__"

        # YouTube smart routing
        if "youtube" in q or "\u0987\u0989\u099f\u09bf\u0989\u09ac" in q:
            m = _re.search(r"(?:search|sarche|\u09b8\u09be\u09b0\u09cd\u099a|\u0996\u09cb\u0981\u099c)\s+(.+)", q)
            if m:
                url = "https://www.youtube.com/results?search_query=" + _up.quote(m.group(1).strip())
            else:
                url = "https://www.youtube.com"
            self.after(0, lambda u=url: _wb.open(u))
            self.after(0, lambda: self.log("JARVIS", "YouTube open korchi, sir!"))
            return "__HANDLED__"

        # Google smart routing
        if "google" in q or "\u0997\u09c1\u0997\u09b2" in q:
            m = _re.search(r"(?:search|sarche|\u09b8\u09be\u09b0\u09cd\u099a)\s+(.+)", q)
            if m:
                url = "https://www.google.com/search?q=" + _up.quote(m.group(1).strip())
            else:
                url = "https://www.google.com"
            self.after(0, lambda u=url: _wb.open(u))
            self.after(0, lambda: self.log("JARVIS", "Google open korchi, sir!"))
            return "__HANDLED__"

        # Chrome / Browser open
        if any(w in q for w in ["chrome", "browser", "open chrome",
                                  "\u09ac\u09cd\u09b0\u09be\u0989\u099c\u09be\u09b0",
                                  "\u0995\u09cd\u09b0\u09cb\u09ae"]):
            try:
                import subprocess
                subprocess.Popen(["start", "chrome"], shell=True)
            except Exception:
                _wb.open("https://www.google.com")
            self.after(0, lambda: self.log("JARVIS", "Chrome open korchi, sir!"))
            return "__HANDLED__"

        # Aliases
        aliases = {
            "clean":      ("\u0995\u09cd\u09b2\u09bf\u09a8", "\u09aa\u09b0\u09bf\u09b7\u09cd\u0995\u09be\u09b0", "\u09b8\u09be\u09ab"),
            "workspace":  ("\u0993\u09af\u09bc\u09be\u09b0\u09cd\u0995\u09b8\u09cd\u09aa\u09c7\u09b8", "\u0995\u09be\u099c \u09b6\u09c1\u09b0\u09c1"),
            "screenshot": ("\u09b8\u09cd\u0995\u09cd\u09b0\u09bf\u09a8\u09b6\u099f", "\u09b8\u09cd\u0995\u09cd\u09b0\u09bf\u09a8 \u09b6\u099f", "\u099b\u09ac\u09bf \u09a4\u09cb\u09b2\u09cb"),
            "disk":       ("\u09a1\u09bf\u09b8\u09cd\u0995", "\u09b8\u09cd\u099f\u09cb\u09b0\u09c7\u099c"),
            "battery":    ("\u09ac\u09cd\u09af\u09be\u099f\u09be\u09b0\u09bf", "\u099a\u09be\u09b0\u09cd\u099c"),
            "processes":  ("\u09aa\u09cd\u09b0\u09b8\u09c7\u09b8", "\u099a\u09b2\u09ae\u09be\u09a8"),
            "memory":     ("\u09ae\u09c7\u09ae\u09b0\u09bf", "ram"),
            "taskmgr":    ("\u099f\u09be\u09b8\u09cd\u0995 \u09ae\u09cd\u09af\u09be\u09a8\u09c7\u099c\u09be\u09b0",),
            "wifi":       ("\u0993\u09af\u09bc\u09be\u0987\u09ab\u09be\u0987", "\u0993\u09af\u09bc\u09be\u0987 \u09ab\u09be\u0987"),
            "users":      ("\u0987\u0989\u099c\u09be\u09b0", "\u09ac\u09cd\u09af\u09ac\u09b9\u09be\u09b0\u0995\u09be\u09b0\u09c0"),
            "devices":    ("\u09a1\u09bf\u09ad\u09be\u0987\u09b8", "\u09af\u09a8\u09cd\u09a4\u09cd\u09b0"),
            "router":     ("\u09b0\u09be\u0989\u099f\u09be\u09b0",),
            "mobile":     ("\u09ae\u09cb\u09ac\u09be\u0987\u09b2", "atom", "atom 5"),
            "android":    ("\u098f\u09a8\u09cd\u09a1\u09cd\u09b0\u09af\u09bc\u09be\u09a1", "android"),
            "kali":       ("\u0995\u09be\u09b2\u09bf", "\u0995\u09be\u09b2 \u09b9\u09cb\u09b8\u09cd\u099f", "kali mode"),
            "virus":      ("\u09ad\u09be\u0987\u09b0\u09be\u09b8",),
            "call":       ("\u09ab\u09cb\u09a8 \u0995\u09b2", "\u0995\u09b2 \u0995\u09b0\u09cb"),
            "monitor":    ("\u09ae\u09a8\u09bf\u099f\u09b0",),
        }
        for cmd, words in aliases.items():
            if q == cmd or any(w in q for w in words):
                return cmd
        return query

'''

# Find positions
start_idx = content.find(old_start)
end_idx   = content.find(old_end, start_idx)

if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find normalize_voice_command method!")
    print(f"start found: {start_idx != -1}, end found: {end_idx != -1}")
else:
    new_content = content[:start_idx] + new_method + content[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS: normalize_voice_command patched!")

# Also fix process to handle __HANDLED__
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_process_start = "    def process(self, query):\n        # Skip if already handled by normalize"
if old_process_start not in content:
    # Add skip at beginning of process
    old = "    def process(self, query):\n        self.core.set_state"
    new = "    def process(self, query):\n        if query == \"__HANDLED__\":\n            return\n        self.core.set_state"
    if old in content:
        content = content.replace(old, new, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: process() __HANDLED__ guard added!")
    else:
        print("WARNING: process() start not found for guard patch")
else:
    print("INFO: __HANDLED__ guard already present")

print("\nAll patches done!")
