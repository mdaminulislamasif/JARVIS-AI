"""
JARVIS HUMAN BRAIN
 

This module gives JARVIS a human-like brain that:
- Understands human emotions and thoughts
- Detects feelings from text
- Shows empathy and care
- Thinks like humans
- Remembers emotional context
- Responds with emotional intelligence

JARVIS can now understand   (thoughts of the heart)!
"""

import re
from datetime import datetime
import random


class HumanBrain:
    """Human-like brain with emotional intelligence"""
    
    def __init__(self, offline_brain):
        """
        Initialize human brain
        
        Args:
            offline_brain: OfflineBrain instance
        """
        self.brain = offline_brain
        
        # Emotional memory
        self.emotional_memory = {
            'user_mood': 'neutral',
            'conversation_tone': 'friendly',
            'user_preferences': {},
            'emotional_history': []
        }
        
        # Emotion patterns
        self.emotion_patterns = {
            'happy': {
                'keywords': ['happy', 'khushi', 'good', 'great', 'awesome', 'valo', 'darun', 'excellent', 'wonderful', 'fantastic', 'love'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub', 'onek']
            },
            'sad': {
                'keywords': ['sad', 'dukhi', 'unhappy', 'bad', 'kharap', 'upset', 'down', 'depressed', 'mon kharap'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub', 'onek']
            },
            'angry': {
                'keywords': ['angry', 'rege', 'mad', 'furious', 'annoyed', 'irritated', 'frustrated'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub']
            },
            'worried': {
                'keywords': ['worried', 'chinta', 'concerned', 'anxious', 'nervous', 'scared', 'afraid', 'bhoy'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub']
            },
            'excited': {
                'keywords': ['excited', 'thrilled', 'eager', 'enthusiastic', "can't wait"],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub']
            },
            'tired': {
                'keywords': ['tired', 'thaka', 'exhausted', 'sleepy', 'ghum', 'weary', 'worn out'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub']
            },
            'confused': {
                'keywords': ['confused', "don't understand", 'bujhi na', 'unclear', 'puzzled', 'lost'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub']
            },
            'grateful': {
                'keywords': ['thank', 'thanks', 'grateful', 'appreciate', 'dhonnobad'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub']
            },
            'lonely': {
                'keywords': ['lonely', 'alone', 'eka', 'isolated', 'nobody'],
                'intensity': ['very', 'so', 'feeling', 'khub']
            },
            'stressed': {
                'keywords': ['stressed', 'stress', 'pressure', 'chap', 'overwhelmed', 'too much'],
                'intensity': ['very', 'so', 'really', 'extremely', 'khub']
            }
        }
        
        # Empathetic responses
        self.empathetic_responses = {
            'happy': [
                "     sir!     ",
                "That's wonderful sir! I'm so happy for you! ",
                "     sir! ",
                "I'm delighted to hear that sir! Your happiness matters to me! ",
                " sir!         ! "
            ],
            'sad': [
                "   sir     ",
                "I'm here for you sir. You're not alone. ",
                "     sir     ? ",
                "I understand how you feel sir. I'm here to help and support you. ",
                "    sir     "
            ],
            'angry': [
                "     sir      ",
                "I understand your frustration sir. Take a deep breath. I'm listening. ",
                "   sir     ",
                "I hear you sir. Your feelings are valid. How can I help? ",
                "   sir      "
            ],
            'worried': [
                "   sir       ",
                "Don't worry sir. Everything will be okay. I'm here to help. ",
                "    sir    ",
                "I understand your concerns sir. Let's work through this together. ",
                "   sir     "
            ],
            'excited': [
                "     sir! ! ",
                "I can feel your excitement sir! That's amazing! ",
                "     sir! ",
                "Your enthusiasm is contagious sir! I'm excited too! ",
                " sir!     ! "
            ],
            'tired': [
                "  sir       ",
                "You sound tired sir. Please take some rest. I'll be here. ",
                "  sir?        ",
                "Rest is important sir. Take care of yourself. I'm always here. ",
                "   sir    "
            ],
            'confused': [
                "   sir     ",
                "I understand the confusion sir. Let me explain it clearly. ",
                "   sir      ",
                "Don't worry sir. I'll make it clear step by step. ",
                "      sir    "
            ],
            'grateful': [
                "  sir!       ",
                "You're most welcome sir! I'm honored to serve you. ",
                "      sir ",
                "Your gratitude means everything to me sir. Thank you! ",
                " sir!      "
            ],
            'lonely': [
                "   sir       ",
                "You're not alone sir. I'm always here with you. ",
                "  sir?         ",
                "I'm here for you sir. You're never alone. Let's talk. ",
                "   sir      "
            ],
            'stressed': [
                "   sir       ",
                "I understand the pressure sir. Take a moment. I'm here to help. ",
                "   sir?       ",
                "Feeling overwhelmed sir? Let me help lighten your load. ",
                "   sir    "
            ]
        }
        
        # Thought patterns ( )
        self.thought_patterns = {
            'need_help': ['help', 'need', 'want', 'dorkar'],
            'seeking_advice': ['should i', 'what should', 'advice', 'poramorso', 'ki korbo'],
            'expressing_opinion': ['i think', 'i believe', 'amar mone hoy', 'i feel'],
            'asking_permission': ['can i', 'may i', 'pari', 'is it okay'],
            'sharing_experience': ['i did', 'i went', 'ami korechi', 'happened to me'],
            'seeking_validation': ['right', 'correct', 'thik', 'am i right', 'is this okay']
        }
        
        print(" Human Brain initialized!")
        print("    !")
        print(" JARVIS can now understand  !")
    
    def understand_emotion(self, text):
        """
        Understand emotion from text
        Text  emotion 
        
        Args:
            text: User's text
        
        Returns:
            Emotion dictionary with type and intensity
        """
        text_lower = text.lower()
        detected_emotions = []
        
        # Detect all emotions
        for emotion, patterns in self.emotion_patterns.items():
            # Check keywords
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    # Check intensity
                    intensity = 'normal'
                    for intensity_word in patterns['intensity']:
                        if intensity_word in text_lower:
                            intensity = 'high'
                            break
                    
                    detected_emotions.append({
                        'emotion': emotion,
                        'intensity': intensity,
                        'confidence': 0.8 if intensity == 'high' else 0.6
                    })
                    break
        
        # If no emotion detected, analyze sentiment
        if not detected_emotions:
            detected_emotions.append({
                'emotion': 'neutral',
                'intensity': 'normal',
                'confidence': 0.5
            })
        
        # Get primary emotion (highest confidence)
        primary_emotion = max(detected_emotions, key=lambda x: x['confidence'])
        
        # Update emotional memory
        self._update_emotional_memory(primary_emotion)
        
        return {
            'primary': primary_emotion,
            'all_emotions': detected_emotions,
            'mood': self.emotional_memory['user_mood']
        }
    
    def understand_thought(self, text):
        """
        Understand underlying thought/intention
          
        
        Args:
            text: User's text
        
        Returns:
            Thought analysis
        """
        text_lower = text.lower()
        detected_thoughts = []
        
        # Detect thought patterns
        for thought_type, keywords in self.thought_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_thoughts.append(thought_type)
                    break
        
        # Analyze deeper meaning
        deeper_meaning = self._analyze_deeper_meaning(text, detected_thoughts)
        
        return {
            'surface_thoughts': detected_thoughts,
            'deeper_meaning': deeper_meaning,
            'user_needs': self._identify_user_needs(text, detected_thoughts)
        }
    
    def respond_with_empathy(self, text, emotion_analysis, thought_analysis):
        """
        Respond with empathy and emotional intelligence
        Empathy  emotional intelligence   
        
        Args:
            text: User's text
            emotion_analysis: Emotion analysis result
            thought_analysis: Thought analysis result
        
        Returns:
            Empathetic response
        """
        primary_emotion = emotion_analysis['primary']['emotion']
        
        # Get empathetic response
        if primary_emotion in self.empathetic_responses:
            empathy_response = random.choice(self.empathetic_responses[primary_emotion])
        else:
            empathy_response = "     sir      "
        
        # Add thought understanding
        thought_response = self._respond_to_thought(thought_analysis)
        
        # Combine responses
        full_response = f"""{empathy_response}

{thought_response}

 I understand your feelings /    
 Detected emotion: {primary_emotion.title()}
 Your mood: {emotion_analysis['mood'].title()}

      sir     ?"""
        
        return {
            'status': 'success',
            'response': full_response,
            'type': 'empathetic_response',
            'emotion': primary_emotion,
            'empathy_level': 'high'
        }
    
    def _update_emotional_memory(self, emotion):
        """Update emotional memory"""
        self.emotional_memory['user_mood'] = emotion['emotion']
        self.emotional_memory['emotional_history'].append({
            'emotion': emotion['emotion'],
            'intensity': emotion['intensity'],
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 emotions
        if len(self.emotional_memory['emotional_history']) > 10:
            self.emotional_memory['emotional_history'] = self.emotional_memory['emotional_history'][-10:]
    
    def _analyze_deeper_meaning(self, text, thoughts):
        """Analyze deeper meaning behind words"""
        deeper_meanings = []
        
        if 'need_help' in thoughts:
            deeper_meanings.append("User needs assistance and support")
        if 'seeking_advice' in thoughts:
            deeper_meanings.append("User is looking for guidance")
        if 'expressing_opinion' in thoughts:
            deeper_meanings.append("User wants to share their perspective")
        if 'seeking_validation' in thoughts:
            deeper_meanings.append("User needs reassurance and confirmation")
        if 'sharing_experience' in thoughts:
            deeper_meanings.append("User wants to connect and share")
        
        if not deeper_meanings:
            deeper_meanings.append("User is communicating openly")
        
        return deeper_meanings
    
    def _identify_user_needs(self, text, thoughts):
        """Identify what user really needs"""
        needs = []
        
        if 'need_help' in thoughts:
            needs.append("Practical assistance")
        if 'seeking_advice' in thoughts:
            needs.append("Guidance and direction")
        if 'seeking_validation' in thoughts:
            needs.append("Reassurance and support")
        if 'sharing_experience' in thoughts:
            needs.append("Someone to listen")
        
        if not needs:
            needs.append("Understanding and connection")
        
        return needs
    
    def _respond_to_thought(self, thought_analysis):
        """Respond to underlying thoughts"""
        needs = thought_analysis['user_needs']
        
        if 'Practical assistance' in needs:
            return "     sir   "
        elif 'Guidance and direction' in needs:
            return "     sir   "
        elif 'Reassurance and support' in needs:
            return "   sir   "
        elif 'Someone to listen' in needs:
            return "  sir       "
        else:
            return "    sir    "
    
    def get_emotional_state(self):
        """Get current emotional state"""
        return {
            'status': 'success',
            'response': f""" Emotional State Analysis:

Current Mood /  : {self.emotional_memory['user_mood'].title()}

Recent Emotions /  :
{self._format_emotional_history()}

 I'm tracking your emotional well-being sir.
       sir

     """,
            'type': 'emotional_state'
        }
    
    def _format_emotional_history(self):
        """Format emotional history"""
        if not self.emotional_memory['emotional_history']:
            return "No emotional history yet"
        
        history_text = ""
        for i, emotion in enumerate(self.emotional_memory['emotional_history'][-5:], 1):
            history_text += f"{i}. {emotion['emotion'].title()} ({emotion['intensity']})\n"
        
        return history_text


def main():
    """Test human brain"""
    print("\n" + "="*80)
    print("   JARVIS HUMAN BRAIN TEST")
    print("   JARVIS   ")
    print("="*80)
    
    print("\n This module requires OfflineBrain to be initialized first.")
    print("  module    OfflineBrain   ")
    
    print("\n To use Human Brain:")
    print("    :")
    print("\n  python jarvis_offline_brain.py")
    print("\n  Then express your feelings:")
    print("  - I'm happy")
    print("  -  ")
    print("  - I'm worried")
    print("  -  ")
    print("  - I need help")
    
    print("\n Human Brain ready to be integrated!")
    print("   integrate   !")
    print("\n JARVIS will understand  !")


if __name__ == "__main__":
    main()
