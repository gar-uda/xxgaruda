# 🦅 XXGARUDA v2.0 — The Ultimate Tool


---

## 🔥 Features

| Feature | Command |
|---------|---------|
| Port scanning | `xxgscan --TARGET 192.168.1.1` |
| OS detection | `xxgos --TARGET 192.168.1.1` |
| SSH brute-force | `xxgbrute --TARGET 192.168.1.1 --USER root --WORDLIST passwords.txt` |
| SQL injection | `xxgsqli --URL "https://example.com?id=1" --PARAM id` |
| XSS scanner | `xxgxss --URL "https://example.com?q=test" --PARAM q` |
| LFI scanner | `xxglfi --URL "https://example.com?file=index" --PARAM file` |
| RCE scanner | `xxgrce --URL "https://example.com?cmd=id" --PARAM cmd` |
| Payload generator | `xxgexp` |
| OSINT (email) | `xxgosint --TARGET test@example.com` |
| OSINT (domain) | `xxgosint --TARGET example.com` |
| Encode text | `xxgencode --INPUT "hello"` |
| Hash generator | `xxghash --INPUT "password"` |
| Code generator | `xxggen --LANGUAGE python` |
| Directory fuzzing | `xxgfuzz --URL https://example.com --WORDLIST common.txt` |
| Subdomain enumeration | `xxgrecon --TARGET example.com --WORDLIST subdomains.txt` |
| Hash cracker | `xxgcrack --HASH-VALUE 5f4dcc3b5aa765d61d8327deb882cf99 --WORDLIST passwords.txt` |

---

## 🚀 Installation

### From PyPI

```bash
pip install xxgaruda
```

### From GitHub

```bash
git clone https://github.com/gar-uda/xxgaruda.git
cd xxgaruda
pip install -r requirements.txt
```

### One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/gar-uda/xxgaruda/main/xxgaruda.py | python3
```

---

## 📖 Usage

```bash
xxgaruda --help
xxgaruda --SCAN --TARGET 127.0.0.1
xxgaruda --EXPLOIT
xxgaruda --OSINT --TARGET test@example.com
```

---

## 🎯 Bash Aliases (Add to `~/.bashrc`)

```bash
# XXGARUDA shortcuts
alias xxghelp='xxgaruda --help'
alias xxgscan='xxgaruda --SCAN'
alias xxgos='xxgaruda --OS'
alias xxgbrute='xxgaruda --BRUTE'
alias xxgsqli='xxgaruda --SQLI'
alias xxgxss='xxgaruda --XSS'
alias xxglfi='xxgaruda --LFI'
alias xxgrce='xxgaruda --RCE'
alias xxgexp='xxgaruda --EXPLOIT'
alias xxgosint='xxgaruda --OSINT'
alias xxgencode='xxgaruda --ENCODE'
alias xxghash='xxgaruda --HASH'
alias xxggen='xxgaruda --GENERATE'
alias xxgfuzz='xxgaruda --FUZZ'
alias xxgrecon='xxgaruda --RECON'
alias xxgcrack='xxgaruda --CRACK'
```

Reload:

```bash
source ~/.bashrc
```

---

## 👤 Author

Built by [gar-uda](https://github.com/gar-uda)
