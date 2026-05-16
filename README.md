<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=mit&logoColor=white">
  <img src="https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge">
  <img src="https://img.shields.io/badge/DVWA-Tested-red?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/github/stars/kepper88-prog/dvwa-xss-scanner?style=for-the-badge&logo=github">
</p>

# 🐉 XSS Auto Exploit

## Автоматический сканер и эксплуатация Reflected XSS уязвимостей

**XSS Auto Exploit** — это инструмент для автоматического обнаружения и эксплуатации **Reflected XSS** уязвимостей. Проект разработан в рамках перехода из инженерной сферы (6+ лет испытаний двигателей) в **Application Security**.

> *"Что я делал с двигателями — поиск аномалий, анализ причин отказов, строгие регламенты — теперь я применяю к веб-безопасности. Только вместо двигателей — HTTP запросы."*

---

## 🎯 Цель проекта

Показать практическое понимание:

| Область | Что демонстрирует проект |
|---------|--------------------------|
| **OWASP Top 10** | XSS (A7:2017 / A3:2021) — отражённый тип |
| **HTTP протокол** | GET/POST запросы, параметры, статусы |
| **Сессии и cookies** | Работа с PHPSESSID, аутентификация |
| **Автоматизация** | Полностью автоматический цикл: логин → атака → детекция |
| **Python** | Модульная архитектура, ООП, requests |

---

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| 🔍 **Автоматический поиск XSS** | Обнаруживает Reflected XSS без ручного вмешательства |
| 🎭 **4+ XSS payload'ов** | `<script>`, `<img>`, `<body>`, `<svg>` и другие |
| 🔐 **Работа с сессиями** | Поддерживает аутентифицированные цели (cookies, PHPSESSID) |
| 🧩 **Модульная архитектура** | Легко добавлять новые payload'ы и типы атак |
| 🐳 **Docker поддержка** | Изолированная тестовая среда DVWA |
| 📊 **Цветной вывод** | Интуитивно понятный лог с цветовой индикацией |

---

## 🚀 Быстрый старт

### Предварительные требования

- Установленный **Python 3.12+**
- Установленный **Docker** (для тестовой среды)
- Установленный **Git**

### Установка и запуск

#### 1. Клонируй репозиторий

```bash
git clone https://github.com/kepper88-prog/dvwa-xss-scanner.git
cd dvwa-xss-scanner

2. Установи зависимости
bash

pip install requests
# или
pip3 install requests

3. Запусти тестовую среду (DVWA)
bash

# Установи Docker если нет
sudo apt update && sudo apt install docker.io -y

# Запусти DVWA
docker run --rm -d -p 8081:80 vulnerables/web-dvwa

4. Настрой DVWA
Шаг	Действие
1	Открой в браузере http://localhost:8081
2	Войди: admin / password
3	Нажми "DVWA Security" → выбери "low" → Submit
4	Скопируй PHPSESSID (F12 → Application → Cookies)
5. Вставь свой PHPSESSID в скрипт

Открой dvwa_xss_final.py и замени строку:
python

PHPSESSID = "68jrank2o2bc9fiksn53l1c506"  # Вставь свой

6. Запусти сканер
bash

python3 dvwa_xss_final.py

📸 Пример работы
bash

┌──(venv)─(serg㉿HackBug)-[~/Projects/portswigger-auto-solver]
└─$ python3 dvwa_xss_final.py

text

╔═══════════════════════════════════════════╗
║   🐉 DVWA XSS Auto Exploit               ║
╚═══════════════════════════════════════════╝
[*] Checking session...
[+] Session is valid!
[*] Testing XSS vulnerabilities...
    Trying: <script>alert(1)</script>...

[🔥] XSS FOUND! Payload: <script>alert(1)</script>
[✓] Vulnerability successfully exploited

[🎉] SUCCESS! Your script works!

📁 Архитектура проекта
text

dvwa-xss-scanner/
│
├── 🐍 dvwa_xss_final.py   # 🔥 Основной скрипт (простая версия)
├── 🧠 solver.py           # Модульный солвер (расширяемый)
│
├── 📚 labs/               # Модули для разных лабораторий
│   ├── __init__.py
│   ├── xss_reflected.py   # Решение PortSwigger XSS
│   └── dvwa_xss.py        # Решение DVWA XSS
│
├── 🛠️ utils/              # Вспомогательные утилиты
│   ├── __init__.py
│   ├── requester.py       # HTTP обёртка с сессиями
│   └── logger.py          # Цветное логирование
│
├── ⚙️ config.py           # Конфигурация (прокси, таймауты)
└── 📖 README.md           # Документация

🔧 Как это работает

Алгоритм:

    Аутентификация — использует валидную сессию (PHPSESSID)

    Перебор payload'ов — отправляет каждый вектор в параметр name

    Детекция — проверяет, отразился ли payload в ответе сервера

    Отчёт — выводит результат в консоль с цветовым кодированием

📈 Roadmap (планы по развитию)

    Базовый XSS сканер для DVWA

    Поддержка сессий и cookies

    Модульная архитектура

    Профессиональный README

    DOM-based XSS детекция

    Stored XSS проверка

    Генерация JSON/HTML отчётов

    Интеграция с Telegram ботом

    Поддержка сканирования списка URL

    Обфускация payload'ов (WAF обход)

    CI/CD через GitHub Actions

📝 

Этот проект демонстрирует следующие навыки:
Навык	Как проявлен
🐍 Python	Чистый код, модульная архитектура, ООП
🌐 HTTP протокол	Работа с requests, сессиями, cookies, параметрами
🔒 OWASP Top 10	Понимание XSS (отражённый тип)
🤖 Автоматизация	Полностью автоматический процесс от логина до эксплуатации
📦 Git	Чистая история коммитов, .gitignore, ветки
🐳 Docker	Запуск изолированной тестовой среды
📖 Документация	Профессиональный README с примерами
🤝 Как внести вклад

    Форкни репозиторий (https://github.com/kepper88-prog/dvwa-xss-scanner/fork)

    Создай ветку для фичи (git checkout -b feature/amazing-feature)

    Закоммить изменения (git commit -m 'Add amazing feature')

    Запушь ветку (git push origin feature/amazing-feature)

    Открой Pull Request

📄 Лицензия

Проект распространяется под лицензией MIT. Подробности в файле LICENSE.
text

MIT License

Copyright (c) 2026 Serg (kepper88-prog)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

🔗 Ссылки
Ресурс	Ссылка
🐙 GitHub	github.com/kepper88-prog
📦 Проект	dvwa-xss-scanner
🎓 DVWA	Damn Vulnerable Web Application
📚 OWASP XSS	Cross Site Scripting (XSS)
⭐ Благодарности

    DVWA — за отличный учебный полигон

    PortSwigger — за вдохновение

    Всем, кто ставит звезды и форкает проект 🙌

<p align="center"> <b>Сделано с 🐍 и ☕ в Kali Linux</b><br> <a href="#"><b>⬆ Наверх</b></a> </p> ```
