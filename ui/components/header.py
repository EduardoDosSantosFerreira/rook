# ui/components/header.py
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

from styles.theme_manager import ThemeManager

class Header(QFrame):
    """Cabeçalho da aplicação"""
    
    def __init__(self, title="Dashboard", parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)
        self.setObjectName("header")
        
        self.setStyleSheet(f"""
            #header {{
                background-color: transparent;
                border-bottom: 1px solid {ThemeManager.COLORS['border']};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 0, 25, 0)
        
        # Título
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 22px;
                font-weight: 600;
            }}
        """)
        
        # Ações do header
        actions_frame = QFrame()
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setSpacing(10)
        
        self.btn_settings = QPushButton("⚙️ Configurações")
        self.btn_settings.setFixedHeight(36)
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {ThemeManager.COLORS['text_secondary']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                color: {ThemeManager.COLORS['text_primary']};
            }}
        """)
        
        self.btn_help = QPushButton("❓ Ajuda")
        self.btn_help.setFixedHeight(36)
        self.btn_help.setCursor(Qt.PointingHandCursor)
        self.btn_help.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {ThemeManager.COLORS['text_secondary']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                color: {ThemeManager.COLORS['text_primary']};
            }}
        """)
        
        actions_layout.addWidget(self.btn_settings)
        actions_layout.addWidget(self.btn_help)
        
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(actions_frame)
        
    def set_title(self, title):
        """Atualiza o título do header"""
        self.title_label.setText(title)