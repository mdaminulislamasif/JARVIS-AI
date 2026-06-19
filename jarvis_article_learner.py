#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS FULL ARTICLE LEARNER
জার্ভিস সম্পূর্ণ আর্টিকেল লার্নার

JARVIS can now learn complete articles and full pages!
জার্ভিস এখন সম্পূর্ণ আর্টিকেল এবং পূর্ণ পেজ শিখতে পারে!

Features:
বৈশিষ্ট্য:
1. Read full Wikipedia articles
   সম্পূর্ণ উইকিপিডিয়া আর্টিকেল পড়ুন
2. Extract complete web page content
   সম্পূর্ণ ওয়েব পেজ কন্টেন্ট এক্সট্র্যাক্ট করুন
3. Learn detailed information
   বিস্তারিত তথ্য শিখুন
4. Save full articles to database
   সম্পূর্ণ আর্টিকেল ডাটাবেসে সংরক্ষণ করুন
5. Support multiple sources
   একাধিক উৎস সমর্থন
"""

import os
import sys
import sqlite3
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime
from html.parser import HTMLParser

DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

class HTMLTextExtractor(HTMLParser):
    """Extract text from HTML"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'meta', 'link', 'noscript'}
        self.current_tag = None
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
    
    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.text.append(text)
    
    def get_text(self):
        return ' '.join(self.text)

class ArticleLearner:
    """
    JARVIS Full Article Learner
    জার্ভিস সম্পূর্ণ আর্টিকেল লার্নার
    """
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.articles_learned = 0
        
        # Create articles table
        self.create_articles_table()
    
    def create_articles_table(self):
        """Create table for full articles"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS learned_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT,
                    full_content TEXT NOT NULL,
                    summary TEXT,
                    word_count INTEGER,
                    source TEXT,
                    learned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Error creating table: {e}")
    
    def show_banner(self):
        """Show banner"""
        print("\n" + "="*80)
        print("  📚 JARVIS FULL ARTICLE LEARNER")
        print("  📚 জার্ভিস সম্পূর্ণ আর্টিকেল লার্নার")
        print("="*80 + "\n")
        print("  Learn complete articles and full pages!")
        print("  সম্পূর্ণ আর্টিকেল এবং পূর্ণ পেজ শিখুন!")
        print("\n" + "="*80 + "\n")
    
    def fetch_wikipedia_full_article(self, topic):
        """
        Fetch full Wikipedia article with complete content
        """
        try:
            # Try multiple Wikipedia API methods
            
            # Method 1: Full extract with sections
            url1 = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={urllib.parse.quote(topic)}&explaintext=1&exsectionformat=plain"
            
            # Method 2: Page content
            url2 = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={urllib.parse.quote(topic)}&rvprop=content&rvslots=main"
            
            # Method 3: Simple search and get first result
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={urllib.parse.quote(topic)}&limit=1"
            
            # Try Method 1 first
            req = urllib.request.Request(url1)
            req.add_header('User-Agent', 'Mozilla/5.0 (JARVIS Article Learner)')
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
                
                pages = data.get('query', {}).get('pages', {})
                
                if pages:
                    page = list(pages.values())[0]
                    
                    if 'extract' in page and page['extract']:
                        full_text = page['extract']
                        title = page.get('title', topic)
                        page_id = page.get('pageid', '')
                        url = f"https://en.wikipedia.org/?curid={page_id}"
                        
                        # Get summary (first paragraph)
                        paragraphs = full_text.split('\n\n')
                        summary = paragraphs[0] if paragraphs else full_text[:500]
                        
                        return {
                            'success': True,
                            'title': title,
                            'url': url,
                            'full_content': full_text,
                            'summary': summary,
                            'word_count': len(full_text.split()),
                            'source': 'Wikipedia'
                        }
            
            # If Method 1 fails, try simple web scraping
            print("⚠️ API method failed, trying web scraping...")
            
            # Get Wikipedia page URL
            wiki_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(topic.replace(' ', '_'))}"
            
            req = urllib.request.Request(wiki_url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Extract text from paragraphs
                paragraphs = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
                
                # Clean HTML tags
                full_text = []
                for p in paragraphs:
                    # Remove HTML tags
                    text = re.sub(r'<[^>]+>', '', p)
                    # Decode HTML entities
                    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
                    text = text.strip()
                    if text and len(text) > 50:  # Only substantial paragraphs
                        full_text.append(text)
                
                full_content = '\n\n'.join(full_text)
                
                if full_content:
                    # Get title
                    title_match = re.search(r'<title>(.*?) - Wikipedia</title>', html)
                    title = title_match.group(1) if title_match else topic
                    
                    summary = full_text[0] if full_text else full_content[:500]
                    
                    return {
                        'success': True,
                        'title': title,
                        'url': wiki_url,
                        'full_content': full_content,
                        'summary': summary,
                        'word_count': len(full_content.split()),
                        'source': 'Wikipedia'
                    }
            
            return {'success': False, 'error': 'Could not fetch article content'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def fetch_web_page_content(self, url):
        """
        Fetch full content from any web page
        """
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Extract text from HTML
                extractor = HTMLTextExtractor()
                extractor.feed(html)
                full_text = extractor.get_text()
                
                # Clean up text
                full_text = re.sub(r'\s+', ' ', full_text).strip()
                
                # Get title from HTML
                title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
                title = title_match.group(1) if title_match else url
                
                # Get summary (first 500 chars)
                summary = full_text[:500] + '...' if len(full_text) > 500 else full_text
                
                return {
                    'success': True,
                    'title': title,
                    'url': url,
                    'full_content': full_text,
                    'summary': summary,
                    'word_count': len(full_text.split()),
                    'source': 'Web Page'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def learn_article(self, topic_or_url):
        """
        Learn a full article from Wikipedia or web URL
        """
        print(f"📚 Learning full article: {topic_or_url}")
        print(f"📚 সম্পূর্ণ আর্টিকেল শিখছি: {topic_or_url}\n")
        
        # Check if it's a URL or topic
        if topic_or_url.startswith('http://') or topic_or_url.startswith('https://'):
            # It's a URL
            print("🌐 Fetching from web page...")
            result = self.fetch_web_page_content(topic_or_url)
        else:
            # It's a Wikipedia topic
            print("📖 Fetching from Wikipedia...")
            result = self.fetch_wikipedia_full_article(topic_or_url)
        
        if not result['success']:
            print(f"❌ Failed to fetch article: {result.get('error')}\n")
            return False
        
        # Display article info
        print(f"✅ Article fetched successfully!")
        print(f"✅ আর্টিকেল সফলভাবে আনা হয়েছে!\n")
        print(f"📝 Title: {result['title']}")
        print(f"🔗 URL: {result['url']}")
        print(f"📊 Word Count: {result['word_count']} words")
        print(f"📄 Content Length: {len(result['full_content'])} characters\n")
        
        # Show summary
        print(f"📋 Summary:")
        print(f"   {result['summary'][:200]}...\n")
        
        # Save to database
        self.save_article(result)
        
        self.articles_learned += 1
        
        return True
    
    def save_article(self, article_data):
        """Save full article to database"""
        try:
            # Save to learned_articles table
            self.cursor.execute("""
                INSERT INTO learned_articles 
                (title, url, full_content, summary, word_count, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                article_data['title'],
                article_data['url'],
                article_data['full_content'],
                article_data['summary'],
                article_data['word_count'],
                article_data['source']
            ))
            
            # Also save to knowledge_base for compatibility
            content = f"""
{article_data['title']}

Source: {article_data['source']}
URL: {article_data['url']}
Word Count: {article_data['word_count']} words

SUMMARY:
{article_data['summary']}

FULL CONTENT:
{article_data['full_content'][:5000]}{'...' if len(article_data['full_content']) > 5000 else ''}

Learned: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            self.cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source)
                VALUES (?, ?, ?)
            """, (
                article_data['title'],
                content.strip(),
                f"Article: {article_data['source']}"
            ))
            
            self.conn.commit()
            
            print(f"✅ Article saved to database!")
            print(f"✅ আর্টিকেল ডাটাবেসে সংরক্ষিত!\n")
            
        except Exception as e:
            print(f"⚠️ Error saving article: {e}\n")
    
    def learn_multiple_articles(self, topics, delay=3):
        """
        Learn multiple articles
        """
        print(f"📚 Learning {len(topics)} articles...")
        print(f"📚 {len(topics)}টি আর্টিকেল শিখছি...\n")
        
        import time
        
        for i, topic in enumerate(topics, 1):
            print(f"[{i}/{len(topics)}] ", end="")
            
            success = self.learn_article(topic)
            
            if success and i < len(topics):
                print(f"⏳ Waiting {delay} seconds before next article...\n")
                time.sleep(delay)
        
        print("\n" + "="*80)
        print(f"  ✅ Learned {self.articles_learned} articles!")
        print(f"  ✅ {self.articles_learned}টি আর্টিকেল শিখেছি!")
        print("="*80)
    
    def show_learned_articles(self, limit=10):
        """Show recently learned articles"""
        print("\n" + "="*80)
        print("  📚 LEARNED ARTICLES")
        print("  📚 শেখা আর্টিকেল")
        print("="*80 + "\n")
        
        try:
            self.cursor.execute("""
                SELECT title, source, word_count, learned_date
                FROM learned_articles
                ORDER BY learned_date DESC
                LIMIT ?
            """, (limit,))
            
            articles = self.cursor.fetchall()
            
            if articles:
                for i, (title, source, words, date) in enumerate(articles, 1):
                    print(f"  {i}. {title}")
                    print(f"     Source: {source} | Words: {words} | Date: {date}\n")
            else:
                print("  No articles learned yet.")
                print("  এখনো কোনো আর্টিকেল শেখা হয়নি।")
        
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
    
    def show_statistics(self):
        """Show learning statistics"""
        print("\n" + "="*80)
        print("  📊 ARTICLE LEARNING STATISTICS")
        print("  📊 আর্টিকেল শেখার পরিসংখ্যান")
        print("="*80 + "\n")
        
        try:
            # Total articles
            self.cursor.execute("SELECT COUNT(*) FROM learned_articles")
            total = self.cursor.fetchone()[0]
            
            # Total words
            self.cursor.execute("SELECT SUM(word_count) FROM learned_articles")
            total_words = self.cursor.fetchone()[0] or 0
            
            # By source
            self.cursor.execute("""
                SELECT source, COUNT(*), SUM(word_count)
                FROM learned_articles
                GROUP BY source
            """)
            by_source = self.cursor.fetchall()
            
            print(f"  Total Articles: {total}")
            print(f"  Total Words: {total_words:,}")
            print(f"  Average Words per Article: {total_words // total if total > 0 else 0:,}")
            print(f"\n  By Source:")
            for source, count, words in by_source:
                print(f"    • {source}: {count} articles ({words:,} words)")
        
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
    
    learner = ArticleLearner()
    learner.show_banner()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            # Show learned articles
            learner.show_learned_articles()
        elif sys.argv[1] == "stats":
            # Show statistics
            learner.show_statistics()
        elif sys.argv[1] == "multi":
            # Learn multiple articles
            topics = sys.argv[2:] if len(sys.argv) > 2 else [
                "Artificial Intelligence",
                "Machine Learning",
                "Python Programming"
            ]
            learner.learn_multiple_articles(topics)
        else:
            # Learn single article
            learner.learn_article(sys.argv[1])
    else:
        # Demo mode
        print("Usage:")
        print("  python jarvis_article_learner.py <topic_or_url>")
        print("  python jarvis_article_learner.py multi <topic1> <topic2> ...")
        print("  python jarvis_article_learner.py list")
        print("  python jarvis_article_learner.py stats")
        print("\nExamples:")
        print("  python jarvis_article_learner.py \"Artificial Intelligence\"")
        print("  python jarvis_article_learner.py \"https://example.com/article\"")
        print("  python jarvis_article_learner.py multi \"Python\" \"JavaScript\" \"AI\"")
        
        # Demo: Learn one article
        print("\n" + "="*80)
        print("  🎯 DEMO: Learning a full article")
        print("  🎯 ডেমো: একটি সম্পূর্ণ আর্টিকেল শিখছি")
        print("="*80 + "\n")
        
        learner.learn_article("Artificial Intelligence")
    
    learner.close()

if __name__ == "__main__":
    main()
