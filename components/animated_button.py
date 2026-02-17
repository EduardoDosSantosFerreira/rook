# components/animated_button.py
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor

class AnimatedButton(QPushButton):
    """Botão com animações suaves"""
    
    def __init__(self, text="", parent=None, button_type="primary"):
        super().__init__(text, parent)
        self.button_type = button_type
        self._animation_progress = 0
        self._hover_animation = QPropertyAnimation(self, b"animation_progress")
        self._hover_animation.setDuration(200)
        self._hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Configurar classes CSS
        self.setProperty("class", f"{button_type.capitalize()}Button")
        
    def _get_animation_progress(self):
        return self._animation_progress
        
    def _set_animation_progress(self, value):
        self._animation_progress = value
        self.update()
        
    animation_progress = Property(float, _get_animation_progress, _set_animation_progress)
    
    def enterEvent(self, event):
        self._hover_animation.setStartValue(0)
        self._hover_animation.setEndValue(1)
        self._hover_animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._hover_animation.setStartValue(1)
        self._hover_animation.setEndValue(0)
        self._hover_animation.start()
        super().leaveEvent(event)