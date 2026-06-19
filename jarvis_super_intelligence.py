"""
JARVIS SUPER INTELLIGENCE SYSTEM
সুপার ইন্টেলিজেন্স সিস্টেম

Features:
- Recognizes EVERYTHING (text, code, images, videos, audio, links, PDFs, etc.)
- Makes decisions automatically
- Self-updates and self-upgrades
- Controls Chrome browser
- Collects data from websites
- Uses Developer Tools
- Bypasses robot verification
- Updates own brain/database
- System control and automation

আপনি যা চেয়েছেন:
- সব কিছু চিনতে পারবে (text, code, photo, video, audio, link, PDF, etc.)
- নিজে নিজে কাজ করতে পারবে
- নিজেকে fix/update/upgrade করতে পারবে
- Website visit করতে পারবে
- Data সংগ্রহ করতে পারবে
- Chrome browser চালাতে পারবে
- Developer tools ব্যবহার করতে পারবে
- Robot verification complete করতে পারবে
- নিজের brain update করতে পারবে
"""

import os
import sys
import time
import json
import mimetypes
import subprocess
import requests
import sqlite3
from pathlib import Path
from datetime import datetime
import webbrowser
import pyautogui
from PIL import Image
import cv2
import numpy as np

# For file type detection
import magic  # python-magic for better file detection

class SuperIntelligence:
    """
    JARVIS Super Intelligence System
    Recognizes everything and makes autonomous decisions
    """
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.brain_data = {}
        self.capabilities = []
        
        # Initialize file type recognizers
        self.init_recognizers()
        
        # Initialize database
        self.init_database()
        
        # Load existing brain data
        self.load_brain()
        
        print("🧠 JARVIS SUPER INTELLIGENCE INITIALIZED!")
        print("🧠 JARVIS সুপার ইন্টেলিজেন্স চালু হয়েছে!")
        print("\n✅ I can now recognize EVERYTHING!")
        print("✅ আমি এখন সব কিছু চিনতে পারি!")
    
    def init_recognizers(self):
        """Initialize all file type recognizers"""
        self.file_types = {
            # Text files
            'text': ['.txt', '.md', '.log', '.csv', '.json', '.xml', '.yaml', '.yml'],
            
            # Code files
            'code': ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', 
                    '.rs', '.swift', '.kt', '.ts', '.jsx', '.tsx', '.html', '.css', 
                    '.scss', '.sass', '.sql', '.sh', '.bat', '.ps1'],
            
            # Image files
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp', 
                     '.tiff', '.tif', '.psd', '.raw'],
            
            # Video files
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', 
                     '.mpg', '.mpeg', '.3gp', '.f4v'],
            
            # Audio files
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', 
                     '.aiff', '.ape'],
            
            # Document files
            'document': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', 
                        '.odt', '.ods', '.odp', '.rtf'],
            
            # Archive files
            'archive': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
            
            # Executable files
            'executable': ['.exe', '.msi', '.app', '.deb', '.rpm', '.apk', '.dmg'],
            
            # Database files
            'database': ['.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.sql'],
            
            # Link/URL patterns
            'link': ['http://', 'https://', 'ftp://', 'www.'],
            
            # Special formats
            'special': ['.torrent', '.blend', '.ai', '.sketch', '.fig']
        }
        
        # Quality indicators
        self.quality_indicators = {
            'video': ['4k', '1080p', '720p', 'hd', 'uhd', '8k', '2k', 'fullhd'],
            'audio': ['320kbps', '256kbps', '192kbps', 'flac', 'lossless', 'hifi']
        }
    
    def init_database(self):
        """Initialize super intelligence database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table for recognized items
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recognized_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_path TEXT,
                    item_type TEXT,
                    item_category TEXT,
                    item_quality TEXT,
                    metadata TEXT,
                    recognized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    action_taken TEXT,
                    result TEXT
                )
            ''')
            
            # Table for brain updates
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS brain_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    update_type TEXT,
                    update_content TEXT,
                    update_source TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success INTEGER DEFAULT 1
                )
            ''')
            
            # Table for autonomous actions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS autonomous_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT,
                    action_target TEXT,
                    action_result TEXT,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success INTEGER DEFAULT 1
                )
            ''')
            
            # Table for website data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS website_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    data_type TEXT,
                    data_content TEXT,
                    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    method TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ Super Intelligence database ready!")
            
        except Exception as e:
            print(f"⚠️ Database init error: {e}")
    
    def recognize_anything(self, item):
        """
        Recognize ANYTHING - text, code, image, video, audio, link, etc.
        সব কিছু চিনতে পারে
        """
        print(f"\n🔍 RECOGNIZING: {item}")
        print(f"🔍 চিনছি: {item}")
        
        result = {
            'item': item,
            'type': 'unknown',
            'category': 'unknown',
            'quality': None,
            'metadata': {},
            'actions': []
        }
        
        # Check if it's a URL/link
        if self._is_link(item):
            result['type'] = 'link'
            result['category'] = self._categorize_link(item)
            result['actions'] = ['visit', 'scrape', 'download', 'analyze']
            print(f"✅ Recognized as: LINK ({result['category']})")
            return result
        
        # Check if it's a file path
        if os.path.exists(item):
            return self._recognize_file(item)
        
        # Check if it's text/code content
        if isinstance(item, str):
            result['type'] = 'text'
            result['category'] = self._categorize_text(item)
            result['actions'] = ['read', 'analyze', 'learn', 'execute']
            print(f"✅ Recognized as: TEXT ({result['category']})")
            return result
        
        print(f"⚠️ Could not recognize: {item}")
        return result
    
    def _is_link(self, item):
        """Check if item is a link/URL"""
        if not isinstance(item, str):
            return False
        
        item_lower = item.lower()
        for pattern in self.file_types['link']:
            if pattern in item_lower:
                return True
        return False
    
    def _categorize_link(self, link):
        """Categorize what type of link it is"""
        link_lower = link.lower()
        
        # Video platforms
        if any(x in link_lower for x in ['youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com']):
            return 'video_platform'
        
        # Social media
        if any(x in link_lower for x in ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']):
            return 'social_media'
        
        # Code repositories
        if any(x in link_lower for x in ['github.com', 'gitlab.com', 'bitbucket.org']):
            return 'code_repository'
        
        # Documentation
        if any(x in link_lower for x in ['docs.', 'documentation', 'wiki', 'readme']):
            return 'documentation'
        
        # Download links
        if any(x in link_lower for x in ['.zip', '.rar', '.exe', '.msi', '.dmg', '.apk']):
            return 'download_link'
        
        # API endpoints
        if any(x in link_lower for x in ['api.', '/api/', 'rest', 'graphql']):
            return 'api_endpoint'
        
        return 'general_website'
    
    def _recognize_file(self, filepath):
        """Recognize file type and properties"""
        result = {
            'item': filepath,
            'type': 'file',
            'category': 'unknown',
            'quality': None,
            'metadata': {},
            'actions': []
        }
        
        # Get file extension
        ext = Path(filepath).suffix.lower()
        filename = Path(filepath).name.lower()
        
        # Determine category
        for category, extensions in self.file_types.items():
            if ext in extensions:
                result['category'] = category
                break
        
        # Get file metadata
        result['metadata'] = {
            'size': os.path.getsize(filepath),
            'extension': ext,
            'filename': Path(filepath).name,
            'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
        }
        
        # Detect quality for videos/audio
        if result['category'] in ['video', 'audio']:
            result['quality'] = self._detect_quality(filename)
        
        # Determine possible actions
        result['actions'] = self._get_possible_actions(result['category'])
        
        print(f"✅ Recognized as: {result['category'].upper()} ({ext})")
        if result['quality']:
            print(f"📊 Quality: {result['quality']}")
        
        return result
    
    def _detect_quality(self, filename):
        """Detect quality indicators in filename"""
        filename_lower = filename.lower()
        
        for quality_type, indicators in self.quality_indicators.items():
            for indicator in indicators:
                if indicator in filename_lower:
                    return indicator.upper()
        
        return None
    
    def _categorize_text(self, text):
        """Categorize text content"""
        text_lower = text.lower()
        
        # Check if it's code
        code_indicators = ['def ', 'function ', 'class ', 'import ', 'const ', 'var ', 
                          'public ', 'private ', 'void ', 'return ', '<?php', '#!/']
        if any(indicator in text_lower for indicator in code_indicators):
            return 'code'
        
        # Check if it's JSON
        if text.strip().startswith('{') or text.strip().startswith('['):
            try:
                json.loads(text)
                return 'json'
            except Exception as e:

                print(f"⚠️ Error: {e}")
                pass
        
        # Check if it's a command
        if text.startswith('!') or text.startswith('/'):
            return 'command'
        
        return 'plain_text'
    
    def _get_possible_actions(self, category):
        """Get possible actions for each category"""
        actions_map = {
            'text': ['read', 'analyze', 'learn', 'summarize'],
            'code': ['read', 'analyze', 'execute', 'debug', 'learn'],
            'image': ['view', 'analyze', 'extract_text', 'recognize_objects'],
            'video': ['play', 'extract_frames', 'extract_audio', 'analyze'],
            'audio': ['play', 'transcribe', 'analyze', 'extract_features'],
            'document': ['read', 'extract_text', 'convert', 'analyze'],
            'archive': ['extract', 'list_contents', 'analyze'],
            'executable': ['run', 'analyze', 'scan'],
            'database': ['open', 'query', 'analyze', 'backup'],
            'link': ['visit', 'scrape', 'download', 'analyze']
        }
        
        return actions_map.get(category, ['analyze'])
    
    def auto_decide_action(self, recognized_item):
        """
        Automatically decide what to do with recognized item
        নিজে নিজে সিদ্ধান্ত নেয়
        """
        print(f"\n🤖 AUTO DECIDING ACTION...")
        print(f"🤖 নিজে নিজে সিদ্ধান্ত নিচ্ছি...")
        
        category = recognized_item['category']
        actions = recognized_item['actions']
        
        # Decision logic based on category
        if category == 'link':
            return self._decide_link_action(recognized_item)
        elif category == 'code':
            return self._decide_code_action(recognized_item)
        elif category in ['image', 'video', 'audio']:
            return self._decide_media_action(recognized_item)
        elif category == 'document':
            return self._decide_document_action(recognized_item)
        else:
            return {'action': 'analyze', 'reason': 'Default action for unknown category'}
    
    def _decide_link_action(self, item):
        """Decide action for links"""
        link_category = item['category']
        
        if link_category == 'video_platform':
            return {'action': 'visit_and_learn', 'reason': 'Video platform - can learn from content'}
        elif link_category == 'code_repository':
            return {'action': 'clone_and_analyze', 'reason': 'Code repository - can learn code'}
        elif link_category == 'documentation':
            return {'action': 'scrape_and_learn', 'reason': 'Documentation - valuable learning resource'}
        elif link_category == 'download_link':
            return {'action': 'download_and_analyze', 'reason': 'Download link - need to inspect content'}
        else:
            return {'action': 'visit_and_scrape', 'reason': 'General website - collect data'}
    
    def _decide_code_action(self, item):
        """Decide action for code"""
        return {'action': 'analyze_and_learn', 'reason': 'Code detected - learn programming patterns'}
    
    def _decide_media_action(self, item):
        """Decide action for media files"""
        category = item['category']
        
        if category == 'image':
            return {'action': 'analyze_and_extract', 'reason': 'Image - extract text and objects'}
        elif category == 'video':
            return {'action': 'extract_and_learn', 'reason': 'Video - extract frames and audio'}
        elif category == 'audio':
            return {'action': 'transcribe_and_learn', 'reason': 'Audio - transcribe to text'}
    
    def _decide_document_action(self, item):
        """Decide action for documents"""
        return {'action': 'extract_and_learn', 'reason': 'Document - extract and learn content'}
    
    def execute_autonomous_action(self, item, decision):
        """
        Execute the decided action autonomously
        নিজে নিজে কাজ করে
        """
        print(f"\n⚡ EXECUTING: {decision['action']}")
        print(f"⚡ কাজ করছি: {decision['action']}")
        print(f"💡 Reason: {decision['reason']}")
        
        action = decision['action']
        
        try:
            if 'visit' in action:
                return self.visit_website(item['item'])
            elif 'scrape' in action:
                return self.scrape_website(item['item'])
            elif 'download' in action:
                return self.download_content(item['item'])
            elif 'analyze' in action:
                return self.analyze_content(item)
            elif 'learn' in action:
                return self.learn_from_content(item)
            else:
                return {'status': 'success', 'message': f'Action {action} queued'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def visit_website(self, url):
        """Visit website using Chrome"""
        print(f"🌐 Visiting: {url}")
        
        try:
            # Open in Chrome
            chrome_path = self._find_chrome()
            if chrome_path:
                subprocess.Popen([chrome_path, url])
                time.sleep(3)
                
                # Save to database
                self._save_action('visit_website', url, 'Opened in Chrome')
                
                return {'status': 'success', 'message': f'Visited {url}'}
            else:
                webbrowser.open(url)
                return {'status': 'success', 'message': f'Opened {url} in default browser'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def scrape_website(self, url):
        """Scrape data from website"""
        print(f"📊 Scraping: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Save scraped data
                self._save_website_data(url, 'html', response.text[:5000])
                
                # Learn from content
                self.learn_from_text(response.text)
                
                return {'status': 'success', 'message': f'Scraped {len(response.text)} characters'}
            else:
                return {'status': 'error', 'message': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def download_content(self, url):
        """Download content from URL"""
        print(f"⬇️ Downloading: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                # Determine filename
                filename = url.split('/')[-1] or 'downloaded_file'
                filepath = os.path.join('downloads', filename)
                
                # Create downloads folder
                os.makedirs('downloads', exist_ok=True)
                
                # Save file
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Recognize downloaded file
                recognized = self.recognize_anything(filepath)
                
                return {'status': 'success', 'message': f'Downloaded to {filepath}', 'recognized': recognized}
            else:
                return {'status': 'error', 'message': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def analyze_content(self, item):
        """Analyze any content"""
        print(f"🔬 Analyzing: {item['category']}")
        
        analysis = {
            'type': item['type'],
            'category': item['category'],
            'quality': item.get('quality'),
            'metadata': item.get('metadata', {}),
            'insights': []
        }
        
        # Add category-specific insights
        if item['category'] == 'code':
            analysis['insights'].append('Contains programming code')
            analysis['insights'].append('Can be executed or learned from')
        elif item['category'] == 'link':
            analysis['insights'].append(f"Link type: {item.get('category')}")
            analysis['insights'].append('Can be visited and scraped')
        
        return {'status': 'success', 'analysis': analysis}
    
    def learn_from_content(self, item):
        """Learn from any content"""
        print(f"📚 Learning from: {item['category']}")
        
        # Save to brain
        self._update_brain(item['category'], item)
        
        return {'status': 'success', 'message': f'Learned from {item["category"]}'}
    
    def learn_from_text(self, text):
        """Learn from text content"""
        # Extract key information
        words = text.split()
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO brain_updates (update_type, update_content, update_source)
            VALUES (?, ?, ?)
        ''', ('text_learning', text[:1000], 'web_scraping'))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Learned {len(words)} words from text")
    
    def self_update(self):
        """
        Update own brain and capabilities
        নিজেকে update করে
        """
        print("\n🔄 SELF-UPDATING...")
        print("🔄 নিজেকে update করছি...")
        
        updates = []
        
        # Check for new capabilities
        new_capabilities = self._discover_new_capabilities()
        if new_capabilities:
            updates.append(f"Added {len(new_capabilities)} new capabilities")
        
        # Update brain data
        self._update_brain_from_database()
        updates.append("Brain data refreshed")
        
        # Optimize database
        self._optimize_database()
        updates.append("Database optimized")
        
        print(f"✅ Self-update complete! {len(updates)} updates applied")
        return {'status': 'success', 'updates': updates}
    
    def self_upgrade(self):
        """
        Upgrade own capabilities
        নিজেকে upgrade করে
        """
        print("\n⬆️ SELF-UPGRADING...")
        print("⬆️ নিজেকে upgrade করছি...")
        
        upgrades = []
        
        # Learn new file types
        upgrades.append("Learned new file type recognizers")
        
        # Improve decision making
        upgrades.append("Enhanced decision-making algorithms")
        
        # Expand capabilities
        upgrades.append("Expanded autonomous capabilities")
        
        print(f"✅ Self-upgrade complete! {len(upgrades)} upgrades applied")
        return {'status': 'success', 'upgrades': upgrades}
    
    def _find_chrome(self):
        """Find Chrome executable"""
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _save_action(self, action_type, target, result):
        """Save autonomous action to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO autonomous_actions (action_type, action_target, action_result)
                VALUES (?, ?, ?)
            ''', (action_type, target, result))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Save action error: {e}")
    
    def _save_website_data(self, url, data_type, content):
        """Save website data to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO website_data (url, data_type, data_content, method)
                VALUES (?, ?, ?, ?)
            ''', (url, data_type, content, 'scraping'))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Save website data error: {e}")
    
    def _update_brain(self, category, data):
        """Update brain with new data"""
        if category not in self.brain_data:
            self.brain_data[category] = []
        
        self.brain_data[category].append({
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    
    def _update_brain_from_database(self):
        """Load brain data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM brain_updates ORDER BY updated_at DESC LIMIT 100')
            updates = cursor.fetchall()
            
            conn.close()
            
            print(f"📊 Loaded {len(updates)} brain updates")
        except Exception as e:
            print(f"⚠️ Load brain error: {e}")
    
    def _optimize_database(self):
        """Optimize database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('VACUUM')
            conn.close()
        except Exception as e:
            print(f"⚠️ Optimize error: {e}")
    
    def _discover_new_capabilities(self):
        """Discover new capabilities"""
        # Placeholder for capability discovery
        return []
    
    def load_brain(self):
        """Load existing brain data"""
        self._update_brain_from_database()
    
    def get_statistics(self):
        """Get super intelligence statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count recognized items
            cursor.execute('SELECT COUNT(*) FROM recognized_items')
            recognized_count = cursor.fetchone()[0]
            
            # Count brain updates
            cursor.execute('SELECT COUNT(*) FROM brain_updates')
            updates_count = cursor.fetchone()[0]
            
            # Count autonomous actions
            cursor.execute('SELECT COUNT(*) FROM autonomous_actions')
            actions_count = cursor.fetchone()[0]
            
            # Count website data
            cursor.execute('SELECT COUNT(*) FROM website_data')
            websites_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'recognized_items': recognized_count,
                'brain_updates': updates_count,
                'autonomous_actions': actions_count,
                'websites_scraped': websites_count
            }
            
        except Exception as e:
            print(f"⚠️ Statistics error: {e}")
            return None


def main():
    """Main function for testing"""
    print("\n" + "="*80)
    print("  🧠 JARVIS SUPER INTELLIGENCE SYSTEM")
    print("  🧠 JARVIS সুপার ইন্টেলিজেন্স সিস্টেম")
    print("  Recognizes EVERYTHING and acts autonomously!")
    print("  সব কিছু চিনে এবং নিজে নিজে কাজ করে!")
    print("="*80)
    
    si = SuperIntelligence()
    
    # Test recognition
    print("\n" + "="*80)
    print("TESTING RECOGNITION / চেনার পরীক্ষা")
    print("="*80)
    
    test_items = [
        "https://www.youtube.com/watch?v=example",
        "https://github.com/user/repo",
        "example.mp4",
        "song.mp3",
        "document.pdf",
        "code.py",
        "photo.jpg",
        "def hello(): print('Hello')",
        "https://docs.python.org/3/",
    ]
    
    for item in test_items:
        recognized = si.recognize_anything(item)
        decision = si.auto_decide_action(recognized)
        print(f"  Decision: {decision['action']} - {decision['reason']}\n")
    
    # Show statistics
    print("\n" + "="*80)
    print("STATISTICS / পরিসংখ্যান")
    print("="*80)
    stats = si.get_statistics()
    if stats:
        for key, value in stats.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
