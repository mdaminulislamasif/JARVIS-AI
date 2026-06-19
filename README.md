# 🤖 JARVIS — Just A Rather Very Intelligent System

> An Iron Man-inspired AI Assistant with a 3D animated face, voice control, multi-model AI brain, automation engine, and a full-featured GUI control panel.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 🧠 **Multi-Model Brain** | Supports Gemini, Claude, GPT-4o, Groq, Mistral, DeepSeek, Cohere |
| 🎙️ **Voice Engine** | Real-time speech-to-text + text-to-speech with male/female voice selector |
| 🖥️ **3D Animated Face** | Panda3D-powered 3D face with blinking, jaw movement, and head sway |
| ⚡ **Automation Engine** | Full PC control — mouse, keyboard, network scanning, process management |
| 📱 **Mobile Bridge** | Remote socket server to control JARVIS from any device on the network |
| 🔐 **Auth System** | Server-backed authentication with token sync |
| 🌐 **GUI Control Panel** | Rich customtkinter panel with OSINT tools, chat, and system controls |
| 🧬 **Self-Learning** | Learns from every interaction and improves over time |

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install customtkinter panda3d panda3d-gltf pillow psutil pyautogui speechrecognition pyttsx3
```

### Launch
```bash
python START_JARVIS.py
```

---

## 🗂️ Project Structure

```
ai/
├── START_JARVIS.py              # Main launcher
├── jarvis_panel.py              # Central GUI control panel
├── jarvis_ultimate_learner.py   # Self-learning engine
├── jarvis_face.glb              # 3D face model (Blender-generated)
├── core/
│   ├── brain.py                 # AI brain (multi-provider routing)
│   ├── database.py              # SQLite session history
│   ├── auth.py                  # Authentication system
│   └── login_window.py          # Login UI
├── engine/
│   ├── face3d.py                # 3D face controller
│   ├── face3d_run.py            # Panda3D face renderer
│   ├── voice.py                 # Voice engine
│   ├── automation.py            # OS automation
│   └── mobile_server.py         # Mobile socket bridge
└── jarvis_learned_files/        # Training & model files
```

---

## 🔑 API Keys Setup

Create `jarvis_config.txt` in the project root (one key per line):
```
AIza...          ← Gemini key
sk-ant-...       ← Claude/Anthropic key
sk-proj-...      ← OpenAI key
gsk_...          ← Groq key
```

> ⚠️ Never commit your API keys. `jarvis_config.txt` is in `.gitignore`.

---

## 🧠 AI Providers Supported

- **Google Gemini** (2.5 Pro, 2.0 Flash, 1.5 Pro...)
- **Anthropic Claude** (claude-3-5-sonnet)
- **OpenAI GPT-4o**
- **Groq** (Llama 3.3 70B)
- **Mistral** (mistral-large)
- **DeepSeek** (deepseek-chat)
- **Cohere** (command-r-plus)

---

## 👨‍💻 Developer

**ASIF GK** — `asifgk.hacker@gmail.com`

Built with ❤️ and the help of **Antigravity AI** coding assistant.

---

## 📜 License

MIT License — Free to use, modify, and distribute.
