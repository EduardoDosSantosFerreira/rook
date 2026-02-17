# styles/__init__.py
"""
Gerenciamento de estilos e temas do Windows Optimizer Pro
Contém configurações de cores, fontes e estilos globais
"""

from .theme_manager import ThemeManager

__all__ = [
    'ThemeManager'
]

__version__ = '1.0.0'

print(f"[INFO] Temas e estilos v{__version__} carregados")