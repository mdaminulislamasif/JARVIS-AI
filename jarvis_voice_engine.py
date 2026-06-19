"""
JARVIS Voice Engine - Python Text-to-Speech
Better voice quality and clarity than browser TTS
"""

import pyttsx3
import sys
import time

class JarvisVoice:
    def __init__(self):
        """Initialize JARVIS voice engine"""
        self.engine = pyttsx3.init()
        self.setup_voice()
    
    def setup_voice(self):
        """Configure voice settings for JARVIS"""
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Try to find best male voice
        male_voice = None
        for voice in voices:
            if 'david' in voice.name.lower() or 'male' in voice.name.lower():
                male_voice = voice
                break
        
        # Set voice
        if male_voice:
            self.engine.setProperty('voice', male_voice.id)
            print(f"✅ JARVIS Voice: {male_voice.name}")
        else:
            # Use first available voice
            self.engine.setProperty('voice', voices[0].id)
            print(f"✅ JARVIS Voice: {voices[0].name}")
        
        # Voice settings for clarity
        self.engine.setProperty('rate', 150)    # Speed (slower = clearer)
        self.engine.setProperty('volume', 1.0)  # Volume (max)
    
    def speak(self, text):
        """Make JARVIS speak"""
        print(f"🔊 JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def greet(self):
        """JARVIS greeting"""
        greetings = [
            "Good day sir. All systems are operational.",
            "Welcome back. I have prepared everything for you.",
            "At your service sir. All features are unlocked.",
            "Systems online. Ready to assist you.",
            "Hello sir. All Antigravity protocols are active."
        ]
        import random
        greeting = random.choice(greetings)
        self.speak(greeting)
    
    def confirm_action(self, action):
        """Confirm button actions"""
        responses = {
            'premium': "Premium activated successfully sir.",
            'unlock': "All features unlocked sir.",
            'key': "License key generated sir.",
            'dark': "Dark mode activated sir.",
            'light': "Light mode activated sir.",
            'api': "API access granted sir.",
            'cloud': "Cloud storage enabled sir.",
            'team': "Team mode activated sir.",
            'backup': "Auto backup enabled sir.",
            'offline': "Offline mode enabled sir.",
            'analytics': "Analytics access granted sir."
        }
        
        message = responses.get(action, f"{action} completed sir.")
        self.speak(message)


def main():
    """Main function"""
    print("=" * 60)
    print("🤖 JARVIS Voice Engine - Python Edition")
    print("=" * 60)
    
    # Initialize JARVIS
    jarvis = JarvisVoice()
    
    if len(sys.argv) > 1:
        # Speak provided text
        text = ' '.join(sys.argv[1:])
        jarvis.speak(text)
    else:
        # Interactive mode
        print("\n✅ JARVIS Voice Engine Ready!")
        print("\nCommands:")
        print("  greet     - JARVIS greeting")
        print("  premium   - Confirm premium activation")
        print("  unlock    - Confirm features unlock")
        print("  key       - Confirm key generation")
        print("  dark      - Confirm dark mode")
        print("  light     - Confirm light mode")
        print("  api       - Confirm API access")
        print("  cloud     - Confirm cloud storage")
        print("  quit      - Exit")
        print("\nOr type any text for JARVIS to speak!")
        print("=" * 60)
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = input("\n🤖 JARVIS > ").strip().lower()
                
                if not user_input:
                    continue
                
                if user_input in ['quit', 'exit', 'q']:
                    jarvis.speak("Goodbye sir. Shutting down.")
                    break
                
                elif user_input == 'greet':
                    jarvis.greet()
                
                elif user_input in ['premium', 'unlock', 'key', 'dark', 'light', 
                                   'api', 'cloud', 'team', 'backup', 'offline', 'analytics']:
                    jarvis.confirm_action(user_input)
                
                else:
                    # Speak custom text
                    jarvis.speak(user_input)
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                jarvis.speak("Goodbye sir.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
