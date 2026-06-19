import sqlite3
DB_PATH = "jarvis_memory.db.fixed-20260504-091901"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

training = [
    ("Python Programming", "Python is a high-level programming language. Easy syntax, used for web, AI, data science. পাইথন সহজ প্রোগ্রামিং ভাষা।", "Auto Training"),
    ("JavaScript", "JavaScript is for web development. Runs in browsers and Node.js. জাভাস্ক্রিপ্ট ওয়েব ডেভেলপমেন্টের জন্য।", "Auto Training"),
    ("Machine Learning", "ML is AI where computers learn from data. Used for predictions, image recognition. মেশিন লার্নিং ডেটা থেকে শেখে।", "Auto Training"),
    ("Cloud Computing", "Cloud delivers computing services over internet. AWS, Azure, Google Cloud. ক্লাউড ইন্টারনেটে সেবা দেয়।", "Auto Training"),
    ("Git Version Control", "Git tracks code changes. Commands: commit, push, pull, branch. গিট কোড ট্র্যাক করে।", "Auto Training"),
    ("Bangladesh", "Bangladesh is in South Asia. 170 million people. Capital: Dhaka. বাংলাদেশ দক্ষিণ এশিয়ার দেশ।", "Auto Training"),
    ("HTML", "HTML is markup language for web pages. Uses tags and elements. এইচটিএমএল ওয়েব পেজ তৈরি করে।", "Auto Training"),
    ("CSS", "CSS styles web pages. Controls colors, fonts, layout. সিএসএস ওয়েব পেজ সাজায়।", "Auto Training"),
    ("SQL Database", "SQL manages relational databases. Commands: SELECT, INSERT, UPDATE, DELETE. এসকিউএল ডাটাবেস পরিচালনা করে।", "Auto Training"),
    ("Cybersecurity", "Cybersecurity protects systems from attacks. Includes encryption, firewalls, authentication. সাইবার নিরাপত্তা সিস্টেম রক্ষা করে।", "Auto Training")
]

added = 0
for topic, content, source in training:
    try:
        cursor.execute("INSERT INTO knowledge_base (topic, content, source) VALUES (?, ?, ?)", (topic, content, source))
        added += 1
        print(f"✅ {topic}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

conn.commit()
cursor.execute("SELECT COUNT(*) FROM knowledge_base")
total = cursor.fetchone()[0]
conn.close()

print(f"\n✅ Added {added} entries! Total: {total}")
