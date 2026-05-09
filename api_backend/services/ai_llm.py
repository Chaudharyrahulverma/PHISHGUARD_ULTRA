# ========================================
# PHISHGUARD ULTRA - AI LLM ENGINE (FIXED)
# Essential Tools + Attacks + Roadmap + Domains
# No API Key Required
# ========================================

import re

# ========================================
# SECTION 1: ESSENTIAL CYBERSECURITY TOOLS
# ========================================

TOOLS = {
    "nmap": "Network scanner | nmap -sV target.com",
    "theharvester": "Email/domain harvesting | theHarvester -d target.com -b google",
    "whois": "Domain registration lookup | whois example.com",
    "dnsenum": "DNS enumeration | dnsenum target.com",
    "sublist3r": "Subdomain discovery | sublist3r -d target.com",
    "amass": "DNS mapping | amass enum -d target.com",
    "masscan": "Fast port scanner | masscan -p1-1000 target.com --rate=1000",
    "nessus": "Professional vuln scanner",
    "openvas": "Open-source vuln scanner | openvas-setup",
    "nikto": "Web server scanner | nikto -h target.com",
    "nuclei": "Template-based scanner | nuclei -u target.com",
    "burp suite": "Web proxy - MOST IMPORTANT | Set proxy to 127.0.0.1:8080",
    "sqlmap": "SQL injection tool | sqlmap -u target.com?id=1 --dbs",
    "xsstrike": "XSS scanner | python xsstrike.py -u target.com",
    "ffuf": "Web fuzzer | ffuf -u https://target.com/FUZZ -w wordlist.txt",
    "gobuster": "Directory brute-force | gobuster dir -u target.com -w wordlist.txt",
    "wpscan": "WordPress scanner | wpscan --url target.com",
    "hydra": "Login cracker | hydra -l admin -P pass.txt target.com ssh",
    "john the ripper": "Password cracker | john --wordlist=rockyou.txt hash.txt",
    "hashcat": "GPU password cracker | hashcat -m 0 hash.txt rockyou.txt",
    "mimikatz": "Windows credential dumper",
    "cewl": "Wordlist generator | cewl target.com -w wordlist.txt",
    "aircrack-ng": "WiFi auditing | aircrack-ng capture.cap -w wordlist.txt",
    "wifite": "Auto WiFi auditor | wifite",
    "reaver": "WPS attack | reaver -i wlan0mon -b BSSID",
    "metasploit": "Pentest framework | msfconsole",
    "searchsploit": "Exploit database | searchsploit apache",
    "beef": "Browser exploitation | beef-xss",
    "wireshark": "Packet analyzer | wireshark",
    "ettercap": "MITM tool | ettercap -T -M arp:remote",
    "responder": "LLMNR poisoner | responder -I eth0 -wrf",
    "tcpdump": "CLI packet capture | tcpdump -i eth0 -w capture.pcap",
    "bloodhound": "AD mapping | bloodhound-python -d domain.com",
    "crackmapexec": "AD swiss army knife | crackmapexec smb target -u user -p pass",
    "impacket": "Python network protocols | psexec.py domain/user@target",
    "linpeas": "Linux privesc automation | ./linpeas.sh",
    "winpeas": "Windows privesc | winpeas.exe",
    "gophish": "Phishing framework | ./gophish",
    "evilginx2": "2FA bypass | evilginx2 -p phishlets",
    "setoolkit": "Social engineer toolkit | setoolkit",
    "zphisher": "Automated phishing | bash zphisher.sh",
    "ghidra": "Reverse engineering | ghidra",
    "radare2": "RE framework | r2 binary",
    "volatility": "Memory forensics | vol.py -f memory.dump imageinfo",
    "apktool": "APK decompiler | apktool d app.apk",
    "spiderfoot": "OSINT automation | spiderfoot -l 127.0.0.1:5001",
    "sherlock": "Username search | python sherlock.py username",
    "trufflehog": "Secret finder | trufflehog git https://github.com/user/repo",
}

# ========================================
# SECTION 2: ATTACK KNOWLEDGE BASE
# ========================================

ATTACKS = {
    "phishing": {
        "desc": "Attacker fake website/email se data churata hai",
        "types": ["Email", "Spear", "Clone", "Smishing", "Vishing", "Whaling"],
        "prevention": "Check URLs, 2FA, Security training, Email filters",
        "tools": "Gophish, Evilginx2, SEToolkit, Zphisher"
    },
    "sql injection": {
        "desc": "Database queries manipulate karta hai",
        "types": ["Error-based", "Union-based", "Blind", "Time-based"],
        "prevention": "Parameterized queries, Input validation, WAF",
        "tools": "SQLmap, NoSQLMap"
    },
    "xss": {
        "desc": "Malicious scripts inject karta hai",
        "types": ["Stored", "Reflected", "DOM-based"],
        "prevention": "Input sanitization, Output encoding, CSP",
        "tools": "XSStrike, Dalfox, BeEF"
    },
    "csrf": {
        "desc": "User identity ka misuse karta hai",
        "prevention": "CSRF tokens, SameSite cookies, Referer validation",
        "tools": "Burp Suite, OWASP ZAP"
    },
    "ddos": {
        "desc": "Server par overwhelming traffic bhejta hai",
        "types": ["Volume-based", "Protocol", "Application layer"],
        "prevention": "Rate limiting, CDN, WAF, Load balancers",
        "tools": "LOIC, HOIC, GoldenEye"
    },
    "brute force": {
        "desc": "Passwords guess karta hai repeatedly",
        "prevention": "Account lockout, CAPTCHA, 2FA, Strong passwords",
        "tools": "Hydra, Medusa, Ncrack, John the Ripper"
    },
    "mitm": {
        "desc": "Communication intercept karta hai",
        "prevention": "HTTPS, VPN, Certificate pinning",
        "tools": "Ettercap, Bettercap, Responder"
    }
}

# ========================================
# SECTION 3: CYBERSECURITY DOMAINS & ROADMAP
# ========================================

DOMAINS = {
    "web security": "Web applications ko attacks se bachana. Skills: HTTP, OWASP Top 10, Burp Suite, SQLi, XSS",
    "network security": "Networks ko unauthorized access se bachana. Skills: TCP/IP, Firewalls, IDS/IPS, Wireshark, Nmap",
    "cloud security": "AWS/Azure/GCP infrastructure security. Skills: IAM, S3, CloudTrail, KMS, Container security",
    "mobile security": "Android/iOS app security. Skills: APK decompilation, Frida, MobSF, SSL pinning",
    "forensics": "Digital evidence analysis. Skills: Memory forensics, Disk forensics, Log analysis, Volatility",
    "malware analysis": "Malware behavior analysis. Skills: Reverse engineering, Sandbox, Assembly, Ghidra",
    "incident response": "Security breach handling. Skills: Detection, Containment, Eradication, Recovery",
    "red teaming": "Adversary simulation. Skills: C2 frameworks, Evasion, TTPs, OPSEC",
    "blue teaming": "Defense monitoring. Skills: SIEM, EDR, Threat hunting, Log analysis",
    "ctf": "Capture The Flag competitions. Skills: Cryptography, Forensics, Reverse, Pwn, Web",
}

ROADMAP = """
🔰 CYBERSECURITY ROADMAP (Complete Guide)

Phase 1: Foundations (1-2 months)
- Networking: TCP/IP, DNS, HTTP/HTTPS, OSI model
- Operating Systems: Windows, Linux (Kali), macOS
- Basic Programming: Python, Bash, JavaScript
- Security Basics: CIA triad, Authentication, Encryption

Phase 2: Core Security (2-3 months)
- Web Security: OWASP Top 10, Burp Suite, SQLi, XSS
- Network Security: Firewalls, IDS/IPS, VPN, Wireshark
- System Security: Privilege escalation, Hardening
- Tools: Nmap, Metasploit, John, Hydra

Phase 3: Choose Your Path (3-6 months)

Red Team (Offensive)
- Learn: AD exploitation, C2 frameworks, Bypassing EDR
- Labs: HackTheBox, TryHackMe, OSCP
- Tools: Cobalt Strike, BloodHound, Mimikatz

Blue Team (Defensive)
- Learn: SIEM (Splunk), EDR, Threat hunting
- Labs: Blue Team Labs Online, LetsDefend
- Tools: Wireshark, Sysmon, Velociraptor

Phase 4: Certifications
- Entry: CompTIA Security+, CEH
- Advanced: OSCP, CISSP, CISM

Quick Start: Start with TryHackMe's Pre Security path + install Kali Linux!
"""

# ========================================
# SECTION 4: LAB GUIDANCE
# ========================================

LABS = {
    "tryhackme": "Beginner-friendly platform | Start with Pre Security, Web Fundamentals",
    "hackthebox": "Advanced platform | Need VPN | Start: Starting Point Tier 0",
    "portswigger": "Best for web security | ALL labs free | OWASP Top 10 practice",
    "dvwa": "Damn Vulnerable Web App | PHP practice | 4 security levels",
    "vulnhub": "Free vulnerable VMs | Download and run locally",
}

# ========================================
# SECTION 5: PROJECT KNOWLEDGE
# ========================================

PROJECT_INFO = {
    "name": "PhishGuard Ultra",
    "about": "AI-powered cybersecurity suite for phishing detection",
    "features": [
        "URL Scanner - Phishing URL detection",
        "Email Scanner - Suspicious email analysis",
        "Content Scanner - Text phishing detection",
        "Password Checker - Strength analysis",
        "Image OCR Scanner - Extract text from images",
        "AI Chat Assistant - Cybersecurity Q&A"
    ],
    "tech_stack": "Python, Flask, SQLite, Tailwind CSS, Tesseract OCR",
}

# ========================================
# SECTION 6: HELPER FUNCTIONS
# ========================================

def find_tool(query):
    query_lower = query.lower()
    if query_lower in TOOLS:
        return query_lower, TOOLS[query_lower]
    for tool, desc in TOOLS.items():
        if tool in query_lower or query_lower in tool:
            return tool, desc
    return None, None

def find_attack(query):
    query_lower = query.lower()
    for attack in ATTACKS:
        if attack in query_lower:
            return attack, ATTACKS[attack]
    return None, None

def find_lab(query):
    query_lower = query.lower()
    for lab in LABS:
        if lab in query_lower:
            return lab, LABS[lab]
    return None, None

def find_domain(query):
    query_lower = query.lower()
    for domain, info in DOMAINS.items():
        if domain in query_lower:
            return domain, info
    return None, None

# ========================================
# SECTION 7: RESPONSE BUILDERS
# ========================================

def tool_response(tool, desc):
    parts = desc.split('|')
    description = parts[0].strip()
    usage = parts[1].strip() if len(parts) > 1 else "Check documentation"
    return f"🔧 {tool.upper()}\n\nDescription: {description}\n\nUsage: {usage}\n\nNote: Use only on authorized systems."

def attack_response(attack, info):
    result = f"⚠️ {attack.upper()} ATTACK\n\nDescription: {info['desc']}\n"
    if 'types' in info:
        result += f"\nTypes: {', '.join(info['types'])}"
    if 'prevention' in info:
        result += f"\n\nPrevention: {info['prevention']}"
    if 'tools' in info:
        result += f"\n\nTools: {info['tools']}"
    return result

def lab_response(lab, info):
    return f"🧪 {lab.upper()} LAB\n\nInfo: {info}\n\nStart with beginner rooms and practice daily!"

def domain_response(domain, info):
    return f"📚 {domain.upper()} DOMAIN\n\n{info}"

# ========================================
# SECTION 8: MAIN AI FUNCTION
# ========================================

def llm_reply(context, message, lang="english"):
    msg = message.lower().strip()
    
    # Greetings
    greetings = ["hi", "hello", "hey", "namaste"]
    if any(g in msg for g in greetings) and len(msg) < 20:
        return """Welcome to PhishGuard Ultra AI Assistant!

I can help you with:
- Security Tools (nmap, sqlmap, metasploit, burp)
- Attack Explanations (Phishing, SQLi, XSS)
- Lab Guidance (TryHackMe, HackTheBox)
- Cybersecurity Roadmap
- Project Features

Type 'roadmap' for complete learning path!"""
    
    # Roadmap
    if "roadmap" in msg or "how to become" in msg or "career" in msg:
        return ROADMAP
    
    # Project info
    if "project" in msg or "phishguard" in msg or "about" in msg:
        features = "\n".join([f"- {f}" for f in PROJECT_INFO['features']])
        return f"PhishGuard Ultra\n\nAbout: {PROJECT_INFO['about']}\n\nFeatures:\n{features}\n\nTech: {PROJECT_INFO['tech_stack']}"
    
    # Tool help
    tool, desc = find_tool(msg)
    if tool:
        return tool_response(tool, desc)
    
    # Attack help
    attack, info = find_attack(msg)
    if attack:
        return attack_response(attack, info)
    
    # Lab help
    lab, info = find_lab(msg)
    if lab:
        return lab_response(lab, info)
    
    # Domain help
    domain, info = find_domain(msg)
    if domain:
        return domain_response(domain, info)
    
    # Password help
    if "password" in msg:
        return """Password Security Tips:
- Use 12+ characters
- Mix uppercase, lowercase, numbers, symbols
- Avoid common words
- Use our Password Checker tab for analysis!"""
    
    # Phishing help
    if "phishing" in msg:
        return """Phishing Detection Tips:
- Check sender email carefully
- Hover over links before clicking
- Look for urgency or threats
- Use our URL Scanner to check suspicious links!"""
    
    # Default response
    return f"""PhishGuard AI Assistant

I can help with cybersecurity topics!

Try asking:
- 'What is nmap?'
- 'Explain SQL injection'
- 'TryHackMe guidance'
- 'cybersecurity roadmap'
- 'About PhishGuard'

You asked: {message[:100]}"""