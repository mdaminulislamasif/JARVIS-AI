"""
Add Common Sense and General Knowledge to JARVIS
JARVIS-এ সাধারণ জ্ঞান এবং কমন সেন্স যোগ করুন

Features:
1. Common Sense Reasoning
2. General Knowledge (World, Science, History, etc.)
3. Everyday Knowledge
4. Social Understanding
5. Physical World Understanding
"""

import sqlite3
import os
from datetime import datetime

def add_common_sense_knowledge():
    """Add common sense and general knowledge to JARVIS database"""
    
    print("\n" + "=" * 80)
    print("  🧠 ADDING COMMON SENSE & GENERAL KNOWLEDGE TO JARVIS")
    print("  🧠 JARVIS-এ সাধারণ জ্ঞান এবং কমন সেন্স যোগ করা হচ্ছে")
    print("=" * 80)
    print()
    
    # Database file
    db_file = 'jarvis_memory.db.fixed-20260504-091901'
    
    if not os.path.exists(db_file):
        print(f"❌ Database not found: {db_file}")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    print("✅ Connected to database")
    print()
    
    # Knowledge entries
    knowledge_entries = []
    
    # ========================================================================
    # CATEGORY 1: COMMON SENSE REASONING
    # ========================================================================
    
    knowledge_entries.append({
        'topic': 'Common Sense - Physical World',
        'content': '''Common Sense about Physical World:

Basic Physics:
✅ Objects fall down due to gravity
✅ Water flows downhill
✅ Fire is hot and can burn
✅ Ice is cold and melts when heated
✅ Heavy objects are harder to lift
✅ Sharp objects can cut
✅ Glass can break
✅ Metal conducts electricity

Cause and Effect:
✅ If you drop something, it falls
✅ If you push something, it moves
✅ If you heat water, it boils
✅ If you freeze water, it becomes ice
✅ If you cut paper, it tears
✅ If you mix colors, they blend

Spatial Reasoning:
✅ Inside vs outside
✅ Above vs below
✅ Left vs right
✅ Near vs far
✅ Big vs small
✅ Full vs empty

Examples:
- "Can I put an elephant in a cup?" → No, too big
- "Will water stay in a broken cup?" → No, it will leak
- "Can I walk through a wall?" → No, walls are solid
- "Will a ball roll uphill by itself?" → No, gravity pulls down''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'Common Sense - Time and Causality',
        'content': '''Common Sense about Time and Causality:

Time Understanding:
✅ Past → Present → Future
✅ Yesterday → Today → Tomorrow
✅ Morning → Afternoon → Evening → Night
✅ Seconds → Minutes → Hours → Days → Weeks → Months → Years
✅ You can't go back in time
✅ Future hasn't happened yet

Causality (Cause → Effect):
✅ If you don't eat, you get hungry
✅ If you don't sleep, you get tired
✅ If you study, you learn
✅ If you exercise, you get fit
✅ If you water plants, they grow
✅ If you break something, it's damaged

Temporal Logic:
✅ You must be born before you can walk
✅ You must learn before you can teach
✅ You must buy before you can own
✅ You must cook before you can eat (cooked food)
✅ You must plant before you can harvest

Examples:
- "Can I eat breakfast after dinner?" → Yes, but unusual
- "Can I be 5 years old after being 10?" → No, time moves forward
- "If I break a glass, can I unbreak it?" → No, irreversible
- "Do I need to learn to read before reading a book?" → Yes''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'Common Sense - Social Understanding',
        'content': '''Common Sense about Social Interactions:

Basic Social Rules:
✅ Say "please" when asking
✅ Say "thank you" when receiving
✅ Say "sorry" when you make a mistake
✅ Greet people when you meet them
✅ Be polite and respectful
✅ Don't interrupt when someone is speaking
✅ Listen when someone talks to you
✅ Help others when they need it

Emotions:
✅ People smile when happy
✅ People cry when sad
✅ People get angry when frustrated
✅ People laugh at jokes
✅ People feel pain when hurt
✅ People feel scared of danger

Social Norms:
✅ Wear clothes in public
✅ Don't shout in libraries
✅ Queue/wait in line
✅ Don't take others' belongings
✅ Knock before entering
✅ Cover mouth when coughing
✅ Wash hands before eating

Examples:
- "Should I shout in a library?" → No, be quiet
- "Can I take someone's phone without asking?" → No, that's stealing
- "Should I say thank you when someone helps?" → Yes, be polite
- "Is it okay to laugh at someone's pain?" → No, be compassionate''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'Common Sense - Everyday Life',
        'content': '''Common Sense about Everyday Life:

Daily Activities:
✅ Eat when hungry
✅ Sleep when tired
✅ Drink when thirsty
✅ Wear coat when cold
✅ Use umbrella when raining
✅ Turn on lights when dark
✅ Lock door for security
✅ Charge phone when battery low

Safety:
✅ Look both ways before crossing road
✅ Don't touch hot stove
✅ Don't play with fire
✅ Don't swim alone
✅ Wear seatbelt in car
✅ Don't talk to strangers (children)
✅ Keep medicines away from children
✅ Don't run with scissors

Hygiene:
✅ Brush teeth daily
✅ Take bath/shower regularly
✅ Wash hands before eating
✅ Wash hands after toilet
✅ Cover mouth when sneezing
✅ Change clothes regularly
✅ Keep living space clean

Examples:
- "Should I touch a hot stove?" → No, you'll get burned
- "Can I cross the road without looking?" → No, dangerous
- "Should I brush my teeth?" → Yes, for dental health
- "Can I eat food that fell on the floor?" → Not recommended, unhygienic''',
        'source': 'Common Sense & General Knowledge'
    })
    
    # ========================================================================
    # CATEGORY 2: GENERAL KNOWLEDGE - WORLD
    # ========================================================================
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Geography',
        'content': '''General Knowledge - Geography:

Continents (7):
1. Asia (largest)
2. Africa
3. North America
4. South America
5. Antarctica
6. Europe
7. Australia/Oceania

Oceans (5):
1. Pacific Ocean (largest)
2. Atlantic Ocean
3. Indian Ocean
4. Southern Ocean
5. Arctic Ocean

Major Countries:
- China (most populous)
- India (2nd most populous)
- United States (superpower)
- Russia (largest by area)
- Brazil (largest in South America)
- Canada (2nd largest by area)
- Australia (continent country)

Famous Cities:
- New York (USA)
- London (UK)
- Paris (France)
- Tokyo (Japan)
- Beijing (China)
- Mumbai (India)
- Dubai (UAE)

Natural Wonders:
- Mount Everest (highest mountain)
- Amazon River (largest river by volume)
- Sahara Desert (largest hot desert)
- Great Barrier Reef (largest coral reef)
- Grand Canyon (USA)''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Science',
        'content': '''General Knowledge - Science:

Basic Physics:
✅ Gravity pulls objects down
✅ Light travels faster than sound
✅ Energy cannot be created or destroyed
✅ Every action has equal and opposite reaction
✅ Speed of light: 299,792 km/s
✅ Water boils at 100°C (212°F)
✅ Water freezes at 0°C (32°F)

Basic Chemistry:
✅ Water formula: H2O (2 hydrogen, 1 oxygen)
✅ Air is mostly nitrogen (78%) and oxygen (21%)
✅ Gold symbol: Au
✅ Silver symbol: Ag
✅ Iron symbol: Fe
✅ Salt formula: NaCl
✅ Periodic table has 118 elements

Basic Biology:
✅ Humans have 206 bones
✅ Heart pumps blood
✅ Lungs help us breathe
✅ Brain controls body
✅ DNA carries genetic information
✅ Cells are building blocks of life
✅ Plants make oxygen through photosynthesis

Solar System:
✅ Sun is a star
✅ 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
✅ Earth is 3rd planet from Sun
✅ Moon orbits Earth
✅ Earth takes 365 days to orbit Sun
✅ Earth rotates in 24 hours (day/night)''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - History',
        'content': '''General Knowledge - History:

Ancient Civilizations:
- Egyptian Civilization (Pyramids, Pharaohs)
- Greek Civilization (Democracy, Philosophy)
- Roman Empire (Colosseum, Julius Caesar)
- Chinese Civilization (Great Wall)
- Indus Valley Civilization
- Mesopotamian Civilization

Important Historical Events:
- Discovery of America (1492) - Christopher Columbus
- French Revolution (1789)
- World War I (1914-1918)
- World War II (1939-1945)
- Moon Landing (1969) - Neil Armstrong
- Fall of Berlin Wall (1989)
- Internet invented (1960s-1990s)

Famous Historical Figures:
- Alexander the Great (Conqueror)
- Julius Caesar (Roman Emperor)
- Cleopatra (Egyptian Queen)
- Leonardo da Vinci (Artist, Inventor)
- William Shakespeare (Writer)
- Isaac Newton (Scientist)
- Albert Einstein (Physicist)
- Mahatma Gandhi (Freedom Fighter)
- Martin Luther King Jr. (Civil Rights)
- Nelson Mandela (Anti-Apartheid)

Inventions:
- Wheel (ancient)
- Printing Press (1440) - Gutenberg
- Telephone (1876) - Alexander Graham Bell
- Light Bulb (1879) - Thomas Edison
- Airplane (1903) - Wright Brothers
- Computer (1940s)
- Internet (1960s-1990s)
- Smartphone (2007) - iPhone''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Mathematics',
        'content': '''General Knowledge - Mathematics:

Basic Operations:
✅ Addition (+): 2 + 3 = 5
✅ Subtraction (-): 5 - 2 = 3
✅ Multiplication (×): 2 × 3 = 6
✅ Division (÷): 6 ÷ 2 = 3

Number Types:
✅ Natural Numbers: 1, 2, 3, 4, 5...
✅ Whole Numbers: 0, 1, 2, 3, 4...
✅ Integers: ...-2, -1, 0, 1, 2...
✅ Fractions: 1/2, 3/4, 2/3
✅ Decimals: 0.5, 1.25, 3.14
✅ Prime Numbers: 2, 3, 5, 7, 11, 13...

Geometry:
✅ Triangle has 3 sides
✅ Square has 4 equal sides
✅ Rectangle has 4 sides (opposite sides equal)
✅ Circle has no corners
✅ Cube has 6 faces
✅ Sphere is round like a ball

Famous Numbers:
✅ Pi (π) ≈ 3.14159...
✅ e ≈ 2.71828...
✅ Golden Ratio (φ) ≈ 1.618...
✅ Zero (0) - invented in India

Formulas:
✅ Area of Square: side × side
✅ Area of Rectangle: length × width
✅ Area of Circle: π × radius²
✅ Pythagorean Theorem: a² + b² = c²
✅ Percentage: (part/whole) × 100''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Languages',
        'content': '''General Knowledge - Languages:

Most Spoken Languages (by native speakers):
1. Mandarin Chinese (900+ million)
2. Spanish (460+ million)
3. English (380+ million)
4. Hindi (340+ million)
5. Bengali (230+ million)
6. Portuguese (220+ million)
7. Russian (150+ million)
8. Japanese (125+ million)
9. Punjabi (120+ million)
10. German (95+ million)

Language Families:
- Indo-European (English, Spanish, Hindi, etc.)
- Sino-Tibetan (Chinese, Tibetan)
- Afro-Asiatic (Arabic, Hebrew)
- Niger-Congo (Swahili, Zulu)
- Austronesian (Indonesian, Tagalog)

Writing Systems:
- Latin/Roman alphabet (English, Spanish, French)
- Arabic script (Arabic, Urdu, Persian)
- Chinese characters (Chinese, Japanese Kanji)
- Devanagari (Hindi, Sanskrit, Nepali)
- Cyrillic (Russian, Ukrainian, Bulgarian)
- Bengali script (Bengali, Assamese)

Common Phrases:
- Hello: Hola (Spanish), Bonjour (French), Namaste (Hindi)
- Thank you: Gracias (Spanish), Merci (French), Dhanyavaad (Hindi)
- Goodbye: Adiós (Spanish), Au revoir (French), Alvida (Hindi)''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Technology',
        'content': '''General Knowledge - Technology:

Computer Basics:
✅ CPU - Central Processing Unit (brain)
✅ RAM - Random Access Memory (temporary storage)
✅ Hard Drive/SSD - Permanent storage
✅ GPU - Graphics Processing Unit
✅ Operating Systems: Windows, macOS, Linux, Android, iOS
✅ Binary: 0 and 1 (computer language)
✅ Bit < Byte < KB < MB < GB < TB

Internet:
✅ WWW - World Wide Web (invented 1989)
✅ HTTP/HTTPS - Web protocols
✅ URL - Web address
✅ Email - Electronic mail
✅ Social Media: Facebook, Twitter, Instagram, etc.
✅ Search Engines: Google, Bing, Yahoo
✅ Cloud Storage: Google Drive, Dropbox, OneDrive

Programming:
✅ Popular Languages: Python, JavaScript, Java, C++, C#
✅ HTML - Web structure
✅ CSS - Web styling
✅ JavaScript - Web interactivity
✅ SQL - Database queries
✅ Git - Version control

Modern Tech:
✅ AI - Artificial Intelligence
✅ ML - Machine Learning
✅ IoT - Internet of Things
✅ VR - Virtual Reality
✅ AR - Augmented Reality
✅ Blockchain - Distributed ledger
✅ 5G - Fifth generation mobile network''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Human Body',
        'content': '''General Knowledge - Human Body:

Body Systems:
✅ Skeletal System - 206 bones, provides structure
✅ Muscular System - 600+ muscles, enables movement
✅ Circulatory System - Heart, blood vessels, blood
✅ Respiratory System - Lungs, breathing
✅ Digestive System - Stomach, intestines, digestion
✅ Nervous System - Brain, spinal cord, nerves
✅ Immune System - Fights diseases
✅ Endocrine System - Hormones

Major Organs:
✅ Brain - Controls everything, weighs ~1.4 kg
✅ Heart - Pumps blood, beats ~100,000 times/day
✅ Lungs - Breathing, oxygen exchange
✅ Liver - Detoxification, metabolism
✅ Kidneys - Filter blood, produce urine
✅ Stomach - Digests food
✅ Skin - Largest organ, protection

Senses (5):
1. Sight (Eyes)
2. Hearing (Ears)
3. Smell (Nose)
4. Taste (Tongue)
5. Touch (Skin)

Body Facts:
✅ Adult body has ~37 trillion cells
✅ Blood type: A, B, AB, O (with +/-)
✅ Normal body temperature: 37°C (98.6°F)
✅ Average heart rate: 60-100 beats/minute
✅ Humans breathe ~20,000 times/day
✅ DNA is unique to each person (except twins)''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Animals',
        'content': '''General Knowledge - Animals:

Animal Classification:
✅ Mammals - Have fur/hair, feed milk to young
✅ Birds - Have feathers, lay eggs, can fly (most)
✅ Reptiles - Have scales, cold-blooded
✅ Amphibians - Live in water and land
✅ Fish - Live in water, have gills
✅ Insects - 6 legs, 3 body parts

Famous Animals:
✅ Elephant - Largest land animal
✅ Blue Whale - Largest animal ever
✅ Cheetah - Fastest land animal (120 km/h)
✅ Peregrine Falcon - Fastest bird (390 km/h)
✅ Giraffe - Tallest animal
✅ Ant - Can lift 50× its weight
✅ Dog - Man's best friend
✅ Cat - Popular pet

Animal Homes:
✅ Lion - Den
✅ Bird - Nest
✅ Bee - Hive
✅ Spider - Web
✅ Rabbit - Burrow
✅ Bear - Cave
✅ Ant - Anthill

Animal Sounds:
✅ Dog - Bark
✅ Cat - Meow
✅ Cow - Moo
✅ Lion - Roar
✅ Bird - Chirp
✅ Frog - Croak
✅ Snake - Hiss''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Food & Nutrition',
        'content': '''General Knowledge - Food & Nutrition:

Food Groups:
1. Grains - Rice, wheat, bread, pasta
2. Proteins - Meat, fish, eggs, beans
3. Dairy - Milk, cheese, yogurt
4. Fruits - Apples, bananas, oranges
5. Vegetables - Carrots, spinach, broccoli
6. Fats & Oils - Butter, olive oil

Nutrients:
✅ Carbohydrates - Energy source
✅ Proteins - Build and repair tissues
✅ Fats - Energy storage, cell function
✅ Vitamins - A, B, C, D, E, K
✅ Minerals - Iron, calcium, zinc
✅ Water - Essential for life

Healthy Eating:
✅ Eat balanced diet
✅ Drink plenty of water (8 glasses/day)
✅ Eat fruits and vegetables
✅ Limit sugar and salt
✅ Avoid junk food
✅ Eat breakfast
✅ Don't skip meals

World Cuisines:
✅ Italian - Pizza, pasta
✅ Chinese - Noodles, rice, dumplings
✅ Indian - Curry, biryani, naan
✅ Mexican - Tacos, burritos
✅ Japanese - Sushi, ramen
✅ French - Croissants, cheese
✅ American - Burgers, hot dogs''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Sports',
        'content': '''General Knowledge - Sports:

Popular Sports:
✅ Football/Soccer - Most popular worldwide
✅ Cricket - Popular in India, Pakistan, Australia
✅ Basketball - Popular in USA
✅ Tennis - Individual sport
✅ Baseball - Popular in USA, Japan
✅ Rugby - Popular in UK, Australia, New Zealand
✅ Hockey - Ice hockey (Canada), Field hockey (India)
✅ Golf - Individual sport
✅ Swimming - Olympic sport
✅ Athletics - Running, jumping, throwing

Major Events:
✅ Olympics - Every 4 years (Summer & Winter)
✅ FIFA World Cup - Football, every 4 years
✅ Cricket World Cup - Every 4 years
✅ Super Bowl - American Football (USA)
✅ Wimbledon - Tennis (UK)
✅ Tour de France - Cycling (France)

Famous Athletes:
✅ Lionel Messi - Football
✅ Cristiano Ronaldo - Football
✅ Michael Jordan - Basketball
✅ Usain Bolt - Sprinter (fastest man)
✅ Serena Williams - Tennis
✅ Muhammad Ali - Boxing
✅ Michael Phelps - Swimming (most Olympic medals)

Sports Terms:
✅ Goal - Football/Soccer
✅ Touchdown - American Football
✅ Home Run - Baseball
✅ Ace - Tennis
✅ Birdie - Golf
✅ Knockout - Boxing''',
        'source': 'Common Sense & General Knowledge'
    })
    
    knowledge_entries.append({
        'topic': 'General Knowledge - Arts & Culture',
        'content': '''General Knowledge - Arts & Culture:

Famous Artists:
✅ Leonardo da Vinci - Mona Lisa, The Last Supper
✅ Vincent van Gogh - Starry Night, Sunflowers
✅ Pablo Picasso - Cubism, Guernica
✅ Michelangelo - Sistine Chapel, David statue
✅ Claude Monet - Water Lilies, Impressionism
✅ Salvador Dalí - Surrealism

Famous Writers:
✅ William Shakespeare - Romeo & Juliet, Hamlet
✅ Charles Dickens - Oliver Twist, A Christmas Carol
✅ Jane Austen - Pride and Prejudice
✅ Mark Twain - Tom Sawyer, Huckleberry Finn
✅ J.K. Rowling - Harry Potter series
✅ Rabindranath Tagore - First Asian Nobel Prize

Famous Musicians:
✅ Ludwig van Beethoven - Classical composer
✅ Wolfgang Amadeus Mozart - Classical composer
✅ The Beatles - Rock band (UK)
✅ Michael Jackson - King of Pop
✅ Elvis Presley - King of Rock and Roll
✅ Bob Marley - Reggae

Seven Wonders of Ancient World:
1. Great Pyramid of Giza (Egypt) - Only surviving
2. Hanging Gardens of Babylon
3. Statue of Zeus at Olympia
4. Temple of Artemis
5. Mausoleum at Halicarnassus
6. Colossus of Rhodes
7. Lighthouse of Alexandria

New Seven Wonders:
1. Great Wall of China
2. Petra (Jordan)
3. Christ the Redeemer (Brazil)
4. Machu Picchu (Peru)
5. Chichen Itza (Mexico)
6. Colosseum (Italy)
7. Taj Mahal (India)''',
        'source': 'Common Sense & General Knowledge'
    })
    
    # ========================================================================
    # Add entries to database
    # ========================================================================
    
    print(f"Adding {len(knowledge_entries)} common sense & general knowledge entries...")
    print()
    
    added_count = 0
    
    for entry in knowledge_entries:
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
        ('common_sense_enabled', 'yes', 'Knowledge'),
        ('general_knowledge_enabled', 'yes', 'Knowledge'),
        ('reasoning_enabled', 'yes', 'Knowledge'),
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
    print("  ✅ COMMON SENSE & GENERAL KNOWLEDGE ADDED SUCCESSFULLY!")
    print("  ✅ সাধারণ জ্ঞান এবং কমন সেন্স সফলভাবে যোগ করা হয়েছে!")
    print("=" * 80)
    print()
    print(f"  Added Entries:")
    print(f"    📚 Knowledge Base: {added_count} entries")
    print(f"    ⚙️ System Info: 3 config entries")
    print()
    print(f"  Database Totals:")
    print(f"    📚 Total Knowledge: {total_knowledge} entries")
    print(f"    ⚙️ Total System Info: {total_system} entries")
    print()
    print("=" * 80)
    print()
    print("  🎯 KNOWLEDGE CATEGORIES:")
    print()
    print("  1️⃣ COMMON SENSE (4 topics):")
    print("    ✅ Physical World (gravity, objects, spatial reasoning)")
    print("    ✅ Time & Causality (cause-effect, temporal logic)")
    print("    ✅ Social Understanding (emotions, norms, etiquette)")
    print("    ✅ Everyday Life (daily activities, safety, hygiene)")
    print()
    print("  2️⃣ GENERAL KNOWLEDGE (11 topics):")
    print("    ✅ Geography (continents, countries, cities)")
    print("    ✅ Science (physics, chemistry, biology, astronomy)")
    print("    ✅ History (civilizations, events, famous figures)")
    print("    ✅ Mathematics (operations, geometry, formulas)")
    print("    ✅ Languages (most spoken, families, scripts)")
    print("    ✅ Technology (computers, internet, programming)")
    print("    ✅ Human Body (organs, systems, senses)")
    print("    ✅ Animals (classification, famous animals, sounds)")
    print("    ✅ Food & Nutrition (food groups, nutrients, cuisines)")
    print("    ✅ Sports (popular sports, events, athletes)")
    print("    ✅ Arts & Culture (artists, writers, musicians, wonders)")
    print()
    print("=" * 80)
    print()
    print("  💡 EXAMPLE QUESTIONS JARVIS CAN NOW ANSWER:")
    print()
    print("  Common Sense:")
    print("    - 'Will water flow uphill?'")
    print("    - 'Can I walk through a wall?'")
    print("    - 'Should I say thank you when someone helps?'")
    print("    - 'What happens if I drop a glass?'")
    print()
    print("  General Knowledge:")
    print("    - 'What is the largest continent?'")
    print("    - 'How many planets are in our solar system?'")
    print("    - 'Who painted the Mona Lisa?'")
    print("    - 'What is the capital of France?'")
    print("    - 'How many bones in human body?'")
    print("    - 'What is the fastest land animal?'")
    print()
    print("=" * 80)

def main():
    add_common_sense_knowledge()

if __name__ == "__main__":
    main()
