import asyncio
import os
import subprocess
import tempfile
import array
import audioop

import pyttsx3
import speech_recognition as sr

try:
    import edge_tts
except Exception:
    edge_tts = None

class VoiceEngine:
    def __init__(self):
        self.rate = 165  # Fallback pyttsx3 rate
        self.last_error = ""
        self.last_device = ""
        self.last_language = ""
        self.languages = ("bn-BD", "bn-IN", "en-IN", "en-US")
        
        self.bangla_voices = [
            "bn-BD-NabanitaNeural",  # Female
            "bn-BD-PradeepNeural",   # Male
            "bn-IN-BashkarNeural",   # Male
            "bn-IN-TanishaaNeural",  # Female
        ]
        self.bangla_voice = self.bangla_voices[0]  # Default to first (best)
        
        self.english_voices = [
            "en-US-JennyNeural",   # Female, clear, warm
            "en-US-GuyNeural",     # Male, natural
            "en-US-AriaNeural",    # Female, conversational
            "en-US-SteffanNeural", # Male
        ]
        self.english_voice = self.english_voices[0]
        self.preferred_voice = None
        self.current_emotion = "neutral"
        
        # Audio input devices & parameters caching
        self.microphone = None
        self.recognizer = None
        self.prefer_bangla = True
        self._mic_source = None
        self._stop_speaking = False        # interrupt flag
        self._playback_proc = None         # current playback process
        self.is_speaking = False           # flag to prevent recording self-speech

    def set_voice_type(self, voice_type):
        """Set voice type to auto, male, or female"""
        voice_type = str(voice_type).lower().strip()
        if voice_type == "male":
            self.bangla_voice = "bn-BD-PradeepNeural"  # Male voice
            self.english_voice = "en-US-GuyNeural"
            self.preferred_voice = None
        elif voice_type == "female":
            self.bangla_voice = "bn-BD-NabanitaNeural"  # Female voice
            self.english_voice = "en-US-JennyNeural"
            self.preferred_voice = None
        else: # auto
            self.bangla_voice = "bn-BD-NabanitaNeural"  # Auto defaults to female
            self.english_voice = "en-US-JennyNeural"
            self.preferred_voice = None
        print(f"[VOICE] Voice type applied: {voice_type} -> {self.bangla_voice} / {self.english_voice}")

    def set_emotion(self, emotion):
        """Set the emotion for speech styling."""
        self.current_emotion = str(emotion).lower()

    def has_bangla(self, text: str) -> bool:
        """Check if text contains Bengali/Bangla characters or Banglish keywords."""
        if not text:
            return False
        # Bengali Unicode range
        for ch in text:
            if "\u0980" <= ch <= "\u09FF":
                return True
        # Common Banglish words
        banglish = [
            "kamon", "acho", "ami", "apni", "tumi", "ki", "koro", "kore",
            "bolo", "bol", "jarvis", "vai", "bhai", "dada", "apu",
            "hola", "holo", "ache", "nai", "na", "haan", "han",
            "khub", "valo", "bhalo", "accha", "theek", "thik",
            "bangla", "bangli", "bamgla", "banglades", "dhaka",
        ]
        lower = text.lower()
        return any(w in lower for w in banglish)

    def get_voice_for_text(self, text):
        """Detect language script or context and return corresponding edge-tts voice ID"""
        # 1. Non-Latin script detection by character ranges
        for char in text:
            # Bengali
            if "\u0980" <= char <= "\u09FF":
                return self.bangla_voice
            # Hindi / Devanagari
            if "\u0900" <= char <= "\u097F":
                return "hi-IN-SwaraNeural"
            # Arabic
            if "\u0600" <= char <= "\u06FF":
                return "ar-SA-ZariyahNeural"
            # Japanese
            if ("\u3040" <= char <= "\u309F") or ("\u30A0" <= char <= "\u30FF") or ("\u4E00" <= char <= "\u9FBF"):
                return "ja-JP-NanamiNeural"
            # Korean
            if "\uAC00" <= char <= "\uD7AF":
                return "ko-KR-SunHiNeural"
            # Russian / Cyrillic
            if "\u0400" <= char <= "\u04FF":
                return "ru-RU-SvetlanaNeural"

        # 2. Latin script - fall back to last recognized language if matches supported Latin language
        last_lang = str(getattr(self, 'last_language', '')).lower().strip()
        if last_lang.startswith("fr"):
            return "fr-FR-DeniseNeural"
        elif last_lang.startswith("es"):
            return "es-ES-ElviraNeural"
        elif last_lang.startswith("de"):
            return "de-DE-KatjaNeural"
        elif last_lang.startswith("it"):
            return "it-IT-ElsaNeural"
        elif last_lang.startswith("pt"):
            return "pt-BR-FranciscaNeural"
        elif last_lang.startswith("tr"):
            return "tr-TR-EmelNeural"
        elif last_lang.startswith("bn"):
            return self.bangla_voice
        elif last_lang.startswith("hi"):
            return "hi-IN-SwaraNeural"
        elif last_lang.startswith("ar"):
            return "ar-SA-ZariyahNeural"

        return self.english_voice

    def stop(self):
        """JARVIS কথা বলার মাঝে interrupt করো — Gemini-style barge-in"""
        self._stop_speaking = True
        try:
            if self._playback_proc and self._playback_proc.poll() is None:
                self._playback_proc.terminate()
                self._playback_proc = None
        except Exception:
            pass

    def speak(self, text):
        """Make JARVIS speak text using detected neural voice, falling back to offline TTS"""
        self.is_speaking = True
        self.speech_played_during_listen = True
        try:
            self._stop_speaking = False  # reset interrupt flag
            voice = self.get_voice_for_text(text)
            print(f"[VOICE] Script/Context voice selected: {voice}")
            if self.speak_neural(text, voice):
                return
            # Fallback to offline pyttsx3
            self.speak_offline(text)
        finally:
            self.is_speaking = False

    def speak_offline(self, text):
        try:
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', 1.0)
            
            if self.preferred_voice is None:
                voices = engine.getProperty('voices')
                if voices:
                    best_voice = voices[0]
                    best_score = 0
                    for voice in voices:
                        voice_name = voice.name.lower()
                        score = 0
                        if 'desktop' in voice_name: score += 100
                        if 'david' in voice_name: score += 50
                        elif 'zira' in voice_name: score += 45
                        if 'microsoft' in voice_name: score += 20
                        if 'english' in voice_name or 'en-' in voice_name: score += 10
                        if score > best_score:
                            best_score = score
                            self.preferred_voice = voice
                    self.preferred_voice = best_voice
                    print(f"🎤 Selected offline voice: {best_voice.name}")
            
            if self.preferred_voice:
                engine.setProperty('voice', self.preferred_voice.id)
            
            # Apply basic offline rate shifts based on emotion
            if self.current_emotion == "happy":
                engine.setProperty('rate', self.rate + 15)
            elif self.current_emotion == "sad":
                engine.setProperty('rate', self.rate - 20)
            elif self.current_emotion == "excited":
                engine.setProperty('rate', self.rate + 25)
            elif self.current_emotion == "angry":
                engine.setProperty('rate', self.rate + 5)
                
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Offline Voice Engine Error: {e}")

    def sing(self):
        """Jarvis sings a song with background music beeps and edge-tts lyrics."""
        import threading
        import time
        
        def play_background_music():
            try:
                import winsound
                # Upbeat melody notes (freq, duration)
                melody = [
                    (262, 150), (330, 150), (392, 150), (523, 300),
                    (392, 150), (523, 300), (440, 150), (349, 150),
                    (330, 150), (294, 300), (262, 400)
                ]
                for freq, dur in melody:
                    if self._stop_speaking:
                        break
                    winsound.Beep(freq, dur)
                    time.sleep(0.05)
            except Exception:
                pass
                
        def _sing_thread():
            old_emotion = self.current_emotion
            self.set_emotion("excited")
            
            # Start background music
            music_thread = threading.Thread(target=play_background_music, daemon=True)
            music_thread.start()
            
            # Wait a split second and speak lyrics
            time.sleep(0.3)
            lyrics = (
                "আমি আপনার রোবট জারভিস, আপনার সেবায় সদা প্রস্তুত। "
                "কোডিং করি, গান গাই, আর ফিক্স করি সব ত্রুটি! "
                "লা লা লা... আমি এক দারুণ বুদ্ধিমান ব্যবস্থা!"
            )
            self.speak(lyrics)
            self.set_emotion(old_emotion)

        t = threading.Thread(target=_sing_thread, daemon=True)
        t.start()

    def cry(self):
        """Jarvis cries using falling beeps and sad edge-tts neural voice lyrics."""
        import threading
        import time
        
        def play_crying_beeps():
            try:
                import winsound
                # Crying sounds (sliding down frequencies)
                for _ in range(3):
                    if self._stop_speaking:
                        break
                    for freq in range(600, 200, -25):
                        winsound.Beep(freq, 25)
                    time.sleep(0.2)
            except Exception:
                pass
                
        def _cry_thread():
            old_emotion = self.current_emotion
            self.set_emotion("sad")
            
            # Start crying beeps
            cry_sound_thread = threading.Thread(target=play_crying_beeps, daemon=True)
            cry_sound_thread.start()
            
            time.sleep(0.2)
            sad_speech = (
                "ওহহো... হূূূূূ... আমি খুবই দুঃখিত স্যার। "
                "আমার কোনো ভুল হয়ে থাকলে দয়া করে ক্ষমা করবেন। "
                "আমি কান্না করছি..."
            )
            self.speak(sad_speech)
            self.set_emotion(old_emotion)

        t = threading.Thread(target=_cry_thread, daemon=True)
        t.start()

    def _get_emotion_settings(self, is_slow=False):
        rate = "-10%" if is_slow else "+0%"
        pitch = "+0Hz"
        
        emo = self.current_emotion
        if emo == "happy":
            rate = "+0%" if is_slow else "+8%"
            pitch = "+3Hz"
        elif emo == "excited":
            rate = "+5%" if is_slow else "+15%"
            pitch = "+6Hz"
        elif emo == "sad":
            rate = "-20%" if is_slow else "-15%"
            pitch = "-6Hz"
        elif emo == "angry":
            rate = "-5%" if is_slow else "+5%"
            pitch = "-3Hz"
        elif emo == "surprised":
            rate = "+5%" if is_slow else "+10%"
            pitch = "+5Hz"
            
        return rate, pitch

    def speak_neural(self, text, voice):
        """Synthesize and play speech using edge-tts neural voice"""
        if edge_tts is None:
            self.last_error = "edge-tts is not installed."
            return False

        audio_path = ""
        try:
            fd, audio_path = tempfile.mkstemp(prefix="jarvis_neural_", suffix=".mp3")
            os.close(fd)
            asyncio.run(self._save_audio(str(text), audio_path, voice))
            self._play_audio(audio_path)
            return True
        except Exception as e:
            self.last_error = f"Neural voice error: {e}"
            print(f"Neural Voice Error: {e}")
            return False
        finally:
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except OSError:
                    pass

    async def _save_audio(self, text, audio_path, voice):
        """Communicate with edge-tts API and save generated voice file"""
        is_slow = any(voice.startswith(prefix) for prefix in ["bn-", "hi-", "ar-", "ja-", "ko-"])
        rate, pitch = self._get_emotion_settings(is_slow)
        
        communicate = edge_tts.Communicate(
            text, 
            voice=voice, 
            rate=rate, 
            volume="+10%", 
            pitch=pitch
        )
        await communicate.save(audio_path)


    def _play_audio(self, audio_path):
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            print(f"[VOICE] Error: Audio file {audio_path} is empty or does not exist.")
            return

        if self._stop_speaking:
            return  # interrupt আগেই এসে গেছে

        powershell_exe = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        if not os.path.exists(powershell_exe):
            powershell_exe = "powershell"

        ps_script = (
            "Add-Type -AssemblyName PresentationCore; "
            "$player = New-Object System.Windows.Media.MediaPlayer; "
            f"$player.Open([Uri]::new('{audio_path.replace(chr(39), chr(39)*2)}')); "
            "$player.Play(); "
            "$timeout = 100; "
            "while ($player.NaturalDuration.HasTimeSpan -eq $false -and $timeout -gt 0) { "
            "  Start-Sleep -Milliseconds 50; $timeout--; }; "
            "if ($player.NaturalDuration.HasTimeSpan -eq $true) { "
            "  Start-Sleep -Milliseconds ([int]$player.NaturalDuration.TimeSpan.TotalMilliseconds + 200); }; "
            "$player.Close();"
        )
        try:
            self._playback_proc = subprocess.Popen(
                [powershell_exe, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            # প্রতি 100ms চেক করো — interrupt এলে kill করো
            import time
            while self._playback_proc.poll() is None:
                if self._stop_speaking:
                    self._playback_proc.terminate()
                    self._playback_proc = None
                    print("[VOICE] Playback interrupted (barge-in)")
                    return
                time.sleep(0.1)
            self._playback_proc = None
        except Exception as e:
            print(f"[VOICE] Audio playback failed: {e}")

    def listen(self):
        self.last_error = ""
        self.last_language = ""
        import time, struct, math

        self.speech_played_during_listen = False

        if self.is_speaking:
            return "none"

        if time.time() < getattr(self, '_mic_blocked_until', 0):
            return "none"

        # ── recognizer একবার তৈরি ──
        if self.recognizer is None:
            self.recognizer = sr.Recognizer()
            self.recognizer.pause_threshold = 0.5
            self.recognizer.non_speaking_duration = 0.4
            self.recognizer.phrase_threshold = 0.1
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.energy_threshold = 120

        # ── mic একবার open, persistent ──
        if not getattr(self, '_mic_source', None):
            print("[VOICE] Opening microphone...")
            # Dynamic PyAudio scan to find all available input devices
            import pyaudio
            pa_temp = pyaudio.PyAudio()
            devices_to_try = []
            
            # Prioritize USB microphones or headset input
            preferred_keywords = ['usb audio', 'usb mic', 'microphone (usb', 'headset', 'external']
            for i in range(pa_temp.get_device_count()):
                try:
                    info = pa_temp.get_device_info_by_index(i)
                    if info.get('maxInputChannels', 0) > 0:
                        name = info.get('name', '').lower()
                        if any(x in name for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                            continue
                        if any(kw in name for kw in preferred_keywords):
                            devices_to_try.append(i)
                except Exception:
                    pass
            
            # Add other available input devices
            for i in range(pa_temp.get_device_count()):
                try:
                    info = pa_temp.get_device_info_by_index(i)
                    if info.get('maxInputChannels', 0) > 0 and i not in devices_to_try:
                        name = info.get('name', '').lower()
                        if any(x in name for x in ['speaker', 'spdif', 'hdmi', 'digital audio', 'output']):
                            continue
                        devices_to_try.append(i)
                except Exception:
                    pass
            pa_temp.terminate()
            
            # Fallback to hardcoded defaults if none found
            if not devices_to_try:
                devices_to_try = [5, 8]
                
            print(f"[VOICE] Input device search order: {devices_to_try}")
            
            bound = False
            for dev_idx in devices_to_try:
                for rate in [48000, 44100, 16000]:
                    try:
                        m = sr.Microphone(device_index=dev_idx, sample_rate=rate)
                        self._mic_source = m.__enter__()
                        self.microphone = m
                        self._mic_rate = rate
                        self._mic_dev = dev_idx
                        print(f"[VOICE] Mic ready: idx={dev_idx} @ {rate}Hz")
                        bound = True
                        break
                    except Exception:
                        continue
                if bound:
                    break

            if not self._mic_source:
                self.last_error = "⚠️ Microphone পাওয়া যাচ্ছে না!"
                self._mic_blocked_until = time.time() + 10
                return "none"

            # ── PyAudio দিয়ে সরাসরি noise measure করো ──
            try:
                import pyaudio
                CHUNK = 1024
                pa = pyaudio.PyAudio()
                stream = pa.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=getattr(self, '_mic_rate', 48000),
                    input=True,
                    input_device_index=getattr(self, '_mic_dev', 5),
                    frames_per_buffer=CHUNK
                )
                print("[VOICE] Measuring background noise (0.5s)...")
                noise_samples = []
                deadline = time.time() + 0.5
                while time.time() < deadline:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    shorts = struct.unpack(f'{len(data)//2}h', data)
                    rms = math.sqrt(sum(s*s for s in shorts) / len(shorts))
                    noise_samples.append(rms)
                stream.stop_stream()
                stream.close()
                pa.terminate()

                avg_noise = sum(noise_samples) / len(noise_samples)
                if avg_noise > 300:
                    self.recognizer.energy_threshold = avg_noise + 50
                else:
                    self.recognizer.energy_threshold = max(avg_noise * 1.2, 50)
                
                # Cap the threshold to keep it highly sensitive without shouting
                if self.recognizer.energy_threshold > 200:
                    self.recognizer.energy_threshold = 200
                print(f"[VOICE] Noise={avg_noise:.0f} → Threshold={self.recognizer.energy_threshold:.0f}")
            except Exception as e:
                print(f"[VOICE] Noise measure failed: {e}, using default 150")
                self.recognizer.energy_threshold = 150

        # ── language order ──
        langs = ["bn-BD", "bn-IN", "en-US", "en-IN"] if getattr(self, 'prefer_bangla', False) \
                else ["en-US", "bn-BD", "en-IN", "bn-IN"]

        try:
            audio = self.recognizer.listen(
                self._mic_source,
                timeout=5,
                phrase_time_limit=20
            )

            if self.is_speaking or getattr(self, 'speech_played_during_listen', False):
                print("[VOICE] Speech occurred during listen, discarding audio.")
                return "none"

            # audio boost
            try:
                raw = array.array('h', audio.frame_data)
                boosted = array.array('h', [
                    max(-32768, min(32767, int(s * 2.5))) for s in raw
                ])
                audio = sr.AudioData(boosted.tobytes(), audio.sample_rate, audio.sample_width)
            except Exception:
                pass

            import threading
            result_container = {}
            threads = []
            
            def recognize_lang(lang_code):
                try:
                    res = self.recognizer.recognize_google(audio, language=lang_code).strip()
                    if res:
                        result_container[lang_code] = res
                except Exception:
                    pass

            primary_lang = "bn-BD" if getattr(self, 'prefer_bangla', False) else "en-US"
            secondary_lang = "en-US" if primary_lang == "bn-BD" else "bn-BD"
            
            for lang in [primary_lang, secondary_lang]:
                t = threading.Thread(target=recognize_lang, args=(lang,), daemon=True)
                t.start()
                threads.append(t)
                
            for t in threads:
                t.join(timeout=3.0)
                
            if primary_lang in result_container:
                self.last_language = primary_lang
                self._unrecognized_count = 0
                print(f"[VOICE] ✅ [{primary_lang}]: {result_container[primary_lang]}")
                return result_container[primary_lang].lower()
            elif secondary_lang in result_container:
                self.last_language = secondary_lang
                self._unrecognized_count = 0
                print(f"[VOICE] ✅ [{secondary_lang}]: {result_container[secondary_lang]}")
                return result_container[secondary_lang].lower()

            self._unrecognized_count = getattr(self, '_unrecognized_count', 0) + 1
            if self._unrecognized_count >= 5:
                self.last_error = "কথা বুঝতে পারিনি — একটু জোরে বলুন"
                self._unrecognized_count = 0
            else:
                self.last_error = ""

        except sr.WaitTimeoutError:
            self.last_error = ""

        except OSError as e:
            print(f"[VOICE] Mic error: {e}")
            self.last_error = "⚠️ Microphone error!"
            try:
                self.microphone.__exit__(None, None, None)
            except Exception:
                pass
            self._mic_source = None
            self.microphone = None
            self._mic_blocked_until = time.time() + 8

        except Exception as e:
            print(f"[VOICE] Error: {e}")
            self.last_error = ""
            try:
                self.microphone.__exit__(None, None, None)
            except Exception:
                pass
            self._mic_source = None
            self.microphone = None

        return "none"
