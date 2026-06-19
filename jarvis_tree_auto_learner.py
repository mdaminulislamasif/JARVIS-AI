"""
JARVIS TREE AUTO LEARNER
Tree Learning + Auto Learning = Automatic New Tab Opening with Learning

Features:
- Tree structure এ tabs open করে
- প্রতিটা tab automatically learn করে
- Word by word, paragraph by paragraph শেখে
- New tabs automatically open হয়
- NO DUPLICATES - একটা link একবারই open হবে
"""

import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

class TreeAutoLearner:
    """Tree structure with automatic learning - Auto opens new tabs and learns"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.conn = None
        self.driver = None
        self.opened_urls = set()  # Track opened URLs (NO DUPLICATES)
        self.learned_content = []
        self.is_learning = False
        self.max_depth = 5  # Maximum tree depth
        self.max_children_per_node = 10  # Maximum children per node
        self.auto_learn_enabled = True  # Auto learning enabled
        self.setup_database()
        
        print("🌳🤖 JARVIS TREE AUTO LEARNER INITIALIZED!")
        print("🌳🤖 JARVIS ট্রি অটো শিক্ষার্থী চালু হয়েছে!")
        print("🌳 Tree Structure + 🤖 Auto Learning = Perfect!")
    
    def setup_database(self):
        """Setup database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tree_auto_learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    parent_url TEXT,
                    depth_level INTEGER,
                    title TEXT,
                    content TEXT,
                    word_count INTEGER,
                    paragraph_count INTEGER,
                    children_count INTEGER,
                    learned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
            print("✅ Tree Auto Learner database ready!")
            
        except Exception as e:
            print(f"⚠️ Database error: {e}")
    
    def start_tree_auto_learning(self, search_query):
        """
        Start tree auto learning:
        
        1. Search করে
        2. প্রতিটা result new tab এ open করে
        3. প্রতিটা tab automatically learn করে (word by word)
        4. প্রতিটা page এর links new tab এ open করে
        5. Tree structure এ organize করে
        6. Automatically চলতে থাকে!
        """
        print(f"\n🌳🤖 STARTING TREE AUTO LEARNING FOR: {search_query}")
        print(f"🌳🤖 ট্রি অটো শেখা শুরু হচ্ছে: {search_query}")
        
        self.is_learning = True
        
        # Setup Chrome
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome browser started!")
            
            # Level 0: Search
            print(f"\n🔍 LEVEL 0: Searching Google...")
            self.driver.get('https://www.google.com')
            time.sleep(2)
            
            # Find search box and search
            search_box = self.driver.find_element(By.NAME, 'q')
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            
            # Get search results (Level 0 nodes)
            search_results = self._get_search_results()
            
            print(f"\n✅ LEVEL 0: Found {len(search_results)} search results")
            print(f"   Results: {', '.join([r['name'] for r in search_results[:10]])}")
            
            # Process tree level by level with auto learning
            self._process_tree_level_with_auto_learning(search_results, depth=1, parent_name='Search')
            
        except Exception as e:
            print(f"❌ Error in tree auto learning: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if self.driver:
                print("\n⚠️ Tree auto learning complete!")
                # Don't close - let user see the tree
                # self.driver.quit()
    
    def _get_search_results(self):
        """Get search results (Level 0)"""
        results = []
        
        try:
            search_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.g a')
            
            for i, element in enumerate(search_elements[:10], 1):  # Top 10 results
                try:
                    href = element.get_attribute('href')
                    if href and href.startswith('http'):
                        normalized = self._normalize_url(href)
                        
                        if normalized not in self.opened_urls:
                            results.append({
                                'url': href,
                                'normalized': normalized,
                                'name': chr(96 + i) if i <= 26 else str(i),  # a, b, c... or numbers
                                'depth': 0
                            })
                            self.opened_urls.add(normalized)
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    continue
        
        except Exception as e:
            print(f"⚠️ Error getting search results: {e}")
        
        return results
    
    def _process_tree_level_with_auto_learning(self, nodes, depth, parent_name):
        """
        Process one level of the tree WITH AUTO LEARNING
        
        For each node:
        1. Open in new tab
        2. AUTO LEARN from page (word by word, paragraph by paragraph)
        3. Get all links (children)
        4. Recursively process children
        """
        if depth > self.max_depth:
            print(f"\n⚠️ Maximum depth {self.max_depth} reached!")
            return
        
        if not self.is_learning:
            return
        
        print(f"\n{'  ' * depth}🌳 LEVEL {depth}: Processing {len(nodes)} nodes with AUTO LEARNING...")
        
        for node_index, node in enumerate(nodes, 1):
            try:
                node_name = node.get('name', f'Node{node_index}')
                node_url = node['url']
                
                print(f"\n{'  ' * depth}📂 [{node_index}/{len(nodes)}] Opening: {node_name} → {node_url[:60]}...")
                
                # Open in new tab
                self.driver.execute_script(f"window.open('{node_url}', '_blank');")
                time.sleep(1)
                
                # Switch to new tab
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(2)
                
                # 🤖 AUTO LEARN from this page
                print(f"{'  ' * depth}   🤖 AUTO LEARNING from page...")
                learned_data = self._auto_learn_from_page(node_url, depth)
                
                # Get page title
                try:
                    title = self.driver.title
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    title = node_name
                
                # Find all links on this page (children)
                children = self._find_children_links(node_url, depth)
                
                print(f"{'  ' * depth}   ✅ Learned: {learned_data['word_count']} words, {learned_data['paragraph_count']} paragraphs")
                print(f"{'  ' * depth}   ✅ Found {len(children)} children for {node_name}")
                
                if children:
                    print(f"{'  ' * depth}   Children: {', '.join([c['name'] for c in children[:5]])}{'...' if len(children) > 5 else ''}")
                
                # Save to database
                self._save_to_database(node_url, node.get('parent_url'), depth, title, 
                                      learned_data['content'], learned_data['word_count'], 
                                      learned_data['paragraph_count'], len(children))
                
                # Recursively process children (next level) with auto learning
                if children and depth < self.max_depth:
                    # Add parent_url to children
                    for child in children:
                        child['parent_url'] = node_url
                    
                    self._process_tree_level_with_auto_learning(children, depth + 1, node_name)
                
                # Close this tab (keep tree clean)
                self.driver.close()
                
                # Switch back to first tab
                self.driver.switch_to.window(self.driver.window_handles[0])
                
            except Exception as e:
                print(f"{'  ' * depth}   ⚠️ Error processing node: {e}")
                continue
    
    def _auto_learn_from_page(self, url, depth):
        """
        AUTO LEARN from current page
        Word by word, paragraph by paragraph
        """
        try:
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Count words
            words = text.split()
            word_count = len(words)
            
            # Count paragraphs
            paragraphs = [p for p in text.split('\n\n') if p.strip()]
            paragraph_count = len(paragraphs)
            
            # Limit content length
            content = text[:5000]  # First 5000 characters
            
            return {
                'content': content,
                'word_count': word_count,
                'paragraph_count': paragraph_count
            }
            
        except Exception as e:
            print(f"      ⚠️ Auto learning error: {e}")
            return {
                'content': '',
                'word_count': 0,
                'paragraph_count': 0
            }
    
    def _find_children_links(self, parent_url, current_depth):
        """Find all child links on current page"""
        children = []
        
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            all_links = soup.find_all('a', href=True)
            
            child_index = 1
            for a_tag in all_links:
                if len(children) >= self.max_children_per_node:
                    break
                
                href = a_tag['href']
                
                # Convert relative to absolute
                if href.startswith('/'):
                    base_url = '/'.join(parent_url.split('/')[:3])
                    href = base_url + href
                
                # Only HTTP/HTTPS
                if not href.startswith('http'):
                    continue
                
                # Normalize
                normalized = self._normalize_url(href)
                
                # Check duplicate
                if normalized in self.opened_urls:
                    continue
                
                # Add as child
                children.append({
                    'url': href,
                    'normalized': normalized,
                    'name': str(child_index),  # 1, 2, 3, 4, 5...
                    'depth': current_depth + 1,
                    'parent_url': parent_url
                })
                
                self.opened_urls.add(normalized)
                child_index += 1
        
        except Exception as e:
            print(f"      ⚠️ Error finding children: {e}")
        
        return children
    
    def _normalize_url(self, url):
        """Normalize URL to detect duplicates"""
        if not url:
            return ""
        
        try:
            url = url.rstrip('/')
            if '?' in url:
                url = url.split('?')[0]
            if '#' in url:
                url = url.split('#')[0]
            url = url.lower()
            return url
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return url
    
    def _save_to_database(self, url, parent_url, depth, title, content, word_count, paragraph_count, children_count):
        """Save to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO tree_auto_learned 
                (url, parent_url, depth_level, title, content, word_count, paragraph_count, children_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (url, parent_url, depth, title, content, word_count, paragraph_count, children_count))
            self.conn.commit()
        except Exception as e:
            print(f"      ⚠️ Database save error: {e}")
    
    def stop_learning(self):
        """Stop tree auto learning"""
        print("\n🛑 Stopping tree auto learning...")
        self.is_learning = False
        
        if self.driver:
            self.driver.quit()
        
        print(f"✅ Stopped! Total URLs learned: {len(self.opened_urls)}")
    
    def get_statistics(self):
        """Get tree auto learning statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total nodes
            cursor.execute("SELECT COUNT(*) FROM tree_auto_learned")
            total_nodes = cursor.fetchone()[0]
            
            # Total words learned
            cursor.execute("SELECT SUM(word_count) FROM tree_auto_learned")
            total_words = cursor.fetchone()[0] or 0
            
            # Total paragraphs learned
            cursor.execute("SELECT SUM(paragraph_count) FROM tree_auto_learned")
            total_paragraphs = cursor.fetchone()[0] or 0
            
            # Nodes by depth
            cursor.execute("""
                SELECT depth_level, COUNT(*), SUM(word_count)
                FROM tree_auto_learned 
                GROUP BY depth_level 
                ORDER BY depth_level
            """)
            depth_stats = cursor.fetchall()
            
            stats = f"""
🌳🤖 TREE AUTO LEARNING STATISTICS:
🌳🤖 ট্রি অটো শেখার পরিসংখ্যান:

📊 Total nodes learned: {total_nodes}
📊 মোট nodes শেখা হয়েছে: {total_nodes}

📝 Total words learned: {total_words:,}
📝 মোট words শেখা হয়েছে: {total_words:,}

📄 Total paragraphs learned: {total_paragraphs:,}
📄 মোট paragraphs শেখা হয়েছে: {total_paragraphs:,}

🌊 Nodes by depth level:
"""
            
            for depth, count, words in depth_stats:
                stats += f"   Level {depth}: {count} nodes ({words:,} words)\n"
            
            stats += f"""
📂 Unique URLs opened: {len(self.opened_urls)}
📂 Unique URLs খোলা হয়েছে: {len(self.opened_urls)}

🌳 Tree Structure + 🤖 Auto Learning = Perfect Knowledge!
"""
            
            return {
                'status': 'success',
                'response': stats,
                'type': 'statistics'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'response': f'Error: {e}',
                'type': 'statistics'
            }


# Test
if __name__ == "__main__":
    print("🌳🤖 TESTING TREE AUTO LEARNER...")
    
    learner = TreeAutoLearner()
    
    search_query = input("Enter search query (or press Enter for 'Python'): ").strip()
    if not search_query:
        search_query = "Python"
    
    print(f"\n🌳🤖 Starting tree auto learning for: {search_query}")
    print("⚠️ Press Ctrl+C to stop...")
    
    try:
        learner.start_tree_auto_learning(search_query)
        
        # Show statistics
        stats = learner.get_statistics()
        print(stats['response'])
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user!")
        learner.stop_learning()
