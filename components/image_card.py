# components/image_card.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from .animated_card import AnimatedCard
import os

class ImageCard(AnimatedCard):
    """Card com suporte a imagens e thumbnails"""
    
    def __init__(self, title="", image_path=None, parent=None):
        super().__init__(title, parent)
        self.image_path = image_path
        self.setup_image_ui()
        
    def setup_image_ui(self):
        # Área de imagem
        self.image_container = QWidget()
        self.image_container.setFixedHeight(150)
        self.image_container.setStyleSheet("""
            QWidget {
                background-color: #102A43;
                border-radius: 8px;
            }
        """)
        
        image_layout = QVBoxLayout(self.image_container)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(200, 120)
        
        if self.image_path and os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            scaled_pixmap = pixmap.scaled(200, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            # Placeholder
            self.image_label.setText("[Sem imagem]")
            self.image_label.setStyleSheet("color: #9FB3C8; font-size: 14px;")
            
        image_layout.addWidget(self.image_label)
        
        # Adicionar ao layout principal
        self.layout().addWidget(self.image_container)
        
        # Info adicional
        info_layout = QHBoxLayout()
        
        size_label = QLabel("Tamanho: 2.3 MB" if self.image_path else "Tamanho: --")
        size_label.setStyleSheet("color: #9FB3C8; font-size: 11px;")
        
        type_label = QLabel("Tipo: PNG" if self.image_path else "Tipo: --")
        type_label.setStyleSheet("color: #9FB3C8; font-size: 11px;")
        
        info_layout.addWidget(size_label)
        info_layout.addWidget(type_label)
        info_layout.addStretch()
        
        self.layout().addLayout(info_layout)
        
    def set_image(self, image_path):
        """Define uma nova imagem no card"""
        self.image_path = image_path
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(200, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")