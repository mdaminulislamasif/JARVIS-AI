"""
Add Flipper Zero Database Memory and Flipper Patcher Information
Adds comprehensive Flipper Zero knowledge to JARVIS database
"""
import sqlite3
import os
import glob
from datetime import datetime

def find_database():
    """Find the most recent working database"""
    # Check for main database first
    if os.path.exists('jarvis_memory.db'):
        try:
            conn = sqlite3.connect('jarvis_memory.db', timeout=5)
            conn.execute("PRAGMA quick_check").fetchall()
            conn.close()
            return 'jarvis_memory.db'
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    # Find most recent fixed database
    fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
    if fixed_dbs:
        fixed_dbs.sort(reverse=True)
        return fixed_dbs[0]
    
    return None

def add_flipper_zero_data(db_path):
    """Add Flipper Zero information to database"""
    print("=" * 70)
    print("  ADDING FLIPPER ZERO DATABASE MEMORY & PATCHER INFO")
    print("=" * 70)
    print(f"\nDatabase: {db_path}\n")
    
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    
    # Add Flipper Zero system information
    print("[1/4] Adding Flipper Zero system information...")
    flipper_system_info = [
        ('flipper_zero_version', 'Flipper Zero - Multi-tool Device', 'hardware'),
        ('flipper_firmware', 'Official/Unleashed/RogueMaster', 'software'),
        ('flipper_storage', 'Internal + microSD support', 'hardware'),
        ('flipper_connectivity', 'USB-C, Bluetooth, Sub-GHz, NFC, RFID, IR', 'hardware'),
        ('flipper_processor', 'STM32WB55 (Cortex-M4 + M0+)', 'hardware'),
        ('flipper_display', '128x64 monochrome LCD', 'hardware'),
        ('flipper_battery', '2000mAh Li-Po', 'hardware'),
        ('flipper_gpio', '18 GPIO pins', 'hardware'),
    ]
    
    for key, value, category in flipper_system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] {key}: {value}")
    
    # Add Flipper Zero knowledge base entries
    print("\n[2/4] Adding Flipper Zero knowledge base...")
    flipper_knowledge = [
        (
            'Flipper Zero Overview',
            'Flipper Zero is a portable multi-tool for pentesters and hardware hackers. '
            'It can interact with various digital systems including RFID, NFC, Sub-GHz, '
            'Infrared, Bluetooth, GPIO, iButton, and more. Features include: '
            'Signal capture and replay, Protocol analysis, Hardware debugging, '
            'BadUSB attacks, GPIO control, U2F authentication.',
            'flipper_basics'
        ),
        (
            'Flipper Zero Frequencies',
            'Sub-GHz Radio Frequencies: 300-348 MHz, 387-464 MHz, 779-928 MHz. '
            'Common uses: Car key fobs (315/433/868/915 MHz), Garage doors, '
            'Weather stations, Wireless doorbells, Remote controls. '
            'Note: Always check local regulations - some frequencies are restricted.',
            'flipper_radio'
        ),
        (
            'Flipper Zero RFID/NFC',
            'RFID: 125 kHz (EM4100, HID Prox, Indala). NFC: 13.56 MHz (ISO14443A/B, '
            'ISO15693, FeliCa). Supported cards: MIFARE Classic, MIFARE Ultralight, '
            'NTAG, DESFire, EMV (read-only). Functions: Read, Write, Emulate, Clone. '
            'Use cases: Access cards, Hotel keys, Transit cards, Payment cards (limited).',
            'flipper_rfid_nfc'
        ),
        (
            'Flipper Zero Infrared',
            'Universal IR remote control. Database includes: TVs, Air conditioners, '
            'Audio systems, Projectors, Fans, LED strips. Features: Learn mode (capture '
            'any IR signal), Universal remote library, Custom signal creation. '
            'Frequency: 800-1000 nm wavelength. Can save and replay IR commands.',
            'flipper_infrared'
        ),
        (
            'Flipper Zero BadUSB',
            'BadUSB: Emulate USB keyboard/mouse for automated attacks. DuckyScript support. '
            'Common payloads: Reverse shells, Data exfiltration, System reconnaissance, '
            'Credential harvesting, Persistence mechanisms. Platforms: Windows, Linux, macOS. '
            'Scripts stored on SD card in /badusb/ folder. Use responsibly and legally!',
            'flipper_badusb'
        ),
        (
            'Flipper Zero GPIO',
            '18 GPIO pins for hardware hacking. Protocols: UART, SPI, I2C, 1-Wire. '
            'Voltage: 3.3V logic level. Features: Logic analyzer, UART terminal, '
            'SPI/I2C sniffer, PWM output, ADC input. Use cases: Hardware debugging, '
            'Firmware dumping, IoT device analysis, Arduino communication.',
            'flipper_gpio'
        ),
        (
            'Flipper Zero iButton',
            'iButton (Dallas/Maxim 1-Wire): Read, Write, Emulate. Common types: '
            'DS1990A (read-only), DS1992-DS1996 (read/write memory), TM2004 (crypto). '
            'Use cases: Building access, Elevator control, Time tracking systems, '
            'Vending machines. Can save keys and emulate them without physical key.',
            'flipper_ibutton'
        ),
        (
            'Flipper Zero Firmware Options',
            '1. Official Firmware: Stable, regular updates, limited features. '
            '2. Unleashed Firmware: More features, removed restrictions, community-driven. '
            '3. RogueMaster: Most features, includes games, extra protocols. '
            '4. Xtreme Firmware: Customizable, performance-focused. '
            'Update via: qFlipper app (official), Web updater, or manual SD card method.',
            'flipper_firmware'
        ),
        (
            'Flipper Zero File Structure',
            'SD Card structure: /badusb/ (BadUSB scripts), /subghz/ (Sub-GHz captures), '
            '/nfc/ (NFC dumps), /rfid/ (RFID dumps), /infrared/ (IR signals), '
            '/ibutton/ (iButton keys), /u2f/ (U2F keys), /apps/ (FAP applications), '
            '/apps_data/ (App data), /music_player/ (RTTTL ringtones).',
            'flipper_files'
        ),
        (
            'Flipper Patcher Overview',
            'Flipper Patcher is a tool for modifying Flipper Zero firmware and applications. '
            'Features: Custom firmware building, App patching, Resource modification, '
            'Animation customization, Icon editing, Manifest editing. '
            'Use cases: Remove region locks, Add custom features, Modify UI, '
            'Enable hidden functions, Create custom builds.',
            'flipper_patcher'
        ),
        (
            'Flipper Patcher Usage',
            'Installation: Download from GitHub, requires Python 3.8+. '
            'Basic usage: python flipper_patcher.py --firmware <path> --patch <patch_file>. '
            'Common patches: Region unlock, Frequency expansion, Feature enablement, '
            'UI modifications. Output: Modified firmware .dfu file. '
            'Flash with: qFlipper or dfu-util. Always backup original firmware!',
            'flipper_patcher_usage'
        ),
        (
            'Flipper Zero Apps',
            'App types: Built-in apps, External apps (.fap files), Plugins. '
            'Popular apps: Snake game, Tetris, Music player, TOTP generator, '
            'WiFi scanner (with ESP32), GPS (with module), Spectrum analyzer, '
            'Signal generator, UART terminal, USB keyboard. '
            'Install: Copy .fap to /apps/ on SD card or use qFlipper.',
            'flipper_apps'
        ),
        (
            'Flipper Zero Security & Legal',
            'LEGAL USE ONLY: Only test on devices you own or have permission to test. '
            'Illegal activities: Cloning access cards without permission, Car key attacks, '
            'Unauthorized network access, Payment card fraud. '
            'Legal uses: Personal device testing, Security research, Educational purposes, '
            'Home automation, Hardware development. Know your local laws regarding '
            'radio frequencies and security testing.',
            'flipper_legal'
        ),
        (
            'Flipper Zero Resources',
            'Official: flipperzero.one, docs.flipperzero.one, forum.flipperzero.one. '
            'GitHub: github.com/flipperdevices, github.com/UberGuidoZ/Flipper. '
            'Communities: Reddit r/flipperzero, Discord servers, Telegram groups. '
            'Tools: qFlipper (official app), Flipper Mobile App (iOS/Android), '
            'Web updater, Python CLI. Databases: Sub-GHz signal database, '
            'IR remote database, NFC card database.',
            'flipper_resources'
        ),
        (
            'Flipper Zero Sub-GHz Protocols',
            'Supported protocols: Princeton, KeeLoq, Star Line, Nice FLO, Came, '
            'Faac SLH, Somfy Telis, Somfy Keytis, Chamberlain, Linear, Megacode, '
            'Security+, BFT Mitto, Holtek, Marantec, Mastercode, Firefly. '
            'Functions: Read RAW, Decode, Save, Emulate, Brute force (some protocols). '
            'Range: Up to 50-100 meters depending on conditions.',
            'flipper_subghz_protocols'
        ),
    ]
    
    for topic, content, source in flipper_knowledge:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    # Add Flipper Zero preferences
    print("\n[3/4] Adding Flipper Zero preferences...")
    flipper_preferences = [
        ('flipper_zero_enabled', 'true'),
        ('flipper_default_firmware', 'unleashed'),
        ('flipper_auto_save', 'true'),
        ('flipper_frequency_analyzer', 'enabled'),
    ]
    
    for key, value in flipper_preferences:
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        print(f"  [+] {key}: {value}")
    
    # Add Flipper Zero command examples
    print("\n[4/4] Adding Flipper Zero command examples...")
    flipper_commands = [
        (
            'Flipper CLI Commands',
            'CLI access via USB serial. Common commands: storage (manage files), '
            'gpio (control GPIO), rfid (RFID operations), nfc (NFC operations), '
            'subghz (Sub-GHz radio), ir (infrared), bt (Bluetooth), power (battery info), '
            'led (control LED), vibro (vibration motor), speaker (sound). '
            'Access: Screen serial terminal or qFlipper CLI.',
            'flipper_cli'
        ),
    ]
    
    for topic, content, source in flipper_commands:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM system_info WHERE key LIKE 'flipper%'")
    sys_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source LIKE 'flipper%'")
    kb_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_preferences WHERE preference_key LIKE 'flipper%'")
    pref_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("  FLIPPER ZERO DATA ADDED SUCCESSFULLY!")
    print("=" * 70)
    print(f"  Database: {os.path.abspath(db_path)}")
    print(f"  Flipper system info: {sys_count} entries")
    print(f"  Flipper knowledge: {kb_count} entries")
    print(f"  Flipper preferences: {pref_count} entries")
    print(f"  Total Flipper data: {sys_count + kb_count + pref_count} entries")
    print("\n  Topics covered:")
    print("  ✅ Flipper Zero hardware specs")
    print("  ✅ Sub-GHz radio & frequencies")
    print("  ✅ RFID/NFC capabilities")
    print("  ✅ Infrared remote control")
    print("  ✅ BadUSB & DuckyScript")
    print("  ✅ GPIO & hardware hacking")
    print("  ✅ iButton support")
    print("  ✅ Firmware options (Official/Unleashed/RogueMaster)")
    print("  ✅ Flipper Patcher usage")
    print("  ✅ Apps & plugins")
    print("  ✅ Security & legal considerations")
    print("  ✅ Resources & communities")
    print("\n  View with: python view_database.py")
    print("=" * 70)

def main():
    print("\n🔧 Flipper Zero Database Integration\n")
    
    db_path = find_database()
    
    if not db_path:
        print("[ERROR] No working database found!")
        print("Run: python fix_database_windows10.py first")
        return
    
    print(f"[INFO] Found database: {db_path}\n")
    
    try:
        add_flipper_zero_data(db_path)
        print("\n✅ SUCCESS! Flipper Zero data has been added to JARVIS database.")
        print("\nYou can now ask JARVIS about:")
        print("  - Flipper Zero features and capabilities")
        print("  - Sub-GHz frequencies and protocols")
        print("  - RFID/NFC card cloning")
        print("  - BadUSB attacks and payloads")
        print("  - Flipper Patcher usage")
        print("  - Firmware options and updates")
        print("  - And much more!")
    except Exception as e:
        print(f"\n[ERROR] Failed to add Flipper Zero data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
