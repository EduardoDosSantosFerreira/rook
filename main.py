# main.py
import sys
import os
import ctypes

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import MainWindow
from styles.theme_manager import ThemeManager
from managers.log_manager import LogManager
from managers.system_manager import SystemManager

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.app.setApplicationName("rook")
        
        # PySide6 lida com DPI automaticamente - removendo atributo deprecated
        
        # Inicializar gerenciadores
        self.log_manager = LogManager()
        self.system_manager = SystemManager()
        
        # Criar janela principal
        self.window = MainWindow(self.log_manager, self.system_manager)
        
    def check_admin(self):
        """Verifica se está rodando como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def run(self):
        """Executa a aplicação"""
        # Verificar permissões de admin
        if not self.check_admin():
            self.window.log_message("Execute como administrador para todas as funcionalidades", "warning")
        else:
            self.window.log_message("Executando com privilégios de administrador", "success")
            
        self.window.show()
        return self.app.exec()

def main():
    """Função principal"""
    # Configurar variáveis de ambiente para DPI
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    
    app = Application()
    sys.exit(app.run())

if __name__ == '__main__':
    main()