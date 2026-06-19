"""
JARVIS VOICE RECOGNITION
Voice-to-Text with Natural Language Processing

This module provides voice recognition for JARVIS.
এই module JARVIS এর জন্য voice recognition প্রদান করে।

Features:
- Real-time voice recognition
- Multi-language support (Bengali + English)
- Noise cancellation
- Continuous listening
- Wake word detection
"""

import speech_recognition as sr
import threading
import time
from typing import Optional, Callable
import queue


class VoiceRecognition:
    """Voice recognition system for JARVIS"""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.callback = callback
        self.audio_queue = queue.Queue()
        self.listen_thread = None
        
        # Wake words
        self.wake_words = ["jarvis", "hey jarvis", "ok jarvis", "জার্ভিস"]
        self.wake_word_enabled = False
        
        # Settings
        self.language = "bn-BD"  # Default Bangla
        self.energy_threshold = 4000
        self.pause_threshold = 2.0
        
        # Initialize microphone
        self._init_microphone()
    
    def _init_microphone(self):
        """Initialize microphone"""
        try:
            self.microphone = None
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    pass
            except Exception as e:
                print(f"⚠️ Default mic failed: {e}. Searching for working mic index...")
                try:
                    mics = sr.Microphone.list_microphone_names()
                    for idx, name in enumerate(mics):
                        name_lower = name.lower()
                        if "microphone" in name_lower or "mic" in name_lower or "input" in name_lower:
                            try:
                                test_mic = sr.Microphone(device_index=idx)
                                with test_mic:
                                    self.microphone = test_mic
                                    print(f"✅ Bound to microphone index {idx}: {name}")
                                    break
                            except:
                                continue
                except Exception as le:
                    print(f"❌ Failed listing microphones: {le}")
            
            if not self.microphone:
                print("❌ No working microphone found")
                return False
                
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Microphone initialization failed: {e}")
            return False
    
    def set_language(self, language: str):
        """
        Set recognition language
        
        Args:
            language: Language code (e.g., 'en-US', 'bn-BD')
        """
        self.language = language
        print(f"✅ Language set to: {language}")
    
    def set_callback(self, callback: Callable):
        """Set callback function for recognized text"""
        self.callback = callback
    
    def enable_wake_word(self, enabled: bool = True):
        """Enable/disable wake word detection"""
        self.wake_word_enabled = enabled
        print(f"✅ Wake word {'enabled' if enabled else 'disabled'}")
    
    def listen_once(self) -> Optional[str]:
        """
        Listen for a single command
        
        Returns:
            Recognized text or None
        """
        if not self.microphone:
            print("❌ Microphone not available")
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=20)
                
            print("🔄 Processing...")
            
            # Try Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"✅ Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"❌ Recognition service error: {e}")
                # Fallback to offline recognition
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    print(f"✅ Recognized (offline): {text}")
                    return text
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    return None
                    
        except Exception as e:
            print(f"❌ Listen error: {e}")
            return None
    
    def start_continuous_listening(self):
        """Start continuous listening in background"""
        if self.is_listening:
            print("⚠️ Already listening")
            return
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._continuous_listen, daemon=True)
        self.listen_thread.start()
        print("✅ Continuous listening started")
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("✅ Continuous listening stopped")
    
    def _continuous_listen(self):
        """Continuous listening loop"""
        if not self.microphone:
            print("❌ Microphone not available")
            return
        
        with self.microphone as source:
            while self.is_listening:
                try:
                    print("🎤 Listening (continuous)...")
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=20)
                    
                    # Process in background
                    threading.Thread(
                        target=self._process_audio,
                        args=(audio,),
                        daemon=True
                    ).start()
                    
                except Exception as e:
                    print(f"❌ Listen error: {e}")
                    time.sleep(1)
    
    def _process_audio(self, audio):
        """Process audio in background"""
        try:
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"✅ Recognized: {text}")
            
            # Check wake word if enabled
            if self.wake_word_enabled:
                text_lower = text.lower()
                if not any(wake_word in text_lower for wake_word in self.wake_words):
                    print("⏭️ Wake word not detected, ignoring")
                    return
                # Remove wake word from text
                for wake_word in self.wake_words:
                    text = text.replace(wake_word, "").replace(wake_word.title(), "").strip()
            
            # Call callback if set
            if self.callback and text:
                self.callback(text)
                
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
        except sr.RequestError as e:
            print(f"❌ Recognition service error: {e}")
        except Exception as e:
            print(f"❌ Process error: {e}")
    
    def test_microphone(self) -> bool:
        """Test if microphone is working"""
        print("🧪 Testing microphone...")
        
        if not self.microphone:
            print("❌ Microphone not initialized")
            return False
        
        try:
            with self.microphone as source:
                print("🎤 Say something...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=20)
                
            print("🔄 Processing...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"✅ Test successful! Recognized: {text}")
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    def get_available_microphones(self):
        """Get list of available microphones"""
        try:
            mics = sr.Microphone.list_microphone_names()
            print("🎤 Available microphones:")
            for i, mic in enumerate(mics):
                print(f"  {i}: {mic}")
            return mics
        except Exception as e:
            print(f"❌ Could not list microphones: {e}")
            return []
    
    def set_microphone(self, device_index: int):
        """Set microphone by device index"""
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"✅ Microphone set to device {device_index}")
            return True
        except Exception as e:
            print(f"❌ Could not set microphone: {e}")
            return False


# Test function
def test_voice_recognition():
    """Test voice recognition"""
    print("=" * 60)
    print("JARVIS VOICE RECOGNITION TEST")
    print("=" * 60)
    
    def on_recognized(text):
        print(f"📝 Callback received: {text}")
    
    # Create voice recognition
    vr = VoiceRecognition(callback=on_recognized)
    
    # Test 1: List microphones
    print("\n🧪 Test 1: List Microphones")
    vr.get_available_microphones()
    
    # Test 2: Test microphone
    print("\n🧪 Test 2: Test Microphone")
    vr.test_microphone()
    
    # Test 3: Listen once
    print("\n🧪 Test 3: Listen Once")
    text = vr.listen_once()
    if text:
        print(f"✅ Success: {text}")
    else:
        print("❌ Failed")
    
    # Test 4: Continuous listening (5 seconds)
    print("\n🧪 Test 4: Continuous Listening (5 seconds)")
    vr.start_continuous_listening()
    time.sleep(5)
    vr.stop_continuous_listening()
    
    print("\n" + "=" * 60)
    print("✅ All tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_voice_recognition()
