"""
JARVIS CONVERSATION LEARNER
Learns how to talk, have conversations, answer questions naturally

Features:
- Learns conversations from internet
- Learns question-answer patterns
- Learns sentence structures
- Learns natural language responses
- Saves to database for future use
"""

import os
import sqlite3
import requests
from datetime import datetime
import random
import re

class ConversationLearner:
    """Learns conversations and how to talk naturally"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.init_db()
        
        # Conversation topics to learn
        self.conversation_topics = [
            # Greetings
            "how to greet someone", "saying hello", "good morning greetings",
            "how to introduce yourself", "meeting someone new",
            
            # Questions
            "how to ask questions", "question words", "asking for help",
            "asking about weather", "asking about time", "asking about location",
            
            # Responses
            "how to answer questions", "polite responses", "agreeing and disagreeing",
            "expressing opinions", "giving suggestions", "making recommendations",
            
            # Emotions
            "expressing happiness", "expressing sadness", "expressing anger",
            "showing empathy", "comforting someone", "encouraging words",
            
            # Daily conversation
            "talking about weather", "talking about food", "talking about hobbies",
            "talking about work", "talking about family", "talking about plans",
            
            # Technical conversation
            "explaining programming", "talking about technology", "discussing AI",
            "explaining concepts", "teaching something", "answering technical questions",
            
            # Bengali conversation
            "bangla conversation", "bengali greetings", "bangla questions",
            "bengali responses", "bangla daily talk", "bengali expressions"
        ]
        
        # Common conversation patterns
        self.patterns = {
            'greeting': [
                "Hello! How are you?",
                "Hi there! How can I help you?",
                "Good morning! What can I do for you?",
                "Hey! Nice to meet you!",
                "Greetings! How may I assist you?"
            ],
            'question': [
                "What is {topic}?",
                "How does {topic} work?",
                "Can you explain {topic}?",
                "Tell me about {topic}",
                "Why is {topic} important?"
            ],
            'response': [
                "That's a great question!",
                "Let me explain...",
                "Here's what I know...",
                "I understand your concern.",
                "That's interesting!"
            ],
            'agreement': [
                "I agree with you.",
                "You're absolutely right!",
                "That makes sense.",
                "I think so too.",
                "Exactly!"
            ],
            'disagreement': [
                "I see it differently.",
                "I'm not sure about that.",
                "Let me offer another perspective.",
                "I respectfully disagree.",
                "That's one way to look at it."
            ],
            'thanks': [
                "Thank you so much!",
                "I appreciate your help!",
                "Thanks a lot!",
                "That's very kind of you!",
                "I'm grateful!"
            ],
            'apology': [
                "I'm sorry about that.",
                "My apologies.",
                "I apologize for the confusion.",
                "Sorry, let me clarify.",
                "Pardon me."
            ]
        }
        
        print("✅ Conversation Learner initialized!")
        print("✅ Ready to learn how to talk!")
    
    def init_db(self):
        """Initialize database for conversations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations_learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    answer TEXT,
                    context TEXT,
                    pattern_type TEXT,
                    language TEXT DEFAULT 'english',
                    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            # Create sentence patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sentence_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT,
                    example TEXT,
                    category TEXT,
                    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Conversation database ready!")
            
        except Exception as e:
            print(f"⚠️ Database init error: {e}")
    
    def learn_from_wikipedia(self, topic):
        """Learn conversation patterns from Wikipedia"""
        try:
            print(f"📚 Learning conversation about: {topic}")
            
            # Wikipedia API
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                extract = data.get('extract', '')
                
                if extract:
                    # Extract sentences
                    sentences = re.split(r'[.!?]+', extract)
                    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
                    
                    # Save conversation patterns
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    
                    for sentence in sentences[:10]:  # First 10 sentences
                        # Create Q&A pairs
                        question = f"What is {topic}?"
                        answer = sentence
                        
                        cursor.execute('''
                            INSERT INTO conversations_learned 
                            (question, answer, context, pattern_type, language)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (question, answer, topic, 'factual', 'english'))
                    
                    conn.commit()
                    conn.close()
                    
                    print(f"✅ Learned {len(sentences[:10])} conversation patterns about {topic}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Wikipedia learning error: {e}")
            return False
    
    def learn_conversation_patterns(self):
        """Learn basic conversation patterns"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            count = 0
            
            # Learn greeting patterns
            greetings = [
                ("Hello", "Hello! How can I help you?", "greeting"),
                ("Hi", "Hi there! What can I do for you?", "greeting"),
                ("Good morning", "Good morning! How are you today?", "greeting"),
                ("How are you", "I'm doing great, thank you! How about you?", "greeting"),
                ("What's up", "Not much! Just here to help you. What do you need?", "greeting"),
            ]
            
            for q, a, pattern in greetings:
                cursor.execute('''
                    INSERT INTO conversations_learned 
                    (question, answer, context, pattern_type, language)
                    VALUES (?, ?, ?, ?, ?)
                ''', (q, a, 'greeting', pattern, 'english'))
                count += 1
            
            # Learn question patterns
            questions = [
                ("What is Python", "Python is a high-level programming language known for its simplicity and readability.", "technical"),
                ("How does AI work", "AI works by using algorithms and data to learn patterns and make decisions.", "technical"),
                ("What is machine learning", "Machine learning is a subset of AI that enables systems to learn from data.", "technical"),
                ("Tell me about yourself", "I'm JARVIS, your AI assistant. I can help you with various tasks!", "personal"),
                ("What can you do", "I can help with programming, answer questions, search the web, and much more!", "personal"),
            ]
            
            for q, a, pattern in questions:
                cursor.execute('''
                    INSERT INTO conversations_learned 
                    (question, answer, context, pattern_type, language)
                    VALUES (?, ?, ?, ?, ?)
                ''', (q, a, 'question', pattern, 'english'))
                count += 1
            
            # Learn Bengali patterns
            bengali = [
                ("হ্যালো", "হ্যালো! আমি কিভাবে সাহায্য করতে পারি?", "greeting"),
                ("তুমি কেমন আছো", "আমি ভালো আছি, ধন্যবাদ! তুমি কেমন?", "greeting"),
                ("Python কি", "Python একটি programming language যা সহজ এবং শক্তিশালী।", "technical"),
                ("তুমি কি করতে পারো", "আমি programming, প্রশ্নের উত্তর, web search এবং আরো অনেক কিছু করতে পারি!", "personal"),
            ]
            
            for q, a, pattern in bengali:
                cursor.execute('''
                    INSERT INTO conversations_learned 
                    (question, answer, context, pattern_type, language)
                    VALUES (?, ?, ?, ?, ?)
                ''', (q, a, 'bengali', pattern, 'bengali'))
                count += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ Learned {count} conversation patterns!")
            return True
            
        except Exception as e:
            print(f"⚠️ Pattern learning error: {e}")
            return False
    
    def learn_from_topics(self, num_topics=10):
        """Learn conversations from multiple topics"""
        print(f"\n🤖 Learning conversations from {num_topics} topics...")
        
        learned = 0
        topics = random.sample(self.conversation_topics, min(num_topics, len(self.conversation_topics)))
        
        for topic in topics:
            print(f"\n📖 Topic: {topic}")
            if self.learn_from_wikipedia(topic):
                learned += 1
            
            # Small delay
            import time
            time.sleep(1)
        
        print(f"\n✅ Learned conversations from {learned}/{num_topics} topics!")
        return learned
    
    def get_response(self, user_input):
        """Get a learned response for user input"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Search for matching conversation
            cursor.execute('''
                SELECT answer, pattern_type FROM conversations_learned
                WHERE question LIKE ? OR question LIKE ?
                ORDER BY usage_count ASC
                LIMIT 1
            ''', (f'%{user_input}%', f'{user_input}%'))
            
            result = cursor.fetchone()
            
            if result:
                answer, pattern_type = result
                
                # Update usage count
                cursor.execute('''
                    UPDATE conversations_learned
                    SET usage_count = usage_count + 1
                    WHERE answer = ?
                ''', (answer,))
                
                conn.commit()
                conn.close()
                
                return {
                    'status': 'success',
                    'response': answer,
                    'pattern_type': pattern_type,
                    'learned': True
                }
            
            conn.close()
            return {
                'status': 'not_found',
                'response': "I haven't learned how to respond to that yet. Let me learn more!",
                'learned': False
            }
            
        except Exception as e:
            print(f"⚠️ Response error: {e}")
            return {
                'status': 'error',
                'response': f"Error: {e}",
                'learned': False
            }
    
    def get_statistics(self):
        """Get conversation learning statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total conversations
            cursor.execute('SELECT COUNT(*) FROM conversations_learned')
            total = cursor.fetchone()[0]
            
            # By pattern type
            cursor.execute('''
                SELECT pattern_type, COUNT(*) as count
                FROM conversations_learned
                GROUP BY pattern_type
                ORDER BY count DESC
            ''')
            by_pattern = cursor.fetchall()
            
            # By language
            cursor.execute('''
                SELECT language, COUNT(*) as count
                FROM conversations_learned
                GROUP BY language
            ''')
            by_language = cursor.fetchall()
            
            # Most used
            cursor.execute('''
                SELECT question, answer, usage_count
                FROM conversations_learned
                ORDER BY usage_count DESC
                LIMIT 10
            ''')
            most_used = cursor.fetchall()
            
            conn.close()
            
            return {
                'total': total,
                'by_pattern': by_pattern,
                'by_language': by_language,
                'most_used': most_used
            }
            
        except Exception as e:
            print(f"⚠️ Statistics error: {e}")
            return None


def main():
    """Main function for testing"""
    print("\n" + "="*80)
    print("  🗣️ JARVIS CONVERSATION LEARNER")
    print("  🗣️ Learning how to talk naturally!")
    print("="*80)
    
    learner = ConversationLearner()
    
    # Learn basic patterns
    print("\n📚 Learning basic conversation patterns...")
    learner.learn_conversation_patterns()
    
    # Learn from topics
    print("\n📚 Learning from conversation topics...")
    learner.learn_from_topics(5)
    
    # Show statistics
    print("\n📊 Conversation Learning Statistics:")
    stats = learner.get_statistics()
    if stats:
        print(f"  Total conversations learned: {stats['total']}")
        print(f"\n  By pattern type:")
        for pattern, count in stats['by_pattern']:
            print(f"    {pattern}: {count}")
        print(f"\n  By language:")
        for lang, count in stats['by_language']:
            print(f"    {lang}: {count}")
    
    # Test responses
    print("\n🧪 Testing learned responses:")
    test_inputs = ["Hello", "What is Python", "How are you", "হ্যালো"]
    for inp in test_inputs:
        result = learner.get_response(inp)
        print(f"\n  Input: {inp}")
        print(f"  Response: {result['response']}")
        print(f"  Learned: {result['learned']}")


if __name__ == "__main__":
    main()
