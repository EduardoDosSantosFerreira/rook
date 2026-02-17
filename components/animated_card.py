# components/animated_card.py
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property, Qt
from PySide6.QtGui import QPainter, QColor, QBrush

class AnimatedCard(QFrame):
    """Card com animação de elevação"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._elevation = 0
        self.title = title
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        self.setProperty("class", "Card")
        self.setMinimumHeight(100)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #E6F1FF;")
            layout.addWidget(title_label)
        
    def setup_animations(self):
        self._elevation_animation = QPropertyAnimation(self, b"elevation")
        self._elevation_animation.setDuration(200)
        self._elevation_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def _get_elevation(self):
        return self._elevation
        
    def _set_elevation(self, value):
        self._elevation = value
        self.update()
        
    elevation = Property(float, _get_elevation, _set_elevation)
    
    def enterEvent(self, event):
        self._elevation_animation.setStartValue(0)
        self._elevation_animation.setEndValue(10)
        self._elevation_animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._elevation_animation.setStartValue(10)
        self._elevation_animation.setEndValue(0)
        self._elevation_animation.start()
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        super().paintEvent(event)
        if self._elevation > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Desenhar sombra baseada na elevação
            shadow_color = QColor(0, 0, 0, int(20 * self._elevation))
            painter.setBrush(QBrush(shadow_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)