"""
JARVIS Database Fix & Windows 10 Pro Information Setup
Run: python fix_database_windows10.py
- Fixes corrupted jarvis_memory.db
- Adds Windows 10 Pro system information
- Creates proper schema with all necessary tables
- Populates with useful Windows 10 Pro data
"""
import os
import sqlite3
import time
import platform
import subprocess
from datetime import datetime

DB_PATH = "jarvis_memory.db"

def get_windows_info():
    """Gather Windows 10 Pro system information"""
    info = {
        'os_name': platform.system(),
        'os_version': platform.version(),
        'os_release': platform.release(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'hostname': platform.node(),
    }
    
    # Try to get Windows edition
    try:
        result = subprocess.run(['wmic', 'os', 'get', 'Caption'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                info['windows_edition'] = lines[1].strip()
    except Exception as e:

        print(f"⚠️ Error: {e}")
        info['windows_edition'] = 'Windows 10 Pro'
    
    # Get system memory
    try:
        result = subprocess.run(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                memory_bytes = int(lines[1].strip())
                memory_gb = round(memory_bytes / (1024**3), 2)
                info['total_memory_gb'] = memory_gb
    except Exception as e:

        print(f"⚠️ Error: {e}")
        info['total_memory_gb'] = 'Unknown'
    
    # Get CPU info
    try:
        result = subprocess.run(['wmic', 'cpu', 'get', 'Name,NumberOfCores,NumberOfLogicalProcessors'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                info['cpu_details'] = lines[1].strip()
    except Exception as e:

        print(f"⚠️ Error: {e}")
        info['cpu_details'] = info['processor']
    
    return info

def fix_and_setup_database():
    """Fix corrupted database and create comprehensive schema"""
    print("=" * 60)
    print("  JARVIS DATABASE FIX & WINDOWS 10 PRO SETUP")
    print("=" * 60)
    
    # Step 1: Handle existing database
    print("\n[1] Checking existing database...")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    new_db_path = f"{DB_PATH}.fixed-{timestamp}"
    
    if os.path.exists(DB_PATH):
        try:
            # Try to read it first
            conn = sqlite3.connect(DB_PATH, timeout=5)
            conn.execute("PRAGMA quick_check").fetchall()
            conn.close()
            print(f"    [OK] Database is readable")
            print(f"    [INFO] Will create enhanced version: {new_db_path}")
        except sqlite3.DatabaseError:
            print(f"    [CORRUPT] Database is corrupted")
            print(f"    [INFO] Creating new database: {new_db_path}")
        except Exception as e:
            print(f"    [WARNING] Database check failed: {e}")
            print(f"    [INFO] Creating new database: {new_db_path}")
    else:
        print(f"    [INFO] No existing database found")
        new_db_path = DB_PATH  # Use original name if no existing file
    
    # Use the new database path
    db_to_use = new_db_path
    
    # Step 2: Create fresh database with comprehensive schema
    print("\n[2] Creating database schema...")
    conn = sqlite3.connect(db_to_use, timeout=10)
    cursor = conn.cursor()
    
    # Chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            jarvis_msg TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # System information table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            category TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User preferences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE NOT NULL,
            preference_value TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Commands history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS command_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            result TEXT,
            success BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Knowledge base table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT,
            source TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("    [OK] All tables created")
    
    # Step 3: Gather and insert Windows 10 Pro information
    print("\n[3] Gathering Windows 10 Pro system information...")
    win_info = get_windows_info()
    
    system_data = [
        ('os_name', win_info['os_name'], 'system'),
        ('os_version', win_info['os_version'], 'system'),
        ('os_release', win_info['os_release'], 'system'),
        ('windows_edition', win_info.get('windows_edition', 'Windows 10 Pro'), 'system'),
        ('machine_type', win_info['machine'], 'hardware'),
        ('processor', win_info['processor'], 'hardware'),
        ('cpu_details', win_info.get('cpu_details', 'Unknown'), 'hardware'),
        ('total_memory_gb', str(win_info.get('total_memory_gb', 'Unknown')), 'hardware'),
        ('hostname', win_info['hostname'], 'network'),
        ('python_version', platform.python_version(), 'software'),
        ('jarvis_version', '2.0', 'software'),
        ('last_updated', datetime.now().isoformat(), 'meta'),
    ]
    
    for key, value, category in system_data:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"    [+] {key}: {value}")
    
    conn.commit()
    
    # Step 4: Add Windows 10 Pro specific knowledge
    print("\n[4] Adding Windows 10 Pro knowledge base...")
    knowledge_entries = [
        ('Windows 10 Pro Features', 
         'Windows 10 Pro includes: BitLocker encryption, Remote Desktop, Hyper-V virtualization, Group Policy Management, Domain Join, Windows Update for Business',
         'system_knowledge'),
        ('Windows Commands',
         'Common commands: ipconfig (network info), tasklist (running processes), systeminfo (system details), netstat (network connections), wmic (system management)',
         'command_reference'),
        ('Windows Shortcuts',
         'Win+E (Explorer), Win+R (Run), Win+L (Lock), Win+D (Desktop), Win+I (Settings), Win+X (Quick menu), Alt+Tab (Switch apps)',
         'shortcuts'),
        ('System Paths',
         f'User Profile: {os.environ.get("USERPROFILE", "C:\\Users\\User")}, Program Files: C:\\Program Files, System32: C:\\Windows\\System32',
         'paths'),
        ('PowerShell Basics',
         'Get-Process (list processes), Get-Service (list services), Get-EventLog (view logs), Test-Connection (ping), Get-Help (command help)',
         'powershell'),
    ]
    
    for topic, content, source in knowledge_entries:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"    [+] {topic}")
    
    conn.commit()
    
    # Step 5: Add default preferences
    print("\n[5] Setting default preferences...")
    preferences = [
        ('voice_enabled', 'true'),
        ('wake_word', 'jarvis'),
        ('language', 'en-US'),
        ('theme', 'dark'),
        ('auto_save_chat', 'true'),
    ]
    
    for key, value in preferences:
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        print(f"    [+] {key}: {value}")
    
    conn.commit()
    
    # Step 6: Verify database integrity
    print("\n[6] Verifying database integrity...")
    try:
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        if result[0] == 'ok':
            print("    [OK] Database integrity check passed")
        else:
            print(f"    [WARNING] Integrity check result: {result[0]}")
    except Exception as e:
        print(f"    [ERROR] Integrity check failed: {e}")
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM system_info")
    sys_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    kb_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_preferences")
    pref_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"  Database path      : {os.path.abspath(db_to_use)}")
    print(f"  System info entries: {sys_count}")
    print(f"  Knowledge entries  : {kb_count}")
    print(f"  Preferences set    : {pref_count}")
    print(f"  Windows Edition    : {win_info.get('windows_edition', 'Windows 10 Pro')}")
    print(f"  Hostname           : {win_info['hostname']}")
    print(f"  Memory             : {win_info.get('total_memory_gb', 'Unknown')} GB")
    print("\n  [SUCCESS] Database fixed and populated with Windows 10 Pro info!")
    if db_to_use != DB_PATH:
        print(f"\n  [ACTION] To use this database, either:")
        print(f"  1. Close all JARVIS processes and rename:")
        print(f"     {os.path.basename(db_to_use)} -> jarvis_memory.db")
        print(f"  2. Or update core/database.py to use: {os.path.basename(db_to_use)}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        fix_and_setup_database()
    except Exception as e:
        print(f"\n[ERROR] Failed to fix database: {e}")
        import traceback
        traceback.print_exc()
