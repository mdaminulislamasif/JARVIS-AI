#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS SEARCH ENGINE AUTO-LEARNER
জার্ভিস সার্চ ইঞ্জিন অটো-লার্নার

JARVIS will use search engines to learn word by word!
জার্ভিস সার্চ ইঞ্জিন ব্যবহার করে একটা একটা শব্দ শিখবে!

Features:
বৈশিষ্ট্য:
1. Search using multiple search engines
   একাধিক সার্চ ইঞ্জিন ব্যবহার করে সার্চ করুন
2. Learn word by word automatically
   স্বয়ংক্রিয়ভাবে একটা একটা শব্দ শিখুন
3. Extract knowledge from search results
   সার্চ ফলাফল থেকে জ্ঞান এক্সট্র্যাক্ট করুন
4. Save to database
   ডাটাবেসে সংরক্ষণ করুন
5. Continuous learning
   ক্রমাগত শেখা
"""

import os
import sys
import sqlite3
import time
import random
from datetime import datetime
import urllib.request
import urllib.parse
import json
import re

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class SearchLearner:
    """
    JARVIS Search Engine Auto-Learner
    জার্ভিস সার্চ ইঞ্জিন অটো-লার্নার
    """
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.words_learned = 0
        self.searches_done = 0
        
        # Search engines
        self.search_engines = {
            'DuckDuckGo': 'https://api.duckduckgo.com/?q={}&format=json',
            'Wikipedia': 'https://en.wikipedia.org/api/rest_v1/page/summary/{}',
        }
        
        # Words to learn (can be expanded)
        self.learning_topics = [
            # Technology
            "Python", "JavaScript", "AI", "Machine Learning", "Deep Learning",
            "Neural Network", "Algorithm", "Database", "API", "Cloud Computing",
            "Blockchain", "Cryptocurrency", "Quantum Computing", "IoT", "5G",
            
            # Science
            "Physics", "Chemistry", "Biology", "Astronomy", "Genetics",
            "Evolution", "Photosynthesis", "DNA", "Atom", "Molecule",
            
            # Mathematics
            "Algebra", "Calculus", "Geometry", "Statistics", "Probability",
            "Matrix", "Vector", "Derivative", "Integral", "Equation",
            
            # General Knowledge
            "History", "Geography", "Culture", "Art", "Music",
            "Literature", "Philosophy", "Psychology", "Sociology", "Economics",
            
            # Programming
            "Function", "Variable", "Loop", "Array", "Object",
            "Class", "Method", "Interface", "Inheritance", "Polymorphism",
            
            # Computer Science
            "Operating System", "Compiler", "Interpreter", "Memory", "CPU",
            "GPU", "RAM", "Storage", "Network", "Protocol",
        ]
        
        # Create search history table
        self.create_search_table()
    
    def create_search_table(self):
        """Create table for search history"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_term TEXT NOT NULL,
                    search_engine TEXT,
                    result_summary TEXT,
                    learned_content TEXT,
                    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Error creating table: {e}")
    
    def show_banner(self):
        """Show banner"""
        print("\n" + "="*80)
        print("  🔍 JARVIS SEARCH ENGINE AUTO-LEARNER")
        print("  🔍 জার্ভিস সার্চ ইঞ্জিন অটো-লার্নার")
        print("="*80 + "\n")
        print("  JARVIS will search and learn word by word!")
        print("  জার্ভিস একটা একটা শব্দ সার্চ করবে এবং শিখবে!")
        print("\n" + "="*80 + "\n")
    
    def search_duckduckgo(self, query):
        """
        Search using DuckDuckGo Instant Answer API
        """
        try:
            url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                # Extract information
                result = {
                    'title': query,
                    'abstract': data.get('Abstract', ''),
                    'definition': data.get('Definition', ''),
                    'url': data.get('AbstractURL', ''),
                    'source': data.get('AbstractSource', 'DuckDuckGo'),
                }
                
                # Get related topics
                related = []
                for topic in data.get('RelatedTopics', [])[:3]:
                    if isinstance(topic, dict) and 'Text' in topic:
                        related.append(topic['Text'])
                
                result['related'] = related
                
                return result
                
        except Exception as e:
            return {'error': str(e)}
    
    def search_wikipedia(self, query):
        """
        Search using Wikipedia API
        """
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                result = {
                    'title': data.get('title', query),
                    'abstract': data.get('extract', ''),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'source': 'Wikipedia',
                }
                
                return result
                
        except Exception as e:
            return {'error': str(e)}
    
    def learn_from_search(self, query):
        """
        Search and learn from results
        """
        print(f"🔍 Searching for: {query}")
        print(f"🔍 সার্চ করছি: {query}\n")
        
        # Try DuckDuckGo first
        result = self.search_duckduckgo(query)
        
        if 'error' in result or not result.get('abstract'):
            # Try Wikipedia
            print("   Trying Wikipedia...")
            result = self.search_wikipedia(query)
        
        if 'error' in result:
            print(f"   ⚠️ Search failed: {result['error']}\n")
            return False
        
        # Extract learned content
        learned_content = ""
        
        if result.get('abstract'):
            learned_content = result['abstract']
            print(f"   ✅ Found: {result['abstract'][:150]}...")
        
        if result.get('definition'):
            learned_content += f"\n\nDefinition: {result['definition']}"
        
        if result.get('related'):
            learned_content += f"\n\nRelated: {', '.join(result['related'])}"
        
        if not learned_content:
            print(f"   ⚠️ No content found\n")
            return False
        
        # Save to search history
        try:
            self.cursor.execute("""
                INSERT INTO search_history (search_term, search_engine, result_summary, learned_content)
                VALUES (?, ?, ?, ?)
            """, (query, result.get('source', 'Unknown'), result.get('abstract', '')[:500], learned_content))
            
            self.conn.commit()
        except Exception as e:
            print(f"   ⚠️ Error saving search history: {e}")
        
        # Save to knowledge base
        try:
            content = f"""
{query}

Source: {result.get('source', 'Search Engine')}
URL: {result.get('url', 'N/A')}

{learned_content}

Learned via: JARVIS Search Engine Auto-Learner
শিখেছে: জার্ভিস সার্চ ইঞ্জিন অটো-লার্নার
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            self.cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source)
                VALUES (?, ?, ?)
            """, (query, content.strip(), f"Search: {result.get('source', 'Unknown')}"))
            
            self.conn.commit()
            
            print(f"   ✅ Learned and saved to database!")
            print(f"   ✅ শিখেছি এবং ডাটাবেসে সংরক্ষণ করেছি!\n")
            
            self.words_learned += 1
            self.searches_done += 1
            
            return True
            
        except Exception as e:
            print(f"   ⚠️ Error saving to knowledge base: {e}\n")
            return False
    
    def auto_learn_words(self, num_words=10, delay=2):
        """
        Automatically learn multiple words
        """
        print(f"🎓 Starting auto-learning: {num_words} words")
        print(f"🎓 অটো-লার্নিং শুরু হচ্ছে: {num_words} শব্দ\n")
        
        # Shuffle topics for variety
        topics = random.sample(self.learning_topics, min(num_words, len(self.learning_topics)))
        
        for i, topic in enumerate(topics, 1):
            print(f"[{i}/{num_words}] ", end="")
            
            success = self.learn_from_search(topic)
            
            if success and i < num_words:
                print(f"   ⏳ Waiting {delay} seconds before next search...")
                time.sleep(delay)
        
        print("\n" + "="*80)
        print(f"  ✅ Auto-learning complete!")
        print(f"  ✅ অটো-লার্নিং সম্পন্ন!")
        print("="*80)
        print(f"\n  📊 Statistics:")
        print(f"     Words learned: {self.words_learned}")
        print(f"     Searches done: {self.searches_done}")
        print(f"     Success rate: {(self.words_learned/self.searches_done*100) if self.searches_done > 0 else 0:.1f}%")
    
    def learn_custom_word(self, word):
        """
        Learn a specific word
        """
        print(f"\n🎓 Learning: {word}")
        print(f"🎓 শিখছি: {word}\n")
        
        success = self.learn_from_search(word)
        
        if success:
            print(f"\n✅ Successfully learned: {word}")
            print(f"✅ সফলভাবে শিখেছি: {word}")
        else:
            print(f"\n❌ Failed to learn: {word}")
            print(f"❌ শিখতে ব্যর্থ: {word}")
    
    def show_search_history(self, limit=10):
        """
        Show recent search history
        """
        print("\n" + "="*80)
        print("  📜 SEARCH HISTORY")
        print("  📜 সার্চ ইতিহাস")
        print("="*80 + "\n")
        
        try:
            self.cursor.execute("""
                SELECT search_term, search_engine, search_date
                FROM search_history
                ORDER BY search_date DESC
                LIMIT ?
            """, (limit,))
            
            history = self.cursor.fetchall()
            
            if history:
                for i, (term, engine, date) in enumerate(history, 1):
                    print(f"  {i}. {term}")
                    print(f"     Engine: {engine} | Date: {date}\n")
            else:
                print("  No search history yet.")
                print("  এখনো কোনো সার্চ ইতিহাস নেই।")
        
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
    
    def show_statistics(self):
        """
        Show learning statistics
        """
        print("\n" + "="*80)
        print("  📊 LEARNING STATISTICS")
        print("  📊 শেখার পরিসংখ্যান")
        print("="*80 + "\n")
        
        try:
            # Total searches
            self.cursor.execute("SELECT COUNT(*) FROM search_history")
            total_searches = self.cursor.fetchone()[0]
            
            # Total knowledge
            self.cursor.execute("SELECT COUNT(*) FROM knowledge_base")
            total_knowledge = self.cursor.fetchone()[0]
            
            # Searches by engine
            self.cursor.execute("""
                SELECT search_engine, COUNT(*) 
                FROM search_history 
                GROUP BY search_engine
            """)
            by_engine = self.cursor.fetchall()
            
            print(f"  Total Searches: {total_searches}")
            print(f"  Total Knowledge Entries: {total_knowledge}")
            print(f"\n  Searches by Engine:")
            for engine, count in by_engine:
                print(f"    • {engine}: {count}")
            
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
    
    learner = SearchLearner()
    learner.show_banner()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "auto":
            # Auto-learn mode
            num_words = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            learner.auto_learn_words(num_words)
        elif sys.argv[1] == "history":
            # Show history
            learner.show_search_history()
        elif sys.argv[1] == "stats":
            # Show statistics
            learner.show_statistics()
        else:
            # Learn specific word
            learner.learn_custom_word(sys.argv[1])
    else:
        # Interactive mode
        print("Usage:")
        print("  python jarvis_search_learner.py auto [num_words]  - Auto-learn multiple words")
        print("  python jarvis_search_learner.py <word>            - Learn specific word")
        print("  python jarvis_search_learner.py history           - Show search history")
        print("  python jarvis_search_learner.py stats             - Show statistics")
        print("\nExample:")
        print("  python jarvis_search_learner.py auto 20")
        print("  python jarvis_search_learner.py Python")
        print("\nStarting auto-learn with 10 words...\n")
        
        learner.auto_learn_words(10)
    
    learner.close()

if __name__ == "__main__":
    main()
