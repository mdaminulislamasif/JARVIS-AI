import os
import sys

# Try the newer google-genai SDK first, fall back to google-generativeai
try:
    import google.genai as genai
    USE_NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_SDK = False

# Resolve config path: workspace-local first, then Desktop/ai/
_WORKSPACE_CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jarvis_config.txt')
_DESKTOP_CFG   = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'ai', 'jarvis_config.txt')
CONFIG_PATH    = _WORKSPACE_CFG if os.path.exists(_WORKSPACE_CFG) else _DESKTOP_CFG


def get_saved_keys():
    keys = []
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            for line in f:
                key = line.strip()
                if (key.startswith("AIza") or key.startswith("AQ.")) and len(key) > 30:
                    keys.append(key)
    return keys


keys = get_saved_keys()
if not keys:
    raise SystemExit(f"No Gemini API key found in {CONFIG_PATH}")

print(f"Found {len(keys)} key(s). Checking models for first key: {keys[0][:10]}...")

try:
    if USE_NEW_SDK:
        client = genai.Client(api_key=keys[0])
        for m in client.models.list():
            name = getattr(m, 'name', '')
            methods = getattr(m, 'supported_generation_methods', []) or []
            if 'generateContent' in methods or not methods:
                print(name)
    else:
        genai.configure(api_key=keys[0])
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
