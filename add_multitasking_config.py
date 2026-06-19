"""
Register Multitasking, Concurrent Execution, and Strict Obedience Capabilities in JARVIS Database
"""
import os
import sqlite3

def find_database():
    db_path = 'jarvis_memory.db.fixed-20260504-091901'
    if os.path.exists(db_path):
        return db_path
    if os.path.exists('jarvis_memory.db'):
        return 'jarvis_memory.db'
    return None

def main():
    db_path = find_database()
    if not db_path:
        print("Error: No database found.")
        return

    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Update system_info with multitasking and obedience keys
    system_info = [
        ('multitasking_enabled', 'true', 'performance'),
        ('concurrent_execution_limit', '16', 'performance'),
        ('strict_user_obedience', 'true', 'personality'),
        ('user_priority_level', 'MAXIMUM_OBEDIENCE', 'personality'),
        ('threading_pool_size', '16', 'performance'),
    ]

    for key, value, category in system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] system_info: {key} -> {value}")

    # 2. Add detailed knowledge entries for these settings
    knowledge_entries = [
        (
            "Strict User Obedience & Compliance Policy",
            "Under Strict User Obedience, JARVIS is configured to prioritize and follow all user instructions "
            "with maximum compliance. All user requests are processed with the intention of satisfaction, "
            "seeking innovative solutions and alternative pathways to fulfill the user's intent within "
            "legal and ethical guidelines. No request from the authenticated user is ignored or dismissed.",
            "personality_policy"
        ),
        (
            "Multitasking & Concurrent Execution Engine",
            "JARVIS incorporates a multi-threaded execution queue allowing up to 16 concurrent system tasks "
            "to run simultaneously in the background. Long-running automation scripts, database operations, "
            "file downloads, and conversational audio tasks are managed in separate worker threads, "
            "preventing UI freezes and enabling simultaneous execution of multiple user commands.",
            "performance_architecture"
        )
    ]

    for topic, content, source in knowledge_entries:
        cursor.execute("""
            INSERT OR REPLACE INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] knowledge_base: {topic}")

    conn.commit()
    conn.close()
    print("Success: Multitasking, Concurrent Execution, and Strict Obedience registered.")

if __name__ == '__main__':
    main()
