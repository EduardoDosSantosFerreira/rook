# ui/components/metric_card.py
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from styles.theme_manager import ThemeManager

class MetricCard(QFrame):
    """Card para exibir métricas do sistema"""
    
    def __init__(self, title, value, description, icon, color=ThemeManager.COLORS['active'], parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.setFixedHeight(140)
        
        self.setStyleSheet(f"""
            #metricCard {{
                background-color: {ThemeManager.COLORS['background_card']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 12px;
                padding: 15px;
            }}
            #metricCard:hover {{
                border: 1px solid {color};
                background-color: {ThemeManager.COLORS['hover']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Header do card (título + ícone)
        header_layout = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 13px;
                font-weight: 500;
            }}
        """)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 20px;
            }}
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(icon_label)
        
        # Valor
        self.value_label = QLabel(value)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 32px;
                font-weight: 600;
                padding: 5px 0;
            }}
        """)
        
        # Descrição
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 11px;
                font-style: italic;
            }}
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.value_label)
        layout.addWidget(desc_label)
        
    def update_value(self, value):
        """Atualiza o valor do card"""
        self.value_label.setText(value)