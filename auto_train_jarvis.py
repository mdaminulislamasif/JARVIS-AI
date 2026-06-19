#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Train JARVIS - Comprehensive Knowledge Training
JARVIS-কে স্বয়ংক্রিয়ভাবে ট্রেনিং দেওয়া
"""

import sqlite3
import os

# Database path
DB_PATH = "jarvis_memory.db.fixed-20260504-091901"

def auto_train_jarvis():
    """Automatically train JARVIS with comprehensive knowledge"""
    
    print("\n" + "="*80)
    print("  🎓 AUTO TRAINING JARVIS - স্বয়ংক্রিয় ট্রেনিং")
    print("  🧠 Teaching JARVIS comprehensive knowledge...")
    print("="*80 + "\n")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Comprehensive training data
    training_data = [
        # ==================== PROGRAMMING LANGUAGES ====================
        {
            "topic": "Python Programming",
            "content": """Python is a high-level, interpreted programming language known for its simplicity and readability. 
Created by Guido van Rossum in 1991. Used for web development, data science, AI, automation, and more.
Key features: Easy syntax, extensive libraries, cross-platform, object-oriented.
পাইথন একটি সহজ এবং শক্তিশালী প্রোগ্রামিং ভাষা।""",
            "source": "Programming Knowledge"
        },
        {
            "topic": "JavaScript",
            "content": """JavaScript is a programming language primarily used for web development. 
Runs in browsers and on servers (Node.js). Created by Brendan Eich in 1995.
Used for: Interactive websites, web apps, mobile apps, server-side programming.
জাভাস্ক্রিপ্ট ওয়েব ডেভেলপমেন্টের জন্য সবচেয়ে জনপ্রিয় ভাষা।""",
            "source": "Programming Knowledge"
        },
        {
            "topic": "Java",
            "content": """Java is a class-based, object-oriented programming language. 
Created by James Gosling at Sun Microsystems in 1995. Known for "Write Once, Run Anywhere" (WORA).
Used for: Android apps, enterprise software, web applications, big data.
জাভা একটি শক্তিশালী অবজেক্ট-ওরিয়েন্টেড ভাষা।""",
            "source": "Programming Knowledge"
        },
        {
            "topic": "C++ Programming",
            "content": """C++ is a powerful general-purpose programming language. 
Extension of C language with object-oriented features. Created by Bjarne Stroustrup in 1985.
Used for: System software, game development, embedded systems, high-performance applications.
সি++ একটি দ্রুত এবং শক্তিশালী ভাষা।""",
            "source": "Programming Knowledge"
        },
        {
            "topic": "C# (C Sharp)",
            "content": """C# is a modern, object-oriented programming language developed by Microsoft.
Part of the .NET framework. Created in 2000. Similar to Java but with Microsoft ecosystem.
Used for: Windows applications, game development (Unity), web apps, enterprise software.
সি শার্প মাইক্রোসফটের শক্তিশালী ভাষা।""",
            "source": "Programming Knowledge"
        },
        
        # ==================== WEB DEVELOPMENT ====================
        {
            "topic": "HTML (HyperText Markup Language)",
            "content": """HTML is the standard markup language for creating web pages.
Defines the structure and content of web pages using tags and elements.
Current version: HTML5. Not a programming language, but a markup language.
এইচটিএমএল ওয়েব পেজের কাঠামো তৈরি করে।""",
            "source": "Web Development"
        },
        {
            "topic": "CSS (Cascading Style Sheets)",
            "content": """CSS is used to style and layout web pages.
Controls colors, fonts, spacing, positioning, animations, and responsive design.
Current version: CSS3. Works with HTML to create beautiful websites.
সিএসএস ওয়েব পেজকে সুন্দর করে।""",
            "source": "Web Development"
        },
        {
            "topic": "React",
            "content": """React is a JavaScript library for building user interfaces.
Developed by Facebook (Meta). Uses component-based architecture and virtual DOM.
Popular for: Single-page applications, mobile apps (React Native), dynamic UIs.
রিঅ্যাক্ট ইউজার ইন্টারফেস তৈরির জন্য জনপ্রিয়।""",
            "source": "Web Development"
        },
        {
            "topic": "Node.js",
            "content": """Node.js is a JavaScript runtime built on Chrome's V8 engine.
Allows JavaScript to run on servers, not just browsers. Created by Ryan Dahl in 2009.
Used for: Backend APIs, real-time applications, microservices, command-line tools.
নোড.জেএস সার্ভার-সাইড জাভাস্ক্রিপ্ট।""",
            "source": "Web Development"
        },
        
        # ==================== DATABASES ====================
        {
            "topic": "SQL (Structured Query Language)",
            "content": """SQL is a language for managing and querying relational databases.
Used to create, read, update, and delete data (CRUD operations).
Common commands: SELECT, INSERT, UPDATE, DELETE, CREATE TABLE, JOIN.
এসকিউএল ডাটাবেস পরিচালনার ভাষা।""",
            "source": "Database Knowledge"
        },
        {
            "topic": "MySQL",
            "content": """MySQL is an open-source relational database management system.
One of the most popular databases. Owned by Oracle. Uses SQL language.
Used for: Web applications, content management systems, e-commerce.
মাইএসকিউএল একটি জনপ্রিয় ডাটাবেস।""",
            "source": "Database Knowledge"
        },
        {
            "topic": "MongoDB",
            "content": """MongoDB is a NoSQL document database.
Stores data in flexible JSON-like documents. Schema-less and scalable.
Used for: Big data, real-time analytics, content management, IoT applications.
মংগোডিবি একটি নোএসকিউএল ডাটাবেস।""",
            "source": "Database Knowledge"
        },
        
        # ==================== ARTIFICIAL INTELLIGENCE ====================
        {
            "topic": "Machine Learning",
            "content": """Machine Learning is a subset of AI where computers learn from data without explicit programming.
Types: Supervised learning, unsupervised learning, reinforcement learning.
Applications: Image recognition, speech recognition, recommendation systems, predictions.
মেশিন লার্নিং কম্পিউটারকে ডেটা থেকে শিখতে দেয়।""",
            "source": "AI Knowledge"
        },
        {
            "topic": "Deep Learning",
            "content": """Deep Learning is a subset of machine learning using neural networks with multiple layers.
Inspired by human brain structure. Excellent for complex pattern recognition.
Applications: Computer vision, natural language processing, autonomous vehicles, voice assistants.
ডিপ লার্নিং নিউরাল নেটওয়ার্ক ব্যবহার করে।""",
            "source": "AI Knowledge"
        },
        {
            "topic": "Natural Language Processing (NLP)",
            "content": """NLP is AI technology that helps computers understand, interpret, and generate human language.
Applications: Chatbots, translation, sentiment analysis, text summarization, voice assistants.
Techniques: Tokenization, named entity recognition, sentiment analysis, language models.
এনএলপি কম্পিউটারকে মানুষের ভাষা বুঝতে সাহায্য করে।""",
            "source": "AI Knowledge"
        },
        {
            "topic": "Neural Networks",
            "content": """Neural Networks are computing systems inspired by biological neural networks in animal brains.
Consist of layers: Input layer, hidden layers, output layer. Learn through backpropagation.
Used in: Image recognition, speech recognition, game playing, autonomous systems.
নিউরাল নেটওয়ার্ক মানুষের মস্তিষ্ক থেকে অনুপ্রাণিত।""",
            "source": "AI Knowledge"
        },
        
        # ==================== OPERATING SYSTEMS ====================
        {
            "topic": "Windows Operating System",
            "content": """Windows is a family of operating systems developed by Microsoft.
Most popular desktop OS. Current version: Windows 11. Known for user-friendly GUI.
Features: File management, multitasking, security, compatibility with most software.
উইন্ডোজ মাইক্রোসফটের অপারেটিং সিস্টেম।""",
            "source": "Operating Systems"
        },
        {
            "topic": "Linux Operating System",
            "content": """Linux is an open-source Unix-like operating system kernel.
Created by Linus Torvalds in 1991. Free and highly customizable.
Popular distributions: Ubuntu, Debian, Fedora, CentOS, Arch Linux.
Used for: Servers, embedded systems, supercomputers, Android devices.
লিনাক্স একটি ওপেন-সোর্স অপারেটিং সিস্টেম।""",
            "source": "Operating Systems"
        },
        {
            "topic": "macOS",
            "content": """macOS is Apple's operating system for Mac computers.
Based on Unix. Known for elegant design and seamless integration with Apple devices.
Features: Spotlight search, Time Machine backup, iCloud integration, security.
ম্যাকওএস অ্যাপলের অপারেটিং সিস্টেম।""",
            "source": "Operating Systems"
        },
        
        # ==================== NETWORKING ====================
        {
            "topic": "IP Address",
            "content": """IP (Internet Protocol) Address is a unique numerical label assigned to each device on a network.
Two versions: IPv4 (e.g., 192.168.1.1) and IPv6 (e.g., 2001:0db8:85a3::8a2e:0370:7334).
Used for: Device identification and location addressing on networks.
আইপি অ্যাড্রেস নেটওয়ার্কে ডিভাইস চিহ্নিত করে।""",
            "source": "Networking"
        },
        {
            "topic": "HTTP and HTTPS",
            "content": """HTTP (HyperText Transfer Protocol) is the foundation of data communication on the web.
HTTPS is the secure version using SSL/TLS encryption. Port 80 for HTTP, 443 for HTTPS.
HTTPS protects data from eavesdropping and tampering. Essential for secure websites.
এইচটিটিপিএস নিরাপদ ওয়েব যোগাযোগ।""",
            "source": "Networking"
        },
        {
            "topic": "DNS (Domain Name System)",
            "content": """DNS translates human-readable domain names (like google.com) into IP addresses.
Called the "phonebook of the internet". Hierarchical and distributed system.
DNS servers: Root servers, TLD servers, authoritative servers, recursive resolvers.
ডিএনএস ডোমেইন নামকে আইপি অ্যাড্রেসে রূপান্তর করে।""",
            "source": "Networking"
        },
        
        # ==================== CYBERSECURITY ====================
        {
            "topic": "Encryption",
            "content": """Encryption is the process of converting data into a coded format to prevent unauthorized access.
Types: Symmetric (same key) and Asymmetric (public/private key pair).
Algorithms: AES, RSA, DES, Blowfish. Used for: Secure communication, data protection.
এনক্রিপশন ডেটা সুরক্ষিত করে।""",
            "source": "Cybersecurity"
        },
        {
            "topic": "Firewall",
            "content": """A firewall is a network security system that monitors and controls incoming and outgoing traffic.
Types: Hardware firewall, software firewall, cloud firewall.
Functions: Packet filtering, stateful inspection, proxy service, NAT.
ফায়ারওয়াল নেটওয়ার্ক সুরক্ষা প্রদান করে।""",
            "source": "Cybersecurity"
        },
        {
            "topic": "Phishing",
            "content": """Phishing is a cyber attack where attackers impersonate legitimate entities to steal sensitive information.
Methods: Email phishing, spear phishing, whaling, smishing (SMS), vishing (voice).
Prevention: Verify sender, don't click suspicious links, use 2FA, security awareness training.
ফিশিং একটি সাইবার আক্রমণ পদ্ধতি।""",
            "source": "Cybersecurity"
        },
        
        # ==================== CLOUD COMPUTING ====================
        {
            "topic": "Cloud Computing",
            "content": """Cloud computing delivers computing services over the internet (the cloud).
Services: Servers, storage, databases, networking, software, analytics, intelligence.
Types: Public cloud, private cloud, hybrid cloud. Models: IaaS, PaaS, SaaS.
ক্লাউড কম্পিউটিং ইন্টারনেটের মাধ্যমে সেবা প্রদান করে।""",
            "source": "Cloud Computing"
        },
        {
            "topic": "AWS (Amazon Web Services)",
            "content": """AWS is Amazon's comprehensive cloud computing platform.
Offers 200+ services including EC2 (compute), S3 (storage), RDS (database), Lambda (serverless).
Market leader in cloud services. Pay-as-you-go pricing model.
এডব্লিউএস অ্যামাজনের ক্লাউড প্ল্যাটফর্ম।""",
            "source": "Cloud Computing"
        },
        {
            "topic": "Microsoft Azure",
            "content": """Azure is Microsoft's cloud computing platform and services.
Offers: Virtual machines, app services, AI/ML services, IoT, databases, DevOps tools.
Strong integration with Microsoft products. Second largest cloud provider.
অ্যাজুর মাইক্রোসফটের ক্লাউড সেবা।""",
            "source": "Cloud Computing"
        },
        
        # ==================== DATA SCIENCE ====================
        {
            "topic": "Data Science",
            "content": """Data Science combines statistics, mathematics, programming, and domain expertise to extract insights from data.
Process: Data collection, cleaning, exploration, modeling, visualization, interpretation.
Tools: Python, R, SQL, Jupyter, Pandas, NumPy, Matplotlib, Scikit-learn.
ডেটা সায়েন্স ডেটা থেকে জ্ঞান আহরণ করে।""",
            "source": "Data Science"
        },
        {
            "topic": "Big Data",
            "content": """Big Data refers to extremely large datasets that traditional software cannot process efficiently.
Characteristics (3 Vs): Volume (size), Velocity (speed), Variety (types).
Technologies: Hadoop, Spark, Kafka, NoSQL databases, data lakes.
বিগ ডেটা বিশাল পরিমাণ তথ্য।""",
            "source": "Data Science"
        },
        
        # ==================== MOBILE DEVELOPMENT ====================
        {
            "topic": "Android Development",
            "content": """Android is Google's mobile operating system and development platform.
Programming languages: Java, Kotlin (preferred). IDE: Android Studio.
Components: Activities, Services, Broadcast Receivers, Content Providers.
অ্যান্ড্রয়েড গুগলের মোবাইল প্ল্যাটফর্ম।""",
            "source": "Mobile Development"
        },
        {
            "topic": "iOS Development",
            "content": """iOS is Apple's mobile operating system for iPhone and iPad.
Programming languages: Swift (modern), Objective-C (legacy). IDE: Xcode.
Frameworks: UIKit, SwiftUI, Core Data, Core Animation.
আইওএস অ্যাপলের মোবাইল সিস্টেম।""",
            "source": "Mobile Development"
        },
        
        # ==================== VERSION CONTROL ====================
        {
            "topic": "Git",
            "content": """Git is a distributed version control system for tracking changes in source code.
Created by Linus Torvalds in 2005. Most popular VCS in the world.
Key concepts: Repository, commit, branch, merge, pull, push, clone.
Commands: git init, git add, git commit, git push, git pull, git branch.
গিট কোড পরিবর্তন ট্র্যাক করে।""",
            "source": "Version Control"
        },
        {
            "topic": "GitHub",
            "content": """GitHub is a web-based platform for version control and collaboration using Git.
Owned by Microsoft. Features: Repositories, pull requests, issues, actions (CI/CD), pages.
Largest host of source code in the world. Used for open-source and private projects.
গিটহাব কোড শেয়ারিং প্ল্যাটফর্ম।""",
            "source": "Version Control"
        },
        
        # ==================== BANGLADESH KNOWLEDGE ====================
        {
            "topic": "Bangladesh",
            "content": """Bangladesh is a country in South Asia with a population of about 170 million people.
Capital: Dhaka. Official language: Bengali (Bangla). Currency: Taka (BDT).
Independence: March 26, 1971. Victory Day: December 16, 1971.
Known for: Rich culture, longest sea beach (Cox's Bazar), Sundarbans mangrove forest, Royal Bengal Tiger.
বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ।""",
            "source": "General Knowledge"
        },
        {
            "topic": "Bengali Language",
            "content": """Bengali (Bangla) is the 7th most spoken language in the world with 230+ million speakers.
Official language of Bangladesh and West Bengal (India). Written in Bengali script.
Rich literary tradition: Rabindranath Tagore (Nobel Prize), Kazi Nazrul Islam.
Language Movement Day: February 21 (International Mother Language Day).
বাংলা বিশ্বের ৭ম সর্বাধিক কথ্য ভাষা।""",
            "source": "General Knowledge"
        },
        
        # ==================== SCIENCE ====================
        {
            "topic": "Physics",
            "content": """Physics is the natural science that studies matter, energy, motion, and force.
Branches: Classical mechanics, thermodynamics, electromagnetism, quantum mechanics, relativity.
Famous physicists: Newton, Einstein, Hawking, Feynman, Curie.
ফিজিক্স পদার্থ এবং শক্তি নিয়ে অধ্যয়ন করে।""",
            "source": "Science"
        },
        {
            "topic": "Chemistry",
            "content": """Chemistry is the science of matter, its properties, composition, structure, and changes.
Branches: Organic, inorganic, physical, analytical, biochemistry.
Periodic table has 118 elements. Created by Dmitri Mendeleev.
কেমিস্ট্রি পদার্থের গঠন এবং বিক্রিয়া নিয়ে অধ্যয়ন করে।""",
            "source": "Science"
        },
        {
            "topic": "Biology",
            "content": """Biology is the science of life and living organisms.
Branches: Zoology (animals), botany (plants), microbiology (microorganisms), genetics, ecology.
Cell is the basic unit of life. DNA carries genetic information.
বায়োলজি জীবন এবং জীবিত প্রাণী নিয়ে অধ্যয়ন করে।""",
            "source": "Science"
        },
        
        # ==================== MATHEMATICS ====================
        {
            "topic": "Algebra",
            "content": """Algebra is a branch of mathematics dealing with symbols and rules for manipulating those symbols.
Includes: Equations, variables, functions, polynomials, matrices.
Used in: Science, engineering, economics, computer science.
অ্যালজেব্রা গাণিতিক চিহ্ন এবং সমীকরণ নিয়ে কাজ করে।""",
            "source": "Mathematics"
        },
        {
            "topic": "Calculus",
            "content": """Calculus is the mathematical study of continuous change.
Two main branches: Differential calculus (rates of change) and integral calculus (accumulation).
Invented by Newton and Leibniz. Used in: Physics, engineering, economics, statistics.
ক্যালকুলাস পরিবর্তনের হার নিয়ে অধ্যয়ন করে।""",
            "source": "Mathematics"
        },
        
        # ==================== HISTORY ====================
        {
            "topic": "World War II",
            "content": """World War II (1939-1945) was the deadliest conflict in human history.
Major powers: Allies (USA, UK, USSR, China) vs Axis (Germany, Japan, Italy).
Key events: Holocaust, atomic bombs on Hiroshima and Nagasaki, D-Day invasion.
Resulted in 70-85 million deaths. Led to formation of United Nations.
দ্বিতীয় বিশ্বযুদ্ধ মানব ইতিহাসের সবচেয়ে ভয়াবহ যুদ্ধ।""",
            "source": "History"
        },
        {
            "topic": "Industrial Revolution",
            "content": """The Industrial Revolution (1760-1840) was a period of major industrialization and innovation.
Started in Britain, spread worldwide. Key inventions: Steam engine, spinning jenny, power loom.
Transformed: Manufacturing, transportation, agriculture, society.
Shifted from agrarian to industrial economy.
শিল্প বিপ্লব উৎপাদন পদ্ধতিতে বিপ্লব এনেছিল।""",
            "source": "History"
        },
        
        # ==================== GEOGRAPHY ====================
        {
            "topic": "Seven Continents",
            "content": """The world has seven continents: Asia, Africa, North America, South America, Antarctica, Europe, Australia.
Largest: Asia (44.58 million km²). Smallest: Australia (8.6 million km²).
Most populous: Asia (4.6+ billion). Least populous: Antarctica (no permanent residents).
সাতটি মহাদেশ: এশিয়া, আফ্রিকা, উত্তর আমেরিকা, দক্ষিণ আমেরিকা, অ্যান্টার্কটিকা, ইউরোপ, অস্ট্রেলিয়া।""",
            "source": "Geography"
        },
        {
            "topic": "Five Oceans",
            "content": """The world has five oceans: Pacific, Atlantic, Indian, Southern (Antarctic), Arctic.
Largest: Pacific Ocean (165.2 million km²). Smallest: Arctic Ocean (14.06 million km²).
Oceans cover 71% of Earth's surface. Contain 97% of Earth's water.
পাঁচটি মহাসাগর: প্রশান্ত, আটলান্টিক, ভারত, দক্ষিণ, আর্কটিক।""",
            "source": "Geography"
        }
    ]
    
    print(f"📚 Training JARVIS with {len(training_data)} comprehensive knowledge entries...\n")
    
    added = 0
    for idx, entry in enumerate(training_data, 1):
        try:
            cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source)
                VALUES (?, ?, ?)
            """, (entry['topic'], entry['content'], entry['source']))
            print(f"  ✅ [{idx}/{len(training_data)}] {entry['topic']}")
            added += 1
        except Exception as e:
            print(f"  ❌ [{idx}/{len(training_data)}] {entry['topic']} - Error: {e}")
    
    conn.commit()
    
    # Get totals
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total_knowledge = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM system_info")
    total_system = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*80)
    print("  ✅ AUTO TRAINING COMPLETED! - স্বয়ংক্রিয় ট্রেনিং সম্পন্ন!")
    print("="*80)
    
    print(f"\n  📊 Training Results:")
    print(f"     • Successfully added: {added} entries")
    print(f"     • Total knowledge: {total_knowledge} entries")
    print(f"     • Total system info: {total_system} entries")
    
    print("\n" + "="*80)
    print("  📚 KNOWLEDGE CATEGORIES TRAINED:")
    print("="*80)
    print("""
  1️⃣  Programming Languages (5 entries)
      • Python, JavaScript, Java, C++, C#
      
  2️⃣  Web Development (4 entries)
      • HTML, CSS, React, Node.js
      
  3️⃣  Databases (3 entries)
      • SQL, MySQL, MongoDB
      
  4️⃣  Artificial Intelligence (4 entries)
      • Machine Learning, Deep Learning, NLP, Neural Networks
      
  5️⃣  Operating Systems (3 entries)
      • Windows, Linux, macOS
      
  6️⃣  Networking (3 entries)
      • IP Address, HTTP/HTTPS, DNS
      
  7️⃣  Cybersecurity (3 entries)
      • Encryption, Firewall, Phishing
      
  8️⃣  Cloud Computing (3 entries)
      • Cloud Computing, AWS, Azure
      
  9️⃣  Data Science (2 entries)
      • Data Science, Big Data
      
  🔟 Mobile Development (2 entries)
      • Android, iOS
      
  1️⃣1️⃣ Version Control (2 entries)
      • Git, GitHub
      
  1️⃣2️⃣ Bangladesh Knowledge (2 entries)
      • Bangladesh, Bengali Language
      
  1️⃣3️⃣ Science (3 entries)
      • Physics, Chemistry, Biology
      
  1️⃣4️⃣ Mathematics (2 entries)
      • Algebra, Calculus
      
  1️⃣5️⃣ History (2 entries)
      • World War II, Industrial Revolution
      
  1️⃣6️⃣ Geography (2 entries)
      • Seven Continents, Five Oceans
    """)
    
    print("="*80)
    print("\n  🧪 TEST JARVIS NOW:")
    print("="*80)
    print("""
  Try these commands:
  
  python jarvis_offline_brain.py "What is Python?"
  python jarvis_offline_brain.py "Tell me about Bangladesh"
  python jarvis_offline_brain.py "What is machine learning?"
  python jarvis_offline_brain.py "Explain cloud computing"
  python jarvis_offline_brain.py "What is Git?"
    """)
    
    print("="*80)
    print("  🎉 JARVIS IS NOW MUCH SMARTER!")
    print("  🎉 জার্ভিস এখন আরও বুদ্ধিমান!")
    print("="*80 + "\n")

if __name__ == "__main__":
    auto_train_jarvis()
