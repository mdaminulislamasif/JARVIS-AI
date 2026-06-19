import requests
from bs4 import BeautifulSoup
import time
import random

class InternetBrain:
    def __init__(self, brain_module):
        self.brain = brain_module
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]

    def search_and_learn(self, query):
        self.brain.speak(f"Searching for {query}...")
        
        # Strategy 1: Wikipedia
        wiki_res = self._search_wikipedia(query)
        if wiki_res:
            self.brain.db.save_memory(query, wiki_res, "Wikipedia")
            return wiki_res
            
        # Strategy 2: Google Scraper
        google_res = self._search_google(query)
        if google_res:
            self.brain.db.save_memory(query, google_res, "Google")
            return google_res
            
        # Strategy 3: DuckDuckGo
        ddg_res = self._search_ddg(query)
        if ddg_res:
            self.brain.db.save_memory(query, ddg_res, "DuckDuckGo")
            return ddg_res
            
        return "I couldn't find any information online. / আমি অনলাইনে কোনো তথ্য খুঁজে পাইনি।"

    def _search_wikipedia(self, query):
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"From Wikipedia: {data.get('extract', '')}"
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None

    def _search_google(self, query):
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Try to find snippets in Google's common classes
                snippets = []
                # Method 1: BNeawe (Featured snippets)
                for div in soup.find_all('div', class_='BNeawe'):
                    snippets.append(div.get_text())
                
                # Method 2: VwiC3b (Search result snippets)
                for span in soup.find_all('span', class_='VwiC3b'):
                    snippets.append(span.get_text())
                
                if snippets:
                    content = " ".join(snippets[:3])
                    return f"Google Snippet: {content[:500]}..."
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None

    def _search_ddg(self, query):
        try:
            url = f"https://api.duckduckgo.com/?q={query.replace(' ', '+')}&format=json"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('AbstractText'):
                    return f"From DuckDuckGo: {data['AbstractText']}"
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return None
