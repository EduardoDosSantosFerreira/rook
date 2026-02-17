# ui/components/log_area.py
from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from datetime import datetime
from styles.theme_manager import ThemeManager

class LogArea(QTextEdit):
    """Área de log com formatação especial"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumHeight(150)
        self.setObjectName("logArea")
        
        self.setStyleSheet(f"""
            #logArea {{
                background-color: {ThemeManager.COLORS['background_secondary']};
                color: {ThemeManager.COLORS['text_primary']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }}
        """)
        
    def add_message(self, message, msg_type="info"):
        """Adiciona uma mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "info": ThemeManager.COLORS['info'],
            "success": ThemeManager.COLORS['success'],
            "error": ThemeManager.COLORS['error'],
            "warning": ThemeManager.COLORS['warning']
        }
        
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️"
        }
        
        color = colors.get(msg_type, ThemeManager.COLORS['text_secondary'])
        icon = icons.get(msg_type, "📝")
        
        formatted_msg = f'<span style="color: {color};"><b>[{timestamp}]</b> {icon} {message}</span><br>'
        
        self.insertHtml(formatted_msg)
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()