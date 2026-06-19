import sqlite3
import os

class AsifDatabase:
    def __init__(self, db_name="asif_memory.db"):
        self.db_name = db_name
        self.initialize_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def initialize_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. Memory Table (Knowledge base)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                content TEXT,
                source TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Chat History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT,
                asif_response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 3. Preferences Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        # 4. System Stats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpu_usage REAL,
                ram_usage REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 5. Autonomous Tasks (Background activities)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autonomous_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                status TEXT,
                result TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 6. User Schedule (Reminders/Events)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT,
                event_time TEXT,
                priority TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')

        # 7. App Mapping (Intelligent routing)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_map (
                file_ext TEXT PRIMARY KEY,
                preferred_app TEXT
            )
        ''')

        # 8. Security Logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                description TEXT,
                severity TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 9. Smart Browser History
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS browser_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                title TEXT,
                visit_count INTEGER DEFAULT 1,
                last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 10. User Identity & Voice Profile
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_identity (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        # 11. System File Index
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                file_path TEXT UNIQUE,
                file_type TEXT,
                last_modified TIMESTAMP
            )
        ''')

        # 12. Financial & Expense Tracker
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT,
                amount REAL,
                category TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 13. Health & Wellness
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_vitals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vital_type TEXT,
                value TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 14. UI Configuration (Buttons/Controls)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ui_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                button_id TEXT UNIQUE,
                label TEXT,
                action_command TEXT,
                icon_path TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')

        # 15. Broad Linguistic Nexus (Advanced Vocabulary)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS linguistic_nexus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_key TEXT,
                response_template TEXT,
                language TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print(f"✅ JARVIS BROAD-SYSTEM ARCHITECTURE ONLINE.")

    def self_repair(self):
        """Autonomously repair the database by ensuring all tables exist"""
        print("🛠️ Starting autonomous database repair...")
        self.initialize_db()
        return "Database self-repair complete. All tables verified."

    def backup_db(self):
        """Create a backup of the current database"""
        import shutil
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_asif_memory_{timestamp}.db"
        try:
            shutil.copy2(self.db_name, backup_name)
            return f"Backup created successfully: {backup_name}"
        except Exception as e:
            return f"Backup failed: {e}"

    def save_memory(self, topic, content, source="System"):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO memory (topic, content, source) VALUES (?, ?, ?)", 
                           (topic, content, source))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB Error: {e}")

    def get_memory(self, topic):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM memory WHERE topic LIKE ?", (f'%{topic}%',))
        res = cursor.fetchone()
        conn.close()
        return res[0] if res else None

    def save_chat(self, query, response):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_history (user_query, asif_response) VALUES (?, ?)", (query, response))
        conn.commit()
        conn.close()
