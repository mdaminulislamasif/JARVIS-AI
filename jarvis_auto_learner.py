"""
JARVIS AUTO LEARNER - NO LIMITS!
Automatically learns EVERYTHING word by word, paragraph by paragraph

Features:
- NO LIMITS - learns everything
- Word by word search
- Paragraph by paragraph learning
- Saves to own files
- Automatic learning
- Chrome + DevTools + Google
"""

import os
import sys
import time
import json
import sqlite3
import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class AutoLearner:
    """Auto learning system - NO LIMITS!"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.conn = None
        self.learning_folder = 'jarvis_learned_files'
        self.setup_database()
        self.create_learning_folder()
        
        print("🚀 JARVIS AUTO LEARNER - NO LIMITS!")
        print("🚀 JARVIS অটো শিক্ষার্থী - কোনো সীমা নেই!")
        
    def setup_database(self):
        """Setup database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create auto_learned table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auto_learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    paragraph TEXT NOT NULL,
                    file_path TEXT,
                    learned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    word_count INTEGER,
                    source TEXT
                )
            """)
            
            self.conn.commit()
            print("✅ Auto Learner database ready!")
            
        except Exception as e:
            print(f"⚠️ Database error: {e}")
    
    def create_learning_folder(self):
        """Create folder for learned files"""
        try:
            if not os.path.exists(self.learning_folder):
                os.makedirs(self.learning_folder)
                print(f"✅ Created learning folder: {self.learning_folder}")
        except Exception as e:
            print(f"⚠️ Folder creation error: {e}")
    
    def learn_word_by_word(self, text):
        """Learn text word by word"""
        print(f"\n📖 LEARNING WORD BY WORD...")
        print(f"📖 শব্দে শব্দে শিখছি...")
        
        # Split into words
        words = text.split()
        total_words = len(words)
        
        print(f"📊 Total words to learn: {total_words}")
        print(f"📊 মোট শেখার শব্দ: {total_words}")
        
        learned_words = []
        
        for i, word in enumerate(words, 1):
            # Clean word
            clean_word = re.sub(r'[^\w\s]', '', word).strip()
            
            if len(clean_word) > 2:  # Skip very short words
                print(f"[{i}/{total_words}] Learning: {clean_word}")
                
                # Search and learn this word
                result = self._search_word(clean_word)
                
                if result:
                    learned_words.append({
                        'word': clean_word,
                        'content': result
                    })
                
                time.sleep(0.5)  # Small delay
        
        return learned_words
    
    def _search_word(self, word):
        """Search and learn a single word"""
        try:
            # Try Wikipedia first
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{word}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    return data['extract']
            
            # Try Google search
            search_url = f"https://www.google.com/search?q={word}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get featured snippet
                featured = soup.find('div', class_='hgKElc')
                if featured:
                    return featured.get_text()
            
            return None
            
        except Exception as e:
            return None
    
    def learn_paragraph_by_paragraph(self, text):
        """Learn text paragraph by paragraph"""
        print(f"\n📄 LEARNING PARAGRAPH BY PARAGRAPH...")
        print(f"📄 প্যারাগ্রাফে প্যারাগ্রাফে শিখছি...")
        
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        total_paragraphs = len(paragraphs)
        
        print(f"📊 Total paragraphs: {total_paragraphs}")
        print(f"📊 মোট প্যারাগ্রাফ: {total_paragraphs}")
        
        learned_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs, 1):
            if paragraph.strip():
                print(f"\n[{i}/{total_paragraphs}] Learning paragraph...")
                print(f"Content: {paragraph[:100]}...")
                
                # Extract key words from paragraph
                words = paragraph.split()
                key_words = [w for w in words if len(w) > 5][:5]  # Top 5 long words
                
                # Search for each key word
                paragraph_knowledge = []
                for word in key_words:
                    clean_word = re.sub(r'[^\w\s]', '', word).strip()
                    result = self._search_word(clean_word)
                    if result:
                        paragraph_knowledge.append({
                            'word': clean_word,
                            'content': result
                        })
                
                learned_paragraphs.append({
                    'paragraph': paragraph,
                    'knowledge': paragraph_knowledge
                })
                
                time.sleep(1)  # Delay between paragraphs
        
        return learned_paragraphs
    
    def save_to_file(self, topic, content):
        """Save learned content to file"""
        try:
            # Create filename
            filename = f"{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(self.learning_folder, filename)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"JARVIS AUTO LEARNED CONTENT\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Date: {datetime.now()}\n")
                f.write(f"=" * 80 + "\n\n")
                f.write(content)
            
            print(f"✅ Saved to file: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ File save error: {e}")
            return None
    
    def auto_learn_everything(self, topic):
        """Automatically learn everything about a topic"""
        print(f"\n🚀 AUTO LEARNING EVERYTHING ABOUT: {topic}")
        print(f"🚀 সব কিছু স্বয়ংক্রিয়ভাবে শিখছি: {topic}")
        
        start_time = time.time()
        all_content = []
        
        try:
            # Step 1: Open Chrome and search
            print("\n🌐 Step 1: Opening Chrome and searching...")
            search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
            webbrowser.open(search_url)
            time.sleep(2)
            
            # Step 2: Learn from Wikipedia
            print("\n📚 Step 2: Learning from Wikipedia...")
            wiki_content = self._learn_from_wikipedia(topic)
            if wiki_content:
                all_content.append(f"=== WIKIPEDIA ===\n{wiki_content}\n\n")
                
                # Learn word by word from Wikipedia
                print("\n📖 Learning Wikipedia content word by word...")
                words = wiki_content.split()[:50]  # First 50 words
                for word in words:
                    clean_word = re.sub(r'[^\w\s]', '', word).strip()
                    if len(clean_word) > 3:
                        result = self._search_word(clean_word)
                        if result:
                            all_content.append(f"Word: {clean_word}\n{result}\n\n")
                            self._save_to_db(clean_word, result, "Wikipedia")
            
            # Step 3: Learn from Google
            print("\n🔍 Step 3: Learning from Google...")
            google_content = self._learn_from_google(topic)
            if google_content:
                all_content.append(f"=== GOOGLE ===\n{google_content}\n\n")
            
            # Step 4: Learn programming (if applicable)
            if self._is_programming_topic(topic):
                print("\n💻 Step 4: Learning programming concepts...")
                prog_content = self._learn_programming(topic)
                if prog_content:
                    all_content.append(f"=== PROGRAMMING ===\n{prog_content}\n\n")
            
            # Step 5: Save everything to file
            print("\n💾 Step 5: Saving to file...")
            full_content = '\n'.join(all_content)
            filepath = self.save_to_file(topic, full_content)
            
            # Step 6: Save to database
            print("\n💿 Step 6: Saving to database...")
            self._save_to_db(topic, full_content, "Auto Learning")
            
            duration = int(time.time() - start_time)
            word_count = len(full_content.split())
            
            return {
                'status': 'success',
                'response': f"""✅ AUTO LEARNED EVERYTHING ABOUT '{topic}'!
✅ '{topic}' সম্পর্কে সব কিছু স্বয়ংক্রিয়ভাবে শিখেছি!

📊 Learning Summary:
   • Duration: {duration} seconds
   • Total Words: {word_count}
   • File: {filepath}
   • Database: Updated
   
🌐 Chrome opened with search
📚 Learned from Wikipedia (word by word)
🔍 Learned from Google
💻 Learned programming concepts (if applicable)
💾 Saved to file: {filepath}
💿 Saved to database

NO LIMITS - EVERYTHING LEARNED!
কোনো সীমা নেই - সব কিছু শিখেছি!""",
                'type': 'auto_learning',
                'filepath': filepath,
                'words': word_count
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'response': f"❌ Auto learning error: {e}",
                'type': 'auto_learning'
            }
    
    def _learn_from_wikipedia(self, topic):
        """Learn from Wikipedia"""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    return data['extract']
            return None
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None
    
    def _learn_from_google(self, topic):
        """Learn from Google"""
        try:
            search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get featured snippet
                featured = soup.find('div', class_='hgKElc')
                if featured:
                    return featured.get_text()
                
                # Get search results
                results = soup.find_all('div', class_='BNeawe')
                if results:
                    return ' '.join([r.get_text() for r in results[:5]])
            
            return None
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None
    
    def _is_programming_topic(self, topic):
        """Check if programming topic"""
        programming_keywords = [
            'python', 'java', 'javascript', 'programming', 'code', 'coding',
            'software', 'algorithm', 'data structure', 'web development'
        ]
        return any(keyword in topic.lower() for keyword in programming_keywords)
    
    def _learn_programming(self, topic):
        """Learn programming"""
        try:
            so_url = f"https://stackoverflow.com/search?q={topic.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(so_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                summaries = soup.find_all('div', class_='s-post-summary--content')
                if summaries:
                    return ' '.join([s.get_text()[:200] for s in summaries[:3]])
            
            return None
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None
    
    def _save_to_db(self, word, content, source):
        """Save to database"""
        try:
            cursor = self.conn.cursor()
            word_count = len(content.split())
            
            cursor.execute("""
                INSERT INTO auto_learned (word, paragraph, word_count, source)
                VALUES (?, ?, ?, ?)
            """, (word, content, word_count, source))
            
            # Also save to knowledge_base
            cursor.execute("""
                INSERT OR REPLACE INTO knowledge_base (topic, content)
                VALUES (?, ?)
            """, (word, content))
            
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ DB save error: {e}")
    
    def list_learned_files(self):
        """List all learned files"""
        try:
            files = os.listdir(self.learning_folder)
            
            if files:
                response = f"📁 LEARNED FILES / শেখা ফাইল:\n\n"
                for i, file in enumerate(files, 1):
                    filepath = os.path.join(self.learning_folder, file)
                    size = os.path.getsize(filepath)
                    response += f"{i}. {file} ({size} bytes)\n"
                
                return {
                    'status': 'success',
                    'response': response,
                    'type': 'file_list',
                    'count': len(files)
                }
            else:
                return {
                    'status': 'info',
                    'response': "No files yet.\nএখনো কোনো ফাইল নেই।",
                    'type': 'file_list'
                }
        except Exception as e:
            return {
                'status': 'error',
                'response': f"Error: {e}",
                'type': 'file_list'
            }
    
    def close(self):
        """Close database"""
        if self.conn:
            self.conn.close()


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("  🚀 JARVIS AUTO LEARNER - NO LIMITS!")
    print("  🚀 JARVIS অটো শিক্ষার্থী - কোনো সীমা নেই!")
    print("  Learn everything word by word, paragraph by paragraph!")
    print("  শব্দে শব্দে, প্যারাগ্রাফে প্যারাগ্রাফে সব কিছু শিখুন!")
    print("=" * 80)
    
    learner = AutoLearner()
    
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        
        if command.startswith('learn '):
            topic = command.replace('learn ', '')
            result = learner.auto_learn_everything(topic)
            print(f"\n{result['response']}")
        
        elif command == 'list':
            result = learner.list_learned_files()
            print(f"\n{result['response']}")
    
    else:
        print("\nCommands:")
        print("  learn <topic>  - Auto learn everything")
        print("  list           - List learned files")
        print("  exit           - Exit")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("🤖 JARVIS: Goodbye!")
                    break
                
                if user_input.startswith('learn '):
                    topic = user_input.replace('learn ', '')
                    result = learner.auto_learn_everything(topic)
                    print(f"\n🤖 JARVIS: {result['response']}")
                
                elif user_input == 'list':
                    result = learner.list_learned_files()
                    print(f"\n🤖 JARVIS: {result['response']}")
                
                else:
                    print("\n🤖 JARVIS: Unknown command. Try 'learn <topic>' or 'list'")
            
            except KeyboardInterrupt:
                print("\n\n🤖 JARVIS: Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    learner.close()


if __name__ == "__main__":
    main()
