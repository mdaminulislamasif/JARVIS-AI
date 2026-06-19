#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS UNIVERSAL TRANSLATOR
জার্ভিস ইউনিভার্সাল ট্রান্সলেটর

JARVIS can translate between any languages!
জার্ভিস যেকোনো ভাষার মধ্যে অনুবাদ করতে পারে!

Features:
বৈশিষ্ট্য:
1. Auto-detect source language
   স্বয়ংক্রিয়ভাবে উৎস ভাষা সনাক্ত করুন
2. Translate to any language
   যেকোনো ভাষায় অনুবাদ করুন
3. Multiple translation engines
   একাধিক অনুবাদ ইঞ্জিন
4. Save translation history
   অনুবাদ ইতিহাস সংরক্ষণ করুন
5. Support 100+ languages
   ১০০+ ভাষা সমর্থন
"""

import os
import sys
import sqlite3
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class JarvisTranslator:
    """
    JARVIS Universal Translator
    জার্ভিস ইউনিভার্সাল ট্রান্সলেটর
    """
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.translations_done = 0
        
        # Supported languages
        self.languages = {
            'en': 'English',
            'bn': 'Bengali (বাংলা)',
            'hi': 'Hindi (हिन्दी)',
            'es': 'Spanish (Español)',
            'fr': 'French (Français)',
            'de': 'German (Deutsch)',
            'it': 'Italian (Italiano)',
            'pt': 'Portuguese (Português)',
            'ru': 'Russian (Русский)',
            'ja': 'Japanese (日本語)',
            'ko': 'Korean (한국어)',
            'zh': 'Chinese (中文)',
            'ar': 'Arabic (العربية)',
            'tr': 'Turkish (Türkçe)',
            'nl': 'Dutch (Nederlands)',
            'pl': 'Polish (Polski)',
            'sv': 'Swedish (Svenska)',
            'da': 'Danish (Dansk)',
            'fi': 'Finnish (Suomi)',
            'no': 'Norwegian (Norsk)',
            'cs': 'Czech (Čeština)',
            'el': 'Greek (Ελληνικά)',
            'he': 'Hebrew (עברית)',
            'th': 'Thai (ไทย)',
            'vi': 'Vietnamese (Tiếng Việt)',
            'id': 'Indonesian (Bahasa Indonesia)',
            'ms': 'Malay (Bahasa Melayu)',
            'ur': 'Urdu (اردو)',
            'fa': 'Persian (فارسی)',
            'uk': 'Ukrainian (Українська)',
        }
        
        # Create translation history table
        self.create_translation_table()
    
    def create_translation_table(self):
        """Create table for translation history"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS translation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT NOT NULL,
                    source_lang TEXT,
                    target_lang TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    translation_engine TEXT,
                    translation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Error creating table: {e}")
    
    def show_banner(self):
        """Show banner"""
        print("\n" + "="*80)
        print("  🌍 JARVIS UNIVERSAL TRANSLATOR")
        print("  🌍 জার্ভিস ইউনিভার্সাল ট্রান্সলেটর")
        print("="*80 + "\n")
        print("  Translate between any languages!")
        print("  যেকোনো ভাষার মধ্যে অনুবাদ করুন!")
        print("\n" + "="*80 + "\n")
    
    def detect_language(self, text):
        """
        Detect language of text
        """
        # Simple language detection based on character patterns
        if re.search(r'[\u0980-\u09FF]', text):
            return 'bn'  # Bengali
        elif re.search(r'[\u0900-\u097F]', text):
            return 'hi'  # Hindi
        elif re.search(r'[\u4E00-\u9FFF]', text):
            return 'zh'  # Chinese
        elif re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text):
            return 'ja'  # Japanese
        elif re.search(r'[\uAC00-\uD7AF]', text):
            return 'ko'  # Korean
        elif re.search(r'[\u0600-\u06FF]', text):
            return 'ar'  # Arabic
        elif re.search(r'[\u0400-\u04FF]', text):
            return 'ru'  # Russian
        elif re.search(r'[\u0E00-\u0E7F]', text):
            return 'th'  # Thai
        else:
            return 'en'  # Default to English
    
    def translate_mymemory(self, text, source_lang, target_lang):
        """
        Translate using MyMemory API (Free, no API key required)
        """
        try:
            # MyMemory API endpoint
            url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={source_lang}|{target_lang}"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                if data.get('responseStatus') == 200:
                    translated = data.get('responseData', {}).get('translatedText', '')
                    return {
                        'success': True,
                        'translated_text': translated,
                        'source_lang': source_lang,
                        'target_lang': target_lang,
                        'engine': 'MyMemory'
                    }
                else:
                    return {'success': False, 'error': 'Translation failed'}
                    
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def translate_libre(self, text, source_lang, target_lang):
        """
        Translate using LibreTranslate API (Free, no API key required)
        """
        try:
            # LibreTranslate API endpoint (public instance)
            url = "https://libretranslate.de/translate"
            
            data = json.dumps({
                "q": text,
                "source": source_lang,
                "target": target_lang,
                "format": "text"
            }).encode()
            
            req = urllib.request.Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                
                if 'translatedText' in result:
                    return {
                        'success': True,
                        'translated_text': result['translatedText'],
                        'source_lang': source_lang,
                        'target_lang': target_lang,
                        'engine': 'LibreTranslate'
                    }
                else:
                    return {'success': False, 'error': 'Translation failed'}
                    
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def translate(self, text, target_lang='en', source_lang='auto'):
        """
        Translate text to target language
        """
        # Auto-detect source language if needed
        if source_lang == 'auto':
            source_lang = self.detect_language(text)
            print(f"🔍 Detected language: {self.languages.get(source_lang, source_lang)}")
        
        print(f"🌍 Translating from {self.languages.get(source_lang, source_lang)} to {self.languages.get(target_lang, target_lang)}...")
        
        # Try MyMemory first
        result = self.translate_mymemory(text, source_lang, target_lang)
        
        if not result['success']:
            # Try LibreTranslate as fallback
            print("   Trying LibreTranslate...")
            result = self.translate_libre(text, source_lang, target_lang)
        
        if result['success']:
            print(f"✅ Translation successful!")
            print(f"✅ অনুবাদ সফল!\n")
            
            # Save to database
            self.save_translation(
                text, 
                source_lang, 
                target_lang, 
                result['translated_text'],
                result['engine']
            )
            
            self.translations_done += 1
            
            return result
        else:
            print(f"❌ Translation failed: {result.get('error')}")
            return result
    
    def save_translation(self, source_text, source_lang, target_lang, translated_text, engine):
        """Save translation to database"""
        try:
            # Save to translation_history
            self.cursor.execute("""
                INSERT INTO translation_history 
                (source_text, source_lang, target_lang, translated_text, translation_engine)
                VALUES (?, ?, ?, ?, ?)
            """, (source_text, source_lang, target_lang, translated_text, engine))
            
            # Save to knowledge_base
            content = f"""
Translation
অনুবাদ

Source ({self.languages.get(source_lang, source_lang)}):
{source_text}

Target ({self.languages.get(target_lang, target_lang)}):
{translated_text}

Engine: {engine}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            self.cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source)
                VALUES (?, ?, ?)
            """, (
                f"Translation: {source_lang} → {target_lang}",
                content.strip(),
                f"Translator: {engine}"
            ))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"⚠️ Error saving translation: {e}")
    
    def show_translation_history(self, limit=10):
        """Show recent translation history"""
        print("\n" + "="*80)
        print("  📜 TRANSLATION HISTORY")
        print("  📜 অনুবাদ ইতিহাস")
        print("="*80 + "\n")
        
        try:
            self.cursor.execute("""
                SELECT source_text, source_lang, target_lang, translated_text, translation_date
                FROM translation_history
                ORDER BY translation_date DESC
                LIMIT ?
            """, (limit,))
            
            history = self.cursor.fetchall()
            
            if history:
                for i, (src, src_lang, tgt_lang, trans, date) in enumerate(history, 1):
                    print(f"  {i}. {self.languages.get(src_lang, src_lang)} → {self.languages.get(tgt_lang, tgt_lang)}")
                    print(f"     Source: {src[:50]}{'...' if len(src) > 50 else ''}")
                    print(f"     Translation: {trans[:50]}{'...' if len(trans) > 50 else ''}")
                    print(f"     Date: {date}\n")
            else:
                print("  No translation history yet.")
                print("  এখনো কোনো অনুবাদ ইতিহাস নেই।")
        
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
    
    def show_supported_languages(self):
        """Show supported languages"""
        print("\n" + "="*80)
        print("  🌍 SUPPORTED LANGUAGES")
        print("  🌍 সমর্থিত ভাষা")
        print("="*80 + "\n")
        
        print(f"  Total: {len(self.languages)} languages\n")
        
        for code, name in sorted(self.languages.items(), key=lambda x: x[1]):
            print(f"  {code:5} - {name}")
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
    
    translator = JarvisTranslator()
    translator.show_banner()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "history":
            # Show history
            translator.show_translation_history()
        elif sys.argv[1] == "languages":
            # Show supported languages
            translator.show_supported_languages()
        elif len(sys.argv) >= 3:
            # Translate: python jarvis_translator.py "text" target_lang [source_lang]
            text = sys.argv[1]
            target_lang = sys.argv[2]
            source_lang = sys.argv[3] if len(sys.argv) > 3 else 'auto'
            
            result = translator.translate(text, target_lang, source_lang)
            
            if result['success']:
                print("\n" + "="*80)
                print("  📝 TRANSLATION RESULT")
                print("  📝 অনুবাদ ফলাফল")
                print("="*80 + "\n")
                print(f"  Source: {text}")
                print(f"  Translation: {result['translated_text']}")
                print(f"  Engine: {result['engine']}")
        else:
            print("Usage:")
            print("  python jarvis_translator.py \"text\" target_lang [source_lang]")
            print("  python jarvis_translator.py history")
            print("  python jarvis_translator.py languages")
            print("\nExamples:")
            print("  python jarvis_translator.py \"Hello World\" bn")
            print("  python jarvis_translator.py \"আমি জার্ভিস\" en")
            print("  python jarvis_translator.py \"Bonjour\" en fr")
    else:
        # Interactive mode
        print("Usage:")
        print("  python jarvis_translator.py \"text\" target_lang [source_lang]")
        print("  python jarvis_translator.py history")
        print("  python jarvis_translator.py languages")
        print("\nExamples:")
        print("  python jarvis_translator.py \"Hello World\" bn")
        print("  python jarvis_translator.py \"আমি জার্ভিস\" en")
        
        # Demo translation
        print("\n" + "="*80)
        print("  🎯 DEMO TRANSLATION")
        print("  🎯 ডেমো অনুবাদ")
        print("="*80 + "\n")
        
        # English to Bengali
        print("Example 1: English → Bengali")
        result1 = translator.translate("Hello, I am JARVIS. I can translate any language!", "bn", "en")
        if result1['success']:
            print(f"Result: {result1['translated_text']}\n")
        
        # Bengali to English
        print("Example 2: Bengali → English")
        result2 = translator.translate("আমি জার্ভিস। আমি যেকোনো ভাষা অনুবাদ করতে পারি!", "en", "bn")
        if result2['success']:
            print(f"Result: {result2['translated_text']}\n")
    
    translator.close()

if __name__ == "__main__":
    main()
