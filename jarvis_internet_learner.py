"""
JARVIS INTERNET LEARNER
Automatically learns from the internet and saves to knowledge base

Features:
- Search and learn from any topic
- Extract information from websites
- Save to JARVIS memory
- Build knowledge base automatically
"""

import os
import sys
import sqlite3
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json

class InternetLearner:
    """Learn from internet and save to JARVIS knowledge base"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.conn = None
        self.setup_database()
        
    def setup_database(self):
        """Setup database for learned content"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create internet_learned table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS internet_learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source_url TEXT,
                    learned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    word_count INTEGER,
                    category TEXT
                )
            """)
            
            self.conn.commit()
            print("[OK] Internet Learner database ready!")
            
        except Exception as e:
            print(f"[!] Database setup error: {e}")
    
    def search_and_learn(self, topic):
        """Search internet for topic and learn"""
        print(f"\n[SEARCH] Searching internet for: {topic}")
        print(f"[SEARCH] Internet এ খুঁজছি: {topic}")
        
        try:
            # Step 1: Search Wikipedia
            wiki_content = self._learn_from_wikipedia(topic)
            
            if wiki_content:
                # Save to knowledge base
                self._save_to_knowledge(topic, wiki_content, "Wikipedia", "encyclopedia")
                return {
                    'status': 'success',
                    'response': f"✅ Learned about '{topic}' from Wikipedia!\n✅ '{topic}' সম্পর্কে Wikipedia থেকে শিখেছি!\n\nContent: {wiki_content[:200]}...\n\nSaved to JARVIS memory!",
                    'type': 'learning',
                    'source': 'Wikipedia',
                    'word_count': len(wiki_content.split())
                }
            
            # Step 2: If Wikipedia fails, try web search
            web_content = self._learn_from_web(topic)
            
            if web_content:
                self._save_to_knowledge(topic, web_content, "Web Search", "general")
                return {
                    'status': 'success',
                    'response': f"✅ Learned about '{topic}' from web!\n✅ '{topic}' সম্পর্কে web থেকে শিখেছি!\n\nContent: {web_content[:200]}...\n\nSaved to JARVIS memory!",
                    'type': 'learning',
                    'source': 'Web',
                    'word_count': len(web_content.split())
                }
            
            # Step 3: If web search fails, try alternative APIs
            alt_content = self._learn_from_alternative_apis(topic)
            
            if alt_content:
                self._save_to_knowledge(topic, alt_content, "Alternative API", "general")
                return {
                    'status': 'success',
                    'response': f"✅ Learned about '{topic}' from alternative sources!\n✅ '{topic}' সম্পর্কে alternative sources থেকে শিখেছি!\n\nContent: {alt_content[:200]}...\n\nSaved to JARVIS memory!",
                    'type': 'learning',
                    'source': 'Alternative API',
                    'word_count': len(alt_content.split())
                }
            
            # Step 4: If all else fails, try built-in knowledge
            builtin_content = self._get_builtin_knowledge(topic)
            
            if builtin_content:
                self._save_to_knowledge(topic, builtin_content, "Built-in Knowledge", "general")
                return {
                    'status': 'success',
                    'response': f"✅ Learned about '{topic}' from built-in knowledge!\n✅ '{topic}' সম্পর্কে built-in knowledge থেকে শিখেছি!\n\nContent: {builtin_content[:200]}...\n\nSaved to JARVIS memory!",
                    'type': 'learning',
                    'source': 'Built-in Knowledge',
                    'word_count': len(builtin_content.split())
                }
            
            return {
                'status': 'error',
                'response': f"❌ Could not learn about '{topic}' from internet.\n❌ '{topic}' সম্পর্কে internet থেকে শিখতে পারিনি।",
                'type': 'learning'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'response': f"❌ Learning error: {e}\n❌ শেখার সময় error: {e}",
                'type': 'learning'
            }
    
    def _learn_from_wikipedia(self, topic):
        """Learn from Wikipedia"""
        try:
            print("📚 Trying Wikipedia...")
            
            # Wikipedia API
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'extract' in data:
                    content = data['extract']
                    print(f"[OK] Found on Wikipedia: {len(content)} characters")
                    return content
            
            return None
            
        except Exception as e:
            print(f"[!] Wikipedia error: {e}")
            return None
    
    def _learn_from_web(self, topic):
        """Learn from web search with retry logic and multiple search engines"""
        try:
            print("🌐 Trying web search...")
            
            # List of user agents to try
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]
            
            # Try Google first with different user agents
            for user_agent in user_agents:
                try:
                    search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
                    headers = {'User-Agent': user_agent}
                    
                    response = requests.get(search_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Try multiple extraction methods
                        content_parts = []
                        
                        # Method 1: BNeawe class
                        paragraphs = soup.find_all('div', class_='BNeawe')
                        if paragraphs:
                            content_parts.extend([p.get_text() for p in paragraphs[:5]])
                        
                        # Method 2: VwiC3b class (Google snippets)
                        snippets = soup.find_all('span', class_='VwiC3b')
                        if snippets:
                            content_parts.extend([s.get_text() for s in snippets[:3]])
                        
                        # Method 3: st class (older Google format)
                        descriptions = soup.find_all('span', class_='st')
                        if descriptions:
                            content_parts.extend([d.get_text() for d in descriptions[:3]])
                        
                        if content_parts:
                            content = ' '.join(content_parts)
                            print(f"[OK] Found on Google: {len(content)} characters")
                            return content
                
                except Exception as e:
                    print(f"[!] Google attempt failed with user agent {user_agent[:50]}...: {e}")
                    continue
            
            # Try DuckDuckGo if Google fails
            try:
                print("🦆 Trying DuckDuckGo...")
                ddg_url = f"https://duckduckgo.com/html/?q={topic.replace(' ', '+')}"
                headers = {'User-Agent': user_agents[0]}
                
                response = requests.get(ddg_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract snippets from DuckDuckGo results
                    results = soup.find_all('a', class_='result__snippet')
                    if results:
                        content = ' '.join([r.get_text() for r in results[:5]])
                        print(f"[OK] Found on DuckDuckGo: {len(content)} characters")
                        return content
            
            except Exception as e:
                print(f"[!] DuckDuckGo error: {e}")
            
            # Try Bing if DuckDuckGo fails
            try:
                print("[SEARCH] Trying Bing...")
                bing_url = f"https://www.bing.com/search?q={topic.replace(' ', '+')}"
                headers = {'User-Agent': user_agents[0]}
                
                response = requests.get(bing_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract snippets from Bing results
                    results = soup.find_all('p', class_='b_lineclamp')
                    if not results:
                        results = soup.find_all('div', class_='b_caption')
                    
                    if results:
                        content = ' '.join([r.get_text() for r in results[:5]])
                        print(f"[OK] Found on Bing: {len(content)} characters")
                        return content
            
            except Exception as e:
                print(f"[!] Bing error: {e}")
            
            return None
            
        except Exception as e:
            print(f"[!] Web search error: {e}")
            return None
    
    def _learn_from_alternative_apis(self, topic):
        """Learn from alternative APIs like DuckDuckGo Instant Answer"""
        try:
            print("🔄 Trying alternative APIs...")
            
            # Try DuckDuckGo Instant Answer API
            try:
                ddg_api_url = f"https://api.duckduckgo.com/?q={topic.replace(' ', '+')}&format=json"
                
                response = requests.get(ddg_api_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract content from various fields
                    content_parts = []
                    
                    if data.get('Abstract'):
                        content_parts.append(data['Abstract'])
                    
                    if data.get('AbstractText'):
                        content_parts.append(data['AbstractText'])
                    
                    if data.get('Definition'):
                        content_parts.append(data['Definition'])
                    
                    # Extract related topics
                    if data.get('RelatedTopics'):
                        for topic_item in data['RelatedTopics'][:3]:
                            if isinstance(topic_item, dict) and topic_item.get('Text'):
                                content_parts.append(topic_item['Text'])
                    
                    if content_parts:
                        content = ' '.join(content_parts)
                        print(f"[OK] Found on DuckDuckGo API: {len(content)} characters")
                        return content
            
            except Exception as e:
                print(f"[!] DuckDuckGo API error: {e}")
            
            # Try extracting domain information for .com/.org domains
            topic_lower = topic.lower().replace('.com', '').replace('.org', '').replace('.net', '').replace('www.', '')
            
            # Check if it's a domain name
            if any(ext in topic.lower() for ext in ['.com', '.org', '.net', '.edu', '.gov', '.io', '.co']):
                domain_name = topic_lower.strip()
                content = f"{domain_name.capitalize()} is a website domain. It is an online platform accessible via the internet at {topic}."
                print(f"[OK] Generated domain information: {len(content)} characters")
                return content
            
            return None
            
        except Exception as e:
            print(f"[!] Alternative API error: {e}")
            return None
    
    def _get_builtin_knowledge(self, topic):
        """Get built-in knowledge for common websites and topics"""
        try:
            print("📚 Trying built-in knowledge...")
            
            # Normalize topic
            topic_lower = topic.lower().replace('.com', '').replace('.org', '').replace('.net', '').replace('www.', '').strip()
            
            # Built-in knowledge base for common websites
            builtin_knowledge = {
                'youtube': "YouTube is a free video sharing website owned by Google. It was created in 2005 and allows users to upload, view, rate, share, and comment on videos. YouTube is the world's second most visited website after Google Search. Content includes video clips, TV show clips, music videos, short films, documentaries, audio recordings, movie trailers, live streams, and video blogging. YouTube has over 2 billion monthly active users who watch over 1 billion hours of video daily.",
                
                'facebook': "Facebook is a social networking service owned by Meta Platforms (formerly Facebook, Inc.). Founded by Mark Zuckerberg in 2004, Facebook allows users to create profiles, upload photos and videos, send messages, and keep in touch with friends, family and colleagues. As of 2021, Facebook has over 2.9 billion monthly active users, making it the world's largest social network. Users can join groups, follow pages, and interact with content through likes, comments, and shares.",
                
                'google': "Google is an American multinational technology company that specializes in Internet-related services and products. Founded in 1998 by Larry Page and Sergey Brin, Google is best known for its search engine, which is the most widely used search engine in the world. Google also offers many other services including Gmail (email), Google Maps (mapping), Google Drive (cloud storage), YouTube (video sharing), Android (mobile operating system), Chrome (web browser), and Google Cloud Platform. Google's parent company is Alphabet Inc.",
                
                'twitter': "Twitter is a social media platform where users post and interact with messages called 'tweets'. Founded in 2006 by Jack Dorsey, Noah Glass, Biz Stone, and Evan Williams, Twitter allows users to post tweets of up to 280 characters. Users can follow other users, retweet content, like tweets, and reply to messages. Twitter is widely used for news, entertainment, politics, and real-time communication. As of 2021, Twitter has over 330 million monthly active users worldwide.",
                
                'instagram': "Instagram is a photo and video sharing social networking service owned by Meta Platforms (Facebook). Launched in 2010 by Kevin Systrom and Mike Krieger, Instagram allows users to upload photos and videos, apply filters, and share them with followers. Features include Stories (24-hour temporary posts), Reels (short videos), IGTV (long-form videos), and Direct Messages. Instagram has over 1 billion monthly active users and is particularly popular among younger demographics for visual content sharing.",
                
                'amazon': "Amazon is an American multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence. Founded by Jeff Bezos in 1994, Amazon started as an online bookstore and has grown to become the world's largest online retailer. Amazon offers millions of products across various categories, provides cloud computing services through Amazon Web Services (AWS), streaming services through Prime Video, and smart home devices like Alexa. Amazon is one of the world's most valuable companies.",
                
                'wikipedia': "Wikipedia is a free online encyclopedia created and edited by volunteers around the world. Founded in 2001 by Jimmy Wales and Larry Sanger, Wikipedia contains over 60 million articles in more than 300 languages. It is one of the most popular websites in the world and is often among the top search results for informational queries. Wikipedia operates on a wiki model, meaning anyone can edit most articles. The site is maintained by the Wikimedia Foundation, a non-profit organization.",
                
                'reddit': "Reddit is a social news aggregation, web content rating, and discussion website. Founded in 2005 by Steve Huffman and Alexis Ohanian, Reddit allows users to submit content such as text posts, links, images, and videos. Content is organized into user-created communities called 'subreddits' covering virtually every topic imaginable. Users can vote content up or down, determining its visibility. Reddit has over 430 million monthly active users and is known for its diverse communities and influential discussions.",
                
                'linkedin': "LinkedIn is a professional networking platform owned by Microsoft. Founded in 2002 and launched in 2003, LinkedIn is designed for career and business professionals to connect. Users create profiles that function as online resumes, connect with colleagues and industry professionals, join professional groups, and search for jobs. Companies use LinkedIn for recruiting, networking, and brand building. LinkedIn has over 800 million members in more than 200 countries and territories worldwide.",
                
                'netflix': "Netflix is a streaming service that offers a wide variety of TV shows, movies, documentaries, and original content. Founded in 1997 by Reed Hastings and Marc Randolph as a DVD rental service, Netflix transitioned to streaming in 2007. Netflix produces its own original content including popular series and films. The service operates on a subscription model with different pricing tiers. Netflix has over 220 million subscribers worldwide and is available in over 190 countries.",
                
                'microsoft': "Microsoft Corporation is an American multinational technology company founded by Bill Gates and Paul Allen in 1975. Microsoft is best known for its Windows operating system, Office productivity suite (Word, Excel, PowerPoint), and cloud computing platform Azure. Other major products include the Xbox gaming console, Surface devices, LinkedIn, and GitHub. Microsoft is one of the world's largest technology companies and has been a leader in personal computing and enterprise software for decades.",
                
                'apple': "Apple Inc. is an American multinational technology company founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976. Apple designs and manufactures consumer electronics, computer software, and online services. Major products include the iPhone smartphone, iPad tablet, Mac computers, Apple Watch, AirPods, and services like the App Store, Apple Music, iCloud, and Apple TV+. Apple is known for its innovative design, user-friendly interfaces, and integrated ecosystem. It is one of the world's most valuable companies.",
                
                'tiktok': "TikTok is a short-form video hosting service owned by Chinese company ByteDance. Launched internationally in 2018, TikTok allows users to create and share videos up to 10 minutes long, though most content is much shorter. The app is known for its algorithm that personalizes content feeds, viral trends, music integration, and creative editing tools. TikTok has become extremely popular, especially among younger users, with over 1 billion monthly active users worldwide. The platform has influenced pop culture, music, and social media trends globally.",
                
                'github': "GitHub is a web-based platform for version control and collaboration using Git. Founded in 2008 and acquired by Microsoft in 2018, GitHub allows developers to store, manage, and track changes to their code. It provides features like pull requests, code review, issue tracking, and project management tools. GitHub hosts millions of open-source projects and is the world's largest source code host. Developers use GitHub to collaborate on projects, contribute to open source, and showcase their work. It has over 100 million developers using the platform.",
                
                'spotify': "Spotify is a digital music streaming service that gives users access to millions of songs, podcasts, and videos from artists worldwide. Founded in 2006 by Daniel Ek and Martin Lorentzon in Sweden, Spotify launched in 2008. The service offers both free ad-supported streaming and paid premium subscriptions. Spotify uses algorithms to create personalized playlists and recommendations. With over 450 million users including 195 million premium subscribers, Spotify is the world's largest music streaming service.",
                
                'zoom': "Zoom is a video conferencing platform that allows users to connect online for video and audio meetings, webinars, and chat. Founded by Eric Yuan in 2011 and launched in 2013, Zoom became widely popular during the COVID-19 pandemic for remote work, online education, and virtual social gatherings. Features include screen sharing, virtual backgrounds, breakout rooms, and recording capabilities. Zoom is known for its ease of use and reliability. The platform serves millions of users worldwide across businesses, schools, and personal use."
            }
            
            # Check if we have built-in knowledge for this topic
            if topic_lower in builtin_knowledge:
                content = builtin_knowledge[topic_lower]
                print(f"[OK] Found in built-in knowledge: {len(content)} characters")
                return content
            
            return None
            
        except Exception as e:
            print(f"[!] Built-in knowledge error: {e}")
            return None
    
    def _save_to_knowledge(self, topic, content, source, category):
        """Save learned content to knowledge base"""
        try:
            cursor = self.conn.cursor()
            
            # Save to internet_learned table
            cursor.execute("""
                INSERT INTO internet_learned (topic, content, source_url, word_count, category)
                VALUES (?, ?, ?, ?, ?)
            """, (topic, content, source, len(content.split()), category))
            
            # Also save to knowledge_base table for quick access
            cursor.execute("""
                INSERT OR REPLACE INTO knowledge_base (topic, content)
                VALUES (?, ?)
            """, (topic, content))
            
            self.conn.commit()
            print(f"[OK] Saved to knowledge base: {topic}")
            
        except Exception as e:
            print(f"[!] Save error: {e}")
    
    def get_learned_topics(self):
        """Get list of all learned topics"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT topic, learned_date, word_count, source_url, category
                FROM internet_learned
                ORDER BY learned_date DESC
                LIMIT 50
            """)
            
            topics = cursor.fetchall()
            
            if topics:
                result = "📚 Learned Topics / শেখা বিষয়:\n\n"
                for i, (topic, date, words, source, category) in enumerate(topics, 1):
                    result += f"{i}. {topic}\n"
                    result += f"   📅 Date: {date}\n"
                    result += f"   📝 Words: {words}\n"
                    result += f"   🔗 Source: {source}\n"
                    result += f"   📂 Category: {category}\n\n"
                
                return {
                    'status': 'success',
                    'response': result,
                    'type': 'list',
                    'count': len(topics)
                }
            else:
                return {
                    'status': 'info',
                    'response': "No topics learned yet.\nএখনো কোনো বিষয় শেখা হয়নি।",
                    'type': 'list'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'response': f"Error getting topics: {e}",
                'type': 'list'
            }
    
    def search_learned_knowledge(self, query):
        """Search in learned knowledge"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT topic, content, source_url
                FROM internet_learned
                WHERE topic LIKE ? OR content LIKE ?
                ORDER BY learned_date DESC
                LIMIT 5
            """, (f"%{query}%", f"%{query}%"))
            
            results = cursor.fetchall()
            
            if results:
                response = f"🔍 Found {len(results)} results for '{query}':\n\n"
                for topic, content, source in results:
                    response += f"📌 {topic}\n"
                    response += f"   {content[:150]}...\n"
                    response += f"   🔗 Source: {source}\n\n"
                
                return {
                    'status': 'success',
                    'response': response,
                    'type': 'search'
                }
            else:
                return {
                    'status': 'info',
                    'response': f"No results found for '{query}'.\n'{query}' এর জন্য কোনো ফলাফল পাওয়া যায়নি।",
                    'type': 'search'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'response': f"Search error: {e}",
                'type': 'search'
            }
    
    def learn_multiple_topics(self, topics_list):
        """Learn multiple topics at once"""
        results = []
        
        for topic in topics_list:
            print(f"\n📖 Learning: {topic}")
            result = self.search_and_learn(topic)
            results.append({
                'topic': topic,
                'status': result['status']
            })
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        
        return {
            'status': 'success',
            'response': f"✅ Learned {success_count}/{len(topics_list)} topics!\n✅ {success_count}/{len(topics_list)} টি বিষয় শিখেছি!",
            'type': 'batch_learning',
            'results': results
        }
    
    def get_statistics(self):
        """Get learning statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total topics learned
            cursor.execute("SELECT COUNT(*) FROM internet_learned")
            total_topics = cursor.fetchone()[0]
            
            # Total words learned
            cursor.execute("SELECT SUM(word_count) FROM internet_learned")
            total_words = cursor.fetchone()[0] or 0
            
            # Topics by category
            cursor.execute("""
                SELECT category, COUNT(*) 
                FROM internet_learned 
                GROUP BY category
            """)
            categories = cursor.fetchall()
            
            response = f"""📊 Learning Statistics / শেখার পরিসংখ্যান:

📚 Total Topics Learned: {total_topics}
📝 Total Words Learned: {total_words}

📂 Topics by Category:
"""
            for category, count in categories:
                response += f"   • {category}: {count} topics\n"
            
            return {
                'status': 'success',
                'response': response,
                'type': 'statistics'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'response': f"Statistics error: {e}",
                'type': 'statistics'
            }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Main function for testing"""
    print("\n" + "=" * 80)
    print("  [BRAIN] JARVIS INTERNET LEARNER")
    print("  [BRAIN] JARVIS ইন্টারনেট শিক্ষার্থী")
    print("=" * 80)
    
    learner = InternetLearner()
    
    if len(sys.argv) > 1:
        # Command line mode
        command = ' '.join(sys.argv[1:])
        
        if command.startswith('learn '):
            topic = command.replace('learn ', '')
            result = learner.search_and_learn(topic)
            print(f"\n{result['response']}")
        
        elif command == 'list':
            result = learner.get_learned_topics()
            print(f"\n{result['response']}")
        
        elif command.startswith('search '):
            query = command.replace('search ', '')
            result = learner.search_learned_knowledge(query)
            print(f"\n{result['response']}")
        
        elif command == 'stats':
            result = learner.get_statistics()
            print(f"\n{result['response']}")
    
    else:
        # Interactive mode
        print("\nCommands:")
        print("  learn <topic>  - Learn about a topic")
        print("  list           - List learned topics")
        print("  search <query> - Search learned knowledge")
        print("  stats          - Show statistics")
        print("  exit           - Exit")
        
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("[ROBOT] JARVIS: Goodbye!")
                    break
                
                if user_input.startswith('learn '):
                    topic = user_input.replace('learn ', '')
                    result = learner.search_and_learn(topic)
                    print(f"\n[ROBOT] JARVIS: {result['response']}")
                
                elif user_input == 'list':
                    result = learner.get_learned_topics()
                    print(f"\n[ROBOT] JARVIS: {result['response']}")
                
                elif user_input.startswith('search '):
                    query = user_input.replace('search ', '')
                    result = learner.search_learned_knowledge(query)
                    print(f"\n[ROBOT] JARVIS: {result['response']}")
                
                elif user_input == 'stats':
                    result = learner.get_statistics()
                    print(f"\n[ROBOT] JARVIS: {result['response']}")
                
                else:
                    print("\n[ROBOT] JARVIS: Unknown command. Try 'learn <topic>', 'list', 'search <query>', or 'stats'")
            
            except KeyboardInterrupt:
                print("\n\n[ROBOT] JARVIS: Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n[X] Error: {e}")
    
    learner.close()


if __name__ == "__main__":
    main()
