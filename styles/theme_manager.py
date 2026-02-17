# styles/theme_manager.py
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject

class ThemeManager(QObject):
    """Gerenciador de temas e animações"""
    
    # Paleta de cores baseada em azul profundo
    COLORS = {
        'background_primary': '#0B1C2D',
        'background_secondary': '#102A43',
        'background_card': '#102A43',
        'hover': '#163A5F',
        'active': '#1F4E79',
        'text_primary': '#E6F1FF',
        'text_secondary': '#9FB3C8',
        'success': '#1ABC9C',
        'error': '#E74C3C',
        'warning': '#F39C12',
        'info': '#3498DB',
        'border': '#1F4E79',
        'border_light': '#163A5F',
    }
    
    # Tipografia
    FONTS = {
        'heading': {
            'family': 'Segoe UI',
            'size': 24,
            'weight': 600
        },
        'subheading': {
            'family': 'Segoe UI',
            'size': 18,
            'weight': 500
        },
        'body': {
            'family': 'Segoe UI',
            'size': 12,
            'weight': 400
        },
        'small': {
            'family': 'Segoe UI',
            'size': 10,
            'weight': 400
        },
        'mono': {
            'family': 'Consolas, Monaco, monospace',
            'size': 11,
            'weight': 400
        }
    }
    
    @classmethod
    def get_color(cls, name):
        return cls.COLORS.get(name, '#FFFFFF')
    
    @classmethod
    def get_stylesheet(cls):
        """Retorna a stylesheet principal"""
        return f"""
            /* Estilos Globais */
            QWidget {{
                background-color: {cls.COLORS['background_primary']};
                color: {cls.COLORS['text_primary']};
                font-family: 'Segoe UI';
                font-size: 12px;
            }}
            
            /* Cards */
            .Card {{
                background-color: {cls.COLORS['background_card']};
                border-radius: 12px;
                padding: 16px;
                border: 1px solid {cls.COLORS['border']};
            }}
            
            .Card:hover {{
                border: 1px solid {cls.COLORS['active']};
                background-color: {cls.COLORS['hover']};
            }}
            
            /* Botões Primários */
            QPushButton.PrimaryButton {{
                background-color: {cls.COLORS['active']};
                color: {cls.COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                min-width: 120px;
            }}
            
            QPushButton.PrimaryButton:hover {{
                background-color: {cls.COLORS['hover']};
            }}
            
            QPushButton.PrimaryButton:pressed {{
                background-color: {cls.COLORS['background_secondary']};
            }}
            
            QPushButton.PrimaryButton:disabled {{
                background-color: {cls.COLORS['background_secondary']};
                color: {cls.COLORS['text_secondary']};
            }}
            
            /* Botões Secundários */
            QPushButton.SecondaryButton {{
                background-color: transparent;
                color: {cls.COLORS['text_primary']};
                border: 1px solid {cls.COLORS['border']};
                border-radius: 8px;
                padding: 9px 19px;
                font-weight: 500;
            }}
            
            QPushButton.SecondaryButton:hover {{
                background-color: {cls.COLORS['hover']};
                border: 1px solid {cls.COLORS['active']};
            }}
            
            /* Botões de Ação */
            QPushButton.SuccessButton {{
                background-color: {cls.COLORS['success']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            
            QPushButton.ErrorButton {{
                background-color: {cls.COLORS['error']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            
            /* Barra de Progresso */
            QProgressBar {{
                border: none;
                background-color: {cls.COLORS['background_secondary']};
                border-radius: 6px;
                text-align: center;
                height: 20px;
            }}
            
            QProgressBar::chunk {{
                background-color: {cls.COLORS['success']};
                border-radius: 6px;
            }}
            
            /* Scrollbar */
            QScrollBar:vertical {{
                border: none;
                background-color: {cls.COLORS['background_secondary']};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {cls.COLORS['active']};
                border-radius: 6px;
                min-height: 30px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {cls.COLORS['hover']};
            }}
            
            QScrollBar:horizontal {{
                border: none;
                background-color: {cls.COLORS['background_secondary']};
                height: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {cls.COLORS['active']};
                border-radius: 6px;
                min-width: 30px;
            }}
            
            /* Inputs */
            QLineEdit, QTextEdit {{
                background-color: {cls.COLORS['background_secondary']};
                border: 1px solid {cls.COLORS['border']};
                border-radius: 8px;
                padding: 8px;
                color: {cls.COLORS['text_primary']};
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid {cls.COLORS['active']};
            }}
            
            /* Toggle Switch */
            QCheckBox::indicator {{
                width: 40px;
                height: 20px;
                border-radius: 10px;
            }}
            
            QCheckBox::indicator:unchecked {{
                background-color: {cls.COLORS['background_secondary']};
                border: 1px solid {cls.COLORS['border']};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {cls.COLORS['success']};
                border: 1px solid {cls.COLORS['success']};
            }}
            
            /* Área de Log */
            .LogArea {{
                background-color: {cls.COLORS['background_secondary']};
                border: 1px solid {cls.COLORS['border']};
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }}
            
            /* Status Indicators */
            .StatusSuccess {{
                color: {cls.COLORS['success']};
                font-weight: 600;
            }}
            
            .StatusError {{
                color: {cls.COLORS['error']};
                font-weight: 600;
            }}
            
            .StatusWarning {{
                color: {cls.COLORS['warning']};
                font-weight: 600;
            }}
            
            .StatusInfo {{
                color: {cls.COLORS['info']};
                font-weight: 600;
            }}
        """