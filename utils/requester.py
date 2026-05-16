import requests
from config import REQUEST_TIMEOUT, USER_AGENT, PROXY, USE_PROXY
from utils.logger import get_logger

logger = get_logger(__name__)

class Requester:
    def __init__(self):
        # Создаём сессию ОДИН раз и используем её для всех запросов
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        
        if USE_PROXY:
            self.session.proxies = {"http": PROXY, "https": PROXY}
            logger.info(f"Using proxy: {PROXY}")
        else:
            logger.info("Direct connection (no proxy)")
    
    def get(self, url, params=None):
        logger.debug(f"GET {url}")
        try:
            response = self.session.get(
                url, 
                params=params, 
                timeout=REQUEST_TIMEOUT
            )
            logger.debug(f"Response: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def post(self, url, data=None):
        logger.debug(f"POST {url}")
        try:
            response = self.session.post(
                url, 
                data=data, 
                timeout=REQUEST_TIMEOUT
            )
            logger.debug(f"Response: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def get_cookies(self):
        """Возвращает текущие cookies сессии"""
        return self.session.cookies.get_dict()
