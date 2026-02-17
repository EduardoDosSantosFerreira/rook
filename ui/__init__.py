# ui/__init__.py
"""
Módulo de interface do usuário do rook
"""

from .main_window import MainWindow
from .sidebar import Sidebar

__all__ = ['MainWindow', 'Sidebar']

__version__ = '1.0.0'

print(f"[INFO] Interface UI v{__version__} carregada")