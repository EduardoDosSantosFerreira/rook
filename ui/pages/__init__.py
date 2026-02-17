# ui/pages/__init__.py
"""
Páginas da interface do rook
"""

from .dashboard_page import DashboardPage
from .quick_optimize_page import QuickOptimizePage
from .deep_clean_page import DeepCleanPage
from .diagnostics_page import DiagnosticsPage
from .startup_page import StartupPage
from .services_page import ServicesPage
from .network_page import NetworkPage

__all__ = [
    'DashboardPage',
    'QuickOptimizePage',
    'DeepCleanPage',
    'DiagnosticsPage',
    'StartupPage',
    'ServicesPage',
    'NetworkPage'
]