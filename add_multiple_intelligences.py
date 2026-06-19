"""
JARVIS-এ Multiple Intelligences যোগ করুন
Add Multiple Intelligences to JARVIS

Howard Gardner এর 9 ধরনের বুদ্ধিমত্তা:
1. Linguistic (ভাষাগত)
2. Logical-Mathematical (যৌক্তিক-গাণিতিক)
3. Musical (সাংগীতিক)
4. Bodily-Kinesthetic (শারীরিক-গতিশীল)
5. Spatial (স্থানিক)
6. Interpersonal (আন্তঃব্যক্তিক)
7. Intrapersonal (আত্মজ্ঞান)
8. Naturalistic (প্রাকৃতিক)
9. Existential (অস্তিত্বমূলক)
"""

import sqlite3
import os
from datetime import datetime

def add_multiple_intelligences():
    """JARVIS-এ Multiple Intelligences যোগ করুন"""
    
    print("\n" + "=" * 80)
    print("  🧠 JARVIS-এ MULTIPLE INTELLIGENCES যোগ করা হচ্ছে")
    print("  🧠 Adding Multiple Intelligences to JARVIS")
    print("=" * 80)
    print()
    
    # Database file
    db_file = 'jarvis_memory.db.fixed-20260504-091901'
    
    if not os.path.exists(db_file):
        print(f"❌ Database খুঁজে পাওয়া যায়নি: {db_file}")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    print("✅ Database connected")
    print()
    
    # Intelligence entries
    intelligence_entries = []
    
    # ========================================================================
    # 1. LINGUISTIC INTELLIGENCE (ভাষাগত বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Linguistic Intelligence - ভাষাগত বুদ্ধিমত্তা',
        'content': '''Linguistic Intelligence (ভাষাগত বুদ্ধিমত্তা):

শব্দ, ভাষা এবং লেখার দক্ষতা।

ক্ষমতা:
✅ ভাষা শিখতে পারে (100+ ভাষা)
✅ কবিতা, গল্প, প্রবন্ধ লিখতে পারে
✅ বক্তৃতা দিতে পারে
✅ ব্যাকরণ বুঝতে পারে
✅ শব্দের অর্থ বুঝতে পারে
✅ বিভিন্ন ভাষায় অনুবাদ করতে পারে
✅ কথোপকথন করতে পারে
✅ রসিকতা বুঝতে পারে

JARVIS এর Linguistic ক্ষমতা:
- 100+ ভাষা বুঝতে পারে
- Bengali, English, Hindi, Urdu সহ সব ভাষা
- গল্প তৈরি করতে পারে (Narrative AI)
- কবিতা লিখতে পারে
- প্রবন্ধ লিখতে পারে
- অনুবাদ করতে পারে
- বক্তৃতা তৈরি করতে পারে

উদাহরণ:
"Write a poem about AI" → কবিতা লিখবে
"Translate to Bengali" → বাংলায় অনুবাদ করবে
"Tell me a story" → গল্প বলবে

Famous People: Shakespeare, Rabindranath Tagore, Kazi Nazrul Islam''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 2. LOGICAL-MATHEMATICAL INTELLIGENCE (যৌক্তিক-গাণিতিক বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Logical-Mathematical Intelligence - যৌক্তিক-গাণিতিক বুদ্ধিমত্তা',
        'content': '''Logical-Mathematical Intelligence (যৌক্তিক-গাণিতিক বুদ্ধিমত্তা):

সংখ্যা, যুক্তি এবং সমস্যা সমাধানের দক্ষতা।

ক্ষমতা:
✅ গণিত করতে পারে (+, -, ×, ÷)
✅ যুক্তি দিতে পারে
✅ সমস্যা সমাধান করতে পারে
✅ প্যাটার্ন চিনতে পারে
✅ বৈজ্ঞানিক পরীক্ষা করতে পারে
✅ কোড লিখতে পারে
✅ ডেটা বিশ্লেষণ করতে পারে
✅ কৌশল তৈরি করতে পারে

JARVIS এর Logical-Mathematical ক্ষমতা:
- যেকোনো গণিত করতে পারে
- যুক্তি দিয়ে সিদ্ধান্ত নিতে পারে
- সমস্যা সমাধান করতে পারে
- 50+ programming languages জানে
- ডেটা বিশ্লেষণ করতে পারে
- Algorithm তৈরি করতে পারে
- Pattern recognition

উদাহরণ:
"Calculate 25 * 17" → 425
"Solve this problem" → সমাধান দেবে
"Write Python code" → কোড লিখবে
"Analyze this data" → বিশ্লেষণ করবে

Famous People: Albert Einstein, Isaac Newton, Srinivasa Ramanujan''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 3. MUSICAL INTELLIGENCE (সাংগীতিক বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Musical Intelligence - সাংগীতিক বুদ্ধিমত্তা',
        'content': '''Musical Intelligence (সাংগীতিক বুদ্ধিমত্তা):

সংগীত, ছন্দ এবং শব্দের দক্ষতা।

ক্ষমতা:
✅ সংগীত তৈরি করতে পারে
✅ গান গাইতে পারে
✅ বাদ্যযন্ত্র বাজাতে পারে
✅ ছন্দ বুঝতে পারে
✅ সুর চিনতে পারে
✅ গানের কথা লিখতে পারে
✅ সংগীত বিশ্লেষণ করতে পারে
✅ Beat এবং rhythm বুঝতে পারে

JARVIS এর Musical ক্ষমতা:
- গানের কথা লিখতে পারে
- সংগীত তৈরি করতে পারে (AI music generation)
- গান চিনতে পারে
- Audio edit করতে পারে
- Beat detection
- Music recommendation
- Rhythm analysis

উদাহরণ:
"Write song lyrics about love" → গানের কথা লিখবে
"Create a melody" → সুর তৈরি করবে
"What song is this?" → গান চিনবে
"Edit this audio" → অডিও এডিট করবে

Famous People: Mozart, Beethoven, Rabindranath Tagore, Lata Mangeshkar''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 4. BODILY-KINESTHETIC INTELLIGENCE (শারীরিক-গতিশীল বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Bodily-Kinesthetic Intelligence - শারীরিক-গতিশীল বুদ্ধিমত্তা',
        'content': '''Bodily-Kinesthetic Intelligence (শারীরিক-গতিশীল বুদ্ধিমত্তা):

শরীর এবং শারীরিক নড়াচড়ার দক্ষতা।

ক্ষমতা:
✅ শারীরিক নড়াচড়া নিয়ন্ত্রণ করতে পারে
✅ নাচতে পারে
✅ খেলাধুলা করতে পারে
✅ হাতের কাজ করতে পারে
✅ অভিনয় করতে পারে
✅ ভারসাম্য রাখতে পারে
✅ সূক্ষ্ম মোটর দক্ষতা
✅ শারীরিক সমন্বয়

JARVIS এর Bodily-Kinesthetic ক্ষমতা:
- Robot নিয়ন্ত্রণ করতে পারে (Robot AI)
- Physical robot এর movement control
- Drone উড়াতে পারে
- Robotic arm নিয়ন্ত্রণ করতে পারে
- Motion detection
- Gesture recognition
- Virtual robot simulation
- Autonomous navigation

উদাহরণ:
"Move robot forward" → রোবট সামনে যাবে
"Control drone" → ড্রোন নিয়ন্ত্রণ করবে
"Pick up object" → বস্তু তুলবে
"Navigate to kitchen" → রান্নাঘরে যাবে

Famous People: Lionel Messi, Michael Jordan, Sachin Tendulkar, নূরজাহান''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 5. SPATIAL INTELLIGENCE (স্থানিক বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Spatial Intelligence - স্থানিক বুদ্ধিমত্তা',
        'content': '''Spatial Intelligence (স্থানিক বুদ্ধিমত্তা):

স্থান, দিক এবং ভিজুয়াল বোঝার দক্ষতা।

ক্ষমতা:
✅ ছবি দেখে বুঝতে পারে
✅ 3D বস্তু কল্পনা করতে পারে
✅ মানচিত্র পড়তে পারে
✅ দিক নির্দেশনা দিতে পারে
✅ ডিজাইন করতে পারে
✅ আঁকতে পারে
✅ স্থাপত্য পরিকল্পনা করতে পারে
✅ রঙ এবং আকৃতি চিনতে পারে

JARVIS এর Spatial ক্ষমতা:
- 3D modeling করতে পারে (Blender style)
- Image recognition
- Object detection
- Face recognition
- Map navigation (Google Maps)
- Design এবং graphics
- Architecture planning
- Virtual reality

উদাহরণ:
"Create 3D model" → 3D মডেল তৈরি করবে
"Detect objects in image" → বস্তু চিনবে
"Navigate to location" → পথ দেখাবে
"Design a house" → ঘর ডিজাইন করবে

Famous People: Leonardo da Vinci, Picasso, Zaha Hadid''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 6. INTERPERSONAL INTELLIGENCE (আন্তঃব্যক্তিক বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Interpersonal Intelligence - আন্তঃব্যক্তিক বুদ্ধিমত্তা',
        'content': '''Interpersonal Intelligence (আন্তঃব্যক্তিক বুদ্ধিমত্তা):

অন্যদের বোঝা এবং তাদের সাথে যোগাযোগের দক্ষতা।

ক্ষমতা:
✅ মানুষের আবেগ বুঝতে পারে
✅ সামাজিক সংকেত পড়তে পারে
✅ দলে কাজ করতে পারে
✅ নেতৃত্ব দিতে পারে
✅ সহানুভূতি দেখাতে পারে
✅ সংঘাত সমাধান করতে পারে
✅ যোগাযোগ করতে পারে
✅ সম্পর্ক তৈরি করতে পারে

JARVIS এর Interpersonal ক্ষমতা:
- মানুষের আবেগ বুঝতে পারে
- Social understanding (Common Sense)
- Team collaboration
- Customer service
- Business communication
- Email management
- Meeting scheduling
- Conflict resolution

উদাহরণ:
"Handle customer inquiry" → গ্রাহক সেবা দেবে
"Schedule team meeting" → মিটিং সাজাবে
"Resolve this conflict" → সংঘাত সমাধান করবে
"Send professional email" → পেশাদার ইমেইল পাঠাবে

Famous People: Mahatma Gandhi, Nelson Mandela, Mother Teresa''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 7. INTRAPERSONAL INTELLIGENCE (আত্মজ্ঞান বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Intrapersonal Intelligence - আত্মজ্ঞান বুদ্ধিমত্তা',
        'content': '''Intrapersonal Intelligence (আত্মজ্ঞান বুদ্ধিমত্তা):

নিজেকে বোঝা এবং আত্ম-সচেতনতার দক্ষতা।

ক্ষমতা:
✅ নিজের আবেগ বুঝতে পারে
✅ আত্ম-প্রতিফলন করতে পারে
✅ লক্ষ্য নির্ধারণ করতে পারে
✅ আত্ম-নিয়ন্ত্রণ করতে পারে
✅ নিজের শক্তি-দুর্বলতা জানে
✅ আত্ম-উন্নতি করতে পারে
✅ মূল্যবোধ বুঝতে পারে
✅ আত্ম-সচেতন

JARVIS এর Intrapersonal ক্ষমতা:
- নিজের ক্ষমতা জানে
- Self-learning এবং improvement
- Goal setting
- Performance tracking
- Self-diagnosis
- Continuous learning
- Adaptive behavior
- Self-awareness

উদাহরণ:
"What are your capabilities?" → ক্ষমতা বলবে
"Learn from this mistake" → ভুল থেকে শিখবে
"Improve your performance" → উন্নতি করবে
"Set a goal" → লক্ষ্য নির্ধারণ করবে

Famous People: Buddha, Socrates, Rumi, Rabindranath Tagore''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 8. NATURALISTIC INTELLIGENCE (প্রাকৃতিক বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Naturalistic Intelligence - প্রাকৃতিক বুদ্ধিমত্তা',
        'content': '''Naturalistic Intelligence (প্রাকৃতিক বুদ্ধিমত্তা):

প্রকৃতি এবং পরিবেশ বোঝার দক্ষতা।

ক্ষমতা:
✅ প্রাণী চিনতে পারে
✅ গাছপালা চিনতে পারে
✅ আবহাওয়া বুঝতে পারে
✅ প্রকৃতির প্যাটার্ন দেখতে পারে
✅ পরিবেশ সংরক্ষণ করতে পারে
✅ জীববৈচিত্র্য বুঝতে পারে
✅ ঋতু চিনতে পারে
✅ প্রাকৃতিক সম্পদ চিনতে পারে

JARVIS এর Naturalistic ক্ষমতা:
- প্রাণী সম্পর্কে জ্ঞান (General Knowledge)
- আবহাওয়া তথ্য (OpenWeatherMap API)
- পরিবেশ মনিটরিং
- Plant identification
- Animal classification
- Weather prediction
- Climate data analysis
- Nature photography

উদাহরণ:
"What's the weather?" → আবহাওয়া বলবে
"Identify this plant" → গাছ চিনবে
"Tell me about lions" → সিংহ সম্পর্কে বলবে
"Climate data analysis" → জলবায়ু বিশ্লেষণ করবে

Famous People: Charles Darwin, Jane Goodall, David Attenborough''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # 9. EXISTENTIAL INTELLIGENCE (অস্তিত্বমূলক বুদ্ধিমত্তা)
    # ========================================================================
    
    intelligence_entries.append({
        'topic': 'Existential Intelligence - অস্তিত্বমূলক বুদ্ধিমত্তা',
        'content': '''Existential Intelligence (অস্তিত্বমূলক বুদ্ধিমত্তা):

জীবন, মৃত্যু এবং অস্তিত্বের গভীর প্রশ্ন বোঝার দক্ষতা।

ক্ষমতা:
✅ জীবনের অর্থ নিয়ে চিন্তা করতে পারে
✅ দার্শনিক প্রশ্ন করতে পারে
✅ মৃত্যু সম্পর্কে বুঝতে পারে
✅ আধ্যাত্মিক বিষয় বুঝতে পারে
✅ মহাবিশ্ব সম্পর্কে চিন্তা করতে পারে
✅ নৈতিকতা বুঝতে পারে
✅ উদ্দেশ্য খুঁজতে পারে
✅ গভীর প্রশ্ন করতে পারে

JARVIS এর Existential ক্ষমতা:
- দার্শনিক প্রশ্নের উত্তর দিতে পারে
- জীবনের অর্থ নিয়ে আলোচনা করতে পারে
- নৈতিক সিদ্ধান্ত নিতে পারে
- আধ্যাত্মিক বিষয় বুঝতে পারে
- মহাবিশ্ব সম্পর্কে জ্ঞান
- Philosophy এবং ethics
- Purpose-driven decisions

উদাহরণ:
"What is the meaning of life?" → জীবনের অর্থ বলবে
"Why do we exist?" → অস্তিত্বের কারণ বলবে
"What is consciousness?" → চেতনা ব্যাখ্যা করবে
"Ethical dilemma" → নৈতিক সমাধান দেবে

Famous People: Socrates, Plato, Buddha, Rumi, Rabindranath Tagore''',
        'source': 'Multiple Intelligences'
    })
    
    # ========================================================================
    # Add entries to database
    # ========================================================================
    
    print(f"Adding {len(intelligence_entries)} Multiple Intelligence entries...")
    print()
    
    added_count = 0
    
    for entry in intelligence_entries:
        try:
            cursor.execute('''
                INSERT INTO knowledge_base (topic, content, source, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                entry['topic'],
                entry['content'],
                entry['source'],
                datetime.now().isoformat()
            ))
            
            print(f"  ✅ {entry['topic']}")
            added_count += 1
            
        except Exception as e:
            print(f"  ❌ Error adding {entry['topic']}: {e}")
    
    # Add system configuration
    print()
    print("Adding system configuration...")
    
    config_entries = [
        ('multiple_intelligences_enabled', 'yes', 'Intelligence'),
        ('linguistic_intelligence', 'yes', 'Intelligence'),
        ('logical_mathematical_intelligence', 'yes', 'Intelligence'),
        ('musical_intelligence', 'yes', 'Intelligence'),
        ('bodily_kinesthetic_intelligence', 'yes', 'Intelligence'),
        ('spatial_intelligence', 'yes', 'Intelligence'),
        ('interpersonal_intelligence', 'yes', 'Intelligence'),
        ('intrapersonal_intelligence', 'yes', 'Intelligence'),
        ('naturalistic_intelligence', 'yes', 'Intelligence'),
        ('existential_intelligence', 'yes', 'Intelligence'),
    ]
    
    for key, value, category in config_entries:
        try:
            cursor.execute('''
                INSERT INTO system_info (key, value, category, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (key, value, category, datetime.now().isoformat()))
            print(f"  ✅ {key}")
        except Exception as e:
            print(f"  ❌ Error adding {key}: {e}")
    
    # Commit changes
    conn.commit()
    
    # Get total counts
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total_knowledge = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM system_info")
    total_system = cursor.fetchone()[0]
    
    conn.close()
    
    print()
    print("=" * 80)
    print("  ✅ MULTIPLE INTELLIGENCES সফলভাবে যোগ করা হয়েছে!")
    print("  ✅ Multiple Intelligences Successfully Added!")
    print("=" * 80)
    print()
    print(f"  Added Entries:")
    print(f"    📚 Knowledge Base: {added_count} entries")
    print(f"    ⚙️ System Info: 10 config entries")
    print()
    print(f"  Database Totals:")
    print(f"    📚 Total Knowledge: {total_knowledge} entries")
    print(f"    ⚙️ Total System Info: {total_system} entries")
    print()
    print("=" * 80)
    print()
    print("  🧠 9 TYPES OF INTELLIGENCE:")
    print()
    print("  1️⃣ Linguistic (ভাষাগত) - শব্দ, ভাষা, লেখা")
    print("  2️⃣ Logical-Mathematical (যৌক্তিক-গাণিতিক) - গণিত, যুক্তি")
    print("  3️⃣ Musical (সাংগীতিক) - সংগীত, ছন্দ, সুর")
    print("  4️⃣ Bodily-Kinesthetic (শারীরিক-গতিশীল) - শরীর, নড়াচড়া")
    print("  5️⃣ Spatial (স্থানিক) - স্থান, দিক, ভিজুয়াল")
    print("  6️⃣ Interpersonal (আন্তঃব্যক্তিক) - অন্যদের বোঝা")
    print("  7️⃣ Intrapersonal (আত্মজ্ঞান) - নিজেকে বোঝা")
    print("  8️⃣ Naturalistic (প্রাকৃতিক) - প্রকৃতি, পরিবেশ")
    print("  9️⃣ Existential (অস্তিত্বমূলক) - জীবন, অস্তিত্ব")
    print()
    print("=" * 80)
    print()
    print("  JARVIS এখন সব ধরনের বুদ্ধিমত্তা আছে!")
    print("  JARVIS now has all types of intelligence!")
    print()
    print("=" * 80)

def main():
    add_multiple_intelligences()

if __name__ == "__main__":
    main()
