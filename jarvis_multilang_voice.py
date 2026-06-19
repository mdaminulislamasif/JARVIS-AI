"""
JARVIS MULTI-LANGUAGE VOICE ENGINE
====================================
Jarvis ekhon SHOB bhasha bujhbe!
বাংলা | English | Hindi | Arabic | এবং আরো অনেক ভাষা

How it works:
  - Google Speech Recognition supports 100+ languages
  - Auto-detects language OR tries multiple languages
  - Responds in the same language user spoke
  - Banglish (mix of Bangla + English) also supported
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
import os
import json
import time

# ─────────────────────────────────────────────────────────────────────────────
# SUPPORTED LANGUAGES  (Google STT language codes)
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGES = {
    "bn":    "bn-BD",   # বাংলা (Bangladesh)
    "bn-IN": "bn-IN",   # বাংলা (India/West Bengal)
    "en":    "en-US",   # English
    "hi":    "hi-IN",   # हिन्दी
    "ar":    "ar-SA",   # العربية
    "ur":    "ur-PK",   # اردو
    "fr":    "fr-FR",   # Français
    "de":    "de-DE",   # Deutsch
    "zh":    "zh-CN",   # 中文
    "es":    "es-ES",   # Español
    "pt":    "pt-BR",   # Português
    "ru":    "ru-RU",   # Русский
    "ja":    "ja-JP",   # 日本語
    "ko":    "ko-KR",   # 한국어
    "tr":    "tr-TR",   # Türkçe
    "id":    "id-ID",   # Bahasa Indonesia
    "ms":    "ms-MY",   # Bahasa Melayu
    "th":    "th-TH",   # ภาษาไทย
    "vi":    "vi-VN",   # Tiếng Việt
    "fa":    "fa-IR",   # فارسی
    "ta":    "ta-IN",   # தமிழ்
    "te":    "te-IN",   # తెలుగు
    "ml":    "ml-IN",   # മലയാളം
    "mr":    "mr-IN",   # मराठी
    "gu":    "gu-IN",   # ગુજરાતી
    "pa":    "pa-IN",   # ਪੰਜਾਬੀ
    "ne":    "ne-NP",   # नेपाली
    "si":    "si-LK",   # සිංහල
    "my":    "my-MM",   # မြန်မာဘာသာ
    "km":    "km-KH",   # ភាសាខ្មែរ
    "lo":    "lo-LA",   # ພາສາລາວ
    "sw":    "sw-KE",   # Kiswahili
    "yo":    "yo-NG",   # Yorùbá
    "am":    "am-ET",   # አማርኛ
    "so":    "so-SO",   # Soomaali
    "ha":    "ha-NG",   # Hausa
    "zu":    "zu-ZA",   # isiZulu
    "af":    "af-ZA",   # Afrikaans
    "sq":    "sq-AL",   # Shqip
    "hy":    "hy-AM",   # Հայերեն
    "az":    "az-AZ",   # Azərbaycan
    "eu":    "eu-ES",   # Euskara
    "be":    "be-BY",   # Беларуская
    "bs":    "bs-BA",   # Bosanski
    "bg":    "bg-BG",   # Български
    "ca":    "ca-ES",   # Català
    "hr":    "hr-HR",   # Hrvatski
    "cs":    "cs-CZ",   # Čeština
    "da":    "da-DK",   # Dansk
    "nl":    "nl-NL",   # Nederlands
    "et":    "et-EE",   # Eesti
    "fi":    "fi-FI",   # Suomi
    "gl":    "gl-ES",   # Galego
    "ka":    "ka-GE",   # ქართული
    "el":    "el-GR",   # Ελληνικά
    "hu":    "hu-HU",   # Magyar
    "is":    "is-IS",   # Íslenska
    "ga":    "ga-IE",   # Gaeilge
    "it":    "it-IT",   # Italiano
    "lv":    "lv-LV",   # Latviešu
    "lt":    "lt-LT",   # Lietuvių
    "mk":    "mk-MK",   # Македонски
    "mt":    "mt-MT",   # Malti
    "no":    "nb-NO",   # Norsk
    "pl":    "pl-PL",   # Polski
    "ro":    "ro-RO",   # Română
    "sr":    "sr-RS",   # Српски
    "sk":    "sk-SK",   # Slovenčina
    "sl":    "sl-SI",   # Slovenščina
    "sv":    "sv-SE",   # Svenska
    "uk":    "uk-UA",   # Українська
    "cy":    "cy-GB",   # Cymraeg
}

# ─────────────────────────────────────────────────────────────────────────────
# BANGLA KEYWORDS & RESPONSES
# ─────────────────────────────────────────────────────────────────────────────
BANGLA_GREETINGS = [
    "হ্যালো", "হেই", "হাই", "নমস্কার", "আস্সালামু আলাইকুম",
    "আলাইকুম", "সালাম", "কেমন আছেন", "কি খবর", "ভালো আছেন"
]

BANGLA_RESPONSES = {
    "greeting": [
        "হ্যালো! আমি জারভিস। কী সাহায্য করতে পারি?",
        "আস্সালামু আলাইকুম! আমি আপনার সেবায় প্রস্তুত।",
        "নমস্কার! আপনার কী দরকার?",
    ],
    "how_are_you": [
        "আমি দারুণ আছি! আপনি কেমন আছেন?",
        "আলহামদুলিল্লাহ! আমি ভালো আছি। আপনি?",
        "সব সিস্টেম চালু আছে। আপনি কেমন আছেন?",
    ],
    "thanks": [
        "আপনাকে স্বাগতম!",
        "সবসময় সেবায় আছি!",
        "আমার আনন্দ হলো সাহায্য করতে পেরে।",
    ],
    "time": "এখন সময় হলো {}",
    "date": "আজকের তারিখ হলো {}",
    "unknown": [
        "আমি বুঝতে পারিনি। আবার বলুন।",
        "দুঃখিত, একটু আবার বলবেন?",
        "আপনি কী বলছেন বুঝিনি।",
    ],
    "goodbye": [
        "আল্লাহ হাফেজ! আবার কথা হবে।",
        "বিদায়! ভালো থাকুন।",
        "আসলাম! আবার ডাকবেন।",
    ],
    "capabilities": (
        "আমি অনেক কিছু করতে পারি! "
        "ওয়েব সার্চ, ওয়েবসাইট খোলা, সময় ও তারিখ বলা, "
        "কম্পিউটার নিয়ন্ত্রণ, এবং আরো অনেক কিছু। "
        "কী করতে চান বলুন।"
    ),
}

BANGLA_SEARCH_WORDS   = ["খুঁজুন", "সার্চ", "খোঁজো", "দেখাও", "বলো"]
BANGLA_OPEN_WORDS     = ["খোলো", "চালু", "শুরু", "ওপেন"]
BANGLA_TIME_WORDS     = ["সময়", "টাইম", "ঘড়ি", "কটা বাজে"]
BANGLA_DATE_WORDS     = ["তারিখ", "আজকে", "আজ", "কত তারিখ"]
BANGLA_WEATHER_WORDS  = ["আবহাওয়া", "মৌসুম", "বৃষ্টি", "রোদ", "ঠান্ডা"]
BANGLA_HELP_WORDS     = ["সাহায্য", "হেল্প", "কী পারো", "কী করতে পারো"]
BANGLA_STOP_WORDS     = ["বাই", "বিদায়", "যাও", "থামো", "বন্ধ", "আল্লাহ হাফেজ"]

# Priority order: try Bengali first, then English
DEFAULT_LANG_ORDER = ["bn-BD", "en-US", "hi-IN"]


# ─────────────────────────────────────────────────────────────────────────────
class JarvisMultiLangVoice:
    """
    Drop-in replacement / wrapper for speech recognition in JARVIS.
    Supports 100+ languages — tries Bengali first, then English.
    """

    def __init__(self, preferred_lang="bn-BD", fallback_langs=None, mic_index=None):
        self.preferred_lang  = preferred_lang
        self.fallback_langs  = fallback_langs or ["en-US", "hi-IN"]
        self.recognizer      = sr.Recognizer()
        self.recognizer.energy_threshold = 100
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.2
        self.mic_index       = mic_index or self._load_mic_config()
        self.microphone      = self._init_mic()
        self.mic_muted       = False
        self.detected_lang   = preferred_lang  # last detected language
        self.auto_detect     = True            # try multiple langs
        self._calibrated     = False

        print(f"🌐 Multi-Language Voice Engine READY")
        print(f"   Primary Language : {preferred_lang}")
        print(f"   Fallback         : {self.fallback_langs}")
        print(f"   Microphone       : {self._mic_name()}")

    # ── MICROPHONE SETUP ──────────────────────────────────────────────────────
    def _load_mic_config(self):
        """Load phone mic index from jarvis_mic_config.json if present."""
        # Bypassed to prioritize PC local microphone over phone mic as requested
        # cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                         "jarvis_mic_config.json")
        # if os.path.exists(cfg_path):
        #     try:
        #         with open(cfg_path) as f:
        #             cfg = json.load(f)
        #         idx = cfg.get("phone_mic_index")
        #         if idx is not None:
        #             print(f"   [PHONE MIC CONFIG] Using index {idx}")
        #             return idx
        #     except Exception:
        #         pass

        # Auto-detect USB mic
        mics = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mics):
            n = name.lower()
            if any(k in n for k in ["usb audio", "usb mic", "microphone (usb", "headset", "external"]):
                if not any(bad in n for bad in ["speaker", "spdif", "hdmi", "output"]):
                    print(f"   [AUTO MIC] Selected: [{i}] {name}")
                    return i
        print("   [DEFAULT MIC] Using system default")
        return None

    def _init_mic(self):
        if self.mic_index is not None:
            return sr.Microphone(device_index=self.mic_index)
        return sr.Microphone()

    def _mic_name(self):
        mics = sr.Microphone.list_microphone_names()
        if self.mic_index is not None and self.mic_index < len(mics):
            return mics[self.mic_index]
        return "System Default"

    # ── CALIBRATION ───────────────────────────────────────────────────────────
    def calibrate(self, duration=1.0):
        """Calibrate for ambient noise once."""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
            self._calibrated = True
            
            # Capping threshold to prevent it from going too high under ambient noise
            # or too low on silent inputs.
            if self.recognizer.energy_threshold > 200:
                print(f"   [CALIBRATION] Cap threshold: {self.recognizer.energy_threshold:.0f} -> 200")
                self.recognizer.energy_threshold = 200
            elif self.recognizer.energy_threshold < 30:
                print(f"   [CALIBRATION] Floor threshold: {self.recognizer.energy_threshold:.0f} -> 30")
                self.recognizer.energy_threshold = 30
            else:
                print(f"   [CALIBRATED] Energy threshold: {self.recognizer.energy_threshold:.0f}")
                
            # Run quick silent check
            self.check_and_recover_silent_mic()
            
        except Exception as e:
            print(f"   [CALIB ERR] {e}")

    def check_and_recover_silent_mic(self):
        """Quick check if current mic is silent. If so, scan for alternative active mic."""
        try:
            import pyaudio
            import numpy as np
            
            idx = self.mic_index if self.mic_index is not None else 0
            pa = pyaudio.PyAudio()
            try:
                info = pa.get_device_info_by_index(idx)
                rate = int(info['defaultSampleRate'])
                stream = pa.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    input_device_index=idx,
                    frames_per_buffer=1024
                )
                
                # Capture a few chunks
                amplitudes = []
                for _ in range(8):
                    data = stream.read(1024, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    amplitudes.append(np.max(np.abs(audio_data)))
                    
                stream.stop_stream()
                stream.close()
                
                peak = max(amplitudes)
                avg = sum(amplitudes) / len(amplitudes)
                
                # Check for dead/silent line (peak < 400 or flatline variance < 50)
                if peak < 400 or (peak - avg) < 50:
                    print(f"   ⚠️  [SILENT MIC WARNING] Mic index {idx} ({info['name']}) is silent (Peak: {peak}, Avg: {avg:.1f}).")
                    print("       Auto-scanning for active microphone inputs...")
                    self.auto_detect_active_microphone()
            except Exception as e:
                print(f"   ⚠️  Error querying mic level: {e}. Auto-scanning for active microphone inputs...")
                self.auto_detect_active_microphone()
            finally:
                pa.terminate()
        except ImportError:
            pass

    def auto_detect_active_microphone(self):
        """Scan all input devices and switch to the first one with active sound levels."""
        try:
            import pyaudio
            import numpy as np
            
            pa = pyaudio.PyAudio()
            best_idx = None
            best_peak = 0
            
            mics = sr.Microphone.list_microphone_names()
            for i in range(pa.get_device_count()):
                try:
                    info = pa.get_device_info_by_index(i)
                    if info['maxInputChannels'] > 0:
                        rate = int(info['defaultSampleRate'])
                        stream = pa.open(
                            format=pyaudio.paInt16,
                            channels=1,
                            rate=rate,
                            input=True,
                            input_device_index=i,
                            frames_per_buffer=512
                        )
                        
                        amplitudes = []
                        for _ in range(12):
                            data = stream.read(512, exception_on_overflow=False)
                            audio_data = np.frombuffer(data, dtype=np.int16)
                            amplitudes.append(np.max(np.abs(audio_data)))
                            
                        stream.stop_stream()
                        stream.close()
                        
                        peak = max(amplitudes)
                        avg = sum(amplitudes) / len(amplitudes)
                        variance = peak - avg
                        
                        # Real signal has high peak and significant variance from white noise/DC offset
                        if peak > 500 and variance > 100:
                            if peak > best_peak:
                                best_peak = peak
                                best_idx = i
                except Exception:
                    continue
            
            pa.terminate()
            
            if best_idx is not None:
                print(f"   🚀 [AUTO-RECOVERY] Switching to active microphone: [{best_idx}] {mics[best_idx]}")
                self.switch_mic(best_idx)
                # Calibrate the new mic
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Cap again
                if self.recognizer.energy_threshold > 200:
                    self.recognizer.energy_threshold = 200
                elif self.recognizer.energy_threshold < 30:
                    self.recognizer.energy_threshold = 30
                print(f"   🚀 [RE-CALIBRATED] Energy threshold for mic [{best_idx}] is {self.recognizer.energy_threshold:.0f}")
                return True
            else:
                print("   ❌ [AUTO-RECOVERY FAILED] No active microphone signal detected.")
                print("       Please check if the phone audio bridge (START_PHONE_MIC_BRIDGE.bat) is running,")
                print("       or if your USB microphone is muted in Windows / hardware.")
                return False
        except Exception as e:
            print(f"   [RECOVERY ERROR] {e}")
            return False

    # ── CORE LISTEN ───────────────────────────────────────────────────────────
    def listen(self, timeout=8, phrase_limit=15):
        """
        Listen and return (text, detected_language_code).
        Tries preferred language first, then fallbacks.
        Returns (None, None) on failure.
        """
        if self.mic_muted:
            print("🔇 Mic MUTED — skipping listen")
            return None, None

        if not self._calibrated:
            self.calibrate(duration=0.5)

        try:
            with self.microphone as source:
                print("\n🎤 শুনছি... (বাংলায় বলুন বা English-এ)")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
        except sr.WaitTimeoutError:
            return None, None
        except OSError as e:
            print(f"⚠️ Mic error: {e} — Reinitializing...")
            self.mic_index  = self._load_mic_config()
            self.microphone = self._init_mic()
            return None, None

        # Try preferred language first
        langs_to_try = [self.preferred_lang] + [
            l for l in self.fallback_langs if l != self.preferred_lang
        ]

        for lang_code in langs_to_try:
            try:
                text = self.recognizer.recognize_google(audio, language=lang_code)
                if text:
                    self.detected_lang = lang_code
                    lang_label = self._lang_label(lang_code)
                    print(f"✅ [{lang_label}] আপনি বললেন: {text}")
                    return text.strip(), lang_code
            except sr.UnknownValueError:
                continue   # try next language
            except sr.RequestError as e:
                print(f"⚠️ Google STT error ({lang_code}): {e}")
                break

        print("❓ কথা বোঝা যায়নি। আবার বলুন।")
        return None, None

    def listen_bangla(self, timeout=8, phrase_limit=15):
        """Listen specifically for Bangla only."""
        if self.mic_muted:
            return None

        if not self._calibrated:
            self.calibrate(0.5)

        try:
            with self.microphone as source:
                print("\n🎤 বাংলায় বলুন...")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
            text = self.recognizer.recognize_google(audio, language="bn-BD")
            print(f"✅ [বাংলা] {text}")
            return text.strip()
        except sr.UnknownValueError:
            print("❓ বোঝা যায়নি।")
            return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return None

    def listen_english(self, timeout=8, phrase_limit=15):
        """Listen specifically for English only."""
        if self.mic_muted:
            return None

        if not self._calibrated:
            self.calibrate(0.5)

        try:
            with self.microphone as source:
                print("\n🎤 Listening (English)...")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
            text = self.recognizer.recognize_google(audio, language="en-US")
            print(f"✅ [English] {text}")
            return text.strip()
        except sr.UnknownValueError:
            print("❓ Could not understand.")
            return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return None

    def listen_any_language(self, lang_code, timeout=8, phrase_limit=15):
        """Listen in any specific language by code (e.g. 'hi-IN', 'ar-SA')."""
        if self.mic_muted:
            return None

        if not self._calibrated:
            self.calibrate(0.5)

        try:
            with self.microphone as source:
                print(f"\n🎤 Listening [{lang_code}]...")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
            text = self.recognizer.recognize_google(audio, language=lang_code)
            print(f"✅ [{lang_code}] {text}")
            return text.strip()
        except sr.UnknownValueError:
            return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return None

    # ── LANGUAGE HELPERS ──────────────────────────────────────────────────────
    def _lang_label(self, code):
        labels = {
            "bn-BD": "বাংলা",
            "bn-IN": "বাংলা(ভারত)",
            "en-US": "English",
            "hi-IN": "हिन्दी",
            "ar-SA": "عربي",
            "ur-PK": "اردو",
            "fr-FR": "Français",
            "de-DE": "Deutsch",
            "zh-CN": "中文",
            "es-ES": "Español",
        }
        return labels.get(code, code)

    def set_language(self, lang_key):
        """Change primary language. Accept short codes like 'bn', 'en', 'hi'."""
        if lang_key in LANGUAGES:
            self.preferred_lang = LANGUAGES[lang_key]
            print(f"🌐 Language changed to: {self.preferred_lang}")
            return True
        if lang_key in LANGUAGES.values():
            self.preferred_lang = lang_key
            print(f"🌐 Language changed to: {self.preferred_lang}")
            return True
        return False

    def list_languages(self):
        """Return formatted list of all supported languages."""
        lines = ["🌐 Supported Languages:\n"]
        for key, code in LANGUAGES.items():
            lines.append(f"  {key:8s} → {code}")
        return "\n".join(lines)

    # ── BANGLA TEXT PROCESSING ────────────────────────────────────────────────
    def is_bangla(self, text):
        """Return True if text contains Bangla Unicode characters."""
        for ch in text:
            if "\u0980" <= ch <= "\u09FF":
                return True
        return False

    def process_bangla_command(self, text):
        """
        Understand Bangla command and return English action key.
        Returns dict: { 'action': str, 'query': str, 'response': str }
        """
        t = text.lower()

        # Greetings
        if any(w in t for w in BANGLA_GREETINGS):
            import random
            return {
                "action": "greeting",
                "query": text,
                "response": random.choice(BANGLA_RESPONSES["greeting"])
            }

        # Sing a song
        if any(w in t for w in ["গান গাও", "গান শোনাও", "গান গাইতে", "গান গা", "sing"]):
            return {
                "action": "sing",
                "query": text,
                "response": "আমি গান গাইছি..."
            }

        # Cry
        if any(w in t for w in ["কান্না করো", "কাঁদো", "কান্না কর", "cry", "crying"]):
            return {
                "action": "cry",
                "query": text,
                "response": "ওহহো... আমি কান্না করছি..."
            }

        # How are you
        if "কেমন আছ" in t or "কেমন আছেন" in t or "কি খবর" in t:
            import random
            return {
                "action": "how_are_you",
                "query": text,
                "response": random.choice(BANGLA_RESPONSES["how_are_you"])
            }

        # Thanks
        if any(w in t for w in ["ধন্যবাদ", "শুক্রিয়া", "থ্যাংকস"]):
            import random
            return {
                "action": "thanks",
                "query": text,
                "response": random.choice(BANGLA_RESPONSES["thanks"])
            }

        # Time
        if any(w in t for w in BANGLA_TIME_WORDS):
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            return {
                "action": "time",
                "query": text,
                "response": BANGLA_RESPONSES["time"].format(current_time)
            }

        # Date
        if any(w in t for w in BANGLA_DATE_WORDS):
            from datetime import datetime
            current_date = datetime.now().strftime("%d %B, %Y")
            return {
                "action": "date",
                "query": text,
                "response": BANGLA_RESPONSES["date"].format(current_date)
            }

        # Weather
        if any(w in t for w in BANGLA_WEATHER_WORDS):
            return {
                "action": "weather",
                "query": text,
                "response": "আবহাওয়া দেখাচ্ছি..."
            }

        # Search
        if any(w in t for w in BANGLA_SEARCH_WORDS):
            query = t
            for w in BANGLA_SEARCH_WORDS:
                query = query.replace(w, "").strip()
            return {
                "action": "search",
                "query": query or text,
                "response": f"{query} সার্চ করছি..."
            }

        # Open / launch
        if any(w in t for w in BANGLA_OPEN_WORDS):
            target = t
            for w in BANGLA_OPEN_WORDS:
                target = target.replace(w, "").strip()
            return {
                "action": "open",
                "query": target or text,
                "response": f"{target} খুলছি..."
            }

        # Help
        if any(w in t for w in BANGLA_HELP_WORDS):
            return {
                "action": "help",
                "query": text,
                "response": BANGLA_RESPONSES["capabilities"]
            }

        # Stop / bye
        if any(w in t for w in BANGLA_STOP_WORDS):
            import random
            return {
                "action": "goodbye",
                "query": text,
                "response": random.choice(BANGLA_RESPONSES["goodbye"])
            }

        # Unknown
        import random
        return {
            "action": "unknown",
            "query": text,
            "response": random.choice(BANGLA_RESPONSES["unknown"])
        }

    # ── MIC CONTROL ───────────────────────────────────────────────────────────
    def mute(self):
        self.mic_muted = True
        return "🔇 মাইক্রোফোন মিউট করা হয়েছে।"

    def unmute(self):
        self.mic_muted = False
        return "🎤 মাইক্রোফোন চালু করা হয়েছে।"

    def switch_mic(self, index):
        mics = sr.Microphone.list_microphone_names()
        if 0 <= index < len(mics):
            self.mic_index  = index
            self.microphone = sr.Microphone(device_index=index)
            return f"মাইক্রোফোন পরিবর্তন হয়েছে: {mics[index]}"
        return f"ভুল ইন্ডেক্স: {index}"

    def list_mics(self):
        mics = sr.Microphone.list_microphone_names()
        lines = ["🎤 Available Microphones:"]
        for i, m in enumerate(mics):
            mark = " ◄ ACTIVE" if i == self.mic_index else ""
            lines.append(f"  [{i}] {m}{mark}")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# PATCH: upgrade existing JarvisConversational to multi-lang
# ─────────────────────────────────────────────────────────────────────────────
def patch_jarvis_conversational():
    """
    Monkey-patch JarvisConversational.listen() to support multi-language.
    Call this ONCE after importing jarvis_conversational.
    """
    try:
        from jarvis_conversational import JarvisConversational

        _mlv = JarvisMultiLangVoice(preferred_lang="bn-BD", fallback_langs=["en-US", "hi-IN"])

        def _multilang_listen(self, timeout=8):
            """Patched listen: tries Bengali first, then English."""
            if self.mic_muted:
                print("🔇 Mic MUTED")
                return None

            text, lang = _mlv.listen(timeout=timeout, phrase_limit=15)
            if text:
                # Save to conversation context
                from datetime import datetime
                self.conversation_context.append({
                    "speaker": "user",
                    "text": text,
                    "timestamp": datetime.now(),
                    "language": lang,
                })
                # If Bangla, also process Bangla command
                if lang and lang.startswith("bn"):
                    result = _mlv.process_bangla_command(text)
                    if result["action"] != "unknown":
                        print(f"🇧🇩 Bangla command: {result['action']}")
                        self.speak(result["response"])
                        return "__BANGLA_HANDLED__"
            return text

        JarvisConversational.listen       = _multilang_listen
        JarvisConversational._mlv_engine  = _mlv
        print("✅ JarvisConversational patched with Multi-Language support!")
        return True
    except ImportError as e:
        print(f"⚠️ Could not patch JarvisConversational: {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# STANDALONE TEST
# ─────────────────────────────────────────────────────────────────────────────
def test_multilang():
    """Run a quick multi-language voice test."""
    print("\n" + "="*60)
    print("  🌐 JARVIS MULTI-LANGUAGE VOICE TEST")
    print("  বাংলায় বলুন অথবা English-এ বলুন")
    print("="*60)

    engine = JarvisMultiLangVoice(
        preferred_lang="bn-BD",
        fallback_langs=["en-US", "hi-IN"]
    )

    import pyttsx3 as _tts
    tts = _tts.init()
    tts.setProperty("rate", 140)
    tts.setProperty("volume", 1.0)

    def speak(text):
        print(f"🤖 JARVIS: {text}")
        try:
            tts.say(text)
            tts.runAndWait()
        except Exception:
            pass

    speak("হ্যালো! আমি জারভিস। বাংলায় বলুন অথবা English-এ বলুন। আমি সব বুঝব।")
    speak("Hello! I understand Bangla, English, Hindi and 100 more languages.")

    for i in range(10):
        print(f"\n--- Round {i+1}/10 ---")
        text, lang = engine.listen(timeout=10)

        if text is None:
            speak("কথা বোঝা যায়নি। আবার বলুন।")
            continue

        if lang and lang.startswith("bn"):
            result = engine.process_bangla_command(text)
            speak(result["response"])
            if result["action"] == "goodbye":
                break
        else:
            # English fallback echo
            speak(f"You said: {text}")

        if any(w in (text or "").lower() for w in ["exit", "quit", "stop", "bye"]):
            speak("বিদায়! আল্লাহ হাফেজ!")
            break


if __name__ == "__main__":
    test_multilang()
