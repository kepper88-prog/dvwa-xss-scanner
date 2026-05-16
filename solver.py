#!/usr/bin/env python3
import sys
from utils.logger import get_logger
from labs.dvwa_xss import DVWAXSSSolver

logger = get_logger(__name__)

def banner():
    print("""
    ╔═══════════════════════════════════════════╗
    ║   🐉 Web Security Auto Solver - Kali     ║
    ║   DVWA | PortSwigger | More...          ║
    ╚═══════════════════════════════════════════╝
    """)

def main():
    banner()
    
    if len(sys.argv) < 2:
        logger.error("Usage: python3 solver.py <target_url>")
        logger.info("Example for DVWA: python3 solver.py http://localhost:8081")
        logger.info("Example for PortSwigger: python3 solver.py https://0abc...")
        sys.exit(1)
    
    target_url = sys.argv[1]
    logger.info(f"[*] Target: {target_url}")
    
    # Пробуем разные солверы
    solvers = [DVWAXSSSolver]
    
    for SolverClass in solvers:
        logger.info(f"[*] Trying {SolverClass.__name__}...")
        solver = SolverClass(target_url)
        if solver.solve():
            logger.info("\n[🎉] SUCCESS! Vulnerability found and exploited!")
            logger.info("[*] Check your browser to confirm")
            return
    
    logger.error("\n[❌] Could not exploit target")

if __name__ == "__main__":
    main()
