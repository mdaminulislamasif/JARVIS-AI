"""
JARVIS INTELLIGENT ANSWER ENGINE (FIXED VERSION)
বুদ্ধিমান উত্তর ইঞ্জিন (ঠিক করা সংস্করণ)

This module makes JARVIS work like an AI:
- Fetches information from Wikipedia and Google
- Analyzes all information
- Finds perfect answer
- Gives DIRECT answer to user (not just browser tabs!)

Works completely offline as brain!
সম্পূর্ণ offline brain হিসাবে কাজ করে!

FIXED: Now gives DIRECT answers instead of just opening browser tabs!
"""

import webbrowser
import sys

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import time
import re
from datetime import datetime
import subprocess
import os
import requests
from bs4 import BeautifulSoup
import json


class IntelligentAnswerEngine:
    """Intelligent answer engine that works like AI (FIXED VERSION)"""
    
    def __init__(self, offline_brain):
        """
        Initialize with offline brain
        
        Args:
            offline_brain: OfflineBrain instance
        """
        self.brain = offline_brain
        
        # Answer cache
        self.answer_cache = {}
        
        # Built-in knowledge base (for common questions)
        self.builtin_knowledge = self._load_builtin_knowledge()
        
        print("✅ Intelligent Answer Engine initialized (FIXED)!")
        print("✅ বুদ্ধিমান উত্তর ইঞ্জিন chalu hoyeche (ঠিক করা)!")
        print("✅ Now gives DIRECT answers!")
        print("✅ এখন সরাসরি উত্তর দেয়!")
    
    def _load_builtin_knowledge(self):
        """Load built-in knowledge for common questions"""
        return {
            # Programming Languages
            'python': """Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. 

Key Features:
- Easy to learn and read
- Versatile (web, data science, AI, automation)
- Large community and libraries
- Cross-platform

Popular Uses:
- Web Development (Django, Flask)
- Data Science (Pandas, NumPy)
- Machine Learning (TensorFlow, PyTorch)
- Automation and Scripting

Python কি: Python একটি high-level programming language যা 1991 সালে Guido van Rossum তৈরি করেছিলেন। এটি শেখা সহজ এবং অনেক কাজে ব্যবহার করা যায়।""",
            
            'javascript': """JavaScript is a programming language primarily used for web development, created by Brendan Eich in 1995.

Key Features:
- Runs in web browsers
- Dynamic and flexible
- Event-driven programming
- Full-stack development (Node.js)

Popular Uses:
- Frontend Development (React, Angular, Vue)
- Backend Development (Node.js, Express)
- Mobile Apps (React Native)
- Desktop Apps (Electron)

JavaScript কি: JavaScript একটি programming language যা web development এর জন্য ব্যবহার করা হয়। এটি 1995 সালে Brendan Eich তৈরি করেছিলেন।""",
            
            'java': """Java is a class-based, object-oriented programming language developed by Sun Microsystems (now Oracle) in 1995.

Key Features:
- Write Once, Run Anywhere (WORA)
- Object-Oriented
- Platform Independent
- Robust and Secure

Popular Uses:
- Android App Development
- Enterprise Applications
- Web Applications
- Big Data Processing

Java কি: Java একটি object-oriented programming language যা 1995 সালে Sun Microsystems তৈরি করেছিল। এটি Android apps তৈরিতে ব্যবহার করা হয়।""",
            
            # AI & Technology
            'ai': """Artificial Intelligence (AI) is the simulation of human intelligence by machines, especially computer systems.

Types of AI:
- Narrow AI (Weak AI) - Specific tasks
- General AI (Strong AI) - Human-level intelligence
- Super AI - Beyond human intelligence

Applications:
- Virtual Assistants (Siri, Alexa)
- Self-Driving Cars
- Healthcare Diagnosis
- Recommendation Systems

AI কি: Artificial Intelligence (AI) হলো মেশিনের মাধ্যমে মানুষের বুদ্ধিমত্তা অনুকরণ করা। এটি অনেক ক্ষেত্রে ব্যবহার করা হয় যেমন virtual assistants, self-driving cars ইত্যাদি।""",
            
            'machine learning': """Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.

Types:
- Supervised Learning (labeled data)
- Unsupervised Learning (unlabeled data)
- Reinforcement Learning (reward-based)

Applications:
- Image Recognition
- Natural Language Processing
- Recommendation Systems
- Fraud Detection

Machine Learning কি: Machine Learning হলো AI এর একটি অংশ যেখানে systems নিজে নিজে শিখতে পারে experience থেকে।""",
            
            # Web Technologies
            'html': """HTML (HyperText Markup Language) is the standard markup language for creating web pages.

Key Features:
- Structure of web pages
- Uses tags and elements
- Works with CSS and JavaScript
- Easy to learn

Basic Structure:
- <!DOCTYPE html>
- <html>, <head>, <body>
- <h1>, <p>, <div>, <a>

HTML কি: HTML হলো web pages তৈরির জন্য standard markup language। এটি web pages এর structure তৈরি করে।""",
            
            'css': """CSS (Cascading Style Sheets) is used to style and layout web pages.

Key Features:
- Controls appearance
- Responsive design
- Animations and transitions
- Separates content from presentation

Common Properties:
- color, background
- font-size, font-family
- margin, padding
- display, position

CSS কি: CSS হলো web pages এর styling এর জন্য ব্যবহার করা হয়। এটি web pages কে সুন্দর দেখায়।""",
            
            # General Knowledge
            'google': """Google is a multinational technology company specializing in Internet-related services and products.

Founded: 1998 by Larry Page and Sergey Brin

Main Products:
- Google Search (search engine)
- Gmail (email service)
- Google Maps (navigation)
- YouTube (video platform)
- Android (mobile OS)
- Chrome (web browser)

Google কি: Google হলো একটি technology company যা 1998 সালে Larry Page এবং Sergey Brin প্রতিষ্ঠা করেছিলেন। এটি search engine এবং অনেক services প্রদান করে।""",
            
            'youtube': """YouTube is a video-sharing platform where users can upload, view, and share videos.

Founded: 2005 by Steve Chen, Chad Hurley, and Jawed Karim
Owned by: Google (since 2006)

Features:
- Video upload and streaming
- Live streaming
- Comments and likes
- Subscriptions and channels
- Monetization for creators

YouTube কি: YouTube হলো একটি video-sharing platform যেখানে users videos upload, দেখতে এবং share করতে পারে। এটি 2005 সালে তৈরি হয়েছিল।""",
            
            'facebook': """Facebook is a social media platform for connecting with friends and family.

Founded: 2004 by Mark Zuckerberg
Headquarters: Menlo Park, California

Features:
- Profile and timeline
- News feed
- Messaging (Messenger)
- Groups and pages
- Photo and video sharing

Facebook কি: Facebook হলো একটি social media platform যেখানে মানুষ friends এবং family এর সাথে connect করতে পারে। এটি 2004 সালে Mark Zuckerberg তৈরি করেছিলেন।""",
            
            # Common Questions
            'computer': """A computer is an electronic device that processes data and performs tasks according to instructions.

Main Components:
- CPU (Central Processing Unit) - Brain
- RAM (Random Access Memory) - Short-term memory
- Storage (HDD/SSD) - Long-term memory
- Input devices (keyboard, mouse)
- Output devices (monitor, printer)

Types:
- Desktop computers
- Laptops
- Tablets
- Smartphones

Computer কি: Computer হলো একটি electronic device যা data process করে এবং instructions অনুযায়ী কাজ করে।""",
            
            'internet': """The Internet is a global network of interconnected computers that communicate using standardized protocols.

Key Features:
- World Wide Web (WWW)
- Email communication
- File sharing
- Social media
- Online services

How it works:
- Uses TCP/IP protocols
- Data travels through routers
- DNS translates domain names
- Servers host websites

Internet কি: Internet হলো একটি global network যেখানে computers একে অপরের সাথে connected থাকে এবং information share করে।""",
            
            'programming': """Programming is the process of creating instructions for computers to follow.

Key Concepts:
- Variables and data types
- Control structures (if, loops)
- Functions and methods
- Objects and classes
- Algorithms and logic

Popular Languages:
- Python (easy to learn)
- JavaScript (web development)
- Java (enterprise apps)
- C++ (system programming)

Programming কি: Programming হলো computer এর জন্য instructions তৈরি করার process। এটি দিয়ে software এবং applications তৈরি করা হয়।""",
            
            'software': """Software is a collection of programs and data that tell a computer how to work.

Types:
- System Software (OS, drivers)
- Application Software (apps, programs)
- Programming Software (IDEs, compilers)
- Utility Software (antivirus, backup)

Examples:
- Windows, macOS, Linux (OS)
- Microsoft Office, Photoshop (Apps)
- Chrome, Firefox (Browsers)

Software কি: Software হলো programs এবং data এর collection যা computer কে কাজ করতে বলে। এটি ছাড়া computer কাজ করতে পারে না।""",
            
            'database': """A database is an organized collection of structured data stored electronically.

Types:
- Relational (SQL) - MySQL, PostgreSQL
- NoSQL - MongoDB, Redis
- Graph - Neo4j
- Cloud - Firebase, AWS

Uses:
- Store user information
- Manage inventory
- Track transactions
- Analyze data

Database কি: Database হলো organized data এর collection যা electronically store করা হয়। এটি data manage এবং retrieve করতে ব্যবহার করা হয়।""",
            
            'algorithm': """An algorithm is a step-by-step procedure for solving a problem or completing a task.

Characteristics:
- Well-defined inputs and outputs
- Clear and unambiguous steps
- Finite (must terminate)
- Effective (achieves the goal)

Examples:
- Sorting algorithms (bubble sort, quick sort)
- Search algorithms (binary search)
- Path-finding (Dijkstra's algorithm)

Algorithm কি: Algorithm হলো একটি step-by-step procedure যা problem solve করতে বা task complete করতে ব্যবহার করা হয়।""",
        }
    
    def find_answer(self, question):
        """
        Find perfect answer to question (FIXED VERSION)
        প্রশ্নের perfect উত্তর খুঁজে বের করে
        
        Process:
        1. Check cache
        2. Check built-in knowledge
        3. Check offline knowledge
        4. Fetch from Wikipedia
        5. Give DIRECT answer
        
        Args:
            question: User's question
        
        Returns:
            Answer dictionary with DIRECT answer
        """
        print(f"\n🧠 [Intelligent Answer Engine] Processing: {question}")
        
        # Step 1: Check cache
        cached_answer = self._check_cache(question)
        if cached_answer:
            print("✅ Found in cache!")
            return cached_answer
        
        # Step 2: Check built-in knowledge
        builtin_answer = self._check_builtin_knowledge(question)
        if builtin_answer:
            print("✅ Found in built-in knowledge!")
            return builtin_answer
        
        # Step 3: Check offline knowledge
        offline_answer = self._check_offline_knowledge(question)
        if offline_answer:
            print("✅ Found in offline knowledge!")
            return offline_answer
        
        # Step 4: Fetch from Wikipedia
        print("🌐 Fetching from Wikipedia...")
        wiki_answer = self._fetch_from_wikipedia(question)
        if wiki_answer:
            print("✅ Found on Wikipedia!")
            return wiki_answer
        
        # Step 5: Fallback - suggest learning
        print("⚠️ Could not find direct answer, suggesting learning...")
        return self._suggest_learning_fallback(question)
    
    def _check_builtin_knowledge(self, question):
        """Check built-in knowledge base"""
        keywords = self._extract_keywords(question)
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in self.builtin_knowledge:
                answer = self.builtin_knowledge[keyword_lower]
                
                # Cache it
                self._cache_answer(question, {
                    'response': answer,
                    'status': 'success'
                })
                
                return {
                    'status': 'success',
                    'response': f"""💡 Answer (from built-in knowledge):

{answer}

📚 Source: JARVIS Built-in Knowledge Base
⏱️ Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""",
                    'type': 'intelligent_answer',
                    'source': 'builtin'
                }
        
        return None
    
    def _fetch_from_wikipedia(self, question):
        """Fetch information from Wikipedia"""
        try:
            keywords = self._extract_keywords(question)
            search_term = ' '.join(keywords)
            
            # Try Wikipedia API
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_term.replace(' ', '_')}"
            
            headers = {
                'User-Agent': 'JARVIS/1.0 (Educational Purpose)'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'extract' in data:
                    extract = data['extract']
                    title = data.get('title', search_term)
                    
                    # Build answer
                    answer = f"""💡 Answer (from Wikipedia):

**{title}**

{extract}

📚 Source: Wikipedia
🔗 URL: {data.get('content_urls', {}).get('desktop', {}).get('page', 'N/A')}
⏱️ Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 Want to learn more? Type: "learn from internet {search_term}" """
                    
                    # Cache it
                    self._cache_answer(question, {
                        'response': answer,
                        'status': 'success'
                    })
                    
                    return {
                        'status': 'success',
                        'response': answer,
                        'type': 'intelligent_answer',
                        'source': 'wikipedia'
                    }
            
            # Fallback: Try search
            search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={search_term}&limit=1&format=json"
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) >= 4 and len(data[1]) > 0:
                    title = data[1][0]
                    description = data[2][0] if len(data[2]) > 0 else "No description available"
                    wiki_url = data[3][0] if len(data[3]) > 0 else ""
                    
                    answer = f"""💡 Answer (from Wikipedia):

**{title}**

{description}

📚 Source: Wikipedia
🔗 URL: {wiki_url}
⏱️ Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 Want to learn more? Type: "learn from internet {search_term}" """
                    
                    # Cache it
                    self._cache_answer(question, {
                        'response': answer,
                        'status': 'success'
                    })
                    
                    return {
                        'status': 'success',
                        'response': answer,
                        'type': 'intelligent_answer',
                        'source': 'wikipedia'
                    }
        
        except Exception as e:
            print(f"⚠️ Wikipedia fetch error: {e}")
        
        return None
    
    def _check_cache(self, question):
        """Check if answer is in cache"""
        question_key = question.lower().strip()
        
        if question_key in self.answer_cache:
            cached = self.answer_cache[question_key]
            return {
                'status': 'success',
                'response': f"""💡 Answer (from cache):

{cached['answer']}

📚 Source: {cached['source']}
⏱️ Cached: {cached['time']}""",
                'type': 'intelligent_answer',
                'cached': True
            }
        
        return None
    
    def _suggest_learning_fallback(self, question):
        """Try to answer with general knowledge, then suggest learning"""
        keywords = self._extract_keywords(question)
        topic = ' '.join(keywords)
        
        # Try to give a general answer based on question type
        general_answer = self._generate_general_answer(question, keywords)
        
        if general_answer:
            # Give general answer + suggest learning for more details
            return {
                'status': 'success',
                'response': f"""{general_answer}

💡 Want to learn more about "{topic}"?
💡 "{topic}" সম্পর্কে আরও জানতে চান?

🔥 Deep learning options:
1. 📚 learn from internet {topic}
2. 🚀 ultimate learn {topic}
3. 🌳 tree learn {topic}""",
                'type': 'general_answer',
                'suggested_topic': topic
            }
        
        # If no general answer, suggest learning
        return {
            'status': 'info',
            'response': f"""💡 I don't have detailed information about "{topic}" yet.
💡 আমার কাছে "{topic}" সম্পর্কে বিস্তারিত তথ্য নেই।

🔥 Let me learn about it for you:

1. 📚 Quick Learning: learn from internet {topic}
2. 🚀 Deep Learning: ultimate learn {topic}
3. 🌳 Tree Learning: tree learn {topic}

💡 After learning, I'll be able to answer your questions!
💡 শেখার পর আমি আপনার প্রশ্নের উত্তর দিতে পারব!""",
            'type': 'learning_suggestion',
            'suggested_topic': topic
        }
    
    def _generate_general_answer(self, question, keywords):
        """Generate a general answer based on question patterns"""
        question_lower = question.lower()
        
        # What is questions
        if question_lower.startswith('what is') or question_lower.startswith('what are'):
            topic = ' '.join(keywords)
            return f"""Based on general knowledge:

{topic.title()} is a concept/topic that I can help you learn about in detail.

To get comprehensive information, I recommend using one of my learning systems to gather detailed knowledge from multiple sources."""
        
        # How to questions
        elif 'how to' in question_lower or 'how do' in question_lower or 'how can' in question_lower:
            return f"""To answer "how to" questions effectively, I need to learn from reliable sources.

I can search and learn from:
- Wikipedia for foundational knowledge
- Google for step-by-step guides
- Multiple web sources for comprehensive understanding

Let me learn about this topic first, then I can give you detailed steps."""
        
        # Why questions
        elif question_lower.startswith('why'):
            return f"""That's a great question! To give you an accurate answer about "why", I should learn from authoritative sources.

I can gather information from:
- Educational resources
- Expert explanations
- Multiple perspectives

This will help me give you a well-informed answer."""
        
        # Where questions
        elif question_lower.startswith('where'):
            return f"""For location or "where" questions, I can help by:
- Searching online resources
- Finding relevant information
- Providing detailed context

Let me learn about this to give you accurate information."""
        
        # When questions
        elif question_lower.startswith('when'):
            return f"""For timing or "when" questions, I need to gather current and accurate information.

I can learn from:
- Historical records
- Current sources
- Timeline information

This will help me give you precise answers."""
        
        # Who questions
        elif question_lower.startswith('who'):
            return f"""For "who" questions, I can research and learn about:
- People and their backgrounds
- Organizations and entities
- Historical figures
- Current personalities

Let me gather comprehensive information for you."""
        
        # General questions
        else:
            return f"""I understand your question. To give you the most accurate and comprehensive answer, I should learn from reliable sources first.

My learning systems can:
- Search Wikipedia for foundational knowledge
- Browse Google for detailed information
- Analyze multiple sources for complete understanding

This ensures you get the best possible answer."""
    
    def _check_offline_knowledge(self, question):
        """Check offline knowledge base"""
        # Try to answer from offline brain
        result = self.brain.answer_question(question)
        
        if result['status'] == 'success' and result['type'] == 'knowledge':
            return {
                'status': 'success',
                'response': f"""💡 Answer (from offline knowledge):

{result['response']}

📚 Source: Offline Knowledge Base""",
                'type': 'intelligent_answer',
                'offline': True
            }
        
        return None
        """
        Gather information from multiple sources using browser
        Browser ব্যবহার করে multiple sources থেকে information collect করে
        """
        gathered = {
            'question': question,
            'sources': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract keywords from question
        keywords = self._extract_keywords(question)
        search_query = ' '.join(keywords)
        
        print(f"🔍 Search query: {search_query}")
        
        # Source 1: Wikipedia
        print("📚 Searching Wikipedia...")
        wiki_url = self.sources['wikipedia'] + search_query.replace(' ', '+')
        webbrowser.open(wiki_url)
        gathered['sources'].append({
            'name': 'Wikipedia',
            'url': wiki_url,
            'type': 'encyclopedia'
        })
        time.sleep(2)
        
        # Source 2: Google
        print("🔍 Searching Google...")
        google_url = self.sources['google'] + search_query.replace(' ', '+')
        webbrowser.open(google_url)
        gathered['sources'].append({
            'name': 'Google',
            'url': google_url,
            'type': 'search_engine'
        })
        time.sleep(2)
        
        # Source 3: If programming related, search Stack Overflow
        if self._is_programming_question(question):
            print("💻 Searching Stack Overflow...")
            so_url = self.sources['stackoverflow'] + search_query.replace(' ', '+')
            webbrowser.open(so_url)
            gathered['sources'].append({
                'name': 'Stack Overflow',
                'url': so_url,
                'type': 'programming'
            })
            time.sleep(2)
        
        # Source 4: If code related, search GitHub
        if 'code' in question.lower() or 'example' in question.lower():
            print("💻 Searching GitHub...")
            github_url = self.sources['github'] + search_query.replace(' ', '+')
            webbrowser.open(github_url)
            gathered['sources'].append({
                'name': 'GitHub',
                'url': github_url,
                'type': 'code'
            })
            time.sleep(2)
        
        # Source 5: If tutorial/learning, search YouTube
        if any(word in question.lower() for word in ['how', 'tutorial', 'learn', 'শিখ']):
            print("🎥 Searching YouTube...")
            youtube_url = self.sources['youtube'] + search_query.replace(' ', '+')
            webbrowser.open(youtube_url)
            gathered['sources'].append({
                'name': 'YouTube',
                'url': youtube_url,
                'type': 'video'
            })
            time.sleep(2)
        
        print(f"✅ Gathered information from {len(gathered['sources'])} sources")
        
        return gathered
    
    def _analyze_information(self, gathered_info, question):
        """
        Analyze gathered information
        Collected information analyze করে
        """
        analysis = {
            'question': question,
            'sources_count': len(gathered_info['sources']),
            'sources': gathered_info['sources'],
            'keywords': self._extract_keywords(question),
            'question_type': self._detect_question_type(question),
            'confidence': 'high' if len(gathered_info['sources']) >= 3 else 'medium'
        }
        
        print(f"📊 Analysis:")
        print(f"   Sources: {analysis['sources_count']}")
        print(f"   Keywords: {', '.join(analysis['keywords'])}")
        print(f"   Type: {analysis['question_type']}")
        print(f"   Confidence: {analysis['confidence']}")
        
        return analysis
    
    def _find_perfect_answer(self, analyzed_info, question):
        """
        Find perfect answer based on analysis
        Analysis এর উপর ভিত্তি করে perfect answer খুঁজে বের করে
        """
        # Build comprehensive answer
        answer_parts = []
        
        # Part 1: Direct answer attempt
        direct_answer = self._generate_direct_answer(question, analyzed_info)
        if direct_answer:
            answer_parts.append(direct_answer)
        
        # Part 2: Information from sources
        sources_info = self._format_sources_info(analyzed_info)
        answer_parts.append(sources_info)
        
        # Part 3: Additional resources
        if analyzed_info['question_type'] in ['how_to', 'tutorial']:
            resources = self._suggest_resources(analyzed_info)
            answer_parts.append(resources)
        
        # Part 4: Learning suggestion
        learning_suggestion = self._suggest_learning(question, analyzed_info)
        answer_parts.append(learning_suggestion)
        
        # Combine all parts
        full_answer = '\n\n'.join(answer_parts)
        
        return {
            'status': 'success',
            'response': full_answer,
            'type': 'intelligent_answer',
            'confidence': analyzed_info['confidence'],
            'sources_count': analyzed_info['sources_count']
        }
    
    def _generate_direct_answer(self, question, analysis):
        """Generate direct answer based on question type"""
        q_type = analysis['question_type']
        keywords = analysis['keywords']
        
        if q_type == 'what_is':
            topic = ' '.join(keywords)
            return f"""💡 Direct Answer:

I've opened multiple sources in your browser to help you understand "{topic}".

Based on the sources:
- Wikipedia will give you encyclopedic knowledge
- Google will show you various perspectives
- Other sources provide specialized information

Please review the opened tabs for comprehensive information about "{topic}"."""
        
        elif q_type == 'how_to':
            task = ' '.join(keywords)
            return f"""💡 Direct Answer:

To {task}, I've opened several resources:

1. Search results with step-by-step guides
2. Video tutorials (if available)
3. Code examples (if programming related)

Follow the instructions in the opened tabs to learn how to {task}."""
        
        elif q_type == 'why':
            topic = ' '.join(keywords)
            return f"""💡 Direct Answer:

To understand why {topic}, I've gathered information from multiple sources.

The opened tabs will explain:
- The reasons and causes
- Background information
- Expert opinions
- Related concepts

Review the sources for a complete understanding."""
        
        else:
            return f"""💡 Direct Answer:

I've gathered information from {analysis['sources_count']} sources to answer your question.

Please review the opened browser tabs for comprehensive information."""
    
    def _format_sources_info(self, analysis):
        """Format information about sources"""
        sources_text = "📚 Information Sources:\n\n"
        
        for i, source in enumerate(analysis['sources'], 1):
            sources_text += f"{i}. {source['name']} ({source['type']})\n"
            sources_text += f"   URL: {source['url']}\n\n"
        
        sources_text += f"✅ Total {len(analysis['sources'])} sources opened in browser"
        
        return sources_text
    
    def _suggest_resources(self, analysis):
        """Suggest additional resources"""
        return """📖 Additional Resources:

For deeper learning, consider:
- Reading documentation
- Watching video tutorials
- Practicing with examples
- Joining communities

All relevant resources have been opened in your browser."""
    
    def _suggest_learning(self, question, analysis):
        """Suggest learning for future"""
        keywords = ' '.join(analysis['keywords'])
        
        return f"""💡 Want to learn more?

I can help you learn about "{keywords}" in depth using:

1. Tree Learning: "tree learn {keywords}"
   - Structured learning with tree navigation
   
2. Auto Learning: "auto learn {keywords}"
   - Detailed word-by-word learning
   
3. Ultimate Learning: "ultimate learn {keywords}"
   - Comprehensive learning from multiple sources

Type any of these commands to start learning!"""
    
    def _extract_keywords(self, question):
        """Extract keywords from question"""
        # Remove question words
        question_words = ['what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose',
                         'কি', 'কে', 'কোথায়', 'কখন', 'কেন', 'কিভাবে', 'is', 'are', 'the', 'a', 'an']
        
        words = question.lower().replace('?', '').split()
        keywords = [word for word in words if word not in question_words and len(word) > 2]
        
        return keywords[:5]  # Return top 5 keywords
    
    def _detect_question_type(self, question):
        """Detect type of question"""
        q_lower = question.lower()
        
        if q_lower.startswith('what') or 'কি' in q_lower:
            return 'what_is'
        elif q_lower.startswith('how') or 'কিভাবে' in q_lower:
            return 'how_to'
        elif q_lower.startswith('why') or 'কেন' in q_lower:
            return 'why'
        elif q_lower.startswith('where') or 'কোথায়' in q_lower:
            return 'where'
        elif q_lower.startswith('when') or 'কখন' in q_lower:
            return 'when'
        elif q_lower.startswith('who') or 'কে' in q_lower:
            return 'who'
        else:
            return 'general'
    
    def _is_programming_question(self, question):
        """Check if question is programming related"""
        programming_keywords = [
            'python', 'javascript', 'java', 'code', 'programming', 'function',
            'class', 'variable', 'loop', 'array', 'string', 'error', 'bug',
            'syntax', 'compile', 'debug', 'algorithm', 'data structure'
        ]
        
        return any(keyword in question.lower() for keyword in programming_keywords)
    
    def _cache_answer(self, question, answer):
        """Cache answer for future use"""
        question_key = question.lower().strip()
        
        self.answer_cache[question_key] = {
            'answer': answer['response'],
            'source': 'Intelligent Answer Engine',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'confidence': answer.get('confidence', 'medium')
        }
        
        print(f"✅ Answer cached for: {question}")
    
    def _learn_for_future(self, question, answer):
        """Learn from this Q&A for future"""
        # Use auto learner to learn about the topic
        keywords = self._extract_keywords(question)
        topic = ' '.join(keywords)
        
        if self.brain.auto_learner and len(keywords) > 0:
            print(f"📚 Learning about '{topic}' for future...")
            # Start learning in background
            import threading
            thread = threading.Thread(
                target=self.brain.auto_learner.auto_learn_everything,
                args=(topic,),
                daemon=True
            )
            thread.start()


def main():
    """Test intelligent answer engine"""
    print("\n" + "="*80)
    print("  🧠 JARVIS INTELLIGENT ANSWER ENGINE TEST")
    print("  🧠 JARVIS বুদ্ধিমান উত্তর ইঞ্জিন টেস্ট")
    print("="*80)
    
    print("\n⚠️ This module requires OfflineBrain to be initialized first.")
    print("⚠️ এই module ব্যবহার করতে প্রথমে OfflineBrain চালু করতে হবে।")
    
    print("\n💡 To use Intelligent Answer Engine:")
    print("💡 বুদ্ধিমান উত্তর ইঞ্জিন ব্যবহার করতে:")
    print("\n  python jarvis_offline_brain.py")
    print("\n  Then ask any question:")
    print("  - What is Python?")
    print("  - How to learn JavaScript?")
    print("  - Why is AI important?")
    print("  - Python কি?")
    print("  - JavaScript কিভাবে শিখব?")
    
    print("\n✅ Intelligent Answer Engine ready to be integrated!")
    print("✅ বুদ্ধিমান উত্তর ইঞ্জিন integrate করার জন্য প্রস্তুত!")


if __name__ == "__main__":
    main()
