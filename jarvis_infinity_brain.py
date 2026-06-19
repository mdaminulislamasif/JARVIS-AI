#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS INFINITY BRAIN - Unlimited Knowledge Through Internet
জার্ভিস ইনফিনিটি ব্রেইন - ইন্টারনেটের মাধ্যমে সীমাহীন জ্ঞান

This system gives JARVIS access to unlimited knowledge by:
এই সিস্টেম জার্ভিসকে সীমাহীন জ্ঞানের অ্যাক্সেস দেয়:

1. Wikipedia Search (Free, unlimited)
2. Web Search (DuckDuckGo - no API key needed)
3. Real-time information
4. Automatic learning from internet
5. Caching for offline access
"""

import sqlite3
import os
import sys
from datetime import datetime
import json
import urllib.request
import urllib.parse
import re

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class JarvisInfinityBrain:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.learned_count = 0
        self.cache_enabled = True
        
    def show_banner(self):
        print("\n" + "="*80)
        print("  ♾️  JARVIS INFINITY BRAIN")
        print("  ♾️  জার্ভিস ইনফিনিটি ব্রেইন")
        print("="*80 + "\n")
        print("  Unlimited Knowledge Through Internet!")
        print("  ইন্টারনেটের মাধ্যমে সীমাহীন জ্ঞান!")
        print("\n" + "="*80 + "\n")
        
    def search_wikipedia(self, query):
        """
        Search Wikipedia for information
        Works without API key!
        """
        try:
            print(f"🔍 Searching Wikipedia for: {query}")
            print(f"🔍 Wikipedia-তে খুঁজছি: {query}\n")
            
            # Wikipedia API endpoint (free, no key needed)
            base_url = "https://en.wikipedia.org/w/api.php"
            
            # Search for the page
            search_params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': 1
            }
            
            search_url = base_url + '?' + urllib.parse.urlencode(search_params)
            
            with urllib.request.urlopen(search_url, timeout=10) as response:
                search_data = json.loads(response.read().decode())
                
            if not search_data.get('query', {}).get('search'):
                return None
                
            page_title = search_data['query']['search'][0]['title']
            
            # Get page content
            content_params = {
                'action': 'query',
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
                'titles': page_title,
                'format': 'json'
            }
            
            content_url = base_url + '?' + urllib.parse.urlencode(content_params)
            
            with urllib.request.urlopen(content_url, timeout=10) as response:
                content_data = json.loads(response.read().decode())
                
            pages = content_data.get('query', {}).get('pages', {})
            page_id = list(pages.keys())[0]
            extract = pages[page_id].get('extract', '')
            
            if extract:
                # Limit to first 500 characters for summary
                summary = extract[:500] + "..." if len(extract) > 500 else extract
                
                print(f"✅ Found on Wikipedia!")
                print(f"📄 Title: {page_title}")
                print(f"📝 Summary: {summary[:100]}...\n")
                
                return {
                    'source': 'Wikipedia',
                    'title': page_title,
                    'content': extract,
                    'url': f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️ Wikipedia search error: {e}\n")
            return None
            
    def search_web_duckduckgo(self, query):
        """
        Search web using DuckDuckGo Instant Answer API
        Free, no API key needed!
        """
        try:
            print(f"🌐 Searching web for: {query}")
            print(f"🌐 ওয়েবে খুঁজছি: {query}\n")
            
            # DuckDuckGo Instant Answer API (free, no key)
            base_url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            url = base_url + '?' + urllib.parse.urlencode(params)
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            # Get abstract or definition
            content = data.get('Abstract') or data.get('Definition') or ''
            
            if content:
                print(f"✅ Found on DuckDuckGo!")
                print(f"📝 Info: {content[:100]}...\n")
                
                return {
                    'source': 'DuckDuckGo',
                    'title': data.get('Heading', query),
                    'content': content,
                    'url': data.get('AbstractURL', '')
                }
                
            return None
            
        except Exception as e:
            print(f"⚠️ Web search error: {e}\n")
            return None
            
    def search_internet(self, query):
        """
        Search internet using multiple sources
        """
        print(f"♾️  INFINITY BRAIN SEARCHING...")
        print(f"♾️  ইনফিনিটি ব্রেইন খুঁজছে...\n")
        
        # Try Wikipedia first (most reliable)
        result = self.search_wikipedia(query)
        
        # If not found, try DuckDuckGo
        if not result:
            result = self.search_web_duckduckgo(query)
            
        return result
        
    def save_to_database(self, query, result):
        """
        Save learned information to database
        """
        if not result:
            return False
            
        try:
            content = f"""
Topic: {query}
Source: {result['source']} (Internet)
Title: {result['title']}
URL: {result['url']}

Content:
{result['content']}

Learned from Internet on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
ইন্টারনেট থেকে শেখা হয়েছে {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-এ

This knowledge was acquired through Infinity Brain internet search.
এই জ্ঞান ইনফিনিটি ব্রেইন ইন্টারনেট সার্চের মাধ্যমে অর্জিত হয়েছে।
"""
            
            topic_name = f"{query} (Internet)"
            
            # Check if already exists
            self.cursor.execute("""
                SELECT COUNT(*) FROM knowledge_base 
                WHERE topic = ?
            """, (topic_name,))
            
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO knowledge_base (topic, content, source)
                    VALUES (?, ?, ?)
                """, (topic_name, content.strip(), f"Infinity Brain - {result['source']}"))
                
                self.conn.commit()
                self.learned_count += 1
                
                print(f"💾 Saved to database!")
                print(f"💾 ডাটাবেসে সংরক্ষিত!\n")
                return True
            else:
                print(f"ℹ️  Already in database")
                print(f"ℹ️  ইতিমধ্যে ডাটাবেসে আছে\n")
                return False
                
        except Exception as e:
            print(f"❌ Error saving: {e}\n")
            return False
            
    def learn_from_internet(self, query):
        """
        Learn about a topic from internet
        """
        result = self.search_internet(query)
        
        if result:
            self.save_to_database(query, result)
            return result
        else:
            print(f"❌ Could not find information about: {query}")
            print(f"❌ তথ্য পাওয়া যায়নি: {query}\n")
            return None
            
    def auto_learn_topics(self, topics):
        """
        Automatically learn multiple topics from internet
        """
        print(f"🚀 Auto-learning {len(topics)} topics from internet...")
        print(f"🚀 ইন্টারনেট থেকে {len(topics)}টি বিষয় স্বয়ংক্রিয়ভাবে শিখছি...\n")
        
        for i, topic in enumerate(topics, 1):
            print(f"[{i}/{len(topics)}] Learning: {topic}")
            print("="*80)
            
            self.learn_from_internet(topic)
            
            print("="*80 + "\n")
            
    def show_statistics(self):
        """
        Show learning statistics
        """
        print("\n" + "="*80)
        print("  📊 INFINITY BRAIN STATISTICS")
        print("  📊 ইনফিনিটি ব্রেইন পরিসংখ্যান")
        print("="*80 + "\n")
        
        # Total knowledge
        self.cursor.execute("SELECT COUNT(*) FROM knowledge_base")
        total = self.cursor.fetchone()[0]
        
        # Internet learned
        self.cursor.execute("""
            SELECT COUNT(*) FROM knowledge_base 
            WHERE source LIKE 'Infinity Brain%'
        """)
        internet_learned = self.cursor.fetchone()[0]
        
        print(f"  📚 Total Knowledge: {total} entries")
        print(f"  ♾️  Internet-Learned: {internet_learned} entries")
        print(f"  ➕ This Session: {self.learned_count} entries")
        
        print("\n" + "="*80 + "\n")
        
    def interactive_mode(self):
        """
        Interactive mode - ask anything!
        """
        print("="*80)
        print("  💬 INTERACTIVE MODE")
        print("  💬 ইন্টারঅ্যাক্টিভ মোড")
        print("="*80 + "\n")
        print("  Ask JARVIS anything! Type 'exit' to quit.")
        print("  জার্ভিসকে যেকোনো কিছু জিজ্ঞাসা করুন! 'exit' টাইপ করুন বের হতে।")
        print("\n" + "="*80 + "\n")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                query = input("You: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['exit', 'quit', 'bye']:
                    print("\n👋 Goodbye! | বিদায়!\n")
                    break
                    
                print()
                result = self.learn_from_internet(query)
                
                if result:
                    print(f"JARVIS: {result['content'][:300]}...")
                    print(f"\n🔗 Source: {result['url']}\n")
                else:
                    print("JARVIS: Sorry, I couldn't find information about that.")
                    print("জার্ভিস: দুঃখিত, আমি সে সম্পর্কে তথ্য খুঁজে পাইনি।\n")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! | বিদায়!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                
    def run_demo(self):
        """
        Run demo with sample topics
        """
        self.show_banner()
        
        print("="*80)
        print("  🎯 DEMO MODE - Learning from Internet")
        print("  🎯 ডেমো মোড - ইন্টারনেট থেকে শিখছি")
        print("="*80 + "\n")
        
        # Sample topics to learn
        topics = [
            "Artificial Intelligence",
            "Quantum Computing",
            "Machine Learning",
            "Python Programming",
            "Bangladesh"
        ]
        
        self.auto_learn_topics(topics)
        self.show_statistics()
        
        print("="*80)
        print("  ✅ DEMO COMPLETED!")
        print("  ✅ ডেমো সম্পন্ন!")
        print("="*80)
        
        print(f"""
  🧪 TEST JARVIS NOW:
  
  python jarvis_offline_brain.py "What is Artificial Intelligence?"
  python jarvis_offline_brain.py "Tell me about Quantum Computing"
  python jarvis_offline_brain.py "What is Bangladesh?"
        """)
        
        print("="*80 + "\n")
        
    def run_interactive(self):
        """
        Run interactive mode
        """
        self.show_banner()
        self.interactive_mode()
        self.show_statistics()
        
        self.conn.close()

def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
        
    brain = JarvisInfinityBrain()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            brain.run_interactive()
        elif sys.argv[1] == "--demo" or sys.argv[1] == "-d":
            brain.run_demo()
        elif sys.argv[1] == "--learn":
            # Learn specific topic
            if len(sys.argv) > 2:
                topic = " ".join(sys.argv[2:])
                brain.show_banner()
                brain.learn_from_internet(topic)
                brain.show_statistics()
            else:
                print("Usage: python jarvis_infinity_brain.py --learn <topic>")
        else:
            print("Usage:")
            print("  python jarvis_infinity_brain.py --demo          # Run demo")
            print("  python jarvis_infinity_brain.py --interactive   # Interactive mode")
            print("  python jarvis_infinity_brain.py --learn <topic> # Learn specific topic")
    else:
        # Default: run demo
        brain.run_demo()
        
    brain.conn.close()

if __name__ == "__main__":
    main()
