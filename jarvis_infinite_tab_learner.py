"""
JARVIS INFINITE TAB LEARNER
Infinite deep web crawling with multi-tab learning

Features:
- Search করে প্রতিটা result new tab এ open করে
- প্রতিটা page এর সব links new tab এ open করে
- প্রতিটা new tab এর আবার সব links new tab এ open করে
- INFINITE চলতে থাকে - কখনো থামে না!
- সব tabs থেকে learn করে
"""

import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import re

class InfiniteTabLearner:
    """Infinite tab learning system - opens ALL links in new tabs infinitely"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.conn = None
        self.driver = None
        self.opened_urls = set()  # Track opened URLs to avoid duplicates
        self.learned_content = []
        self.max_tabs = 50  # Maximum tabs at once (to prevent crash)
        self.is_learning = False
        self.setup_database()
        
        print("🚀 JARVIS INFINITE TAB LEARNER INITIALIZED!")
        print("🚀 JARVIS অসীম ট্যাব শিক্ষার্থী চালু হয়েছে!")
    
    def setup_database(self):
        """Setup database for storing learned content"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS infinite_learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    title TEXT,
                    content TEXT,
                    links_found INTEGER,
                    learned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    depth_level INTEGER
                )
            """)
            
            self.conn.commit()
            print("✅ Infinite Tab Learner database ready!")
            
        except Exception as e:
            print(f"⚠️ Database error: {e}")
    
    def start_infinite_learning(self, search_query):
        """
        Start infinite learning process:
        1. Search করে
        2. প্রতিটা result new tab এ open করে
        3. প্রতিটা page এর সব links new tab এ open করে
        4. INFINITE চলতে থাকে!
        """
        print(f"\n🔥 STARTING INFINITE TAB LEARNING FOR: {search_query}")
        print(f"🔥 অসীম ট্যাব শেখা শুরু হচ্ছে: {search_query}")
        
        self.is_learning = True
        
        # Setup Chrome with options
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Comment out to see tabs
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome browser started!")
            
            # Step 1: Search on Google
            print(f"\n🔍 Step 1: Searching Google for: {search_query}")
            self.driver.get('https://www.google.com')
            time.sleep(2)
            
            # Find search box and search
            search_box = self.driver.find_element(By.NAME, 'q')
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            
            # Step 2: Open ALL search results in new tabs
            print(f"\n📂 Step 2: Opening ALL search results in new tabs...")
            self._open_all_search_results_in_tabs()
            
            # Step 3: Start infinite tab opening loop
            print(f"\n♾️ Step 3: Starting INFINITE tab opening loop...")
            self._infinite_tab_opening_loop()
            
        except Exception as e:
            print(f"❌ Error in infinite learning: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            if self.driver:
                print("\n⚠️ Stopping infinite learning...")
                # Don't close driver - let it run infinitely!
                # self.driver.quit()
    
    def _open_all_search_results_in_tabs(self):
        """Open ALL Google search results in new tabs (NO DUPLICATES)"""
        try:
            # Get all search result links
            search_results = self.driver.find_elements(By.CSS_SELECTOR, 'div.g a')
            
            links_to_open = []
            for result in search_results:
                try:
                    href = result.get_attribute('href')
                    
                    # Normalize URL (remove trailing slash, query params for duplicate check)
                    normalized_url = self._normalize_url(href)
                    
                    if href and href.startswith('http') and normalized_url not in self.opened_urls:
                        links_to_open.append(href)
                        self.opened_urls.add(normalized_url)
                except Exception as e:

                    print(f"⚠️ Error: {e}")
                    continue
            
            print(f"✅ Found {len(links_to_open)} UNIQUE search results to open")
            print(f"✅ {len(links_to_open)}টি UNIQUE search results পাওয়া গেছে")
            
            # Open each link in new tab
            for i, link in enumerate(links_to_open, 1):
                try:
                    print(f"  [{i}/{len(links_to_open)}] Opening: {link[:80]}...")
                    
                    # Open in new tab
                    self.driver.execute_script(f"window.open('{link}', '_blank');")
                    time.sleep(0.5)  # Small delay between tabs
                    
                except Exception as e:
                    print(f"    ⚠️ Error opening tab: {e}")
                    continue
            
            print(f"✅ Opened {len(links_to_open)} UNIQUE tabs from search results!")
            print(f"✅ {len(links_to_open)}টি UNIQUE ট্যাব খোলা হয়েছে!")
            
        except Exception as e:
            print(f"❌ Error opening search results: {e}")
    
    def _infinite_tab_opening_loop(self):
        """
        INFINITE LOOP:
        - প্রতিটা tab visit করে
        - সব links খুঁজে বের করে
        - সব links new tab এ open করে
        - আবার নতুন tabs visit করে
        - এভাবে INFINITE চলতে থাকে!
        """
        depth_level = 0
        
        while self.is_learning:
            try:
                depth_level += 1
                print(f"\n🌊 DEPTH LEVEL {depth_level} - Processing all tabs...")
                print(f"🌊 গভীরতা স্তর {depth_level} - সব ট্যাব প্রসেস করছি...")
                
                # Get all window handles (tabs)
                all_tabs = self.driver.window_handles
                total_tabs = len(all_tabs)
                
                print(f"📊 Total tabs open: {total_tabs}")
                print(f"📊 মোট খোলা ট্যাব: {total_tabs}")
                
                # If too many tabs, close some old ones
                if total_tabs > self.max_tabs:
                    print(f"⚠️ Too many tabs ({total_tabs}), closing oldest {total_tabs - self.max_tabs} tabs...")
                    tabs_to_close = total_tabs - self.max_tabs
                    for i in range(tabs_to_close):
                        try:
                            self.driver.switch_to.window(all_tabs[i])
                            self.driver.close()
                        except Exception as e:

                            print(f"⚠️ Error: {e}")
                            pass
                    
                    # Refresh tab list
                    all_tabs = self.driver.window_handles
                    total_tabs = len(all_tabs)
                
                # Process each tab
                for tab_index, tab_handle in enumerate(all_tabs, 1):
                    try:
                        print(f"\n  🔍 Processing Tab {tab_index}/{total_tabs}...")
                        
                        # Switch to this tab
                        self.driver.switch_to.window(tab_handle)
                        time.sleep(1)
                        
                        # Get current URL
                        current_url = self.driver.current_url
                        normalized_current = self._normalize_url(current_url)
                        
                        # Skip if already processed (DUPLICATE PREVENTION)
                        if normalized_current in self.opened_urls:
                            print(f"    ⏭️ SKIPPED (already processed): {current_url[:80]}")
                            continue
                        
                        self.opened_urls.add(normalized_current)
                        
                        print(f"    📄 NEW URL: {current_url[:80]}...")
                        
                        # Learn from this page
                        self._learn_from_current_page(depth_level)
                        
                        # Find ALL links on this page
                        links = self._find_all_links_on_page()
                        
                        print(f"    🔗 Found {len(links)} links on this page")
                        
                        # Open ALL links in new tabs
                        self._open_links_in_new_tabs(links)
                        
                    except Exception as e:
                        print(f"    ⚠️ Error processing tab: {e}")
                        continue
                
                print(f"\n✅ Completed depth level {depth_level}")
                print(f"✅ গভীরতা স্তর {depth_level} সম্পন্ন হয়েছে")
                print(f"📊 Total URLs opened so far: {len(self.opened_urls)}")
                print(f"📊 এখন পর্যন্ত মোট খোলা URL: {len(self.opened_urls)}")
                
                # Small delay before next depth level
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error in infinite loop: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(5)
                continue
    
    def _find_all_links_on_page(self):
        """Find ALL links on current page (NO DUPLICATES)"""
        links = []
        
        try:
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find all <a> tags
            all_a_tags = soup.find_all('a', href=True)
            
            for a_tag in all_a_tags:
                href = a_tag['href']
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    current_url = self.driver.current_url
                    base_url = '/'.join(current_url.split('/')[:3])
                    href = base_url + href
                
                # Normalize URL for duplicate check
                normalized_url = self._normalize_url(href)
                
                # Only add valid HTTP/HTTPS links that haven't been opened
                if href.startswith('http') and normalized_url not in self.opened_urls:
                    links.append(href)
            
        except Exception as e:
            print(f"      ⚠️ Error finding links: {e}")
        
        return links
    
    def _normalize_url(self, url):
        """
        Normalize URL to detect duplicates
        URL normalize করে duplicate detect করার জন্য
        
        Examples:
        - https://example.com/ → https://example.com
        - https://example.com?utm=123 → https://example.com
        - https://example.com#section → https://example.com
        """
        if not url:
            return ""
        
        try:
            # Remove trailing slash
            url = url.rstrip('/')
            
            # Remove query parameters (everything after ?)
            if '?' in url:
                url = url.split('?')[0]
            
            # Remove fragments (everything after #)
            if '#' in url:
                url = url.split('#')[0]
            
            # Convert to lowercase for case-insensitive comparison
            url = url.lower()
            
            return url
            
        except Exception as e:

            
            print(f"⚠️ Error: {e}")
            return url
    
    def _open_links_in_new_tabs(self, links):
        """Open ALL links in new tabs (NO DUPLICATES - একটা link একবারই open হবে)"""
        if not links:
            return
        
        # Limit links per page to prevent explosion
        max_links_per_page = 10
        links_to_open = links[:max_links_per_page]
        
        print(f"      📂 Opening {len(links_to_open)} UNIQUE links in new tabs...")
        print(f"      📂 {len(links_to_open)}টি UNIQUE link নতুন ট্যাবে খুলছি...")
        
        opened_count = 0
        skipped_count = 0
        
        for i, link in enumerate(links_to_open, 1):
            try:
                # Normalize URL for duplicate check
                normalized_url = self._normalize_url(link)
                
                # Check if we already opened this (DUPLICATE PREVENTION)
                if normalized_url in self.opened_urls:
                    skipped_count += 1
                    print(f"        ⏭️ [{i}/{len(links_to_open)}] SKIPPED (duplicate): {link[:60]}...")
                    continue
                
                print(f"        ✅ [{i}/{len(links_to_open)}] Opening: {link[:60]}...")
                
                # Open in new tab
                self.driver.execute_script(f"window.open('{link}', '_blank');")
                self.opened_urls.add(normalized_url)
                opened_count += 1
                
                time.sleep(0.3)  # Small delay
                
            except Exception as e:
                print(f"          ⚠️ Error opening link: {e}")
                continue
        
        print(f"      ✅ Opened {opened_count} new tabs, skipped {skipped_count} duplicates")
        print(f"      ✅ {opened_count}টি নতুন ট্যাব খোলা হয়েছে, {skipped_count}টি duplicate skip করা হয়েছে")
    
    def _learn_from_current_page(self, depth_level):
        """Learn content from current page"""
        try:
            # Get page title
            title = self.driver.title
            
            # Get page text content
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
            
            # Limit text length
            text = text[:5000]
            
            # Count links found
            links_found = len(self._find_all_links_on_page())
            
            # Save to database
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO infinite_learned (url, title, content, links_found, depth_level)
                VALUES (?, ?, ?, ?, ?)
            """, (self.driver.current_url, title, text, links_found, depth_level))
            self.conn.commit()
            
            print(f"      ✅ Learned from: {title[:50]}... (Links: {links_found})")
            
        except Exception as e:
            print(f"      ⚠️ Error learning from page: {e}")
    
    def stop_learning(self):
        """Stop infinite learning"""
        print("\n🛑 Stopping infinite learning...")
        self.is_learning = False
        
        if self.driver:
            self.driver.quit()
        
        print(f"✅ Stopped! Total URLs learned: {len(self.opened_urls)}")
    
    def get_statistics(self):
        """Get learning statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total learned
            cursor.execute("SELECT COUNT(*) FROM infinite_learned")
            total_learned = cursor.fetchone()[0]
            
            # Total links found
            cursor.execute("SELECT SUM(links_found) FROM infinite_learned")
            total_links = cursor.fetchone()[0] or 0
            
            # Max depth reached
            cursor.execute("SELECT MAX(depth_level) FROM infinite_learned")
            max_depth = cursor.fetchone()[0] or 0
            
            stats = f"""
📊 INFINITE TAB LEARNING STATISTICS:
📊 অসীম ট্যাব শেখার পরিসংখ্যান:

✅ Total pages learned: {total_learned}
✅ মোট শেখা পৃষ্ঠা: {total_learned}

🔗 Total links found: {total_links}
🔗 মোট পাওয়া লিংক: {total_links}

🌊 Maximum depth reached: {max_depth}
🌊 সর্বোচ্চ গভীরতা: {max_depth}

📂 Currently opened URLs: {len(self.opened_urls)}
📂 বর্তমানে খোলা URL: {len(self.opened_urls)}
"""
            
            return {
                'status': 'success',
                'response': stats,
                'type': 'statistics',
                'data': {
                    'total_learned': total_learned,
                    'total_links': total_links,
                    'max_depth': max_depth,
                    'opened_urls': len(self.opened_urls)
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'response': f'Error getting statistics: {e}',
                'type': 'statistics'
            }


# Test function
if __name__ == "__main__":
    print("🚀 TESTING INFINITE TAB LEARNER...")
    
    learner = InfiniteTabLearner()
    
    # Start infinite learning
    search_query = input("Enter search query (or press Enter for 'Python programming'): ").strip()
    if not search_query:
        search_query = "Python programming"
    
    print(f"\n🔥 Starting infinite learning for: {search_query}")
    print("⚠️ Press Ctrl+C to stop...")
    
    try:
        learner.start_infinite_learning(search_query)
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user!")
        learner.stop_learning()
    
    # Show statistics
    stats = learner.get_statistics()
    print(stats['response'])
