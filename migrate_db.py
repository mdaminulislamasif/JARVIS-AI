import sqlite3
import os

def migrate():
    source_db = r"c:\Users\PHP\Desktop\ai\jarvis_memory.db.fixed-20260504-091901"
    target_db = "asif_memory.db"
    
    if not os.path.exists(source_db):
        print(f"Source DB not found: {source_db}")
        return

    print(f"Migrating data from {source_db} to {target_db}...")
    
    try:
        s_conn = sqlite3.connect(source_db)
        t_conn = sqlite3.connect(target_db)
        s_cursor = s_conn.cursor()
        t_cursor = t_conn.cursor()
        
        # Ensure target table exists
        t_cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                content TEXT,
                source TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        knowledge_tables = [
            'knowledge_base', 'internet_learned', 'ultimate_knowledge', 
            'auto_learned', 'infinite_learned', 'tree_learned'
        ]
        
        total_migrated = 0
        for table in knowledge_tables:
            try:
                s_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if s_cursor.fetchone():
                    print(f"Processing {table}...")
                    s_cursor.execute(f"SELECT * FROM {table}")
                    rows = s_cursor.fetchall()
                    
                    for row in rows:
                        try:
                            # Map based on typical structure (id, topic, content, ...)
                            topic = str(row[1])
                            content = str(row[2])
                            source = f"JARVIS Migration ({table})"
                            t_cursor.execute("INSERT OR IGNORE INTO memory (topic, content, source) VALUES (?, ?, ?)", 
                                           (topic, content, source))
                            total_migrated += 1
                        except Exception as e:

                            print(f"⚠️ Error: {e}")
                            continue
                    t_conn.commit()
            except Exception as e:
                print(f"Error processing {table}: {e}")
                
        print(f"Successfully migrated {total_migrated} total entries to Asif's memory.")
        s_conn.close()
        t_conn.close()
        
    except Exception as e:
        print(f"Migration Error: {e}")

if __name__ == "__main__":
    migrate()
