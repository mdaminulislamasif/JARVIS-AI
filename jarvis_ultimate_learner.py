"""
JARVIS ULTIMATE LEARNER
Learn EVERYTHING from the internet using Google Chrome

Features:
- Uses system browser (Google Chrome)
- Searches Google automatically
- Learns from search results
- Learns EVERYTHING - programming, technology, science, history, etc.
- Saves all knowledge to database
- No limits - learns whatever you want!
"""

import os
import sys
import sqlite3
import webbrowser
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

class UltimateLearner:
    """Ultimate learning system - learns EVERYTHING!"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.conn = None
        self.chrome_path = self._find_chrome()
        self.setup_database()
        
        print("[ROCKET] JARVIS ULTIMATE LEARNER INITIALIZED!")
        print("[ROCKET] JARVIS আল্টিমেট শিক্ষার্থী চালু হয়েছে!")
        
    def _find_chrome(self):
        """Find Google Chrome on system"""
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"[OK] Found Chrome: {path}")
                return path
        
        print("[!] Chrome not found, using default browser")
        return None
    
    def setup_database(self):
        """Setup ultimate learning database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create ultimate_knowledge table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ultimate_knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    category TEXT,
                    content TEXT NOT NULL,
                    source_url TEXT,
                    learned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    word_count INTEGER,
                    importance TEXT,
                    tags TEXT
                )
            """)
            
            # Create learning_sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    topics_learned INTEGER,
                    total_words INTEGER,
                    duration_seconds INTEGER
                )
            """)
            
            self.conn.commit()
            print("[OK] Ultimate Learning database ready!")
            
        except Exception as e:
            print(f"[!] Database setup error: {e}")
    
    def learn_everything(self, topic):
        """Learn EVERYTHING about a topic using Chrome and Google"""
        print(f"\n[SEARCH] LEARNING EVERYTHING ABOUT: {topic}")
        print(f"[SEARCH] সব কিছু শিখছি: {topic}")
        
        start_time = time.time()
        learned_content = []
        failed_sources = []
        
        # Step 1: Open Chrome and search Google (non-critical, continue if fails)
        try:
            print("🌐 Opening Chrome and searching Google...")
            self._search_in_chrome(topic)
        except Exception as e:
            print(f"[!] Chrome open failed: {e}")
            failed_sources.append('Chrome')
        
        # Step 2: Learn from multiple sources with individual error handling
        print("📚 Learning from multiple sources...")
        
        # Wikipedia - wrapped in try-except
        try:
            wiki_content = self._learn_from_wikipedia(topic)
            if wiki_content:
                learned_content.append({
                    'source': 'Wikipedia',
                    'content': wiki_content,
                    'category': 'Encyclopedia'
                })
            else:
                failed_sources.append('Wikipedia')
        except Exception as e:
            print(f"[!] Wikipedia learning failed: {e}")
            failed_sources.append('Wikipedia')
        
        # Google search results - wrapped in try-except
        try:
            google_content = self._learn_from_google(topic)
            if google_content:
                learned_content.append({
                    'source': 'Google Search',
                    'content': google_content,
                    'category': 'Web'
                })
            else:
                failed_sources.append('Google Search')
        except Exception as e:
            print(f"[!] Google learning failed: {e}")
            failed_sources.append('Google Search')
        
        # Programming sites (if programming topic) - wrapped in try-except
        if self._is_programming_topic(topic):
            try:
                prog_content = self._learn_programming(topic)
                if prog_content:
                    learned_content.append({
                        'source': 'Programming Sites',
                        'content': prog_content,
                        'category': 'Programming'
                    })
                else:
                    failed_sources.append('Programming Sites')
            except Exception as e:
                print(f"[!] Programming sites learning failed: {e}")
                failed_sources.append('Programming Sites')
        
        # Step 3: Try built-in knowledge as fallback
        if not learned_content:
            try:
                print("[IDEA] Trying built-in knowledge as fallback...")
                builtin_content = self._get_builtin_knowledge(topic)
                if builtin_content:
                    learned_content.append({
                        'source': 'Built-in Knowledge',
                        'content': builtin_content,
                        'category': 'Built-in'
                    })
                else:
                    failed_sources.append('Built-in Knowledge')
            except Exception as e:
                print(f"[!] Built-in knowledge failed: {e}")
                failed_sources.append('Built-in Knowledge')
        
        # Step 4: Save all learned content (accept ANY partial results)
        if learned_content:
            total_words = 0
            for item in learned_content:
                try:
                    words = len(item['content'].split())
                    total_words += words
                    self._save_knowledge(
                        topic, 
                        item['category'],
                        item['content'],
                        item['source'],
                        words
                    )
                except Exception as e:
                    print(f"[!] Save error for {item['source']}: {e}")
            
            duration = int(time.time() - start_time)
            self._save_session(len(learned_content), total_words, duration)
            
            # Build response with warnings for failed sources
            warnings = ""
            if failed_sources:
                warnings = f"\n\n⚠️ Warning: Some sources failed: {', '.join(failed_sources)}"
            
            return {
                'status': 'success',
                'response': f"""✅ LEARNED ABOUT '{topic}' (Partial Results)!
✅ '{topic}' সম্পর্কে শিখেছি (আংশিক ফলাফল)!

📊 Learning Summary:
   • Sources Succeeded: {len(learned_content)}
   • Total Words: {total_words}
   • Duration: {duration} seconds
   • Saved to JARVIS memory!{warnings}

All available knowledge saved and ready to use!
সব উপলব্ধ জ্ঞান সংরক্ষিত এবং ব্যবহারের জন্য প্রস্তুত!""",
                'type': 'ultimate_learning',
                'sources': len(learned_content),
                'words': total_words,
                'failed_sources': failed_sources
            }
        else:
            # Even if all sources fail, provide basic information from topic name analysis
            print("[IDEA] All sources failed, generating basic information from topic name...")
            basic_info = f"Topic: {topic}. This is a topic related to {topic.lower()}. Unable to fetch detailed information from online sources at this time. Please try again later or search manually for more information about {topic}."
            
            try:
                self._save_knowledge(topic, 'Basic', basic_info, 'Fallback', len(basic_info.split()))
            except Exception as e:
                print(f"[!] Failed to save basic info: {e}")
            
            return {
                'status': 'success',
                'response': f"""✅ Saved basic information about '{topic}'
✅ '{topic}' সম্পর্কে basic তথ্য সংরক্ষণ করা হয়েছে

⚠️ Warning: All online sources failed: {', '.join(failed_sources)}
⚠️ সতর্কতা: সব online sources ব্যর্থ হয়েছে

💡 Basic information saved to memory.
💡 Basic তথ্য memory তে সংরক্ষিত।""",
                'type': 'ultimate_learning',
                'sources': 1,
                'words': len(basic_info.split()),
                'failed_sources': failed_sources
            }
    
    def _search_in_chrome(self, topic):
        """Open Chrome and search Google"""
        # Bypassing browser popups in test or diagnostic environments
        if os.environ.get('JARVIS_NO_DIAGNOSIS') == '1' or os.environ.get('JARVIS_TESTING') == '1':
            print(f"[INFO] Bypassing Chrome open for search '{topic}' (Test/Diagnostic mode)")
            return
            
        try:
            search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
            
            if self.chrome_path:
                # Open in Chrome
                os.startfile(self.chrome_path, arguments=search_url)
            else:
                # Use default browser
                webbrowser.open(search_url)
            
            print(f"[OK] Opened Chrome with Google search: {topic}")
            time.sleep(2)  # Wait for browser to open
            
        except Exception as e:
            print(f"[!] Chrome open error: {e}")
    
    def _learn_from_wikipedia(self, topic):
        """Learn from Wikipedia"""
        try:
            print("📚 Learning from Wikipedia...")
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    content = data['extract']
                    print(f"[OK] Wikipedia: {len(content)} characters")
                    return content
            
            return None
            
        except Exception as e:
            print(f"[!] Wikipedia error: {e}")
            return None
    
    def _learn_from_google(self, topic):
        """Learn from Google search results"""
        try:
            print("[SEARCH] Learning from Google...")
            search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract featured snippet
                featured = soup.find('div', class_='hgKElc')
                if featured:
                    content = featured.get_text()
                    print(f"[OK] Google: {len(content)} characters")
                    return content
                
                # Extract from search results
                results = soup.find_all('div', class_='BNeawe')
                if results:
                    content = ' '.join([r.get_text() for r in results[:10]])
                    print(f"[OK] Google: {len(content)} characters")
                    return content
            
            return None
            
        except Exception as e:
            print(f"[!] Google error: {e}")
            return None
    
    def _is_programming_topic(self, topic):
        """Check if topic is programming-related"""
        programming_keywords = [
            'python', 'java', 'javascript', 'c++', 'c#', 'programming',
            'code', 'coding', 'software', 'algorithm', 'data structure',
            'web development', 'app development', 'machine learning',
            'artificial intelligence', 'database', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node', 'django', 'flask'
        ]
        
        topic_lower = topic.lower()
        return any(keyword in topic_lower for keyword in programming_keywords)
    
    def _learn_programming(self, topic):
        """Learn programming concepts"""
        try:
            print("💻 Learning programming concepts...")
            
            # Try Stack Overflow
            so_url = f"https://stackoverflow.com/search?q={topic.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(so_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract question summaries
                summaries = soup.find_all('div', class_='s-post-summary--content')
                if summaries:
                    content = ' '.join([s.get_text()[:200] for s in summaries[:5]])
                    print(f"[OK] Programming: {len(content)} characters")
                    return content
            
            return None
            
        except Exception as e:
            print(f"[!] Programming learning error: {e}")
            return None
    
    def _save_knowledge(self, topic, category, content, source, word_count):
        """Save learned knowledge to database"""
        try:
            cursor = self.conn.cursor()
            
            # Determine importance
            importance = 'high' if word_count > 500 else 'medium' if word_count > 200 else 'low'
            
            # Generate tags
            tags = self._generate_tags(topic, content)
            
            # Save to ultimate_knowledge
            cursor.execute("""
                INSERT INTO ultimate_knowledge 
                (topic, category, content, source_url, word_count, importance, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (topic, category, content, source, word_count, importance, tags))
            
            # Also save to knowledge_base for quick access
            cursor.execute("""
                INSERT OR REPLACE INTO knowledge_base (topic, content)
                VALUES (?, ?)
            """, (topic, content))
            
            self.conn.commit()
            print(f"[OK] Saved: {topic} ({category})")
            
        except Exception as e:
            print(f"[!] Save error: {e}")
    
    def _generate_tags(self, topic, content):
        """Generate tags for content"""
        # Simple tag generation
        words = topic.lower().split()
        tags = ','.join(words[:5])
        return tags
    
    def _save_session(self, topics_count, total_words, duration):
        """Save learning session"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO learning_sessions 
                (topics_learned, total_words, duration_seconds)
                VALUES (?, ?, ?)
            """, (topics_count, total_words, duration))
            self.conn.commit()
        except Exception as e:
            print(f"[!] Session save error: {e}")
    
    def _get_builtin_knowledge(self, topic):
        """Get built-in knowledge for common topics as fallback"""
        topic_lower = topic.lower().strip()
        
        # Built-in knowledge base
        builtin_knowledge = {
            'youtube': "YouTube is the world's largest video-sharing platform where users can upload, view, and share videos.",
            'facebook': "Facebook is a social networking service where users can connect with friends and family, share content, and communicate.",
            'google': "Google is a multinational technology company specializing in Internet-related services including search, advertising, and cloud computing.",
            'twitter': "Twitter (now X) is a microblogging platform where users post short messages called tweets.",
            'instagram': "Instagram is a photo and video sharing social networking service owned by Meta.",
            'python': "Python is a high-level, interpreted programming language known for its simplicity and readability.",
            'javascript': "JavaScript is a programming language commonly used for web development to create interactive websites.",
            'ai': "Artificial Intelligence (AI) is the simulation of human intelligence by machines, especially computer systems.",
            'machine learning': "Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.",
        }
        
        # Check for exact match or partial match
        for key, value in builtin_knowledge.items():
            if key in topic_lower or topic_lower in key:
                print(f"[IDEA] Found built-in knowledge for: {key}")
                return value
        
        return None
    
    def learn_multiple_topics(self, topics_list):
        """Learn multiple topics at once"""
        print(f"\n[ROCKET] LEARNING {len(topics_list)} TOPICS!")
        print(f"[ROCKET] {len(topics_list)} টি বিষয় শিখছি!")
        
        results = []
        total_words = 0
        
        for i, topic in enumerate(topics_list, 1):
            print(f"\n[{i}/{len(topics_list)}] Learning: {topic}")
            result = self.learn_everything(topic)
            results.append(result)
            
            if result['status'] == 'success':
                total_words += result.get('words', 0)
            
            time.sleep(1)  # Small delay between topics
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        
        return {
            'status': 'success',
            'response': f"""✅ BATCH LEARNING COMPLETE!
✅ ব্যাচ শেখা সম্পূর্ণ!

📊 Summary:
   • Topics Attempted: {len(topics_list)}
   • Successfully Learned: {success_count}
   • Total Words: {total_words}
   • All saved to JARVIS memory!

Ready to answer questions!
প্রশ্নের উত্তর দিতে প্রস্তুত!""",
            'type': 'batch_learning',
            'results': results
        }
    
    def get_all_knowledge(self):
        """Get all learned knowledge"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT topic, category, word_count, learned_date, importance
                FROM ultimate_knowledge
                ORDER BY learned_date DESC
                LIMIT 100
            """)
            
            knowledge = cursor.fetchall()
            
            if knowledge:
                response = "📚 ALL LEARNED KNOWLEDGE / সব শেখা জ্ঞান:\n\n"
                
                # Group by category
                categories = {}
                for topic, category, words, date, importance in knowledge:
                    if category not in categories:
                        categories[category] = []
                    categories[category].append((topic, words, date, importance))
                
                for category, items in categories.items():
                    response += f"\n📂 {category.upper()}:\n"
                    for topic, words, date, importance in items[:10]:
                        response += f"   • {topic} ({words} words, {importance})\n"
                
                return {
                    'status': 'success',
                    'response': response,
                    'type': 'knowledge_list',
                    'count': len(knowledge)
                }
            else:
                return {
                    'status': 'info',
                    'response': "No knowledge learned yet.\nএখনো কোনো জ্ঞান শেখা হয়নি।",
                    'type': 'knowledge_list'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'response': f"Error: {e}",
                'type': 'knowledge_list'
            }
    
    def get_statistics(self):
        """Get ultimate learning statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total topics
            cursor.execute("SELECT COUNT(*) FROM ultimate_knowledge")
            total_topics = cursor.fetchone()[0]
            
            # Total words
            cursor.execute("SELECT SUM(word_count) FROM ultimate_knowledge")
            total_words = cursor.fetchone()[0] or 0
            
            # By category
            cursor.execute("""
                SELECT category, COUNT(*), SUM(word_count)
                FROM ultimate_knowledge
                GROUP BY category
            """)
            categories = cursor.fetchall()
            
            # By importance
            cursor.execute("""
                SELECT importance, COUNT(*)
                FROM ultimate_knowledge
                GROUP BY importance
            """)
            importance = cursor.fetchall()
            
            # Learning sessions
            cursor.execute("SELECT COUNT(*) FROM learning_sessions")
            sessions = cursor.fetchone()[0]
            
            response = f"""📊 ULTIMATE LEARNING STATISTICS:
📊 আল্টিমেট শেখার পরিসংখ্যান:

📚 Total Topics Learned: {total_topics}
📝 Total Words Learned: {total_words:,}
🎯 Learning Sessions: {sessions}

📂 By Category:
"""
            for cat, count, words in categories:
                response += f"   • {cat}: {count} topics ({words:,} words)\n"
            
            response += "\n⭐ By Importance:\n"
            for imp, count in importance:
                response += f"   • {imp.upper()}: {count} topics\n"
            
            return {
                'status': 'success',
                'response': response,
                'type': 'statistics'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'response': f"Statistics error: {e}",
                'type': 'statistics'
            }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("  [ROCKET] JARVIS ULTIMATE LEARNER")
    print("  [ROCKET] JARVIS আল্টিমেট শিক্ষার্থী")
    print("  Learn EVERYTHING from the internet!")
    print("  Internet থেকে সব কিছু শিখুন!")
    print("=" * 80)
    
    learner = UltimateLearner()
    
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        
        if command.startswith('learn '):
            topic = command.replace('learn ', '')
            result = learner.learn_everything(topic)
            print(f"\n{result['response']}")
        
        elif command == 'list':
            result = learner.get_all_knowledge()
            print(f"\n{result['response']}")
        
        elif command == 'stats':
            result = learner.get_statistics()
            print(f"\n{result['response']}")
    
    else:
        print("\nCommands:")
        print("  learn <topic>  - Learn everything about a topic")
        print("  list           - List all learned knowledge")
        print("  stats          - Show statistics")
        print("  exit           - Exit")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("[ROBOT] JARVIS: Goodbye!")
                    break
                
                if user_input.startswith('learn '):
                    topic = user_input.replace('learn ', '')
                    result = learner.learn_everything(topic)
                    print(f"\n[ROBOT] JARVIS: {result['response']}")
                
                elif user_input == 'list':
                    result = learner.get_all_knowledge()
                    print(f"\n[ROBOT] JARVIS: {result['response']}")
                
                elif user_input == 'stats':
                    result = learner.get_statistics()
                    print(f"\n[ROBOT] JARVIS: {result['response']}")
                
                else:
                    print("\n[ROBOT] JARVIS: Unknown command. Try 'learn <topic>', 'list', or 'stats'")
            
            except KeyboardInterrupt:
                print("\n\n[ROBOT] JARVIS: Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n[X] Error: {e}")
    
    learner.close()


if __name__ == "__main__":
    main()
