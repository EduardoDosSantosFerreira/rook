# styles/theme_manager.py
class ThemeManager:
    """Gerenciador de temas e estilos"""
    
    # Paleta de cores azul profundo
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
    
    @classmethod
    def get_stylesheet(cls):
        """Retorna a stylesheet principal"""
        return f"""
            QWidget {{
                background-color: {cls.COLORS['background_primary']};
                color: {cls.COLORS['text_primary']};
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 12px;
            }}
            
            QFrame#contentContainer {{
                background-color: {cls.COLORS['background_primary']};
                border: none;
            }}
            
            QFrame#pageStack {{
                background-color: {cls.COLORS['background_primary']};
                border: none;
            }}
            
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
        """