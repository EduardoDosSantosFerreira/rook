# ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QStackedWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, Signal

from styles.theme_manager import ThemeManager
from ui.sidebar import Sidebar
from ui.components.header import Header
from ui.pages.dashboard_page import DashboardPage
from ui.pages.quick_optimize_page import QuickOptimizePage
from ui.pages.deep_clean_page import DeepCleanPage
from ui.pages.diagnostics_page import DiagnosticsPage
from ui.pages.startup_page import StartupPage
from ui.pages.services_page import ServicesPage
from ui.pages.network_page import NetworkPage

class MainWindow(QMainWindow):
    """Janela principal do rook"""
    
    optimization_requested = Signal(str)
    
    def __init__(self, log_manager, system_manager):
        super().__init__()
        self.log_manager = log_manager
        self.system_manager = system_manager
        self.current_page = "dashboard"
        
        self.setWindowTitle("rook - Otimizador de Sistema")
        self.setMinimumSize(1300, 800)
        
        # Aplicar tema
        self.setStyleSheet(ThemeManager.get_stylesheet())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.change_page)
        main_layout.addWidget(self.sidebar)
        
        # Container de conteúdo
        content_container = QFrame()
        content_container.setObjectName("contentContainer")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Header
        self.header = Header("Dashboard")
        content_layout.addWidget(self.header)
        
        # Stacked Widget para páginas
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("pageStack")
        
        # Inicializar páginas
        self.pages = {
            "dashboard": DashboardPage(self.log_manager, self.system_manager),
            "quick_optimize": QuickOptimizePage(self.log_manager, self.system_manager),
            "deep_clean": DeepCleanPage(self.log_manager, self.system_manager),
            "diagnostics": DiagnosticsPage(self.log_manager, self.system_manager),
            "startup": StartupPage(self.log_manager, self.system_manager),
            "services": ServicesPage(self.log_manager, self.system_manager),
            "network": NetworkPage(self.log_manager, self.system_manager)
        }
        
        # Adicionar páginas ao stacked widget
        for page in self.pages.values():
            self.stacked_widget.addWidget(page)
            
        content_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(content_container, 1)
        
        # Conectar sinais das páginas
        self.connect_page_signals()
        
        # Configurar animações
        self.setup_animations()
        
    def connect_page_signals(self):
        """Conecta sinais das páginas"""
        for page in self.pages.values():
            if hasattr(page, 'log_message'):
                page.log_message.connect(self.log_message)
            # Conectar sinais de progresso se existirem
            if hasattr(page, 'progress_updated'):
                page.progress_updated.connect(self.update_progress)
                
    def setup_animations(self):
        """Configura animações da janela"""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(400)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        QTimer.singleShot(100, self.fade_animation.start)
        
    def change_page(self, page_name):
        """Muda a página atual"""
        if page_name == self.current_page:
            return
            
        # Atualizar header
        page_titles = {
            "dashboard": "Dashboard",
            "quick_optimize": "Otimização Rápida",
            "deep_clean": "Limpeza Profunda",
            "diagnostics": "Diagnóstico do Sistema",
            "startup": "Gerenciar Inicialização",
            "services": "Serviços do Windows",
            "network": "Otimização de Rede"
        }
        
        self.header.set_title(page_titles.get(page_name, page_name))
        
        # Mudar página no stacked widget
        if page_name in self.pages:
            self.stacked_widget.setCurrentWidget(self.pages[page_name])
            self.current_page = page_name
            
    def log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'add_log_message'):
            current_widget.add_log_message(message, msg_type)
            
    def update_progress(self, value):
        """Atualiza barra de progresso na página atual"""
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'progress_bar'):
            current_widget.progress_bar.setVisible(True)
            current_widget.progress_bar.setValue(value)