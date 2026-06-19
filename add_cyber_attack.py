"""
Add Cyber Attack Memory to JARVIS Database
Comprehensive cybersecurity attack knowledge for educational and authorized testing
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
    print("=" * 70)
    print("  ADDING CYBER ATTACK MEMORY TO JARVIS DATABASE")
    print("=" * 70)
    print(f"\nDatabase: {db_path}\n")
    
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    
    # Add cyber attack system information
    print("[1/4] Adding cyber attack system information...")
    cyber_system_info = [
        ('cyber_security_version', 'JARVIS CyberSec v2.0', 'software'),
        ('attack_database_version', '2026.05.04', 'software'),
        ('security_framework', 'MITRE ATT&CK, OWASP, NIST', 'software'),
        ('penetration_testing', 'Enabled for authorized testing', 'security'),
        ('threat_intelligence', 'Active monitoring enabled', 'security'),
        ('vulnerability_scanning', 'Automated scanning available', 'security'),
        ('incident_response', 'IR protocols loaded', 'security'),
        ('forensics_tools', 'Digital forensics ready', 'security'),
    ]
    
    for key, value, category in cyber_system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] {key}: {value}")
    
    # Add cyber attack knowledge base entries
    print("\n[2/4] Adding cyber attack knowledge base...")
    cyber_knowledge = [
        # Attack Categories
        (
            'Cyber Attack Categories - Overview',
            'Main attack categories: 1) Network Attacks (DoS, DDoS, MitM, Sniffing), '
            '2) Web Application Attacks (SQL Injection, XSS, CSRF, RCE), '
            '3) Social Engineering (Phishing, Pretexting, Baiting), '
            '4) Malware (Ransomware, Trojans, Worms, Rootkits), '
            '5) Password Attacks (Brute Force, Dictionary, Rainbow Tables), '
            '6) Wireless Attacks (Evil Twin, WPA/WEP cracking), '
            '7) Physical Attacks (USB drops, Tailgating, Dumpster diving).',
            'cyber_overview'
        ),
        
        # Network Attacks
        (
            'Network Attacks - DoS and DDoS',
            'Denial of Service (DoS): Overwhelm target with traffic. Types: SYN Flood, '
            'UDP Flood, ICMP Flood, HTTP Flood, Slowloris. DDoS (Distributed): Multiple '
            'sources attack simultaneously. Tools: LOIC, HOIC, hping3, Slowloris. '
            'Defense: Rate limiting, Traffic filtering, CDN, DDoS protection services. '
            'Detection: Unusual traffic patterns, High bandwidth usage, Service degradation.',
            'cyber_network_attacks'
        ),
        (
            'Network Attacks - Man-in-the-Middle (MitM)',
            'MitM: Intercept communication between two parties. Types: ARP Spoofing, '
            'DNS Spoofing, SSL Stripping, Session Hijacking. Tools: Ettercap, Bettercap, '
            'mitmproxy, Wireshark. Techniques: ARP poisoning, DHCP spoofing, Rogue AP. '
            'Defense: Encryption (TLS/SSL), Certificate pinning, VPN, HTTPS everywhere. '
            'Detection: Certificate warnings, Unexpected network behavior, ARP table anomalies.',
            'cyber_network_attacks'
        ),
        (
            'Network Attacks - Packet Sniffing',
            'Packet Sniffing: Capture and analyze network traffic. Tools: Wireshark, '
            'tcpdump, Ettercap, NetworkMiner, Kismet. Protocols vulnerable: HTTP, FTP, '
            'Telnet, SMTP (unencrypted). Data captured: Passwords, Cookies, Session tokens, '
            'Sensitive data. Defense: Encryption (TLS/SSL), VPN, Secure protocols (HTTPS, SFTP). '
            'Legal: Only on networks you own or have authorization.',
            'cyber_network_attacks'
        ),
        
        # Web Application Attacks
        (
            'Web Attacks - SQL Injection (SQLi)',
            'SQL Injection: Insert malicious SQL code into queries. Types: Classic SQLi, '
            'Blind SQLi, Time-based SQLi, Union-based SQLi. Impact: Data theft, Authentication '
            'bypass, Data modification, Server compromise. Tools: sqlmap, Havij, jSQL Injection. '
            'Example: \' OR 1=1-- , UNION SELECT username,password FROM users. '
            'Defense: Parameterized queries, Input validation, WAF, Least privilege DB access. '
            'Detection: SQL errors in logs, Unusual query patterns.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - Cross-Site Scripting (XSS)',
            'XSS: Inject malicious scripts into web pages. Types: Stored XSS (persistent), '
            'Reflected XSS (non-persistent), DOM-based XSS. Impact: Session hijacking, '
            'Cookie theft, Phishing, Defacement. Payloads: <script>alert(1)</script>, '
            'Cookie stealing, Keyloggers. Tools: XSSer, BeEF, Burp Suite. '
            'Defense: Input sanitization, Output encoding, CSP headers, HTTPOnly cookies. '
            'Detection: Unusual script tags, Encoded payloads in URLs.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - Remote Code Execution (RCE)',
            'RCE: Execute arbitrary code on target system. Vectors: File upload vulnerabilities, '
            'Deserialization flaws, Command injection, Template injection. Impact: Full system '
            'compromise, Data theft, Malware installation. Examples: PHP shell upload, '
            'eval() exploitation, OS command injection. Tools: Metasploit, Weevely, Commix. '
            'Defense: Input validation, Disable dangerous functions, Sandboxing, WAF. '
            'Detection: Unexpected processes, File system changes, Outbound connections.',
            'cyber_web_attacks'
        ),
        (
            'Web Attacks - CSRF and SSRF',
            'CSRF (Cross-Site Request Forgery): Force authenticated user to perform unwanted '
            'actions. Impact: Unauthorized transactions, Account changes, Data modification. '
            'Defense: CSRF tokens, SameSite cookies, Referer validation. '
            'SSRF (Server-Side Request Forgery): Make server perform requests to internal resources. '
            'Impact: Internal network scanning, Cloud metadata access, Port scanning. '
            'Defense: Whitelist URLs, Disable unnecessary protocols, Network segmentation.',
            'cyber_web_attacks'
        ),
        
        # Password Attacks
        (
            'Password Attacks - Brute Force and Dictionary',
            'Brute Force: Try all possible combinations. Dictionary Attack: Try common passwords '
            'from wordlists. Tools: Hydra, Medusa, John the Ripper, Hashcat, Burp Intruder. '
            'Targets: SSH, FTP, RDP, Web logins, Hash cracking. Wordlists: rockyou.txt, '
            'SecLists, CrackStation. Defense: Account lockout, Rate limiting, Strong passwords, '
            'MFA, CAPTCHA. Detection: Multiple failed login attempts, Unusual login patterns.',
            'cyber_password_attacks'
        ),
        (
            'Password Attacks - Hash Cracking',
            'Hash Cracking: Reverse password hashes. Hash types: MD5, SHA1, SHA256, bcrypt, '
            'NTLM. Methods: Dictionary attack, Rainbow tables, Brute force, Hybrid attacks. '
            'Tools: Hashcat, John the Ripper, RainbowCrack, Ophcrack. GPU acceleration: '
            'Significantly faster cracking. Defense: Strong hashing (bcrypt, Argon2), Salt, '
            'Pepper, Key stretching. Online tools: CrackStation, HashKiller (for testing only).',
            'cyber_password_attacks'
        ),
        (
            'Password Attacks - Credential Stuffing',
            'Credential Stuffing: Use leaked credentials on multiple sites. Source: Data breaches, '
            'Paste sites, Dark web. Tools: Sentry MBA, SNIPR, OpenBullet. Impact: Account takeover, '
            'Identity theft, Financial fraud. Defense: Password uniqueness, MFA, Breach monitoring, '
            'CAPTCHA, Rate limiting. Check breaches: haveibeenpwned.com, DeHashed.',
            'cyber_password_attacks'
        ),
        
        # Social Engineering
        (
            'Social Engineering - Phishing',
            'Phishing: Fraudulent emails/messages to steal credentials. Types: Spear phishing '
            '(targeted), Whaling (executives), Smishing (SMS), Vishing (voice). Techniques: '
            'Spoofed sender, Urgent language, Fake links, Malicious attachments. Tools: '
            'SET (Social Engineering Toolkit), Gophish, King Phisher. Defense: Email filtering, '
            'User training, Link verification, MFA, Anti-phishing tools. Red flags: Urgency, '
            'Suspicious links, Grammar errors, Unexpected attachments.',
            'cyber_social_engineering'
        ),
        (
            'Social Engineering - Pretexting and Baiting',
            'Pretexting: Create false scenario to gain trust. Examples: Fake IT support, '
            'Impersonation, Authority exploitation. Baiting: Offer something enticing. '
            'Examples: Free USB drives, Fake software, Prize scams. Physical: USB drops in '
            'parking lots, Infected media. Defense: Verification procedures, Security awareness, '
            'USB blocking, Incident reporting. Psychology: Exploits trust, curiosity, fear, greed.',
            'cyber_social_engineering'
        ),
        
        # Malware
        (
            'Malware - Ransomware',
            'Ransomware: Encrypt files and demand payment. Famous: WannaCry, Petya, Ryuk, '
            'LockBit, REvil. Delivery: Phishing emails, RDP exploitation, Drive-by downloads. '
            'Impact: Data encryption, Business disruption, Financial loss. Defense: Backups '
            '(offline), Patch management, Email filtering, EDR, Network segmentation. '
            'Response: Isolate infected systems, DO NOT pay ransom, Restore from backups, '
            'Report to authorities. Prevention: Regular backups, Security training, MFA on RDP.',
            'cyber_malware'
        ),
        (
            'Malware - Trojans and RATs',
            'Trojan: Disguised malicious software. Types: Backdoor, Banking, Downloader, '
            'Infostealer. RAT (Remote Access Trojan): Full remote control. Famous: DarkComet, '
            'njRAT, Poison Ivy, Cobalt Strike. Capabilities: Keylogging, Screen capture, '
            'File access, Webcam control, Command execution. Defense: Antivirus, EDR, '
            'Application whitelisting, Network monitoring. Detection: Unusual processes, '
            'Outbound connections, Registry changes.',
            'cyber_malware'
        ),
        (
            'Malware - Rootkits and Bootkits',
            'Rootkit: Hide malware presence at OS level. Types: User-mode, Kernel-mode, '
            'Bootkit (firmware). Capabilities: Process hiding, File hiding, Network hiding, '
            'Keylogging. Famous: Sony BMG rootkit, Stuxnet, TDL4. Detection: Rootkit scanners '
            '(GMER, RootkitRevealer), Behavioral analysis, Memory forensics. Defense: Secure boot, '
            'UEFI protection, Integrity monitoring, Regular scans. Removal: Often requires '
            'clean OS reinstall.',
            'cyber_malware'
        ),
        
        # Wireless Attacks
        (
            'Wireless Attacks - WiFi Cracking',
            'WiFi Cracking: Break wireless encryption. WEP: Weak, easily cracked (aircrack-ng). '
            'WPA/WPA2: Capture handshake, offline cracking. WPA3: More secure, SAE. '
            'Tools: Aircrack-ng suite, Wifite, Reaver (WPS), Hashcat, Fern WiFi Cracker. '
            'Techniques: Deauth attack, Handshake capture, Dictionary attack, Pixie dust (WPS). '
            'Defense: WPA3, Strong passwords, Disable WPS, MAC filtering, Hidden SSID. '
            'Hardware: WiFi adapter with monitor mode (Alfa AWUS036ACH).',
            'cyber_wireless_attacks'
        ),
        (
            'Wireless Attacks - Evil Twin and Rogue AP',
            'Evil Twin: Fake access point mimicking legitimate one. Rogue AP: Unauthorized AP '
            'on network. Purpose: Credential theft, Traffic interception, MitM attacks. '
            'Tools: Airbase-ng, hostapd, WiFi Pineapple, Fluxion. Techniques: Deauth legitimate AP, '
            'Stronger signal, Captive portal. Defense: 802.1X authentication, Certificate validation, '
            'Wireless IDS, User awareness. Detection: Multiple APs with same SSID, Signal anomalies.',
            'cyber_wireless_attacks'
        ),
        
        # Exploitation Frameworks
        (
            'Exploitation - Metasploit Framework',
            'Metasploit: Comprehensive penetration testing framework. Components: Exploits, '
            'Payloads, Auxiliary modules, Post-exploitation. Usage: msfconsole, search exploits, '
            'set options, exploit. Payloads: Meterpreter (interactive shell), Reverse shells, '
            'Bind shells. Features: Exploit database, Payload generation, Post-exploitation, '
            'Pivoting. Modules: exploit/windows/smb/ms17_010_eternalblue. Defense: Patch management, '
            'IDS/IPS, Network segmentation, EDR.',
            'cyber_exploitation'
        ),
        (
            'Exploitation - Payload Generation',
            'Payload Generation: Create malicious executables. Tools: msfvenom, Veil, '
            'TheFatRat, Shellter. Formats: EXE, DLL, APK, MSI, Office macros. Encoders: '
            'Bypass AV detection. Examples: msfvenom -p windows/meterpreter/reverse_tcp. '
            'Obfuscation: Encoding, Encryption, Packing. Delivery: Phishing, USB drops, '
            'Web downloads. Defense: Antivirus, EDR, Application whitelisting, Email filtering. '
            'Detection: Behavioral analysis, Sandbox execution.',
            'cyber_exploitation'
        ),
        
        # Reconnaissance
        (
            'Reconnaissance - Information Gathering',
            'Recon: Gather information about target. Passive: OSINT, Google dorking, WHOIS, '
            'DNS records, Social media. Active: Port scanning, Service enumeration, Vulnerability '
            'scanning. Tools: Nmap, Shodan, theHarvester, Maltego, Recon-ng, SpiderFoot. '
            'Google Dorks: site:, filetype:, inurl:, intitle:. DNS: nslookup, dig, dnsenum. '
            'WHOIS: Domain registration info. Shodan: Internet-connected device search engine.',
            'cyber_reconnaissance'
        ),
        (
            'Reconnaissance - Port Scanning',
            'Port Scanning: Discover open ports and services. Tools: Nmap, Masscan, Unicornscan. '
            'Scan types: TCP SYN (stealth), TCP Connect, UDP, FIN, NULL, Xmas. Nmap commands: '
            'nmap -sS (SYN scan), -sV (version detection), -O (OS detection), -A (aggressive). '
            'Service enumeration: Banner grabbing, Version detection. Defense: Firewall, '
            'Port filtering, IDS, Minimal services. Detection: IDS alerts, Firewall logs.',
            'cyber_reconnaissance'
        ),
        
        # Privilege Escalation
        (
            'Privilege Escalation - Windows',
            'Windows PrivEsc: Gain higher privileges. Techniques: Unquoted service paths, '
            'Weak service permissions, DLL hijacking, Token impersonation, Kernel exploits. '
            'Tools: PowerUp, WinPEAS, Sherlock, Watson, Mimikatz. Commands: whoami /priv, '
            'net user, systeminfo. Exploits: MS16-032, MS17-010, PrintSpoofer. '
            'Defense: Patch management, Least privilege, UAC, Credential Guard. '
            'Post-exploit: Dump credentials, Persistence, Lateral movement.',
            'cyber_privilege_escalation'
        ),
        (
            'Privilege Escalation - Linux',
            'Linux PrivEsc: Gain root access. Techniques: SUID binaries, Sudo misconfigurations, '
            'Cron jobs, Kernel exploits, Writable /etc/passwd. Tools: LinPEAS, LinEnum, '
            'linux-exploit-suggester. Commands: sudo -l, find / -perm -4000, crontab -l. '
            'SUID: find / -perm -u=s -type f 2>/dev/null. GTFOBins: Exploit legitimate binaries. '
            'Defense: Minimal SUID, Sudo restrictions, Kernel updates, File permissions.',
            'cyber_privilege_escalation'
        ),
        
        # Post-Exploitation
        (
            'Post-Exploitation - Persistence',
            'Persistence: Maintain access after reboot. Windows: Registry Run keys, Scheduled tasks, '
            'Services, WMI events, Startup folder. Linux: Cron jobs, .bashrc, SSH keys, Systemd. '
            'Tools: Metasploit persistence modules, Empire, Cobalt Strike. Techniques: Backdoor '
            'accounts, Web shells, Rootkits. Defense: Integrity monitoring, Baseline comparison, '
            'Regular audits. Detection: Startup items, Scheduled tasks, Unusual services.',
            'cyber_post_exploitation'
        ),
        (
            'Post-Exploitation - Lateral Movement',
            'Lateral Movement: Spread to other systems. Techniques: Pass-the-Hash, Pass-the-Ticket, '
            'RDP, PSExec, WMI, SSH. Tools: Mimikatz, CrackMapExec, Impacket, BloodHound. '
            'Credentials: Dump SAM, LSASS, Kerberos tickets. Pivoting: Use compromised host as '
            'proxy. Defense: Network segmentation, Credential protection, MFA, Monitoring. '
            'Detection: Unusual authentication, Lateral tool usage, Network anomalies.',
            'cyber_post_exploitation'
        ),
        (
            'Post-Exploitation - Data Exfiltration',
            'Data Exfiltration: Steal sensitive data. Methods: FTP, HTTP/HTTPS, DNS tunneling, '
            'Email, Cloud storage, Steganography. Tools: Wget, curl, PowerShell, Netcat. '
            'Covert channels: DNS, ICMP, HTTP headers. Compression: Reduce data size. '
            'Encryption: Hide content. Defense: DLP, Network monitoring, Egress filtering, '
            'Encryption at rest. Detection: Large data transfers, Unusual protocols, '
            'Off-hours activity.',
            'cyber_post_exploitation'
        ),
        
        # Defense and Detection
        (
            'Defense - Security Tools and Solutions',
            'Security Tools: Antivirus/EDR (CrowdStrike, SentinelOne, Defender), Firewall '
            '(pfSense, Fortinet, Palo Alto), IDS/IPS (Snort, Suricata, Zeek), SIEM '
            '(Splunk, ELK, QRadar), WAF (ModSecurity, Cloudflare), Vulnerability Scanners '
            '(Nessus, OpenVAS, Qualys). Network: Wireshark, tcpdump, NetworkMiner. '
            'Forensics: Autopsy, FTK, Volatility. Hardening: CIS Benchmarks, STIG.',
            'cyber_defense'
        ),
        (
            'Defense - Incident Response',
            'Incident Response: Handle security incidents. Phases: 1) Preparation, 2) Detection, '
            '3) Containment, 4) Eradication, 5) Recovery, 6) Lessons Learned. Actions: Isolate '
            'affected systems, Preserve evidence, Analyze logs, Remove threats, Restore services. '
            'Tools: SIEM, EDR, Forensics tools, Threat intelligence. Documentation: Timeline, '
            'Actions taken, Evidence collected. Frameworks: NIST, SANS. Team: CSIRT/SOC.',
            'cyber_defense'
        ),
        
        # Legal and Ethics
        (
            'Legal and Ethical Hacking',
            'Ethical Hacking: Authorized security testing. Requirements: Written authorization, '
            'Scope definition, Rules of engagement, NDA. Certifications: CEH, OSCP, GPEN, GWAPT. '
            'Legal frameworks: CFAA (USA), Computer Misuse Act (UK), Local laws. Bug bounty: '
            'HackerOne, Bugcrowd, Synack. Responsible disclosure: Report vulnerabilities to vendor. '
            'ILLEGAL: Unauthorized access, Data theft, System damage, Extortion. Penalties: '
            'Fines, Imprisonment, Civil liability. Always get permission!',
            'cyber_legal'
        ),
    ]
    
    for topic, content, source in cyber_knowledge:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    # Add cyber attack preferences
    print("\n[3/4] Adding cyber attack preferences...")
    cyber_preferences = [
        ('cyber_attack_mode', 'educational_only'),
        ('authorization_required', 'true'),
        ('ethical_hacking', 'enabled'),
        ('threat_intelligence', 'active'),
        ('vulnerability_alerts', 'enabled'),
        ('security_logging', 'verbose'),
    ]
    
    for key, value in cyber_preferences:
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        print(f"  [+] {key}: {value}")
    
    # Add common attack tools reference
    print("\n[4/4] Adding attack tools reference...")
    tools_reference = [
        (
            'Penetration Testing Tools - Kali Linux',
            'Kali Linux: Penetration testing distribution. Categories: Information Gathering '
            '(Nmap, theHarvester, Maltego), Vulnerability Analysis (Nessus, OpenVAS, Nikto), '
            'Web Applications (Burp Suite, OWASP ZAP, sqlmap), Password Attacks (John, Hashcat, '
            'Hydra), Wireless (Aircrack-ng, Wifite, Reaver), Exploitation (Metasploit, '
            'SearchSploit), Sniffing (Wireshark, tcpdump, Ettercap), Post-Exploitation '
            '(Mimikatz, PowerSploit, Empire), Forensics (Autopsy, Volatility, Binwalk).',
            'cyber_tools'
        ),
        (
            'Attack Tools - Command Reference',
            'Nmap: nmap -sS -sV -O target. Metasploit: msfconsole, use exploit, set RHOST, exploit. '
            'Sqlmap: sqlmap -u URL --dbs --dump. Hydra: hydra -l user -P pass.txt ssh://target. '
            'Hashcat: hashcat -m 0 -a 0 hash.txt wordlist.txt. Aircrack-ng: aircrack-ng -w wordlist '
            'capture.cap. Burp Suite: Proxy, Intruder, Repeater, Scanner. John: john --wordlist=rockyou.txt '
            'hashes.txt. Netcat: nc -lvp 4444 (listener), nc target 4444 (connect).',
            'cyber_tools'
        ),
    ]
    
    for topic, content, source in tools_reference:
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
    cursor.execute("SELECT COUNT(*) FROM user_preferences WHERE preference_key LIKE 'cyber_%' OR preference_key IN ('authorization_required', 'ethical_hacking', 'threat_intelligence', 'vulnerability_alerts', 'security_logging')")
    pref_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("  CYBER ATTACK MEMORY ADDED SUCCESSFULLY!")
    print("=" * 70)
    print(f"  Database: {os.path.abspath(db_path)}")
    print(f"  Security system info: {sys_count} entries")
    print(f"  Cyber attack knowledge: {kb_count} entries")
    print(f"  Security preferences: {pref_count} entries")
    print(f"  Total cyber data: {sys_count + kb_count + pref_count} entries")
    print("\n  Topics covered:")
    print("  ✅ Attack categories and methodologies")
    print("  ✅ Network attacks (DoS, MitM, Sniffing)")
    print("  ✅ Web attacks (SQLi, XSS, RCE, CSRF)")
    print("  ✅ Password attacks (Brute force, Hash cracking)")
    print("  ✅ Social engineering (Phishing, Pretexting)")
    print("  ✅ Malware (Ransomware, Trojans, Rootkits)")
    print("  ✅ Wireless attacks (WiFi cracking, Evil Twin)")
    print("  ✅ Exploitation frameworks (Metasploit)")
    print("  ✅ Reconnaissance and scanning")
    print("  ✅ Privilege escalation (Windows/Linux)")
    print("  ✅ Post-exploitation (Persistence, Lateral movement)")
    print("  ✅ Defense and incident response")
    print("  ✅ Legal and ethical hacking guidelines")
    print("  ✅ Penetration testing tools (Kali Linux)")
    print("\n  View with: python view_database.py")
    print("=" * 70)

def main():
    print("\n🔐 Cyber Attack Memory Integration\n")
    
    db_path = find_database()
    
    if not db_path:
        print("[ERROR] No working database found!")
        print("Run: python fix_database_windows10.py first")
        return
    
    print(f"[INFO] Found database: {db_path}\n")
    
    try:
        add_cyber_attack_data(db_path)
        print("\n✅ SUCCESS! Cyber attack memory has been added to JARVIS database.")
        print("\n⚠️  IMPORTANT LEGAL NOTICE:")
        print("  All information is for EDUCATIONAL and AUTHORIZED testing only!")
        print("  Unauthorized access to computer systems is ILLEGAL.")
        print("  Always obtain written permission before testing.")
        print("\nYou can now ask JARVIS about:")
        print("  - Attack methodologies and techniques")
        print("  - Penetration testing procedures")
        print("  - Security tools and frameworks")
        print("  - Defense and incident response")
        print("  - Ethical hacking guidelines")
    except Exception as e:
        print(f"\n[ERROR] Failed to add cyber attack data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
