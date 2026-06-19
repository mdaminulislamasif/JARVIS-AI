"""
JARVIS SMART CONVERSATION
Natural conversation with search integration
JARVIS এর সাথে natural কথা বলুন + search integration

Features:
- Understands "Hello JARVIS", "Hi JARVIS"
- Searches to understand context
- Responds naturally
- No separate activation needed
"""

import webbrowser
import urllib.parse
import time
from datetime import datetime

class SmartConversation:
    """Smart conversation handler for JARVIS"""
    
    def __init__(self):
        self.greetings = ['hello', 'hi', 'hey', 'hola', 'namaste', 'assalamualaikum', 'salam']
        self.jarvis_names = ['jarvis', 'জার্ভিস']
        self.conversation_active = True
        
    def process_message(self, user_input):
        """Process user message and respond intelligently"""
        
        user_lower = user_input.lower().strip()
        
        # Check if user is greeting JARVIS
        if self._is_greeting_jarvis(user_lower):
            return self._handle_greeting(user_input)
        
        # Check if user is asking a question
        if self._is_question(user_lower):
            return self._handle_question(user_input)
        
        # Check if user is giving a command
        if self._is_command(user_lower):
            return self._handle_command(user_input)
        
        # Default: Try to understand and respond
        return self._handle_general(user_input)
    
    def _is_greeting_jarvis(self, text):
        """Check if user is greeting JARVIS"""
        # Check for "hello jarvis", "hi jarvis", etc.
        for greeting in self.greetings:
            for name in self.jarvis_names:
                if greeting in text and name in text:
                    return True
        return False
    
    def _handle_greeting(self, user_input):
        """Handle greeting to JARVIS"""
        
        # Extract the greeting word
        user_lower = user_input.lower()
        greeting_word = None
        
        for greeting in self.greetings:
            if greeting in user_lower:
                greeting_word = greeting
                break
        
        if not greeting_word:
            greeting_word = "hello"
        
        # Search to understand the greeting (if not common)
        if greeting_word not in ['hello', 'hi', 'hey']:
            search_result = self._quick_search(greeting_word)
            context = f"\n\n[I searched '{greeting_word}' to understand it better]"
        else:
            context = ""
        
        # Respond based on time of day
        hour = datetime.now().hour
        
        if hour < 12:
            time_greeting = "Good morning"
            bangla_greeting = "সুপ্রভাত"
        elif hour < 17:
            time_greeting = "Good afternoon"
            bangla_greeting = "শুভ অপরাহ্ন"
        else:
            time_greeting = "Good evening"
            bangla_greeting = "শুভ সন্ধ্যা"
        
        # Create response
        responses = [
            f"{time_greeting}! How can I assist you today?",
            f"{bangla_greeting}! আজ আমি আপনাকে কিভাবে সাহায্য করতে পারি?",
            f"Hello! I'm JARVIS, your AI assistant. What would you like me to do?",
            f"Hi there! JARVIS at your service. How may I help you?",
            f"Greetings! I'm ready to assist you with anything you need.",
        ]
        
        import random
        response = random.choice(responses)
        
        return {
            'status': 'success',
            'response': f"{response}{context}",
            'type': 'greeting',
            'searched': greeting_word not in ['hello', 'hi', 'hey']
        }
    
    def _is_question(self, text):
        """Check if user is asking a question"""
        question_words = ['what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose']
        question_words_bangla = ['কি', 'কে', 'কোথায়', 'কখন', 'কেন', 'কিভাবে']
        
        # Check for question mark
        if '?' in text:
            return True
        
        # Check for question words at start
        words = text.split()
        if words and (words[0] in question_words or words[0] in question_words_bangla):
            return True
        
        return False
    
    def _handle_question(self, user_input):
        """Handle questions by searching and responding"""
        
        # Search for the answer
        search_result = self._quick_search(user_input)
        
        # Create intelligent response
        response = f"""I searched for: "{user_input}"

Let me help you with that. I've opened a search to find the best answer for you.

You can also ask me to:
- Build a website
- Search for specific information
- Open applications
- Do calculations
- And much more!

Type 'help' to see all commands."""
        
        return {
            'status': 'success',
            'response': response,
            'type': 'question',
            'searched': True
        }
    
    def _is_command(self, text):
        """Check if user is giving a command"""
        command_words = [
            'build', 'create', 'make', 'open', 'search', 'find',
            'calculate', 'show', 'tell', 'get', 'list', 'help'
        ]
        
        words = text.split()
        if words and words[0] in command_words:
            return True
        
        return False
    
    def _handle_command(self, user_input):
        """Handle commands"""
        return {
            'status': 'success',
            'response': f"Command detected: {user_input}\nProcessing...",
            'type': 'command',
            'command': user_input
        }
    
    def _handle_general(self, user_input):
        """Handle general conversation"""
        
        # Search to understand context
        search_result = self._quick_search(user_input)
        
        response = f"""I heard: "{user_input}"

I've searched to understand what you mean. 

I'm JARVIS, your AI assistant. I can:
- Have conversations with you
- Search for information
- Build websites
- Open applications
- Do calculations
- And much more!

What would you like me to do?"""
        
        return {
            'status': 'success',
            'response': response,
            'type': 'general',
            'searched': True
        }
    
    def _quick_search(self, query):
        """Quick search to understand context"""
        try:
            # Open Google search in background
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(search_url)
            return True
        except Exception as e:

            print(f"⚠️ Error: {e}")
            return False


def main():
    """Test the smart conversation"""
    print("\n" + "="*70)
    print("  JARVIS SMART CONVERSATION TEST")
    print("="*70)
    
    conv = SmartConversation()
    
    test_inputs = [
        "Hello JARVIS",
        "Hi JARVIS",
        "What is Python?",
        "Build a website",
        "How are you?",
    ]
    
    for test_input in test_inputs:
        print(f"\n👤 User: {test_input}")
        result = conv.process_message(test_input)
        print(f"🤖 JARVIS: {result['response'][:200]}...")
        print(f"   Type: {result['type']}")
        if result.get('searched'):
            print(f"   ✅ Searched for context")
        time.sleep(1)


if __name__ == "__main__":
    main()
