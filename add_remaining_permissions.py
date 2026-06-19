"""
Add User, Program, Hardware, Security, System, and Human-like Keyboard/Mouse Control Permissions to JARVIS Database
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

    # 1. Update system_info table with the requested permissions
    system_info = [
        ('user_permission_enabled', 'true', 'permissions'),
        ('program_permission_enabled', 'true', 'permissions'),
        ('hardware_permission_enabled', 'true', 'permissions'),
        ('security_permission_enabled', 'true', 'permissions'),
        ('system_permission_enabled', 'true', 'permissions'),
        ('human_like_input_automation', 'true', 'permissions'),
        ('all_permissions_status', 'ALL SAFE PERMISSIONS ENABLED (145+)', 'permissions')
    ]

    for key, value, category in system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] system_info: {key} -> {value}")

    # 2. Add detailed knowledge entries for these categories
    knowledge_entries = [
        (
            "User Permission Detail",
            "User Permission allows JARVIS to access active user folders, custom user profiles, "
            "browsing configurations, and user app settings. This is used for personalized "
            "file structuring, desktop personalization, and localized notifications.",
            "host_permissions"
        ),
        (
            "Program Permission Detail",
            "Program Permission grants JARVIS the ability to open, manage, inspect, and terminate "
            "local applications on the host machine. This includes managing windows, setting process "
            "priority levels, and launching system utilities.",
            "host_permissions"
        ),
        (
            "Hardware Permission Detail",
            "Hardware Permission enables JARVIS to interact directly with connected system devices, "
            "including monitor display settings, graphics card acceleration resources, sound devices, "
            "camera/microphone inputs, and mouse/keyboard controllers.",
            "host_permissions"
        ),
        (
            "Security Permission Detail",
            "Security Permission allows JARVIS to handle safe cryptographic operations, check "
            "firewall status, configure security policies, update security patches, and consolidate "
            "memory databases securely without exposing host vulnerability.",
            "host_permissions"
        ),
        (
            "System Permission Detail",
            "System Permission provides access to essential operating system services, including "
            "registry queries, scheduled task execution, background service control, mount points, "
            "environment variables, and system event logging.",
            "host_permissions"
        ),
        (
            "Human-like Keyboard and Mouse Control",
            "Human-like Keyboard and Mouse Control grants JARVIS the capability to control mouse movements "
            "smoothly, perform double-clicks, scroll windows, and simulate keyboard inputs (including "
            "shortcuts and text macros) just like a human operator, automating user interfaces from A to Z.",
            "automation_capabilities"
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
    print("Success: Remaining User, Program, Hardware, Security, and System permissions added.")

if __name__ == '__main__':
    main()
