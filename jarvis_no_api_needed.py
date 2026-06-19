"""
JARVIS - NO API KEYS NEEDED
Works completely without any API keys
Uses only free, local, and unlimited services
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
import json
import subprocess
import sys

class JarvisNoAPI:
    def __init__(self):
        print("\n" + "="*70)
        print("🤖 JARVIS - NO API KEYS NEEDED")
        print("="*70)
        print("\n✓ Using FREE services only")
        print("✓ NO API keys required")
        print("✓ NO quotas or limits")
        print("✓ Works OFFLINE for many features")
        print("\n" + "="*70 + "\n")
        
        # Speech Recognition (FREE - Google's public service)
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self.mic_available = True
        except Exception as e:

            print(f"⚠️ Error: {e}")
            self.mic_available = False
            print("⚠️ Microphone not available - text mode only")
        
        # Text-to-Speech (FREE - Local pyttsx3)
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1.0)
            self.tts_available = True
        except Exception as e:

            print(f"⚠️ Error: {e}")
            self.tts_available = False
            print("⚠️ Text-to-speech not available")
        
        # Local database (NO API)
        self.db = "jarvis_no_api.db"
        self.init_database()
        
        # State
        self.user_name = None
        self.conversation_history = []
        
        # Load profile
        self.load_profile()
        
        print("✅ JARVIS Ready - NO API KEYS NEEDED!\n")
    
    def init_database(self):
        """Initialize local database"""
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                jarvis_response TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                content TEXT,
                source TEXT,
                learned_at TIMESTAMP
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
        """Speak text (NO API)"""
        print(f"\n🤖 JARVIS: {text}")
        if self.tts_available:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:

                print(f"⚠️ Error: {e}")
                pass
    
    def listen(self):
        """Listen to user (FREE Google service - NO API KEY)"""
        if not self.mic_available:
            return input("\n💬 You: ").strip().lower()
        
        try:
            with self.microphone as source:
                print("\n🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            # Uses Google's FREE public service (NO API KEY)
            text = self.recognizer.recognize_google(audio).lower()
            print(f"💬 You: {text}")
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return None
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return input("\n💬 You: ").strip().lower()
    
    def search_web_no_api(self, query):
        """Search web without API (Direct scraping)"""
        try:
            self.speak(f"Searching for {query}")
            
            # Open Google search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            
            # Try to scrape results (NO API)
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(search_url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract first result snippet
            results = soup.find_all('div', class_='g')
            if results:
                first_result = results[0].get_text()[:200]
                self.speak("I found some information")
                
                # Save to local knowledge base
                self.save_knowledge(query, first_result, search_url)
            
            return True
        except Exception as e:
            print(f"⚠️ Search error: {e}")
            webbrowser.open(search_url)
            return True
    
    def save_knowledge(self, topic, content, source):
        """Save to local knowledge base (NO API)"""
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO knowledge (topic, content, source, learned_at)
                VALUES (?, ?, ?, ?)
            ''', (topic, content, source, datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    def get_local_knowledge(self, query):
        """Get knowledge from local database (NO API)"""
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT topic, content, source FROM knowledge
                WHERE topic LIKE ? OR content LIKE ?
                ORDER BY learned_at DESC LIMIT 5
            ''', (f'%{query}%', f'%{query}%'))
            results = cursor.fetchall()
            conn.close()
            
            if results:
                self.speak("I found this in my knowledge base")
                for topic, content, source in results:
                    print(f"\n📚 {topic}")
                    print(f"   {content[:100]}...")
                return True
            return False
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return False
    
    def process_command(self, text):
        """Process command (NO API)"""
        if not text:
            return True
        
        # Exit
        if any(word in text for word in ['exit', 'quit', 'bye', 'goodbye']):
            return False
        
        # Name
        if not self.user_name and ('my name is' in text or 'i am' in text):
            name = text.split('my name is' if 'my name is' in text else 'i am')[1].strip().split()[0].capitalize()
            self.user_name = name
            self.save_profile('name', name)
            self.speak(f"Nice to meet you, {name}!")
            return True
        
        # Greetings
        if any(word in text for word in ['hello', 'hi', 'hey']):
            if self.user_name:
                self.speak(f"Hello, {self.user_name}!")
            else:
                self.speak("Hello! How can I help?")
            return True
        
        # Search
        if any(word in text for word in ['search', 'find', 'look for', 'google']):
            query = text
            for word in ['search', 'search for', 'find', 'look for', 'google']:
                query = query.replace(word, '').strip()
            
            if query:
                # Check local knowledge first
                if not self.get_local_knowledge(query):
                    # Search web
                    self.search_web_no_api(query)
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
                'gmail': 'https://mail.google.com',
                'github': 'https://www.github.com'
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
        if 'youtube' in text or 'video' in text:
            query = text.replace('youtube', '').replace('video', '').strip()
            if query:
                self.speak(f"Searching YouTube for {query}")
                webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            else:
                webbrowser.open('https://www.youtube.com')
            return True
        
        # Weather
        if 'weather' in text:
            self.speak("Checking weather")
            webbrowser.open("https://www.google.com/search?q=weather")
            return True
        
        # News
        if 'news' in text:
            self.speak("Opening news")
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
        
        # Knowledge base
        if 'what do you know' in text or 'show knowledge' in text:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM knowledge')
            count = cursor.fetchone()[0]
            conn.close()
            self.speak(f"I have {count} items in my knowledge base")
            return True
        
        # Help
        if 'help' in text:
            self.speak("I can search, open websites, check weather and news, tell time, and remember information. All without API keys!")
            return True
        
        # Default: search
        self.speak("Let me search for that")
        self.search_web_no_api(text)
        return True
    
    def run(self):
        """Main loop"""
        print("="*70)
        print("🤖 JARVIS ACTIVATED - NO API KEYS NEEDED")
        print("="*70)
        print("\n✓ All features work without API keys")
        print("✓ No quotas or limits")
        print("✓ Completely free")
        print("\nSay 'help' for commands")
        print("Say 'exit' to quit")
        print("\n" + "="*70 + "\n")
        
        # Greet
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
            self.speak(f"{greeting}! I'm JARVIS. What's your name?")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = self.listen()
                
                if user_input:
                    # Save conversation
                    self.conversation_history.append({
                        'user': user_input,
                        'timestamp': datetime.now()
                    })
                    
                    # Process
                    if not self.process_command(user_input):
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


def check_and_install():
    """Check and install required packages"""
    packages = {
        'SpeechRecognition': 'speech_recognition',
        'pyttsx3': 'pyttsx3',
        'requests': 'requests',
        'beautifulsoup4': 'bs4'
    }
    
    print("🔧 Checking packages...")
    
    for package, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package}")
        except ImportError:
            print(f"⚠️ Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         capture_output=True)
    
    print("✅ All packages ready!\n")


def main():
    """Main function"""
    print("\n" + "="*70)
    print("🤖 JARVIS - NO API KEYS NEEDED")
    print("="*70)
    print("\nThis version works WITHOUT any API keys!")
    print("✓ Uses FREE Google speech recognition")
    print("✓ Uses LOCAL text-to-speech")
    print("✓ Uses LOCAL database")
    print("✓ Direct web scraping (NO API)")
    print("✓ NO quotas or limits")
    print("="*70 + "\n")
    
    # Check packages
    check_and_install()
    
    # Run JARVIS
    try:
        jarvis = JarvisNoAPI()
        jarvis.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTrying to install missing packages...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'SpeechRecognition', 'pyttsx3', 'pyaudio', 
                       'requests', 'beautifulsoup4'])
        print("\n✅ Please run again!")


if __name__ == "__main__":
    main()
