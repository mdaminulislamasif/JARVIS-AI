# Cyber Attacks Menu & Memory - Complete Reference

## ⚠️ LEGAL DISCLAIMER

**THIS INFORMATION IS FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY**

Unauthorized access to computer systems is **ILLEGAL** in most jurisdictions worldwide. This knowledge base is intended for:
- Authorized penetration testing
- Security research on your own systems
- Educational purposes in controlled environments
- Defensive security and threat intelligence
- Bug bounty programs with proper authorization

**Always obtain written authorization before conducting any security testing.**

---

## 📊 Database Statistics

- **System Info Entries**: 6
- **Knowledge Base Entries**: 37
- **Preferences**: 3
- **Total Cyber Attack Data**: 46 entries

---

## 📁 Attack Categories

### 1. Network Attacks (3 entries)

#### DDoS (Distributed Denial of Service)
- **Types**: Volumetric, Protocol, Application Layer
- **Tools**: LOIC, HOIC, Hping3
- **Defense**: Rate limiting, CDN, DDoS mitigation services
- **Famous Botnets**: Mirai, Emotet

#### Man-in-the-Middle (MITM)
- **Types**: ARP spoofing, DNS spoofing, SSL stripping, Session hijacking
- **Tools**: Ettercap, Bettercap, mitmproxy, Wireshark
- **Defense**: HTTPS, HSTS, Certificate pinning, VPN

#### Port Scanning & Enumeration
- **Tools**: Nmap, Masscan, Unicornscan
- **Techniques**: TCP SYN, UDP, FIN/NULL/Xmas scans
- **Defense**: Firewall rules, IDS/IPS (Snort, Suricata)

---

### 2. Web Application Attacks (6 entries)

#### SQL Injection (SQLi)
- **Types**: In-band, Blind, Out-of-band
- **Tools**: sqlmap, Havij, jSQL Injection
- **Payloads**: `OR 1=1`, `UNION SELECT`, Time delays
- **Defense**: Prepared statements, Parameterized queries, WAF

#### Cross-Site Scripting (XSS)
- **Types**: Stored, Reflected, DOM-based
- **Payloads**: `<script>alert(1)</script>`, Cookie theft
- **Tools**: XSSer, BeEF, Burp Suite
- **Defense**: Input sanitization, CSP headers, HTTPOnly cookies

#### Cross-Site Request Forgery (CSRF)
- **Attack**: Force authenticated users to execute unwanted actions
- **Defense**: CSRF tokens, SameSite cookies, Referer validation

#### Remote Code Execution (RCE)
- **Vectors**: File upload, Deserialization, Command injection
- **Tools**: Metasploit, Commix, Weevely
- **Defense**: Input validation, Sandboxing, WAF

#### Local/Remote File Inclusion (LFI/RFI)
- **Payloads**: `../../../../etc/passwd`, Log poisoning
- **Defense**: Whitelist files, Disable allow_url_include

#### XML External Entity (XXE)
- **Impact**: File disclosure, SSRF, DoS, RCE
- **Defense**: Disable external entities, Use JSON

---

### 3. Social Engineering (2 entries)

#### Phishing
- **Types**: Spear phishing, Whaling, Vishing, Smishing
- **Tools**: SET, Gophish, King Phisher
- **Defense**: Email filtering, User training, 2FA, DMARC/SPF/DKIM

#### Pretexting & Baiting
- **Techniques**: Impersonation, Authority exploitation
- **Physical**: Tailgating, Dumpster diving
- **Defense**: Verification procedures, Security awareness

---

### 4. Malware (4 entries)

#### Ransomware
- **Types**: Crypto, Locker, Scareware
- **Famous**: WannaCry, Petya, Ryuk, REvil, LockBit
- **Defense**: Backups (3-2-1 rule), Patch management, EDR

#### Trojans & RATs
- **Famous**: Zeus, Emotet, DarkComet, njRAT
- **Capabilities**: Keylogging, Screen capture, File theft
- **Defense**: Antivirus, Application whitelisting

#### Rootkits & Bootkits
- **Types**: User-mode, Kernel-mode, Firmware
- **Detection**: GMER, RootkitRevealer, Memory forensics
- **Defense**: Secure Boot, UEFI protection

#### Worms & Viruses
- **Famous**: Morris, ILOVEYOU, Conficker, Stuxnet
- **Propagation**: Email, Network shares, USB drives
- **Defense**: Patching, Network segmentation, Antivirus

---

### 5. Password Attacks (3 entries)

#### Brute Force & Dictionary
- **Tools**: Hydra, Medusa, John the Ripper, Hashcat
- **Targets**: SSH, RDP, FTP, Web logins
- **Defense**: Account lockout, Rate limiting, 2FA

#### Credential Stuffing & Spraying
- **Tools**: Sentry MBA, STORM, Burp Suite
- **Sources**: Data breaches (Have I Been Pwned)
- **Defense**: Breach monitoring, 2FA, Password managers

#### Hash Cracking
- **Types**: MD5, SHA1, SHA256, bcrypt, NTLM
- **Methods**: Rainbow tables, GPU cracking
- **Defense**: Strong hashing (bcrypt, Argon2), Salting

---

### 6. Wireless Attacks (3 entries)

#### WiFi Cracking
- **Targets**: WEP, WPA/WPA2-PSK, WPA3
- **Tools**: Aircrack-ng, Reaver, Wifite, Hashcat
- **Techniques**: Deauth attack, Handshake capture, PMKID
- **Defense**: WPA3, Strong passwords, Disable WPS

#### Evil Twin & Rogue AP
- **Tools**: Airbase-ng, hostapd, WiFi Pineapple
- **Defense**: 802.1X, Certificate validation, Wireless IDS

#### Bluetooth & RFID
- **Bluetooth**: Bluejacking, Bluesnarfing, Bluebugging
- **RFID**: Cloning, Eavesdropping, Relay attacks
- **Tools**: Proxmark3, Chameleon Mini, HackRF

---

### 7. Advanced Persistent Threats (APT)

**Phases**:
1. Reconnaissance
2. Initial compromise
3. Establish foothold
4. Escalate privileges
5. Internal reconnaissance
6. Lateral movement
7. Maintain presence
8. Complete mission

**Famous APT Groups**:
- APT28 (Fancy Bear)
- APT29 (Cozy Bear)
- Lazarus Group
- Equation Group

**Defense**: Threat intelligence, EDR, Network segmentation

---

### 8. Exploitation Frameworks (2 entries)

#### Metasploit
- **Components**: Exploits, Payloads, Auxiliary, Post-exploitation
- **Payloads**: Meterpreter, Shell, VNC, Reverse/Bind shells
- **Modules**: 2000+ exploits, 500+ payloads

#### Cobalt Strike & Empire
- **Cobalt Strike**: Commercial adversary simulation
- **Empire**: PowerShell post-exploitation
- **Techniques**: Living off the land, Fileless attacks

---

### 9. Reconnaissance (2 entries)

#### OSINT & Information Gathering
- **Tools**: theHarvester, Maltego, Shodan, Censys, Recon-ng
- **Techniques**: Google dorking, WHOIS, DNS enumeration
- **Targets**: Email addresses, Subdomains, Employee info

#### Vulnerability Scanning
- **Tools**: Nessus, OpenVAS, Qualys, Nexpose, Nikto
- **Output**: CVSS scores, Remediation advice
- **Defense**: Regular scanning, Patch management

---

### 10. Privilege Escalation (2 entries)

#### Windows PrivEsc
- **Techniques**: Unquoted service paths, Token impersonation, DLL hijacking
- **Tools**: PowerUp, WinPEAS, Sherlock, Watson
- **Defense**: Least privilege, Patch management, Credential Guard

#### Linux PrivEsc
- **Techniques**: SUID binaries, Sudo misconfig, Kernel exploits
- **Tools**: LinPEAS, LinEnum, Linux Exploit Suggester
- **Defense**: Minimal SUID, Kernel updates, SELinux/AppArmor

---

### 11. Persistence Mechanisms

**Windows**:
- Registry Run keys
- Scheduled tasks
- Services
- WMI event subscriptions
- DLL hijacking

**Linux**:
- Cron jobs
- .bashrc
- systemd services
- SSH keys
- LD_PRELOAD

**Defense**: Autoruns monitoring, File integrity monitoring, EDR

---

### 12. Defense & Mitigation (2 entries)

#### Security Best Practices
- Defense in Depth
- Patch management
- Least privilege
- Network segmentation
- Strong authentication (2FA/MFA)
- Encryption (at rest/in transit)
- Security awareness training
- Incident response plan
- Regular backups
- Log monitoring

**Frameworks**: NIST, CIS Controls, ISO 27001

#### Detection & Response
- **Detection**: IDS/IPS, SIEM, EDR, Network monitoring
- **Response**: Incident response plan, Forensics, Containment
- **Tools**: Wireshark, Volatility, Autopsy, FTK
- **Threat Hunting**: Proactive search for threats

---

### 13. Penetration Testing

**Phases**:
1. Planning & Reconnaissance
2. Scanning & Enumeration
3. Gaining Access
4. Maintaining Access
5. Covering Tracks
6. Reporting

**Types**:
- Black box (no knowledge)
- White box (full knowledge)
- Gray box (partial knowledge)

**Standards**: PTES, OWASP, OSSTMM

**Certifications**: OSCP, CEH, GPEN

---

### 14. MITRE ATT&CK Framework

**Tactics** (14 phases):
1. Reconnaissance
2. Resource Development
3. Initial Access
4. Execution
5. Persistence
6. Privilege Escalation
7. Defense Evasion
8. Credential Access
9. Discovery
10. Lateral Movement
11. Collection
12. Command and Control
13. Exfiltration
14. Impact

**Use Cases**:
- Threat intelligence
- Detection engineering
- Red/Blue team exercises

**Website**: attack.mitre.org

---

## 🛠️ Security Tools

### Network Tools
- **Nmap**: Port scanning
- **Wireshark**: Packet analysis
- **Metasploit**: Exploitation
- **Burp Suite**: Web testing
- **Aircrack-ng**: WiFi cracking
- **Ettercap**: MITM attacks
- **Nessus**: Vulnerability scanning
- **Hydra**: Password cracking
- **sqlmap**: SQL injection
- **John the Ripper**: Password cracking
- **Hashcat**: Hash cracking
- **Nikto**: Web scanning
- **OWASP ZAP**: Web security

### Security Operating Systems
- **Kali Linux**: Most popular (600+ tools)
- **Parrot OS**: Privacy-focused
- **BlackArch**: 2800+ tools
- **BackBox**: Ubuntu-based
- **Pentoo**: Gentoo-based

---

## ⚖️ Legal & Ethical Guidelines

### Legal Framework

**Laws**:
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Cybercrime laws worldwide

**Penalties**:
- Fines
- Imprisonment
- Civil liability

### Ethical Hacking Principles

1. **Authorization**: Always get written permission
2. **Scope**: Stay within defined boundaries
3. **Confidentiality**: Protect discovered information
4. **Disclosure**: Report vulnerabilities responsibly
5. **No Harm**: Avoid damage to systems
6. **Professionalism**: Follow industry standards

### Responsible Disclosure

- 90-day disclosure window
- Vendor notification
- Public disclosure after fix
- Coordinated vulnerability disclosure

---

## 🎯 JARVIS Integration

### Query Examples

Ask JARVIS:
```
"What is SQL injection and how does it work?"
"How do I defend against DDoS attacks?"
"What tools are used for penetration testing?"
"Explain the MITRE ATT&CK framework"
"What is the difference between a worm and a virus?"
"How does ransomware work?"
"What are the phases of an APT attack?"
"How do I perform ethical hacking legally?"
"What is the best defense against phishing?"
"Explain privilege escalation techniques"
```

### Database Location

All cyber attack information is stored in:
- `system_info` table (security category)
- `knowledge_base` table (cyber_* sources)
- `user_preferences` table (cyber_* keys)

### View Cyber Attack Data

```bash
python view_cyber_attacks.py
```

### Add More Data

```bash
python add_cyber_attacks.py
```

---

## 📚 Additional Resources

### Learning Platforms
- **TryHackMe**: Hands-on cybersecurity training
- **HackTheBox**: Penetration testing labs
- **PortSwigger Web Security Academy**: Free web security training
- **OWASP**: Web application security resources
- **Cybrary**: Free cybersecurity courses

### Certifications
- **OSCP**: Offensive Security Certified Professional
- **CEH**: Certified Ethical Hacker
- **GPEN**: GIAC Penetration Tester
- **CISSP**: Certified Information Systems Security Professional
- **Security+**: CompTIA Security+

### Communities
- Reddit: r/netsec, r/AskNetsec, r/cybersecurity
- Discord: Many cybersecurity servers
- Twitter: #infosec, #cybersecurity
- Conferences: DEF CON, Black Hat, BSides

---

## 🔄 Updates

**Last Updated**: May 4, 2026  
**Database Version**: 2.0  
**Cyber Attack Entries**: 46

---

## ⚠️ FINAL WARNING

**This information is provided for EDUCATIONAL and DEFENSIVE purposes ONLY.**

- Unauthorized access to computer systems is **ILLEGAL**
- Always obtain **written authorization** before testing
- Follow **ethical hacking guidelines**
- Respect **privacy and property rights**
- Use knowledge for **defense, not offense**

**Unauthorized hacking can result in criminal prosecution, fines, and imprisonment.**

---

**🔒 Stay Safe. Stay Legal. Stay Ethical.**
