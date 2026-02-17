# components/__init__.py
"""
Componentes reutilizáveis da interface do Windows Optimizer Pro
Contém widgets personalizados e animados
"""

from .animated_button import AnimatedButton
from .animated_card import AnimatedCard
from .image_card import ImageCard
from .loading_indicator import LoadingIndicator

__all__ = [
    'AnimatedButton',
    'AnimatedCard',
    'ImageCard',
    'LoadingIndicator'
]

__version__ = '1.0.0'

print(f"[INFO] Componentes UI v{__version__} carregados")