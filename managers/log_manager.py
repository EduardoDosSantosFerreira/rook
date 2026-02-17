# managers/log_manager.py
from datetime import datetime
from pathlib import Path
import logging

class LogManager:
    """Gerenciador de logs do sistema"""
    
    def __init__(self):
        self.log_dir = Path.home() / 'rook_logs'
        self.log_dir.mkdir(exist_ok=True)
        
        log_file = self.log_dir / f'rook_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        self.logger = logging.getLogger('rook')
        
    def info(self, message):
        """Registra mensagem informativa"""
        self.logger.info(message)
        print(f"[INFO] {message}")
        
    def success(self, message):
        """Registra sucesso"""
        self.logger.info(f"SUCCESS: {message}")
        print(f"[SUCCESS] {message}")
        
    def warning(self, message):
        """Registra aviso"""
        self.logger.warning(message)
        print(f"[WARNING] {message}")
        
    def error(self, message):
        """Registra erro"""
        self.logger.error(message)
        print(f"[ERROR] {message}")
        
    def get_recent_logs(self, lines=50):
        """Retorna logs recentes"""
        log_file = self.log_dir / f'rook_{datetime.now().strftime("%Y%m%d")}.log'
        if log_file.exists():
            with open(log_file, 'r') as f:
                return f.readlines()[-lines:]
        return []