# WORDLISTS & RESOURCES REFERENCE
# April 2026 Red Team Stack
# Every wordlist, feed, and reference you need — with install commands

---

## WORDLIST INSTALLATION

```bash
# Install SecLists (most important):
sudo apt install seclists

# Install rockyou:
gunzip /usr/share/wordlists/rockyou.txt.gz
```

---

## PASSWORD WORDLISTS

```
/usr/share/wordlists/rockyou.txt  133MB    General password cracking
seclists/Passwords/xato-net-10-million-passwords-10000.txt  10k  Web login brute
seclists/Passwords/Common-Credentials/top-passwords-shortlist.txt  10  Quick spray
```

**Generate target-specific wordlist:**
```bash
cewl https://[TARGET] -d 3 -m 6 -w /tmp/cewl.txt --with-numbers
```

---

## DIRECTORY / URL WORDLISTS

```
seclists/Discovery/Web-Content/raft-large-directories.txt  62k  Comprehensive dir brute
seclists/Discovery/Web-Content/raft-medium-directories.txt  29k  Balanced speed/coverage
seclists/Discovery/Web-Content/common.txt             4.5k  Fast common paths
```

---

## NUCLEI TEMPLATES

```bash
nuclei -update-templates
# Templates at: ~/.local/nuclei-templates/ (4000+)
```

---

## OSINT RESOURCES

```
Shodan              shodan.io
crt.sh              crt.sh/?q=%25.[domain]
HaveIBeenPwned      haveibeenpwned.com/API
GitHub              github.com/search (code/secret search)
```

---

*April 2026 | Keep wordlists updated — SecLists is updated weekly*
