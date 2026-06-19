#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Knowledge Types and Human Senses to JARVIS Database
জ্ঞানের ধরন এবং মানুষের ইন্দ্রিয় যোগ করা হচ্ছে
"""

import sqlite3
import os

# Database path
DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

def add_knowledge_and_senses():
    """Add all knowledge types and human senses to database"""
    
    print("\n" + "="*80)
    print("  🧠 JARVIS-এ KNOWLEDGE TYPES এবং HUMAN SENSES যোগ করা হচ্ছে")
    print("  🧠 Adding Knowledge Types and Human Senses to JARVIS")
    print("="*80 + "\n")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("✅ Database connected\n")
    
    # ==================== KNOWLEDGE TYPES ====================
    
    knowledge_types = [
        # 1. General Types (Philosophy)
        {
            "category": "knowledge_type",
            "subcategory": "philosophy",
            "topic": "Propositional Knowledge",
            "description": "Knowing 'that' something is true. জ্ঞান যে কিছু সত্য।",
            "details": "Example: 'I know that Paris is the capital of France.' This is factual knowledge about the world.",
            "bengali": "প্রস্তাবনামূলক জ্ঞান - জানা যে কিছু সত্য। উদাহরণ: 'আমি জানি প্যারিস ফ্রান্সের রাজধানী।'"
        },
        {
            "category": "knowledge_type",
            "subcategory": "philosophy",
            "topic": "Procedural Knowledge",
            "description": "Knowing 'how' to do something. জানা কিভাবে কিছু করতে হয়।",
            "details": "Example: 'I know how to ride a bicycle.' This is skill-based knowledge.",
            "bengali": "প্রক্রিয়াগত জ্ঞান - জানা কিভাবে কিছু করতে হয়। উদাহরণ: 'আমি জানি কিভাবে সাইকেল চালাতে হয়।'"
        },
        {
            "category": "knowledge_type",
            "subcategory": "philosophy",
            "topic": "Acquaintance Knowledge",
            "description": "Knowing 'of' a person, place, or thing. পরিচিতি জ্ঞান।",
            "details": "Example: 'I know John' or 'I know Paris.' This is experiential familiarity.",
            "bengali": "পরিচিতি জ্ঞান - কোনো ব্যক্তি, স্থান বা জিনিসের সাথে পরিচিত। উদাহরণ: 'আমি জনকে চিনি।'"
        },
        
        # 2. Based on Source
        {
            "category": "knowledge_type",
            "subcategory": "source",
            "topic": "A Priori Knowledge",
            "description": "Based on logic, before experience. যুক্তি-ভিত্তিক জ্ঞান, অভিজ্ঞতার আগে।",
            "details": "Example: 'All bachelors are unmarried.' This is known through pure reasoning, not experience.",
            "bengali": "পূর্ব-অভিজ্ঞতামূলক জ্ঞান - যুক্তি দিয়ে জানা যায়, অভিজ্ঞতা ছাড়াই। উদাহরণ: 'সব ব্যাচেলর অবিবাহিত।'"
        },
        {
            "category": "knowledge_type",
            "subcategory": "source",
            "topic": "A Posteriori Knowledge",
            "description": "Based on observation, after experience. পর্যবেক্ষণ-ভিত্তিক জ্ঞান, অভিজ্ঞতার পরে।",
            "details": "Example: 'The sky is blue.' This is learned through sensory experience.",
            "bengali": "পরবর্তী-অভিজ্ঞতামূলক জ্ঞান - পর্যবেক্ষণ থেকে জানা। উদাহরণ: 'আকাশ নীল।'"
        },
        
        # 3. Business and Management
        {
            "category": "knowledge_type",
            "subcategory": "business",
            "topic": "Explicit Knowledge",
            "description": "Documented and easy to share. লিখিত এবং শেয়ার করা সহজ।",
            "details": "Example: Manuals, procedures, databases. Can be written down and transferred easily.",
            "bengali": "স্পষ্ট জ্ঞান - ডকুমেন্ট করা এবং শেয়ার করা সহজ। উদাহরণ: ম্যানুয়াল, পদ্ধতি।"
        },
        {
            "category": "knowledge_type",
            "subcategory": "business",
            "topic": "Tacit Knowledge",
            "description": "Personal experience, hard to write down. ব্যক্তিগত অভিজ্ঞতা, লেখা কঠিন।",
            "details": "Example: Intuition, expertise gained through years of practice. Hard to transfer to others.",
            "bengali": "অব্যক্ত জ্ঞান - ব্যক্তিগত অভিজ্ঞতা, লিখে প্রকাশ করা কঠিন। উদাহরণ: অন্তর্দৃষ্টি, দক্ষতা।"
        },
        {
            "category": "knowledge_type",
            "subcategory": "business",
            "topic": "Implicit Knowledge",
            "description": "Applied skills. প্রয়োগকৃত দক্ষতা।",
            "details": "Example: Knowing how to use software without reading the manual. Learned through doing.",
            "bengali": "অন্তর্নিহিত জ্ঞান - প্রয়োগকৃত দক্ষতা। উদাহরণ: ম্যানুয়াল না পড়েই সফটওয়্যার ব্যবহার করা।"
        },
        
        # 4. Domain-Specific
        {
            "category": "knowledge_type",
            "subcategory": "domain",
            "topic": "Domain Knowledge",
            "description": "Expertise in a specific field. নির্দিষ্ট ক্ষেত্রে দক্ষতা।",
            "details": "Example: Medical knowledge for doctors, legal knowledge for lawyers. Specialized expertise.",
            "bengali": "ডোমেইন জ্ঞান - নির্দিষ্ট ক্ষেত্রে দক্ষতা। উদাহরণ: ডাক্তারদের চিকিৎসা জ্ঞান।"
        },
        {
            "category": "knowledge_type",
            "subcategory": "domain",
            "topic": "Empirical Knowledge",
            "description": "Based on data and scientific testing. তথ্য এবং বৈজ্ঞানিক পরীক্ষা-ভিত্তিক।",
            "details": "Example: Scientific experiments, research data. Knowledge gained through systematic observation.",
            "bengali": "অভিজ্ঞতালব্ধ জ্ঞান - তথ্য এবং বৈজ্ঞানিক পরীক্ষা থেকে প্রাপ্ত। উদাহরণ: গবেষণা।"
        }
    ]
    
    # ==================== HUMAN SENSES ====================
    
    human_senses = [
        # 1. Traditional 5 Senses (External)
        {
            "category": "human_sense",
            "subcategory": "traditional_5",
            "topic": "Vision (Sight)",
            "description": "Ability to see light, colors, shapes. আলো, রঙ, আকৃতি দেখার ক্ষমতা।",
            "details": "Eyes detect light waves. Allows us to perceive the visual world around us.",
            "bengali": "দৃষ্টি - চোখ দিয়ে দেখার ক্ষমতা। আলো, রঙ, আকৃতি দেখতে পারি।"
        },
        {
            "category": "human_sense",
            "subcategory": "traditional_5",
            "topic": "Audition (Hearing)",
            "description": "Ability to hear sounds. শব্দ শোনার ক্ষমতা।",
            "details": "Ears detect sound waves. Allows us to perceive auditory information.",
            "bengali": "শ্রবণ - কান দিয়ে শোনার ক্ষমতা। শব্দ তরঙ্গ শনাক্ত করে।"
        },
        {
            "category": "human_sense",
            "subcategory": "traditional_5",
            "topic": "Olfaction (Smell)",
            "description": "Ability to smell odors. গন্ধ নেওয়ার ক্ষমতা।",
            "details": "Nose detects chemical molecules in the air. Allows us to perceive scents.",
            "bengali": "ঘ্রাণ - নাক দিয়ে গন্ধ নেওয়ার ক্ষমতা। বাতাসে রাসায়নিক অণু শনাক্ত করে।"
        },
        {
            "category": "human_sense",
            "subcategory": "traditional_5",
            "topic": "Gustation (Taste)",
            "description": "Ability to taste flavors. স্বাদ নেওয়ার ক্ষমতা।",
            "details": "Tongue detects sweet, sour, salty, bitter, umami. Allows us to perceive flavors.",
            "bengali": "স্বাদ - জিহ্বা দিয়ে স্বাদ নেওয়ার ক্ষমতা। মিষ্টি, টক, নোনতা, তিক্ত, উমামি।"
        },
        {
            "category": "human_sense",
            "subcategory": "traditional_5",
            "topic": "Tactition (Touch)",
            "description": "Ability to feel physical contact. স্পর্শ অনুভব করার ক্ষমতা।",
            "details": "Skin detects pressure, texture, temperature. Allows us to feel the physical world.",
            "bengali": "স্পর্শ - ত্বক দিয়ে স্পর্শ অনুভব করার ক্ষমতা। চাপ, গঠন, তাপমাত্রা অনুভব করি।"
        },
        
        # 2. Somatic & Internal Senses (Body Awareness)
        {
            "category": "human_sense",
            "subcategory": "somatic_internal",
            "topic": "Proprioception",
            "description": "Sense of body part position. শরীরের অংশের অবস্থান বোঝার ক্ষমতা।",
            "details": "Knowing where your limbs are without looking. Body position awareness.",
            "bengali": "প্রোপ্রিওসেপশন - না দেখেই শরীরের অংশের অবস্থান জানা। উদাহরণ: চোখ বন্ধ করে হাত তোলা।"
        },
        {
            "category": "human_sense",
            "subcategory": "somatic_internal",
            "topic": "Equilibrioception",
            "description": "Sense of balance and acceleration. ভারসাম্য এবং ত্বরণ বোঝার ক্ষমতা।",
            "details": "Inner ear detects balance and movement. Prevents falling, maintains posture.",
            "bengali": "ভারসাম্য ইন্দ্রিয় - ভারসাম্য এবং গতি বোঝার ক্ষমতা। পড়ে যাওয়া থেকে রক্ষা করে।"
        },
        {
            "category": "human_sense",
            "subcategory": "somatic_internal",
            "topic": "Thermoception",
            "description": "Sense of heat and cold. গরম এবং ঠান্ডা অনুভব করার ক্ষমতা।",
            "details": "Skin detects temperature changes. Allows us to feel hot and cold.",
            "bengali": "তাপ ইন্দ্রিয় - গরম এবং ঠান্ডা অনুভব করার ক্ষমতা। তাপমাত্রা পরিবর্তন শনাক্ত করে।"
        },
        {
            "category": "human_sense",
            "subcategory": "somatic_internal",
            "topic": "Nociception",
            "description": "Sense of pain. ব্যথা অনুভব করার ক্ষমতা।",
            "details": "Nerve endings detect harmful stimuli. Warning system for injury or damage.",
            "bengali": "ব্যথা ইন্দ্রিয় - ব্যথা অনুভব করার ক্ষমতা। ক্ষতি থেকে সতর্ক করে।"
        },
        {
            "category": "human_sense",
            "subcategory": "somatic_internal",
            "topic": "Interoception",
            "description": "Sense of internal bodily needs. অভ্যন্তরীণ শারীরিক চাহিদা বোঝার ক্ষমতা।",
            "details": "Hunger, thirst, heartbeat, needing the bathroom. Internal body state awareness.",
            "bengali": "অন্তঃইন্দ্রিয় - ক্ষুধা, তৃষ্ণা, হৃদস্পন্দন, বাথরুমের প্রয়োজন অনুভব করা।"
        },
        
        # 3. Specialized Sensory Inputs
        {
            "category": "human_sense",
            "subcategory": "specialized",
            "topic": "Chronoception",
            "description": "Sense of the passage of time. সময়ের গতি বোঝার ক্ষমতা।",
            "details": "Internal clock that tracks time passing. Allows us to estimate duration.",
            "bengali": "সময় ইন্দ্রিয় - সময়ের গতি বোঝার ক্ষমতা। কতক্ষণ হলো তা অনুমান করা।"
        },
        {
            "category": "human_sense",
            "subcategory": "specialized",
            "topic": "Kinaesthesia",
            "description": "Sense of body movement. শরীরের নড়াচড়া বোঝার ক্ষমতা।",
            "details": "Awareness of body motion and position during movement. Movement coordination.",
            "bengali": "গতি ইন্দ্রিয় - শরীরের নড়াচড়া এবং গতি বোঝার ক্ষমতা। চলাফেরার সমন্বয়।"
        },
        {
            "category": "human_sense",
            "subcategory": "specialized",
            "topic": "Chemoreception",
            "description": "Detection of chemicals. রাসায়নিক শনাক্তকরণ।",
            "details": "Detecting oxygen or carbon dioxide levels in blood. Chemical sensing in body.",
            "bengali": "রাসায়নিক ইন্দ্রিয় - রক্তে অক্সিজেন বা কার্বন ডাই অক্সাইড শনাক্ত করা।"
        },
        {
            "category": "human_sense",
            "subcategory": "specialized",
            "topic": "Baroreception",
            "description": "Detection of blood pressure. রক্তচাপ শনাক্তকরণ।",
            "details": "Sensors in blood vessels detect pressure changes. Regulates blood pressure.",
            "bengali": "চাপ ইন্দ্রিয় - রক্তচাপ শনাক্ত করার ক্ষমতা। রক্তচাপ নিয়ন্ত্রণ করে।"
        },
        {
            "category": "human_sense",
            "subcategory": "specialized",
            "topic": "Vestibular Sense",
            "description": "Spatial orientation and movement. স্থানিক দিকনির্দেশনা এবং গতি।",
            "details": "Inner ear system for balance and spatial awareness. Head position and movement.",
            "bengali": "ভেস্টিবুলার ইন্দ্রিয় - ভারসাম্য এবং স্থানিক সচেতনতা। মাথার অবস্থান এবং গতি।"
        },
        
        # 4. Cognitive/Practical Senses
        {
            "category": "human_sense",
            "subcategory": "cognitive",
            "topic": "Common Sense",
            "description": "Practical daily judgment. দৈনন্দিন ব্যবহারিক বিচার।",
            "details": "Practical reasoning and sound judgment in everyday situations. Basic wisdom.",
            "bengali": "সাধারণ জ্ঞান - দৈনন্দিন জীবনে ব্যবহারিক বিচার এবং বুদ্ধি। মৌলিক প্রজ্ঞা।"
        },
        {
            "category": "human_sense",
            "subcategory": "cognitive",
            "topic": "Moral Sense",
            "description": "Internal sense of right and wrong. সঠিক এবং ভুলের অভ্যন্তরীণ বোধ।",
            "details": "Conscience and ethical intuition. Knowing what is morally right or wrong.",
            "bengali": "নৈতিক বোধ - সঠিক এবং ভুলের অভ্যন্তরীণ বোধ। বিবেক এবং নৈতিক অন্তর্দৃষ্টি।"
        },
        {
            "category": "human_sense",
            "subcategory": "cognitive",
            "topic": "Sixth Sense (Intuition)",
            "description": "Intuition or gut feelings. অন্তর্দৃষ্টি বা অনুভূতি।",
            "details": "Instinctive feeling without conscious reasoning. Often called 'gut feeling' or intuition.",
            "bengali": "ষষ্ঠ ইন্দ্রিয় - অন্তর্দৃষ্টি বা অনুভূতি। যুক্তি ছাড়াই অনুভব করা। 'পেটের কথা' বলা হয়।"
        }
    ]
    
    # Add Knowledge Types
    print("Adding Knowledge Types...")
    print()
    
    for idx, item in enumerate(knowledge_types, 1):
        # Combine all info into content field
        content = f"""
{item['description']}

Details: {item['details']}

Bengali (বাংলা): {item['bengali']}

Category: {item['category']} > {item['subcategory']}
"""
        cursor.execute("""
            INSERT INTO knowledge_base 
            (topic, content, source)
            VALUES (?, ?, ?)
        """, (
            item['topic'],
            content.strip(),
            'Knowledge Types System'
        ))
        print(f"  ✅ {item['topic']}")
    
    print()
    
    # Add Human Senses
    print("Adding Human Senses...")
    print()
    
    for idx, item in enumerate(human_senses, 1):
        # Combine all info into content field
        content = f"""
{item['description']}

Details: {item['details']}

Bengali (বাংলা): {item['bengali']}

Category: {item['category']} > {item['subcategory']}
"""
        cursor.execute("""
            INSERT INTO knowledge_base 
            (topic, content, source)
            VALUES (?, ?, ?)
        """, (
            item['topic'],
            content.strip(),
            'Human Senses System'
        ))
        print(f"  ✅ {item['topic']}")
    
    print()
    
    # Add system configuration
    print("Adding system configuration...")
    
    configs = [
        ("knowledge_types_enabled", "true"),
        ("human_senses_enabled", "true"),
        ("propositional_knowledge", "true"),
        ("procedural_knowledge", "true"),
        ("acquaintance_knowledge", "true"),
        ("a_priori_knowledge", "true"),
        ("a_posteriori_knowledge", "true"),
        ("explicit_knowledge", "true"),
        ("tacit_knowledge", "true"),
        ("implicit_knowledge", "true"),
        ("domain_knowledge", "true"),
        ("empirical_knowledge", "true"),
        ("traditional_5_senses", "true"),
        ("somatic_senses", "true"),
        ("specialized_senses", "true"),
        ("cognitive_senses", "true")
    ]
    
    for key, value in configs:
        cursor.execute("""
            INSERT INTO system_info (key, value, category)
            VALUES (?, ?, 'knowledge_senses')
        """, (key, value))
        print(f"  ✅ {key}")
    
    conn.commit()
    
    # Get totals
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total_knowledge = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM system_info")
    total_system = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*80)
    print("  ✅ KNOWLEDGE TYPES এবং HUMAN SENSES সফলভাবে যোগ করা হয়েছে!")
    print("  ✅ Knowledge Types and Human Senses Successfully Added!")
    print("="*80)
    
    print(f"\n  Added Entries:")
    print(f"    📚 Knowledge Types: {len(knowledge_types)} entries")
    print(f"    👁️ Human Senses: {len(human_senses)} entries")
    print(f"    ⚙️ System Config: {len(configs)} entries")
    
    print(f"\n  Database Totals:")
    print(f"    📚 Total Knowledge: {total_knowledge} entries")
    print(f"    ⚙️ Total System Info: {total_system} entries")
    
    print("\n" + "="*80)
    print("\n  📚 KNOWLEDGE TYPES ADDED:\n")
    print("  1️⃣ Philosophy:")
    print("     • Propositional (প্রস্তাবনামূলক)")
    print("     • Procedural (প্রক্রিয়াগত)")
    print("     • Acquaintance (পরিচিতি)")
    
    print("\n  2️⃣ Source-Based:")
    print("     • A Priori (পূর্ব-অভিজ্ঞতামূলক)")
    print("     • A Posteriori (পরবর্তী-অভিজ্ঞতামূলক)")
    
    print("\n  3️⃣ Business:")
    print("     • Explicit (স্পষ্ট)")
    print("     • Tacit (অব্যক্ত)")
    print("     • Implicit (অন্তর্নিহিত)")
    
    print("\n  4️⃣ Domain:")
    print("     • Domain Knowledge (ডোমেইন জ্ঞান)")
    print("     • Empirical (অভিজ্ঞতালব্ধ)")
    
    print("\n" + "="*80)
    print("\n  👁️ HUMAN SENSES ADDED:\n")
    print("  1️⃣ Traditional 5 Senses:")
    print("     • Vision (দৃষ্টি)")
    print("     • Hearing (শ্রবণ)")
    print("     • Smell (ঘ্রাণ)")
    print("     • Taste (স্বাদ)")
    print("     • Touch (স্পর্শ)")
    
    print("\n  2️⃣ Somatic & Internal:")
    print("     • Proprioception (শরীরের অবস্থান)")
    print("     • Equilibrioception (ভারসাম্য)")
    print("     • Thermoception (তাপ)")
    print("     • Nociception (ব্যথা)")
    print("     • Interoception (অভ্যন্তরীণ চাহিদা)")
    
    print("\n  3️⃣ Specialized:")
    print("     • Chronoception (সময়)")
    print("     • Kinaesthesia (গতি)")
    print("     • Chemoreception (রাসায়নিক)")
    print("     • Baroreception (রক্তচাপ)")
    print("     • Vestibular (স্থানিক দিকনির্দেশনা)")
    
    print("\n  4️⃣ Cognitive:")
    print("     • Common Sense (সাধারণ জ্ঞান)")
    print("     • Moral Sense (নৈতিক বোধ)")
    print("     • Sixth Sense (ষষ্ঠ ইন্দ্রিয়)")
    
    print("\n" + "="*80)
    print("\n  JARVIS এখন সব ধরনের জ্ঞান এবং ইন্দ্রিয় সম্পর্কে জানে!")
    print("  JARVIS now knows all types of knowledge and human senses!")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    add_knowledge_and_senses()
