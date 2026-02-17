# modules/logger.py
import logging
from datetime import datetime
from pathlib import Path

class Logger:
    """Gerencia logs do sistema"""
    
    def __init__(self):
        self.log_dir = Path.home() / 'WindowsOptimizer_Logs'
        self.log_dir.mkdir(exist_ok=True)
        
        log_file = self.log_dir / f'optimizer_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
    def log_action(self, action, status):
        """Registra uma ação no log"""
        logging.info(f"{action}: {status}")