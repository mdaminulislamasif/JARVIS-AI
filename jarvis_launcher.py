"""
JARVIS - Portable AI Assistant
Can be copied and run on any Windows computer
"""
import os
import sys
import subprocess
import sqlite3
from pathlib import Path

# Get the directory where the exe is located
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up paths
DB_PATH = os.path.join(BASE_DIR, 'jarvis_memory.db')
CONFIG_PATH = os.path.join(BASE_DIR, 'jarvis_config.txt')

def check_database():
    """Check if database exists and is valid"""
    if not os.path.exists(DB_PATH):
        print("⚠️  Database not found. Creating new database...")
        create_database()
        return True
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        conn.execute("PRAGMA quick_check").fetchall()
        conn.close()
        return True
    except Exception as e:

        print(f"⚠️ Error: {e}")
        print("⚠️  Database corrupted. Creating new database...")
        os.rename(DB_PATH, DB_PATH + '.backup')
        create_database()
        return True

def create_database():
    """Create a fresh database with basic schema"""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            jarvis_msg TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            category TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT,
            source TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE NOT NULL,
            preference_value TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add basic system info
    import platform
    cursor.execute("INSERT OR REPLACE INTO system_info (key, value, category) VALUES (?, ?, ?)",
                   ('os_name', platform.system(), 'system'))
    cursor.execute("INSERT OR REPLACE INTO system_info (key, value, category) VALUES (?, ?, ?)",
                   ('hostname', platform.node(), 'system'))
    cursor.execute("INSERT OR REPLACE INTO system_info (key, value, category) VALUES (?, ?, ?)",
                   ('jarvis_version', '2.0 Portable', 'software'))
    
    conn.commit()
    conn.close()
    print("✅ Database created successfully")

def check_config():
    """Check if config file exists"""
    if not os.path.exists(CONFIG_PATH):
        print("⚠️  Config file not found. Creating default config...")
        with open(CONFIG_PATH, 'w') as f:
            f.write("# JARVIS Configuration\n")
            f.write("# Add your API keys here (one per line)\n")
            f.write("# Example: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        print("✅ Config file created. Please add your API keys.")
        return False
    return True

def main():
    """Main JARVIS launcher"""
    print("=" * 70)
    print("  JARVIS - Portable AI Assistant")
    print("  পোর্টেবল AI সহায়ক")
    print("=" * 70)
    print(f"\nRunning from: {BASE_DIR}")
    print(f"Database: {DB_PATH}")
    print(f"Config: {CONFIG_PATH}\n")
    
    # Check database
    print("[1/3] Checking database...")
    check_database()
    
    # Check config
    print("\n[2/3] Checking configuration...")
    if not check_config():
        print("\n⚠️  Please edit jarvis_config.txt and add your API keys")
        print("    Then run JARVIS again.\n")
        input("Press Enter to exit...")
        return
    
    # Check if main JARVIS script exists
    print("\n[3/3] Starting JARVIS...")
    
    # Try to import and run JARVIS
    try:
        # Add current directory to path
        sys.path.insert(0, BASE_DIR)
        
        # Check if core modules exist
        core_path = os.path.join(BASE_DIR, 'core')
        if os.path.exists(core_path):
            print("✅ Core modules found")
            
            # Import and run JARVIS
            try:
                from core import brain
                print("\n" + "=" * 70)
                print("  JARVIS STARTED SUCCESSFULLY!")
                print("  JARVIS সফলভাবে চালু হয়েছে!")
                print("=" * 70)
                print("\nType 'exit' or 'quit' to stop JARVIS\n")
                
                # Simple chat loop
                # WARNING: Infinite loop - ensure break condition exists
                while True:
                    user_input = input("You: ")
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        print("\nJARVIS: Goodbye! আবার দেখা হবে!\n")
                        break
                    
                    # Process with JARVIS brain
                    response = brain.process_query(user_input)
                    print(f"JARVIS: {response}\n")
                    
            except ImportError as e:
                print(f"❌ Error importing JARVIS modules: {e}")
                print("\nPlease ensure all JARVIS files are in the same folder as the .exe")
        else:
            print("❌ Core modules not found")
            print("\nPlease ensure the 'core' folder is in the same directory as JARVIS.exe")
            print("\nRequired structure:")
            print("  JARVIS.exe")
            print("  jarvis_memory.db")
            print("  jarvis_config.txt")
            print("  core/")
            print("    brain.py")
            print("    database.py")
            print("    auth.py")
            print("  engine/")
            print("    (other modules)")
    
    except Exception as e:
        print(f"\n❌ Error starting JARVIS: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
