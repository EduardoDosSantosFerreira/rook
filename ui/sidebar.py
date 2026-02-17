# ui/sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt, Signal

from styles.theme_manager import ThemeManager

class SidebarButton(QPushButton):
    """Botão da sidebar com estilo moderno"""
    
    def __init__(self, text, icon, page_name, parent=None):
        super().__init__(f"   {icon}   {text}", parent)
        self.page_name = page_name
        self.setFixedHeight(48)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {ThemeManager.COLORS['text_secondary']};
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                margin: 2px 10px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                color: {ThemeManager.COLORS['text_primary']};
            }}
            QPushButton:checked {{
                background-color: {ThemeManager.COLORS['active']};
                color: {ThemeManager.COLORS['text_primary']};
                font-weight: 600;
                border-left: 3px solid {ThemeManager.COLORS['success']};
            }}
        """)

class Sidebar(QFrame):
    """Sidebar principal do aplicativo"""
    
    page_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        self.setObjectName("sidebar")
        
        self.setStyleSheet(f"""
            #sidebar {{
                background-color: {ThemeManager.COLORS['background_secondary']};
                border-right: 1px solid {ThemeManager.COLORS['border']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(5)
        
        # Logo
        logo_container = QFrame()
        logo_container.setFixedHeight(80)
        logo_layout = QVBoxLayout(logo_container)
        
        logo = QLabel("rook")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
        """)
        
        version = QLabel("v2.0")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 11px;
            }}
        """)
        
        logo_layout.addWidget(logo)
        logo_layout.addWidget(version)
        layout.addWidget(logo_container)
        
        # Espaço
        layout.addSpacing(20)
        
        # Seção: OTIMIZAÇÃO
        section_label = QLabel("OTIMIZAÇÃO")
        section_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 11px;
                font-weight: 600;
                padding: 10px 20px;
                letter-spacing: 1px;
            }}
        """)
        layout.addWidget(section_label)
        
        # Botões de otimização
        self.btn_dashboard = SidebarButton("Dashboard", "📊", "dashboard")
        self.btn_quick = SidebarButton("Otimização Rápida", "⚡", "quick_optimize")
        self.btn_deep = SidebarButton("Limpeza Profunda", "🧹", "deep_clean")
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_quick)
        layout.addWidget(self.btn_deep)
        
        # Seção: FERRAMENTAS
        section_label2 = QLabel("FERRAMENTAS")
        section_label2.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 11px;
                font-weight: 600;
                padding: 20px 20px 10px 20px;
                letter-spacing: 1px;
            }}
        """)
        layout.addWidget(section_label2)
        
        # Botões de ferramentas
        self.btn_diagnostics = SidebarButton("Diagnóstico", "🔍", "diagnostics")
        self.btn_startup = SidebarButton("Inicialização", "🚀", "startup")
        self.btn_services = SidebarButton("Serviços", "⚙️", "services")
        self.btn_network = SidebarButton("Rede", "🌐", "network")
        
        layout.addWidget(self.btn_diagnostics)
        layout.addWidget(self.btn_startup)
        layout.addWidget(self.btn_services)
        layout.addWidget(self.btn_network)
        
        # Espaçador
        layout.addStretch()
        
        # Status do sistema
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_frame.setFixedHeight(80)
        status_frame.setStyleSheet(f"""
            #statusFrame {{
                background-color: {ThemeManager.COLORS['background_primary']};
                border-radius: 10px;
                margin: 10px;
                padding: 10px;
            }}
        """)
        
        status_layout = QVBoxLayout(status_frame)
        
        status_title = QLabel("STATUS DO SISTEMA")
        status_title.setStyleSheet(f"color: {ThemeManager.COLORS['text_secondary']}; font-size: 10px;")
        
        status_value = QLabel("● Online")
        status_value.setStyleSheet(f"color: {ThemeManager.COLORS['success']}; font-size: 13px; font-weight: 600;")
        
        status_layout.addWidget(status_title)
        status_layout.addWidget(status_value)
        
        layout.addWidget(status_frame)
        
        # Conectar botões - CORREÇÃO AQUI
        self.btn_dashboard.clicked.connect(lambda: self.on_button_clicked("dashboard"))
        self.btn_quick.clicked.connect(lambda: self.on_button_clicked("quick_optimize"))
        self.btn_deep.clicked.connect(lambda: self.on_button_clicked("deep_clean"))
        self.btn_diagnostics.clicked.connect(lambda: self.on_button_clicked("diagnostics"))
        self.btn_startup.clicked.connect(lambda: self.on_button_clicked("startup"))
        self.btn_services.clicked.connect(lambda: self.on_button_clicked("services"))
        self.btn_network.clicked.connect(lambda: self.on_button_clicked("network"))
        
        # Selecionar dashboard por padrão
        self.btn_dashboard.setChecked(True)
        
    def on_button_clicked(self, page_name):
        """Handler para clique em botão"""
        # Desmarcar todos os botões
        buttons = [
            self.btn_dashboard, self.btn_quick, self.btn_deep,
            self.btn_diagnostics, self.btn_startup, self.btn_services,
            self.btn_network
        ]
        
        for btn in buttons:
            btn.setChecked(False)
        
        # Encontrar e marcar o botão correto
        for btn in buttons:
            if hasattr(btn, 'page_name') and btn.page_name == page_name:
                btn.setChecked(True)
                break
            
        # Emitir sinal de mudança de página
        self.page_changed.emit(page_name)