"""
JARVIS AUTO BACKGROUND LEARNER
Automatically learns topics in the background WITHOUT user input!

Features:
- Runs in background 24/7
- Automatically selects topics to learn
- Uses all 4 learning systems
- No user input needed
- Learns popular topics automatically
- Saves everything to database
"""

import os
import time
import random
import threading
import sqlite3
from datetime import datetime

class AutoBackgroundLearner:
    """Automatically learns topics in background without user input"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.is_running = False
        self.learning_thread = None
        
        # Popular topics to learn automatically
        self.topic_categories = {
            'programming': [
                'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'Rust',
                'TypeScript', 'PHP', 'Swift', 'Kotlin', 'R', 'MATLAB', 'Perl',
                'HTML', 'CSS', 'SQL', 'Shell Scripting', 'Assembly'
            ],
            'technology': [
                'Artificial Intelligence', 'Machine Learning', 'Deep Learning',
                'Neural Networks', 'Computer Vision', 'Natural Language Processing',
                'Blockchain', 'Cryptocurrency', 'Cloud Computing', 'DevOps',
                'Cybersecurity', 'Internet of Things', 'Big Data', 'Data Science',
                'Quantum Computing', 'Augmented Reality', 'Virtual Reality',
                '5G Technology', 'Edge Computing', 'Robotics'
            ],
            'frameworks': [
                'React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring Boot',
                'Node.js', 'Express.js', 'TensorFlow', 'PyTorch', 'Keras',
                'Laravel', 'Ruby on Rails', 'ASP.NET', 'Flutter', 'React Native',
                'Electron', 'Next.js', 'Svelte', 'FastAPI'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
                'Microsoft SQL Server', 'Cassandra', 'Elasticsearch', 'Neo4j',
                'DynamoDB', 'Firebase', 'CouchDB', 'MariaDB', 'InfluxDB'
            ],
            'tools': [
                'Git', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible',
                'VS Code', 'IntelliJ IDEA', 'PyCharm', 'Eclipse', 'Vim',
                'Postman', 'Jira', 'Slack', 'GitHub', 'GitLab', 'Bitbucket'
            ],
            'concepts': [
                'Object Oriented Programming', 'Functional Programming',
                'Design Patterns', 'Data Structures', 'Algorithms',
                'Software Architecture', 'Microservices', 'REST API',
                'GraphQL', 'WebSockets', 'Agile', 'Scrum', 'Test Driven Development',
                'Continuous Integration', 'Continuous Deployment'
            ],
            'science': [
                'Physics', 'Chemistry', 'Biology', 'Mathematics', 'Astronomy',
                'Geology', 'Ecology', 'Genetics', 'Neuroscience', 'Psychology',
                'Quantum Mechanics', 'Thermodynamics', 'Electromagnetism',
                'Organic Chemistry', 'Calculus', 'Statistics', 'Probability'
            ],
            'general': [
                'History', 'Geography', 'Economics', 'Philosophy', 'Literature',
                'Art', 'Music', 'Sports', 'Health', 'Nutrition', 'Fitness',
                'Meditation', 'Yoga', 'Cooking', 'Photography', 'Travel'
            ]
        }
        
        # Initialize database
        self.init_db()
        
        print("[OK] Auto Background Learner initialized!")
        print("[OK] Ready to learn automatically in background!")
    
    def init_db(self):
        """Initialize database for tracking learned topics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create table for auto learned topics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auto_background_learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    category TEXT,
                    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    systems_used TEXT,
                    success INTEGER DEFAULT 1
                )
            ''')
            
            conn.commit()
            conn.close()
            print("[OK] Auto background learning database ready!")
            
        except Exception as e:
            print(f"[!] Database init error: {e}")
    
    def get_random_topic(self):
        """Get a random topic to learn"""
        # Select random category
        category = random.choice(list(self.topic_categories.keys()))
        
        # Select random topic from category
        topic = random.choice(self.topic_categories[category])
        
        return topic, category
    
    def check_already_learned(self, topic):
        """Check if topic was already learned recently"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if learned in last 7 days
            cursor.execute('''
                SELECT COUNT(*) FROM auto_background_learned
                WHERE topic = ? AND learned_at > datetime('now', '-7 days')
            ''', (topic,))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count > 0
            
        except Exception as e:
            print(f"[!] Check learned error: {e}")
            return False
    
    def save_learned_topic(self, topic, category, systems_used, success=True):
        """Save learned topic to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO auto_background_learned (topic, category, systems_used, success)
                VALUES (?, ?, ?, ?)
            ''', (topic, category, systems_used, 1 if success else 0))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"[!] Save learned error: {e}")
    
    def learn_topic_with_all_systems(self, topic, category):
        """Learn a topic using all 5 learning systems (including conversation)"""
        print(f"\n{'='*80}")
        print(f"[ROBOT] AUTO LEARNING: {topic} (Category: {category})")
        print(f"{'='*80}")
        
        systems_used = []
        
        try:
            # Import offline brain
            from jarvis_offline_brain import OfflineBrain
            offline_brain = OfflineBrain()
            
            # System 1: Internet Learner
            print(f"[BRAIN] System 1: Internet Learner - Learning {topic}...")
            try:
                result1 = offline_brain.process_command(f"learn from internet {topic}")
                if result1['status'] == 'success':
                    systems_used.append('Internet')
                    print(f"[OK] Internet Learner: Success")
                time.sleep(3)
            except Exception as e:
                print(f"[!] Internet Learner error: {e}")
            
            # System 2: Ultimate Learner
            print(f"[ROCKET] System 2: Ultimate Learner - Learning {topic}...")
            try:
                result2 = offline_brain.process_command(f"ultimate learn {topic}")
                if result2['status'] == 'success':
                    systems_used.append('Ultimate')
                    print(f"[OK] Ultimate Learner: Success")
                time.sleep(3)
            except Exception as e:
                print(f"[!] Ultimate Learner error: {e}")
            
            # System 3: Auto Learner
            print(f"📖 System 3: Auto Learner - Learning {topic}...")
            try:
                result3 = offline_brain.process_command(f"auto learn {topic}")
                if result3['status'] == 'success':
                    systems_used.append('Auto')
                    print(f"[OK] Auto Learner: Success")
                time.sleep(3)
            except Exception as e:
                print(f"[!] Auto Learner error: {e}")
            
            # System 4: Chrome DevTools (skip if Chrome not available)
            print(f"[TOOL] System 4: Chrome DevTools - Learning {topic}...")
            try:
                result4 = offline_brain.process_command(f"devtools learn {topic}")
                if result4['status'] == 'success':
                    systems_used.append('DevTools')
                    print(f"[OK] Chrome DevTools: Success")
            except Exception as e:
                print(f"[!] Chrome DevTools error: {e}")
            
            # System 5: Conversation Learner (Learn how to talk about this topic)
            print(f"🗣️ System 5: Conversation Learner - Learning to talk about {topic}...")
            try:
                from jarvis_conversation_learner import ConversationLearner
                conv_learner = ConversationLearner()
                if conv_learner.learn_from_wikipedia(topic):
                    systems_used.append('Conversation')
                    print(f"[OK] Conversation Learner: Success - Learned how to talk about {topic}")
            except Exception as e:
                print(f"[!] Conversation Learner error: {e}")
            
            # Close offline brain
            offline_brain.close()
            
            # Save to database
            systems_str = ', '.join(systems_used) if systems_used else 'None'
            self.save_learned_topic(topic, category, systems_str, len(systems_used) > 0)
            
            print(f"\n{'='*80}")
            print(f"[OK] AUTO LEARNING COMPLETE: {topic}")
            print(f"📊 Systems used: {systems_str}")
            print(f"{'='*80}\n")
            
            return len(systems_used) > 0
            
        except Exception as e:
            print(f"[X] Auto learning error: {e}")
            return False
    
    def learning_loop(self):
        """Main learning loop - runs continuously"""
        print("\n[ROBOT] AUTO BACKGROUND LEARNER STARTED!")
        print("[ROBOT] Learning automatically without user input...")
        print("[ROBOT] Press Ctrl+C to stop\n")
        
        topics_learned = 0
        
        while self.is_running:
            try:
                # Get random topic
                topic, category = self.get_random_topic()
                
                # Check if already learned recently
                if self.check_already_learned(topic):
                    print(f"⏭️ Skipping {topic} (learned recently)")
                    time.sleep(5)
                    continue
                
                # Learn the topic
                success = self.learn_topic_with_all_systems(topic, category)
                
                if success:
                    topics_learned += 1
                    print(f"📊 Total topics learned: {topics_learned}")
                
                # Wait before learning next topic (5-10 minutes)
                wait_time = random.randint(300, 600)  # 5-10 minutes
                print(f"⏳ Waiting {wait_time//60} minutes before next topic...")
                
                for _ in range(wait_time):
                    if not self.is_running:
                        break
                    time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n[!] Stopping auto background learner...")
                self.is_running = False
                break
            except Exception as e:
                print(f"[X] Learning loop error: {e}")
                time.sleep(60)  # Wait 1 minute on error
        
        print(f"\n[OK] Auto Background Learner stopped!")
        print(f"📊 Total topics learned: {topics_learned}")
    
    def start(self):
        """Start automatic background learning"""
        if self.is_running:
            print("[!] Auto background learner already running!")
            return
        
        self.is_running = True
        self.learning_thread = threading.Thread(target=self.learning_loop, daemon=True)
        self.learning_thread.start()
        
        print("[OK] Auto background learner started!")
        print("[OK] JARVIS will learn automatically in background!")
    
    def stop(self):
        """Stop automatic background learning"""
        if not self.is_running:
            print("[!] Auto background learner not running!")
            return
        
        self.is_running = False
        print("⏳ Stopping auto background learner...")
        
        if self.learning_thread:
            self.learning_thread.join(timeout=5)
        
        print("[OK] Auto background learner stopped!")
    
    def get_statistics(self):
        """Get learning statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total topics learned
            cursor.execute('SELECT COUNT(*) FROM auto_background_learned WHERE success = 1')
            total = cursor.fetchone()[0]
            
            # Topics by category
            cursor.execute('''
                SELECT category, COUNT(*) as count
                FROM auto_background_learned
                WHERE success = 1
                GROUP BY category
                ORDER BY count DESC
            ''')
            by_category = cursor.fetchall()
            
            # Recent topics
            cursor.execute('''
                SELECT topic, category, learned_at, systems_used
                FROM auto_background_learned
                WHERE success = 1
                ORDER BY learned_at DESC
                LIMIT 10
            ''')
            recent = cursor.fetchall()
            
            conn.close()
            
            return {
                'total': total,
                'by_category': by_category,
                'recent': recent
            }
            
        except Exception as e:
            print(f"[!] Statistics error: {e}")
            return None


def main():
    """Main function for testing"""
    print("\n" + "="*80)
    print("  [ROBOT] JARVIS AUTO BACKGROUND LEARNER")
    print("  [ROBOT] Learns automatically WITHOUT user input!")
    print("="*80)
    
    learner = AutoBackgroundLearner()
    
    try:
        learner.start()
        
        # Keep running until Ctrl+C
        # WARNING: Infinite loop - ensure break condition exists
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n[!] Stopping...")
        learner.stop()


if __name__ == "__main__":
    main()
