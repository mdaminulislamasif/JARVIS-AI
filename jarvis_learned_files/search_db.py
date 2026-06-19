import sqlite3
import os

db_files = [
    "jarvis_logins.db",
    "jarvis_contacts.db",
    "jarvis_memory.db",
    "asif_memory.db",
    "jarvis_chat_history.db"
]

search_term = "Idrish"

for db in db_files:
    db_path = os.path.join("c:\\Users\\PHP\\Desktop\\ai", db)
    if os.path.exists(db_path):
        print(f"--- Checking {db} ---")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                # Try to search all columns
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.execute(f"PRAGMA table_info({table_name})").fetchall()]
                
                query = f"SELECT * FROM {table_name} WHERE " + " OR ".join([f"CAST({col} AS TEXT) LIKE '%{search_term}%'" for col in columns])
                try:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    if results:
                        print(f"Found in table {table_name}:")
                        for row in results:
                            print(row)
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            conn.close()
        except Exception as e:
            print(f"Error reading {db}: {e}")
    else:
        print(f"{db} not found.")
