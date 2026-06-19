"""View Cyber Attack Menu and Memory in the database"""
import sqlite3
import glob

# Find the fixed database
fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
fixed_dbs.sort(reverse=True)
db_path = fixed_dbs[0] if fixed_dbs else 'jarvis_memory.db'

print("=" * 90)
print("  CYBER ATTACK MENU & MEMORY - DATABASE CONTENTS")
print("=" * 90)
print(f"\nDatabase: {db_path}\n")
print("⚠️  FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY\n")

conn = sqlite3.connect(db_path, timeout=5)
cursor = conn.cursor()

# Cyber System Info
print("=" * 90)
print("CYBER ATTACK SYSTEM INFORMATION")
print("=" * 90)
cursor.execute("SELECT key, value, category FROM system_info WHERE category = 'security' ORDER BY key")
cyber_sys = cursor.fetchall()
for key, value, category in cyber_sys:
    print(f"  {key:<35} {value:<45} [{category}]")

# Attack Categories
print("\n" + "=" * 90)
print("ATTACK CATEGORIES")
print("=" * 90)

categories = [
    ('Network Attacks', 'cyber_network_attacks'),
    ('Web Application Attacks', 'cyber_web_attacks'),
    ('Social Engineering', 'cyber_social_engineering'),
    ('Malware', 'cyber_malware'),
    ('Password Attacks', 'cyber_password_attacks'),
    ('Wireless Attacks', 'cyber_wireless_attacks'),
    ('Advanced Persistent Threats', 'cyber_apt'),
    ('Exploitation Frameworks', 'cyber_exploitation'),
    ('Reconnaissance', 'cyber_reconnaissance'),
    ('Privilege Escalation', 'cyber_privilege_escalation'),
    ('Persistence', 'cyber_persistence'),
    ('Defense & Mitigation', 'cyber_defense'),
    ('Penetration Testing', 'cyber_pentest'),
    ('Security Frameworks', 'cyber_frameworks'),
    ('Security Tools', 'cyber_tools'),
    ('Legal & Ethics', 'cyber_legal'),
]

for category_name, source_filter in categories:
    cursor.execute("SELECT topic, content FROM knowledge_base WHERE source = ? ORDER BY topic", (source_filter,))
    attacks = cursor.fetchall()
    
    if attacks:
        print(f"\n{'─' * 90}")
        print(f"📁 {category_name.upper()} ({len(attacks)} entries)")
        print(f"{'─' * 90}")
        
        for i, (topic, content) in enumerate(attacks, 1):
            print(f"\n[{i}] {topic}")
            # Show first 200 characters
            preview = content[:200] + "..." if len(content) > 200 else content
            print(f"    {preview}")

# Cyber Preferences
print("\n" + "=" * 90)
print("CYBER ATTACK PREFERENCES")
print("=" * 90)
cursor.execute("SELECT preference_key, preference_value FROM user_preferences WHERE preference_key LIKE 'cyber_%' OR preference_key LIKE '%security%' OR preference_key LIKE '%ethical%'")
cyber_prefs = cursor.fetchall()
for key, value in cyber_prefs:
    print(f"  {key:<40} {value}")

# Statistics
cursor.execute("SELECT COUNT(*) FROM system_info WHERE category = 'security'")
sys_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source LIKE 'cyber_%'")
kb_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM user_preferences WHERE preference_key LIKE 'cyber_%' OR preference_key LIKE '%security%' OR preference_key LIKE '%ethical%'")
pref_count = cursor.fetchone()[0]

print("\n" + "=" * 90)
print("STATISTICS")
print("=" * 90)
print(f"  Cyber System Info Entries: {sys_count}")
print(f"  Cyber Knowledge Entries:   {kb_count}")
print(f"  Cyber Preferences:         {pref_count}")
print(f"  Total Cyber Attack Data:   {sys_count + kb_count + pref_count}")

# Attack type breakdown
print("\n  Attack Type Breakdown:")
for category_name, source_filter in categories:
    cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source = ?", (source_filter,))
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"    • {category_name:<30} {count} entries")

print("\n" + "=" * 90)
print("⚠️  LEGAL WARNING")
print("=" * 90)
print("  This information is for EDUCATIONAL and DEFENSIVE purposes ONLY.")
print("  Unauthorized access to computer systems is ILLEGAL.")
print("  Always obtain written authorization before security testing.")
print("=" * 90)

conn.close()
