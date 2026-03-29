# ui/widgets.py
"""
Componentes reutilizáveis da interface
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class Card(QFrame):
    """Card estilizado com borda arredondada"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet("""
            #card {
                background-color: #102A43;
                border: 1px solid #1F4E79;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #E6F1FF;
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 8px;
                }
            """)
            layout.addWidget(title_label)


class Button(QPushButton):
    """Botão estilizado"""
    
    def __init__(self, text: str, variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(42)
        
        colors = {
            "primary": {
                "bg": "#1F4E79",
                "hover": "#163A5F"
            },
            "success": {
                "bg": "#1ABC9C",
                "hover": "#16A085"
            },
            "danger": {
                "bg": "#E74C3C",
                "hover": "#C0392B"
            },
            "secondary": {
                "bg": "#2C3E50",
                "hover": "#1F2C38"
            }
        }
        
        color = colors.get(variant, colors["primary"])
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color['bg']};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 20px;
            }}
            QPushButton:hover {{
                background-color: {color['hover']};
            }}
            QPushButton:disabled {{
                background-color: #2C3E50;
                color: #7F8C8D;
            }}
        """)


class LogArea(QFrame):
    """Área para exibição de logs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("logArea")
        self.setStyleSheet("""
            #logArea {
                background-color: #0B1C2D;
                border: 1px solid #1F4E79;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        self._log_text = QLabel()
        self._log_text.setWordWrap(True)
        self._log_text.setTextFormat(Qt.RichText)
        self._log_text.setStyleSheet("""
            QLabel {
                color: #9FB3C8;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        
        layout.addWidget(self._log_text)
    
    def add_message(self, msg_type: str, message: str):
        """Adiciona uma mensagem ao log"""
        colors = {
            "info": "#3498DB",
            "success": "#1ABC9C",
            "warning": "#F39C12",
            "error": "#E74C3C"
        }
        
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        color = colors.get(msg_type, "#9FB3C8")
        icon = icons.get(msg_type, "📝")
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        current = self._log_text.text()
        new_line = f'<span style="color: {color};">[{timestamp}] {icon} {message}</span><br>'
        
        if current:
            self._log_text.setText(new_line + current)
        else:
            self._log_text.setText(new_line)
    
    def clear(self):
        """Limpa a área de log"""
        self._log_text.setText("")