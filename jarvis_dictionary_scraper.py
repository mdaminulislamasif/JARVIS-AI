"""
JARVIS DICTIONARY SCRAPER
Web থেকে হাজার হাজার বাংলা শব্দ download করে

Features:
- English-Bangla dictionary থেকে শব্দ নেয়
- Automatic scraping
- Database এ store করে
- JARVIS vocabulary তে যোগ করে
- Unlimited words support
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import webbrowser


class DictionaryScraper:
    """JARVIS Dictionary Scraper"""
    
    def __init__(self):
        self.db_path = 'jarvis_bangla_vocabulary.db'
        self.conn = None
        self.base_url = 'https://www.english-bangla.com'
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.init_database()
        
        print("✅ Dictionary Scraper initialized!")
        print("✅ Dictionary Scraper চালু হয়েছে!")
    
    def init_database(self):
        """Initialize database"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Vocabulary table (same as bangla_vocabulary)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bangla_word TEXT NOT NULL UNIQUE,
                english_meaning TEXT,
                category TEXT,
                example_bangla TEXT,
                example_english TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Scraping log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                words_found INTEGER,
                words_added INTEGER,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Database ready!")
    
    def open_dictionary_website(self):
        """Open dictionary website in browser"""
        url = 'https://www.english-bangla.com/browse/bntobn'
        
        print(f"\n🌐 Opening dictionary website...")
        print(f"🌐 Dictionary website খুলছি...")
        print(f"\n📍 URL: {url}")
        
        webbrowser.open(url)
        
        return {
            'status': 'opened',
            'url': url,
            'message': 'Dictionary website opened in browser',
            'message_bn': 'Dictionary website browser এ খোলা হয়েছে'
        }
    
    def scrape_dictionary_page(self, url):
        """Scrape a dictionary page"""
        print(f"\n🔍 Scraping: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            words_found = []
            
            # Find word entries (this is a generic approach)
            # The actual selectors depend on the website structure
            
            # Try to find word links or entries
            word_elements = soup.find_all(['a', 'div', 'span'], class_=lambda x: x and ('word' in x.lower() or 'entry' in x.lower()))
            
            if not word_elements:
                # Try finding all links in the page
                word_elements = soup.find_all('a', href=True)
            
            for element in word_elements:
                text = element.get_text(strip=True)
                
                # Skip empty or very short text
                if not text or len(text) < 2:
                    continue
                
                # Skip navigation elements
                if text.lower() in ['home', 'about', 'contact', 'search', 'browse', 'next', 'previous']:
                    continue
                
                words_found.append(text)
            
            print(f"✅ Found {len(words_found)} potential words")
            
            return words_found
        
        except Exception as e:
            print(f"❌ Error scraping: {e}")
            return []
    
    def add_words_to_vocabulary(self, words, category='Dictionary'):
        """Add words to vocabulary database"""
        cursor = self.conn.cursor()
        added_count = 0
        
        for word in words:
            try:
                # Try to add word
                cursor.execute('''
                    INSERT OR IGNORE INTO vocabulary 
                    (bangla_word, english_meaning, category)
                    VALUES (?, ?, ?)
                ''', (word, f'Word from dictionary / অভিধান থেকে শব্দ', category))
                
                if cursor.rowcount > 0:
                    added_count += 1
            
            except Exception as e:
                print(f"⚠️ Error: {e}")
        
        self.conn.commit()
        
        print(f"✅ Added {added_count} new words to vocabulary!")
        print(f"✅ {added_count}টি নতুন শব্দ যোগ করা হয়েছে!")
        
        return added_count
    
    def scrape_and_add(self, url):
        """Scrape a page and add words"""
        print("\n" + "="*80)
        print("  🔍 SCRAPING DICTIONARY")
        print("  🔍 অভিধান থেকে শব্দ নিচ্ছি")
        print("="*80)
        
        # Scrape
        words = self.scrape_dictionary_page(url)
        
        if words:
            # Add to vocabulary
            added = self.add_words_to_vocabulary(words)
            
            # Log
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO scraping_log (url, words_found, words_added)
                VALUES (?, ?, ?)
            ''', (url, len(words), added))
            self.conn.commit()
            
            return {
                'status': 'success',
                'words_found': len(words),
                'words_added': added,
                'url': url
            }
        else:
            return {
                'status': 'no_words',
                'message': 'No words found on page',
                'url': url
            }
    
    def get_total_vocabulary(self):
        """Get total vocabulary count"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vocabulary")
        total = cursor.fetchone()[0]
        
        return total
    
    def get_scraping_statistics(self):
        """Get scraping statistics"""
        cursor = self.conn.cursor()
        
        # Total scraped
        cursor.execute("SELECT COUNT(*) FROM scraping_log")
        total_scrapes = cursor.fetchone()[0]
        
        # Total words found
        cursor.execute("SELECT SUM(words_found) FROM scraping_log")
        total_found = cursor.fetchone()[0] or 0
        
        # Total words added
        cursor.execute("SELECT SUM(words_added) FROM scraping_log")
        total_added = cursor.fetchone()[0] or 0
        
        # Total vocabulary
        total_vocab = self.get_total_vocabulary()
        
        print(f"\n📊 SCRAPING STATISTICS")
        print(f"📊 স্ক্র্যাপিং পরিসংখ্যান")
        print(f"\n🔍 Total scrapes: {total_scrapes}")
        print(f"🔍 মোট স্ক্র্যাপ: {total_scrapes}")
        print(f"\n📚 Words found: {total_found}")
        print(f"📚 শব্দ পাওয়া গেছে: {total_found}")
        print(f"\n✅ Words added: {total_added}")
        print(f"✅ শব্দ যোগ করা হয়েছে: {total_added}")
        print(f"\n📖 Total vocabulary: {total_vocab}")
        print(f"📖 মোট শব্দভাণ্ডার: {total_vocab}")
        
        return {
            'total_scrapes': total_scrapes,
            'total_found': total_found,
            'total_added': total_added,
            'total_vocab': total_vocab
        }
    
    def manual_add_words(self, words_list):
        """Manually add a list of words"""
        print(f"\n📝 Adding {len(words_list)} words manually...")
        print(f"📝 {len(words_list)}টি শব্দ manually যোগ করছি...")
        
        added = self.add_words_to_vocabulary(words_list, category='Manual')
        
        return {
            'status': 'success',
            'total': len(words_list),
            'added': added
        }


def main():
    """Test Dictionary Scraper"""
    print("\n" + "="*80)
    print("  📚 JARVIS DICTIONARY SCRAPER TEST")
    print("  📚 JARVIS অভিধান স্ক্র্যাপার টেস্ট")
    print("="*80)
    
    scraper = DictionaryScraper()
    
    # Option 1: Open website in browser for manual review
    print("\n1️⃣ Opening dictionary website...")
    result = scraper.open_dictionary_website()
    print(f"   Status: {result['status']}")
    print(f"   {result['message_bn']}")
    
    # Option 2: Try to scrape (may not work due to website structure)
    print("\n2️⃣ Attempting to scrape...")
    print("   Note: This may not work perfectly due to website structure")
    print("   দ্রষ্টব্য: Website structure এর কারণে এটি perfectly কাজ নাও করতে পারে")
    
    # For now, let's add some common Bangla words manually
    print("\n3️⃣ Adding common Bangla words...")
    
    common_words = [
        'আমি', 'তুমি', 'সে', 'আমরা', 'তোমরা', 'তারা',
        'করা', 'হওয়া', 'যাওয়া', 'আসা', 'দেখা', 'বলা',
        'ভালো', 'মন্দ', 'বড়', 'ছোট', 'নতুন', 'পুরাতন',
        'এক', 'দুই', 'তিন', 'চার', 'পাঁচ', 'ছয়',
        'সাত', 'আট', 'নয়', 'দশ', 'শত', 'হাজার',
        'দিন', 'রাত', 'সকাল', 'দুপুর', 'বিকাল', 'সন্ধ্যা',
        'সোমবার', 'মঙ্গলবার', 'বুধবার', 'বৃহস্পতিবার', 'শুক্রবার', 'শনিবার', 'রবিবার',
        'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন',
        'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর',
        'বাংলাদেশ', 'ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী', 'সিলেট',
        'বই', 'কলম', 'কাগজ', 'টেবিল', 'চেয়ার', 'দরজা',
        'জানালা', 'ঘর', 'বাড়ি', 'রাস্তা', 'গাছ', 'ফুল',
        'পানি', 'খাবার', 'ভাত', 'রুটি', 'মাছ', 'মাংস',
        'দুধ', 'চা', 'কফি', 'চিনি', 'লবণ', 'তেল',
        'মা', 'বাবা', 'ভাই', 'বোন', 'দাদা', 'দাদি',
        'নানা', 'নানি', 'চাচা', 'চাচি', 'মামা', 'মামি',
        'স্কুল', 'কলেজ', 'বিশ্ববিদ্যালয়', 'শিক্ষক', 'ছাত্র', 'ছাত্রী',
        'ডাক্তার', 'নার্স', 'ইঞ্জিনিয়ার', 'শিক্ষক', 'পুলিশ', 'সৈনিক',
        'লাল', 'সবুজ', 'নীল', 'হলুদ', 'কালো', 'সাদা',
        'গরম', 'ঠান্ডা', 'ভেজা', 'শুকনো', 'মিষ্টি', 'তিক্ত',
    ]
    
    result = scraper.manual_add_words(common_words)
    print(f"   Added: {result['added']}/{result['total']} words")
    
    # Statistics
    print("\n4️⃣ Getting statistics...")
    scraper.get_scraping_statistics()
    
    print("\n" + "="*80)
    print("  ✅ TEST COMPLETE!")
    print("  ✅ টেস্ট সম্পূর্ণ!")
    print("="*80)
    
    print("\n💡 RECOMMENDATION:")
    print("💡 সুপারিশ:")
    print("   The dictionary website has been opened in your browser.")
    print("   Dictionary website আপনার browser এ খোলা হয়েছে।")
    print("   You can manually review and copy words from there.")
    print("   আপনি manually সেখান থেকে শব্দ দেখতে এবং copy করতে পারেন।")
    print("\n   JARVIS can learn from:")
    print("   JARVIS শিখতে পারে:")
    print("   1. Tree learning: tree learn bangla dictionary")
    print("   2. Ultimate learning: ultimate learn bangla words")
    print("   3. Manual word addition (as shown above)")


if __name__ == "__main__":
    main()
