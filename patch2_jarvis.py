#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch2: Fix normalize_voice_command - move youtube/google checks before browser alias"""

path = r"C:\Users\asifg\OneDrive\Desktop\ai\jarvis_panel.py"

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# The problem: "ব্রাউজারে ইউটিউব অন" hits "ব্রাউজার" alias before youtube check
# Fix: add "ব্রাউজারে ইউটিউব" and similar phrases to youtube check
# Also add voice_capture cleanup to strip trailing routing tags

# Fix 1: In voice_capture, strip routing suffix from query before processing
old_vc = '''            query = self.voice.listen()
            if query != "none":
                self.prefer_bangla_voice = (
                    str(getattr(self.voice, "last_language", "")).lower().startswith("bn")
                    or self.voice.has_bangla(query)
                )
                routed_query = self.normalize_voice_command(query)
                if routed_query != query:
                    self.after(0, lambda q=query, r=routed_query: self.log("VOICE", f"{q} -> {r}"))
                else:
                    self.after(0, lambda q=query: self.log("VOICE", q))
                self.process(routed_query)'''

new_vc = '''            query = self.voice.listen()
            if query != "none":
                # Strip any routing suffix like "-> browser" from voice input
                import re as _re_vc
                query = _re_vc.sub(r'\s*->\s*\w+\s*$', '', query).strip()
                
                self.prefer_bangla_voice = (
                    str(getattr(self.voice, "last_language", "")).lower().startswith("bn")
                    or self.voice.has_bangla(query)
                )
                routed_query = self.normalize_voice_command(query)
                if routed_query not in (query, "__HANDLED__"):
                    self.after(0, lambda q=query, r=routed_query: self.log("VOICE", f"{q} -> {r}"))
                else:
                    self.after(0, lambda q=query: self.log("VOICE", q))
                self.process(routed_query)'''

if old_vc in content:
    content = content.replace(old_vc, new_vc, 1)
    print("FIX 1: voice_capture routing cleanup applied!")
else:
    print("WARNING: voice_capture section not found for fix 1")

# Fix 2: In normalize_voice_command, add youtube/google detection BEFORE browser alias
# Find the youtube check and make it also catch "ব্রাউজারে ইউটিউব"
old_yt = '        # YouTube smart routing\n        if "youtube" in q or'
new_yt = '''        # YouTube smart routing (also catch "browsere youtube" patterns)
        if "youtube" in q or "ইউটিউব" in q or "youtu" in q or'''

if old_yt in content:
    content = content.replace(old_yt, new_yt, 1)
    print("FIX 2: YouTube detection expanded!")
else:
    # Try alternative
    old_yt2 = '        # YouTube smart routing'
    if old_yt2 in content:
        print("INFO: Found youtube section with different content - checking...")
        idx = content.find(old_yt2)
        print(f"Context: {content[idx:idx+100]}")
    else:
        print("WARNING: YouTube section not found")

# Fix 3: Remove "ব্রাউজার" from aliases so it doesn't intercept youtube commands
old_alias_browser = '"browser":    ("ব্রাউজার", "ব্রাউজার ওপেন"),'
new_alias_browser = '"browser":    ("open browser", "browser open"),'  # keep but less greedy

if old_alias_browser in content:
    content = content.replace(old_alias_browser, new_alias_browser, 1)
    print("FIX 3: Browser alias made less greedy!")
else:
    # Try other variants
    old_b2 = '"browser":    ("ব্রাউজার", "ক্রোম", "chrome", "ব্রাউজার ওপেন"),'
    if old_b2 in content:
        # Only keep non-bangla triggers for browser alias since chrome/youtube are handled above
        content = content.replace(old_b2, '"browser":    ("open browser",),', 1)
        print("FIX 3b: Browser alias cleaned!")
    else:
        print("INFO: Browser alias variant - searching...")
        idx = content.find('"browser":')
        if idx > 0:
            print(f"Found browser alias at: {content[idx:idx+80]}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("\nAll patches applied!")
print("Verifying syntax...")
import ast
try:
    ast.parse(open(path, encoding="utf-8", errors="ignore").read())
    print("Syntax OK!")
except SyntaxError as e:
    print(f"Syntax ERROR: {e}")
