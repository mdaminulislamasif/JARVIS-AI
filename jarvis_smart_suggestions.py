"""
JARVIS SMART SUGGESTIONS SYSTEM
স্মার্ট পরামর্শ সিস্টেম

Features:
- Command suggestions based on input
- Auto-complete
- Command history
- Popular commands
- Context-aware suggestions
"""

import sqlite3
from datetime import datetime
from collections import Counter
import re


class SmartSuggestions:
    """Provides smart command suggestions and auto-complete"""
    
    def __init__(self, db_path='jarvis_suggestions.db'):
        self.db_path = db_path
        self.conn = None
        
        # All available commands
        self.all_commands = {
            # Software Creation
            'create calculator software': 'Create a calculator application',
            'build android app': 'Build an Android application',
            'make pc panel': 'Create a PC control panel',
            'create software': 'Create any software',
            
            # Website Building
            'build website': 'Build a simple website',
            'build portfolio website': 'Build a portfolio website',
            'build business website': 'Build a business website',
            'build blog website': 'Build a blog website',
            
            # Learning Commands
            'learn from internet': 'Learn from internet (Wikipedia)',
            'ultimate learn': 'Deep learning with Chrome + Google',
            'auto learn': 'Word by word detailed learning',
            'tree learn': 'Tree structure learning',
            'tree auto': 'Tree structure + Auto learning',
            'infinite learn': 'Infinite deep web crawling',
            
            # Search Commands
            'search': 'Search on Google',
            'search youtube': 'Search on YouTube',
            'search wikipedia': 'Search on Wikipedia',
            'search github': 'Search on GitHub',
            'search stackoverflow': 'Search on Stack Overflow',
            'search image': 'Search for images',
            'search news': 'Search for news',
            'search map': 'Search on maps',
            
            # File Operations
            'create file': 'Create a new file',
            'create folder': 'Create a new folder',
            'list files': 'List files in directory',
            
            # System Commands
            'system info': 'Show system information',
            'time': 'Show current time',
            'date': 'Show current date',
            
            # Open Applications
            'open chrome': 'Open Chrome browser',
            'open youtube': 'Open YouTube',
            'open facebook': 'Open Facebook',
            'open gmail': 'Open Gmail',
            'open notepad': 'Open Notepad',
            'open calculator': 'Open Calculator',
            'open paint': 'Open Paint',
            
            # Statistics
            'learning stats': 'Show learning statistics',
            'tree stats': 'Show tree learning statistics',
            'chat history': 'Show chat history',
            
            # Help
            'help': 'Show all available commands',
        }
        
        # Command categories
        self.categories = {
            'Software Creation': ['create', 'build', 'make', 'software', 'app', 'application'],
            'Learning': ['learn', 'tree', 'auto', 'ultimate', 'infinite'],
            'Search': ['search', 'find', 'youtube', 'wikipedia', 'github'],
            'Files': ['file', 'folder', 'list'],
            'System': ['system', 'time', 'date', 'info'],
            'Open': ['open', 'chrome', 'notepad', 'calculator'],
        }
        
        self.init_database()
    
    def init_database(self):
        """Initialize suggestions database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create command history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    timestamp TEXT,
                    success INTEGER
                )
            ''')
            
            # Create popular commands table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS popular_commands (
                    command TEXT PRIMARY KEY,
                    usage_count INTEGER DEFAULT 1,
                    last_used TEXT
                )
            ''')
            
            self.conn.commit()
            print("✅ Smart Suggestions database initialized!")
            
        except Exception as e:
            print(f"⚠️ Suggestions database error: {e}")
    
    def add_to_history(self, command, success=True):
        """Add command to history"""
        try:
            cursor = self.conn.cursor()
            
            # Add to history
            cursor.execute('''
                INSERT INTO command_history (command, timestamp, success)
                VALUES (?, ?, ?)
            ''', (command, datetime.now().isoformat(), 1 if success else 0))
            
            # Update popular commands
            cursor.execute('''
                INSERT INTO popular_commands (command, usage_count, last_used)
                VALUES (?, 1, ?)
                ON CONFLICT(command) DO UPDATE SET
                    usage_count = usage_count + 1,
                    last_used = ?
            ''', (command, datetime.now().isoformat(), datetime.now().isoformat()))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"⚠️ Error adding to history: {e}")
    
    def get_suggestions(self, partial_input, limit=5):
        """
        Get command suggestions based on partial input
        
        Args:
            partial_input: User's partial input
            limit: Maximum number of suggestions
        
        Returns:
            List of suggested commands with descriptions
        """
        if not partial_input:
            return self.get_popular_commands(limit)
        
        partial_lower = partial_input.lower().strip()
        suggestions = []
        
        # 1. Exact prefix matches
        for cmd, desc in self.all_commands.items():
            if cmd.startswith(partial_lower):
                suggestions.append({
                    'command': cmd,
                    'description': desc,
                    'match_type': 'exact_prefix',
                    'score': 100
                })
        
        # 2. Word matches
        partial_words = set(partial_lower.split())
        for cmd, desc in self.all_commands.items():
            cmd_words = set(cmd.split())
            matches = partial_words.intersection(cmd_words)
            if matches and cmd not in [s['command'] for s in suggestions]:
                score = (len(matches) / len(partial_words)) * 80
                suggestions.append({
                    'command': cmd,
                    'description': desc,
                    'match_type': 'word_match',
                    'score': score
                })
        
        # 3. Contains matches
        for cmd, desc in self.all_commands.items():
            if partial_lower in cmd and cmd not in [s['command'] for s in suggestions]:
                suggestions.append({
                    'command': cmd,
                    'description': desc,
                    'match_type': 'contains',
                    'score': 60
                })
        
        # 4. Category matches
        for category, keywords in self.categories.items():
            if any(keyword in partial_lower for keyword in keywords):
                for cmd, desc in self.all_commands.items():
                    if any(keyword in cmd for keyword in keywords) and cmd not in [s['command'] for s in suggestions]:
                        suggestions.append({
                            'command': cmd,
                            'description': desc,
                            'match_type': 'category',
                            'score': 40
                        })
        
        # Sort by score and limit
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        return suggestions[:limit]
    
    def get_popular_commands(self, limit=5):
        """Get most popular commands"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT command, usage_count
                FROM popular_commands
                ORDER BY usage_count DESC, last_used DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            
            suggestions = []
            for cmd, count in results:
                if cmd in self.all_commands:
                    suggestions.append({
                        'command': cmd,
                        'description': self.all_commands[cmd],
                        'match_type': 'popular',
                        'usage_count': count,
                        'score': 100
                    })
            
            return suggestions
            
        except Exception as e:
            print(f"⚠️ Error getting popular commands: {e}")
            return []
    
    def get_recent_commands(self, limit=5):
        """Get recently used commands"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT command
                FROM command_history
                WHERE success = 1
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            
            suggestions = []
            for (cmd,) in results:
                if cmd in self.all_commands:
                    suggestions.append({
                        'command': cmd,
                        'description': self.all_commands[cmd],
                        'match_type': 'recent'
                    })
            
            return suggestions
            
        except Exception as e:
            print(f"⚠️ Error getting recent commands: {e}")
            return []
    
    def get_command_by_category(self, category):
        """Get all commands in a category"""
        if category not in self.categories:
            return []
        
        keywords = self.categories[category]
        suggestions = []
        
        for cmd, desc in self.all_commands.items():
            if any(keyword in cmd for keyword in keywords):
                suggestions.append({
                    'command': cmd,
                    'description': desc,
                    'category': category
                })
        
        return suggestions
    
    def auto_complete(self, partial_input):
        """
        Auto-complete command
        
        Args:
            partial_input: User's partial input
        
        Returns:
            Best matching complete command or None
        """
        suggestions = self.get_suggestions(partial_input, limit=1)
        
        if suggestions and suggestions[0]['score'] >= 80:
            return suggestions[0]['command']
        
        return None
    
    def get_statistics(self):
        """Get suggestion statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total commands used
            cursor.execute('SELECT COUNT(*) FROM command_history')
            total_commands = cursor.fetchone()[0]
            
            # Successful commands
            cursor.execute('SELECT COUNT(*) FROM command_history WHERE success = 1')
            successful_commands = cursor.fetchone()[0]
            
            # Most popular command
            cursor.execute('''
                SELECT command, usage_count
                FROM popular_commands
                ORDER BY usage_count DESC
                LIMIT 1
            ''')
            result = cursor.fetchone()
            most_popular = result[0] if result else "None"
            most_popular_count = result[1] if result else 0
            
            # Unique commands used
            cursor.execute('SELECT COUNT(DISTINCT command) FROM command_history')
            unique_commands = cursor.fetchone()[0]
            
            return {
                'total_commands': total_commands,
                'successful_commands': successful_commands,
                'most_popular': most_popular,
                'most_popular_count': most_popular_count,
                'unique_commands': unique_commands,
                'success_rate': (successful_commands / total_commands * 100) if total_commands > 0 else 0
            }
            
        except Exception as e:
            print(f"⚠️ Error getting statistics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Test smart suggestions system"""
    print("\n" + "="*80)
    print("  💡 JARVIS SMART SUGGESTIONS SYSTEM TEST")
    print("  💡 JARVIS স্মার্ট পরামর্শ সিস্টেম টেস্ট")
    print("="*80)
    
    suggestions = SmartSuggestions()
    
    # Test adding to history
    print("\n📝 Adding test commands to history...")
    suggestions.add_to_history("search Python", True)
    suggestions.add_to_history("learn from internet AI", True)
    suggestions.add_to_history("create file", True)
    suggestions.add_to_history("search Python", True)  # Duplicate to test popularity
    
    # Test getting suggestions
    test_inputs = [
        "sear",
        "learn",
        "create",
        "tree",
        "open"
    ]
    
    print("\n💡 Testing suggestions:")
    for input_text in test_inputs:
        print(f"\n  Input: '{input_text}'")
        results = suggestions.get_suggestions(input_text, limit=3)
        for i, result in enumerate(results, 1):
            print(f"    {i}. {result['command']}")
            print(f"       {result['description']}")
            print(f"       (Match: {result['match_type']}, Score: {result['score']:.0f})")
    
    # Test auto-complete
    print("\n🔄 Testing auto-complete:")
    test_complete = ["sear", "learn from", "tree le"]
    for input_text in test_complete:
        complete = suggestions.auto_complete(input_text)
        print(f"  '{input_text}' → '{complete}'")
    
    # Test popular commands
    print("\n🔥 Popular commands:")
    popular = suggestions.get_popular_commands(5)
    for i, cmd in enumerate(popular, 1):
        print(f"  {i}. {cmd['command']} (used {cmd.get('usage_count', 0)} times)")
    
    # Test statistics
    print("\n📊 Statistics:")
    stats = suggestions.get_statistics()
    print(f"  Total commands: {stats['total_commands']}")
    print(f"  Successful: {stats['successful_commands']}")
    print(f"  Most popular: {stats['most_popular']} ({stats['most_popular_count']} times)")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    
    suggestions.close()
    
    print("\n✅ Smart Suggestions System test complete!")


if __name__ == "__main__":
    main()
