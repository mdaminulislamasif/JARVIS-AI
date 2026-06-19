"""
Add Cyber Attack Menu and Memory to JARVIS Database
Comprehensive cyber security attack knowledge for educational purposes
⚠️ FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY
"""
import sqlite3
import os
import glob
from datetime import datetime

def find_database():
    """Find the most recent working database"""
    if os.path.exists('jarvis_memory.db'):
        try:
            conn = sqlite3.connect('jarvis_memory.db', timeout=5)
            conn.execute("PRAGMA quick_check").fetchall()
            conn.close()
            return 'jarvis_memory.db'
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
    if fixed_dbs:
        fixed_dbs.sort(reverse=True)
        return fixed_dbs[0]
    
    return None

def add_cyber_attack_data(db_path):
    """Add comprehensive cyber attack information to database"""
    print("=" * 80)
    print("  ADDING CYBER ATTACK MENU & MEMORY TO JARVIS DATABASE")
    print("=" * 80)
    print(f"\nDatabase: {db_path}\n")
    print("⚠️  FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY\n")
    
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    
    # Add cyber attack system information
    print("[1/5] Adding cyber attack system information...")
    cyber_system_info = [
        ('cyber_attack_database', 'Comprehensive Cyber Attack Knowledge Base', 'security'),
        ('cyber_defense_mode', 'Educational & Defensive', 'security'),
        ('attack_categories', 'Network, Web, Social, Malware, Physical, Wireless', 'security'),
        ('security_frameworks', 'MITRE ATT&CK, OWASP, NIST', 'security'),
        ('penetration_testing', 'Ethical Hacking Methodologies', 'security'),
        ('vulnerability_assessment', 'CVE, CVSS, CWE Standards', 'security'),
    ]
    
    for key, value, category in cyber_system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] {key}: {value}")
    
    # Add cyber attack knowledge base entries
    print("\n[2/5] Adding cyber attack knowledge base...")
    cyber_knowledge = [
        # Network Attacks
        (
            'Network Attacks - DDoS',
            'Distributed Denial of Service (DDoS): Overwhelm target with traffic. '
            'Types: Volumetric (UDP/ICMP flood), Protocol (SYN flood, Ping of Death), '
            'Application Layer (HTTP flood, Slowloris). Tools: LOIC, HOIC, Hping3. '
            'Defense: Rate limiting, CDN, DDoS mitigation services (Cloudflare, Akamai). '
            'Botnets: Mirai, Emotet. Attack vectors: Amplification (DNS, NTP, Memcached).',
            'cyber_network_attacks'
        ),
        (
            'Network Attacks - Man-in-the-Middle (MITM)',
            'MITM: Intercept communication between two parties. Types: ARP spoofing, '
            'DNS spoofing, SSL stripping, Session hijacking. Tools: Ettercap, Bettercap, '
            'mitmproxy, Wireshark. Techniques: Packet sniffing, Traffic manipulation, '
            'Credential theft. Defense: HTTPS, HSTS, Certificate pinning, VPN, '
            'Network segmentation. Detection: ARP monitoring, SSL/TLS inspection.',
            'cyber_network_attacks'
        ),
        (
            'Network Attacks - Port Scanning & Enumeration',
            'Port Scanning: Discover open ports and services. Tools: Nmap, Masscan, '
            'Unicornscan, Angry IP Scanner. Techniques: TCP SYN scan, UDP scan, '
            'FIN/NULL/Xmas scans, Idle scan. Enumeration: Banner grabbing, Service '
            'version detection, OS fingerprinting. Defense: Firewall rules, Port knocking, '
            'IDS/IPS (Snort, Suricata). Stealth: Fragmentation, Decoy scanning.',
            'cyber_network_attacks'
        ),
        
        # Web Application Attacks
        (
            'Web Attacks - SQL Injection (SQLi)',
            'SQL Injection: Inject malicious SQL queries. Types: In-band (Error-based, '
            'Union-based), Blind (Boolean, Time-based), Out-of-band. Tools: sqlmap, '
            'Havij, jSQL Injection. Payloads: OR 1=1, UNION SELECT, Time delays. '
            'Advanced: Second-order SQLi, NoSQL injection. Defense: Prepared statements, '
            'Parameterized queries, Input validation, WAF, Least privilege DB access.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - Cross-Site Scripting (XSS)',
            'XSS: Inject malicious scripts into web pages. Types: Stored (Persistent), '
            'Reflected (Non-persistent), DOM-based. Payloads: <script>alert(1)</script>, '
            'Cookie theft, Keylogging, Phishing. Tools: XSSer, BeEF, Burp Suite. '
            'Bypass: Encoding (HTML, URL, Unicode), Filter evasion. Defense: Input '
            'sanitization, Output encoding, CSP headers, HTTPOnly cookies, X-XSS-Protection.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - Cross-Site Request Forgery (CSRF)',
            'CSRF: Force authenticated users to execute unwanted actions. Attack: '
            'Malicious link/form triggers action on victim\'s behalf. Targets: State-changing '
            'operations (transfer money, change password). Defense: CSRF tokens, '
            'SameSite cookies, Referer validation, Double submit cookies. Tools: Burp Suite, '
            'OWASP CSRFTester. Impact: Account takeover, Unauthorized transactions.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - Remote Code Execution (RCE)',
            'RCE: Execute arbitrary code on target system. Vectors: File upload vulnerabilities, '
            'Deserialization flaws, Command injection, Template injection. Tools: Metasploit, '
            'Commix, Weevely. Techniques: Web shells (PHP, ASP, JSP), Reverse shells, '
            'Bind shells. Defense: Input validation, Sandboxing, Disable dangerous functions, '
            'File type validation, WAF. Common targets: WordPress, Drupal, Joomla.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - Local/Remote File Inclusion (LFI/RFI)',
            'LFI: Include local files on server. RFI: Include remote files. Targets: '
            'PHP include(), require(). Payloads: ../../../../etc/passwd, Log poisoning, '
            'PHP wrappers (php://filter, data://). Defense: Whitelist allowed files, '
            'Disable allow_url_include, Input validation. Tools: Fimap, Kadimus. '
            'Exploitation: Read sensitive files, RCE via log poisoning.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - XML External Entity (XXE)',
            'XXE: Exploit XML parsers to access files/systems. Attack: Inject malicious '
            'XML entities. Impact: File disclosure, SSRF, DoS, RCE. Payloads: '
            '<!ENTITY xxe SYSTEM "file:///etc/passwd">. Defense: Disable external entities, '
            'Use JSON instead of XML, Input validation, Update XML parsers. '
            'Tools: Burp Suite, XXEinjector. Targets: SOAP, REST APIs, File uploads.',
            'cyber_web_attacks'
        ),
        
        # Social Engineering
        (
            'Social Engineering - Phishing',
            'Phishing: Fraudulent emails/messages to steal credentials. Types: Spear '
            'phishing (targeted), Whaling (executives), Vishing (voice), Smishing (SMS). '
            'Techniques: Spoofed sender, Urgent language, Fake login pages, Malicious '
            'attachments. Tools: SET (Social Engineering Toolkit), Gophish, King Phisher. '
            'Defense: Email filtering, User training, 2FA, DMARC/SPF/DKIM, Link scanning.',
            'cyber_social_engineering'
        ),
        (
            'Social Engineering - Pretexting & Baiting',
            'Pretexting: Create false scenario to gain trust. Baiting: Offer something '
            'enticing (USB drive, free software). Techniques: Impersonation (IT support, '
            'vendor), Authority exploitation, Curiosity exploitation. Physical: Tailgating, '
            'Dumpster diving. Defense: Verification procedures, Security awareness, '
            'Access controls, Clean desk policy. Famous: Kevin Mitnick attacks.',
            'cyber_social_engineering'
        ),
        
        # Malware
        (
            'Malware - Ransomware',
            'Ransomware: Encrypt files and demand payment. Types: Crypto (encrypt), '
            'Locker (lock system), Scareware (fake). Famous: WannaCry, Petya, Ryuk, '
            'REvil, LockBit. Delivery: Phishing, RDP brute force, Exploit kits. '
            'Defense: Backups (3-2-1 rule), Patch management, Email filtering, EDR, '
            'Network segmentation. Payment: Bitcoin, Monero. Recovery: No guarantee.',
            'cyber_malware'
        ),
        (
            'Malware - Trojans & RATs',
            'Trojan: Disguised malicious software. RAT (Remote Access Trojan): Remote '
            'control of infected system. Famous: Zeus, Emotet, DarkComet, njRAT. '
            'Capabilities: Keylogging, Screen capture, File theft, Webcam access, '
            'Cryptocurrency mining. Delivery: Email attachments, Fake software, Drive-by '
            'downloads. Defense: Antivirus, Application whitelisting, User awareness.',
            'cyber_malware'
        ),
        (
            'Malware - Rootkits & Bootkits',
            'Rootkit: Hide malware presence at OS level. Bootkit: Infect boot process. '
            'Types: User-mode, Kernel-mode, Firmware. Techniques: Hook system calls, '
            'Hide processes/files, Disable security tools. Famous: Sony BMG rootkit, '
            'TDL4, Stuxnet. Detection: Rootkit scanners (GMER, RootkitRevealer), '
            'Memory forensics. Defense: Secure Boot, UEFI protection, Integrity checking.',
            'cyber_malware'
        ),
        (
            'Malware - Worms & Viruses',
            'Worm: Self-replicating malware spreading across networks. Virus: Infects '
            'files/programs. Famous worms: Morris, ILOVEYOU, Conficker, Stuxnet. '
            'Propagation: Email, Network shares, USB drives, Exploits. Impact: Network '
            'congestion, Data theft, System damage. Defense: Patching, Network segmentation, '
            'Antivirus, Disable AutoRun, Email filtering.',
            'cyber_malware'
        ),
        
        # Password Attacks
        (
            'Password Attacks - Brute Force & Dictionary',
            'Brute Force: Try all possible combinations. Dictionary: Try common passwords. '
            'Tools: Hydra, Medusa, John the Ripper, Hashcat, Burp Intruder. Targets: '
            'SSH, RDP, FTP, Web logins, Hash cracking. Wordlists: rockyou.txt, SecLists. '
            'Techniques: Hybrid attacks, Rule-based mutations. Defense: Account lockout, '
            'Rate limiting, Strong passwords, 2FA, CAPTCHA.',
            'cyber_password_attacks'
        ),
        (
            'Password Attacks - Credential Stuffing & Spraying',
            'Credential Stuffing: Use leaked credentials on multiple sites. Password '
            'Spraying: Try common passwords against many accounts. Tools: Sentry MBA, '
            'STORM, Burp Suite. Sources: Data breaches (Have I Been Pwned). Defense: '
            'Breach monitoring, 2FA, Password managers, Account lockout policies, '
            'Anomaly detection. Impact: Account takeover, Data theft.',
            'cyber_password_attacks'
        ),
        (
            'Password Attacks - Hash Cracking',
            'Hash Cracking: Reverse password hashes. Types: MD5, SHA1, SHA256, bcrypt, '
            'NTLM. Methods: Rainbow tables, GPU cracking, Cloud cracking. Tools: Hashcat, '
            'John the Ripper, oclHashcat. Techniques: Mask attacks, Combinator attacks. '
            'Defense: Strong hashing (bcrypt, Argon2), Salting, Peppering, Key stretching. '
            'Speed: MD5 (billions/sec), bcrypt (thousands/sec).',
            'cyber_password_attacks'
        ),
        
        # Wireless Attacks
        (
            'Wireless Attacks - WiFi Cracking',
            'WiFi Cracking: Break wireless encryption. Targets: WEP (weak), WPA/WPA2-PSK, '
            'WPA3. Tools: Aircrack-ng, Reaver, Wifite, Hashcat. Techniques: Deauth attack, '
            'Handshake capture, PMKID attack, WPS PIN attack. Defense: WPA3, Strong '
            'passwords, Disable WPS, MAC filtering (weak), Hidden SSID (weak), '
            '802.1X authentication. Hardware: WiFi adapters with monitor mode.',
            'cyber_wireless_attacks'
        ),
        (
            'Wireless Attacks - Evil Twin & Rogue AP',
            'Evil Twin: Fake access point mimicking legitimate one. Rogue AP: Unauthorized '
            'AP on network. Attack: Capture credentials, MITM, Malware distribution. '
            'Tools: Airbase-ng, hostapd, WiFi Pineapple. Techniques: Stronger signal, '
            'Deauth legitimate AP, Captive portal. Defense: 802.1X, Certificate validation, '
            'Wireless IDS, AP monitoring, User awareness.',
            'cyber_wireless_attacks'
        ),
        (
            'Wireless Attacks - Bluetooth & RFID',
            'Bluetooth: Bluejacking (spam), Bluesnarfing (data theft), Bluebugging (control). '
            'Tools: Bluesniff, btscanner, Ubertooth. RFID: Cloning, Eavesdropping, Relay '
            'attacks. Tools: Proxmark3, Chameleon Mini, HackRF. Defense: Disable when not '
            'in use, Pairing authentication, RFID shielding, Encrypted tags.',
            'cyber_wireless_attacks'
        ),
        
        # Advanced Persistent Threats (APT)
        (
            'Advanced Persistent Threats (APT)',
            'APT: Long-term targeted attacks by sophisticated actors. Phases: Reconnaissance, '
            'Initial compromise, Establish foothold, Escalate privileges, Internal recon, '
            'Lateral movement, Maintain presence, Complete mission. Famous: APT28 (Fancy Bear), '
            'APT29 (Cozy Bear), Lazarus Group, Equation Group. Techniques: Zero-days, '
            'Custom malware, Living off the land. Defense: Threat intelligence, EDR, '
            'Network segmentation, Incident response plan.',
            'cyber_apt'
        ),
        
        # Exploitation Frameworks
        (
            'Exploitation Frameworks - Metasploit',
            'Metasploit: Comprehensive penetration testing framework. Components: Exploits, '
            'Payloads, Auxiliary modules, Post-exploitation. Payloads: Meterpreter (advanced), '
            'Shell (basic), VNC, Reverse/Bind shells. Features: Exploit development, '
            'Payload generation, Post-exploitation, Pivoting. Usage: msfconsole, msfvenom. '
            'Modules: 2000+ exploits, 500+ payloads. Defense: Patch vulnerabilities, '
            'IDS/IPS signatures, Endpoint protection.',
            'cyber_exploitation'
        ),
        (
            'Exploitation Frameworks - Cobalt Strike & Empire',
            'Cobalt Strike: Commercial adversary simulation tool. Features: Beacon (payload), '
            'Malleable C2, Lateral movement, Privilege escalation. Empire: PowerShell '
            'post-exploitation framework. Techniques: Living off the land, Fileless attacks, '
            'In-memory execution. Defense: PowerShell logging, Application whitelisting, '
            'Behavioral analysis, EDR. Note: Often used by red teams and threat actors.',
            'cyber_exploitation'
        ),
        
        # Web Reconnaissance
        (
            'Reconnaissance - OSINT & Information Gathering',
            'OSINT: Open Source Intelligence gathering. Tools: theHarvester, Maltego, '
            'Shodan, Censys, Recon-ng, SpiderFoot. Techniques: Google dorking, WHOIS lookup, '
            'DNS enumeration, Social media mining, Metadata extraction. Targets: Email '
            'addresses, Subdomains, Employee info, Technologies used, Network ranges. '
            'Defense: Minimize public exposure, Monitor mentions, Data classification.',
            'cyber_reconnaissance'
        ),
        (
            'Reconnaissance - Vulnerability Scanning',
            'Vulnerability Scanning: Identify security weaknesses. Tools: Nessus, OpenVAS, '
            'Qualys, Nexpose, Nikto (web). Techniques: Port scanning, Service detection, '
            'Version identification, CVE matching. Output: CVSS scores, Remediation advice. '
            'Types: Network scans, Web app scans, Database scans. Defense: Regular scanning, '
            'Patch management, Vulnerability management program.',
            'cyber_reconnaissance'
        ),
        
        # Privilege Escalation
        (
            'Privilege Escalation - Windows',
            'Windows PrivEsc: Gain higher privileges. Techniques: Unquoted service paths, '
            'AlwaysInstallElevated, Token impersonation, DLL hijacking, Kernel exploits. '
            'Tools: PowerUp, WinPEAS, Sherlock, Watson. Targets: Misconfigured services, '
            'Weak permissions, Stored credentials, Scheduled tasks. Defense: Least privilege, '
            'Patch management, Audit permissions, Credential Guard.',
            'cyber_privilege_escalation'
        ),
        (
            'Privilege Escalation - Linux',
            'Linux PrivEsc: Gain root access. Techniques: SUID binaries, Sudo misconfig, '
            'Cron jobs, Kernel exploits, Capabilities abuse, NFS shares. Tools: LinPEAS, '
            'LinEnum, Linux Exploit Suggester. Targets: /etc/passwd, /etc/shadow, '
            'Writable scripts, PATH hijacking. Defense: Minimal SUID, Sudo restrictions, '
            'Kernel updates, File permissions, SELinux/AppArmor.',
            'cyber_privilege_escalation'
        ),
        
        # Persistence Mechanisms
        (
            'Persistence Mechanisms',
            'Persistence: Maintain access after reboot/detection. Windows: Registry Run keys, '
            'Scheduled tasks, Services, WMI event subscriptions, DLL hijacking. Linux: '
            'Cron jobs, .bashrc, systemd services, SSH keys, LD_PRELOAD. Techniques: '
            'Backdoor accounts, Web shells, Rootkits. Defense: Autoruns monitoring, '
            'File integrity monitoring, Baseline comparison, EDR.',
            'cyber_persistence'
        ),
        
        # Defense & Mitigation
        (
            'Defense - Security Best Practices',
            'Defense in Depth: Multiple security layers. Practices: Patch management, '
            'Least privilege, Network segmentation, Strong authentication (2FA/MFA), '
            'Encryption (at rest/in transit), Security awareness training, Incident response '
            'plan, Regular backups, Log monitoring, Vulnerability scanning. Frameworks: '
            'NIST Cybersecurity Framework, CIS Controls, ISO 27001.',
            'cyber_defense'
        ),
        (
            'Defense - Detection & Response',
            'Detection: IDS/IPS (Snort, Suricata), SIEM (Splunk, ELK), EDR (CrowdStrike, '
            'Carbon Black), Network monitoring, Log analysis. Response: Incident response '
            'plan, Forensics, Containment, Eradication, Recovery, Lessons learned. '
            'Tools: Wireshark, Volatility, Autopsy, FTK. Threat hunting: Proactive '
            'search for threats. IOCs: Indicators of Compromise.',
            'cyber_defense'
        ),
        
        # Penetration Testing
        (
            'Penetration Testing Methodology',
            'Phases: 1. Planning & Reconnaissance, 2. Scanning & Enumeration, 3. Gaining '
            'Access, 4. Maintaining Access, 5. Covering Tracks, 6. Reporting. Types: '
            'Black box (no knowledge), White box (full knowledge), Gray box (partial). '
            'Standards: PTES, OWASP, OSSTMM. Certifications: OSCP, CEH, GPEN. '
            'Tools: Kali Linux, Parrot OS. Ethics: Authorization, Scope, Confidentiality.',
            'cyber_pentest'
        ),
        
        # MITRE ATT&CK Framework
        (
            'MITRE ATT&CK Framework',
            'ATT&CK: Knowledge base of adversary tactics and techniques. Tactics: '
            'Reconnaissance, Resource Development, Initial Access, Execution, Persistence, '
            'Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral '
            'Movement, Collection, Command and Control, Exfiltration, Impact. Use: Threat '
            'intelligence, Detection engineering, Red/Blue team exercises. Matrices: '
            'Enterprise, Mobile, ICS. Website: attack.mitre.org',
            'cyber_frameworks'
        ),
    ]
    
    for topic, content, source in cyber_knowledge:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    # Add cyber attack preferences
    print("\n[3/5] Adding cyber attack preferences...")
    cyber_preferences = [
        ('cyber_attack_mode', 'educational_defensive'),
        ('security_framework', 'MITRE_ATT&CK'),
        ('pentest_methodology', 'PTES'),
        ('ethical_hacking', 'authorized_only'),
    ]
    
    for key, value in cyber_preferences:
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        print(f"  [+] {key}: {value}")
    
    # Add cyber attack tools reference
    print("\n[4/5] Adding cyber attack tools reference...")
    cyber_tools = [
        (
            'Cyber Attack Tools - Network',
            'Network Tools: Nmap (port scanning), Wireshark (packet analysis), '
            'Metasploit (exploitation), Burp Suite (web testing), Aircrack-ng (WiFi), '
            'Ettercap (MITM), Nessus (vulnerability scanning), Hydra (password cracking), '
            'sqlmap (SQL injection), John the Ripper (password cracking), Hashcat (hash '
            'cracking), Nikto (web scanning), OWASP ZAP (web security).',
            'cyber_tools'
        ),
        (
            'Cyber Attack Tools - Operating Systems',
            'Security Distributions: Kali Linux (most popular, 600+ tools), Parrot OS '
            '(privacy-focused), BlackArch (2800+ tools), BackBox (Ubuntu-based), '
            'Pentoo (Gentoo-based). Features: Pre-installed tools, Customized kernel, '
            'Forensics mode, Persistence. Usage: Live boot, Virtual machine, Dual boot. '
            'Updates: Regular tool updates, Community support.',
            'cyber_tools'
        ),
    ]
    
    for topic, content, source in cyber_tools:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    # Add legal and ethical warnings
    print("\n[5/5] Adding legal and ethical guidelines...")
    legal_warnings = [
        (
            'LEGAL WARNING - Cyber Attacks',
            '⚠️ CRITICAL: Unauthorized computer access is ILLEGAL in most jurisdictions. '
            'Laws: Computer Fraud and Abuse Act (USA), Computer Misuse Act (UK), '
            'Cybercrime laws worldwide. Penalties: Fines, imprisonment, civil liability. '
            'LEGAL USES ONLY: Authorized penetration testing, Security research on own '
            'systems, Educational labs, Bug bounty programs, Defensive security. '
            'ALWAYS: Get written authorization, Define scope, Follow rules of engagement, '
            'Maintain confidentiality. This knowledge is for DEFENSE and EDUCATION ONLY.',
            'cyber_legal'
        ),
        (
            'Ethical Hacking Guidelines',
            'Ethics: 1. Authorization: Always get written permission. 2. Scope: Stay within '
            'defined boundaries. 3. Confidentiality: Protect discovered information. '
            '4. Disclosure: Report vulnerabilities responsibly. 5. No harm: Avoid damage '
            'to systems. 6. Professionalism: Follow industry standards. Certifications: '
            'CEH Code of Ethics, OSCP requirements. Responsible disclosure: 90-day window, '
            'Vendor notification, Public disclosure after fix.',
            'cyber_legal'
        ),
    ]
    
    for topic, content, source in legal_warnings:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM system_info WHERE category = 'security'")
    sys_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source LIKE 'cyber_%'")
    kb_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_preferences WHERE preference_key LIKE 'cyber_%' OR preference_key LIKE '%security%' OR preference_key LIKE '%ethical%'")
    pref_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("\n" + "=" * 80)
    print("  CYBER ATTACK MENU & MEMORY ADDED SUCCESSFULLY!")
    print("=" * 80)
    print(f"  Database: {os.path.abspath(db_path)}")
    print(f"  Cyber system info: {sys_count} entries")
    print(f"  Cyber knowledge: {kb_count} entries")
    print(f"  Cyber preferences: {pref_count} entries")
    print(f"  Total cyber data: {sys_count + kb_count + pref_count} entries")
    print("\n  Attack Categories Covered:")
    print("  ✅ Network Attacks (DDoS, MITM, Port Scanning)")
    print("  ✅ Web Application Attacks (SQLi, XSS, CSRF, RCE, LFI/RFI, XXE)")
    print("  ✅ Social Engineering (Phishing, Pretexting, Baiting)")
    print("  ✅ Malware (Ransomware, Trojans, RATs, Rootkits, Worms)")
    print("  ✅ Password Attacks (Brute Force, Credential Stuffing, Hash Cracking)")
    print("  ✅ Wireless Attacks (WiFi Cracking, Evil Twin, Bluetooth, RFID)")
    print("  ✅ Advanced Persistent Threats (APT)")
    print("  ✅ Exploitation Frameworks (Metasploit, Cobalt Strike)")
    print("  ✅ Reconnaissance (OSINT, Vulnerability Scanning)")
    print("  ✅ Privilege Escalation (Windows, Linux)")
    print("  ✅ Persistence Mechanisms")
    print("  ✅ Defense & Mitigation Strategies")
    print("  ✅ Penetration Testing Methodology")
    print("  ✅ MITRE ATT&CK Framework")
    print("  ✅ Security Tools & Operating Systems")
    print("  ✅ Legal & Ethical Guidelines")
    print("\n  ⚠️  FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY")
    print("  View with: python view_cyber_attacks.py")
    print("=" * 80)

def main():
    print("\n🔒 Cyber Attack Menu & Memory Integration\n")
    
    db_path = find_database()
    
    if not db_path:
        print("[ERROR] No working database found!")
        print("Run: python fix_database_windows10.py first")
        return
    
    print(f"[INFO] Found database: {db_path}\n")
    
    try:
        add_cyber_attack_data(db_path)
        print("\n✅ SUCCESS! Cyber attack menu and memory added to JARVIS database.")
        print("\n⚠️  IMPORTANT LEGAL NOTICE:")
        print("  This information is for EDUCATIONAL and DEFENSIVE purposes only.")
        print("  Unauthorized access to computer systems is ILLEGAL.")
        print("  Always obtain written authorization before testing.")
        print("\nYou can now ask JARVIS about:")
        print("  - Types of cyber attacks and how they work")
        print("  - Defense and mitigation strategies")
        print("  - Penetration testing methodologies")
        print("  - Security tools and frameworks")
        print("  - Ethical hacking guidelines")
    except Exception as e:
        print(f"\n[ERROR] Failed to add cyber attack data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
