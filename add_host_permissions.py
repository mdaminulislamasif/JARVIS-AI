"""
Add Super Host and Terminal/PowerShell Permissions to JARVIS Database
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
        print("❌ Error: No database found.")
        return

    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Update system_info table
    system_info = [
        ('super_host_enabled', 'true', 'permissions'),
        ('user_host_enabled', 'true', 'permissions'),
        ('all_host_enabled', 'true', 'permissions'),
        ('terminal_access_enabled', 'true', 'permissions'),
        ('powershell_access_enabled', 'true', 'permissions'),
        ('cmd_access_enabled', 'true', 'permissions'),
        ('host_permissions_level', 'Super Host / Administrator', 'permissions'),
    ]

    for key, value, category in system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] system_info: {key} -> {value}")

    # 2. Add knowledge base articles for these permissions
    knowledge_entries = [
        (
            "Super Host Permission",
            "Super Host Permission allows JARVIS full administrative control over the host system. "
            "It grants permissions to run tasks as administrator, configure system preferences, "
            "manage local user hosts, configure networking, and perform environment optimization. "
            "With Super Host access, JARVIS acts as the ultimate supervisor of system resources.",
            "host_permissions"
        ),
        (
            "User Host & All Host Permission",
            "User Host and All Host permissions define how JARVIS interacts with the user session and "
            "other host settings on the PC. It permits session monitoring, user preference syncing, "
            "cross-user service interaction (where permitted), and execution of automation scripts "
            "tailored to the active user profile.",
            "host_permissions"
        ),
        (
            "Terminal & PowerShell Access",
            "Terminal & PowerShell access permits JARVIS to use Windows Command Prompt (cmd.exe) and "
            "PowerShell (powershell.exe) to execute commands for automation, file diagnostics, service "
            "restarts, and other system utilities. This allows JARVIS to dynamically run command-line "
            "tools to satisfy user needs and resolve system errors autonomously.",
            "host_permissions"
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
    print("Success: Host and Terminal permissions successfully added.")

if __name__ == '__main__':
    main()
