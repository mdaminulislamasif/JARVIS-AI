import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jarvis_code_studio.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'class JarvisVoiceEngine' in line or 'def log_voice' in line:
        print(f"Line {idx+1}: {line.strip()[:120]}")
