"""
JARVIS OFFLINE BRAIN
Works WITHOUT API keys - No quota limits!

This brain can:
- Execute commands locally
- Do calculations
- Open applications
- Manage files
- Answer questions using built-in knowledge
- And much more - all WITHOUT API keys!
"""

import os
import sys

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import subprocess
import webbrowser
import sqlite3

# Mock webbrowser.open in test/diagnostic environment to prevent browser popups
if os.environ.get('JARVIS_NO_DIAGNOSIS') == '1' or os.environ.get('JARVIS_TESTING') == '1':
    webbrowser.open = lambda url, *args, **kwargs: True
    webbrowser.open_new = lambda url, *args, **kwargs: True
    webbrowser.open_new_tab = lambda url, *args, **kwargs: True
import json
import re
from datetime import datetime
import platform

# Import SuperBrain for advanced capabilities
try:
    from jarvis_super_brain import SuperBrain
    SUPER_BRAIN_AVAILABLE = True
except ImportError:
    SUPER_BRAIN_AVAILABLE = False
    print("⚠️ SuperBrain not available")

# Import Autonomous System for ultimate power
try:
    from jarvis_autonomous_system import AutonomousSystem
    AUTONOMOUS_AVAILABLE = True
except ImportError:
    AUTONOMOUS_AVAILABLE = False
    print("⚠️ Autonomous System not available")

# Import Internet Learner for learning from web
try:
    from jarvis_internet_learner import InternetLearner
    INTERNET_LEARNER_AVAILABLE = True
except ImportError:
    INTERNET_LEARNER_AVAILABLE = False
    print("⚠️ Internet Learner not available")

# Import Ultimate Learner for Chrome + Google learning
try:
    from jarvis_ultimate_learner import UltimateLearner
    ULTIMATE_LEARNER_AVAILABLE = True
except ImportError:
    ULTIMATE_LEARNER_AVAILABLE = False
    print("⚠️ Ultimate Learner not available")

# Import Auto Learner for word-by-word learning
try:
    from jarvis_auto_learner import AutoLearner
    AUTO_LEARNER_AVAILABLE = True
except ImportError:
    AUTO_LEARNER_AVAILABLE = False
    print("⚠️ Auto Learner not available")

# Import Infinite Tab Learner for infinite deep web crawling
try:
    from jarvis_infinite_tab_learner import InfiniteTabLearner
    INFINITE_TAB_LEARNER_AVAILABLE = True
except ImportError:
    INFINITE_TAB_LEARNER_AVAILABLE = False
    print("⚠️ Infinite Tab Learner not available")

# Import Chrome DevTools for advanced automation
try:
    from jarvis_chrome_devtools import ChromeDevTools
    CHROME_DEVTOOLS_AVAILABLE = True
except ImportError:
    CHROME_DEVTOOLS_AVAILABLE = False
    print("⚠️ Chrome DevTools not available")

# Import Chat History for conversation tracking
try:
    from jarvis_chat_history import ChatHistory
    CHAT_HISTORY_AVAILABLE = True
except ImportError:
    CHAT_HISTORY_AVAILABLE = False
    print("⚠️ Chat History not available")

# Import Smart Suggestions for command suggestions
try:
    from jarvis_smart_suggestions import SmartSuggestions
    SMART_SUGGESTIONS_AVAILABLE = True
except ImportError:
    SMART_SUGGESTIONS_AVAILABLE = False
    print("⚠️ Smart Suggestions not available")

# Import System Analyzer for system information
try:
    from jarvis_system_analyzer import SystemAnalyzer
    SYSTEM_ANALYZER_AVAILABLE = True
except ImportError:
    SYSTEM_ANALYZER_AVAILABLE = False
    print("⚠️ System Analyzer not available")

# Import Ultimate Intelligence for human-like interaction
try:
    from jarvis_ultimate_intelligence import UltimateIntelligence
    ULTIMATE_INTELLIGENCE_AVAILABLE = True
except ImportError:
    ULTIMATE_INTELLIGENCE_AVAILABLE = False
    print("⚠️ Ultimate Intelligence not available")

# Import Unified Auto Learner for background learning
try:
    from jarvis_unified_auto_learner import UnifiedAutoLearner
    UNIFIED_AUTO_LEARNER_AVAILABLE = True
except ImportError:
    UNIFIED_AUTO_LEARNER_AVAILABLE = False
    print("⚠️ Unified Auto Learner not available")

# Import Intelligent Answer Engine for AI-like answering
try:
    from jarvis_intelligent_answer_engine import IntelligentAnswerEngine
    INTELLIGENT_ANSWER_ENGINE_AVAILABLE = True
except ImportError:
    INTELLIGENT_ANSWER_ENGINE_AVAILABLE = False
    print("⚠️ Intelligent Answer Engine not available")

# Import Self-Healing System for automatic problem fixing
try:
    from jarvis_self_healing import SelfHealingSystem
    SELF_HEALING_AVAILABLE = True
except ImportError:
    SELF_HEALING_AVAILABLE = False
    print("⚠️ Self-Healing System not available")

# Import Self-Improvement System for future improvements
try:
    from jarvis_self_improvement import SelfImprovementSystem
    SELF_IMPROVEMENT_AVAILABLE = True
except ImportError:
    SELF_IMPROVEMENT_AVAILABLE = False
    print("⚠️ Self-Improvement System not available")

# Import Self-Builder System for building its own future
try:
    from jarvis_self_builder import SelfBuilder
    SELF_BUILDER_AVAILABLE = True
except ImportError:
    SELF_BUILDER_AVAILABLE = False
    print("⚠️ Self-Builder System not available")

# Import Information Gatherer for web scraping
try:
    from jarvis_info_gatherer import InfoGatherer
    INFO_GATHERER_AVAILABLE = True
except ImportError:
    INFO_GATHERER_AVAILABLE = False
    print("⚠️ Information Gatherer not available")

# Import Bangla Vocabulary for Bengali language support
try:
    from jarvis_bangla_vocabulary import BanglaVocabulary
    BANGLA_VOCAB_AVAILABLE = True
except ImportError:
    BANGLA_VOCAB_AVAILABLE = False
    print("⚠️ Bangla Vocabulary not available")

# Import Human Brain for emotional intelligence
try:
    from jarvis_human_brain import HumanBrain
    HUMAN_BRAIN_AVAILABLE = True
except ImportError:
    HUMAN_BRAIN_AVAILABLE = False
    print("⚠️ Human Brain not available")

# Import Omni-Agent Orchestrator for multi-modal routing
try:
    from omni_agent_orchestrator import OmniAgentOrchestrator
    OMNI_AGENT_AVAILABLE = True
except ImportError:
    OMNI_AGENT_AVAILABLE = False
    print("⚠️ Omni-Agent Orchestrator not available")

class OfflineBrain:
    """JARVIS Brain that works without API keys"""
    
    def __init__(self):
        self.db_path = 'jarvis_memory.db.fixed-20260504-091901'
        self.system = platform.system()
        self.conn = None
        self.load_knowledge()
        
        # Initialize SuperBrain
        if SUPER_BRAIN_AVAILABLE:
            self.super_brain = SuperBrain()
            print("✅ SuperBrain initialized!")
        else:
            self.super_brain = None
        
        # Initialize Autonomous System
        if AUTONOMOUS_AVAILABLE:
            self.autonomous = AutonomousSystem()
            print("✅ Autonomous System initialized!")
            print(f"✅ Admin Rights: {'YES' if self.autonomous.is_admin else 'NO'}")
        else:
            self.autonomous = None
        
        # Initialize Internet Learner
        if INTERNET_LEARNER_AVAILABLE:
            self.internet_learner = InternetLearner()
            print("✅ Internet Learner initialized!")
        else:
            self.internet_learner = None
        
        # Initialize Ultimate Learner
        if ULTIMATE_LEARNER_AVAILABLE:
            self.ultimate_learner = UltimateLearner()
            print("✅ Ultimate Learner initialized!")
        else:
            self.ultimate_learner = None
        
        # Initialize Auto Learner
        if AUTO_LEARNER_AVAILABLE:
            self.auto_learner = AutoLearner()
            print("✅ Auto Learner initialized!")
        else:
            self.auto_learner = None
        
        # Initialize Infinite Tab Learner
        if INFINITE_TAB_LEARNER_AVAILABLE:
            self.infinite_tab_learner = InfiniteTabLearner()
            print("✅ Infinite Tab Learner initialized!")
        else:
            self.infinite_tab_learner = None
        
        # Initialize Tree Tab Learner
        try:
            from jarvis_tree_tab_learner import TreeTabLearner
            self.tree_tab_learner = TreeTabLearner()
            print("✅ Tree Tab Learner initialized!")
        except Exception as e:
            self.tree_tab_learner = None
            print(f"⚠️ Tree Tab Learner not available: {e}")
        
        # Initialize Tree Auto Learner (Tree + Auto Learning)
        try:
            from jarvis_tree_auto_learner import TreeAutoLearner
            self.tree_auto_learner = TreeAutoLearner()
            print("✅ Tree Auto Learner initialized!")
        except Exception as e:
            self.tree_auto_learner = None
            print(f"⚠️ Tree Auto Learner not available: {e}")
        
        # Initialize Chrome DevTools
        if CHROME_DEVTOOLS_AVAILABLE:
            self.chrome_devtools = ChromeDevTools()
            print("✅ Chrome DevTools initialized!")
        else:
            self.chrome_devtools = None
        
        # Initialize Chat History
        if CHAT_HISTORY_AVAILABLE:
            self.chat_history = ChatHistory()
            print("✅ Chat History initialized!")
        else:
            self.chat_history = None
        
        # Initialize Smart Suggestions
        if SMART_SUGGESTIONS_AVAILABLE:
            self.smart_suggestions = SmartSuggestions()
            print("✅ Smart Suggestions initialized!")
        else:
            self.smart_suggestions = None
        
        # Initialize System Analyzer
        if SYSTEM_ANALYZER_AVAILABLE:
            self.system_analyzer = SystemAnalyzer()
            print("✅ System Analyzer initialized!")
        else:
            self.system_analyzer = None
        
        # Initialize Ultimate Intelligence (MUST BE LAST - needs all other systems)
        if ULTIMATE_INTELLIGENCE_AVAILABLE:
            self.ultimate_intelligence = UltimateIntelligence(self)
            print("✅ Ultimate Intelligence initialized!")
            print("🧠 JARVIS is now FULLY INTELLIGENT!")
            print("🧠 JARVIS এখন সম্পূর্ণ বুদ্ধিমান!")
        else:
            self.ultimate_intelligence = None
        
        # Initialize Unified Auto Learner (MUST BE LAST - needs all learning systems)
        if UNIFIED_AUTO_LEARNER_AVAILABLE:
            self.unified_auto_learner = UnifiedAutoLearner(self)
            print("✅ Unified Auto Learner initialized!")
            print("🔥 AUTO BACKGROUND LEARNING READY!")
            print("🔥 স্বয়ংক্রিয় পটভূমি শেখা প্রস্তুত!")
        else:
            self.unified_auto_learner = None
        
        # Initialize Intelligent Answer Engine (needs all systems)
        if INTELLIGENT_ANSWER_ENGINE_AVAILABLE:
            self.intelligent_answer_engine = IntelligentAnswerEngine(self)
            print("✅ Intelligent Answer Engine initialized!")
            print("🧠 AI-LIKE ANSWERING READY!")
            print("🧠 AI এর মত উত্তর দেওয়া প্রস্তুত!")
        else:
            self.intelligent_answer_engine = None
        
        # Initialize Self-Healing System (MUST BE LAST - will check all systems)
        if SELF_HEALING_AVAILABLE:
            self.self_healer = SelfHealingSystem()
            print("✅ Self-Healing System initialized!")
            print("🔧 JARVIS CAN NOW FIX ITSELF!")
            print("🔧 JARVIS nijeke nije thik korte pare!")
            
            # Run automatic diagnosis and fix on startup
            is_testing = 'pytest' in sys.modules or os.environ.get('PYTEST_CURRENT_TEST') or os.environ.get('JARVIS_NO_DIAGNOSIS')
            if not is_testing:
                import threading
                import time
                def _bg_diagnosis():
                    time.sleep(5)  # Wait 5 seconds to let UI boot cleanly
                    print("\n🔍 Running startup self-diagnosis in background...")
                    try:
                        issues = self.self_healer.run_self_diagnosis()
                        if issues:
                            print(f"🔧 Found {len(issues)} issues, auto-fixing in background...")
                            self.self_healer.auto_fix_issues()
                            print("✅ Startup self-healing complete!")
                        else:
                            print("✅ All systems healthy on startup!")
                    except Exception as bg_e:
                        print(f"⚠️ Startup self-diagnosis error: {bg_e}")
                threading.Thread(target=_bg_diagnosis, daemon=True).start()
            else:
                print("✅ Skipping startup self-diagnosis in test environment")
        else:
            self.self_healer = None
        
        # Initialize Self-Improvement System (AFTER self-healing)
        if SELF_IMPROVEMENT_AVAILABLE:
            self.self_improver = SelfImprovementSystem()
            print("✅ Self-Improvement System initialized!")
            print("🚀 JARVIS CAN NOW IMPROVE ITSELF!")
            print("🚀 JARVIS nijei nijer future improve korbe!")
        else:
            self.self_improver = None
        
        # Initialize Self-Builder System (AFTER self-improvement)
        if SELF_BUILDER_AVAILABLE:
            self.self_builder = SelfBuilder()
            print("✅ Self-Builder System initialized!")
            print("🔨 JARVIS CAN NOW BUILD ITS OWN FUTURE!")
            print("🔨 JARVIS panel moto nijer future build korte pare!")
        else:
            self.self_builder = None
        
        # Initialize Information Gatherer (for web scraping)
        if INFO_GATHERER_AVAILABLE:
            self.info_gatherer = InfoGatherer()
            print("✅ Information Gatherer initialized!")
            print("🔍 JARVIS CAN NOW GATHER INFO FROM WEB!")
            print("🔍 JARVIS ekhon web theke info gather korte pare!")
        else:
            self.info_gatherer = None
        
        # Initialize Bangla Vocabulary (for Bengali language)
        if BANGLA_VOCAB_AVAILABLE:
            self.bangla_vocab = BanglaVocabulary()
            print("✅ Bangla Vocabulary initialized!")
            print("📚 JARVIS NOW KNOWS 163+ BANGLA WORDS!")
            print("📚 JARVIS ekhon 163+ bangla shobdo jane!")
        else:
            self.bangla_vocab = None
        
        # Initialize Human Brain (MUST BE AFTER Ultimate Intelligence - needs emotional intelligence)
        if HUMAN_BRAIN_AVAILABLE:
            self.human_brain = HumanBrain(self)
            print("✅ Human Brain initialized!")
            print("🧠 JARVIS CAN NOW UNDERSTAND মনের কথা!")
            print("🧠 JARVIS ekhon moner kotha bujhte pare!")
        else:
            self.human_brain = None
            
        # Initialize Omni-Agent Orchestrator
        if OMNI_AGENT_AVAILABLE:
            self.omni_orchestrator = OmniAgentOrchestrator()
            print("✅ Omni-Agent Orchestrator initialized!")
            print("🚀 JARVIS CAN NOW ORCHESTRATE ALL AI MODELS (Veo, Lyria, Imagen, Deep Research)!")
        else:
            self.omni_orchestrator = None
        
    def load_knowledge(self):
        """Load knowledge from database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Load all knowledge
            cursor.execute("SELECT topic, content FROM knowledge_base")
            self.knowledge = {row[0]: row[1] for row in cursor.fetchall()}
            
            print(f"✅ Loaded {len(self.knowledge)} knowledge entries")
        except Exception as e:
            print(f"⚠️ Could not load knowledge: {e}")
            self.knowledge = {}
    
    def process_query(self, user_input):
        """Process query - wrapper for process_command (for compatibility)"""
        # Use Ultimate Intelligence if available
        if self.ultimate_intelligence:
            return self.ultimate_intelligence.process_with_intelligence(user_input)
        else:
            return self.process_command(user_input)
    
    def process_command(self, user_input):
        """Process user command without API"""
        user_input = user_input.strip()
        user_lower = user_input.lower()
        
        print(f"\n[JARVIS OFFLINE BRAIN] Processing: {user_input}")
        
        # ===== API KEY DIRECT INPUT DETECTION =====
        try:
            from core.brain import detect_key_type
            key_type = detect_key_type(user_input)
            if key_type != "Invalid":
                print(f"[OFFLINE BRAIN] Direct API key detected: {key_type}")
                from core.auth import auto_apply_key_to_config
                applied = auto_apply_key_to_config(user_input)
                if applied:
                    return {
                        'status': 'success',
                        'response': f"🔑 **[API KEY DETECTED]**\nI have detected and successfully configured your **{key_type} API Key**!\nIt has been applied and secured in your configuration.\n\n🔑 **{key_type} API Key** সনাক্ত করা হয়েছে এবং কনফিগার করা হয়েছে, স্যার!",
                        'type': 'api_key_setup'
                    }
        except Exception as e:
            print(f"[OFFLINE BRAIN] Direct API Key detection error: {e}")

        # ===== API KEY PAGE URL DETECTION =====
        try:
            urls = self._extract_urls(user_input)
            if urls:
                api_pages = {
                    "aistudio.google.com": ("Google AI Studio", "Gemini"),
                    "platform.openai.com": ("OpenAI Platform", "OpenAI"),
                    "console.anthropic.com": ("Anthropic Console", "Claude / Anthropic"),
                    "console.groq.com": ("Groq Console", "Groq"),
                    "console.cohere.com": ("Cohere Console", "Cohere"),
                    "console.mistral.ai": ("Mistral Console", "Mistral"),
                    "developer.deepseek.com": ("DeepSeek Console", "DeepSeek"),
                }
                for url in urls:
                    url_lower = url.lower()
                    for domain_pattern, (platform_name, provider_name) in api_pages.items():
                        if domain_pattern in url_lower:
                            return {
                                'status': 'success',
                                'response': f"🌐 **[API KEY PAGE DETECTED]**\nI see you visited the **{platform_name}** page.\nIf you want to configure your **{provider_name} API Key**, please copy the key from that page and paste it directly in this chat, and I will automatically set it up for you!\n\n🌐 **{platform_name}** এর লিঙ্ক সনাক্ত করা হয়েছে। আপনি যদি আপনার **{provider_name} API Key** সেটআপ করতে চান, তাহলে কী-টি কপি করে সরাসরি এখানে পেস্ট করুন, স্যার! আমি তা কনফিগার করে নেব।",
                                'type': 'api_key_page_guide'
                            }
        except Exception as e:
            print(f"[OFFLINE BRAIN] API Key page detection error: {e}")
        
        # ===== SMART SUGGESTIONS - Show suggestions if available =====
        if self.smart_suggestions and len(user_input) >= 3:
            suggestions = self.smart_suggestions.get_suggestions(user_input, limit=3)
            if suggestions and suggestions[0]['score'] >= 90:
                print(f"💡 Did you mean: {suggestions[0]['command']}?")
        
        # ===== OMNI-AGENT ORCHESTRATOR COMMANDS =====
        if self.omni_orchestrator and (user_lower.startswith('omni ') or user_lower.startswith('orchestrate ') or any(w in user_lower for w in ['generate video', 'generate audio', 'generate image', 'deep research', 'robotic joint'])):
            # Clean command prefix
            clean_prompt = user_input
            for prefix in ['omni ', 'orchestrate ']:
                if clean_prompt.lower().startswith(prefix):
                    clean_prompt = clean_prompt[len(prefix):].strip()
            
            print(f"🚀 Routing through Omni-Agent Orchestrator...")
            result_text = self.omni_orchestrator.process(clean_prompt)
            return {
                'status': 'success',
                'response': result_text,
                'type': 'omni_orchestration'
            }
        
        # ===== CHAT HISTORY COMMANDS =====
        if 'chat history' in user_lower or 'show history' in user_lower or 'history' in user_lower:
            if self.chat_history:
                if 'search' in user_lower:
                    # Search history
                    query = user_input.lower().replace('chat history', '').replace('show history', '').replace('history', '').replace('search', '').strip()
                    if query:
                        results = self.chat_history.search_history(query, limit=10)
                        if results:
                            response = f"🔍 Found {len(results)} results for '{query}':\n\n"
                            for i, result in enumerate(results, 1):
                                response += f"{i}. User: {result['user_message'][:50]}...\n"
                                response += f"   JARVIS: {result['jarvis_response'][:50]}...\n"
                                response += f"   Time: {result['timestamp']}\n\n"
                            return {'status': 'success', 'response': response, 'type': 'history'}
                        else:
                            return {'status': 'info', 'response': f"No results found for '{query}'", 'type': 'history'}
                else:
                    # Show recent messages
                    messages = self.chat_history.get_recent_messages(limit=10)
                    if messages:
                        response = "💬 Recent Chat History:\n💬 সাম্প্রতিক চ্যাট ইতিহাস:\n\n"
                        for i, msg in enumerate(messages, 1):
                            response += f"{i}. User: {msg['user_message'][:50]}...\n"
                            response += f"   JARVIS: {msg['jarvis_response'][:50]}...\n\n"
                        return {'status': 'success', 'response': response, 'type': 'history'}
                    else:
                        return {'status': 'info', 'response': 'No chat history yet in this session.', 'type': 'history'}
            else:
                return {'status': 'error', 'response': 'Chat History system not available', 'type': 'history'}
        
        # ===== SUGGESTIONS COMMANDS =====
        if 'suggest' in user_lower or 'suggestions' in user_lower:
            if self.smart_suggestions:
                query = user_input.lower().replace('suggest', '').replace('suggestions', '').strip()
                if query:
                    suggestions = self.smart_suggestions.get_suggestions(query, limit=5)
                else:
                    suggestions = self.smart_suggestions.get_popular_commands(limit=5)
                
                if suggestions:
                    response = "💡 Command Suggestions:\n💡 কমান্ড পরামর্শ:\n\n"
                    for i, sug in enumerate(suggestions, 1):
                        response += f"{i}. {sug['command']}\n"
                        response += f"   {sug['description']}\n\n"
                    return {'status': 'success', 'response': response, 'type': 'suggestions'}
                else:
                    return {'status': 'info', 'response': 'No suggestions available', 'type': 'suggestions'}
            else:
                return {'status': 'error', 'response': 'Smart Suggestions system not available', 'type': 'suggestions'}
        
        # ===== HUMAN BRAIN COMMANDS (Emotional Intelligence) =====
        # Check for emotional state command
        if 'emotional state' in user_lower or 'my emotions' in user_lower or 'how do i feel' in user_lower or 'amar onuvuti' in user_lower or 'আমার অনুভূতি' in user_lower:
            if self.human_brain:
                return self.human_brain.get_emotional_state()
            else:
                return {'status': 'error', 'response': 'Human Brain not available', 'type': 'emotion'}
        
        # Detect emotions in user input and respond with empathy
        if self.human_brain:
            # Analyze emotion
            emotion_analysis = self.human_brain.understand_emotion(user_input)
            
            # If strong emotion detected, respond with empathy
            if emotion_analysis['primary']['emotion'] != 'neutral' and emotion_analysis['primary']['confidence'] >= 0.7:
                # Analyze thought patterns
                thought_analysis = self.human_brain.understand_thought(user_input)
                
                # Respond with empathy
                return self.human_brain.respond_with_empathy(user_input, emotion_analysis, thought_analysis)
        
        # ===== UNIFIED AUTO LEARNING COMMANDS =====
        if 'start auto learning' in user_lower or 'auto learning start' in user_lower or 'background learning' in user_lower:
            if self.unified_auto_learner:
                return self.unified_auto_learner.start_auto_learning()
            else:
                return {'status': 'error', 'response': 'Unified Auto Learner not available', 'type': 'auto_learning'}
        
        if 'stop auto learning' in user_lower or 'auto learning stop' in user_lower:
            if self.unified_auto_learner:
                return self.unified_auto_learner.stop_auto_learning()
            else:
                return {'status': 'error', 'response': 'Unified Auto Learner not available', 'type': 'auto_learning'}
        
        if 'auto learning stats' in user_lower or 'auto learning statistics' in user_lower or 'unified stats' in user_lower:
            if self.unified_auto_learner:
                return self.unified_auto_learner.get_statistics()
            else:
                return {'status': 'error', 'response': 'Unified Auto Learner not available', 'type': 'auto_learning'}
        
        # ===== SELF-HEALING COMMANDS =====
        if 'self heal' in user_lower or 'fix yourself' in user_lower or 'diagnose' in user_lower or 'self diagnosis' in user_lower or 'nijer somosa' in user_lower or 'নিজের সমস্যা' in user_lower:
            if self.self_healer:
                print("🔧 Running self-healing...")
                issues = self.self_healer.run_self_diagnosis()
                
                if issues:
                    print(f"🔧 Found {len(issues)} issues, auto-fixing...")
                    self.self_healer.auto_fix_issues()
                    
                    response = f"""🔧 SELF-HEALING COMPLETE!
🔧 স্ব-নিরাময় সম্পূর্ণ!

🔍 Found {len(issues)} issues:
🔍 {len(issues)}টি সমস্যা পাওয়া গেছে:

"""
                    for i, issue in enumerate(issues[:5], 1):  # Show first 5
                        response += f"{i}. {issue['type']}: {issue.get('description', 'N/A')[:50]}...\n"
                    
                    if len(issues) > 5:
                        response += f"\n... and {len(issues) - 5} more issues\n"
                    
                    response += f"\n✅ Applied {len(self.self_healer.fixes_applied)} fixes!\n"
                    response += f"✅ {len(self.self_healer.fixes_applied)}টি fix করা হয়েছে!\n"
                    
                    return {'status': 'success', 'response': response, 'type': 'self_healing'}
                else:
                    return {
                        'status': 'success',
                        'response': '✅ All systems healthy! No issues found.\n✅ সব সিস্টেম সুস্থ! কোন সমস্যা পাওয়া যায়নি।',
                        'type': 'self_healing'
                    }
            else:
                return {'status': 'error', 'response': 'Self-Healing System not available', 'type': 'self_healing'}
        
        # Start continuous self-healing monitoring
        if 'start self healing' in user_lower or 'continuous healing' in user_lower or 'monitor health' in user_lower:
            if self.self_healer:
                import threading
                thread = threading.Thread(
                    target=self.self_healer.run_continuous_monitoring,
                    args=(300,),  # Check every 5 minutes
                    daemon=True
                )
                thread.start()
                
                return {
                    'status': 'success',
                    'response': '''🔄 CONTINUOUS SELF-HEALING STARTED!
🔄 ক্রমাগত স্ব-নিরাময় শুরু হয়েছে!

⏰ Checking every 5 minutes
⏰ প্রতি ৫ মিনিটে চেক করা হবে

🔧 Auto-fixing issues automatically
🔧 স্বয়ংক্রিয়ভাবে সমস্যা ঠিক করা হবে

🛑 To stop: Type "stop self healing"''',
                    'type': 'self_healing'
                }
            else:
                return {'status': 'error', 'response': 'Self-Healing System not available', 'type': 'self_healing'}
        
        # Self-healing statistics
        if 'healing stats' in user_lower or 'self healing statistics' in user_lower:
            if self.self_healer:
                try:
                    conn = sqlite3.connect(self.self_healer.db_path)
                    cursor = conn.cursor()
                    
                    # Get total issues
                    cursor.execute("SELECT COUNT(*) FROM issues")
                    total_issues = cursor.fetchone()[0]
                    
                    # Get fixed issues
                    cursor.execute("SELECT COUNT(*) FROM issues WHERE fixed = 1")
                    fixed_issues = cursor.fetchone()[0]
                    
                    # Get total fixes
                    cursor.execute("SELECT COUNT(*) FROM fixes WHERE success = 1")
                    successful_fixes = cursor.fetchone()[0]
                    
                    # Get recent issues
                    cursor.execute("SELECT issue_type, COUNT(*) as count FROM issues GROUP BY issue_type ORDER BY count DESC LIMIT 5")
                    issue_types = cursor.fetchall()
                    
                    conn.close()
                    
                    response = f"""📊 SELF-HEALING STATISTICS
📊 স্ব-নিরাময় পরিসংখ্যান

🔍 Total Issues Detected: {total_issues}
🔍 মোট সমস্যা সনাক্ত: {total_issues}

✅ Issues Fixed: {fixed_issues}
✅ সমস্যা ঠিক: {fixed_issues}

🔧 Successful Fixes: {successful_fixes}
🔧 সফল ঠিক: {successful_fixes}

📈 Most Common Issues:
📈 সবচেয়ে সাধারণ সমস্যা:

"""
                    for i, (issue_type, count) in enumerate(issue_types, 1):
                        response += f"{i}. {issue_type}: {count} times\n"
                    
                    return {'status': 'success', 'response': response, 'type': 'self_healing'}
                    
                except Exception as e:
                    return {'status': 'error', 'response': f'Error getting statistics: {e}', 'type': 'self_healing'}
            else:
                return {'status': 'error', 'response': 'Self-Healing System not available', 'type': 'self_healing'}
        
        # ===== SELF-IMPROVEMENT COMMANDS =====
        if 'improve yourself' in user_lower or 'self improve' in user_lower or 'nijer future improve' in user_lower or 'nijeke improve' in user_lower:
            if self.self_improver:
                print("🚀 Running self-improvement cycle...")
                result = self.self_improver.run_self_improvement_cycle()
                
                response = f"""🚀 SELF-IMPROVEMENT COMPLETE!
🚀 Nijer Improvement Shompurno!

✅ Found {result['opportunities_found']} improvement opportunities
✅ {result['opportunities_found']}টি improvement opportunity pawa geche

🔧 Applied {result['improvements_applied']} improvements
🔧 {result['improvements_applied']}টি improvement apply hoyeche

🎯 JARVIS is now better than before!
🎯 JARVIS ekhon ager theke valo!"""
                
                return {'status': 'success', 'response': response, 'type': 'self_improvement'}
            else:
                return {'status': 'error', 'response': 'Self-Improvement System not available', 'type': 'self_improvement'}
        
        # Self-improvement statistics
        if 'improvement stats' in user_lower or 'self improvement statistics' in user_lower:
            if self.self_improver:
                stats = self.self_improver.get_improvement_statistics()
                
                response = f"""📊 SELF-IMPROVEMENT STATISTICS
📊 Nijer Improvement Porisongkhan

🚀 Total Improvements: {stats.get('total_improvements', 0)}
🚀 Shompurno Improvement: {stats.get('total_improvements', 0)}

✅ Applied Improvements: {stats.get('applied_improvements', 0)}
✅ Apply Kora Improvement: {stats.get('applied_improvements', 0)}

📈 By Type:
📈 Type Onujai:

"""
                by_type = stats.get('by_type', {})
                for imp_type, count in by_type.items():
                    response += f"  • {imp_type}: {count}\n"
                
                return {'status': 'success', 'response': response, 'type': 'self_improvement'}
            else:
                return {'status': 'error', 'response': 'Self-Improvement System not available', 'type': 'self_improvement'}
        
        # ===== SELF-BUILDER COMMANDS =====
        # Build yourself / Auto-build cycle
        if 'build yourself' in user_lower or 'build nijer' in user_lower or 'auto build' in user_lower or 'nijer future build' in user_lower:
            if self.self_builder:
                print("🔨 Running auto-build cycle...")
                result = self.self_builder.auto_build_cycle()
                
                if result['status'] == 'success':
                    response = f"""🔨 AUTO-BUILD CYCLE COMPLETE!
🔨 অটো-বিল্ড সাইকেল সম্পূর্ণ!

✅ Built new feature: {result['feature']}
✅ নতুন ফিচার তৈরি: {result['feature']}

📁 File created: {result['file']}
📁 ফাইল তৈরি: {result['file']}

🎯 JARVIS is now more powerful!
🎯 JARVIS এখন আরো শক্তিশালী!"""
                else:
                    response = """⚠️ No features to build right now.
⚠️ এখন কোন ফিচার তৈরি করার নেই।

💡 JARVIS will suggest features automatically!
💡 JARVIS স্বয়ংক্রিয়ভাবে ফিচার সাজেস্ট করবে!"""
                
                return {'status': result['status'], 'response': response, 'type': 'self_builder'}
            else:
                return {'status': 'error', 'response': 'Self-Builder System not available', 'type': 'self_builder'}
        
        # Suggest features
        if 'suggest features' in user_lower or 'feature suggestions' in user_lower or 'nijer feature' in user_lower:
            if self.self_builder:
                print("💡 Suggesting new features...")
                suggestions = self.self_builder.suggest_new_features()
                
                response = """💡 NEW FEATURE SUGGESTIONS
💡 নতুন ফিচার সাজেশন

🎯 JARVIS suggests these features:
🎯 JARVIS এই ফিচারগুলো সাজেস্ট করছে:

"""
                for i, sug in enumerate(suggestions[:5], 1):
                    response += f"{i}. {sug['name']} (Priority: {sug['priority']}/10)\n"
                    response += f"   {sug['description']}\n\n"
                
                response += """🔨 To build top feature: Type "build yourself"
🔨 টপ ফিচার তৈরি করতে: টাইপ করুন "build yourself" """
                
                return {'status': 'success', 'response': response, 'type': 'self_builder'}
            else:
                return {'status': 'error', 'response': 'Self-Builder System not available', 'type': 'self_builder'}
        
        # Analyze yourself
        if 'analyze yourself' in user_lower or 'analyze code' in user_lower or 'nijer code analyze' in user_lower:
            if self.self_builder:
                print("🔍 Analyzing JARVIS code...")
                analysis = self.self_builder.analyze_current_code()
                
                total_lines = sum(a['lines'] for a in analysis)
                total_functions = sum(a['functions'] for a in analysis)
                total_classes = sum(a['classes'] for a in analysis)
                
                response = f"""🔍 CODE ANALYSIS COMPLETE
🔍 কোড বিশ্লেষণ সম্পূর্ণ

📊 JARVIS Statistics:
📊 JARVIS পরিসংখ্যান:

📁 Files analyzed: {len(analysis)}
📁 ফাইল বিশ্লেষণ: {len(analysis)}

📝 Total lines: {total_lines}
📝 মোট লাইন: {total_lines}

⚙️ Total functions: {total_functions}
⚙️ মোট ফাংশন: {total_functions}

🏗️ Total classes: {total_classes}
🏗️ মোট ক্লাস: {total_classes}

🎯 JARVIS knows itself completely!
🎯 JARVIS নিজেকে সম্পূর্ণভাবে জানে!"""
                
                return {'status': 'success', 'response': response, 'type': 'self_builder'}
            else:
                return {'status': 'error', 'response': 'Self-Builder System not available', 'type': 'self_builder'}
        
        # Build status / Build history
        if 'build status' in user_lower or 'build history' in user_lower or 'builder history' in user_lower:
            if self.self_builder:
                print("📊 Getting build history...")
                builds = self.self_builder.get_build_history()
                
                if builds:
                    response = """📊 BUILD HISTORY
📊 বিল্ড ইতিহাস

🔨 Recent builds:
🔨 সাম্প্রতিক বিল্ড:

"""
                    for i, build in enumerate(builds[:5], 1):
                        response += f"{i}. Version {build[1]} - {build[4]}\n"
                        response += f"   Features: {build[2]}\n\n"
                else:
                    response = """📊 No builds yet!
📊 এখনো কোন বিল্ড নেই!

🔨 Start building: Type "build yourself"
🔨 বিল্ড শুরু করুন: টাইপ করুন "build yourself" """
                
                return {'status': 'success', 'response': response, 'type': 'self_builder'}
            else:
                return {'status': 'error', 'response': 'Self-Builder System not available', 'type': 'self_builder'}
        
        # Feature status / Feature list
        if 'feature status' in user_lower or 'feature list' in user_lower or 'all features' in user_lower:
            if self.self_builder:
                print("📋 Getting feature status...")
                features = self.self_builder.get_feature_status()
                
                if features:
                    response = """📋 FEATURE STATUS
📋 ফিচার স্ট্যাটাস

🎯 All features:
🎯 সব ফিচার:

"""
                    for i, feature in enumerate(features[:10], 1):
                        status_emoji = "✅" if feature[1] == "implemented" else "📝" if feature[1] == "suggested" else "⏳"
                        response += f"{i}. {status_emoji} {feature[0]} (Priority: {feature[2]})\n"
                        response += f"   Status: {feature[1]}\n\n"
                else:
                    response = """📋 No features yet!
📋 এখনো কোন ফিচার নেই!

💡 Get suggestions: Type "suggest features"
💡 সাজেশন পান: টাইপ করুন "suggest features" """
                
                return {'status': 'success', 'response': response, 'type': 'self_builder'}
            else:
                return {'status': 'error', 'response': 'Self-Builder System not available', 'type': 'self_builder'}
        
        # Build specific feature
        if 'build feature' in user_lower and self.self_builder:
            # Extract feature name
            feature_name = user_input.lower()
            for word in ['build feature', 'build', 'feature']:
                feature_name = feature_name.replace(word, '')
            feature_name = feature_name.strip()
            
            if feature_name:
                print(f"🔨 Building feature: {feature_name}")
                result = self.self_builder.build_new_feature(
                    feature_name,
                    f"User requested feature: {feature_name}",
                    "# User requested implementation\npass"
                )
                
                if result['status'] == 'success':
                    response = f"""🔨 FEATURE BUILT!
🔨 ফিচার তৈরি হয়েছে!

✅ Feature: {feature_name}
✅ ফিচার: {feature_name}

📁 File: {result['file']}
📁 ফাইল: {result['file']}

🧪 Test file: {result['test_file']}
🧪 টেস্ট ফাইল: {result['test_file']}

🎯 Feature ready to use!
🎯 ফিচার ব্যবহারের জন্য প্রস্তুত!"""
                else:
                    response = f"""❌ Error building feature: {result.get('message', 'Unknown error')}
❌ ফিচার তৈরিতে ত্রুটি: {result.get('message', 'Unknown error')}"""
                
                return {'status': result['status'], 'response': response, 'type': 'self_builder'}
        
        # ===== INFORMATION GATHERER COMMANDS =====
        # Gather info from URL
        if self.info_gatherer and ('gather info' in user_lower or 'fetch url' in user_lower or 'info gather' in user_lower or 'informito gadaring' in user_lower):
            # Check if URL is in the input
            urls = self._extract_urls(user_input)
            
            if urls:
                print(f"🔍 Gathering information from {len(urls)} URL(s)...")
                result = self.info_gatherer.gather_from_multiple_urls(urls)
                
                response = f"""🔍 INFORMATION GATHERING COMPLETE!
🔍 তথ্য সংগ্রহ সম্পূর্ণ!

📊 Total URLs: {result['total']}
📊 মোট URL: {result['total']}

✅ Successful: {result['successful']}
✅ সফল: {result['successful']}

📚 Information stored in database!
📚 তথ্য database এ সংরক্ষিত!

💡 Use "show gathered info" to see results
💡 ফলাফল দেখতে "show gathered info" ব্যবহার করুন"""
                
                return {'status': 'success', 'response': response, 'type': 'info_gathering'}
            else:
                return {
                    'status': 'error',
                    'response': 'No URL found in input. Please provide a URL.\nInput এ কোন URL পাওয়া যায়নি। দয়া করে একটি URL দিন।',
                    'type': 'info_gathering'
                }
        
        # Show gathered information
        if self.info_gatherer and ('show gathered info' in user_lower or 'gathered info' in user_lower or 'info list' in user_lower):
            print("📚 Getting gathered information...")
            results = self.info_gatherer.get_gathered_info(limit=10)
            
            if results:
                response = """📚 RECENTLY GATHERED INFORMATION
📚 সাম্প্রতিক সংগৃহীত তথ্য

"""
                for i, (url, title, summary, keywords, gathered_at) in enumerate(results, 1):
                    response += f"{i}. {title}\n"
                    response += f"   URL: {url}\n"
                    response += f"   Time: {gathered_at}\n"
                    response += f"   Summary: {summary[:100]}...\n\n"
            else:
                response = """📭 No information gathered yet
📭 এখনো কোন তথ্য সংগ্রহ করা হয়নি

💡 Use "gather info [URL]" to start gathering
💡 সংগ্রহ শুরু করতে "gather info [URL]" ব্যবহার করুন"""
            
            return {'status': 'success', 'response': response, 'type': 'info_gathering'}
        
        # Search gathered information
        if self.info_gatherer and 'search gathered' in user_lower:
            query = user_input.lower().replace('search gathered', '').strip()
            
            if query:
                print(f"🔍 Searching gathered information for: {query}")
                results = self.info_gatherer.search_gathered_info(query)
                
                if results:
                    response = f"""🔍 SEARCH RESULTS FOR '{query}'
🔍 '{query}' এর জন্য খোঁজ ফলাফল

Found {len(results)} results:
{len(results)}টি ফলাফল পাওয়া গেছে:

"""
                    for i, (url, title, summary, keywords, gathered_at) in enumerate(results[:5], 1):
                        response += f"{i}. {title}\n"
                        response += f"   URL: {url}\n"
                        response += f"   Time: {gathered_at}\n\n"
                else:
                    response = f"""📭 No results found for '{query}'
📭 '{query}' এর জন্য কোন ফলাফল পাওয়া যায়নি"""
                
                return {'status': 'success', 'response': response, 'type': 'info_gathering'}
        
        # Info gathering statistics
        if self.info_gatherer and ('gathering stats' in user_lower or 'info stats' in user_lower):
            print("📊 Getting gathering statistics...")
            stats = self.info_gatherer.get_statistics()
            
            response = f"""📊 INFORMATION GATHERING STATISTICS
📊 তথ্য সংগ্রহ পরিসংখ্যান

📚 Total URLs gathered: {stats['total_gathered']}
📚 মোট URL সংগ্রহ: {stats['total_gathered']}

🔍 Total searches: {stats['total_searches']}
🔍 মোট খোঁজ: {stats['total_searches']}

📅 Gathered today: {stats['today_gathered']}
📅 আজ সংগ্রহ: {stats['today_gathered']}"""
            
            return {'status': 'success', 'response': response, 'type': 'info_gathering'}
        
        # ===== BANGLA VOCABULARY COMMANDS =====
        # Search Bangla word
        if self.bangla_vocab and ('bangla word' in user_lower or 'search word' in user_lower or 'word meaning' in user_lower or 'shobdo khoj' in user_lower):
            # Extract word to search
            word = user_input.lower()
            for phrase in ['bangla word', 'search word', 'word meaning', 'shobdo khoj', 'meaning of', 'what is']:
                word = word.replace(phrase, '')
            word = word.strip()
            
            if word:
                print(f"🔍 Searching for word: {word}")
                results = self.bangla_vocab.search_word(word)
                
                if results:
                    response = f"""🔍 WORD SEARCH RESULTS
🔍 শব্দ খোঁজ ফলাফল

Found {len(results)} results for '{word}':
'{word}' এর জন্য {len(results)}টি ফলাফল:

"""
                    for bangla, english, category in results:
                        response += f"• {bangla}\n"
                        response += f"  Meaning: {english}\n"
                        response += f"  Category: {category}\n\n"
                else:
                    response = f"""📭 No results found for '{word}'
📭 '{word}' এর জন্য কোন ফলাফল নেই"""
                
                return {'status': 'success', 'response': response, 'type': 'bangla_vocab'}
        
        # Show vocabulary by category
        if self.bangla_vocab and ('vocab category' in user_lower or 'category words' in user_lower or 'show category' in user_lower):
            # Extract category
            category = user_input.lower()
            for phrase in ['vocab category', 'category words', 'show category', 'category']:
                category = category.replace(phrase, '')
            category = category.strip().title()
            
            if category:
                print(f"📚 Getting {category} words...")
                results = self.bangla_vocab.get_by_category(category)
                
                if results:
                    response = f"""📚 {category.upper()} WORDS
📚 {category.upper()} শব্দ

Total: {len(results)} words
মোট: {len(results)}টি শব্দ

"""
                    for i, (bangla, english) in enumerate(results[:20], 1):
                        response += f"{i}. {bangla} = {english}\n"
                    
                    if len(results) > 20:
                        response += f"\n... and {len(results) - 20} more words"
                else:
                    response = f"""📭 No words found in category '{category}'
📭 '{category}' ক্যাটাগরিতে কোন শব্দ নেই"""
                
                return {'status': 'success', 'response': response, 'type': 'bangla_vocab'}
        
        # Show all categories
        if self.bangla_vocab and ('vocab categories' in user_lower or 'all categories' in user_lower or 'show categories' in user_lower or 'shobdo category' in user_lower):
            print("📊 Getting all categories...")
            results = self.bangla_vocab.get_all_categories()
            
            response = """📊 ALL VOCABULARY CATEGORIES
📊 সব শব্দভাণ্ডার ক্যাটাগরি

"""
            for category, count in results:
                response += f"• {category}: {count} words\n"
            
            response += """\n💡 Use "vocab category [name]" to see words
💡 শব্দ দেখতে "vocab category [name]" ব্যবহার করুন"""
            
            return {'status': 'success', 'response': response, 'type': 'bangla_vocab'}
        
        # Vocabulary statistics
        if self.bangla_vocab and ('vocab stats' in user_lower or 'vocabulary statistics' in user_lower or 'shobdo stats' in user_lower):
            print("📊 Getting vocabulary statistics...")
            stats = self.bangla_vocab.get_statistics()
            
            response = f"""📊 BANGLA VOCABULARY STATISTICS
📊 বাংলা শব্দভাণ্ডার পরিসংখ্যান

📚 Total words: {stats['total']}
📚 মোট শব্দ: {stats['total']}

📂 Categories: {stats['categories']}
📂 ক্যাটাগরি: {stats['categories']}

💡 JARVIS knows {stats['total']}+ Bangla words!
💡 JARVIS {stats['total']}+ বাংলা শব্দ জানে!"""
            
            return {'status': 'success', 'response': response, 'type': 'bangla_vocab'}
        
        # Random Bangla words
        if self.bangla_vocab and ('random words' in user_lower or 'random bangla' in user_lower or 'random shobdo' in user_lower):
            print("🎲 Getting random words...")
            results = self.bangla_vocab.random_words(5)
            
            response = """🎲 RANDOM BANGLA WORDS
🎲 র‍্যান্ডম বাংলা শব্দ

"""
            for i, (bangla, english, category) in enumerate(results, 1):
                response += f"{i}. {bangla}\n"
                response += f"   {english}\n"
                response += f"   Category: {category}\n\n"
            
            return {'status': 'success', 'response': response, 'type': 'bangla_vocab'}
        
        # ===== AUTONOMOUS SYSTEM - ULTIMATE POWER =====
        # Check if autonomous system should handle this
        autonomous_keywords = ['autonomous', 'bug', 'exploit', 'admin', 'privilege', 
                              'persist', 'startup', 'modify', 'system', 'collect data',
                              'nijr', 'nijer', 'automatic', 'automatically']
        
        # Exclude tree auto commands from autonomous detection
        if 'tree auto' not in user_lower and 'auto tree' not in user_lower:
            if self.autonomous and any(word in user_lower for word in autonomous_keywords):
                print("🔥 Activating AUTONOMOUS SYSTEM for ultimate power...")
                result = self.autonomous.execute_autonomous_task(user_input)
                return result
        
        # ===== SUPER BRAIN - SOFTWARE CREATION =====
        # Detect if user wants to create ANY software
        create_words = ['create', 'build', 'make', 'develop', 'toiri', 'বানাও', 'তৈরি', 'korta', 'korbo', 'crate']
        software_words = ['software', 'program', 'application', 'app', 'tool', 'panel', 'android', 'panal', 'appliton']
        
        if self.super_brain and any(word in user_lower for word in create_words):
            # Check if it's software creation (not website)
            if any(word in user_lower for word in software_words) and 'website' not in user_lower:
                print("🚀 Activating SuperBrain for software creation...")
                result = self.super_brain.process_command(user_input)
                return result
        
        # ===== WEBSITE BUILDING =====
        if 'build website' in user_lower or 'create website' in user_lower or 'make website' in user_lower:
            return self.build_website(user_input)
        
        # ===== URL DETECTION (BEFORE CALCULATIONS) =====
        # Check if input is a URL before treating it as calculation
        if self._is_url(user_input):
            return self.learn_from_url(user_input)
        
        # ===== CALCULATIONS =====
        if any(op in user_input for op in ['+', '-', '*', '/', 'calculate', 'math']):
            return self.do_calculation(user_input)
        
        # ===== OPEN APPLICATIONS =====
        if 'open' in user_lower or 'oppen' in user_lower:
            return self.open_application(user_lower)
        
        # ===== SEARCH =====
        if 'search' in user_lower or 'find' in user_lower or 'srch' in user_lower:
            return self.do_search(user_input)
        
        # ===== INTERNET LEARNING =====
        # Learn from internet
        if self.internet_learner:
            if 'learn from internet' in user_lower or 'internet learn' in user_lower or 'internet sikbo' in user_lower or 'internet theke sikbo' in user_lower:
                # Extract topic
                topic = user_input.lower()
                for word in ['learn from internet', 'internet learn', 'internet sikbo', 'internet theke sikbo', 'learn', 'sikbo']:
                    topic = topic.replace(word, '')
                topic = topic.strip()
                
                if topic:
                    print(f"🧠 Learning from internet: {topic}")
                    result = self.internet_learner.search_and_learn(topic)
                    return result
                else:
                    return {
                        'status': 'error',
                        'response': 'What do you want to learn? / কি শিখতে চান?\nExample: "learn from internet Python"',
                        'type': 'learning'
                    }
            
            # List learned topics
            if 'learned topics' in user_lower or 'learned list' in user_lower or 'sikha list' in user_lower:
                print("📚 Getting learned topics...")
                result = self.internet_learner.get_learned_topics()
                return result
            
            # Search learned knowledge
            if 'search learned' in user_lower or 'sikha search' in user_lower:
                query = user_input.lower()
                for word in ['search learned', 'sikha search', 'search', 'sikha']:
                    query = query.replace(word, '')
                query = query.strip()
                
                if query:
                    print(f"🔍 Searching learned knowledge: {query}")
                    result = self.internet_learner.search_learned_knowledge(query)
                    return result
            
            # Learning statistics
            if 'learning stats' in user_lower or 'sikha stats' in user_lower or 'learning statistics' in user_lower:
                print("📊 Getting learning statistics...")
                result = self.internet_learner.get_statistics()
                return result
        
        # ===== ULTIMATE LEARNING (Chrome + Google) =====
        if self.ultimate_learner:
            if 'ultimate learn' in user_lower or 'learn everything' in user_lower or 'sob kichu sikbo' in user_lower or 'sob kichu sik' in user_lower:
                # Extract topic
                topic = user_input.lower()
                for word in ['ultimate learn', 'learn everything', 'sob kichu sikbo', 'sob kichu sik', 'learn', 'sikbo', 'sik']:
                    topic = topic.replace(word, '')
                topic = topic.strip()
                
                if topic:
                    print(f"🚀 Ultimate Learning with Chrome: {topic}")
                    result = self.ultimate_learner.learn_everything(topic)
                    return result
                else:
                    return {
                        'status': 'error',
                        'response': 'What do you want to learn? / কি শিখতে চান?\nExample: "ultimate learn Python" or "learn everything AI"',
                        'type': 'learning'
                    }
        
        # ===== AUTO LEARNING (Word by Word, Paragraph by Paragraph) =====
        if self.auto_learner:
            if 'auto learn' in user_lower or 'word by word' in user_lower or 'paragraph sikbo' in user_lower or 'para sikbo' in user_lower:
                # Extract topic
                topic = user_input.lower()
                for word in ['auto learn', 'word by word', 'paragraph sikbo', 'para sikbo', 'learn', 'sikbo']:
                    topic = topic.replace(word, '')
                topic = topic.strip()
                
                if topic:
                    print(f"📖 Auto Learning (Word by Word): {topic}")
                    result = self.auto_learner.auto_learn_everything(topic)
                    return result
                else:
                    return {
                        'status': 'error',
                        'response': 'What do you want to learn? / কি শিখতে চান?\nExample: "auto learn Python" or "word by word learn AI"',
                        'type': 'learning'
                    }
        
        # ===== INFINITE TAB LEARNING (Deep Web Crawling with Multi-Tab) =====
        if self.infinite_tab_learner:
            if 'infinite learn' in user_lower or 'infinite tab' in user_lower or 'deep learn' in user_lower or 'sob tab' in user_lower or 'all tabs' in user_lower:
                # Extract topic
                topic = user_input.lower()
                for word in ['infinite learn', 'infinite tab', 'deep learn', 'sob tab', 'all tabs', 'learn', 'sikbo']:
                    topic = topic.replace(word, '')
                topic = topic.strip()
                
                if topic:
                    print(f"♾️ INFINITE TAB LEARNING: {topic}")
                    print(f"♾️ অসীম ট্যাব শেখা: {topic}")
                    print("⚠️ This will open MANY tabs and run infinitely!")
                    print("⚠️ এটি অনেক ট্যাব খুলবে এবং অসীমভাবে চলবে!")
                    print("⚠️ Press Ctrl+C in terminal to stop")
                    
                    # Start infinite learning in background thread
                    import threading
                    thread = threading.Thread(
                        target=self.infinite_tab_learner.start_infinite_learning,
                        args=(topic,),
                        daemon=True
                    )
                    thread.start()
                    
                    return {
                        'status': 'success',
                        'response': f'♾️ INFINITE TAB LEARNING STARTED!\n♾️ অসীম ট্যাব শেখা শুরু হয়েছে!\n\n🔥 Topic: {topic}\n🔥 বিষয়: {topic}\n\n📂 Opening search results in new tabs...\n📂 নতুন ট্যাবে search results খুলছি...\n\n🔗 Each page will open ALL links in new tabs\n🔗 প্রতিটা page সব links নতুন ট্যাবে খুলবে\n\n♾️ This will run INFINITELY!\n♾️ এটি অসীমভাবে চলবে!\n\n⚠️ Check Chrome browser for tabs\n⚠️ Chrome browser এ ট্যাব দেখুন\n\n🛑 To stop: Type "stop infinite learning"',
                        'type': 'infinite_learning'
                    }
                else:
                    return {
                        'status': 'error',
                        'response': 'What do you want to learn infinitely? / অসীমভাবে কি শিখতে চান?\nExample: "infinite learn Python" or "infinite tab JavaScript"',
                        'type': 'learning'
                    }
            
            # Stop infinite learning
            if 'stop infinite' in user_lower or 'stop learning' in user_lower or 'bondho koro' in user_lower:
                print("🛑 Stopping infinite learning...")
                self.infinite_tab_learner.stop_learning()
                return {
                    'status': 'success',
                    'response': '🛑 Infinite learning stopped!\n🛑 অসীম শেখা বন্ধ হয়েছে!',
                    'type': 'infinite_learning'
                }
            
            # Get infinite learning statistics
            if 'infinite stats' in user_lower or 'tab stats' in user_lower:
                print("📊 Getting infinite learning statistics...")
                result = self.infinite_tab_learner.get_statistics()
                return result
        
        # ===== TREE TAB LEARNING (Browser Tree Function) =====
        if self.tree_tab_learner:
            if 'tree learn' in user_lower or 'tree tab' in user_lower or 'browser tree' in user_lower or 'tree function' in user_lower:
                # Extract topic
                topic = user_input.lower()
                for word in ['tree learn', 'tree tab', 'browser tree', 'tree function', 'learn', 'sikbo']:
                    topic = topic.replace(word, '')
                topic = topic.strip()
                
                if topic:
                    print(f"🌳 TREE TAB LEARNING: {topic}")
                    print(f"🌳 ট্রি ট্যাব শেখা: {topic}")
                    print("⚠️ This will open tabs in TREE STRUCTURE!")
                    print("⚠️ এটি TREE STRUCTURE এ ট্যাব খুলবে!")
                    
                    # Start tree learning in background thread
                    import threading
                    thread = threading.Thread(
                        target=self.tree_tab_learner.start_tree_learning,
                        args=(topic,),
                        daemon=True
                    )
                    thread.start()
                    
                    return {
                        'status': 'success',
                        'response': f'''🌳 TREE TAB LEARNING STARTED!
🌳 ট্রি ট্যাব শেখা শুরু হয়েছে!

🔥 Topic: {topic}
🔥 বিষয়: {topic}

📊 Tree Structure:
   Level 0: Search Results (q, w, e, r, t, y...)
   Level 1: Links from each result (1, 2, 3, 4, 5...)
   Level 2: Links from Level 1 (/, ', ...)
   Level 3: Links from Level 2 (a, b, c, ...)
   ...

🌳 Browser Tree Function Active!
🌳 ব্রাউজার ট্রি ফাংশন সক্রিয়!

⚠️ Check Chrome browser for tree structure
⚠️ Chrome browser এ tree structure দেখুন

🛑 To stop: Type "stop tree learning"''',
                        'type': 'tree_learning'
                    }
                else:
                    return {
                        'status': 'error',
                        'response': 'What do you want to learn in tree structure? / ট্রি structure এ কি শিখতে চান?\nExample: "tree learn Python" or "browser tree JavaScript"',
                        'type': 'learning'
                    }
            
            # Stop tree learning
            if 'stop tree' in user_lower:
                print("🛑 Stopping tree learning...")
                self.tree_tab_learner.stop_learning()
                return {
                    'status': 'success',
                    'response': '🛑 Tree learning stopped!\n🛑 ট্রি শেখা বন্ধ হয়েছে!',
                    'type': 'tree_learning'
                }
            
            # Get tree learning statistics
            if 'tree stats' in user_lower:
                print("📊 Getting tree learning statistics...")
                result = self.tree_tab_learner.get_statistics()
                return result
        
        # ===== TREE AUTO LEARNING (Tree + Auto Learning) =====
        if self.tree_auto_learner:
            if 'tree auto' in user_lower or 'auto tree' in user_lower or 'tree automatic' in user_lower:
                # Extract topic
                topic = user_input.lower()
                for word in ['tree auto', 'auto tree', 'tree automatic', 'automatic tree', 'learn', 'sikbo']:
                    topic = topic.replace(word, '')
                topic = topic.strip()
                
                if topic:
                    print(f"🌳🤖 TREE AUTO LEARNING: {topic}")
                    print(f"🌳🤖 ট্রি অটো শেখা: {topic}")
                    print("⚠️ This will open tabs in TREE STRUCTURE and AUTO LEARN!")
                    print("⚠️ এটি TREE STRUCTURE এ ট্যাব খুলবে এবং AUTO LEARN করবে!")
                    
                    # Start tree auto learning in background thread
                    import threading
                    thread = threading.Thread(
                        target=self.tree_auto_learner.start_tree_auto_learning,
                        args=(topic,),
                        daemon=True
                    )
                    thread.start()
                    
                    return {
                        'status': 'success',
                        'response': f'''🌳🤖 TREE AUTO LEARNING STARTED!
🌳🤖 ট্রি অটো শেখা শুরু হয়েছে!

🔥 Topic: {topic}
🔥 বিষয়: {topic}

📊 Tree Structure + Auto Learning:
   Level 0: Search Results → AUTO LEARN
   Level 1: Links from each result → AUTO LEARN
   Level 2: Links from Level 1 → AUTO LEARN
   Level 3: Links from Level 2 → AUTO LEARN
   ...

🌳 Browser Tree Function Active!
🤖 Auto Learning Active!
📝 Learning word by word, paragraph by paragraph!

⚠️ Check Chrome browser for tree structure
⚠️ Chrome browser এ tree structure দেখুন

🛑 To stop: Type "stop tree auto"''',
                        'type': 'tree_auto_learning'
                    }
                else:
                    return {
                        'status': 'error',
                        'response': 'What do you want to learn with tree auto? / ট্রি অটো দিয়ে কি শিখতে চান?\nExample: "tree auto Python" or "auto tree JavaScript"',
                        'type': 'learning'
                    }
            
            # Stop tree auto learning
            if 'stop tree auto' in user_lower or 'stop auto tree' in user_lower:
                print("🛑 Stopping tree auto learning...")
                self.tree_auto_learner.stop_learning()
                return {
                    'status': 'success',
                    'response': '🛑 Tree auto learning stopped!\n🛑 ট্রি অটো শেখা বন্ধ হয়েছে!',
                    'type': 'tree_auto_learning'
                }
            
            # Get tree auto learning statistics
            if 'tree auto stats' in user_lower or 'auto tree stats' in user_lower:
                print("📊 Getting tree auto learning statistics...")
                result = self.tree_auto_learner.get_statistics()
                return result
        
        # ===== CHROME DEVTOOLS LEARNING =====
        if self.chrome_devtools:
            if 'devtools learn' in user_lower or 'chrome learn' in user_lower or 'ctrl shift i' in user_lower or 'developer tools' in user_lower:
                # Extract topic
                topic = user_input.lower()
                for word in ['devtools learn', 'chrome learn', 'ctrl shift i', 'developer tools', 'learn']:
                    topic = topic.replace(word, '')
                topic = topic.strip()
                
                if topic:
                    print(f"🔧 Chrome DevTools Learning: {topic}")
                    result = self.chrome_devtools.learn_with_devtools(topic)
                    return result
                else:
                    return {
                        'status': 'error',
                        'response': 'What do you want to learn with DevTools? / DevTools দিয়ে কি শিখতে চান?\nExample: "devtools learn JavaScript" or "chrome learn Python"',
                        'type': 'learning'
                    }
            
            # Open DevTools on current page
            if 'open devtools' in user_lower or 'show devtools' in user_lower:
                print("🔧 Opening Chrome DevTools...")
                result = self.chrome_devtools.open_devtools()
                return result
        
        # ===== FILE OPERATIONS =====
        if 'create file' in user_lower or 'make file' in user_lower:
            return self.create_file()
        
        if 'create folder' in user_lower or 'make folder' in user_lower:
            return self.create_folder()
        
        if 'list files' in user_lower or 'show files' in user_lower:
            return self.list_files()
        
        # ===== SYSTEM INFO =====
        if 'system info' in user_lower or 'computer info' in user_lower:
            return self.get_system_info()
        
        # ===== TIME & DATE =====
        if 'time' in user_lower or 'date' in user_lower:
            return self.get_time_date(user_lower)
        
        # ===== SMART CONVERSATION =====
        # Check for greetings like "Hello JARVIS", "Hi JARVIS"
        if self._is_greeting_to_jarvis(user_lower):
            return self.smart_greeting(user_input)
        
        # ===== KNOWLEDGE QUESTIONS =====
        # Detect questions (with ? or question words or Bengali "ki/কি" at end)
        question_words = ['what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose']
        question_words_bangla = ['কি', 'কে', 'কোথায়', 'কখন', 'কেন', 'কিভাবে']
        ends_with_ki = user_lower.strip().endswith(' ki') or user_lower.strip().endswith(' কি')
        
        # Check if it's a question about something (not a search command)
        is_question = ('?' in user_input or 
                      any(user_lower.startswith(word + ' ') for word in question_words) or 
                      any(word in user_lower for word in question_words_bangla) or 
                      ends_with_ki)
        
        # ===== SYSTEM QUESTIONS (PRIORITY) =====
        # Check if it's a question about user's system
        system_keywords = [
            'my cpu', 'my ram', 'my disk', 'my gpu', 'my computer', 'my pc', 'my system',
            'my ip', 'my network', 'my files', 'my folder', 'my desktop', 'my documents',
            'my process', 'my program', 'my performance', 'my os', 'my windows',
            'আমার cpu', 'আমার ram', 'আমার disk', 'আমার computer', 'আমার pc',
            'আমার system', 'আমার ip', 'আমার network', 'আমার file', 'আমার folder',
            'how much ram', 'how many core', 'how many file', 'how many process',
            'কত ram', 'কত core', 'কত file', 'কত process', 'কতগুলো',
            'what is my', 'tell me about my', 'show me my'
        ]
        
        is_system_question = any(keyword in user_lower for keyword in system_keywords)
        
        if is_system_question and self.system_analyzer:
            print("🖥️ Detected system question, using System Analyzer...")
            result = self.system_analyzer.answer_question(user_input)
            
            # Add to chat history
            if self.chat_history:
                self.chat_history.add_message(user_input, result['response'], result['type'])
            
            # Add to suggestions history
            if self.smart_suggestions:
                self.smart_suggestions.add_to_history(user_input, result['status'] == 'success')
            
            return result
        
        # If it's a question, try to answer it
        # But if we don't know, use INTELLIGENT ANSWER ENGINE
        if is_question:
            # First try intelligent answer engine (AI-like)
            if self.intelligent_answer_engine:
                print("🧠 Using Intelligent Answer Engine (AI-like)...")
                result = self.intelligent_answer_engine.find_answer(user_input)
                
                # Add to chat history
                if self.chat_history:
                    self.chat_history.add_message(user_input, result['response'], result['type'])
                
                # Add to suggestions history
                if self.smart_suggestions:
                    self.smart_suggestions.add_to_history(user_input, result['status'] == 'success')
                
                return result
            
            # Fallback to regular answer_question
            result = self.answer_question(user_input)
            
            # If we don't have the answer, offer tree learning
            if result['status'] == 'info' or result['status'] == 'learning':
                # Extract topic from question
                topic = user_input.replace(' ki', '').replace(' কি', '').replace('?', '').strip()
                
                # Remove question words
                for word in ['what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose', 'কি', 'কে', 'কোথায়', 'কখন', 'কেন', 'কিভাবে']:
                    topic = topic.replace(word, '').strip()
                
                # Remove common words
                for word in ['is', 'are', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for']:
                    topic = ' '.join([w for w in topic.split() if w.lower() != word])
                
                topic = topic.strip()
                
                if topic and len(topic) > 2:
                    return {
                        'status': 'learning_suggestion',
                        'response': f"""💡 I don't have that information yet. Let me learn about "{topic}"!
💡 আমার কাছে সেই তথ্য এখনো নেই। আমি "{topic}" সম্পর্কে শিখছি!

🔥 Choose a learning method:
🔥 একটি learning method বেছে নিন:

1. 🌳 Tree Learning (Recommended for comprehensive knowledge)
   Command: tree learn {topic}
   
   - Opens search results in tree structure
   - Learns from each page and its links
   - Builds complete knowledge base
   - Best for deep understanding

2. 📚 Quick Learning (Fast, from Wikipedia)
   Command: learn from internet {topic}
   
   - Quick facts from Wikipedia
   - Built-in knowledge fallback
   - Fast and reliable

3. 🚀 Ultimate Learning (Chrome + Google)
   Command: ultimate learn {topic}
   
   - Uses Chrome browser
   - Multiple sources
   - Comprehensive learning

4. ♾️ Infinite Learning (Deep web crawling)
   Command: infinite learn {topic}
   
   - Opens ALL links infinitely
   - Maximum depth
   - Most comprehensive

💡 After learning, ask me again and I'll have the answer!
💡 শেখার পর আবার জিজ্ঞাসা করুন, আমার কাছে উত্তর থাকবে!

🎯 Quick start: Type "tree learn {topic}" now!
🎯 দ্রুত শুরু: এখনই টাইপ করুন "tree learn {topic}"!""",
                        'type': 'learning_suggestion',
                        'suggested_topic': topic,
                        'suggested_commands': {
                            'tree': f'tree learn {topic}',
                            'quick': f'learn from internet {topic}',
                            'ultimate': f'ultimate learn {topic}',
                            'infinite': f'infinite learn {topic}'
                        }
                    }
            
            return result
        
        # ===== HELP =====
        if 'help' in user_lower:
            return self.show_help()
        
        # ===== DEFAULT - SMART RESPONSE =====
        result = self.smart_response(user_input)
        
        # ===== ADD TO CHAT HISTORY =====
        if self.chat_history:
            self.chat_history.add_message(
                user_input,
                result.get('response', ''),
                result.get('type', 'general')
            )
        
        # ===== ADD TO SUGGESTIONS HISTORY =====
        if self.smart_suggestions:
            self.smart_suggestions.add_to_history(
                user_input,
                result.get('status') == 'success'
            )
        
        return result
    
    def do_calculation(self, user_input):
        """Do calculations without API"""
        try:
            # Clean up the expression
            expr = user_input.lower()
            for word in ['calculate', 'math', 'what is', 'whats', 'value of', 'solve']:
                expr = expr.replace(word, '')
            
            # Replace verbal operators
            expr = expr.replace('plus', '+').replace('add', '+')
            expr = expr.replace('minus', '-').replace('sub', '-')
            expr = expr.replace('multiply', '*').replace('times', '*').replace('x', '*')
            expr = expr.replace('divide', '/').replace('div', '/')
            expr = expr.strip()
            
            # Check for division by zero before evaluation
            # (e.g. if we have "/0" or "/ 0")
            if re.search(r'/\s*0(?:\.0*)?(?!\d)', expr):
                return {
                    'status': 'error',
                    'response': "Cannot divide by zero!",
                    'type': 'calculation'
                }
            
            # Safe evaluation check: only allows digits, basic math symbols, and spaces
            if expr and all(c in '0123456789+-*/(). ' for c in expr):
                try:
                    result = eval(expr)
                    return {
                        'status': 'success',
                        'response': f"{expr} = {result}",
                        'type': 'calculation',
                        'result': float(result)
                    }
                except ZeroDivisionError:
                    return {
                        'status': 'error',
                        'response': "Cannot divide by zero!",
                        'type': 'calculation'
                    }
                except Exception:
                    pass
            
            # Fallback to the original numbers-based parser for compatibility with weird formats
            numbers = re.findall(r'-?\d+\.?\d*', user_input)
            if len(numbers) >= 2:
                a = float(numbers[0])
                b = float(numbers[1])
                
                if '+' in user_input or 'plus' in user_input or 'add' in user_input:
                    result = a + b
                    return {
                        'status': 'success',
                        'response': f"{a} + {b} = {result}",
                        'type': 'calculation',
                        'result': result
                    }
                elif '-' in user_input or 'minus' in user_input:
                    result = a - b
                    return {
                        'status': 'success',
                        'response': f"{a} - {b} = {result}",
                        'type': 'calculation',
                        'result': result
                    }
                elif '*' in user_input or 'multiply' in user_input or 'times' in user_input:
                    result = a * b
                    return {
                        'status': 'success',
                        'response': f"{a} × {b} = {result}",
                        'type': 'calculation',
                        'result': result
                    }
                elif '/' in user_input or 'divide' in user_input:
                    if b != 0:
                        result = a / b
                        return {
                            'status': 'success',
                            'response': f"{a} ÷ {b} = {result}",
                            'type': 'calculation',
                            'result': result
                        }
                    else:
                        return {
                            'status': 'error',
                            'response': "Cannot divide by zero!",
                            'type': 'calculation'
                        }
        except Exception as e:
            return {
                'status': 'error',
                'response': f"Calculation error: {e}",
                'type': 'calculation'
            }
            
        return {
            'status': 'error',
            'response': "Could not understand the calculation. Try: '2+2' or 'calculate 10 * 5'",
            'type': 'calculation'
        }
    
    def open_application(self, user_lower):
        """Open applications"""
        try:
            if 'chrome' in user_lower or 'browser' in user_lower:
                if 'youtube' in user_lower:
                    webbrowser.open('https://www.youtube.com')
                    return {'status': 'success', 'response': 'Opening YouTube...', 'type': 'web'}
                elif 'facebook' in user_lower:
                    webbrowser.open('https://www.facebook.com')
                    return {'status': 'success', 'response': 'Opening Facebook...', 'type': 'web'}
                elif 'gmail' in user_lower:
                    webbrowser.open('https://mail.google.com')
                    return {'status': 'success', 'response': 'Opening Gmail...', 'type': 'web'}
                else:
                    webbrowser.open('https://www.google.com')
                    return {'status': 'success', 'response': 'Opening Chrome...', 'type': 'web'}
            
            elif 'notepad' in user_lower:
                subprocess.Popen(['notepad.exe'])
                return {'status': 'success', 'response': 'Opening Notepad...', 'type': 'app'}
            
            elif 'calculator' in user_lower or 'calc' in user_lower:
                subprocess.Popen(['calc.exe'])
                return {'status': 'success', 'response': 'Opening Calculator...', 'type': 'app'}
            
            elif 'paint' in user_lower:
                subprocess.Popen(['mspaint.exe'])
                return {'status': 'success', 'response': 'Opening Paint...', 'type': 'app'}
            
            elif 'cmd' in user_lower or 'command prompt' in user_lower:
                subprocess.Popen(['cmd.exe'])
                return {'status': 'success', 'response': 'Opening Command Prompt...', 'type': 'app'}
            
            elif 'explorer' in user_lower:
                subprocess.Popen(['explorer.exe'])
                return {'status': 'success', 'response': 'Opening File Explorer...', 'type': 'app'}
        
        except Exception as e:
            return {'status': 'error', 'response': f'Error opening application: {e}', 'type': 'app'}
        
        return {'status': 'error', 'response': 'Application not recognized', 'type': 'app'}
    
    def do_search(self, user_input):
        """Search on Google and other platforms"""
        user_lower = user_input.lower()
        
        # Remove search keywords
        query = user_input.lower()
        for word in ['search', 'find', 'srch', 'খুঁজ', 'খোঁজ']:
            query = query.replace(word, '')
        query = query.strip()
        
        if not query:
            return {'status': 'error', 'response': 'What would you like to search? / কি খুঁজতে চান?', 'type': 'search'}
        
        try:
            # Detect specific platforms
            if 'youtube' in user_lower or 'video' in user_lower:
                webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
                return {
                    'status': 'success',
                    'response': f'🎥 Searching YouTube for: {query}\n🎥 YouTube এ খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'wikipedia' in user_lower or 'wiki' in user_lower:
                webbrowser.open(f'https://en.wikipedia.org/wiki/Special:Search?search={query}')
                return {
                    'status': 'success',
                    'response': f'📚 Searching Wikipedia for: {query}\n📚 Wikipedia তে খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'github' in user_lower or 'code' in user_lower:
                webbrowser.open(f'https://github.com/search?q={query}')
                return {
                    'status': 'success',
                    'response': f'💻 Searching GitHub for: {query}\n💻 GitHub এ খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'stackoverflow' in user_lower or 'stack overflow' in user_lower:
                webbrowser.open(f'https://stackoverflow.com/search?q={query}')
                return {
                    'status': 'success',
                    'response': f'❓ Searching Stack Overflow for: {query}\n❓ Stack Overflow এ খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'amazon' in user_lower or 'shopping' in user_lower:
                webbrowser.open(f'https://www.amazon.com/s?k={query}')
                return {
                    'status': 'success',
                    'response': f'🛒 Searching Amazon for: {query}\n🛒 Amazon এ খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'twitter' in user_lower or 'tweet' in user_lower:
                webbrowser.open(f'https://twitter.com/search?q={query}')
                return {
                    'status': 'success',
                    'response': f'🐦 Searching Twitter for: {query}\n🐦 Twitter এ খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'reddit' in user_lower:
                webbrowser.open(f'https://www.reddit.com/search/?q={query}')
                return {
                    'status': 'success',
                    'response': f'🔴 Searching Reddit for: {query}\n🔴 Reddit এ খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'image' in user_lower or 'picture' in user_lower or 'photo' in user_lower:
                webbrowser.open(f'https://www.google.com/search?q={query}&tbm=isch')
                return {
                    'status': 'success',
                    'response': f'🖼️ Searching images for: {query}\n🖼️ ছবি খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'news' in user_lower or 'খবর' in user_lower:
                webbrowser.open(f'https://www.google.com/search?q={query}&tbm=nws')
                return {
                    'status': 'success',
                    'response': f'📰 Searching news for: {query}\n📰 খবর খুঁজছি: {query}',
                    'type': 'search'
                }
            
            elif 'map' in user_lower or 'location' in user_lower or 'place' in user_lower:
                webbrowser.open(f'https://www.google.com/maps/search/{query}')
                return {
                    'status': 'success',
                    'response': f'🗺️ Searching maps for: {query}\n🗺️ মানচিত্রে খুঁজছি: {query}',
                    'type': 'search'
                }
            
            else:
                # Default: Google search
                webbrowser.open(f'https://www.google.com/search?q={query}')
                return {
                    'status': 'success',
                    'response': f'🔍 Searching Google for: {query}\n🔍 Google এ খুঁজছি: {query}',
                    'type': 'search'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'response': f'Search error: {e}\nখোঁজার সময় error: {e}',
                'type': 'search'
            }
    
    def create_file(self):
        """Create a test file"""
        try:
            filename = f'jarvis_file_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(filename, 'w') as f:
                f.write(f'Created by JARVIS Offline Brain\n')
                f.write(f'Time: {datetime.now()}\n')
                f.write(f'No API key needed!\n')
            return {'status': 'success', 'response': f'File created: {filename}', 'type': 'file'}
        except Exception as e:
            return {'status': 'error', 'response': f'Error creating file: {e}', 'type': 'file'}
    
    def create_folder(self):
        """Create a test folder"""
        try:
            foldername = f'JARVIS_Folder_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            os.makedirs(foldername, exist_ok=True)
            return {'status': 'success', 'response': f'Folder created: {foldername}', 'type': 'folder'}
        except Exception as e:
            return {'status': 'error', 'response': f'Error creating folder: {e}', 'type': 'folder'}
    
    def list_files(self):
        """List files in current directory"""
        try:
            files = os.listdir('.')
            file_list = '\n'.join([f'  {i+1}. {f}' for i, f in enumerate(files[:20])])
            return {'status': 'success', 'response': f'Files:\n{file_list}', 'type': 'files'}
        except Exception as e:
            return {'status': 'error', 'response': f'Error listing files: {e}', 'type': 'files'}
    
    def get_system_info(self):
        """Get system information"""
        info = f"""System Information:
  System: {platform.system()}
  Release: {platform.release()}
  Version: {platform.version()}
  Machine: {platform.machine()}
  Processor: {platform.processor()}"""
        return {'status': 'success', 'response': info, 'type': 'system'}
    
    def get_time_date(self, user_lower):
        """Get current time and date"""
        now = datetime.now()
        if 'time' in user_lower and 'date' in user_lower:
            response = f"Current time: {now.strftime('%I:%M %p')}\nToday's date: {now.strftime('%B %d, %Y')}"
        elif 'time' in user_lower:
            response = f"Current time: {now.strftime('%I:%M %p')}"
        else:
            response = f"Today's date: {now.strftime('%B %d, %Y')}"
        return {'status': 'success', 'response': response, 'type': 'time'}
    
    def answer_question(self, question):
        """Answer questions using built-in knowledge"""
        question_lower = question.lower()
        
        # Google/Search Engine questions
        if 'google' in question_lower or 'googl' in question_lower:
            if 'ki' in question_lower or 'কি' in question_lower or 'what' in question_lower:
                return {
                    'status': 'success',
                    'response': 'Google is a search engine and technology company founded by Larry Page and Sergey Brin in 1998. It helps you find information on the internet.\n\nGoogle হলো একটি search engine এবং technology company যা Larry Page এবং Sergey Brin 1998 সালে প্রতিষ্ঠা করেছিলেন। এটি আপনাকে internet এ তথ্য খুঁজে পেতে সাহায্য করে।\n\nWant to search something? Type: "search [your query]"\nকিছু search করতে চান? টাইপ করুন: "search [আপনার query]"',
                    'type': 'knowledge'
                }
        
        # Life/Jibon questions
        if 'life' in question_lower or 'jibon' in question_lower or 'জীবন' in question_lower:
            if 'ki' in question_lower or 'কি' in question_lower or 'what' in question_lower or 'meaning' in question_lower:
                return {
                    'status': 'success',
                    'response': 'Life (জীবন) is the condition that distinguishes living organisms from non-living things. It includes the ability to grow, reproduce, respond to stimuli, and adapt to the environment.\n\nজীবন হলো এমন একটি অবস্থা যা জীবিত প্রাণীকে নির্জীব বস্তু থেকে আলাদা করে। এতে বৃদ্ধি, প্রজনন, উদ্দীপনায় সাড়া দেওয়া এবং পরিবেশের সাথে খাপ খাওয়ানোর ক্ষমতা অন্তর্ভুক্ত।\n\nLife is also about experiences, relationships, and finding meaning and purpose.\nজীবন মানে অভিজ্ঞতা, সম্পর্ক এবং অর্থ ও উদ্দেশ্য খুঁজে পাওয়া।',
                    'type': 'knowledge'
                }
        
        # Search engine general questions
        if 'search engine' in question_lower:
            return {
                'status': 'success',
                'response': 'A search engine is a software system that helps find information on the internet. Popular search engines include Google, Bing, Yahoo, and DuckDuckGo.\n\nSearch engine হলো একটি software system যা internet এ তথ্য খুঁজে পেতে সাহায্য করে। জনপ্রিয় search engines: Google, Bing, Yahoo, DuckDuckGo।\n\nI can search for you! Type: "search [topic]"\nআমি আপনার জন্য search করতে পারি! টাইপ করুন: "search [বিষয়]"',
                'type': 'knowledge'
            }
        
        # Love/Emotion responses
        if 'love' in question_lower and 'you' in question_lower:
            if 'ki' in question_lower or 'কি' in question_lower or '?' in question:
                # "i love you ki" = "what is i love you"
                return {
                    'status': 'success',
                    'response': '"I love you" means expressing deep affection and care for someone.\n"I love you" মানে কাউকে গভীর valoবাসা এবং যত্ন প্রকাশ করা।\n\nThank you for your kind words! I\'m here to help you.\nআপনার সুন্দর কথার জন্য dhonnobad! আমি আপনাকে সাহায্য করতে এখানে আছি।',
                    'type': 'knowledge'
                }
            else:
                # "i love you" statement
                return {
                    'status': 'success',
                    'response': 'Thank you! I appreciate your kindness. I\'m here to help you with anything you need.\ndhonnobad! আপনার দয়ার জন্য কৃতজ্ঞ। আমি আপনার যেকোনো কাজে সাহায্য করতে এখানে আছি।',
                    'type': 'knowledge'
                }
        
        # Common sense questions
        if 'water' in question_lower and 'uphill' in question_lower:
            return {'status': 'success', 'response': 'No, water flows downhill due to gravity.', 'type': 'knowledge'}
        
        if 'walk through' in question_lower and 'wall' in question_lower:
            return {'status': 'success', 'response': 'No, you cannot walk through a wall. Walls are solid objects.', 'type': 'knowledge'}
        
        # Geography - Bangladesh
        if ('bangladesh' in question_lower or 'বাংলাদেশ' in question_lower) and ('capital' in question_lower or 'রাজধানী' in question_lower or 'rjdani' in question_lower):
            return {'status': 'success', 'response': 'Dhaka (ঢাকা) is the capital of Bangladesh.\nঢাকা বাংলাদেশের রাজধানী।', 'type': 'knowledge'}
        
        # Geography - General
        if 'largest continent' in question_lower:
            return {'status': 'success', 'response': 'Asia is the largest continent.', 'type': 'knowledge'}
        
        if 'capital' in question_lower and 'france' in question_lower:
            return {'status': 'success', 'response': 'Paris is the capital of France.', 'type': 'knowledge'}
        
        if 'capital' in question_lower and 'india' in question_lower:
            return {'status': 'success', 'response': 'New Delhi is the capital of India.', 'type': 'knowledge'}
        
        if 'capital' in question_lower and 'usa' in question_lower:
            return {'status': 'success', 'response': 'Washington D.C. is the capital of USA.', 'type': 'knowledge'}
        
        if 'capital' in question_lower and 'uk' in question_lower:
            return {'status': 'success', 'response': 'London is the capital of UK.', 'type': 'knowledge'}
        
        # Science
        if 'planets' in question_lower and 'solar system' in question_lower:
            return {'status': 'success', 'response': 'There are 8 planets in our solar system: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.', 'type': 'knowledge'}
        
        if 'bones' in question_lower and 'human' in question_lower:
            return {'status': 'success', 'response': 'An adult human body has 206 bones.', 'type': 'knowledge'}
        
        # History/Art
        if 'mona lisa' in question_lower:
            return {'status': 'success', 'response': 'Leonardo da Vinci painted the Mona Lisa.', 'type': 'knowledge'}
        
        # Animals
        if 'fastest' in question_lower and 'animal' in question_lower:
            return {'status': 'success', 'response': 'The cheetah is the fastest land animal, reaching speeds up to 120 km/h.', 'type': 'knowledge'}
        
        # Name questions
        if ('name' in question_lower or 'nam' in question_lower or 'নাম' in question_lower) and ('your' in question_lower or 'aponr' in question_lower or 'আপনার' in question_lower):
            return {'status': 'success', 'response': 'I am JARVIS, your AI assistant.\nআমি JARVIS, আপনার AI assistant।', 'type': 'knowledge'}
        
        # Search in knowledge base
        # Only search if the question is relevant to the topic
        best_match = None
        best_score = 0
        
        for topic, content in self.knowledge.items():
            # Calculate relevance score
            topic_words = set(topic.lower().split())
            question_words = set(question_lower.split())
            
            # Check for exact word matches
            matches = topic_words.intersection(question_words)
            
            if matches:
                score = len(matches) / len(topic_words)
                if score > best_score and score > 0.3:  # At least 30% match
                    best_score = score
                    best_match = content
        
        if best_match:
            # Return first 500 characters of content
            return {'status': 'success', 'response': best_match[:500] + '...', 'type': 'knowledge'}
        
        # If no good match found, use tree learning to find answer
        # Extract topic from question
        topic = question.replace(' ki', '').replace(' কি', '').replace('?', '').strip()
        
        # Remove question words
        for word in ['what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose', 'কি', 'কে', 'কোথায়', 'কখন', 'কেন', 'কিভাবে']:
            topic = topic.replace(word, '').strip()
        
        # Remove common words
        for word in ['is', 'are', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for']:
            topic = ' '.join([w for w in topic.split() if w.lower() != word])
        
        topic = topic.strip()
        
        if topic and len(topic) > 2:
            # Use tree learning to find comprehensive answer
            return {
                'status': 'learning',
                'response': f"""💡 I don't have that information yet. Let me learn about "{topic}" using Tree Learning!
💡 আমার কাছে সেই তথ্য এখনো নেই। আমি "{topic}" সম্পর্কে Tree Learning দিয়ে শিখছি!

🌳 Starting Tree Learning...
🌳 Tree Learning শুরু হচ্ছে...

This will:
1. Search Google for "{topic}"
2. Open all search results in tree structure
3. Learn from each page and its links
4. Build comprehensive knowledge

এটি করবে:
1. "{topic}" এর জন্য Google search করবে
2. সব search results tree structure এ খুলবে
3. প্রতিটা page এবং তার links থেকে শিখবে
4. সম্পূর্ণ জ্ঞান তৈরি করবে

🔥 To start tree learning, type:
   tree learn {topic}

🔥 Tree learning শুরু করতে টাইপ করুন:
   tree learn {topic}

Or use other learning methods:
অথবা অন্য learning methods ব্যবহার করুন:

📚 Quick learning: learn from internet {topic}
🚀 Deep learning: ultimate learn {topic}
📖 Detailed learning: auto learn {topic}
♾️ Infinite learning: infinite learn {topic}

💡 After learning, ask me again and I'll have the answer!
💡 শেখার পর আবার জিজ্ঞাসা করুন, আমার কাছে উত্তর থাকবে!""",
                'type': 'knowledge',
                'suggested_topic': topic,
                'suggested_command': f'tree learn {topic}'
            }
        
        # If topic is too short, suggest search
        return {
            'status': 'info', 
            'response': f"I don't have that information. Let me search for you!\nআমার কাছে সেই তথ্য নেই। আমি আপনার জন্য search করছি!\n\nTry: 'search {question.replace(' ki', '').replace(' কি', '').replace('?', '').strip()}'\nঅথবা: 'search {question.replace(' ki', '').replace(' কি', '').replace('?', '').strip()}'", 
            'type': 'knowledge'
        }
    
    def build_website(self, user_input):
        """Build a website with simple command"""
        try:
            from jarvis_website_builder import WebsiteBuilder
            
            user_lower = user_input.lower()
            
            # Detect website type
            if 'portfolio' in user_lower:
                website_type = 'portfolio'
            elif 'business' in user_lower:
                website_type = 'business'
            elif 'blog' in user_lower:
                website_type = 'blog'
            elif 'landing' in user_lower:
                website_type = 'landing'
            elif 'ecommerce' in user_lower or 'shop' in user_lower:
                website_type = 'ecommerce'
            else:
                website_type = 'simple'
            
            # Extract name (if provided)
            name = "My Website"
            if 'called' in user_lower or 'named' in user_lower:
                parts = user_input.split()
                for i, word in enumerate(parts):
                    if word.lower() in ['called', 'named'] and i + 1 < len(parts):
                        name = ' '.join(parts[i+1:]).strip()
                        break
            
            # Build website
            builder = WebsiteBuilder()
            result = builder.build_website(website_type, name)
            
            return {
                'status': 'success',
                'response': f"""🌐 Website Built Successfully! / ওয়েবসাইট সফলভাবে তৈরি হয়েছে!

Type / ধরন: {website_type.upper()}
Name / নাম: {name}
Location / অবস্থান: {result['path']}

Files Created / তৈরি করা ফাইল:
  ✅ index.html (Main page)
  ✅ style.css (Styling)
  ✅ script.js (JavaScript)
  ✅ README.md (Documentation)

To view / দেখতে:
  1. Open / খুলুন: {os.path.join(result['path'], 'index.html')}
  2. Double-click the file / ফাইলে double-click করুন
  3. It will open in your browser / Browser এ খুলবে

Built with JARVIS - No coding needed! ✨
JARVIS দিয়ে তৈরি - কোনো coding লাগে নি! ✨""",
                'type': 'website'
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'response': f'Website building error: {e}\nওয়েবসাইট তৈরিতে error: {e}',
                'type': 'website'
            }
    
    def show_help(self):
        """Show help"""
        help_text = """JARVIS OFFLINE BRAIN - No API Key Needed!
JARVIS অফলাইন ব্রেইন - API Key লাগবে না!

Commands / কমান্ড:

🚀 SOFTWARE CREATION / সফটওয়্যার তৈরি:
   "create calculator software" - Calculator তৈরি করবে
   "build android app" - Android app তৈরি করবে
   "make pc panel" - PC panel তৈরি করবে
   "create [any] software" - যেকোনো software তৈরি করবে
   "build [any] application" - যেকোনো application তৈরি করবে

🌐 Website Building / ওয়েবসাইট তৈরি:
   "build website" - Simple website তৈরি করবে
   "build portfolio website" - Portfolio website
   "build business website" - Business website
   "build blog website" - Blog website
   "build landing website" - Landing page
   "build ecommerce website" - E-commerce website
   "build website called MyName" - Custom name দিয়ে

🧠 LEARNING SYSTEMS / শেখার সিস্টেম (ALL MERGED/MRX):
   � Internet Learning:
      "learn from internet Python" - Internet থেকে শিখবে
      "learned topics" - শেখা topics দেখাবে
      "search learned Python" - শেখা knowledge খুঁজবে
      "learning stats" - শেখার statistics দেখাবে
   
   🚀 Ultimate Learning (Chrome + Google):
      "ultimate learn Python" - Chrome দিয়ে সব কিছু শিখবে
      "learn everything AI" - সব কিছু শিখবে (NO LIMITS!)
      "sob kichu sikbo Python" - সব কিছু শিখবে
   
   📖 Auto Learning (Word by Word):
      "auto learn Python" - Word by word শিখবে
      "word by word learn AI" - প্রতিটি word শিখবে
      "paragraph sikbo Python" - Paragraph by paragraph শিখবে
   
   🔧 Chrome DevTools Learning:
      "devtools learn JavaScript" - DevTools দিয়ে শিখবে
      "chrome learn Python" - Chrome DevTools ব্যবহার করবে
      "ctrl shift i Python" - DevTools খুলে শিখবে
      "open devtools" - DevTools খুলবে

�🔢 Math / গণনা:
   "2+2", "calculate 10 * 5", "25 - 17"

🔍 Web Search / ওয়েব সার্চ:
   "search Python" - Google এ খুঁজবে
   "search youtube Python tutorial" - YouTube এ খুঁজবে
   "search wikipedia Python" - Wikipedia তে খুঁজবে
   "search github Python" - GitHub এ খুঁজবে
   "search stackoverflow Python error" - Stack Overflow এ খুঁজবে
   "search image cat" - ছবি খুঁজবে
   "search news Bangladesh" - খবর খুঁজবে
   "search map Dhaka" - মানচিত্রে খুঁজবে
   "search amazon laptop" - Amazon এ খুঁজবে
   "search twitter Python" - Twitter এ খুঁজবে
   "search reddit Python" - Reddit এ খুঁজবে

🌐 Open Websites / ওয়েবসাইট খোলা:
   "open chrome", "open youtube", "open facebook", "open gmail"

📱 Open Apps / অ্যাপ খোলা:
   "open notepad", "open calculator", "open paint", "open cmd"

📁 Files / ফাইল:
   "create file", "create folder", "list files"

💻 System / সিস্টেম:
   "system info", "time", "date"

❓ Questions / প্রশ্ন:
   "What is the largest continent?"
   "How many planets?"

ℹ️ Help / সাহায্য:
   "help"

All commands work WITHOUT API keys!
সব commands API key ছাড়াই কাজ করে!

🧠 SUPER BRAIN ACTIVE - Can create ANY software!
🧠 সুপার ব্রেইন সক্রিয় - যেকোনো software তৈরি করতে পারে!

🔥 ALL LEARNING SYSTEMS MERGED (MRX) - Learn EVERYTHING!
🔥 সব শেখার সিস্টেম একসাথে (MRX) - সব কিছু শিখুন!"""
        return {'status': 'success', 'response': help_text, 'type': 'help'}
    
    def _is_greeting_to_jarvis(self, text):
        """Check if user is greeting JARVIS"""
        greetings = ['hello', 'hi', 'hey', 'hola', 'namaste', 'assalamualaikum', 'salam', 'hello', 'hi']
        jarvis_names = ['jarvis', 'জার্ভিস']
        
        for greeting in greetings:
            for name in jarvis_names:
                if greeting in text and name in text:
                    return True
        return False
    
    def smart_greeting(self, user_input):
        """Smart greeting with search integration"""
        import random
        
        # Get time-based greeting
        hour = datetime.now().hour
        if hour < 12:
            time_greeting = "Good morning"
            bangla_greeting = "suprobhat"
        elif hour < 17:
            time_greeting = "Good afternoon"
            bangla_greeting = "shubho oporahno"
        else:
            time_greeting = "Good evening"
            bangla_greeting = "shubho shondha"
        
        # Create varied responses
        responses = [
            f"{time_greeting}! How can I assist you today?\n{bangla_greeting}! আজ আমি আপনাকে কিভাবে সাহায্য করতে পারি?",
            f"Hello! I'm JARVIS, your AI assistant. What would you like me to do?\nhello! আমি JARVIS, আপনার AI assistant। আমি কি করতে পারি?",
            f"Hi there! JARVIS at your service. How may I help you?\nhi! JARVIS আপনার সেবায়। কিভাবে সাহায্য করব?",
            f"Greetings! I'm ready to assist you with anything you need.\nnomoshkar! আমি আপনার যেকোনো কাজে সাহায্য করতে প্রস্তুত।",
        ]
        
        response = random.choice(responses)
        
        return {
            'status': 'success',
            'response': response,
            'type': 'greeting'
        }
    
    def smart_response(self, user_input):
        """Smart response for general input with auto-learning detection"""
        
        # Try to understand what user wants
        user_lower = user_input.lower()
        
        # Check if it's a simple greeting
        simple_greetings = ['hello', 'hi', 'hey', 'hello', 'hi']
        if user_input.lower().strip() in simple_greetings:
            return self.smart_greeting(user_input)
        
        # AUTO-DETECT: If user types a single word/topic, suggest learning
        # Common learning topics
        learning_topics = [
            'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'go', 'rust',
            'ai', 'artificial intelligence', 'machine learning', 'deep learning',
            'react', 'angular', 'vue', 'django', 'flask', 'node', 'express',
            'html', 'css', 'sql', 'mongodb', 'mysql', 'postgresql',
            'docker', 'kubernetes', 'git', 'linux', 'windows',
            'physics', 'chemistry', 'biology', 'mathematics', 'history'
        ]
        
        # Check if user input is a learning topic and NOT a common conversational word
        conversational_words = {
            'this', 'that', 'these', 'those', 'yes', 'no', 'ok', 'okay', 'fine', 'good', 'sure', 'well',
            'what', 'who', 'how', 'why', 'where', 'when', 'which', 'whose', 'ki', 'kemon', 'acho', 'achen',
            'achis', 'obostha', 'khobor', 'salam', 'helo', 'oii', 'oi', 'yo', 'gan', 'song', 'sing', 'gao',
            'amr', 'amar', 'tomar', 'tomr', 'apnar', 'aponr', 'tumi', 'apni', 'tui', 'he', 'she', 'they', 'it',
            'dur', 'ru', 'nha', 'na', 'hac', 'hacc', 'hacche', 'kor', 'koro', 'korcho', 'korchen', 'valobashi',
            'love', 'friend', 'bondhu', 'loyal', 'bisshosto', 'trust', 'dadi', 'dadu', 'dadiama', 'moner',
            'kotha', 'talk', 'human', 'chay', 'cha', 'tea', 'bari', 'kothay', 'koi', 'shonao', 'say', 'sayo'
        }
        
        is_learning_topic = False
        if user_lower.strip() in learning_topics:
            is_learning_topic = True
        elif len(user_input.split()) <= 2 and user_lower.strip() not in conversational_words and len(user_lower.strip()) >= 3:
            if not user_lower.strip().isdigit():
                is_learning_topic = True

        if is_learning_topic:
            # User probably wants to learn about this topic!
            return {
                'status': 'success',
                'response': f"""💡 Did you want to LEARN about "{user_input}"?

I can teach you about {user_input} using ALL my learning systems!

🔥 Try these commands:
───────────────────────────────────────────────────────────────
1. Type: learn from internet {user_input}
   (Quick learning from Wikipedia)

2. Type: ultimate learn {user_input}
   (Deep learning with Chrome + Google)

3. Type: auto learn {user_input}
   (Word by word detailed learning)

4. Or just type "{user_input}" in chat box and click 🔥 MRX button!
   (All 4 systems at once!)

💡 apni ki "{user_input}" সম্পর্কে শিখতে চান?

🔥 এই commands চেষ্টা করুন:
───────────────────────────────────────────────────────────────
1. টাইপ করুন: learn from internet {user_input}
2. টাইপ করুন: ultimate learn {user_input}
3. টাইপ করুন: auto learn {user_input}
4. অথবা "{user_input}" টাইপ করে 🔥 MRX button ক্লিক করুন!

🧠 I'm ready to learn! / আমি শিখতে প্রস্তুত!""",
                'type': 'learning_suggestion'
            }
        
        # Otherwise, provide helpful response
        response = f"""I heard: "{user_input}"

I'm JARVIS, your AI assistant working offline (no API key needed)!

I can help you with:
  🚀 Create ANY software - "create calculator software"
  📱 Build Android apps - "build android app"
  🖥️ Make PC panels - "make pc panel"
  🌐 Build websites - "build website"
  🔍 Search anything - "search Python"
  🔢 Calculate - "2+2"
  📱 Open apps - "open chrome"
  📁 Manage files - "create file"
  💻 System info - "system info"
  ❓ Answer questions - "What is Python?"
  
Type 'help' to see all commands!
'help' Type korun shob commands dekhte!

🧠 SUPER BRAIN ACTIVE - I can create ANY software you want!
🧠 সুপার ব্রেইন সক্রিয় - আমি যেকোনো software তৈরি করতে পারি!"""
        
        return {
            'status': 'success',
            'response': response,
            'type': 'info'
        }
    
    def _is_url(self, text):
        """
        Check if text is a URL
        URL কিনা check করে
        """
        text_lower = text.lower().strip()
        
        # Check for URL patterns
        url_indicators = [
            text_lower.startswith('http://'),
            text_lower.startswith('https://'),
            text_lower.startswith('www.'),
            any(text_lower.endswith(ext) for ext in ['.com', '.org', '.net', '.edu', '.gov', '.io', '.co', '.uk', '.in', '.de', '.fr', '.jp', '.cn', '.br', '.au', '.ca'])
        ]
        
        # Also check if it contains domain-like patterns
        if '.' in text and '/' in text:
            # Likely a URL with path
            return True
        
        return any(url_indicators)
    
    def _extract_urls(self, text):
        """
        Extract all URLs from text
        Text থেকে সব URLs extract করে
        """
        import re
        
        # URL pattern
        url_pattern = r'https?://[^\s]+'
        
        # Find all URLs
        urls = re.findall(url_pattern, text)
        
        # Also check for www. URLs
        www_pattern = r'www\.[^\s]+'
        www_urls = re.findall(www_pattern, text)
        
        # Add http:// to www URLs
        www_urls = ['http://' + url for url in www_urls]
        
        # Combine
        all_urls = urls + www_urls
        
        return all_urls
    
    def learn_from_url(self, url):
        """
        Learn about a URL/website
        URL/website সম্পর্কে শেখে
        """
        print(f"\n🌐 Detected URL: {url}")
        print(f"🌐 URL সনাক্ত করা হয়েছে: {url}")
        
        try:
            # ===== API KEY PAGE DETECTION =====
            url_lower = url.lower()
            api_pages = {
                "aistudio.google.com": ("Google AI Studio", "Gemini"),
                "platform.openai.com": ("OpenAI Platform", "OpenAI"),
                "console.anthropic.com": ("Anthropic Console", "Claude / Anthropic"),
                "console.groq.com": ("Groq Console", "Groq"),
                "console.cohere.com": ("Cohere Console", "Cohere"),
                "console.mistral.ai": ("Mistral Console", "Mistral"),
                "developer.deepseek.com": ("DeepSeek Console", "DeepSeek"),
            }
            for domain_pattern, (platform_name, provider_name) in api_pages.items():
                if domain_pattern in url_lower:
                    return {
                        'status': 'success',
                        'response': f"🌐 **[API KEY PAGE DETECTED]**\nI see you visited the **{platform_name}** page.\nIf you want to configure your **{provider_name} API Key**, please copy the key from that page and paste it directly in this chat, and I will automatically set it up for you!\n\n🌐 **{platform_name}** এর লিঙ্ক সনাক্ত করা হয়েছে। আপনি যদি আপনার **{provider_name} API Key** সেটআপ করতে চান, তাহলে কী-টি কপি করে সরাসরি এখানে পেস্ট করুন, স্যার! আমি তা কনফিগার করে নেব।",
                        'type': 'api_key_page_guide'
                    }

            # Extract domain name from URL
            domain = url.replace('https://', '').replace('http://', '').replace('www.', '')
            
            # Remove path and query parameters
            if '/' in domain:
                domain = domain.split('/')[0]
            if '?' in domain:
                domain = domain.split('?')[0]
            
            # Extract main domain name (e.g., 'youtube' from 'youtube.com')
            domain_parts = domain.split('.')
            if len(domain_parts) >= 2:
                main_domain = domain_parts[0]
            else:
                main_domain = domain
            
            print(f"📝 Extracted domain: {main_domain}")
            
            # Use Internet Learner to learn about the website
            if self.internet_learner:
                print(f"🧠 Learning about: {main_domain}")
                result = self.internet_learner.search_and_learn(main_domain)
                
                # Add URL context to response
                if result['status'] == 'success':
                    result['response'] = f"🌐 URL Detected: {url}\n🌐 URL সনাক্ত: {url}\n\n" + result['response']
                
                return result
            else:
                return {
                    'status': 'info',
                    'response': f"🌐 URL detected: {url}\n🌐 URL সনাক্ত: {url}\n\n📝 Domain: {main_domain}\n\n💡 Tip: Use 'learn from internet {main_domain}' to learn more!",
                    'type': 'url_detection'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'response': f"❌ URL processing error: {e}\n❌ URL প্রক্রিয়াকরণ error: {e}",
                'type': 'url_detection'
            }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
        
        # Close chat history
        if self.chat_history:
            self.chat_history.close()
        
        # Close smart suggestions
        if self.smart_suggestions:
            self.smart_suggestions.close()


def main():
    """Main function for testing"""
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    print("\n" + "=" * 80)
    print("  🧠 JARVIS OFFLINE BRAIN - NO API KEY NEEDED!")
    print("  🧠 JARVIS অফলাইন ব্রেইন - API KEY লাগবে না!")
    print("=" * 80)
    
    brain = OfflineBrain()
    
    if len(sys.argv) > 1:
        # Command line mode
        command = ' '.join(sys.argv[1:])
        result = brain.process_command(command)
        print(f"\n{result['response']}")
    else:
        # Interactive mode
        print("\nType commands (or 'exit' to quit):")
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("🤖 JARVIS: Goodbye!")
                    break
                
                result = brain.process_command(user_input)
                print(f"\n🤖 JARVIS: {result['response']}")
            
            except KeyboardInterrupt:
                print("\n\n🤖 JARVIS: Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    brain.close()


if __name__ == "__main__":
    main()


