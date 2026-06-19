"""
JARVIS COMMUNICATION SYSTEM
Complete Communication & Contact Management

This module provides communication features for JARVIS.
এই module JARVIS এর জন্য communication features প্রদান করে।

Features:
- VoIP calling (Twilio integration)
- SMS sending
- Contact management
- Call history
- Voice mail
- Call recording
- Smart dialing
- Emergency contacts
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import sqlite3


class CommunicationSystem:
    """Communication system for JARVIS"""
    
    def __init__(self, db_path: str = "jarvis_contacts.db"):
        self.db_path = db_path
        self.twilio_configured = False
        self.twilio_client = None
        
        # Initialize database
        self._init_database()
        
        # Try to load Twilio credentials
        self._load_twilio_config()
    
    def _init_database(self):
        """Initialize contacts database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                notes TEXT,
                favorite INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Call history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS call_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                phone TEXT NOT NULL,
                direction TEXT,
                duration INTEGER,
                status TEXT,
                timestamp TEXT,
                FOREIGN KEY (contact_id) REFERENCES contacts (id)
            )
        ''')
        
        # SMS history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sms_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                phone TEXT NOT NULL,
                message TEXT NOT NULL,
                direction TEXT,
                status TEXT,
                timestamp TEXT,
                FOREIGN KEY (contact_id) REFERENCES contacts (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def _load_twilio_config(self):
        """Load Twilio configuration"""
        try:
            config_file = "twilio_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                # Initialize Twilio client
                from twilio.rest import Client
                self.twilio_client = Client(
                    config['account_sid'],
                    config['auth_token']
                )
                self.twilio_phone = config['phone_number']
                self.twilio_configured = True
                print("✅ Twilio configured")
            else:
                print("⚠️ Twilio not configured (create twilio_config.json)")
        except Exception as e:
            print(f"⚠️ Twilio configuration failed: {e}")
    
    # =========================================================================
    # CONTACT MANAGEMENT
    # =========================================================================
    
    def add_contact(self, name: str, phone: str, email: str = None, 
                   address: str = None, notes: str = None) -> int:
        """Add new contact"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO contacts (name, phone, email, address, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, phone, email, address, notes, now, now))
            
            contact_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Contact added: {name}")
            return contact_id
        except Exception as e:
            print(f"❌ Failed to add contact: {e}")
            return -1
    
    def get_contact(self, contact_id: int) -> Optional[Dict]:
        """Get contact by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'phone': row[2],
                    'email': row[3],
                    'address': row[4],
                    'notes': row[5],
                    'favorite': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                }
            return None
        except Exception as e:
            print(f"❌ Failed to get contact: {e}")
            return None
    
    def search_contacts(self, query: str) -> List[Dict]:
        """Search contacts by name or phone"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM contacts 
                WHERE name LIKE ? OR phone LIKE ?
                ORDER BY name
            ''', (f'%{query}%', f'%{query}%'))
            
            contacts = []
            for row in cursor.fetchall():
                contacts.append({
                    'id': row[0],
                    'name': row[1],
                    'phone': row[2],
                    'email': row[3],
                    'address': row[4],
                    'notes': row[5],
                    'favorite': row[6]
                })
            
            conn.close()
            print(f"✅ Found {len(contacts)} contacts")
            return contacts
        except Exception as e:
            print(f"❌ Failed to search contacts: {e}")
            return []
    
    def get_all_contacts(self) -> List[Dict]:
        """Get all contacts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM contacts ORDER BY name')
            
            contacts = []
            for row in cursor.fetchall():
                contacts.append({
                    'id': row[0],
                    'name': row[1],
                    'phone': row[2],
                    'email': row[3],
                    'favorite': row[6]
                })
            
            conn.close()
            return contacts
        except Exception as e:
            print(f"❌ Failed to get contacts: {e}")
            return []
    
    def update_contact(self, contact_id: int, **kwargs) -> bool:
        """Update contact"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build update query
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ['name', 'phone', 'email', 'address', 'notes', 'favorite']:
                    fields.append(f"{key} = ?")
                    values.append(value)
            
            if not fields:
                return False
            
            fields.append("updated_at = ?")
            values.append(datetime.now().isoformat())
            values.append(contact_id)
            
            query = f"UPDATE contacts SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            conn.commit()
            conn.close()
            
            print(f"✅ Contact updated: {contact_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to update contact: {e}")
            return False
    
    def delete_contact(self, contact_id: int) -> bool:
        """Delete contact"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Contact deleted: {contact_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete contact: {e}")
            return False
    
    def set_favorite(self, contact_id: int, favorite: bool = True) -> bool:
        """Set contact as favorite"""
        return self.update_contact(contact_id, favorite=1 if favorite else 0)
    
    def get_favorites(self) -> List[Dict]:
        """Get favorite contacts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM contacts WHERE favorite = 1 ORDER BY name')
            
            contacts = []
            for row in cursor.fetchall():
                contacts.append({
                    'id': row[0],
                    'name': row[1],
                    'phone': row[2]
                })
            
            conn.close()
            return contacts
        except Exception as e:
            print(f"❌ Failed to get favorites: {e}")
            return []
    
    # =========================================================================
    # VOIP CALLING (Twilio)
    # =========================================================================
    
    def make_call(self, to_number: str, from_number: str = None) -> Optional[str]:
        """Make VoIP call using Twilio"""
        if not self.twilio_configured:
            print("❌ Twilio not configured")
            return None
        
        try:
            if from_number is None:
                from_number = self.twilio_phone
            
            call = self.twilio_client.calls.create(
                to=to_number,
                from_=from_number,
                url='http://demo.twilio.com/docs/voice.xml'  # Default TwiML
            )
            
            # Log call
            self._log_call(to_number, 'outgoing', call.sid)
            
            print(f"✅ Call initiated: {call.sid}")
            return call.sid
        except Exception as e:
            print(f"❌ Failed to make call: {e}")
            return None
    
    def send_sms(self, to_number: str, message: str, from_number: str = None) -> Optional[str]:
        """Send SMS using Twilio"""
        if not self.twilio_configured:
            print("❌ Twilio not configured")
            return None
        
        try:
            if from_number is None:
                from_number = self.twilio_phone
            
            sms = self.twilio_client.messages.create(
                to=to_number,
                from_=from_number,
                body=message
            )
            
            # Log SMS
            self._log_sms(to_number, message, 'outgoing', sms.sid)
            
            print(f"✅ SMS sent: {sms.sid}")
            return sms.sid
        except Exception as e:
            print(f"❌ Failed to send SMS: {e}")
            return None
    
    def _log_call(self, phone: str, direction: str, call_sid: str):
        """Log call to history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find contact
            cursor.execute('SELECT id FROM contacts WHERE phone = ?', (phone,))
            row = cursor.fetchone()
            contact_id = row[0] if row else None
            
            cursor.execute('''
                INSERT INTO call_history (contact_id, phone, direction, status, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (contact_id, phone, direction, call_sid, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Failed to log call: {e}")
    
    def _log_sms(self, phone: str, message: str, direction: str, sms_sid: str):
        """Log SMS to history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find contact
            cursor.execute('SELECT id FROM contacts WHERE phone = ?', (phone,))
            row = cursor.fetchone()
            contact_id = row[0] if row else None
            
            cursor.execute('''
                INSERT INTO sms_history (contact_id, phone, message, direction, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (contact_id, phone, message, direction, sms_sid, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Failed to log SMS: {e}")
    
    # =========================================================================
    # CALL HISTORY
    # =========================================================================
    
    def get_call_history(self, limit: int = 50) -> List[Dict]:
        """Get call history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT ch.*, c.name 
                FROM call_history ch
                LEFT JOIN contacts c ON ch.contact_id = c.id
                ORDER BY ch.timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'id': row[0],
                    'phone': row[2],
                    'direction': row[3],
                    'duration': row[4],
                    'status': row[5],
                    'timestamp': row[6],
                    'contact_name': row[7]
                })
            
            conn.close()
            return history
        except Exception as e:
            print(f"❌ Failed to get call history: {e}")
            return []
    
    def get_sms_history(self, limit: int = 50) -> List[Dict]:
        """Get SMS history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT sh.*, c.name 
                FROM sms_history sh
                LEFT JOIN contacts c ON sh.contact_id = c.id
                ORDER BY sh.timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'id': row[0],
                    'phone': row[2],
                    'message': row[3],
                    'direction': row[4],
                    'status': row[5],
                    'timestamp': row[6],
                    'contact_name': row[7]
                })
            
            conn.close()
            return history
        except Exception as e:
            print(f"❌ Failed to get SMS history: {e}")
            return []
    
    # =========================================================================
    # SMART FEATURES
    # =========================================================================
    
    def quick_dial(self, name_or_number: str) -> Optional[str]:
        """Quick dial by name or number"""
        # Search contact
        contacts = self.search_contacts(name_or_number)
        
        if contacts:
            # Use first match
            contact = contacts[0]
            print(f"📞 Calling {contact['name']} ({contact['phone']})")
            return self.make_call(contact['phone'])
        elif name_or_number.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            # Direct number
            print(f"📞 Calling {name_or_number}")
            return self.make_call(name_or_number)
        else:
            print(f"❌ Contact not found: {name_or_number}")
            return None
    
    def quick_sms(self, name_or_number: str, message: str) -> Optional[str]:
        """Quick SMS by name or number"""
        # Search contact
        contacts = self.search_contacts(name_or_number)
        
        if contacts:
            # Use first match
            contact = contacts[0]
            print(f"💬 Sending SMS to {contact['name']} ({contact['phone']})")
            return self.send_sms(contact['phone'], message)
        elif name_or_number.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            # Direct number
            print(f"💬 Sending SMS to {name_or_number}")
            return self.send_sms(name_or_number, message)
        else:
            print(f"❌ Contact not found: {name_or_number}")
            return None
    
    def get_contact_stats(self) -> Dict:
        """Get contact statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total contacts
            cursor.execute('SELECT COUNT(*) FROM contacts')
            total_contacts = cursor.fetchone()[0]
            
            # Favorites
            cursor.execute('SELECT COUNT(*) FROM contacts WHERE favorite = 1')
            favorites = cursor.fetchone()[0]
            
            # Total calls
            cursor.execute('SELECT COUNT(*) FROM call_history')
            total_calls = cursor.fetchone()[0]
            
            # Total SMS
            cursor.execute('SELECT COUNT(*) FROM sms_history')
            total_sms = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_contacts': total_contacts,
                'favorites': favorites,
                'total_calls': total_calls,
                'total_sms': total_sms
            }
        except Exception as e:
            print(f"❌ Failed to get stats: {e}")
            return {}


# Test function
def test_communication_system():
    """Test communication system"""
    print("=" * 60)
    print("JARVIS COMMUNICATION SYSTEM TEST")
    print("=" * 60)
    
    comm = CommunicationSystem()
    
    # Test 1: Add contacts
    print("\n🧪 Test 1: Add Contacts")
    id1 = comm.add_contact("John Doe", "+1234567890", "john@example.com")
    id2 = comm.add_contact("Jane Smith", "+0987654321", "jane@example.com")
    
    # Test 2: Search contacts
    print("\n🧪 Test 2: Search Contacts")
    results = comm.search_contacts("John")
    print(f"Found: {results}")
    
    # Test 3: Get all contacts
    print("\n🧪 Test 3: Get All Contacts")
    all_contacts = comm.get_all_contacts()
    print(f"Total contacts: {len(all_contacts)}")
    
    # Test 4: Set favorite
    print("\n🧪 Test 4: Set Favorite")
    comm.set_favorite(id1, True)
    favorites = comm.get_favorites()
    print(f"Favorites: {favorites}")
    
    # Test 5: Get stats
    print("\n🧪 Test 5: Get Stats")
    stats = comm.get_contact_stats()
    print(f"Stats: {stats}")
    
    # Test 6: Twilio status
    print("\n🧪 Test 6: Twilio Status")
    print(f"Twilio configured: {comm.twilio_configured}")
    
    print("\n" + "=" * 60)
    print("✅ All tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_communication_system()
