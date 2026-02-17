# components/__init__.py
"""
Componentes compartilhados do rook
"""

from .animated_card import AnimatedCard
from .loading_indicator import LoadingIndicator

__all__ = ['AnimatedCard', 'LoadingIndicator']

__version__ = '1.0.0'

print(f"[INFO] Componentes UI v{__version__} carregados")