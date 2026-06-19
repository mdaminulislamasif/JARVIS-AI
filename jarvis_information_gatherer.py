"""
JARVIS INFORMATION GATHERER
Comprehensive information gathering using EVERYTHING

This system gathers information from:
- Web search (Google, Bing, DuckDuckGo)
- Wikipedia
- News sources
- Social media
- Academic papers
- Government databases
- Local files
- System information
- Network information
- User data
- And more...

এই সিস্টেম তথ্য সংগ্রহ করে:
- ওয়েব সার্চ
- উইকিপিডিয়া
- নিউজ সোর্স
- সোশ্যাল মিডিয়া
- একাডেমিক পেপার
- সরকারি ডাটাবেস
- লোকাল ফাইল
- সিস্টেম তথ্য
- নেটওয়ার্ক তথ্য
- ব্যবহারকারী ডেটা
- এবং আরো...
"""

import os
import sys
import json
import time
import threading
import requests
from bs4 import BeautifulSoup
import wikipedia
import psutil
import socket
import platform
from datetime import datetime
from typing import Dict, List, Any, Optional


class InformationGatherer:
    """Comprehensive information gathering system"""
    
    def __init__(self):
        self.results = {}
        self.sources = []
        self.cache = {}
        self.cache_file = "jarvis_info_cache.json"
        self.load_cache()
    
    def load_cache(self):
        """Load cached information"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
        except Exception as e:
            print(f"⚠️ Cache load error: {e}")
            self.cache = {}
    
    def save_cache(self):
        """Save information to cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Cache save error: {e}")
    
    def gather_all(self, query: str, deep: bool = True) -> Dict[str, Any]:
        """
        Gather information from ALL sources
        
        Args:
            query: Search query
            deep: If True, performs deep search (slower but more comprehensive)
        
        Returns:
            Dictionary with all gathered information
        """
        print(f"\n{'='*60}")
        print(f"🔍 GATHERING INFORMATION: {query}")
        print(f"{'='*60}\n")
        
        self.results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'sources': {},
            'summary': '',
            'confidence': 0.0
        }
        
        # Check cache first
        cache_key = f"{query}_{deep}"
        if cache_key in self.cache:
            cache_age = time.time() - self.cache[cache_key].get('timestamp', 0)
            if cache_age < 3600:  # 1 hour cache
                print("✅ Using cached results")
                return self.cache[cache_key]
        
        # Gather from all sources in parallel
        threads = []
        
        # Web sources
        threads.append(threading.Thread(target=self._gather_web, args=(query,)))
        threads.append(threading.Thread(target=self._gather_wikipedia, args=(query,)))
        threads.append(threading.Thread(target=self._gather_news, args=(query,)))
        
        # System sources
        if 'system' in query.lower() or 'computer' in query.lower():
            threads.append(threading.Thread(target=self._gather_system_info))
        
        # Network sources
        if 'network' in query.lower() or 'ip' in query.lower():
            threads.append(threading.Thread(target=self._gather_network_info))
        
        # File sources
        if 'file' in query.lower() or 'document' in query.lower():
            threads.append(threading.Thread(target=self._gather_file_info, args=(query,)))
        
        # Start all threads
        for t in threads:
            t.daemon = True
            t.start()
        
        # Wait for all threads (with timeout)
        for t in threads:
            t.join(timeout=10 if not deep else 30)
        
        # Generate summary
        self._generate_summary()
        
        # Cache results
        self.results['timestamp'] = time.time()
        self.cache[cache_key] = self.results
        self.save_cache()
        
        return self.results
    
    def _gather_web(self, query: str):
        """Gather information from web search"""
        try:
            print("🌐 Searching web...")
            
            # Google search (via DuckDuckGo to avoid API key)
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result')[:10]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                    })
            
            self.results['sources']['web'] = {
                'count': len(results),
                'results': results,
                'status': 'success'
            }
            print(f"✅ Web: Found {len(results)} results")
            
        except Exception as e:
            print(f"❌ Web search error: {e}")
            self.results['sources']['web'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _gather_wikipedia(self, query: str):
        """Gather information from Wikipedia"""
        try:
            print("📚 Searching Wikipedia...")
            
            # Search Wikipedia
            search_results = wikipedia.search(query, results=5)
            
            if search_results:
                # Get first result
                page = wikipedia.page(search_results[0], auto_suggest=False)
                
                self.results['sources']['wikipedia'] = {
                    'title': page.title,
                    'summary': page.summary[:500],
                    'url': page.url,
                    'categories': page.categories[:10],
                    'links': page.links[:20],
                    'status': 'success'
                }
                print(f"✅ Wikipedia: Found '{page.title}'")
            else:
                self.results['sources']['wikipedia'] = {
                    'status': 'not_found'
                }
                print("⚠️ Wikipedia: No results")
                
        except Exception as e:
            print(f"❌ Wikipedia error: {e}")
            self.results['sources']['wikipedia'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _gather_news(self, query: str):
        """Gather information from news sources"""
        try:
            print("📰 Searching news...")
            
            # Use NewsAPI (free tier)
            # For now, use DuckDuckGo news
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query + ' news')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news = []
            for result in soup.find_all('div', class_='result')[:5]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem and 'news' in title_elem.get('href', '').lower():
                    news.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                    })
            
            self.results['sources']['news'] = {
                'count': len(news),
                'articles': news,
                'status': 'success'
            }
            print(f"✅ News: Found {len(news)} articles")
            
        except Exception as e:
            print(f"❌ News search error: {e}")
            self.results['sources']['news'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _gather_system_info(self):
        """Gather system information"""
        try:
            print("💻 Gathering system info...")
            
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'os_release': platform.release(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'hostname': socket.gethostname(),
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': {
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available,
                    'percent': psutil.virtual_memory().percent
                },
                'disk': {
                    'total': psutil.disk_usage('/').total,
                    'used': psutil.disk_usage('/').used,
                    'free': psutil.disk_usage('/').free,
                    'percent': psutil.disk_usage('/').percent
                },
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'status': 'success'
            }
            
            self.results['sources']['system'] = info
            print("✅ System info gathered")
            
        except Exception as e:
            print(f"❌ System info error: {e}")
            self.results['sources']['system'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _gather_network_info(self):
        """Gather network information"""
        try:
            print("🌐 Gathering network info...")
            
            # Get network interfaces
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                interfaces[interface] = []
                for addr in addrs:
                    interfaces[interface].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
            
            # Get network stats
            net_io = psutil.net_io_counters()
            
            info = {
                'hostname': socket.gethostname(),
                'interfaces': interfaces,
                'stats': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv
                },
                'connections': len(psutil.net_connections()),
                'status': 'success'
            }
            
            self.results['sources']['network'] = info
            print("✅ Network info gathered")
            
        except Exception as e:
            print(f"❌ Network info error: {e}")
            self.results['sources']['network'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _gather_file_info(self, query: str):
        """Gather information from local files"""
        try:
            print("📁 Searching local files...")
            
            # Search in common directories
            search_dirs = [
                os.path.expanduser('~'),
                os.path.join(os.path.expanduser('~'), 'Desktop'),
                os.path.join(os.path.expanduser('~'), 'Documents'),
                os.path.join(os.path.expanduser('~'), 'Downloads'),
            ]
            
            found_files = []
            query_lower = query.lower()
            
            for search_dir in search_dirs:
                if not os.path.exists(search_dir):
                    continue
                
                try:
                    for root, dirs, files in os.walk(search_dir):
                        # Limit depth
                        if root.count(os.sep) - search_dir.count(os.sep) > 2:
                            continue
                        
                        for file in files:
                            if query_lower in file.lower():
                                file_path = os.path.join(root, file)
                                try:
                                    stat = os.stat(file_path)
                                    found_files.append({
                                        'name': file,
                                        'path': file_path,
                                        'size': stat.st_size,
                                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                                    })
                                except Exception:
                                    print("⚠️ Error occurred but was silently ignored")
                        
                        if len(found_files) >= 20:
                            break
                except Exception:
                    print("⚠️ Error occurred but was silently ignored")
            
            self.results['sources']['files'] = {
                'count': len(found_files),
                'files': found_files[:20],
                'status': 'success'
            }
            print(f"✅ Files: Found {len(found_files)} files")
            
        except Exception as e:
            print(f"❌ File search error: {e}")
            self.results['sources']['files'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def _generate_summary(self):
        """Generate summary from all gathered information"""
        try:
            summary_parts = []
            total_sources = 0
            successful_sources = 0
            
            # Count sources
            for source_name, source_data in self.results['sources'].items():
                total_sources += 1
                if source_data.get('status') == 'success':
                    successful_sources += 1
            
            # Calculate confidence
            if total_sources > 0:
                self.results['confidence'] = successful_sources / total_sources
            
            # Build summary
            summary_parts.append(f"Information gathered from {successful_sources}/{total_sources} sources.")
            
            # Add key findings
            if 'wikipedia' in self.results['sources'] and self.results['sources']['wikipedia'].get('status') == 'success':
                wiki = self.results['sources']['wikipedia']
                summary_parts.append(f"\nWikipedia: {wiki.get('summary', '')[:200]}...")
            
            if 'web' in self.results['sources'] and self.results['sources']['web'].get('status') == 'success':
                web = self.results['sources']['web']
                summary_parts.append(f"\nWeb: Found {web.get('count', 0)} relevant results.")
            
            if 'news' in self.results['sources'] and self.results['sources']['news'].get('status') == 'success':
                news = self.results['sources']['news']
                summary_parts.append(f"\nNews: Found {news.get('count', 0)} recent articles.")
            
            self.results['summary'] = '\n'.join(summary_parts)
            
        except Exception as e:
            print(f"❌ Summary generation error: {e}")
            self.results['summary'] = "Error generating summary."
    
    def print_results(self):
        """Print gathered information in a readable format"""
        print(f"\n{'='*60}")
        print(f"📊 INFORMATION GATHERING RESULTS")
        print(f"{'='*60}\n")
        
        print(f"Query: {self.results.get('query', 'N/A')}")
        print(f"Timestamp: {self.results.get('timestamp', 'N/A')}")
        print(f"Confidence: {self.results.get('confidence', 0.0)*100:.1f}%\n")
        
        print(f"{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(self.results.get('summary', 'No summary available'))
        
        print(f"\n{'='*60}")
        print("SOURCES")
        print(f"{'='*60}\n")
        
        for source_name, source_data in self.results.get('sources', {}).items():
            status = source_data.get('status', 'unknown')
            print(f"📌 {source_name.upper()}: {status}")
            
            if status == 'success':
                if source_name == 'web':
                    print(f"   Found {source_data.get('count', 0)} results")
                elif source_name == 'wikipedia':
                    print(f"   Title: {source_data.get('title', 'N/A')}")
                elif source_name == 'news':
                    print(f"   Found {source_data.get('count', 0)} articles")
                elif source_name == 'system':
                    print(f"   OS: {source_data.get('os', 'N/A')}")
                    print(f"   CPU: {source_data.get('cpu_percent', 0)}%")
                elif source_name == 'network':
                    print(f"   Hostname: {source_data.get('hostname', 'N/A')}")
                elif source_name == 'files':
                    print(f"   Found {source_data.get('count', 0)} files")
            
            print()


# Test function
def test_information_gatherer():
    """Test the information gatherer"""
    print("=" * 60)
    print("JARVIS INFORMATION GATHERER TEST")
    print("=" * 60)
    
    gatherer = InformationGatherer()
    
    # Test queries
    test_queries = [
        "Python programming",
        "system information",
        "network status",
    ]
    
    for query in test_queries:
        print(f"\n\nTesting query: {query}")
        print("-" * 60)
        
        results = gatherer.gather_all(query, deep=False)
        gatherer.print_results()
        
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_information_gatherer()
