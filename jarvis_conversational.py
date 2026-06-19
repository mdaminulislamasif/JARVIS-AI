"""
JARVIS CONVERSATIONAL AI  (Multi-Language Edition)
===================================================
বাংলায় কথা বলুন অথবা English-এ — দুটোই বুঝব!
Supports: Bengali, English, Hindi, Arabic and 100+ languages
"""
import sys
import io

# Force console stdout and stderr to use UTF-8 on Windows to prevent encoding crashes
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import os
import time
from datetime import datetime
import random
from engine.voice import VoiceEngine

# ── Multi-Language Voice Engine ───────────────────────────────────────────────
try:
    from jarvis_multilang_voice import (
        JarvisMultiLangVoice,
        BANGLA_GREETINGS,
        BANGLA_SEARCH_WORDS,
        BANGLA_OPEN_WORDS,
        BANGLA_TIME_WORDS,
        BANGLA_DATE_WORDS,
        BANGLA_WEATHER_WORDS,
        BANGLA_HELP_WORDS,
        BANGLA_STOP_WORDS,
        BANGLA_RESPONSES,
    )
    MULTILANG_AVAILABLE = True
except ImportError:
    MULTILANG_AVAILABLE = False
    print("⚠️  jarvis_multilang_voice.py not found — English only mode")

# Try to import Direct AI Chat for smart conversations
try:
    from jarvis_direct_ai_chat import DirectAIChat
    DIRECT_AI_AVAILABLE = True
except ImportError:
    DIRECT_AI_AVAILABLE = False
    print("⚠️  jarvis_direct_ai_chat.py not found — offline fallback only")

class JarvisConversational:
    def __init__(self):
        print("🤖 Initializing JARVIS Conversational AI (Multi-Language)...")

        # ── Multi-Language Engine ──────────────────────────────────────────
        if MULTILANG_AVAILABLE:
            self._mlv = JarvisMultiLangVoice(
                preferred_lang="bn-BD",        # বাংলা first!
                fallback_langs=["en-US", "hi-IN"]
            )
            self.recognizer  = self._mlv.recognizer
            self.microphone  = self._mlv.microphone
            print("✅ বাংলা ভয়েস সাপোর্ট চালু হয়েছে! (Bengali voice support enabled)")
        else:
            self._mlv = None
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            self.recognizer.dynamic_energy_ratio = 1.5
            self.microphone = self._select_best_microphone()
            # Calibrate once on startup
            print("🎤 Calibrating microphone for ambient noise...")
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                if self.recognizer.energy_threshold > 350:
                    self.recognizer.energy_threshold = 350
                elif self.recognizer.energy_threshold < 100:
                    self.recognizer.energy_threshold = 100
                print(f"🎤 Calibrated. Energy threshold: {self.recognizer.energy_threshold:.0f}")
            except Exception as e:
                print(f"⚠️ Microphone calibration failed: {e}")

        self.mic_muted = False
        self.current_language = "bn-BD"   # default
        
        # Text-to-speech
        try:
            self.voice_engine = VoiceEngine()
        except Exception as e:
            print(f"⚠️ Could not load neural VoiceEngine: {e}")

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Set male voice
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'male' in voice.name.lower() and 'female' not in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Conversation state
        self.conversation_context = []
        self.user_name = None
        self.user_preferences = {}
        self.current_topic = None
        self.waiting_for_response = False
        self.last_question = None
        
        # Database
        self.db_file = "jarvis_conversations.db"
        self.init_database()
        
        # Load user profile
        self.load_user_profile()
        
        # Initialize Direct AI Chat client
        if DIRECT_AI_AVAILABLE:
            self.ai_chat = DirectAIChat()
            print("🧠 Smart AI Conversational Chat client initialized!")
        else:
            self.ai_chat = None

        # Initialize Project Indexer and perform startup scan
        try:
            from jarvis_project_indexer import ProjectIndexer
            self.indexer = ProjectIndexer()
            print("📁 Project indexer initialized!")
            # Run startup scan
            scan_results = self.indexer.scan_project()
            self.startup_scan_summary = scan_results
        except Exception as e:
            print(f"⚠️ Indexer failed to start: {e}")
            self.indexer = None
            self.startup_scan_summary = None
            
        print("✅ JARVIS Conversational AI Ready!")

    # ── MICROPHONE CONTROL ────────────────────────────────────────────
    def _select_best_microphone(self):
        """
        Auto-detect the best microphone.
        Priority:
          1. jarvis_mic_config.json  (set by PHONE_AUDIO_BRIDGE.py = phone mic)
          2. USB Audio Device        (phone connected via USB audio class)
          3. System default microphone
        """
        import json, os
        mics = sr.Microphone.list_microphone_names()

        # ── Priority 1: Phone Audio Bridge config ─────────────────────────
        # Bypassed to prioritize PC local microphone over phone mic as requested
        # config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                            "jarvis_mic_config.json")
        # if os.path.exists(config_path):
        #     try:
        #         with open(config_path) as f:
        #             cfg = json.load(f)
        #         idx = cfg.get("phone_mic_index")
        #         if idx is not None and 0 <= idx < len(mics):
        #             print(f"   [PHONE MIC] Using phone mic from config: [{idx}] {mics[idx]}")
        #             return sr.Microphone(device_index=idx)
        #     except Exception:
        #         pass

        # ── Priority 2: USB Audio Device auto-detect ──────────────────────
        preferred_keywords = ['usb audio', 'usb mic', 'microphone (usb', 'headset', 'external']
        print(f"   Scanning {len(mics)} audio device(s)...")
        best_index = None
        for i, name in enumerate(mics):
            name_lower = name.lower()
            if any(x in name_lower for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                continue
            if any(kw in name_lower for kw in preferred_keywords):
                if best_index is None:
                    best_index = i
                    print(f"   [USB MIC] Selected: [{i}] {name}")

        if best_index is not None:
            return sr.Microphone(device_index=best_index)

        # ── Priority 3: Scan for any input device ─────────────────────────
        import pyaudio
        pa_temp = pyaudio.PyAudio()
        any_idx = None
        for i in range(pa_temp.get_device_count()):
            try:
                info = pa_temp.get_device_info_by_index(i)
                if info.get('maxInputChannels', 0) > 0:
                    name_lower = info.get('name', '').lower()
                    if any(x in name_lower for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                        continue
                    any_idx = i
                    break
            except Exception:
                pass
        pa_temp.terminate()
        
        if any_idx is not None:
            print(f"   [ANY MIC] Selected first available input device: [{any_idx}] {mics[any_idx]}")
            return sr.Microphone(device_index=any_idx)

        # ── Priority 4: System default ────────────────────────────────────
        print("   [DEFAULT MIC] Using system default microphone")
        return sr.Microphone()

    def list_microphones(self):
        """Print all available microphone devices."""
        mics = sr.Microphone.list_microphone_names()
        result = "Available microphones:\n"
        for i, name in enumerate(mics):
            marker = "<< ACTIVE" if hasattr(self.microphone, 'device_index') and self.microphone.device_index == i else ""
            result += f"  [{i}] {name} {marker}\n"
        return result

    def switch_microphone(self, index):
        """Switch to a different microphone by index."""
        mics = sr.Microphone.list_microphone_names()
        if 0 <= index < len(mics):
            self.microphone = sr.Microphone(device_index=index)
            return f"Switched to microphone: {mics[index]}"
        return f"Invalid mic index {index}. Use 0–{len(mics)-1}."

    def set_mic_volume(self, level_percent):
        """Set PC microphone volume via Windows API (0-100)."""
        try:
            import subprocess
            level = max(0, min(100, int(level_percent)))
            # Use SoundVolumeView or nircmd if available, else PowerShell
            ps_cmd = (
                f"$obj = New-Object -ComObject WScript.Shell; "
                f"Add-Type -TypeDefinition \""
                f"using System.Runtime.InteropServices;"
                f"[Guid(\"D666063F-1587-4E43-81F1-B948E807363F\")]"
                f"\"; "
                f"$mic = [NAudio.CoreAudioApi.MMDeviceEnumerator]::new(); "
                f"echo 'Volume control attempted'"
            )
            # Simpler: Use mmsys.cpl mic page
            subprocess.Popen(
                'powershell Start-Process sndvol -ArgumentList "-r 0"',
                shell=True
            )
            return f"Microphone volume set attempt for {level}%. Windows Sound panel opened."
        except Exception as e:
            return f"Could not set mic volume: {e}"

    def mute_mic(self, mute=True):
        """Mute or unmute the software microphone listening."""
        self.mic_muted = mute
        state = "MUTED" if mute else "UNMUTED"
        return f"Microphone {state}."

    def adjust_sensitivity(self, threshold=None):
        """Adjust microphone sensitivity (energy threshold)."""
        if threshold:
            self.recognizer.energy_threshold = int(threshold)
            return f"Mic sensitivity set to energy threshold: {threshold}"
        # Auto-calibrate
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            return f"Mic auto-calibrated. Energy threshold: {self.recognizer.energy_threshold:.0f}"
        except Exception as e:
            return f"Calibration failed: {e}"

    def init_database(self):
        """Initialize conversation database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                jarvis_response TEXT,
                context TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def speak(self, text):
        """Speak with personality using premium neural or offline TTS"""
        print(f"\n🤖 JARVIS: {text}")
        
        # Save to conversation
        self.conversation_context.append({
            'speaker': 'jarvis',
            'text': text,
            'timestamp': datetime.now()
        })
        
        try:
            if hasattr(self, 'voice_engine'):
                # Pass the detected/current language context if available
                if hasattr(self, 'current_language'):
                    self.voice_engine.last_language = self.current_language
                self.voice_engine.speak(text)
            else:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"⚠️ Speak Error: {e}")
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass
        
    def listen(self, timeout=10):
        """
        Listen in Bangla + English (+ Hindi) — auto-detects language.
        বাংলায় বলুন বা English-এ — দুটোই বোঝা যাবে!
        """
        if self.mic_muted:
            print("🔇 মাইক্রোফোন মিউট আছে — listening skip")
            return None

        # ── Use Multi-Language Engine if available ─────────────────────────
        if self._mlv:
            text, lang = self._mlv.listen(timeout=timeout, phrase_limit=15)
            if text:
                self.current_language = lang or "en-US"
                # Save to context
                self.conversation_context.append({
                    'speaker': 'user',
                    'text': text,
                    'timestamp': datetime.now(),
                    'language': self.current_language,
                })
                # If Bangla, handle directly here
                if lang and lang.startswith("bn"):
                    result = self._mlv.process_bangla_command(text)
                    if result["action"] not in ("unknown", None):
                        self.speak(result["response"])
                        # For search/open pass through to normal handling
                        if result["action"] in ("search", "open", "weather"):
                            return text   # let process_conversation handle it
                        return "__BANGLA_HANDLED__"
            return text

        # ── Fallback: English-only (if multilang not available) ────────────
        try:
            with self.microphone as source:
                 print("\n🎤 Listening... (Speak now)")
                 audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)

            print("🔄 Processing...")
            # Try Bengali first, then English
            text = None
            for lang_code in ["bn-BD", "en-US", "hi-IN"]:
                try:
                    text = self.recognizer.recognize_google(audio, language=lang_code)
                    if text:
                        print(f"👤 [{lang_code}] You: {text}")
                        break
                except sr.UnknownValueError:
                    continue

            if not text:
                self.speak("বোঝা যায়নি। আবার বলুন।")
                return None

            text = text.strip()
            self.conversation_context.append({
                'speaker': 'user',
                'text': text,
                'timestamp': datetime.now()
            })
            return text

        except sr.WaitTimeoutError:
            return None
        except OSError as e:
            print(f"⚠️ Mic OSError: {e}. Re-initializing...")
            self.microphone = self._select_best_microphone()
            return None
        except Exception as e:
            print(f"⚠️ Listen Error: {e}")
            return None
    
    def load_user_profile(self):
        """Load user profile"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT key, value FROM user_profile')
            for key, value in cursor.fetchall():
                self.user_preferences[key] = value
            conn.close()
            
            self.user_name = self.user_preferences.get('name')
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    def save_user_preference(self, key, value):
        """Save user preference"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO user_profile (key, value)
            VALUES (?, ?)
        ''', (key, value))
        conn.commit()
        conn.close()
        self.user_preferences[key] = value
    
    def greet_user(self):
        """Greet user based on time and context"""
        hour = datetime.now().hour
        
        if self.user_name:
            if hour < 12:
                greeting = f"Good morning, {self.user_name}!"
            elif hour < 18:
                greeting = f"Good afternoon, {self.user_name}!"
            else:
                greeting = f"Good evening, {self.user_name}!"
        else:
            if hour < 12:
                greeting = "Good morning!"
            elif hour < 18:
                greeting = "Good afternoon!"
            else:
                greeting = "Good evening!"
        
        self.speak(greeting + " I'm JARVIS, your conversational AI assistant.")
        
        # Announce project updates if any detected
        if hasattr(self, 'startup_scan_summary') and self.startup_scan_summary:
            new_count = len(self.startup_scan_summary.get("new", []))
            mod_count = len(self.startup_scan_summary.get("modified", []))
            del_count = len(self.startup_scan_summary.get("deleted", []))
            
            if new_count > 0 or mod_count > 0 or del_count > 0:
                update_msg = "স্যার, প্রজেক্ট ফোল্ডারে কিছু পরিবর্তন পাওয়া গেছে। "
                changes = []
                if new_count > 0:
                    changes.append(f"{new_count}টি নতুন ফাইল")
                if mod_count > 0:
                    changes.append(f"{mod_count}টি আপডেট হওয়া ফাইল")
                if del_count > 0:
                    changes.append(f"{del_count}টি মুছে ফেলা ফাইল")
                update_msg += " এবং ".join(changes) + " সনাক্ত করা হয়েছে।"
                self.speak(update_msg)
        
        if not self.user_name:
            self.speak("I don't think we've been properly introduced. What's your name?")
            self.waiting_for_response = True
            self.last_question = "name"
    
    def process_conversation(self, user_input):
        """
        Process conversation — supports Bangla + English + all languages.
        বাংলা এবং English দুটো ভাষাই বোঝা যাবে।
        """
        # Skip if already handled by multi-lang engine
        if user_input == "__BANGLA_HANDLED__":
            return True

        # ── ADB DEVICES & MICROPHONE BOOST COMMAND ─────────────────────────
        has_devices = any(w in t for w in ['devices', 'ডিভাইসেস', 'এডিবি ডিভাইস', 'adb devices'])
        has_boost = any(w in t for w in ['boost', 'বুস্ট', 'পোস্ট', 'বাড়িয়ে', 'বাড়াও']) and any(m in t for m in ['mic', 'microphone', 'মাইক', 'মাইক্রোফোন'])
        
        if has_devices or has_boost:
            if has_devices:
                self.speak("সংযুক্ত এডিবি ডিভাইসগুলোর তালিকা দেখছি...")
                try:
                    adb_path = r"C:\Users\asifg\OneDrive\Desktop\ai\platform-tools\adb.exe"
                    if not os.path.exists(adb_path):
                        adb_path = "adb"
                    import subprocess
                    res = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=5)
                    lines = res.stdout.strip().split("\n")[1:]
                    devices = [line.split()[0] for line in lines if "device" in line and "unauthorized" not in line]
                    
                    if devices:
                        dev_str = ", ".join(devices)
                        self.speak(f"পিসিতে {len(devices)}টি এডিবি ডিভাইস সংযুক্ত আছে। ডিভাইস আইডি: {dev_str}।")
                    else:
                        self.speak("পিসিতে কোনো এডিবি ডিভাইস সংযুক্ত পাওয়া যায়নি।")
                except Exception as e:
                    self.speak(f"এডিবি ডিভাইস চেক করতে সমস্যা হয়েছে: {e}")
            
            if has_boost:
                self.speak("মাইক্রোফোনের ভলিউম সর্বোচ্চ বাড়িয়ে দিচ্ছি...")
                try:
                    self.set_mic_volume(100)
                except Exception:
                    pass
                try:
                    adb_path = r"C:\Users\asifg\OneDrive\Desktop\ai\platform-tools\adb.exe"
                    if not os.path.exists(adb_path):
                        adb_path = "adb"
                    import subprocess
                    serial = "BD354558452086043"
                    settings = [
                        "volume_music",
                        "volume_voice_communication",
                        "volume_ring",
                        "volume_notification",
                    ]
                    for s in settings:
                        subprocess.run([adb_path, "-s", serial, "shell", "settings", "put", "system", s, "15"], capture_output=True)
                    subprocess.run([adb_path, "-s", serial, "shell", "for i in 1 2 3 4 5 6 7 8 9 10; do input keyevent 24; done"], capture_output=True)
                    self.speak("এডিবি ডিভাইস এবং পিসি মাইক্রোফোনের অডিও লেভেল সফলভাবে বুস্ট করা হয়েছে।")
                except Exception as e:
                    self.speak(f"ভলিউম বুস্ট করতে কিছু সমস্যা হয়েছে: {e}")
            return True

        # Handle waiting for specific response
        if self.waiting_for_response:
            return self.handle_expected_response(user_input)

        t = user_input.lower().strip()

        # ── PROJECT/FILES SCAN & UPDATE COMMANDS ───────────────────────────
        if any(w in t for w in ['প্রজেক্ট স্ক্যান', 'ফাইল স্ক্যান', 'নতুন ফাইল', 'আপডেট হওয়া ফাইল', 'কোন ফাইল আপডেট', 'scan project', 'project scan', 'scan files', 'update files']):
            self.speak("প্রজেক্ট ফোল্ডার স্ক্যান করছি, দয়া করে একটু অপেক্ষা করুন...")
            if hasattr(self, 'indexer') and self.indexer:
                scan_res = self.indexer.scan_project()
                new_files = scan_res.get("new", [])
                mod_files = scan_res.get("modified", [])
                del_files = scan_res.get("deleted", [])
                
                if not new_files and not mod_files and not del_files:
                    self.speak("প্রজেক্ট ফোল্ডারে নতুন কোনো পরিবর্তন পাওয়া যায়নি। সব ফাইল অপরিবর্তিত আছে।")
                else:
                    msg = "স্ক্যান সম্পন্ন হয়েছে। "
                    changes = []
                    if new_files:
                        changes.append(f"{len(new_files)}টি নতুন ফাইল (যেমন: {', '.join(new_files[:3])})")
                    if mod_files:
                        changes.append(f"{len(mod_files)}টি পরিবর্তিত ফাইল (যেমন: {', '.join(mod_files[:3])})")
                    if del_files:
                        changes.append(f"{len(del_files)}টি মুছে ফেলা ফাইল")
                    msg += " এবং ".join(changes) + " পাওয়া গেছে।"
                    self.speak(msg)
            else:
                self.speak("দুঃখিত স্যার, প্রজেক্ট ইনডেক্সার সক্রিয় নেই।")
            return True

        # ── BANGLA COMMANDS ────────────────────────────────────────────────
        if MULTILANG_AVAILABLE and self._mlv and self._mlv.is_bangla(t):
            result = self._mlv.process_bangla_command(t)
            action = result.get("action", "unknown")
            if action == "goodbye":
                self.speak(result["response"])
                return False
            if action == "sing":
                if hasattr(self, 'voice_engine') and self.voice_engine:
                    self.voice_engine.sing()
                else:
                    self.speak("আমি গান গাইছি...")
                    import winsound, threading
                    threading.Thread(target=lambda: [winsound.Beep(f, 200) for f in [262, 294, 330, 349, 392]], daemon=True).start()
                return True
            if action == "cry":
                if hasattr(self, 'voice_engine') and self.voice_engine:
                    self.voice_engine.cry()
                else:
                    self.speak("ওহহো... আমি কান্না করছি...")
                    import winsound, threading
                    threading.Thread(target=lambda: [winsound.Beep(f, 100) for f in range(600, 200, -50)], daemon=True).start()
                return True
            if action in ("greeting", "how_are_you", "thanks", "time", "date", "help"):
                self.speak(result["response"])
                return True
            if action == "search":
                self.speak(result["response"])
                return self.handle_search_conversation(result["query"])
            if action == "open":
                self.speak(result["response"])
                return self.handle_website_conversation(result["query"])
            if action == "weather":
                return self.handle_weather_conversation(t)
            # unknown — fall through to English processing below

        # ── BANGLA KEYWORDS (even if mixed with English) ───────────────────
        if MULTILANG_AVAILABLE:
            if any(w in t for w in BANGLA_GREETINGS):
                self.speak(random.choice(BANGLA_RESPONSES["greeting"]))
                return True
            if any(w in t for w in BANGLA_TIME_WORDS):
                current_time = datetime.now().strftime("%I:%M %p")
                self.speak(BANGLA_RESPONSES["time"].format(current_time))
                return True
            if any(w in t for w in BANGLA_DATE_WORDS):
                current_date = datetime.now().strftime("%d %B, %Y")
                self.speak(BANGLA_RESPONSES["date"].format(current_date))
                return True
            if any(w in t for w in BANGLA_STOP_WORDS):
                self.speak(random.choice(BANGLA_RESPONSES["goodbye"]))
                return False
            if any(w in t for w in BANGLA_SEARCH_WORDS):
                query = t
                for w in BANGLA_SEARCH_WORDS:
                    query = query.replace(w, "").strip()
                self.speak(f"{query} সার্চ করছি...")
                return self.handle_search_conversation(query)
            if any(w in t for w in BANGLA_HELP_WORDS):
                self.speak(BANGLA_RESPONSES["capabilities"])
                return True

        # ── ENGLISH COMMANDS ───────────────────────────────────────────────
        if 'sing' in t:
            if hasattr(self, 'voice_engine') and self.voice_engine:
                self.voice_engine.sing()
            else:
                self.speak("I am singing a song...")
                import winsound, threading
                threading.Thread(target=lambda: [winsound.Beep(f, 200) for f in [262, 294, 330, 349, 392]], daemon=True).start()
            return True

        if 'cry' in t:
            if hasattr(self, 'voice_engine') and self.voice_engine:
                self.voice_engine.cry()
            else:
                self.speak("I am so sorry...")
                import winsound, threading
                threading.Thread(target=lambda: [winsound.Beep(f, 100) for f in range(600, 200, -50)], daemon=True).start()
            return True

        if any(word in t for word in ['hello', 'hi', 'hey', 'greetings']):
            responses = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! Ready to assist you!",
                "Greetings! What would you like to do?"
            ]
            self.speak(random.choice(responses))
            return True

        if any(phrase in t for phrase in ['how are you', 'how do you do', 'how are things']):
            responses = [
                "I'm functioning perfectly, thank you for asking! How about you?",
                "I'm doing great! All systems operational. How are you?",
                "Excellent! Ready to help you with anything. How are you doing?",
            ]
            self.speak(random.choice(responses))
            self.waiting_for_response = True
            self.last_question = "user_wellbeing"
            return True

        if any(word in t for word in ['thank', 'thanks', 'appreciate', 'ধন্যবাদ']):
            self.speak(random.choice(["You're very welcome!", "Happy to help!", "আপনাকে স্বাগতম!"]))
            return True

        if 'my name is' in t or ('i am' in t and len(t) < 30) or 'call me' in t:
            self.extract_and_save_name(t)
            return True

        if any(w in t for w in ['mic', 'microphone', 'মাইক', 'মাইক্রোফোন']):
            return self.handle_mic_command(t)

        if any(t.startswith(word) for word in ['cmd ', 'powershell ', 'execute ', 'run ', 'set priority ', 'reg ', 'port conflict ', 'firewall ']) or any(kw in t for kw in ['self heal', 'self-healing']):
            return self.handle_system_command(t)

        if any(word in t for word in ['search', 'find', 'look for', 'google', 'খুঁজুন', 'সার্চ']):
            return self.handle_search_conversation(t)

        if any(word in t for word in ['open', 'go to', 'visit', 'website', 'খোলো', 'চালু']):
            return self.handle_website_conversation(t)

        if any(word in t for word in ['learn', 'teach', 'explain', 'tell me about']):
            return self.handle_learning_conversation(t)

        if any(word in t for word in ['what', 'when', 'where', 'who', 'why', 'how']):
            return self.handle_question_conversation(t)

        if 'time' in t or 'কটা বাজে' in t:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"It's {current_time}")
            return True

        if 'date' in t or 'today' in t:
            current_date = datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            return True

        if 'weather' in t or 'আবহাওয়া' in t:
            return self.handle_weather_conversation(t)

        if 'help' in t or 'what can you do' in t or 'সাহায্য' in t:
            self.show_capabilities_conversational()
            return True

        if any(word in t for word in ['exit', 'quit', 'bye', 'goodbye', 'stop', 'বিদায়', 'বাই']):
            return False

        # Default general response
        self.handle_general_conversation(t)
        return True
    
    def handle_expected_response(self, user_input):
        """Handle expected responses to questions"""
        
        if self.last_question == "name":
            self.extract_and_save_name(user_input)
            self.waiting_for_response = False
            return True
        
        elif self.last_question == "user_wellbeing":
            if any(word in user_input for word in ['good', 'great', 'fine', 'well', 'okay']):
                self.speak("That's wonderful to hear! What can I help you with today?")
            elif any(word in user_input for word in ['bad', 'not good', 'terrible', 'sad']):
                self.speak("I'm sorry to hear that. Is there anything I can do to help?")
            else:
                self.speak("I see. How can I assist you today?")
            self.waiting_for_response = False
            return True
        
        elif self.last_question == "search_confirm":
            if any(word in user_input for word in ['yes', 'yeah', 'sure', 'okay', 'please']):
                self.speak("Great! Opening the search results now.")
                # Execute the pending search
                return True
            else:
                self.speak("Okay, no problem. What else can I help you with?")
            self.waiting_for_response = False
            return True
        
        return True
    
    def handle_mic_command(self, user_input):
        """Handle microphone control voice commands."""
        inp = user_input.lower()

        if any(w in inp for w in ['mute', 'off', 'stop listening', 'disable']):
            msg = self.mute_mic(True)
            self.speak(msg)

        elif any(w in inp for w in ['unmute', 'on', 'enable', 'start listening']):
            msg = self.mute_mic(False)
            self.speak(msg)

        elif any(w in inp for w in ['list', 'show', 'available']):
            info = self.list_microphones()
            print(info)
            self.speak("Here are the available microphones. Check the console for the full list.")

        elif 'switch' in inp or 'change' in inp:
            import re
            nums = re.findall(r'\d+', inp)
            if nums:
                msg = self.switch_microphone(int(nums[0]))
                self.speak(msg)
            else:
                self.speak("Which microphone index would you like to switch to?")

        elif 'calibrate' in inp or 'adjust' in inp or 'sensitivity' in inp:
            self.speak("Calibrating microphone sensitivity. Please stay quiet for a moment.")
            msg = self.adjust_sensitivity()
            self.speak(msg)

        elif 'volume' in inp:
            import re
            nums = re.findall(r'\d+', inp)
            lvl = nums[0] if nums else 80
            msg = self.set_mic_volume(int(lvl))
            self.speak(msg)

        elif 'status' in inp or 'check' in inp:
            state = 'muted' if self.mic_muted else 'active'
            thresh = self.recognizer.energy_threshold
            dev_idx = getattr(self.microphone, 'device_index', 'default')
            mics = sr.Microphone.list_microphone_names()
            dev_name = mics[dev_idx] if isinstance(dev_idx, int) and dev_idx < len(mics) else 'Default'
            self.speak(f"Microphone is {state}. Active device: {dev_name}. Sensitivity threshold: {thresh:.0f}.")

        else:
            self.speak("I can control the microphone. Say mute, unmute, calibrate, status, switch, list, or set volume.")

        return True

    def handle_system_command(self, user_input):
        """Execute system commands and speak the response"""
        try:
            import engine.automation as aut
            
            clean_cmd = user_input.strip()
            if clean_cmd.startswith("jarvis "):
                clean_cmd = clean_cmd[7:].strip()
            if clean_cmd.startswith("run "):
                clean_cmd = clean_cmd[4:].strip()
            if clean_cmd.startswith("execute "):
                clean_cmd = clean_cmd[8:].strip()
                
            parts = clean_cmd.split(" ", 1)
            cmd_root = parts[0]
            cmd_args = parts[1] if len(parts) > 1 else ""
            
            response_text = ""
            
            # Try running via jarvis_system_control first
            try:
                from jarvis_system_control import jarvis_execute
                sys_res = jarvis_execute(clean_cmd)
                if not sys_res.startswith("Command not recognized:"):
                    self.speak(sys_res)
                    return True
            except Exception as e:
                print(f"[!] System control execution failed: {e}")

            if cmd_root == "cmd":
                self.speak(f"Executing command prompt instructions: {cmd_args}")
                response_text = aut.run_command_prompt(cmd_args)
            elif cmd_root == "powershell":
                self.speak(f"Executing PowerShell instructions: {cmd_args}")
                response_text = aut.run_powershell(cmd_args)
            else:
                response_text = aut.app_control(clean_cmd)
                
            self.speak(response_text)
            return True
        except Exception as e:
            self.speak(f"Sorry sir, I encountered an error running that command: {e}")
            return True
            
    def extract_and_save_name(self, text):
        """Extract and save user name"""
        # Try to extract name
        name = None
        
        if 'my name is' in text:
            name = text.split('my name is')[1].strip()
        elif 'i am' in text:
            name = text.split('i am')[1].strip()
        elif 'call me' in text:
            name = text.split('call me')[1].strip()
        else:
            # Assume the whole input is the name
            name = text.strip()
        
        # Clean up name
        name = name.split()[0].capitalize() if name else None
        
        if name:
            self.user_name = name
            self.save_user_preference('name', name)
            self.speak(f"Nice to meet you, {name}! I'll remember that.")
            self.speak("How can I help you today?")
        else:
            self.speak("I didn't quite catch your name. Could you tell me again?")
    
    def handle_search_conversation(self, user_input):
        """Handle search with conversation"""
        # Extract search query
        query = user_input
        for word in ['search', 'search for', 'find', 'look for', 'google']:
            query = query.replace(word, '').strip()
        
        if query:
            self.speak(f"You want me to search for {query}?")
            self.speak("Let me do that for you.")
            
            # Perform search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            
            self.speak(f"I've opened the search results for {query}. Is there anything specific you'd like to know about it?")
            self.current_topic = query
            self.waiting_for_response = True
            self.last_question = "search_followup"
        else:
            self.speak("What would you like me to search for?")
            self.waiting_for_response = True
            self.last_question = "search_query"
        
        return True
    
    def handle_website_conversation(self, user_input):
        """Handle website opening or local application launching (like IDE)"""
        t = user_input.lower()
        if any(w in t for w in ['code studio', 'code editor', 'ide', 'editor', 'কোড স্টুডিও', 'আইডিই']):
            self.speak("Opening Antigravity IDE Code Studio, sir.")
            import subprocess
            subprocess.Popen([sys.executable, "jarvis_code_studio.py"])
            return True

        # Extract website
        website = user_input
        for word in ['open', 'go to', 'visit', 'website', 'site']:
            website = website.replace(word, '').strip()
        
        if website:
            self.speak(f"Opening {website} for you.")
            
            # Open website
            if not website.startswith('http'):
                website = 'https://www.' + website.replace(' ', '') + '.com'
            webbrowser.open(website)
            
            self.speak("There you go! Let me know if you need anything else.")
        else:
            self.speak("Which website would you like me to open?")
            self.waiting_for_response = True
            self.last_question = "website_name"
        
        return True
    
    def handle_learning_conversation(self, user_input):
        """Handle learning with conversation"""
        # Extract topic
        topic = user_input
        for word in ['learn', 'teach', 'teach me', 'explain', 'tell me about']:
            topic = topic.replace(word, '').strip()
        
        if topic:
            self.speak(f"You want to learn about {topic}? Great choice!")
            self.speak("Let me find some information for you.")
            
            # Search Wikipedia
            wiki_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
            webbrowser.open(wiki_url)
            
            self.speak(f"I've opened Wikipedia for {topic}. Would you like me to search for more resources?")
            self.current_topic = topic
            self.waiting_for_response = True
            self.last_question = "learning_more"
        else:
            self.speak("What topic would you like to learn about?")
            self.waiting_for_response = True
            self.last_question = "learning_topic"
        
        return True
    
    def handle_question_conversation(self, user_input):
        """Handle questions with conversation"""
        self.speak("That's an interesting question!")
        self.speak("Let me search for the answer.")
        
        # Search for answer
        search_url = f"https://www.google.com/search?q={user_input.replace(' ', '+')}"
        webbrowser.open(search_url)
        
        self.speak("I've opened the search results. Does this answer your question?")
        self.waiting_for_response = True
        self.last_question = "question_answered"
        
        return True
    
    def handle_weather_conversation(self, user_input):
        """Handle weather with conversation"""
        self.speak("Let me check the weather for you.")
        
        # Open weather
        webbrowser.open("https://www.google.com/search?q=weather")
        
        self.speak("Here's the current weather. Would you like to know the forecast for the week?")
        self.waiting_for_response = True
        self.last_question = "weather_forecast"
        
        return True
    
    def handle_general_conversation(self, user_input):
        """Handle general conversation using DirectAIChat or fall back to static responses"""
        if hasattr(self, 'ai_chat') and self.ai_chat:
            self.speak("Thinking...")
            
            current_prompt = user_input
            max_turns = 8
            final_response = ""
            last_ai_response = ""
            
            for turn in range(max_turns):
                res = self.ai_chat.chat_with_ai(current_prompt)
                if not res.get('success'):
                    last_ai_response = res.get('response', 'AI error')
                    break
                    
                response_text = res.get('response', '')
                last_ai_response = response_text
                
                # Parse lines for EXECUTE commands
                lines = response_text.splitlines()
                execute_commands = []
                for line in lines:
                    if "EXECUTE:" in line:
                        cmd = line.split("EXECUTE:", 1)[1].strip()
                        execute_commands.append(cmd)
                        
                if not execute_commands:
                    final_response = response_text
                    break
                    
                # We have commands to execute!
                feedback_parts = []
                for cmd in execute_commands:
                    print(f"🤖 JARVIS AI Executing: {cmd}")
                    # 1. read_file
                    if cmd.startswith("read_file "):
                        filepath = cmd.split("read_file ", 1)[1].strip()
                        resolved_path = os.path.abspath(os.path.join(_BASE, filepath))
                        try:
                            with open(resolved_path, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                            feedback_parts.append(f"[SYSTEM FEEDBACK: File '{filepath}' read successfully. Content follows:\n```\n{content}\n```]")
                        except Exception as e:
                            feedback_parts.append(f"[SYSTEM FEEDBACK: Error reading file '{filepath}': {e}]")
                    # 2. cmd / powershell
                    elif cmd.startswith("cmd ") or cmd.startswith("powershell "):
                        is_ps = cmd.startswith("powershell ")
                        cmd_str = cmd.split("powershell ", 1)[1].strip() if is_ps else cmd.split("cmd ", 1)[1].strip()
                        # Run visibly in terminal
                        self.execute_ai_system_command(cmd)
                        
                        # Capture output to return to AI
                        try:
                            shell_args = ["powershell.exe", "-Command", cmd_str] if is_ps else ["cmd.exe", "/c", cmd_str]
                            proc_res = subprocess.run(shell_args, capture_output=True, text=True, timeout=15)
                            output_str = f"STDOUT:\n{proc_res.stdout or ''}\nSTDERR:\n{proc_res.stderr or ''}\nExit Code: {proc_res.returncode}"
                        except Exception as e:
                            output_str = f"Execution failed: {e}"
                        feedback_parts.append(f"[SYSTEM FEEDBACK: Command executed. Output:\n{output_str}]")
                    # 3. other actions
                    else:
                        try:
                            self.execute_ai_system_command(cmd)
                            feedback_parts.append(f"[SYSTEM FEEDBACK: Action '{cmd}' triggered successfully.]")
                        except Exception as e:
                            feedback_parts.append(f"[SYSTEM FEEDBACK: Action '{cmd}' failed: {e}]")
                            
                # Combine feedbacks and loop
                follow_up = "Below is the execution result/feedback for your commands:\n\n" + "\n\n".join(feedback_parts) + "\n\nPlease continue. If you need to do more tasks or read/write more files, write EXECUTE: [command]. Otherwise, provide your final response to the user."
                current_prompt = follow_up
                
            # Now speak and process the final response
            response_text = final_response or last_ai_response
            
            # Parse normal lines to speak (excluding EXECUTE statements)
            lines = response_text.splitlines()
            normal_lines = []
            for line in lines:
                if "EXECUTE:" not in line:
                    normal_lines.append(line)
            speak_text = "\n".join(normal_lines).strip()
            
            if speak_text:
                self.speak(speak_text)
            else:
                self.speak("Action completed, sir.")
            return
            
        responses = [
            "I understand. Let me help you with that.",
            "Interesting! Tell me more.",
            "I see. What would you like me to do?",
            "Got it! How can I assist with that?",
            "That's a good point. What do you need help with?"
        ]
        self.speak(random.choice(responses))

    def execute_ai_system_command(self, cmd):
        """Execute a system command generated by the AI model"""
        try:
            import engine.automation as aut
            clean_cmd = cmd.strip()
            
            # Check for mouse or keyboard actions
            if clean_cmd.startswith("mouse ") or clean_cmd.startswith("keyboard "):
                import engine.windows_control as wc
                parts = clean_cmd.split(" ", 1)
                cmd_root = parts[0]
                cmd_args = parts[1] if len(parts) > 1 else ""
                
                sub_parts = cmd_args.strip().split(None, 1)
                sub_action = sub_parts[0].lower() if sub_parts else ""
                sub_text = sub_parts[1].strip() if len(sub_parts) > 1 else ""
                
                if cmd_root == "mouse":
                    sub_args = cmd_args.strip().split()
                    sub_action = sub_args[0].lower() if sub_args else ""
                    sub_args = sub_args[1:]
                    if sub_action in ["move", "go", "moveto"] and len(sub_args) >= 2:
                        wc.mouse_move(sub_args[0], sub_args[1])
                    elif sub_action in ["click", "left", "clk"]:
                        if len(sub_args) >= 2:
                            wc.mouse_click(sub_args[0], sub_args[1])
                        else:
                            wc.mouse_click()
                    elif sub_action in ["right", "rclick"] and len(sub_args) >= 2:
                        wc.mouse_right_click(sub_args[0], sub_args[1])
                    elif sub_action in ["double", "dblclick"] and len(sub_args) >= 2:
                        wc.mouse_double_click(sub_args[0], sub_args[1])
                    elif sub_action in ["scroll"]:
                        amount = int(sub_args[0]) if sub_args else -3
                        x = sub_args[1] if len(sub_args) > 1 else None
                        y = sub_args[2] if len(sub_args) > 2 else None
                        wc.mouse_scroll(amount, x, y)
                elif cmd_root == "keyboard":
                    if sub_action in ["type", "write"]:
                        wc.keyboard_type(sub_text)
                    elif sub_action in ["press", "key"]:
                        wc.keyboard_press(sub_text)
                    elif sub_action in ["hotkey", "shortcut"]:
                        keys = [k.strip() for k in sub_text.replace("+", " ").split() if k.strip()]
                        wc.keyboard_hotkey(*keys)
            elif clean_cmd.startswith("cmd "):
                cmd_args = clean_cmd[4:].strip()
                aut.run_command_prompt(cmd_args)
            elif clean_cmd.startswith("powershell "):
                cmd_args = clean_cmd[11:].strip()
                aut.run_powershell(cmd_args)
            elif clean_cmd.startswith("app "):
                aut.app_control(clean_cmd[4:].strip())
            else:
                # Standard app or system automation command
                aut.app_control(clean_cmd)
        except Exception as e:
            print(f"Error executing AI system command: {e}")
    
    def show_capabilities_conversational(self):
        """Show capabilities in conversational way"""
        self.speak("I can help you with many things!")
        self.speak("I can search the web, open websites, learn new topics with you.")
        self.speak("I can answer questions, check the weather, tell you the time.")
        self.speak("I can also have conversations with you and remember our discussions.")
        self.speak("What would you like to do?")
    
    def save_conversation(self):
        """Save conversation to database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            for entry in self.conversation_context:
                if entry['speaker'] == 'user':
                    # Find corresponding JARVIS response
                    idx = self.conversation_context.index(entry)
                    jarvis_response = ""
                    if idx + 1 < len(self.conversation_context):
                        jarvis_response = self.conversation_context[idx + 1]['text']
                    
                    cursor.execute('''
                        INSERT INTO conversations (user_input, jarvis_response, context, timestamp)
                        VALUES (?, ?, ?, ?)
                    ''', (entry['text'], jarvis_response, self.current_topic or "", entry['timestamp']))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Error saving conversation: {e}")
    
    def run(self):
        """Main conversational loop"""
        print("\n" + "="*70)
        print("🤖 JARVIS CONVERSATIONAL AI ACTIVATED")
        print("="*70)
        print("Have natural conversations with JARVIS!")
        print("JARVIS will talk with you, understand context, and work together.")
        print("Say 'exit' to quit")
        print("="*70 + "\n")
        
        # Greet user
        self.greet_user()
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                # Listen to user
                user_input = self.listen()
                
                if user_input:
                    # Process conversation
                    if not self.process_conversation(user_input):
                        # User wants to exit
                        if self.user_name:
                            self.speak(f"Goodbye, {self.user_name}! It was great talking with you.")
                        else:
                            self.speak("Goodbye! It was nice talking with you.")
                        
                        self.speak("Feel free to come back anytime!")
                        
                        # Save conversation
                        self.save_conversation()
                        break
                
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n\n👋 Conversation ended by user")
                if self.user_name:
                    self.speak(f"Goodbye, {self.user_name}!")
                else:
                    self.speak("Goodbye!")
                self.save_conversation()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue


def main():
    """Main function"""
    print("\n" + "="*70)
    print("🤖 JARVIS CONVERSATIONAL AI")
    print("="*70)
    print("\nFeatures:")
    print("✓ Natural conversations")
    print("✓ Context awareness")
    print("✓ Remembers your name and preferences")
    print("✓ Asks follow-up questions")
    print("✓ Works together with you")
    print("✓ Saves conversation history")
    print("="*70 + "\n")
    
    try:
        jarvis = JarvisConversational()
        jarvis.run()
    except Exception as e:
        print(f"\n❌ Error starting JARVIS: {e}")
        print("\n💡 Make sure required packages are installed:")
        print("   pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4")


if __name__ == "__main__":
    main()
