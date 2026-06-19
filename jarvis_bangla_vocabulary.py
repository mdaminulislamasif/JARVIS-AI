"""
JARVIS BANGLA VOCABULARY SYSTEM
সম্পূর্ণ বাংলা শব্দভাণ্ডার

এই system এ আছে:
- হাজার হাজার বাংলা শব্দ
- প্রতিটি শব্দের অর্থ
- ইংরেজি translation
- Category অনুযায়ী organized
- Search এবং learn করার ক্ষমতা
"""

import sqlite3
from datetime import datetime
import json


class BanglaVocabulary:
    """JARVIS Bangla Vocabulary System"""
    
    def __init__(self):
        self.db_path = 'jarvis_bangla_vocabulary.db'
        self.conn = None
        self.init_database()
        self.load_all_vocabulary()
        
        print("✅ JARVIS Bangla Vocabulary initialized!")
        print("✅ JARVIS বাংলা শব্দভাণ্ডার চালু হয়েছে!")
    
    def init_database(self):
        """Initialize database"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Vocabulary table
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
        
        self.conn.commit()
        print("✅ Bangla Vocabulary database ready!")
    
    def load_all_vocabulary(self):
        """Load all vocabulary from user's list"""
        
        # প্রকৃতি (Nature)
        nature_words = {
            'Pahar': 'Mountain / পাহাড়',
            'mati': 'Soil / মাটি',
            'Akash': 'Sky / আকাশ',
            'aasman': 'Sky / আসমান',
            'Tara': 'Star / তারা',
            'Sonali': 'Golden / সোনালী',
            'phool': 'Flower / ফুল',
            'gas': 'Tree / গাছ',
            'Sheela': 'Cool / শীতল',
            'bishti': 'Rain / বৃষ্টি',
            'megh': 'Cloud / মেঘ',
            'kalo': 'Black / কালো',
            'Shishir': 'Dew / শিশির',
            'Pani': 'Water / পানি',
            'rongdonu': 'Rainbow / রংধনু',
            'Pakhi': 'Bird / পাখি',
            'Moon': 'Moon / চাঁদ',
            'cad': 'Moon / চাঁদ',
            'Hawa': 'Air/Wind / হাওয়া',
            'Pukur': 'Pond / পুকুর',
            'jangla': 'Forest / জঙ্গল',
            'Bali': 'Sand / বালি',
            'Kada': 'Mud / কাদা',
            'Shona': 'Gold / সোনা',
            'jhor': 'Storm / ঝড়',
        }
        
        # আবেগ (Emotions)
        emotion_words = {
            'wrong': 'Wrong / ভুল',
            'sad': 'Sad / দুঃখিত',
            'hasi': 'Laugh / হাসি',
            'smile': 'Smile / হাসি',
            'Bhalo': 'Good / ভালো',
            'Bhalokach': 'Good work / ভালো কাজ',
            'shamakta': 'Forgiveness / ক্ষমা',
            'parthana': 'Prayer / প্রার্থনা',
            'pagal': 'Crazy / পাগল',
            'Bhalobasa': 'Love / ভালোবাসা',
            'hello': 'Hello / হ্যালো',
            'Bhalo Laga': 'Like / ভালো লাগা',
            'Sundar': 'Beautiful / সুন্দর',
            'Sundari': 'Beautiful woman / সুন্দরী',
            'Takano': 'Looking / তাকানো',
            'Durbal': 'Weak / দুর্বল',
            'nishpaap': 'Innocent / নিষ্পাপ',
            'dayaban': 'Kind / দয়াবান',
            'Sukano': 'Dry / শুকনো',
        }
        
        # মানুষ ও সম্পর্ক (People & Relations)
        people_words = {
            'bestie': 'Best friend / বেস্ট ফ্রেন্ড',
            'atithi': 'Guest / অতিথি',
            'belupta': 'Afternoon / বেলুপ্তা',
            'appa': 'Elder sister / আপা',
            'bondhu': 'Friend / বন্ধু',
            'Matrito': 'Motherhood / মাতৃত্ব',
            'manush': 'Human / মানুষ',
            'Bahu': 'Daughter-in-law / বধূ',
            'paribar': 'Family / পরিবার',
            'Baby': 'Baby / শিশু',
        }
        
        # শরীর ও মন (Body & Mind)
        body_words = {
            'mastishk': 'Brain / মস্তিষ্ক',
            'aaina': 'Mirror / আয়না',
            'Bindu': 'Drop / বিন্দু',
            'rokto': 'Blood / রক্ত',
            'Kaner dul': 'Earring / কানের দুল',
            'Brain': 'Brain / মস্তিষ্ক',
        }
        
        # কথা ও ভাষা (Speech & Language)
        speech_words = {
            'Kotha': 'Word/Talk / কথা',
            'abohar': 'Speech / আবহার',
            'Mitha': 'Lie / মিথ্যা',
            'Sotti': 'Truth / সত্য',
            'golpo': 'Story / গল্প',
            'kahini': 'Story / কাহিনী',
            'bakhtobo': 'Speech / বক্তব্য',
            'ishara': 'Signal / ইশারা',
        }
        
        # শক্তি ও ক্ষমতা (Power & Ability)
        power_words = {
            'Shakti': 'Power / শক্তি',
            'mittu': 'Sweet / মিষ্টি',
            'Bhumika': 'Role / ভূমিকা',
            'Vumika': 'Role / ভূমিকা',
            'carrent': 'Current / কারেন্ট',
            'Shaktti': 'Power / শক্তি',
            'creeti': 'Creation / সৃষ্টি',
        }
        
        # জীবন ও সমাজ (Life & Society)
        life_words = {
            'jormo': 'Birth / জন্ম',
            'bibaho': 'Marriage / বিবাহ',
            'Jibon': 'Life / জীবন',
            'palon': 'Nurture / পালন',
            'chakri': 'Job / চাকরি',
            'Taka': 'Money / টাকা',
            'Paisa': 'Money / পয়সা',
            'puraskar': 'Award / পুরস্কার',
            'ghushona': 'Bribe / ঘুষ',
        }
        
        # স্থান ও পথ (Place & Path)
        place_words = {
            'bikulpur': 'Afternoon / বিকেলপুর',
            'road': 'Road / রাস্তা',
            'Rasta': 'Road / রাস্তা',
            'Darja': 'Door / দরজা',
            'Almari': 'Cupboard / আলমারি',
            'Kalagarh': 'Fort / কালাগড়',
        }
        
        # যানবাহন (Vehicles)
        vehicle_words = {
            'gaRi': 'Car / গাড়ি',
            'Train': 'Train / ট্রেন',
            'ghodi': 'Horse / ঘোড়া',
        }
        
        # খাবার ও পানীয় (Food & Drink)
        food_words = {
            'ranna': 'Cooking / রান্না',
            'kaskora': 'Food / খাবার',
            'Pyara': 'Onion / পেঁয়াজ',
            'Supari': 'Betel nut / সুপারি',
            'cigarette': 'Cigarette / সিগারেট',
            'Duya': 'Smoke / ধোঁয়া',
            'Apple': 'Apple / আপেল',
        }
        
        # জিনিসপত্র (Objects)
        object_words = {
            'jinis': 'Thing / জিনিস',
            'patro': 'Leaf/Letter / পাত্র',
            'Khayal': 'Care / খেয়াল',
            'batti': 'Light / বাতি',
            'Column': 'Column / কলাম',
            'shirt': 'Shirt / শার্ট',
            'box': 'Box / বাক্স',
            'gift': 'Gift / উপহার',
            'table': 'Table / টেবিল',
            'Table': 'Table / টেবিল',
            'Khata': 'Notebook / খাতা',
            'Sutta': 'Thread / সুতা',
            'Pencil': 'Pencil / পেন্সিল',
            'Saree': 'Saree / শাড়ি',
            'Gohana': 'Jewelry / গহনা',
            'Churi': 'Bangle / চুড়ি',
            'Nupur': 'Anklet / নূপুর',
        }
        
        # প্রযুক্তি (Technology)
        tech_words = {
            'Tec': 'Technology / প্রযুক্তি',
            'Software': 'Software / সফটওয়্যার',
            'folder': 'Folder / ফোল্ডার',
            'Facebook': 'Facebook / ফেসবুক',
            'Apps': 'Apps / অ্যাপস',
            'Number': 'Number / নম্বর',
            'file': 'File / ফাইল',
            'Mobile': 'Mobile / মোবাইল',
            'Telephone': 'Telephone / টেলিফোন',
            'Laptop': 'Laptop / ল্যাপটপ',
            'signal': 'Signal / সিগন্যাল',
            'dijainar': 'Designer / ডিজাইনার',
            'Machine': 'Machine / মেশিন',
            'Sim': 'SIM card / সিম',
            'network': 'Network / নেটওয়ার্ক',
            'technique': 'Technique / কৌশল',
        }
        
        # সরকার ও রাজনীতি (Government & Politics)
        politics_words = {
            'bipuhal': 'Huge / বিপুল',
            'sarkar': 'Government / সরকার',
            'rajniti': 'Politics / রাজনীতি',
            'pesh Kora': 'Present / পেশ করা',
        }
        
        # বিবিধ (Miscellaneous)
        misc_words = {
            'Biborn': 'Various / বিবর্ণ',
            'Vision': 'Vision / দৃষ্টি',
            'mane': 'Means / মানে',
            'Anek': 'Many / অনেক',
            'Kichu': 'Some / কিছু',
            'kichu': 'Some / কিছু',
            'legend': 'Legend / কিংবদন্তি',
            'Akriti': 'Shape / আকৃতি',
            'Bhoomi': 'Land / ভূমি',
            'compo': 'Composition / কম্পো',
            'suncity': 'Sun city / সানসিটি',
            'Mila': 'Meet / মিলা',
            'Mili': 'Meet / মিলি',
            'again': 'Again / আবার',
            'Aakano': 'Calling / ডাকা',
            'Peledeoya': 'Throwing / ফেলে দেওয়া',
            'De do na': 'Give / দে দো না',
            'Has': 'Duck / হাঁস',
            'Murgi': 'Chicken / মুরগি',
            'Dolphin': 'Dolphin / ডলফিন',
            'Nare': 'Coconut / নারকেল',
            'Realise': 'Realize / উপলব্ধি',
            'Ghurni': 'Whirlpool / ঘূর্ণি',
            'big gun project': 'Big project / বড় প্রজেক্ট',
            'sobi': 'All / সবই',
            'KONALEG': 'Knowledge / জ্ঞান',
        }
        
        # সব categories একসাথে
        all_categories = {
            'Nature': nature_words,
            'Emotions': emotion_words,
            'People': people_words,
            'Body': body_words,
            'Speech': speech_words,
            'Power': power_words,
            'Life': life_words,
            'Place': place_words,
            'Vehicle': vehicle_words,
            'Food': food_words,
            'Objects': object_words,
            'Technology': tech_words,
            'Politics': politics_words,
            'Miscellaneous': misc_words,
        }
        
        # Database এ add করা
        cursor = self.conn.cursor()
        total_added = 0
        
        for category, words in all_categories.items():
            for bangla, english in words.items():
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO vocabulary 
                        (bangla_word, english_meaning, category)
                        VALUES (?, ?, ?)
                    ''', (bangla, english, category))
                    if cursor.rowcount > 0:
                        total_added += 1
                except Exception as e:
                    print(f"⚠️ Error: {e}")
        
        self.conn.commit()
        
        print(f"✅ Loaded {total_added} new Bangla words!")
        print(f"✅ {total_added}টি নতুন বাংলা শব্দ যোগ করা হয়েছে!")
    
    def search_word(self, word):
        """Search for a word"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT bangla_word, english_meaning, category
            FROM vocabulary
            WHERE bangla_word LIKE ? OR english_meaning LIKE ?
            LIMIT 10
        ''', (f'%{word}%', f'%{word}%'))
        
        results = cursor.fetchall()
        
        if results:
            print(f"\n🔍 Found {len(results)} results for '{word}':")
            print(f"🔍 '{word}' এর জন্য {len(results)}টি ফলাফল:")
            
            for bangla, english, category in results:
                print(f"\n   {bangla}")
                print(f"   Meaning: {english}")
                print(f"   Category: {category}")
        else:
            print(f"\n📭 No results found for '{word}'")
            print(f"📭 '{word}' এর জন্য কোন ফলাফল নেই")
        
        return results
    
    def get_by_category(self, category):
        """Get words by category"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT bangla_word, english_meaning
            FROM vocabulary
            WHERE category = ?
            ORDER BY bangla_word
        ''', (category,))
        
        results = cursor.fetchall()
        
        if results:
            print(f"\n📚 {category} words ({len(results)} total):")
            print(f"📚 {category} শব্দ ({len(results)}টি মোট):")
            
            for i, (bangla, english) in enumerate(results, 1):
                print(f"   {i}. {bangla} = {english}")
        
        return results
    
    def get_all_categories(self):
        """Get all categories"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT category, COUNT(*) as count
            FROM vocabulary
            GROUP BY category
            ORDER BY count DESC
        ''')
        
        results = cursor.fetchall()
        
        print(f"\n📊 All Categories:")
        print(f"📊 সব ক্যাটাগরি:")
        
        for category, count in results:
            print(f"   • {category}: {count} words")
        
        return results
    
    def get_statistics(self):
        """Get vocabulary statistics"""
        cursor = self.conn.cursor()
        
        # Total words
        cursor.execute("SELECT COUNT(*) FROM vocabulary")
        total = cursor.fetchone()[0]
        
        # Categories
        cursor.execute("SELECT COUNT(DISTINCT category) FROM vocabulary")
        categories = cursor.fetchone()[0]
        
        print(f"\n📊 BANGLA VOCABULARY STATISTICS")
        print(f"📊 বাংলা শব্দভাণ্ডার পরিসংখ্যান")
        print(f"\n📚 Total words: {total}")
        print(f"📚 মোট শব্দ: {total}")
        print(f"\n📂 Categories: {categories}")
        print(f"📂 ক্যাটাগরি: {categories}")
        
        return {'total': total, 'categories': categories}
    
    def random_words(self, count=10):
        """Get random words"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT bangla_word, english_meaning, category
            FROM vocabulary
            ORDER BY RANDOM()
            LIMIT ?
        ''', (count,))
        
        results = cursor.fetchall()
        
        print(f"\n🎲 Random {count} words:")
        print(f"🎲 র‍্যান্ডম {count}টি শব্দ:")
        
        for i, (bangla, english, category) in enumerate(results, 1):
            print(f"\n   {i}. {bangla}")
            print(f"      {english}")
            print(f"      Category: {category}")
        
        return results


def main():
    """Test Bangla Vocabulary"""
    print("\n" + "="*80)
    print("  📚 JARVIS BANGLA VOCABULARY TEST")
    print("  📚 JARVIS বাংলা শব্দভাণ্ডার টেস্ট")
    print("="*80)
    
    vocab = BanglaVocabulary()
    
    # Statistics
    vocab.get_statistics()
    
    # All categories
    vocab.get_all_categories()
    
    # Search examples
    print("\n" + "="*80)
    print("  🔍 SEARCH EXAMPLES")
    print("="*80)
    
    vocab.search_word('Bhalo')
    vocab.search_word('Taka')
    vocab.search_word('Love')
    
    # Category examples
    print("\n" + "="*80)
    print("  📂 CATEGORY EXAMPLES")
    print("="*80)
    
    vocab.get_by_category('Emotions')
    
    # Random words
    print("\n" + "="*80)
    print("  🎲 RANDOM WORDS")
    print("="*80)
    
    vocab.random_words(5)
    
    print("\n" + "="*80)
    print("  ✅ TEST COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
