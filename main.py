# main.py
import sys
import os

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, Signal

from ui.main_window import MainWindow
from styles.theme_manager import ThemeManager
from modules import (
    StartupOptimizer, ServicesOptimizer, PowerOptimizer,
    CleanupOptimizer, SystemOptimizer, NetworkOptimizer,
    Diagnostics, RestoreManager, Logger
)

class OptimizationThread(QThread):
    """Thread para executar otimizações"""
    log_signal = Signal(str, str)
    progress_signal = Signal(int)
    finished_signal = Signal()
    
    def __init__(self, optimization_type='quick_optimize'):
        super().__init__()
        self.optimization_type = optimization_type
        self.logger = Logger()
        
        # Inicializar módulos
        self.modules = {
            'restore': RestoreManager(),
            'startup': StartupOptimizer(),
            'services': ServicesOptimizer(),
            'power': PowerOptimizer(),
            'cleanup': CleanupOptimizer(),
            'system': SystemOptimizer(),
            'network': NetworkOptimizer(),
            'diagnostics': Diagnostics()
        }
        
    def run(self):
        try:
            if not self._check_admin():
                self.log_signal.emit("ERROR: Execute como administrador!", "error")
                self.finished_signal.emit()
                return
            
            self.log_signal.emit("INFO: Criando ponto de restauracao...", "info")
            if self.modules['restore'].create_restore_point():
                self.log_signal.emit("SUCCESS: Ponto de restauracao criado", "success")
            
            self.progress_signal.emit(10)
            
            if self.optimization_type in ['quick_optimize', 'deep_clean']:
                self._run_quick_optimize()
                
            if self.optimization_type == 'deep_clean':
                self._run_deep_clean()
                
            self.progress_signal.emit(100)
            self.log_signal.emit("SUCCESS: Otimizacao concluida!", "success")
            
        except Exception as e:
            self.log_signal.emit(f"ERROR: {str(e)}", "error")
        finally:
            self.finished_signal.emit()
    
    def _run_quick_optimize(self):
        """Otimização rápida"""
        self.log_signal.emit("INFO: Executando otimizacao rapida...", "info")
        
        # Limpeza básica
        self.modules['cleanup'].clean_temp_files()
        self.progress_signal.emit(30)
        
        # Otimização de energia
        self.modules['power'].apply_optimizations()
        self.progress_signal.emit(50)
        
        # Ajustes rápidos do sistema
        self.modules['system'].disable_background_apps()
        self.modules['system'].disable_notifications()
        self.progress_signal.emit(70)
        
        # Diagnóstico básico
        self.modules['diagnostics'].check_disk_health()
        self.progress_signal.emit(90)
        
        self.log_signal.emit("SUCCESS: Otimizacao rapida concluida!", "success")
    
    def _run_deep_clean(self):
        """Limpeza profunda"""
        self.log_signal.emit("INFO: Executando limpeza profunda...", "info")
        
        # Limpeza avançada
        self.modules['cleanup'].clean_windows_update_cache()
        self.modules['cleanup'].clean_winsxs()
        self.modules['cleanup'].clean_thumbnails_cache()
        self.modules['cleanup'].clean_recycle_bin()
        self.modules['cleanup'].rebuild_icon_cache()
        
        self.log_signal.emit("SUCCESS: Limpeza profunda concluida!", "success")
    
    def _check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        
        self.window = MainWindow()
        self.window.optimization_requested.connect(self.start_optimization)
        
        self.optimization_thread = None
        self.logger = Logger()
        
    def start_optimization(self, opt_type):
        if self.optimization_thread and self.optimization_thread.isRunning():
            self.window.log_message("WARNING: Otimizacao em andamento!", "warning")
            return
            
        self.window.show_loading(True)
        self.window.set_buttons_enabled(False)
        
        self.optimization_thread = OptimizationThread(opt_type)
        self.optimization_thread.log_signal.connect(self.window.log_message)
        self.optimization_thread.progress_signal.connect(self.window.update_progress)
        self.optimization_thread.finished_signal.connect(self.optimization_finished)
        self.optimization_thread.start()
        
    def optimization_finished(self):
        self.window.show_loading(False)
        self.window.set_buttons_enabled(True)
        self.window.log_message("SUCCESS: Pronto!", "success")
        
    def run(self):
        self.window.show()
        return self.app.exec()

def main():
    # Configurar para alta DPI
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    
    # Suprimir warnings de UTF-8 no Windows
    if sys.platform == 'win32':
        import warnings
        warnings.filterwarnings('ignore', category=UnicodeWarning)
    
    app = Application()
    sys.exit(app.run())

if __name__ == '__main__':
    main()