"""
View JARVIS Database Contents
Shows all information stored in jarvis_memory.db
"""
import sqlite3
import os
import glob

def view_database(db_path):
    """Display all database contents in a readable format"""
    print("=" * 70)
    print(f"  JARVIS DATABASE VIEWER: {os.path.basename(db_path)}")
    print("=" * 70)
    
    if not os.path.exists(db_path):
        print(f"\n[ERROR] Database not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path, timeout=5)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        if not tables:
            print("\n[INFO] Database is empty (no tables)")
            return
        
        print(f"\n[INFO] Database contains {len(tables)} tables\n")
        
        # Display each table
        for (table_name,) in tables:
            print("=" * 70)
            print(f"TABLE: {table_name}")
            print("=" * 70)
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Total rows: {count}\n")
            
            if count == 0:
                print("  (empty table)\n")
                continue
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            col_names = [col[1] for col in columns]
            
            # Get all rows
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Display data
            if table_name == 'system_info':
                print(f"{'Key':<25} {'Value':<30} {'Category':<15}")
                print("-" * 70)
                for row in rows:
                    key = str(row[1])[:24]
                    value = str(row[2])[:29]
                    category = str(row[3])[:14] if len(row) > 3 else ''
                    print(f"{key:<25} {value:<30} {category:<15}")
            
            elif table_name == 'knowledge_base':
                for i, row in enumerate(rows, 1):
                    print(f"\n[{i}] Topic: {row[1]}")
                    print(f"    Content: {row[2][:100]}...")
                    print(f"    Source: {row[3]}")
            
            elif table_name == 'user_preferences':
                print(f"{'Preference':<30} {'Value':<30}")
                print("-" * 60)
                for row in rows:
                    pref = str(row[1])[:29]
                    value = str(row[2])[:29]
                    print(f"{pref:<30} {value:<30}")
            
            elif table_name == 'chat_history':
                for i, row in enumerate(rows, 1):
                    print(f"\n[{i}] {row[4] if len(row) > 4 else 'No timestamp'}")
                    print(f"    User: {row[1][:60]}...")
                    print(f"    Jarvis: {row[2][:60]}...")
            
            elif table_name == 'command_history':
                print(f"{'Command':<40} {'Success':<10} {'Timestamp':<20}")
                print("-" * 70)
                for row in rows:
                    cmd = str(row[1])[:39]
                    success = 'Yes' if row[3] else 'No'
                    timestamp = str(row[4])[:19] if len(row) > 4 else ''
                    print(f"{cmd:<40} {success:<10} {timestamp:<20}")
            
            else:
                # Generic display for unknown tables
                print(f"Columns: {', '.join(col_names)}")
                print("-" * 70)
                for row in rows[:10]:  # Show first 10 rows
                    print(row)
                if len(rows) > 10:
                    print(f"... and {len(rows) - 10} more rows")
            
            print()
        
        conn.close()
        
        print("=" * 70)
        print("  END OF DATABASE")
        print("=" * 70)
        
    except sqlite3.DatabaseError as e:
        print(f"\n[ERROR] Database is corrupted: {e}")
        print("Run: python fix_database_windows10.py to fix it")
    except Exception as e:
        print(f"\n[ERROR] Failed to read database: {e}")

if __name__ == "__main__":
    # Check for main database
    main_db = "jarvis_memory.db"
    
    # Also check for fixed databases
    fixed_dbs = glob.glob("jarvis_memory.db.fixed-*")
    
    print("\nAvailable databases:")
    print(f"1. {main_db} {'(exists)' if os.path.exists(main_db) else '(not found)'}")
    
    if fixed_dbs:
        fixed_dbs.sort(reverse=True)
        for i, db in enumerate(fixed_dbs[:3], 2):  # Show up to 3 most recent
            print(f"{i}. {db}")
    
    print("\nViewing main database...\n")
    
    if os.path.exists(main_db):
        view_database(main_db)
    elif fixed_dbs:
        print(f"Main database not found, viewing: {fixed_dbs[0]}\n")
        view_database(fixed_dbs[0])
    else:
        print("[ERROR] No database found!")
        print("Run: python fix_database_windows10.py to create one")
