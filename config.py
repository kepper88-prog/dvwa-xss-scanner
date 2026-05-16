import os

PROXY = os.getenv("PROXY", "http://127.0.0.1:8080")
USE_PROXY = os.getenv("USE_PROXY", "false").lower() == "true"

REQUEST_TIMEOUT = 10
RETRY_COUNT = 3
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"

PAYLOADS_DIR = "payloads"
LOGS_DIR = "logs"
SAVE_HTTP_LOGS = True
