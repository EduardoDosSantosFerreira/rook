# ui/sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt
from styles.theme_manager import ThemeManager

class SidebarButton(QPushButton):
    """Botão da sidebar com ícone e animação"""
    
    def __init__(self, text, icon="⚡", parent=None):
        super().__init__(f" {icon}  {text}", parent)
        self.setFixedHeight(45)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {ThemeManager.COLORS['text_secondary']};
                border: none;
                border-radius: 8px;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                color: {ThemeManager.COLORS['text_primary']};
            }}
            QPushButton:checked {{
                background-color: {ThemeManager.COLORS['active']};
                color: {ThemeManager.COLORS['text_primary']};
                font-weight: 600;
            }}
        """)
        self.setCheckable(True)

class Sidebar(QFrame):
    """Sidebar moderna com navegação"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setProperty("class", "Card")
        self.setStyleSheet(f"""
            Sidebar {{
                background-color: {ThemeManager.COLORS['background_secondary']};
                border-right: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 0px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(8)
        
        # Logo
        logo = QLabel("WOP")
        logo.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 22px;
                font-weight: bold;
                padding: 10px;
                margin-bottom: 20px;
            }}
        """)
        layout.addWidget(logo)
        
        # Seção: Otimização
        section_title = QLabel("OTIMIZACAO")
        section_title.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 11px;
                font-weight: 600;
                padding: 10px 10px 5px 10px;
                letter-spacing: 1px;
            }}
        """)
        layout.addWidget(section_title)
        
        # Botões de navegação
        self.btn_dashboard = SidebarButton("Dashboard", "📊")
        self.btn_quick_optimize = SidebarButton("Otimizacao Rapida", "⚡")
        self.btn_deep_clean = SidebarButton("Limpeza Profunda", "🧹")
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_quick_optimize)
        layout.addWidget(self.btn_deep_clean)
        
        # Seção: Ferramentas
        section_title2 = QLabel("FERRAMENTAS")
        section_title2.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 11px;
                font-weight: 600;
                padding: 20px 10px 5px 10px;
                letter-spacing: 1px;
            }}
        """)
        layout.addWidget(section_title2)
        
        self.btn_diagnostics = SidebarButton("Diagnostico", "🔍")
        self.btn_startup = SidebarButton("Inicializacao", "🚀")
        self.btn_services = SidebarButton("Servicos", "⚙️")
        self.btn_network = SidebarButton("Rede", "🌐")
        
        layout.addWidget(self.btn_diagnostics)
        layout.addWidget(self.btn_startup)
        layout.addWidget(self.btn_services)
        layout.addWidget(self.btn_network)
        
        # Espaçador
        layout.addStretch()
        
        # Status
        status_frame = QFrame()
        status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ThemeManager.COLORS['background_primary']};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        status_layout = QVBoxLayout(status_frame)
        status_layout.setSpacing(5)
        
        status_title = QLabel("STATUS DO SISTEMA")
        status_title.setStyleSheet(f"color: {ThemeManager.COLORS['text_secondary']}; font-size: 10px;")
        
        status_value = QLabel("Otimizado")
        status_value.setStyleSheet(f"color: {ThemeManager.COLORS['success']}; font-size: 12px; font-weight: 600;")
        
        status_layout.addWidget(status_title)
        status_layout.addWidget(status_value)
        
        layout.addWidget(status_frame)
        
        # Selecionar primeiro botão por padrão
        self.btn_dashboard.setChecked(True)