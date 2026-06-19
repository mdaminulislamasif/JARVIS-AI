"""
JARVIS CHAT HISTORY SYSTEM
চ্যাট ইতিহাস সিস্টেম

Features:
- Save all conversations
- Recall previous messages
- Search chat history
- Context awareness
- Conversation flow
"""

import sqlite3
import json
from datetime import datetime
import os


class ChatHistory:
    """Manages chat history and context"""
    
    def __init__(self, db_path='jarvis_chat_history.db'):
        self.db_path = db_path
        self.conn = None
        self.current_session_id = None
        self.conversation_context = []  # Store recent messages for context
        self.max_context_messages = 10  # Keep last 10 messages in context
        
        self.init_database()
        self.start_new_session()
    
    def init_database(self):
        """Initialize chat history database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT,
                    end_time TEXT,
                    message_count INTEGER DEFAULT 0
                )
            ''')
            
            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    role TEXT,
                    message TEXT,
                    response TEXT,
                    response_type TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            
            # Create context table (for quick context retrieval)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS context (
                    session_id TEXT PRIMARY KEY,
                    context_data TEXT,
                    last_updated TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            
            self.conn.commit()
            print("✅ Chat History database initialized!")
            
        except Exception as e:
            print(f"⚠️ Chat History database error: {e}")
    
    def start_new_session(self):
        """Start a new chat session"""
        try:
            self.current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (session_id, start_time, message_count)
                VALUES (?, ?, 0)
            ''', (self.current_session_id, datetime.now().isoformat()))
            
            self.conn.commit()
            
            # Clear conversation context for new session
            self.conversation_context = []
            
            print(f"✅ New chat session started: {self.current_session_id}")
            
        except Exception as e:
            print(f"⚠️ Error starting session: {e}")
    
    def add_message(self, user_message, jarvis_response, response_type='general'):
        """
        Add a message to chat history
        
        Args:
            user_message: User's input
            jarvis_response: JARVIS's response
            response_type: Type of response (calculation, search, learning, etc.)
        """
        try:
            cursor = self.conn.cursor()
            
            # Add to messages table
            cursor.execute('''
                INSERT INTO messages (session_id, timestamp, role, message, response, response_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.current_session_id,
                datetime.now().isoformat(),
                'user',
                user_message,
                jarvis_response,
                response_type
            ))
            
            # Update session message count
            cursor.execute('''
                UPDATE sessions
                SET message_count = message_count + 1
                WHERE session_id = ?
            ''', (self.current_session_id,))
            
            self.conn.commit()
            
            # Add to conversation context
            self.conversation_context.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_message,
                'jarvis': jarvis_response,
                'type': response_type
            })
            
            # Keep only last N messages in context
            if len(self.conversation_context) > self.max_context_messages:
                self.conversation_context = self.conversation_context[-self.max_context_messages:]
            
            # Update context in database
            self.save_context()
            
        except Exception as e:
            print(f"⚠️ Error adding message: {e}")
    
    def save_context(self):
        """Save current conversation context to database"""
        try:
            cursor = self.conn.cursor()
            
            context_json = json.dumps(self.conversation_context)
            
            cursor.execute('''
                INSERT OR REPLACE INTO context (session_id, context_data, last_updated)
                VALUES (?, ?, ?)
            ''', (self.current_session_id, context_json, datetime.now().isoformat()))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"⚠️ Error saving context: {e}")
    
    def get_context(self):
        """Get current conversation context"""
        return self.conversation_context
    
    def get_context_summary(self):
        """Get a summary of recent conversation for context awareness"""
        if not self.conversation_context:
            return "No previous conversation in this session."
        
        summary = "Recent conversation:\n"
        for i, msg in enumerate(self.conversation_context[-5:], 1):  # Last 5 messages
            summary += f"{i}. User: {msg['user'][:50]}...\n"
            summary += f"   JARVIS: {msg['jarvis'][:50]}...\n"
        
        return summary
    
    def search_history(self, query, limit=10):
        """
        Search chat history
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of matching messages
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, message, response, response_type
                FROM messages
                WHERE message LIKE ? OR response LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', limit))
            
            results = cursor.fetchall()
            
            return [{
                'timestamp': row[0],
                'user_message': row[1],
                'jarvis_response': row[2],
                'type': row[3]
            } for row in results]
            
        except Exception as e:
            print(f"⚠️ Error searching history: {e}")
            return []
    
    def get_recent_messages(self, limit=20):
        """Get recent messages from current session"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, message, response, response_type
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (self.current_session_id, limit))
            
            results = cursor.fetchall()
            
            return [{
                'timestamp': row[0],
                'user_message': row[1],
                'jarvis_response': row[2],
                'type': row[3]
            } for row in reversed(results)]  # Reverse to show oldest first
            
        except Exception as e:
            print(f"⚠️ Error getting recent messages: {e}")
            return []
    
    def get_all_sessions(self):
        """Get all chat sessions"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT session_id, start_time, end_time, message_count
                FROM sessions
                ORDER BY start_time DESC
            ''')
            
            results = cursor.fetchall()
            
            return [{
                'session_id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'message_count': row[3]
            } for row in results]
            
        except Exception as e:
            print(f"⚠️ Error getting sessions: {e}")
            return []
    
    def get_session_messages(self, session_id):
        """Get all messages from a specific session"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, message, response, response_type
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp ASC
            ''', (session_id,))
            
            results = cursor.fetchall()
            
            return [{
                'timestamp': row[0],
                'user_message': row[1],
                'jarvis_response': row[2],
                'type': row[3]
            } for row in results]
            
        except Exception as e:
            print(f"⚠️ Error getting session messages: {e}")
            return []
    
    def end_session(self):
        """End current chat session"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                UPDATE sessions
                SET end_time = ?
                WHERE session_id = ?
            ''', (datetime.now().isoformat(), self.current_session_id))
            
            self.conn.commit()
            
            print(f"✅ Session ended: {self.current_session_id}")
            
        except Exception as e:
            print(f"⚠️ Error ending session: {e}")
    
    def get_statistics(self):
        """Get chat history statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total sessions
            cursor.execute('SELECT COUNT(*) FROM sessions')
            total_sessions = cursor.fetchone()[0]
            
            # Total messages
            cursor.execute('SELECT COUNT(*) FROM messages')
            total_messages = cursor.fetchone()[0]
            
            # Messages by type
            cursor.execute('''
                SELECT response_type, COUNT(*) as count
                FROM messages
                GROUP BY response_type
                ORDER BY count DESC
            ''')
            messages_by_type = cursor.fetchall()
            
            # Current session stats
            cursor.execute('''
                SELECT message_count
                FROM sessions
                WHERE session_id = ?
            ''', (self.current_session_id,))
            current_session_messages = cursor.fetchone()[0]
            
            return {
                'total_sessions': total_sessions,
                'total_messages': total_messages,
                'current_session_messages': current_session_messages,
                'messages_by_type': [{'type': row[0], 'count': row[1]} for row in messages_by_type]
            }
            
        except Exception as e:
            print(f"⚠️ Error getting statistics: {e}")
            return {}
    
    def clear_old_sessions(self, days=30):
        """Clear sessions older than specified days"""
        try:
            cursor = self.conn.cursor()
            
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            cutoff_iso = datetime.fromtimestamp(cutoff_date).isoformat()
            
            # Get old session IDs
            cursor.execute('''
                SELECT session_id
                FROM sessions
                WHERE start_time < ?
            ''', (cutoff_iso,))
            
            old_sessions = [row[0] for row in cursor.fetchall()]
            
            if old_sessions:
                # Delete messages from old sessions
                cursor.execute(f'''
                    DELETE FROM messages
                    WHERE session_id IN ({','.join(['?']*len(old_sessions))})
                ''', old_sessions)
                
                # Delete context from old sessions
                cursor.execute(f'''
                    DELETE FROM context
                    WHERE session_id IN ({','.join(['?']*len(old_sessions))})
                ''', old_sessions)
                
                # Delete old sessions
                cursor.execute(f'''
                    DELETE FROM sessions
                    WHERE session_id IN ({','.join(['?']*len(old_sessions))})
                ''', old_sessions)
                
                self.conn.commit()
                
                print(f"✅ Cleared {len(old_sessions)} old sessions")
                return len(old_sessions)
            else:
                print("✅ No old sessions to clear")
                return 0
            
        except Exception as e:
            print(f"⚠️ Error clearing old sessions: {e}")
            return 0
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.end_session()
            self.conn.close()


def main():
    """Test chat history system"""
    print("\n" + "="*80)
    print("  💬 JARVIS CHAT HISTORY SYSTEM TEST")
    print("  💬 JARVIS চ্যাট ইতিহাস সিস্টেম টেস্ট")
    print("="*80)
    
    history = ChatHistory()
    
    # Test adding messages
    print("\n📝 Adding test messages...")
    history.add_message("Hello JARVIS", "Hello! How can I help you?", "greeting")
    history.add_message("2+2", "2.0 + 2.0 = 4.0", "calculation")
    history.add_message("search Python", "Searching Google for: Python", "search")
    
    # Test getting context
    print("\n📚 Current context:")
    context = history.get_context()
    for msg in context:
        print(f"  User: {msg['user']}")
        print(f"  JARVIS: {msg['jarvis'][:50]}...")
    
    # Test searching history
    print("\n🔍 Searching for 'Python':")
    results = history.search_history("Python")
    for result in results:
        print(f"  Found: {result['user_message']}")
    
    # Test statistics
    print("\n📊 Statistics:")
    stats = history.get_statistics()
    print(f"  Total sessions: {stats['total_sessions']}")
    print(f"  Total messages: {stats['total_messages']}")
    print(f"  Current session: {stats['current_session_messages']} messages")
    
    history.close()
    
    print("\n✅ Chat History System test complete!")


if __name__ == "__main__":
    main()
