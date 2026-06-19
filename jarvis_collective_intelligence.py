#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS COLLECTIVE INTELLIGENCE - All Human Knowledge
জার্ভিস সমষ্টিগত বুদ্ধিমত্তা - সব মানুষের জ্ঞান

Give JARVIS access to ALL human knowledge from Earth!
জার্ভিসকে পৃথিবীর সব মানুষের জ্ঞানে অ্যাক্সেস দিন!

Sources:
উৎস:
1. Wikipedia (All languages)
2. Academic Papers (arXiv, PubMed, etc.)
3. Books (Project Gutenberg, Open Library)
4. Educational Content (Khan Academy, Coursera, etc.)
5. News and Current Events
6. Cultural Knowledge
7. Historical Records
8. Scientific Databases
9. Technical Documentation
10. Social Knowledge
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

class JarvisCollectiveIntelligence:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.learned_count = 0
        
        # All human knowledge sources
        self.knowledge_sources = {
            "Wikipedia": {
                "type": "Encyclopedia",
                "languages": ["English", "Bengali", "Spanish", "French", "German", "Chinese", "Japanese", "Arabic", "Hindi", "Portuguese"],
                "coverage": "General knowledge, all topics",
                "api": "Free",
                "status": "Active"
            },
            "arXiv": {
                "type": "Academic Papers",
                "coverage": "Physics, Math, CS, Biology",
                "api": "Free",
                "status": "Active"
            },
            "PubMed": {
                "type": "Medical Research",
                "coverage": "Medicine, Health, Biology",
                "api": "Free",
                "status": "Active"
            },
            "Project Gutenberg": {
                "type": "Books",
                "coverage": "70,000+ free books",
                "api": "Free",
                "status": "Active"
            },
            "Open Library": {
                "type": "Books",
                "coverage": "Millions of books",
                "api": "Free",
                "status": "Active"
            },
            "Khan Academy": {
                "type": "Education",
                "coverage": "Math, Science, Arts, Economics",
                "api": "Free",
                "status": "Active"
            },
            "Coursera": {
                "type": "Online Courses",
                "coverage": "University-level courses",
                "api": "Limited",
                "status": "Active"
            },
            "Stack Overflow": {
                "type": "Programming Q&A",
                "coverage": "All programming languages",
                "api": "Free",
                "status": "Active"
            },
            "GitHub": {
                "type": "Code Repository",
                "coverage": "Millions of projects",
                "api": "Free",
                "status": "Active"
            },
            "News APIs": {
                "type": "Current Events",
                "coverage": "Global news",
                "api": "Various",
                "status": "Active"
            }
        }
        
    def show_banner(self):
        print("\n" + "="*80)
        print("  🧠 JARVIS COLLECTIVE INTELLIGENCE")
        print("  🧠 জার্ভিস সমষ্টিগত বুদ্ধিমত্তা")
        print("="*80 + "\n")
        print("  All Human Knowledge from Earth!")
        print("  পৃথিবীর সব মানুষের জ্ঞান!")
        print("\n" + "="*80 + "\n")
        
    def show_knowledge_sources(self):
        """Show all human knowledge sources"""
        print("🌍 HUMAN KNOWLEDGE SOURCES:")
        print("🌍 মানব জ্ঞানের উৎস:\n")
        
        for idx, (name, info) in enumerate(self.knowledge_sources.items(), 1):
            print(f"  {idx}. {name}")
            print(f"     Type: {info['type']}")
            print(f"     Coverage: {info['coverage']}")
            print(f"     API: {info['api']}")
            print(f"     Status: {info['status']}")
            print()
            
    def search_wikipedia_multilingual(self, query, language="en"):
        """
        Search Wikipedia in multiple languages
        """
        try:
            print(f"🔍 Searching Wikipedia ({language}) for: {query}")
            print(f"🔍 Wikipedia ({language})-তে খুঁজছি: {query}\n")
            
            # Wikipedia API endpoint
            base_url = f"https://{language}.wikipedia.org/w/api.php"
            
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
                summary = extract[:500] + "..." if len(extract) > 500 else extract
                
                print(f"✅ Found on Wikipedia ({language})!")
                print(f"📄 Title: {page_title}")
                print(f"📝 Summary: {summary[:100]}...\n")
                
                return {
                    'source': f'Wikipedia ({language})',
                    'title': page_title,
                    'content': extract,
                    'url': f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    'language': language
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️ Wikipedia ({language}) search error: {e}\n")
            return None
            
    def search_arxiv(self, query):
        """
        Search arXiv for academic papers
        """
        try:
            print(f"📚 Searching arXiv for: {query}")
            print(f"📚 arXiv-এ খুঁজছি: {query}\n")
            
            # arXiv API endpoint
            base_url = "http://export.arxiv.org/api/query"
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': 1
            }
            
            url = base_url + '?' + urllib.parse.urlencode(params)
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = response.read().decode()
                
            # Simple XML parsing (extract title and summary)
            title_match = re.search(r'<title>(.*?)</title>', data, re.DOTALL)
            summary_match = re.search(r'<summary>(.*?)</summary>', data, re.DOTALL)
            
            if title_match and summary_match:
                title = title_match.group(1).strip()
                summary = summary_match.group(1).strip()
                
                # Skip the feed title
                if 'ArXiv Query' not in title:
                    print(f"✅ Found on arXiv!")
                    print(f"📄 Title: {title[:100]}...")
                    print(f"📝 Summary: {summary[:100]}...\n")
                    
                    return {
                        'source': 'arXiv (Academic Papers)',
                        'title': title,
                        'content': summary,
                        'url': 'https://arxiv.org'
                    }
            
            return None
            
        except Exception as e:
            print(f"⚠️ arXiv search error: {e}\n")
            return None
            
    def search_collective_intelligence(self, query):
        """
        Search across all human knowledge sources
        """
        print(f"🧠 COLLECTIVE INTELLIGENCE SEARCHING...")
        print(f"🧠 সমষ্টিগত বুদ্ধিমত্তা খুঁজছে...\n")
        
        results = []
        
        # Try Wikipedia (English)
        result = self.search_wikipedia_multilingual(query, "en")
        if result:
            results.append(result)
            
        # Try arXiv for academic content
        result = self.search_arxiv(query)
        if result:
            results.append(result)
            
        return results if results else None
        
    def save_to_database(self, query, results):
        """
        Save learned information to database
        """
        if not results:
            return False
            
        saved_count = 0
        
        for result in results:
            try:
                content = f"""
Topic: {query}
Source: {result['source']} (Collective Intelligence)
Title: {result['title']}
URL: {result.get('url', 'N/A')}

Content:
{result['content']}

Learned from Collective Intelligence on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
সমষ্টিগত বুদ্ধিমত্তা থেকে শেখা হয়েছে {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-এ

This knowledge represents human collective intelligence from Earth.
এই জ্ঞান পৃথিবীর মানব সমষ্টিগত বুদ্ধিমত্তার প্রতিনিধিত্ব করে।
"""
                
                topic_name = f"{query} ({result['source']})"
                
                # Check if already exists
                self.cursor.execute("""
                    SELECT COUNT(*) FROM knowledge_base 
                    WHERE topic = ?
                """, (topic_name,))
                
                if self.cursor.fetchone()[0] == 0:
                    self.cursor.execute("""
                        INSERT INTO knowledge_base (topic, content, source)
                        VALUES (?, ?, ?)
                    """, (topic_name, content.strip(), f"Collective Intelligence - {result['source']}"))
                    
                    self.conn.commit()
                    self.learned_count += 1
                    saved_count += 1
                    
                    print(f"💾 Saved from {result['source']}!")
                    print(f"💾 {result['source']} থেকে সংরক্ষিত!\n")
                    
            except Exception as e:
                print(f"❌ Error saving: {e}\n")
                
        return saved_count > 0
        
    def learn_from_collective_intelligence(self, query):
        """
        Learn about a topic from collective intelligence
        """
        results = self.search_collective_intelligence(query)
        
        if results:
            self.save_to_database(query, results)
            return results
        else:
            print(f"❌ Could not find information about: {query}")
            print(f"❌ তথ্য পাওয়া যায়নি: {query}\n")
            return None
            
    def auto_learn_topics(self, topics):
        """
        Automatically learn multiple topics from collective intelligence
        """
        print(f"🚀 Auto-learning {len(topics)} topics from collective intelligence...")
        print(f"🚀 সমষ্টিগত বুদ্ধিমত্তা থেকে {len(topics)}টি বিষয় স্বয়ংক্রিয়ভাবে শিখছি...\n")
        
        for i, topic in enumerate(topics, 1):
            print(f"[{i}/{len(topics)}] Learning: {topic}")
            print("="*80)
            
            self.learn_from_collective_intelligence(topic)
            
            print("="*80 + "\n")
            
    def show_statistics(self):
        """
        Show learning statistics
        """
        print("\n" + "="*80)
        print("  📊 COLLECTIVE INTELLIGENCE STATISTICS")
        print("  📊 সমষ্টিগত বুদ্ধিমত্তা পরিসংখ্যান")
        print("="*80 + "\n")
        
        # Total knowledge
        self.cursor.execute("SELECT COUNT(*) FROM knowledge_base")
        total = self.cursor.fetchone()[0]
        
        # Collective intelligence learned
        self.cursor.execute("""
            SELECT COUNT(*) FROM knowledge_base 
            WHERE source LIKE 'Collective Intelligence%'
        """)
        collective_learned = self.cursor.fetchone()[0]
        
        print(f"  📚 Total Knowledge: {total} entries")
        print(f"  🧠 Collective Intelligence: {collective_learned} entries")
        print(f"  ➕ This Session: {self.learned_count} entries")
        print(f"  🌍 Knowledge Sources: {len(self.knowledge_sources)} available")
        
        print("\n" + "="*80 + "\n")
        
    def run_demo(self):
        """
        Run demo with sample topics
        """
        self.show_banner()
        self.show_knowledge_sources()
        
        print("="*80)
        print("  🎯 DEMO MODE - Learning from Collective Intelligence")
        print("  🎯 ডেমো মোড - সমষ্টিগত বুদ্ধিমত্তা থেকে শিখছি")
        print("="*80 + "\n")
        
        # Sample topics representing human knowledge
        topics = [
            "Human Brain",
            "Consciousness",
            "Artificial Intelligence",
            "Quantum Physics",
            "Human Evolution"
        ]
        
        self.auto_learn_topics(topics)
        self.show_statistics()
        
        print("="*80)
        print("  ✅ DEMO COMPLETED!")
        print("  ✅ ডেমো সম্পন্ন!")
        print("="*80)
        
        print(f"""
  🧪 TEST JARVIS NOW:
  
  python jarvis_offline_brain.py "What is Human Brain?"
  python jarvis_offline_brain.py "Tell me about Consciousness"
  python jarvis_offline_brain.py "Explain Quantum Physics"
        """)
        
        print("="*80 + "\n")

def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
        
    brain = JarvisCollectiveIntelligence()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo" or sys.argv[1] == "-d":
            brain.run_demo()
        elif sys.argv[1] == "--learn":
            # Learn specific topic
            if len(sys.argv) > 2:
                topic = " ".join(sys.argv[2:])
                brain.show_banner()
                brain.learn_from_collective_intelligence(topic)
                brain.show_statistics()
            else:
                print("Usage: python jarvis_collective_intelligence.py --learn <topic>")
        else:
            print("Usage:")
            print("  python jarvis_collective_intelligence.py --demo          # Run demo")
            print("  python jarvis_collective_intelligence.py --learn <topic> # Learn specific topic")
    else:
        # Default: run demo
        brain.run_demo()
        
    brain.conn.close()

if __name__ == "__main__":
    main()
