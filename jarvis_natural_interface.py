"""
JARVIS NATURAL INTERFACE
সব কাজ করবে, সব কথা বুঝবে - Natural Computer Control

This module provides natural language interface for JARVIS.
এই module JARVIS এর জন্য natural language interface প্রদান করে।

Features:
- Natural language understanding (বাংলা + English + Banglish)
- Context-aware processing
- Smart command mapping
- Conversational AI
- Proactive assistance
"""

import re
import difflib
from typing import Dict, List, Tuple, Optional
import json
import os
from datetime import datetime


class NaturalInterface:
    """Natural language interface for JARVIS"""
    
    def __init__(self):
        self.context = []  # Conversation context
        self.last_command = None
        self.user_preferences = {}
        self.command_history = []
        
        # Load command mappings
        self.command_map = self._load_command_mappings()
        self.aliases = self._load_aliases()
        self.patterns = self._load_patterns()
        
    def _load_command_mappings(self) -> Dict:
        """Load natural language to command mappings"""
        return {
            # Network commands
            "network": ["recon", "scan network", "network scan", "network check"],
            "wifi": ["wifi", "wifi scan", "wireless scan", "wifi check"],
            "devices": ["devices", "show devices", "list devices", "device list"],
            "router": ["router", "router scan", "router check"],
            
            # System commands
            "clean": ["clean", "cleanup", "clean system", "system clean"],
            "screenshot": ["screenshot", "screen capture", "capture screen", "ss"],
            "disk": ["disk", "disk info", "disk space", "storage"],
            "memory": ["memory", "ram", "memory info", "ram info"],
            "processes": ["processes", "running processes", "task list"],
            
            # Learning commands
            "learn": ["learn", "auto learn", "start learning", "learn from web"],
            "search": ["search", "google", "web search", "search web"],
            "article": ["article", "read article", "learn article"],
            
            # AI commands
            "brain": ["brain", "ai brain", "brain status", "ai status"],
            "think": ["think", "analyze", "process", "understand"],
            
            # File commands
            "open": ["open", "open file", "launch", "start"],
            "close": ["close", "close file", "exit"],
            "save": ["save", "save file", "write"],
            
            # Browser commands
            "browse": ["browse", "browser", "open browser", "web"],
            "youtube": ["youtube", "yt", "open youtube"],
            "google": ["google", "search google", "google search"],
            
            # Security commands
            "scan": ["scan", "security scan", "virus scan", "malware scan"],
            "firewall": ["firewall", "enable firewall", "firewall on"],
            "kali": ["kali", "kali mode", "hacking mode", "pentesting"],
            
            # Control commands
            "lock": ["lock", "lock computer", "lock pc", "lock system"],
            "shutdown": ["shutdown", "shut down", "power off", "turn off"],
            "restart": ["restart", "reboot", "restart pc"],
            
            # Media commands
            "play": ["play", "play music", "play video", "start playing"],
            "pause": ["pause", "stop", "pause music"],
            "volume": ["volume", "sound", "audio", "volume control"],
            
            # Translation
            "translate": ["translate", "translation", "convert language"],
            
            # Generator
            "generate": ["generate", "create", "make", "build"],
            "image": ["image", "picture", "photo", "img"],
            "video": ["video", "vid", "movie"],
        }
    
    def _load_aliases(self) -> Dict:
        """Load Banglish and Bengali aliases"""
        return {
            # Banglish/Bengali to English
            "kholo": "open",
            "bondho": "close",
            "bondho koro": "close",
            "khuje": "search",
            "khuje dao": "search",
            "dekho": "show",
            "dekhao": "show",
            "shuru koro": "start",
            "shesh koro": "stop",
            "bujho": "understand",
            "bojho": "understand",
            "shikho": "learn",
            "shikhao": "teach",
            "bol": "say",
            "bolo": "say",
            "koro": "do",
            "dao": "give",
            "nao": "take",
            "chalu koro": "start",
            "chalu": "start",
            "band koro": "stop",
            "band": "stop",
            "scan koro": "scan",
            "check koro": "check",
            "clean koro": "clean",
            "lock koro": "lock",
            "off koro": "shutdown",
            "restart koro": "restart",
            "translate koro": "translate",
            "generate koro": "generate",
            "create koro": "create",
            "banao": "create",
            "tiri koro": "create",
        }
    
    def _load_patterns(self) -> List[Tuple[str, str]]:
        """Load regex patterns for command detection"""
        return [
            # Network patterns
            (r"(network|wifi|internet).*(scan|check|test)", "network scan"),
            (r"(device|computer).*(find|show|list)", "devices"),
            (r"router.*(scan|check|info)", "router scan"),
            
            # System patterns
            (r"(clean|cleanup|clear).*(system|temp|cache)", "clean"),
            (r"(take|capture|grab).*(screenshot|screen|ss)", "screenshot"),
            (r"(disk|storage|space).*(info|check|show)", "disk"),
            (r"(memory|ram).*(info|check|show)", "memory"),
            
            # Learning patterns
            (r"(learn|study|read).*(from|about|on)", "learn"),
            (r"(search|find|lookup).*(google|web|internet)", "search"),
            (r"(read|learn).*(article|blog|post)", "article"),
            
            # File patterns
            (r"(open|launch|start).*(file|program|app)", "open"),
            (r"(close|exit|quit).*(file|program|app)", "close"),
            
            # Browser patterns
            (r"(open|go to|visit).*(youtube|yt)", "youtube"),
            (r"(search|find).*(google)", "google search"),
            (r"(open|launch).*(browser|chrome|firefox)", "browse"),
            
            # Security patterns
            (r"(scan|check).*(virus|malware|security)", "scan virus"),
            (r"(enable|turn on|activate).*(firewall)", "firewall on"),
            (r"(kali|hacking|pentesting).*(mode)", "kali mode"),
            
            # Control patterns
            (r"(lock|secure).*(computer|pc|system)", "lock"),
            (r"(shutdown|turn off|power off)", "shutdown"),
            (r"(restart|reboot)", "restart"),
            
            # Media patterns
            (r"(play|start).*(music|song|video)", "play"),
            (r"(pause|stop).*(music|song|video)", "pause"),
            (r"(volume|sound).*(up|down|control)", "volume"),
            
            # Translation patterns
            (r"(translate|convert).*(to|into)", "translate"),
            
            # Generator patterns
            (r"(generate|create|make).*(image|picture|photo)", "generate image"),
            (r"(generate|create|make).*(video)", "generate video"),
        ]
    
    def understand(self, user_input: str) -> Dict:
        """
        Understand user input and extract intent
        
        Args:
            user_input: Natural language input from user
            
        Returns:
            Dict with intent, command, confidence, and context
        """
        # Clean input
        cleaned = self._clean_input(user_input)
        
        # Add to context
        self.context.append({
            "input": user_input,
            "cleaned": cleaned,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 context items
        if len(self.context) > 10:
            self.context = self.context[-10:]
        
        # Extract intent
        intent = self._extract_intent(cleaned)
        
        # Map to command
        command = self._map_to_command(intent, cleaned)
        
        # Calculate confidence
        confidence = self._calculate_confidence(cleaned, command)
        
        # Get suggestions
        suggestions = self._get_suggestions(cleaned, command)
        
        return {
            "intent": intent,
            "command": command,
            "confidence": confidence,
            "suggestions": suggestions,
            "context": self.context[-3:],  # Last 3 context items
            "original": user_input,
            "cleaned": cleaned
        }
    
    def _clean_input(self, text: str) -> str:
        """Clean and normalize input text"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Replace Banglish/Bengali with English
        for banglish, english in self.aliases.items():
            text = text.replace(banglish, english)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove punctuation at end
        text = text.rstrip('.,!?;:')
        
        return text
    
    def _extract_intent(self, text: str) -> str:
        """Extract user intent from text"""
        # Check patterns first
        for pattern, intent in self.patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return intent
        
        # Check command map
        for intent, keywords in self.command_map.items():
            for keyword in keywords:
                if keyword in text:
                    return intent
        
        # Check for question words
        if any(word in text for word in ["what", "how", "why", "when", "where", "ki", "kemon", "keno"]):
            return "question"
        
        # Check for action words
        if any(word in text for word in ["do", "make", "create", "start", "stop", "show", "tell"]):
            return "action"
        
        # Default
        return "general"
    
    def _map_to_command(self, intent: str, text: str) -> str:
        """Map intent to JARVIS command"""
        # Direct command mapping
        if intent in self.command_map:
            # Find best matching command
            for keyword in self.command_map[intent]:
                if keyword in text:
                    return keyword
            # Return first command as default
            return self.command_map[intent][0]
        
        # Pattern-based mapping
        for pattern, command in self.patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return command
        
        # Fuzzy matching
        all_commands = []
        for commands in self.command_map.values():
            all_commands.extend(commands)
        
        matches = difflib.get_close_matches(text, all_commands, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        
        # Return original text as command
        return text
    
    def _calculate_confidence(self, text: str, command: str) -> float:
        """Calculate confidence score for command mapping"""
        # Exact match
        if text == command:
            return 1.0
        
        # Contains command
        if command in text:
            return 0.9
        
        # Pattern match
        for pattern, cmd in self.patterns:
            if re.search(pattern, text, re.IGNORECASE) and cmd == command:
                return 0.85
        
        # Fuzzy match
        ratio = difflib.SequenceMatcher(None, text, command).ratio()
        return ratio
    
    def _get_suggestions(self, text: str, command: str) -> List[str]:
        """Get command suggestions based on input"""
        suggestions = []
        
        # Get similar commands
        all_commands = []
        for commands in self.command_map.values():
            all_commands.extend(commands)
        
        matches = difflib.get_close_matches(text, all_commands, n=3, cutoff=0.5)
        suggestions.extend(matches)
        
        # Add context-based suggestions
        if self.last_command:
            # Suggest related commands
            if "network" in self.last_command:
                suggestions.extend(["wifi scan", "devices", "router scan"])
            elif "learn" in self.last_command:
                suggestions.extend(["search", "article", "translate"])
        
        # Remove duplicates and current command
        suggestions = list(set(suggestions))
        if command in suggestions:
            suggestions.remove(command)
        
        return suggestions[:5]  # Return top 5
    
    def process(self, user_input: str) -> Dict:
        """
        Process user input and return response
        
        Args:
            user_input: Natural language input
            
        Returns:
            Dict with command, response, and metadata
        """
        # Understand input
        understanding = self.understand(user_input)
        
        # Update last command
        self.last_command = understanding["command"]
        self.command_history.append({
            "input": user_input,
            "command": understanding["command"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate response
        response = self._generate_response(understanding)
        
        return {
            "command": understanding["command"],
            "response": response,
            "confidence": understanding["confidence"],
            "suggestions": understanding["suggestions"],
            "understanding": understanding
        }
    
    def _generate_response(self, understanding: Dict) -> str:
        """Generate natural language response"""
        command = understanding["command"]
        confidence = understanding["confidence"]
        
        if confidence > 0.8:
            return f"✅ বুঝেছি! {command} execute করছি..."
        elif confidence > 0.6:
            return f"🤔 মনে হচ্ছে আপনি {command} করতে চাচ্ছেন। Confirm করুন?"
        else:
            suggestions = understanding["suggestions"]
            if suggestions:
                return f"❓ আপনি কি এগুলোর কোনটা বোঝাতে চাচ্ছেন? {', '.join(suggestions[:3])}"
            else:
                return f"❓ দুঃখিত, আমি ঠিক বুঝতে পারিনি। আরেকবার বলুন?"
    
    def get_context(self) -> List[Dict]:
        """Get conversation context"""
        return self.context
    
    def clear_context(self):
        """Clear conversation context"""
        self.context = []
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get command history"""
        return self.command_history[-limit:]
    
    def save_preferences(self, filepath: str = "jarvis_preferences.json"):
        """Save user preferences"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "preferences": self.user_preferences,
                    "history": self.command_history[-100:],  # Last 100 commands
                }, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
    
    def load_preferences(self, filepath: str = "jarvis_preferences.json"):
        """Load user preferences"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_preferences = data.get("preferences", {})
                    self.command_history = data.get("history", [])
                return True
        except Exception as e:
            print(f"Error loading preferences: {e}")
        return False


# Test function
def test_natural_interface():
    """Test the natural interface"""
    interface = NaturalInterface()
    
    test_inputs = [
        "network scan koro",
        "wifi check koro",
        "screenshot nao",
        "google a search koro python tutorial",
        "file kholo",
        "system clean koro",
        "translate koro english to bangla",
        "image generate koro",
        "lock koro computer",
        "kali mode enable koro",
    ]
    
    print("=" * 60)
    print("JARVIS NATURAL INTERFACE TEST")
    print("=" * 60)
    
    for user_input in test_inputs:
        print(f"\n📝 Input: {user_input}")
        result = interface.process(user_input)
        print(f"🎯 Command: {result['command']}")
        print(f"💬 Response: {result['response']}")
        print(f"📊 Confidence: {result['confidence']:.2%}")
        if result['suggestions']:
            print(f"💡 Suggestions: {', '.join(result['suggestions'])}")
        print("-" * 60)


if __name__ == "__main__":
    test_natural_interface()
