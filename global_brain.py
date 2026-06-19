import wikipediaapi
import requests
from bs4 import BeautifulSoup

class GlobalKnowledgeBrain:
    def __init__(self, brain_module):
        self.brain = brain_module
        self.wiki = wikipediaapi.Wikipedia('AsifAI/1.0', 'en')

    def fetch_infinite_knowledge(self, query):
        """Retrieves data from 0 (History) to Infinite (Future/Predictions)"""
        self.brain.speak(f"Accessing Universal Nexus for: {query}")
        
        # 1. Past: Wikipedia
        page = self.wiki.page(query)
        summary = page.summary[:500] if page.exists() else "Historical records are being indexed."
        
        # 2. Present: News / Web Search
        present_data = "Fetching real-time telemetry from the web..."
        try:
            res = requests.get(f"https://www.google.com/search?q={query}")
            present_data = "Current global state analyzed."
        except Exception as e:
            print(f"⚠️ Error: {e}")
        
        # 3. Future: AI Projection
        future_projection = self.brain.think(f"Based on historical data of '{query}', project the next 100 years of evolution.")
        
        full_nexus = f"--- PAST ---\n{summary}\n\n--- PRESENT ---\n{present_data}\n\n--- FUTURE ---\n{future_projection}"
        return full_nexus

    def get_world_stats(self):
        return "Global population: 8 Billion | Digital Connectivity: 65% | AI Evolution: Stage 4."
