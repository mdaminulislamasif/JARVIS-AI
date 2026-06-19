"""
JARVIS Browser Controller - Complete Web Browser Integration
Opens browsers, navigates, searches, and learns from web content
"""

import webbrowser
import subprocess
import os
import sys
import time
from pathlib import Path
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

class JarvisBrowserController:
    def __init__(self):
        self.learning_db = "jarvis_web_learning.db"
        self.init_learning_database()
        self.browser_history = []
        
    def init_learning_database(self):
        """Initialize database to store learned web content"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS web_learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                title TEXT,
                content TEXT,
                keywords TEXT,
                learned_at TIMESTAMP,
                category TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS browser_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                action TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def open_browser(self, url=None):
        """Open default browser with optional URL"""
        try:
            if url:
                print(f"🌐 Opening browser: {url}")
                webbrowser.open(url)
                self.log_history(url, "opened")
            else:
                print("🌐 Opening default browser...")
                webbrowser.open("https://www.google.com")
                self.log_history("https://www.google.com", "opened")
            return True
        except Exception as e:
            print(f"❌ Error opening browser: {e}")
            return False
    
    def open_specific_browser(self, browser_name, url="https://www.google.com"):
        """Open specific browser (chrome, firefox, edge, etc.)"""
        browsers = {
            'chrome': 'chrome',
            'firefox': 'firefox',
            'edge': 'msedge',
            'opera': 'opera',
            'brave': 'brave'
        }
        
        try:
            browser_cmd = browsers.get(browser_name.lower())
            if browser_cmd:
                if sys.platform == 'win32':
                    subprocess.Popen([browser_cmd, url], shell=True)
                else:
                    subprocess.Popen([browser_cmd, url])
                print(f"🌐 Opened {browser_name} with {url}")
                self.log_history(url, f"opened in {browser_name}")
                return True
            else:
                print(f"❌ Browser {browser_name} not recognized")
                return False
        except Exception as e:
            print(f"❌ Error opening {browser_name}: {e}")
            return False
    
    def search_google(self, query):
        """Search Google and open results"""
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        print(f"🔍 Searching Google for: {query}")
        self.open_browser(search_url)
        self.log_history(search_url, f"searched: {query}")
        
        # Learn from search results
        self.learn_from_url(search_url, query)
        
    def search_youtube(self, query):
        """Search YouTube"""
        encoded_query = urllib.parse.quote(query)
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        print(f"🎥 Searching YouTube for: {query}")
        self.open_browser(youtube_url)
        self.log_history(youtube_url, f"youtube search: {query}")
        
    def search_wikipedia(self, query):
        """Search Wikipedia"""
        encoded_query = urllib.parse.quote(query)
        wiki_url = f"https://en.wikipedia.org/wiki/{encoded_query}"
        print(f"📚 Opening Wikipedia: {query}")
        self.open_browser(wiki_url)
        self.log_history(wiki_url, f"wikipedia: {query}")
        
        # Learn from Wikipedia
        self.learn_from_url(wiki_url, query)
        
    def search_github(self, query):
        """Search GitHub"""
        encoded_query = urllib.parse.quote(query)
        github_url = f"https://github.com/search?q={encoded_query}"
        print(f"💻 Searching GitHub for: {query}")
        self.open_browser(github_url)
        self.log_history(github_url, f"github search: {query}")
        
    def open_social_media(self, platform):
        """Open social media platforms"""
        platforms = {
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'reddit': 'https://www.reddit.com',
            'tiktok': 'https://www.tiktok.com',
            'youtube': 'https://www.youtube.com'
        }
        
        url = platforms.get(platform.lower())
        if url:
            print(f"📱 Opening {platform}...")
            self.open_browser(url)
            return True
        else:
            print(f"❌ Platform {platform} not found")
            return False
    
    def learn_from_url(self, url, topic=None):
        """Scrape and learn content from URL"""
        try:
            print(f"🧠 Learning from: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text() if title else "No title"
            
            # Extract main content
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs[:20]])  # First 20 paragraphs
            
            # Extract keywords
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            keywords = meta_keywords['content'] if meta_keywords else topic or ""
            
            # Save to learning database
            self.save_learning(url, title_text, content, keywords, topic or "general")
            
            print(f"✅ Learned from {title_text}")
            print(f"📝 Content length: {len(content)} characters")
            
            return {
                'title': title_text,
                'content': content,
                'keywords': keywords
            }
            
        except Exception as e:
            print(f"⚠️ Could not learn from {url}: {e}")
            return None
    
    def save_learning(self, url, title, content, keywords, category):
        """Save learned content to database"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO web_learning (url, title, content, keywords, learned_at, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (url, title, content, keywords, datetime.now(), category))
        
        conn.commit()
        conn.close()
        
    def log_history(self, url, action):
        """Log browser history"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO browser_history (url, action, timestamp)
            VALUES (?, ?, ?)
        ''', (url, action, datetime.now()))
        
        conn.commit()
        conn.close()
        
        self.browser_history.append({
            'url': url,
            'action': action,
            'time': datetime.now()
        })
    
    def get_learning_summary(self):
        """Get summary of learned content"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM web_learning')
        total_learned = cursor.fetchone()[0]
        
        cursor.execute('SELECT category, COUNT(*) FROM web_learning GROUP BY category')
        categories = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM browser_history')
        total_visits = cursor.fetchone()[0]
        
        conn.close()
        
        print("\n" + "="*60)
        print("🧠 JARVIS WEB LEARNING SUMMARY")
        print("="*60)
        print(f"📚 Total pages learned: {total_learned}")
        print(f"🌐 Total browser visits: {total_visits}")
        print(f"\n📊 Learning by category:")
        for category, count in categories:
            print(f"   • {category}: {count} pages")
        print("="*60 + "\n")
        
    def search_learned_content(self, keyword):
        """Search through learned content"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, url, content, learned_at 
            FROM web_learning 
            WHERE content LIKE ? OR title LIKE ? OR keywords LIKE ?
            ORDER BY learned_at DESC
            LIMIT 10
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            print(f"\n🔍 Found {len(results)} results for '{keyword}':\n")
            for i, (title, url, content, learned_at) in enumerate(results, 1):
                print(f"{i}. {title}")
                print(f"   URL: {url}")
                print(f"   Learned: {learned_at}")
                print(f"   Preview: {content[:150]}...")
                print()
        else:
            print(f"❌ No results found for '{keyword}'")
        
        return results
    
    def open_multiple_tabs(self, urls):
        """Open multiple URLs in tabs"""
        print(f"🌐 Opening {len(urls)} tabs...")
        for url in urls:
            self.open_browser(url)
            time.sleep(0.5)  # Small delay between tabs
    
    def quick_access_menu(self):
        """Quick access to common websites"""
        print("\n" + "="*60)
        print("🌐 JARVIS BROWSER - QUICK ACCESS MENU")
        print("="*60)
        print("1. Google")
        print("2. YouTube")
        print("3. Wikipedia")
        print("4. GitHub")
        print("5. Stack Overflow")
        print("6. Reddit")
        print("7. Twitter")
        print("8. LinkedIn")
        print("9. Gmail")
        print("10. Custom URL")
        print("="*60)
        
        quick_sites = {
            '1': 'https://www.google.com',
            '2': 'https://www.youtube.com',
            '3': 'https://www.wikipedia.org',
            '4': 'https://www.github.com',
            '5': 'https://stackoverflow.com',
            '6': 'https://www.reddit.com',
            '7': 'https://www.twitter.com',
            '8': 'https://www.linkedin.com',
            '9': 'https://mail.google.com'
        }
        
        return quick_sites


def main():
    """Main browser controller interface"""
    browser = JarvisBrowserController()
    
    print("\n" + "="*60)
    print("🌐 JARVIS BROWSER CONTROLLER ACTIVATED")
    print("="*60)
    print("Commands:")
    print("  open [url]           - Open URL in browser")
    print("  search [query]       - Search Google")
    print("  youtube [query]      - Search YouTube")
    print("  wiki [query]         - Search Wikipedia")
    print("  github [query]       - Search GitHub")
    print("  social [platform]    - Open social media")
    print("  learn [url]          - Learn from URL")
    print("  summary              - Show learning summary")
    print("  find [keyword]       - Search learned content")
    print("  quick                - Quick access menu")
    print("  history              - Show browser history")
    print("  exit                 - Exit")
    print("="*60 + "\n")
    
    # WARNING: Infinite loop - ensure break condition exists
    while True:
        try:
            command = input("JARVIS Browser> ").strip().lower()
            
            if not command:
                continue
                
            if command == 'exit':
                print("👋 Browser controller deactivated")
                break
                
            elif command.startswith('open '):
                url = command[5:].strip()
                if not url.startswith('http'):
                    url = 'https://' + url
                browser.open_browser(url)
                
            elif command.startswith('search '):
                query = command[7:].strip()
                browser.search_google(query)
                
            elif command.startswith('youtube '):
                query = command[8:].strip()
                browser.search_youtube(query)
                
            elif command.startswith('wiki '):
                query = command[5:].strip()
                browser.search_wikipedia(query)
                
            elif command.startswith('github '):
                query = command[7:].strip()
                browser.search_github(query)
                
            elif command.startswith('social '):
                platform = command[7:].strip()
                browser.open_social_media(platform)
                
            elif command.startswith('learn '):
                url = command[6:].strip()
                if not url.startswith('http'):
                    url = 'https://' + url
                browser.learn_from_url(url)
                
            elif command == 'summary':
                browser.get_learning_summary()
                
            elif command.startswith('find '):
                keyword = command[5:].strip()
                browser.search_learned_content(keyword)
                
            elif command == 'quick':
                sites = browser.quick_access_menu()
                choice = input("\nEnter choice (1-10): ").strip()
                if choice in sites:
                    browser.open_browser(sites[choice])
                elif choice == '10':
                    url = input("Enter URL: ").strip()
                    if not url.startswith('http'):
                        url = 'https://' + url
                    browser.open_browser(url)
                    
            elif command == 'history':
                print("\n📜 Recent Browser History:")
                for i, entry in enumerate(browser.browser_history[-10:], 1):
                    print(f"{i}. {entry['action']}: {entry['url']}")
                    print(f"   Time: {entry['time']}")
                print()
                
            else:
                print("❌ Unknown command. Type 'exit' to quit.")
                
        except KeyboardInterrupt:
            print("\n👋 Browser controller deactivated")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
