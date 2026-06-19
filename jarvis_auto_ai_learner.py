"""
JARVIS AUTO AI LEARNER
======================
JARVIS automatically learns from Gemini AI without user interaction!

Features:
- Auto-connects to Gemini AI
- Asks questions automatically
- Learns from responses
- Builds knowledge base
- Works without API key (uses World AI Chat)
- Can be turned ON/OFF

JARVIS নিজে নিজে Gemini AI এর সাথে কথা বলবে এবং শিখবে!
"""

import time
import threading
import random
from datetime import datetime

class AutoAILearner:
    """Automatic AI Learning System"""
    
    def __init__(self, jarvis_panel=None):
        self.jarvis_panel = jarvis_panel
        self.is_running = False
        self.learning_thread = None
        self.learned_count = 0
        self.questions_asked = 0
        
        # Learning topics
        self.learning_topics = [
            # Programming
            "What is Python programming?",
            "What is JavaScript?",
            "What is machine learning?",
            "What is artificial intelligence?",
            "What is deep learning?",
            "What is neural network?",
            "What is data science?",
            "What is cloud computing?",
            "What is blockchain?",
            "What is cybersecurity?",
            
            # General Knowledge
            "What is the solar system?",
            "What is photosynthesis?",
            "What is gravity?",
            "What is electricity?",
            "What is the internet?",
            "What is climate change?",
            "What is renewable energy?",
            "What is quantum physics?",
            "What is DNA?",
            "What is evolution?",
            
            # Technology
            "What is 5G technology?",
            "What is IoT?",
            "What is virtual reality?",
            "What is augmented reality?",
            "What is robotics?",
            "What is nanotechnology?",
            "What is biotechnology?",
            "What is cryptocurrency?",
            "What is big data?",
            "What is edge computing?",
            
            # Science
            "What is the Big Bang theory?",
            "What is black hole?",
            "What is atom?",
            "What is molecule?",
            "What is chemical reaction?",
            "What is ecosystem?",
            "What is biodiversity?",
            "What is genetics?",
            "What is cell?",
            "What is virus?",
            
            # Mathematics
            "What is algebra?",
            "What is calculus?",
            "What is geometry?",
            "What is statistics?",
            "What is probability?",
            "What is trigonometry?",
            "What is matrix?",
            "What is algorithm?",
            "What is data structure?",
            "What is graph theory?",
        ]
        
        self.current_topic_index = 0
    
    def start(self):
        """Start auto-learning"""
        if self.is_running:
            print("⚠️ Auto-learning already running!")
            return False
        
        self.is_running = True
        self.learning_thread = threading.Thread(target=self._learning_loop, daemon=True)
        self.learning_thread.start()
        
        print("✅ Auto AI Learner started!")
        return True
    
    def stop(self):
        """Stop auto-learning"""
        self.is_running = False
        print("✅ Auto AI Learner stopped!")
        print(f"📊 Stats: {self.questions_asked} questions asked, {self.learned_count} responses learned")
        return True
    
    def _learning_loop(self):
        """Main learning loop"""
        print("🤖 Auto AI Learner: Starting learning loop...")
        
        while self.is_running:
            try:
                # Get next question
                question = self._get_next_question()
                
                print(f"\n🤖 Auto AI Learner: Asking - {question}")
                
                # Ask Gemini AI (through Direct AI Chat or World AI Chat)
                response = self._ask_ai(question)
                
                if response:
                    print(f"✅ Auto AI Learner: Got response ({len(response)} chars)")
                    
                    # Learn from response
                    self._learn_from_response(question, response)
                    
                    self.questions_asked += 1
                    self.learned_count += 1
                    
                    # Log to JARVIS panel
                    if self.jarvis_panel:
                        self.jarvis_panel.after(0, lambda: self.jarvis_panel.log(
                            "AUTO-LEARN",
                            f"📚 Learned: {question[:50]}... ({self.learned_count} total)"
                        ))
                else:
                    print(f"⚠️ Auto AI Learner: No response for - {question}")
                
                # Wait before next question (don't spam!)
                wait_time = random.randint(30, 60)  # 30-60 seconds
                print(f"⏳ Auto AI Learner: Waiting {wait_time}s before next question...")
                
                for _ in range(wait_time):
                    if not self.is_running:
                        break
                    time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ Auto AI Learner error: {e}")
                time.sleep(10)  # Wait before retry
        
        print("🤖 Auto AI Learner: Learning loop stopped")
    
    def _get_next_question(self):
        """Get next question to ask"""
        question = self.learning_topics[self.current_topic_index]
        self.current_topic_index = (self.current_topic_index + 1) % len(self.learning_topics)
        return question
    
    def _ask_ai(self, question):
        """Ask AI and get response"""
        try:
            # Try Direct AI Chat first (instant, no browser)
            if self.jarvis_panel and hasattr(self.jarvis_panel, 'direct_ai_chat'):
                result = self.jarvis_panel.direct_ai_chat.chat_with_ai(question, 'auto')
                if result['success']:
                    return result['response']
            
            # If Direct AI Chat fails, we can't use World AI Chat (requires user interaction)
            # So we'll use a simple fallback
            print("⚠️ Auto AI Learner: Direct AI Chat not available, skipping...")
            return None
            
        except Exception as e:
            print(f"⚠️ Auto AI Learner: Error asking AI - {e}")
            return None
    
    def _learn_from_response(self, question, response):
        """Learn from AI response"""
        try:
            # Save to knowledge base
            if self.jarvis_panel and hasattr(self.jarvis_panel, '_offline_brain_instance'):
                offline_brain = self.jarvis_panel._offline_brain_instance
                
                # Add to knowledge
                if hasattr(offline_brain, 'knowledge'):
                    # Extract key from question
                    key = question.lower().replace("what is ", "").replace("?", "").strip()
                    offline_brain.knowledge[key] = response[:500]  # Store first 500 chars
                    print(f"✅ Saved to knowledge: {key}")
                
                # Try to use learning systems
                if hasattr(offline_brain, 'auto_learner') and offline_brain.auto_learner:
                    try:
                        offline_brain.auto_learner.learn_text(response)
                        print(f"✅ Auto learner trained")
                    except Exception as e:

                        print(f"⚠️ Error: {e}")
                        pass
                
                if hasattr(offline_brain, 'ultimate_learner') and offline_brain.ultimate_learner:
                    try:
                        offline_brain.ultimate_learner.learn(response)
                        print(f"✅ Ultimate learner trained")
                    except Exception as e:

                        print(f"⚠️ Error: {e}")
                        pass
            
            return True
            
        except Exception as e:
            print(f"⚠️ Auto AI Learner: Error learning - {e}")
            return False
    
    def get_stats(self):
        """Get learning statistics"""
        return {
            'is_running': self.is_running,
            'questions_asked': self.questions_asked,
            'learned_count': self.learned_count,
            'current_topic': self.learning_topics[self.current_topic_index] if self.current_topic_index < len(self.learning_topics) else "N/A",
            'total_topics': len(self.learning_topics),
            'progress': f"{self.current_topic_index}/{len(self.learning_topics)}"
        }


# Test function
if __name__ == "__main__":
    print("="*70)
    print("🤖 AUTO AI LEARNER TEST")
    print("="*70)
    
    learner = AutoAILearner()
    
    print(f"\n✅ Auto AI Learner created!")
    print(f"📚 Learning topics: {len(learner.learning_topics)}")
    print(f"📊 Stats: {learner.get_stats()}")
    
    print("\n💡 To use:")
    print("   1. learner.start() - Start auto-learning")
    print("   2. learner.stop() - Stop auto-learning")
    print("   3. learner.get_stats() - Get statistics")
    
    print("\n" + "="*70)
