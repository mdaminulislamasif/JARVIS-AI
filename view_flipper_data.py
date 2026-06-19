"""View Flipper Zero data in the database"""
import sqlite3
import glob

# Find the fixed database
fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
fixed_dbs.sort(reverse=True)
db_path = fixed_dbs[0] if fixed_dbs else 'jarvis_memory.db'

print("=" * 80)
print("  FLIPPER ZERO DATABASE CONTENTS")
print("=" * 80)
print(f"\nDatabase: {db_path}\n")

conn = sqlite3.connect(db_path, timeout=5)
cursor = conn.cursor()

# Flipper System Info
print("=" * 80)
print("FLIPPER ZERO SYSTEM INFORMATION")
print("=" * 80)
cursor.execute("SELECT key, value, category FROM system_info WHERE key LIKE 'flipper%' ORDER BY key")
flipper_sys = cursor.fetchall()
for key, value, category in flipper_sys:
    print(f"  {key:<30} {value:<40} [{category}]")

# Flipper Knowledge Base
print("\n" + "=" * 80)
print("FLIPPER ZERO KNOWLEDGE BASE")
print("=" * 80)
cursor.execute("SELECT topic, content, source FROM knowledge_base WHERE source LIKE 'flipper%' ORDER BY topic")
flipper_kb = cursor.fetchall()
for i, (topic, content, source) in enumerate(flipper_kb, 1):
    print(f"\n[{i}] {topic}")
    print(f"    Source: {source}")
    print(f"    Content: {content[:150]}...")

# Flipper Preferences
print("\n" + "=" * 80)
print("FLIPPER ZERO PREFERENCES")
print("=" * 80)
cursor.execute("SELECT preference_key, preference_value FROM user_preferences WHERE preference_key LIKE 'flipper%'")
flipper_prefs = cursor.fetchall()
for key, value in flipper_prefs:
    print(f"  {key:<35} {value}")

# Statistics
cursor.execute("SELECT COUNT(*) FROM system_info WHERE key LIKE 'flipper%'")
sys_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source LIKE 'flipper%'")
kb_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM user_preferences WHERE preference_key LIKE 'flipper%'")
pref_count = cursor.fetchone()[0]

print("\n" + "=" * 80)
print("STATISTICS")
print("=" * 80)
print(f"  Flipper System Info Entries: {sys_count}")
print(f"  Flipper Knowledge Entries:   {kb_count}")
print(f"  Flipper Preferences:         {pref_count}")
print(f"  Total Flipper Data:          {sys_count + kb_count + pref_count}")
print("=" * 80)

conn.close()
