"""
JARVIS - COMPLETE AI SYSTEM
One file that does everything!
Just run this and JARVIS will do everything automatically
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import time
from datetime import datetime
import random
import subprocess
import sys

class JARVIS:
    def __init__(self):
        print("\n" + "="*70)
        print("                    JARVIS AI SYSTEM")
        print("                  Initializing...")
        print("="*70 + "\n")
        
        # Initialize speech
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Set male voice
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'male' in voice.name.lower() and 'female' not in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Initialize database
        self.db = "jarvis_complete.db"
        self.init_db()
        
        # State
        self.user_name = None
        self.context = []
        self.autonomous = False
        
        # Load profile
        self.load_profile()
        
        print("✅ JARVIS Ready!\n")
    
    def init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                jarvis_response TEXT,
                timestamp TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def load_profile(self):
        """Load user profile"""
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM profile WHERE key="name"')
            result = cursor.fetchone()
            if result:
                self.user_name = result[0]
            conn.close()
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    def save_profile(self, key, value):
        """Save to profile"""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO profile (key, value) VALUES (?, ?)', (key, value))
        conn.commit()
        conn.close()
    
    def speak(self, text):
        """Speak text"""
        print(f"🤖 JARVIS: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    def listen(self):
        """Listen to user"""
        try:
            with self.microphone as source:
                print("\n🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            text = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You: {text}\n")
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return None
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None
    
    def process(self, text):
        """Process user input"""
        if not text:
            return True
        
        # Exit
        if any(word in text for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
            return False
        
        # Autonomous mode
        if 'autonomous' in text:
            self.speak("Autonomous mode activated! I'll work independently now.")
            self.autonomous_mode()
            return True
        
        # Name
        if not self.user_name and ('my name is' in text or 'i am' in text or 'call me' in text):
            name = text.split('my name is' if 'my name is' in text else 'i am' if 'i am' in text else 'call me')[1].strip().split()[0].capitalize()
            self.user_name = name
            self.save_profile('name', name)
            self.speak(f"Nice to meet you, {name}!")
            return True
        
        # Greetings
        if any(word in text for word in ['hello', 'hi', 'hey']):
            if self.user_name:
                self.speak(f"Hello, {self.user_name}! How can I help?")
            else:
                self.speak("Hello! How can I help you?")
            return True
        
        # How are you
        if 'how are you' in text:
            self.speak("I'm doing great! How about you?")
            return True
        
        # Thank you
        if 'thank' in text:
            self.speak("You're welcome!")
            return True
        
        # Search
        if any(word in text for word in ['search', 'find', 'look for', 'google']):
            query = text
            for word in ['search', 'search for', 'find', 'look for', 'google']:
                query = query.replace(word, '').strip()
            if query:
                self.speak(f"Searching for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            return True
        
        # Open website
        if any(word in text for word in ['open', 'go to', 'visit']):
            site = text
            for word in ['open', 'go to', 'visit', 'website']:
                site = site.replace(word, '').strip()
            
            sites = {
                'google': 'https://www.google.com',
                'youtube': 'https://www.youtube.com',
                'facebook': 'https://www.facebook.com',
                'twitter': 'https://www.twitter.com',
                'instagram': 'https://www.instagram.com',
                'gmail': 'https://mail.google.com',
                'github': 'https://www.github.com',
                'reddit': 'https://www.reddit.com',
                'wikipedia': 'https://www.wikipedia.org'
            }
            
            for name, url in sites.items():
                if name in site:
                    self.speak(f"Opening {name}")
                    webbrowser.open(url)
                    return True
            
            if site:
                if not site.startswith('http'):
                    site = 'https://www.' + site.replace(' ', '') + '.com'
                self.speak(f"Opening {site}")
                webbrowser.open(site)
            return True
        
        # YouTube
        if 'youtube' in text or 'video' in text or 'play' in text:
            query = text.replace('youtube', '').replace('video', '').replace('play', '').strip()
            if query:
                self.speak(f"Playing {query} on YouTube")
                webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            else:
                self.speak("Opening YouTube")
                webbrowser.open('https://www.youtube.com')
            return True
        
        # Learn
        if any(word in text for word in ['learn', 'teach', 'explain', 'tell me about']):
            topic = text
            for word in ['learn', 'teach', 'teach me', 'explain', 'tell me about']:
                topic = topic.replace(word, '').strip()
            if topic:
                self.speak(f"Let me teach you about {topic}")
                webbrowser.open(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}")
            return True
        
        # Weather
        if 'weather' in text:
            self.speak("Checking the weather")
            webbrowser.open("https://www.google.com/search?q=weather")
            return True
        
        # News
        if 'news' in text:
            self.speak("Opening latest news")
            webbrowser.open("https://news.google.com")
            return True
        
        # Time
        if 'time' in text:
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"It's {current_time}")
            return True
        
        # Date
        if 'date' in text or 'today' in text:
            current_date = datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            return True
        
        # Calculate
        if 'calculate' in text or 'compute' in text or 'math' in text:
            self.speak("Opening calculator")
            webbrowser.open(f"https://www.google.com/search?q={text}")
            return True
        
        # Update
        if 'update' in text or 'upgrade' in text:
            self.speak("Updating system")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 
                          'SpeechRecognition', 'pyttsx3', 'requests', 'beautifulsoup4'],
                         capture_output=True)
            self.speak("System updated!")
            return True
        
        # Help
        if 'help' in text or 'what can you do' in text:
            self.speak("I can search the web, open websites, play videos, check weather and news, tell time, and much more!")
            self.speak("Just speak naturally and I'll understand!")
            return True
        
        # Default: search
        self.speak(f"Let me search for that")
        webbrowser.open(f"https://www.google.com/search?q={text.replace(' ', '+')}")
        return True
    
    def autonomous_mode(self):
        """Autonomous mode - JARVIS works independently"""
        tasks = [
            "Learn about artificial intelligence",
            "Check latest technology news",
            "Learn about quantum computing",
            "Check weather",
            "Learn about machine learning",
            "Search for Python tutorials"
        ]
        
        for task in tasks:
            print(f"\n🤖 Autonomous Task: {task}")
            self.speak(f"Working on: {task}")
            self.process(task)
            time.sleep(3)
        
        self.speak("Autonomous tasks completed!")
    
    def greet(self):
        """Greet user"""
        hour = datetime.now().hour
        
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        if self.user_name:
            self.speak(f"{greeting}, {self.user_name}!")
        else:
            self.speak(f"{greeting}!")
        
        self.speak("I'm JARVIS, your AI assistant. How can I help you today?")
        
        if not self.user_name:
            self.speak("By the way, what's your name?")
    
    def run(self):
        """Main loop"""
        print("="*70)
        print("                    JARVIS ACTIVATED")
        print("="*70)
        print("\n✓ Speak naturally - JARVIS understands everything")
        print("✓ Say 'autonomous mode' for full automation")
        print("✓ Say 'exit' to stop\n")
        print("="*70 + "\n")
        
        self.greet()
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = self.listen()
                
                if user_input:
                    if not self.process(user_input):
                        if self.user_name:
                            self.speak(f"Goodbye, {self.user_name}!")
                        else:
                            self.speak("Goodbye!")
                        break
                
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n\n👋 JARVIS stopped")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")
                continue


def main():
    """Main function"""
    try:
        jarvis = JARVIS()
        jarvis.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Installing required packages...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'SpeechRecognition', 'pyttsx3', 'pyaudio', 
                       'requests', 'beautifulsoup4'])
        print("\n✅ Packages installed! Please run again.")


if __name__ == "__main__":
    main()
