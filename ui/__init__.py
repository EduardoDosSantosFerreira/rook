# ui/__init__.py
"""
Módulo de interface do usuário do Windows Optimizer Pro
Contém todos os componentes da interface gráfica
"""

from .main_window import MainWindow
from .sidebar import Sidebar, SidebarButton
from .dashboard import Dashboard, MetricCard

__all__ = [
    'MainWindow',
    'Sidebar',
    'SidebarButton',
    'Dashboard',
    'MetricCard'
]

__version__ = '2.0.0'
__author__ = 'Windows Optimizer Pro Team'

print(f"[INFO] Interface UI v{__version__} carregada")