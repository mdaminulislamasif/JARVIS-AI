"""
JARVIS Voice-Controlled Browser
Open websites and control browser using voice commands
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import time
from jarvis_browser_controller import JarvisBrowserController

class JarvisVoiceBrowser:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed
        self.engine.setProperty('volume', 1.0)  # Volume
        
        # Initialize browser controller
        self.browser = JarvisBrowserController()
        
        # Common websites
        self.websites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'reddit': 'https://www.reddit.com',
            'wikipedia': 'https://www.wikipedia.org',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'amazon': 'https://www.amazon.com',
            'netflix': 'https://www.netflix.com',
            'gmail': 'https://mail.google.com',
            'whatsapp': 'https://web.whatsapp.com',
            'tiktok': 'https://www.tiktok.com',
            'pinterest': 'https://www.pinterest.com',
            'tumblr': 'https://www.tumblr.com',
            'quora': 'https://www.quora.com',
            'medium': 'https://www.medium.com',
            'twitch': 'https://www.twitch.tv'
        }
        
        print("🎤 Initializing voice recognition...")
        self.adjust_for_ambient_noise()
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"🔊 JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def adjust_for_ambient_noise(self):
        """Adjust microphone for ambient noise"""
        try:
            with self.microphone as source:
                print("🎤 Adjusting for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("✅ Microphone ready!")
        except Exception as e:
            print(f"⚠️ Microphone setup warning: {e}")
    
    def listen(self):
        """Listen for voice command"""
        try:
            with self.microphone as source:
                print("\n🎤 Listening... (Speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("🔄 Processing...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"📝 You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            self.speak("Sorry, I didn't understand that")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            self.speak("Speech recognition service error")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def process_command(self, command):
        """Process voice command"""
        if not command:
            return True
            
        command = command.lower().strip()
        
        # Exit commands
        if any(word in command for word in ['exit', 'quit', 'stop', 'bye', 'goodbye']):
            self.speak("Goodbye! Voice browser deactivated.")
            return False
        
        # Help command
        if 'help' in command:
            self.show_help()
            return True
        
        # Open website commands
        if 'open' in command or 'go to' in command or 'visit' in command:
            self.handle_open_command(command)
            return True
        
        # Search commands
        if 'search' in command or 'find' in command or 'look for' in command:
            self.handle_search_command(command)
            return True
        
        # YouTube commands
        if 'youtube' in command or 'video' in command:
            self.handle_youtube_command(command)
            return True
        
        # Wikipedia commands
        if 'wikipedia' in command or 'wiki' in command:
            self.handle_wikipedia_command(command)
            return True
        
        # Social media commands
        if any(social in command for social in ['facebook', 'twitter', 'instagram', 'linkedin']):
            self.handle_social_command(command)
            return True
        
        # Learn command
        if 'learn' in command:
            self.speak("Learning mode activated")
            self.browser.get_learning_summary()
            return True
        
        # Summary command
        if 'summary' in command or 'status' in command:
            self.speak("Showing learning summary")
            self.browser.get_learning_summary()
            return True
        
        # Unknown command
        self.speak("I didn't understand that command. Say help for available commands.")
        return True
    
    def handle_open_command(self, command):
        """Handle open website commands"""
        # Remove command words
        for word in ['open', 'go to', 'visit', 'website', 'site']:
            command = command.replace(word, '').strip()
        
        # Check if it's a known website
        for site_name, url in self.websites.items():
            if site_name in command:
                self.speak(f"Opening {site_name}")
                self.browser.open_browser(url)
                return
        
        # Try to open as URL
        if command:
            if not command.startswith('http'):
                command = 'https://www.' + command.replace(' ', '') + '.com'
            self.speak(f"Opening {command}")
            self.browser.open_browser(command)
        else:
            self.speak("Please specify a website to open")
    
    def handle_search_command(self, command):
        """Handle search commands"""
        # Remove command words
        for word in ['search', 'search for', 'find', 'look for', 'google']:
            command = command.replace(word, '').strip()
        
        if command:
            self.speak(f"Searching for {command}")
            self.browser.search_google(command)
        else:
            self.speak("Please specify what to search for")
    
    def handle_youtube_command(self, command):
        """Handle YouTube commands"""
        # Remove command words
        for word in ['youtube', 'video', 'search', 'find', 'play', 'show me']:
            command = command.replace(word, '').strip()
        
        if command:
            self.speak(f"Searching YouTube for {command}")
            self.browser.search_youtube(command)
        else:
            self.speak("Opening YouTube")
            self.browser.open_browser('https://www.youtube.com')
    
    def handle_wikipedia_command(self, command):
        """Handle Wikipedia commands"""
        # Remove command words
        for word in ['wikipedia', 'wiki', 'search', 'find', 'about', 'what is']:
            command = command.replace(word, '').strip()
        
        if command:
            self.speak(f"Searching Wikipedia for {command}")
            self.browser.search_wikipedia(command)
        else:
            self.speak("Opening Wikipedia")
            self.browser.open_browser('https://www.wikipedia.org')
    
    def handle_social_command(self, command):
        """Handle social media commands"""
        for social in ['facebook', 'twitter', 'instagram', 'linkedin', 'reddit', 'tiktok']:
            if social in command:
                self.speak(f"Opening {social}")
                self.browser.open_social_media(social)
                return
    
    def show_help(self):
        """Show available commands"""
        help_text = """
        Available voice commands:
        
        Open websites:
        - Open Google
        - Go to YouTube
        - Visit Facebook
        - Open any website name
        
        Search:
        - Search for artificial intelligence
        - Find Python tutorials
        - Look for quantum computing
        
        YouTube:
        - YouTube Python tutorial
        - Play music video
        - Show me cooking videos
        
        Wikipedia:
        - Wikipedia artificial intelligence
        - What is quantum computing
        
        Social Media:
        - Open Facebook
        - Go to Twitter
        - Visit Instagram
        
        Other:
        - Summary (show learning stats)
        - Help (show this help)
        - Exit (quit voice browser)
        """
        
        print(help_text)
        self.speak("Available commands displayed on screen")
    
    def run(self):
        """Main voice browser loop"""
        print("\n" + "="*70)
        print("🎤 JARVIS VOICE-CONTROLLED BROWSER ACTIVATED")
        print("="*70)
        print("Say 'help' for available commands")
        print("Say 'exit' to quit")
        print("="*70 + "\n")
        
        self.speak("Voice browser activated. How can I help you?")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                command = self.listen()
                
                if command:
                    if not self.process_command(command):
                        break
                
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n\n👋 Voice browser stopped by user")
                self.speak("Voice browser deactivated")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue


def test_microphone():
    """Test if microphone is working"""
    print("\n" + "="*70)
    print("🎤 MICROPHONE TEST")
    print("="*70)
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("✅ Microphone detected!")
            print("🎤 Say something to test...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            
            print("🔄 Processing...")
            text = recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")
            print("✅ Microphone is working!")
            return True
            
    except sr.WaitTimeoutError:
        print("⏱️ No speech detected")
        return False
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return False
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if microphone is connected")
        print("   2. Check microphone permissions")
        print("   3. Try running: pip install pyaudio")
        return False


def main():
    """Main function"""
    print("\n" + "="*70)
    print("🎤 JARVIS VOICE BROWSER SYSTEM")
    print("="*70)
    print("\n1. Start Voice Browser")
    print("2. Test Microphone")
    print("3. Exit")
    print("="*70)
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        try:
            voice_browser = JarvisVoiceBrowser()
            voice_browser.run()
        except Exception as e:
            print(f"\n❌ Error starting voice browser: {e}")
            print("\n💡 Make sure to install required packages:")
            print("   pip install SpeechRecognition pyttsx3 pyaudio")
            
    elif choice == '2':
        test_microphone()
        
    elif choice == '3':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
