# main.py
"""
rook - Windows Optimizer
Ferramenta leve e objetiva para otimização do Windows
"""
import sys
import os
import ctypes

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from core.logger import Logger
from core.optimizer import Optimizer


class Application:
    """Classe principal da aplicação"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.app.setApplicationName("rook")
        
        # Configurar DPI
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        os.environ["QT_SCALE_FACTOR"] = "1"
        
        # Inicializar componentes
        self.logger = Logger()
        self.optimizer = Optimizer(self.logger)
        
        # Criar janela
        self.window = MainWindow(self.logger, self.optimizer)
    
    def is_admin(self) -> bool:
        """Verifica se está rodando como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def run(self) -> int:
        """Executa a aplicação"""
        if not self.is_admin():
            self.window.show_warning(
                "Execute como administrador para todas as funcionalidades"
            )
        else:
            self.window.show_success("Executando com privilégios de administrador")
        
        self.window.show()
        return self.app.exec()


def main():
    app = Application()
    sys.exit(app.run())


if __name__ == '__main__':
    main()