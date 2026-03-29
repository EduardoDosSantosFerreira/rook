# core/logger.py
"""
Sistema de logs - Mantém registro de todas as operações
"""
import logging
from datetime import datetime
from pathlib import Path


class Logger:
    """Gerenciador de logs"""
    
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
        
        self._logger = logging.getLogger('rook')
        self._messages = []
    
    def info(self, message: str):
        """Registra mensagem informativa"""
        self._logger.info(message)
        self._messages.append(('info', message))
    
    def success(self, message: str):
        """Registra sucesso"""
        self._logger.info(f"SUCCESS: {message}")
        self._messages.append(('success', message))
    
    def warning(self, message: str):
        """Registra aviso"""
        self._logger.warning(message)
        self._messages.append(('warning', message))
    
    def error(self, message: str):
        """Registra erro"""
        self._logger.error(message)
        self._messages.append(('error', message))
    
    def get_recent(self, limit: int = 100) -> list:
        """Retorna mensagens recentes"""
        return self._messages[-limit:]