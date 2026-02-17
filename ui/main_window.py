# ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, Signal
from PySide6.QtGui import QFont, QFontDatabase
from styles.theme_manager import ThemeManager
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from components.loading_indicator import LoadingIndicator

class MainWindow(QMainWindow):
    """Janela principal com design moderno"""
    
    optimization_requested = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.current_page = "dashboard"
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        """Inicializa a interface"""
        self.setWindowTitle("Windows Optimizer Pro")
        self.setMinimumSize(1200, 700)
        
        # Aplicar tema global
        self.setStyleSheet(ThemeManager.get_stylesheet())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal com sidebar
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Container do conteúdo
        self.content_container = QFrame()
        self.content_container.setProperty("class", "Card")
        self.content_container.setStyleSheet("""
            QFrame {
                background-color: #0B1C2D;
                border: none;
                border-radius: 0px;
                margin: 0px;
            }
        """)
        
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(20)
        
        main_layout.addWidget(self.content_container)
        
        # Header do conteúdo
        self.setup_content_header()
        
        # Dashboard principal
        self.dashboard = Dashboard()
        self.content_layout.addWidget(self.dashboard)
        
        # Loading indicator
        self.loading = LoadingIndicator()
        self.content_layout.addWidget(self.loading, 0, Qt.AlignCenter)
        
        # Conectar sinais da sidebar
        self.connect_sidebar_signals()
        
    def setup_content_header(self):
        """Configura o cabeçalho do conteúdo"""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("QFrame { background-color: transparent; }")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título da página
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 24px;
                font-weight: 600;
            }}
        """)
        
        # Ações do header
        actions_frame = QFrame()
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setSpacing(10)
        
        self.btn_settings = QPushButton("Configurações")
        self.btn_settings.setProperty("class", "SecondaryButton")
        self.btn_settings.setFixedHeight(36)
        
        self.btn_help = QPushButton("Ajuda")
        self.btn_help.setProperty("class", "SecondaryButton")
        self.btn_help.setFixedHeight(36)
        
        actions_layout.addWidget(self.btn_settings)
        actions_layout.addWidget(self.btn_help)
        
        header_layout.addWidget(self.page_title)
        header_layout.addStretch()
        header_layout.addWidget(actions_frame)
        
        self.content_layout.addWidget(header)
        
    def connect_sidebar_signals(self):
        """Conecta os sinais da sidebar"""
        self.sidebar.btn_dashboard.clicked.connect(lambda: self.change_page("dashboard"))
        self.sidebar.btn_quick_optimize.clicked.connect(lambda: self.change_page("quick_optimize"))
        self.sidebar.btn_deep_clean.clicked.connect(lambda: self.change_page("deep_clean"))
        self.sidebar.btn_diagnostics.clicked.connect(lambda: self.change_page("diagnostics"))
        self.sidebar.btn_startup.clicked.connect(lambda: self.change_page("startup"))
        self.sidebar.btn_services.clicked.connect(lambda: self.change_page("services"))
        self.sidebar.btn_network.clicked.connect(lambda: self.change_page("network"))
        
    def setup_animations(self):
        """Configura animações da janela"""
        # Animação de fade-in
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        # Iniciar fade-in
        QTimer.singleShot(100, self.fade_animation.start)
        
    def change_page(self, page_name):
        """Muda a página atual com animação"""
        if page_name == self.current_page:
            return
            
        # Atualizar título
        titles = {
            "dashboard": "Dashboard",
            "quick_optimize": "Otimizacao Rapida",
            "deep_clean": "Limpeza Profunda",
            "diagnostics": "Diagnostico do Sistema",
            "startup": "Gerenciar Inicializacao",
            "services": "Servicos do Windows",
            "network": "Otimizacao de Rede"
        }
        
        self.page_title.setText(titles.get(page_name, page_name))
        self.current_page = page_name
        
        # Emitir sinal de otimização se for uma ação
        if page_name in ["quick_optimize", "deep_clean"]:
            self.optimization_requested.emit(page_name)
            
    def show_loading(self, show=True):
        """Mostra ou esconde o indicador de loading"""
        self.dashboard.setVisible(not show)
        self.loading.setVisible(show)
        
    def log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log no dashboard"""
        if hasattr(self.dashboard, 'log_message'):
            self.dashboard.log_message(message, msg_type)
            
    def update_progress(self, value):
        """Atualiza barra de progresso"""
        if hasattr(self.dashboard, 'update_progress'):
            self.dashboard.update_progress(value)
            
    def set_buttons_enabled(self, enabled):
        """Habilita/desabilita botões"""
        if hasattr(self.dashboard, 'set_buttons_enabled'):
            self.dashboard.set_buttons_enabled(enabled)