# components/loading_indicator.py
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation, QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QBrush
import math

class LoadingIndicator(QWidget):
    """Indicador de loading animado"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)
        self.hide()
        
    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = 15
        
        for i in range(8):
            angle_rad = math.radians(self.angle + (i * 45))
            x = center.x() + radius * math.cos(angle_rad)
            y = center.y() + radius * math.sin(angle_rad)
            
            # Opacidade baseada na posição
            opacity = 0.2 + (0.8 * (i / 8))
            
            color = QColor(31, 78, 121)  # #1F4E79
            color.setAlphaF(opacity)
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(x, y), 3, 3)