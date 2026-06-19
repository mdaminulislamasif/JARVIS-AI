"""
Replace old jarvis_memory.db with the fixed version
Run this after closing all JARVIS processes
"""
import os
import glob
import time

print("=" * 60)
print("  JARVIS DATABASE REPLACEMENT TOOL")
print("=" * 60)

# Find the most recent fixed database
fixed_dbs = glob.glob("jarvis_memory.db.fixed-*")
if not fixed_dbs:
    print("\n[ERROR] No fixed database found!")
    print("Please run: python fix_database_windows10.py first")
    exit(1)

# Sort by timestamp (newest first)
fixed_dbs.sort(reverse=True)
newest_fixed = fixed_dbs[0]

print(f"\n[INFO] Found fixed database: {newest_fixed}")
print(f"[INFO] Target: jarvis_memory.db")

# Check if old database is locked
old_db = "jarvis_memory.db"
if os.path.exists(old_db):
    print(f"\n[WARNING] Old database exists")
    print("[INFO] Attempting to replace...")
    
    # Try to rename old database
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    old_backup = f"jarvis_memory.db.old-{timestamp}"
    
    try:
        os.rename(old_db, old_backup)
        print(f"[OK] Old database backed up to: {old_backup}")
    except PermissionError:
        print(f"\n[ERROR] Cannot replace database - file is in use!")
        print("\nPlease:")
        print("1. Close all JARVIS processes")
        print("2. Close any database browsers or SQLite tools")
        print("3. Run this script again")
        exit(1)

# Copy fixed database to main location
try:
    import shutil
    shutil.copy2(newest_fixed, old_db)
    print(f"\n[SUCCESS] Database replaced successfully!")
    print(f"[INFO] New database: {old_db}")
    print(f"[INFO] Backup kept: {newest_fixed}")
    
    # Verify the new database
    import sqlite3
    conn = sqlite3.connect(old_db, timeout=5)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n[VERIFY] Database contains {len(tables)} tables:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count} rows")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("  DATABASE REPLACEMENT COMPLETE!")
    print("  You can now start JARVIS")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] Failed to replace database: {e}")
    exit(1)
