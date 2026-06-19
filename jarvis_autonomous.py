"""
JARVIS AUTONOMOUS SYSTEM
Complete AI that does everything automatically
- Searches automatically
- Uses websites automatically
- Understands user needs
- Speaks and listens
- Self-updates and upgrades
- NO API KEYS NEEDED
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import os
import time
import subprocess
import sys
from datetime import datetime
import threading
import queue

class JarvisAutonomous:
    def __init__(self):
        print("🤖 Initializing JARVIS Autonomous System...")
        
        # Speech recognition (NO API KEY - uses Google free service)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text-to-speech (NO API KEY - uses local engine)
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Set voice to male if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'male' in voice.name.lower() and 'female' not in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Database for learning and memory
        self.db_file = "jarvis_autonomous.db"
        self.init_database()
        
        # User preferences and learning
        self.user_preferences = {}
        self.conversation_history = []
        self.task_queue = queue.Queue()
        
        # Auto-update settings
        self.version = "1.0.0"
        self.auto_update_enabled = True
        
        # Load user preferences
        self.load_preferences()
        
        print("✅ JARVIS Autonomous System Ready!")
        
    def init_database(self):
        """Initialize database for memory and learning"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # User preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP
            )
        ''')
        
        # Conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                jarvis_response TEXT,
                action_taken TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        # Learned patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT,
                action TEXT,
                success_count INTEGER DEFAULT 0,
                fail_count INTEGER DEFAULT 0,
                last_used TIMESTAMP
            )
        ''')
        
        # Web knowledge
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS web_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                content TEXT,
                source_url TEXT,
                learned_at TIMESTAMP
            )
        ''')
        
        # Tasks and automation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automated_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                task_type TEXT,
                schedule TEXT,
                last_run TIMESTAMP,
                enabled INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def speak(self, text):
        """Speak text (NO API KEY)"""
        print(f"🔊 JARVIS: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    def listen(self, timeout=5):
        """Listen to user (NO API KEY - uses Google free service)"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            # Uses Google's free speech recognition (NO API KEY NEEDED)
            text = self.recognizer.recognize_google(audio).lower()
            print(f"📝 You said: {text}")
            
            # Save to conversation history
            self.conversation_history.append({
                'user': text,
                'timestamp': datetime.now()
            })
            
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"⚠️ Listen error: {e}")
            return None
    
    def understand_intent(self, text):
        """Understand what user wants (NO API KEY - local processing)"""
        text = text.lower().strip()
        
        intents = {
            'search': ['search', 'find', 'look for', 'google', 'what is', 'who is', 'where is'],
            'open_website': ['open', 'go to', 'visit', 'website', 'site'],
            'youtube': ['youtube', 'video', 'play', 'watch'],
            'social': ['facebook', 'twitter', 'instagram', 'linkedin'],
            'learn': ['learn', 'teach me', 'explain', 'tell me about'],
            'help': ['help', 'what can you do', 'commands'],
            'weather': ['weather', 'temperature', 'forecast'],
            'news': ['news', 'latest', 'headlines'],
            'email': ['email', 'mail', 'gmail'],
            'music': ['music', 'song', 'play music'],
            'time': ['time', 'what time', 'clock'],
            'date': ['date', 'what date', 'today'],
            'calculate': ['calculate', 'math', 'compute'],
            'translate': ['translate', 'translation'],
            'reminder': ['remind', 'reminder', 'remember'],
            'shutdown': ['shutdown', 'turn off', 'power off'],
            'restart': ['restart', 'reboot'],
            'update': ['update', 'upgrade', 'self update'],
            'exit': ['exit', 'quit', 'bye', 'goodbye', 'stop']
        }
        
        # Find matching intent
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in text:
                    return intent, text.replace(keyword, '').strip()
        
        # If no specific intent, assume search
        return 'search', text
    
    def execute_action(self, intent, query):
        """Execute action based on intent (NO API KEY)"""
        
        if intent == 'search':
            self.speak(f"Searching for {query}")
            self.search_web(query)
            
        elif intent == 'open_website':
            self.speak(f"Opening {query}")
            self.open_website(query)
            
        elif intent == 'youtube':
            self.speak(f"Searching YouTube for {query}")
            self.search_youtube(query)
            
        elif intent == 'social':
            self.speak(f"Opening social media")
            self.open_social_media(query)
            
        elif intent == 'learn':
            self.speak(f"Learning about {query}")
            self.learn_topic(query)
            
        elif intent == 'help':
            self.show_capabilities()
            
        elif intent == 'weather':
            self.get_weather(query)
            
        elif intent == 'news':
            self.get_news()
            
        elif intent == 'email':
            self.speak("Opening Gmail")
            webbrowser.open('https://mail.google.com')
            
        elif intent == 'music':
            self.speak(f"Playing music: {query}")
            self.search_youtube(query + " music")
            
        elif intent == 'time':
            current_time = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")
            
        elif intent == 'date':
            current_date = datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            
        elif intent == 'calculate':
            self.calculate(query)
            
        elif intent == 'translate':
            self.translate_text(query)
            
        elif intent == 'reminder':
            self.set_reminder(query)
            
        elif intent == 'shutdown':
            self.speak("Shutting down system")
            os.system("shutdown /s /t 1")
            
        elif intent == 'restart':
            self.speak("Restarting system")
            os.system("shutdown /r /t 1")
            
        elif intent == 'update':
            self.self_update()
            
        elif intent == 'exit':
            return False
            
        return True
    
    def search_web(self, query):
        """Search web and learn (NO API KEY)"""
        try:
            # Open Google search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            
            # Scrape and learn from results
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(search_url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract information
            results = soup.find_all('div', class_='g')
            if results:
                first_result = results[0].get_text()[:500]
                self.save_knowledge(query, first_result, search_url)
                self.speak(f"Found information about {query}")
            
        except Exception as e:
            print(f"⚠️ Search error: {e}")
    
    def open_website(self, query):
        """Open website intelligently"""
        websites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'github': 'https://www.github.com',
            'reddit': 'https://www.reddit.com',
            'wikipedia': 'https://www.wikipedia.org',
            'gmail': 'https://mail.google.com',
            'netflix': 'https://www.netflix.com',
            'amazon': 'https://www.amazon.com'
        }
        
        for name, url in websites.items():
            if name in query.lower():
                webbrowser.open(url)
                return
        
        # Try to open as URL
        if not query.startswith('http'):
            query = 'https://www.' + query.replace(' ', '') + '.com'
        webbrowser.open(query)
    
    def search_youtube(self, query):
        """Search YouTube"""
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
    
    def open_social_media(self, query):
        """Open social media"""
        social = {
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com'
        }
        
        for name, url in social.items():
            if name in query:
                webbrowser.open(url)
                return
    
    def learn_topic(self, topic):
        """Learn about topic from web (NO API KEY)"""
        try:
            # Search Wikipedia
            wiki_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
            response = requests.get(wiki_url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs[:3]])
            
            if content:
                self.save_knowledge(topic, content, wiki_url)
                self.speak(f"I learned about {topic}")
                
                # Open the page
                webbrowser.open(wiki_url)
            
        except Exception as e:
            print(f"⚠️ Learn error: {e}")
            self.search_web(topic)
    
    def get_weather(self, location):
        """Get weather (NO API KEY - scrapes from web)"""
        try:
            if not location:
                location = "current location"
            
            search_url = f"https://www.google.com/search?q=weather+{location.replace(' ', '+')}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(search_url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract weather info
            temp = soup.find('span', class_='wob_t')
            condition = soup.find('span', id='wob_dc')
            
            if temp and condition:
                self.speak(f"The weather is {condition.text} with temperature {temp.text} degrees")
            else:
                self.speak("Opening weather information")
            
            webbrowser.open(search_url)
            
        except Exception as e:
            print(f"⚠️ Weather error: {e}")
            webbrowser.open(f"https://www.google.com/search?q=weather")
    
    def get_news(self):
        """Get latest news (NO API KEY)"""
        self.speak("Opening latest news")
        webbrowser.open("https://news.google.com")
    
    def calculate(self, expression):
        """Calculate math (NO API KEY - local processing)"""
        try:
            # Clean expression
            expression = expression.replace('x', '*').replace('plus', '+').replace('minus', '-')
            result = eval(expression)
            self.speak(f"The answer is {result}")
        except Exception as e:

            print(f"⚠️ Error: {e}")
            self.speak("Opening calculator")
            webbrowser.open(f"https://www.google.com/search?q={expression}")
    
    def translate_text(self, text):
        """Translate text (NO API KEY - uses Google Translate web)"""
        self.speak("Opening translator")
        webbrowser.open(f"https://translate.google.com/?text={text.replace(' ', '+')}")
    
    def set_reminder(self, reminder):
        """Set reminder"""
        self.speak(f"Reminder set for {reminder}")
        # Save to database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO automated_tasks (task_name, task_type, schedule)
            VALUES (?, 'reminder', ?)
        ''', (reminder, datetime.now()))
        conn.commit()
        conn.close()
    
    def save_knowledge(self, topic, content, source):
        """Save learned knowledge"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO web_knowledge (topic, content, source_url, learned_at)
            VALUES (?, ?, ?, ?)
        ''', (topic, content, source, datetime.now()))
        conn.commit()
        conn.close()
    
    def load_preferences(self):
        """Load user preferences"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT key, value FROM preferences')
            for key, value in cursor.fetchall():
                self.user_preferences[key] = value
            conn.close()
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    def save_preference(self, key, value):
        """Save user preference"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now()))
        conn.commit()
        conn.close()
        self.user_preferences[key] = value
    
    def self_update(self):
        """Self-update system (NO API KEY)"""
        self.speak("Checking for updates")
        
        try:
            # Update pip packages
            self.speak("Updating packages")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         capture_output=True)
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 
                          'SpeechRecognition', 'pyttsx3', 'requests', 'beautifulsoup4'],
                         capture_output=True)
            
            self.speak("System updated successfully")
            
        except Exception as e:
            self.speak("Update failed")
            print(f"⚠️ Update error: {e}")
    
    def show_capabilities(self):
        """Show what JARVIS can do"""
        capabilities = """
        I can help you with:
        - Search anything on the web
        - Open websites and apps
        - Play YouTube videos
        - Get weather information
        - Read latest news
        - Calculate math
        - Translate languages
        - Set reminders
        - Control your computer
        - Learn new topics
        - And much more!
        
        Just speak naturally and I'll understand!
        """
        print(capabilities)
        self.speak("I can help you with many tasks. Check the screen for details.")
    
    def autonomous_mode(self):
        """Fully autonomous mode - JARVIS works on its own"""
        self.speak("Autonomous mode activated. I will work independently.")
        
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
            
            intent, query = self.understand_intent(task)
            self.execute_action(intent, query)
            
            time.sleep(5)  # Wait between tasks
        
        self.speak("Autonomous tasks completed")
    
    def run(self):
        """Main JARVIS loop"""
        print("\n" + "="*70)
        print("🤖 JARVIS AUTONOMOUS SYSTEM ACTIVATED")
        print("="*70)
        print("I can understand and do everything automatically!")
        print("Just speak naturally - no commands needed!")
        print("Say 'help' to see what I can do")
        print("Say 'autonomous mode' for fully automatic operation")
        print("Say 'exit' to quit")
        print("="*70 + "\n")
        
        self.speak("Hello! I am JARVIS, your autonomous assistant. How can I help you?")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                # Listen for command
                user_input = self.listen()
                
                if user_input:
                    # Check for autonomous mode
                    if 'autonomous' in user_input:
                        self.autonomous_mode()
                        continue
                    
                    # Understand intent
                    intent, query = self.understand_intent(user_input)
                    
                    # Execute action
                    if not self.execute_action(intent, query):
                        self.speak("Goodbye! JARVIS shutting down.")
                        break
                    
                    # Save conversation
                    conn = sqlite3.connect(self.db_file)
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO conversations (user_input, action_taken, timestamp)
                        VALUES (?, ?, ?)
                    ''', (user_input, intent, datetime.now()))
                    conn.commit()
                    conn.close()
                
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n\n👋 JARVIS stopped by user")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue


def main():
    """Main function"""
    print("\n" + "="*70)
    print("🤖 JARVIS AUTONOMOUS SYSTEM")
    print("="*70)
    print("\nFeatures:")
    print("✓ Voice recognition (NO API KEY)")
    print("✓ Text-to-speech (NO API KEY)")
    print("✓ Automatic web search")
    print("✓ Automatic website usage")
    print("✓ Understands user needs")
    print("✓ Self-learning")
    print("✓ Self-updating")
    print("✓ Fully autonomous mode")
    print("="*70 + "\n")
    
    try:
        jarvis = JarvisAutonomous()
        jarvis.run()
    except Exception as e:
        print(f"\n❌ Error starting JARVIS: {e}")
        print("\n💡 Installing required packages...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'SpeechRecognition', 'pyttsx3', 'pyaudio', 
                       'requests', 'beautifulsoup4'])
        print("\n✅ Packages installed! Please run again.")


if __name__ == "__main__":
    main()
