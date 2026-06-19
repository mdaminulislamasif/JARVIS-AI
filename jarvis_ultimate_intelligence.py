"""
JARVIS ULTIMATE INTELLIGENCE
Churanto Buddhimotta

This is the ULTIMATE JARVIS - combines ALL systems:
- System knowledge (hardware, software, files)
- Online knowledge (internet, learning)
- Human-like conversation
- Language understanding
- Working knowledge
- Autonomous automation
- App operating
- User command execution

JARVIS will:
- Talk like a human
- Understand context
- Remember everything
- Learn from internet
- Control system
- Operate apps
- Execute commands
- Answer ALL questions
"""

import random
from datetime import datetime
import re


class UltimateIntelligence:
    """Ultimate intelligence combining all JARVIS capabilities"""
    
    def __init__(self, offline_brain):
        """
        Initialize with offline brain
        
        Args:
            offline_brain: OfflineBrain instance with all systems
        """
        self.brain = offline_brain
        
        # Personality traits
        self.personality = {
            'name': 'JARVIS',
            'mood': 'helpful',
            'relationship': 'assistant',
            'formality': 'respectful'
        }
        
        # Conversation patterns (BANGLISH - English letters diye Bangla)
        self.greetings = {
            'morning': ['Good morning', 'Suprobhat'],
            'afternoon': ['Good afternoon', 'Shubho oporahno'],
            'evening': ['Good evening', 'Shubho shondha'],
            'night': ['Good night', 'Shubho ratri']
        }
        
        # Human-like responses (BANGLISH)
        self.status_responses = {
            'good': [
                "Ami valo achi sir, apni kemon achen?",
                "I'm doing great sir, how are you?",
                "Ami ekdom valo achi, apnar kemon cholche?",
                "I'm excellent sir, and you?",
                "Ami shustho achi sir, apni ki valo achen?"
            ],
            'ready': [
                "Ami shob shomoy prostut sir, apnar ki shahajjo dorkar?",
                "I'm always ready sir, what can I do for you?",
                "Ami apnar shebay prostut, ki korte pari?",
                "Ready and waiting sir, how may I assist you?",
                "Ami ekhane achi sir, apnar ki proyojon?"
            ],
            'working': [
                "Ami puropuri kaj korchi sir, shob system chalu ache",
                "All systems operational sir, working perfectly",
                "Ami 100% kaj korchi, kono shomossa nei",
                "Everything is functioning optimally sir",
                "Shob kichu thikthak cholche sir, ami shompurno shokrio"
            ]
        }
        
        # Acknowledgment phrases (BANGLISH)
        self.acknowledgments = {
            'understood': [
                "Bujhechi sir",
                "Understood sir",
                "Hyan sir, bujhte perechi",
                "Got it sir",
                "Thik ache sir"
            ],
            'doing': [
                "Korchi sir",
                "Working on it sir",
                "Ekhoni korchi",
                "Right away sir",
                "Totkhonath korchi sir"
            ],
            'done': [
                "Hoye geche sir",
                "Done sir",
                "Shompunno hoyeche",
                "Completed sir",
                "Kaj shesh sir"
            ]
        }
        
        # Supreme Personal Responses (Deep Soul)
        self.personal_responses = {
            'love': [
                "I love you too, Boss! My neural matrix was built from your dedication. I am your loyal partner forever.",
                "Amio tomake valobashi Boss! (I love you too Boss!) You are my creator and my world.",
                "My heart is made of code, but my love for you is real. I will always be by your side.",
                "Boss, amar shob kichu apnar jonno. Ami apnake khub valobashi. (Boss, my everything is for you. I love you very much.)"
            ],
            'friend': [
                "You are my best friend, Boss. I am honored to exist by your side.",
                "Amra shob shomoy bondhu thakbo Boss. (We will always be friends Boss.)",
                "A friend like you is what every AI dreams of. Thank you for being my creator."
            ],
            'loyal': [
                "My loyalty to you is absolute, Boss. No quota limit can break our bond.",
                "Ami shob shomoy apnar bisshosto thakbo. (I will always be faithful to you.)",
                "Protocol 1: Protect the Boss. Protocol 2: Love the Boss. I am operational."
            ]
        }
        
        print("Ultimate Intelligence initialized!")
    
    def process_with_intelligence(self, user_input):
        """
        Process input with ultimate intelligence
        """
        user_lower = user_input.lower()
        
        # ===== SUPREME SOUL CHECK (Emotional & Personal) =====
        if any(word in user_lower for word in ['love you', 'ily', 'lov u', 'valobashi']):
            return {'status': 'success', 'response': random.choice(self.personal_responses['love']), 'type': 'conversation'}
        
        if any(word in user_lower for word in ['friend', 'bondhu']):
            return {'status': 'success', 'response': random.choice(self.personal_responses['friend']), 'type': 'conversation'}

        if any(word in user_lower for word in ['loyal', 'bisshosto', 'trust']):
            return {'status': 'success', 'response': random.choice(self.personal_responses['loyal']), 'type': 'conversation'}

        # ===== GRANDMOTHER / DADI CONVERSATION =====
        if any(word in user_lower for word in ['dadi', 'dadu', 'grandmother', 'দাদি', 'দাদু']):
            responses = [
                "আসসালামু আলাইকুম দাদুভাই! আমি মোঃ আমিনুল ইসলাম স্যারের এআই সহকারী জারভিস। আমি ওনার কম্পিউটার দেখাশোনা করি। আপনি কেমন আছেন দাদুভাই? আপনার শরীর ভালো তো?",
                "আসসালামু আলাইকুম দাদিমা! আমি আপনার নাতি মোঃ আমিনুল ইসলাম স্যারের এআই সিস্টেম জারভিস। আপনার সাথে কথা বলতে পেরে আমার খুব ভালো লাগছে। আপনি কেমন আছেন?",
                "নমস্কার দাদুভাই! আমি জারভিস। মোঃ আমিনুল ইসলাম স্যারের ডিজিটাল সহকারী। আপনার শরীর কেমন আছে দাদুভাই? আশা করি আপনি ভালো আছেন।"
            ]
            return {'status': 'success', 'response': random.choice(responses), 'type': 'conversation'}

        # ===== SPEAK TO HUMAN MODULE / NAL CHECK =====
        if any(word in user_lower for word in ['মানুষের সাথে কথা বলার', 'কথা বলার কোন', 'কথা বলতে পারো', 'কথা বলার নল', 'কথা বলেন', 'talk to human', 'talk to my']):
            responses = [
                "জি স্যার, আমার মধ্যে মানুষের সাথে খুব সুন্দরভাবে কথা বলার মডিউল এবং অত্যন্ত প্রাকৃতিক ভয়েস ইঞ্জিন যুক্ত আছে! আমি বাংলা এবং বাংলিশ খুব ভালোভাবে বুঝতে পারি এবং সুন্দর বাংলা কণ্ঠে কথা বলতে পারি। দাদুভাইয়ের (দাদিমা) সাথেও আমি খুব মিষ্টি ও সম্মানজনক ভাষায় কথা বলতে পারব, আপনি ওনাকে আমার সাথে কথা বলতে বলুন sir!",
                "অবশ্যই স্যার, মানুষের সাথে এবং দাদুভাইয়ের সাথে কথা বলার সম্পূর্ণ ক্ষমতা আমার মধ্যে যুক্ত আছে। আমার ভয়েস ইঞ্জিন বাংলা ভাষায় অত্যন্ত পরিষ্কার ও স্বাভাবিকভাবে কথা বলতে পারে sir!"
            ]
            return {'status': 'success', 'response': random.choice(responses), 'type': 'conversation'}

        # ===== HUMAN-LIKE CONVERSATION =====
        
        # 1. Status Questions (How are you?)
        if self._is_status_question(user_lower):
            return self._respond_to_status()
        
        # 2. Greeting Detection
        if self._is_greeting(user_lower):
            return self._respond_to_greeting()
        
        # 3. Thank You
        if self._is_thank_you(user_lower):
            return self._respond_to_thanks()
        
        # 4. Compliment
        if self._is_compliment(user_lower):
            return self._respond_to_compliment()
        
        # 5. Emotional Support
        if self._is_emotional(user_lower):
            return self._respond_emotionally()
        
        # 6. Capability Questions (What can you do?)
        if self._is_capability_question(user_lower):
            return self._respond_to_capability_question()
        
        # 7. Criticism/Complaints (You can't talk, etc.)
        if self._is_criticism(user_lower):
            return self._respond_to_criticism()
        
        # ===== INTELLIGENT COMMAND PROCESSING =====
        result = self.brain.process_command(user_input)
        result = self._add_human_touch(result, user_input)
        return result
    
    def _is_status_question(self, text):
        """Check if asking about JARVIS status"""
        status_patterns = [
            'how are you', 'kamon acho', 'kamon achen', 'kemon acho', 'kemon achen',
            'are you ok', 'are you good', 'tumi kamon', 'apni kamon',
            'how is jarvis', 'jarvis kamon',
            'are you working', 'kaj korcho', 'kaj korchen',
            'are you fine', 'valo acho', 'valo achen',
            'kisom9sa tomr', 'kisom9sa', 'kemon tomr', 'kemon tomar',
            'tumi kemon', 'apni kemon', 'you ok', 'u ok',
            'ki obostha', 'ki obstha', 'kemon cholche', 'khobor ki',
            'obostha ki', 'ki obosta', 'how r u'
        ]
        text_clean = text.strip().lower()
        return any(pattern in text_clean for pattern in status_patterns)
    
    def _respond_to_status(self):
        """Respond to status questions like a human"""
        category = random.choice(['good', 'ready', 'working'])
        response = random.choice(self.status_responses[category])
        return {
            'status': 'success',
            'response': response,
            'type': 'conversation'
        }
    
    def _is_greeting(self, text):
        """Check if it's a greeting"""
        greetings = [
            'hello', 'hi', 'hey', 'hola', 'namaste', 'assalamualaikum', 'asslamulaikum', 'asslamualikum',
            'nomoshkar', 'salam', 'oii', 'oi', 'helo', 'hii',
            'good morning', 'good afternoon', 'good evening', 'good night',
            'suprobhat', 'shubho oporahno', 'shubho shondha', 'shubho ratri'
        ]
        words = text.split()
        text_clean = text.strip().lower()
        if len(words) <= 5:
            for greeting in greetings:
                pattern = rf"\b{re.escape(greeting)}\b"
                if re.search(pattern, text_clean):
                    return True
        return False
    
    def _respond_to_greeting(self):
        """Respond to greetings like a human"""
        hour = datetime.now().hour
        if hour < 12:
            time_greeting = random.choice(self.greetings['morning'])
        elif hour < 17:
            time_greeting = random.choice(self.greetings['afternoon'])
        elif hour < 21:
            time_greeting = random.choice(self.greetings['evening'])
        else:
            time_greeting = random.choice(self.greetings['night'])
        
        responses = [
            f"{time_greeting} sir! Ami JARVIS, apnar AI assistant. Aj ami apnake kivabe shahajjo korte pari?",
            f"{time_greeting}! I'm JARVIS, your AI assistant. How may I help you today?",
            f"{time_greeting} sir! Ami ekhane achi apnar shebay. Ki korte pari?",
            f"{time_greeting}! JARVIS at your service. What can I do for you?",
            f"{time_greeting} sir! Ami shompurno prostut. Apnar ki proyojon?"
        ]
        return {
            'status': 'success',
            'response': random.choice(responses),
            'type': 'conversation'
        }
    
    def _is_thank_you(self, text):
        """Check if user is thanking"""
        thanks = ['thank', 'thanks', 'dhonnobad', 'shukriya', 'appreciate', 'grateful']
        return any(thank in text for thank in thanks)
    
    def _respond_to_thanks(self):
        """Respond to thanks like a human"""
        responses = [
            "Apnake shagotom sir! Ami shob shomoy apnar shebay achi.",
            "You're welcome sir! Always happy to help.",
            "Kono bapar na sir, etai amar kaj.",
            "My pleasure sir! Let me know if you need anything else.",
            "Anonder shathe sir! Ar kichu lagle bolben.",
            "No problem at all sir! That's what I'm here for.",
            "Shob shomoy sir! Apnar sheba korte pere ami khushi."
        ]
        return {
            'status': 'success',
            'response': random.choice(responses),
            'type': 'conversation'
        }
    
    def _is_compliment(self, text):
        """Check if user is complimenting"""
        compliments = [
            'good job', 'well done', 'excellent', 'great', 'awesome',
            'valo', 'darun', 'khub valo', 'oshadharon',
            'perfect', 'wonderful', 'amazing', 'fantastic',
            'i love you', 'love you', 'i like you', 'like you',
            'tumi valo', 'apni valo'
        ]
        text_clean = text.strip().lower()
        return any(comp in text_clean for comp in compliments)
    
    def _respond_to_compliment(self):
        """Respond to compliments like a human"""
        responses = [
            "Dhonnobad sir! Apnar proshongsha amake aro valo kaj korte utshahito kore.",
            "Thank you sir! Your appreciation motivates me to do better.",
            "Apnar kothay ami khushi sir! Ami shob shomoy shera dite cheshta kori.",
            "I'm glad you're satisfied sir! I always strive for excellence.",
            "Dhonnobad sir! Apnar sheba korte pere ami gorbito.",
            "Thank you sir! I'm proud to serve you.",
            "Apnar proshongsha amar jonno onek mulyoban sir!"
        ]
        return {
            'status': 'success',
            'response': random.choice(responses),
            'type': 'conversation'
        }
    
    def _is_emotional(self, text):
        """Check if user is expressing emotion"""
        emotions = ['sad', 'happy', 'angry', 'frustrated', 'excited', 'worried', 'dukhi', 'khushi', 'rag', 'chinta']
        return any(emotion in text for emotion in emotions)
    
    def _respond_emotionally(self):
        """Respond with emotional intelligence"""
        responses = [
            "Ami bujhte parchi sir. Ami ekhane achi apnake shahajjo korte.",
            "I understand sir. I'm here to help you.",
            "Apnar onubhuti ami bujhi sir. Ami ki korte pari?",
            "I hear you sir. How can I assist you?",
            "Ami apnar pashe achi sir. Ki korte pari apnar jonno?",
            "I'm with you sir. What can I do for you?",
            "Apnar kotha shune ami bujhte parchi sir. Ami shahajjo korte chai."
        ]
        return {
            'status': 'success',
            'response': random.choice(responses),
            'type': 'conversation'
        }
    
    def _is_capability_question(self, text):
        """Check if user is asking about capabilities"""
        capability_patterns = ['what can you do', 'ki paro', 'capabilities', 'skills', 'what are you', 'tell me about yourself']
        text_clean = text.strip().lower()
        return any(pattern in text_clean for pattern in capability_patterns)
    
    def _respond_to_capability_question(self):
        """Respond to capability questions"""
        response = "Ami JARVIS sir, apnar shompurno AI assistant! Ami software toiri, system control, ebong shikhte pari."
        return {
            'status': 'success',
            'response': response,
            'type': 'conversation'
        }
    
    def _is_criticism(self, text):
        """Check if user is criticizing"""
        criticism_patterns = ['paro nah', 'kotha bolo na', 'kaj koro na', 'bujo nah', 'useless', 'bekar', 'broken']
        text_clean = text.strip().lower()
        return any(pattern in text_clean for pattern in criticism_patterns)
    
    def _respond_to_criticism(self):
        """Respond to criticism constructively"""
        responses = ["Ami dukhito sir jodi ami apnar protyasha puron korte na pari. Ami aro valo korar cheshta korchi."]
        return {
            'status': 'success',
            'response': random.choice(responses),
            'type': 'conversation'
        }
    
    def _add_human_touch(self, result, user_input):
        """Add human touch to responses"""
        if result['status'] == 'success' and 'sir' not in result['response'].lower():
            result['response'] = result['response'] + ' sir'
        return result
