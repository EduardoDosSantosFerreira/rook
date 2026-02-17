# ui/components/action_button.py
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from styles.theme_manager import ThemeManager

class ActionButton(QWidget):
    """Botão de ação com título e descrição"""
    
    def __init__(self, title, description, icon, color=ThemeManager.COLORS['active'], parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 100)
        self.setCursor(Qt.PointingHandCursor)
        
        # Botão principal (invisível, apenas para clique)
        self.button = QPushButton(self)
        self.button.setGeometry(0, 0, 180, 100)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Container do conteúdo
        container = QWidget(self)
        container.setGeometry(2, 2, 176, 96)
        container.setObjectName("actionContainer")
        container.setStyleSheet(f"""
            #actionContainer {{
                background-color: {ThemeManager.COLORS['background_card']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 10px;
            }}
            #actionContainer:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                border: 1px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Ícone e título
        title_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"color: {color}; font-size: 20px;")
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 14px;
                font-weight: 600;
            }}
        """)
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Descrição
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 10px;
            }}
        """)
        
        layout.addLayout(title_layout)
        layout.addWidget(desc_label)
        
    def click(self):
        """Simula clique no botão"""
        self.button.click()
        
    def clicked(self):
        """Retorna o sinal clicked do botão"""
        return self.button.clicked