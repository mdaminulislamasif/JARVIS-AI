"""
JARVIS INFORMATION GATHERER
Gathers information from URLs and Google searches

Features:
- Fetch content from any URL
- Parse and extract information
- Google search integration
- Store gathered information
- Smart content extraction
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import json
import re
import webbrowser
import time


class InfoGatherer:
    """JARVIS Information Gatherer"""
    
    def __init__(self):
        self.db_path = 'jarvis_info_gatherer.db'
        self.conn = None
        self.init_database()
        
        # User agent for requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print("✅ JARVIS Information Gatherer initialized!")
        print("✅ JARVIS তথ্য সংগ্রহকারী চালু হয়েছে!")
    
    def init_database(self):
        """Initialize database for storing gathered information"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Gathered information table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gathered_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT,
                content TEXT,
                summary TEXT,
                keywords TEXT,
                gathered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_type TEXT DEFAULT 'url'
            )
        ''')
        
        # Search results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                results TEXT,
                result_count INTEGER,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Info Gatherer database ready!")
    
    def fetch_url_content(self, url):
        """Fetch content from a URL"""
        print(f"\n🔍 Fetching content from: {url}")
        print(f"🔍 URL থেকে content নিচ্ছি: {url}")
        
        try:
            # Try to fetch with requests
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else "No title"
            
            # Extract main content
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Extract keywords (simple approach)
            keywords = self._extract_keywords(text)
            
            # Create summary (first 500 chars)
            summary = text[:500] + "..." if len(text) > 500 else text
            
            # Store in database
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO gathered_info (url, title, content, summary, keywords, source_type)
                VALUES (?, ?, ?, ?, ?, 'url')
            ''', (url, title, text, summary, ', '.join(keywords)))
            self.conn.commit()
            
            print(f"✅ Content fetched successfully!")
            print(f"✅ Content সফলভাবে নেওয়া হয়েছে!")
            print(f"📄 Title: {title}")
            print(f"📝 Content length: {len(text)} characters")
            print(f"🔑 Keywords: {', '.join(keywords[:5])}")
            
            return {
                'status': 'success',
                'url': url,
                'title': title,
                'content': text,
                'summary': summary,
                'keywords': keywords,
                'length': len(text)
            }
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching URL: {e}")
            print(f"❌ URL নিতে ত্রুটি: {e}")
            
            # Try opening in browser as fallback
            print("\n💡 Opening in browser instead...")
            print("💡 পরিবর্তে browser এ খুলছি...")
            webbrowser.open(url)
            
            return {
                'status': 'browser_opened',
                'url': url,
                'message': 'URL opened in browser. Please manually review the content.',
                'message_bn': 'URL browser এ খোলা হয়েছে। দয়া করে manually content দেখুন।'
            }
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {
                'status': 'error',
                'url': url,
                'error': str(e)
            }
    
    def _extract_keywords(self, text, max_keywords=20):
        """Extract keywords from text (simple approach)"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Filter words
        words = [w for w in words if len(w) > 3 and w not in stop_words]
        
        # Count frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def google_search(self, query):
        """Perform Google search and open results"""
        print(f"\n🔍 Google Search: {query}")
        print(f"🔍 Google খোঁজ: {query}")
        
        # Construct Google search URL
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        print(f"🌐 Opening Google search in browser...")
        print(f"🌐 Browser এ Google search খুলছি...")
        
        # Open in browser
        webbrowser.open(search_url)
        
        # Store search query
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO search_results (query, results, result_count)
            VALUES (?, ?, ?)
        ''', (query, search_url, 0))
        self.conn.commit()
        
        return {
            'status': 'success',
            'query': query,
            'search_url': search_url,
            'message': 'Google search opened in browser',
            'message_bn': 'Google search browser এ খোলা হয়েছে'
        }
    
    def gather_from_multiple_urls(self, urls):
        """Gather information from multiple URLs"""
        print(f"\n📚 Gathering information from {len(urls)} URLs...")
        print(f"📚 {len(urls)}টি URL থেকে তথ্য সংগ্রহ করছি...")
        
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            result = self.fetch_url_content(url)
            results.append(result)
            
            # Small delay to avoid overwhelming servers
            if i < len(urls):
                time.sleep(1)
        
        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        
        print(f"\n✅ Gathering complete!")
        print(f"✅ সংগ্রহ সম্পূর্ণ!")
        print(f"📊 Successful: {successful}/{len(urls)}")
        
        return {
            'status': 'complete',
            'total': len(urls),
            'successful': successful,
            'results': results
        }
    
    def get_gathered_info(self, limit=10):
        """Get recently gathered information"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT url, title, summary, keywords, gathered_at
            FROM gathered_info
            ORDER BY gathered_at DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        
        if results:
            print(f"\n📚 Recently Gathered Information:")
            print(f"📚 সাম্প্রতিক সংগৃহীত তথ্য:")
            
            for i, (url, title, summary, keywords, gathered_at) in enumerate(results, 1):
                print(f"\n{i}. {title}")
                print(f"   URL: {url}")
                print(f"   Time: {gathered_at}")
                print(f"   Summary: {summary[:100]}...")
        else:
            print("📭 No information gathered yet")
            print("📭 এখনো কোন তথ্য সংগ্রহ করা হয়নি")
        
        return results
    
    def search_gathered_info(self, query):
        """Search in gathered information"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT url, title, summary, keywords, gathered_at
            FROM gathered_info
            WHERE title LIKE ? OR content LIKE ? OR keywords LIKE ?
            ORDER BY gathered_at DESC
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        
        if results:
            print(f"\n🔍 Found {len(results)} results for '{query}':")
            print(f"🔍 '{query}' এর জন্য {len(results)}টি ফলাফল পাওয়া গেছে:")
            
            for i, (url, title, summary, keywords, gathered_at) in enumerate(results, 1):
                print(f"\n{i}. {title}")
                print(f"   URL: {url}")
                print(f"   Time: {gathered_at}")
        else:
            print(f"📭 No results found for '{query}'")
            print(f"📭 '{query}' এর জন্য কোন ফলাফল পাওয়া যায়নি")
        
        return results
    
    def get_statistics(self):
        """Get gathering statistics"""
        cursor = self.conn.cursor()
        
        # Total gathered
        cursor.execute("SELECT COUNT(*) FROM gathered_info")
        total_gathered = cursor.fetchone()[0]
        
        # Total searches
        cursor.execute("SELECT COUNT(*) FROM search_results")
        total_searches = cursor.fetchone()[0]
        
        # Recent activity
        cursor.execute('''
            SELECT COUNT(*) FROM gathered_info
            WHERE gathered_at > datetime('now', '-1 day')
        ''')
        today_gathered = cursor.fetchone()[0]
        
        print(f"\n📊 INFORMATION GATHERING STATISTICS")
        print(f"📊 তথ্য সংগ্রহ পরিসংখ্যান")
        print(f"\n📚 Total URLs gathered: {total_gathered}")
        print(f"📚 মোট URL সংগ্রহ: {total_gathered}")
        print(f"\n🔍 Total searches: {total_searches}")
        print(f"🔍 মোট খোঁজ: {total_searches}")
        print(f"\n📅 Gathered today: {today_gathered}")
        print(f"📅 আজ সংগ্রহ: {today_gathered}")
        
        return {
            'total_gathered': total_gathered,
            'total_searches': total_searches,
            'today_gathered': today_gathered
        }


def main():
    """Test Information Gatherer"""
    print("\n" + "="*80)
    print("  🔍 JARVIS INFORMATION GATHERER TEST")
    print("  🔍 JARVIS তথ্য সংগ্রহকারী টেস্ট")
    print("="*80)
    
    gatherer = InfoGatherer()
    
    # Example URLs
    test_urls = [
        "https://aistudio.google.com/live",
        "https://www.google.com/search?sourceid=chrome&udm=50&aep=42&source=chrome.crn.rb"
    ]
    
    print("\n📋 Test URLs:")
    for url in test_urls:
        print(f"   • {url}")
    
    # Gather information
    result = gatherer.gather_from_multiple_urls(test_urls)
    
    # Show statistics
    gatherer.get_statistics()
    
    # Show gathered info
    gatherer.get_gathered_info(limit=5)
    
    print("\n" + "="*80)
    print("  ✅ TEST COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
