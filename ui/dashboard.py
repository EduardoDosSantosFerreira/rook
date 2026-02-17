# ui/dashboard.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame, QProgressBar, QTextEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor
from datetime import datetime
from components.animated_card import AnimatedCard
from components.image_card import ImageCard
from styles.theme_manager import ThemeManager

class MetricCard(AnimatedCard):
    """Card para métricas do sistema"""
    
    def __init__(self, title, value, icon, color="#1F4E79", parent=None):
        super().__init__(title, parent)
        self.setMinimumHeight(120)
        
        # Valor
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 28px;
                font-weight: 600;
                margin-top: 10px;
            }}
        """)
        
        # Ícone
        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 24px;
            }}
        """)
        
        # Layout do conteúdo
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.value_label)
        content_layout.addStretch()
        content_layout.addWidget(self.icon_label)
        
        self.layout().addLayout(content_layout)
        
    def update_value(self, value):
        self.value_label.setText(value)

class Dashboard(QWidget):
    """Dashboard principal com métricas e controles"""
    
    optimization_requested = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Grid de métricas
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(16)
        
        # Cards de métricas
        self.cpu_card = MetricCard("CPU", "23%", "⚡", "#3498DB")
        self.ram_card = MetricCard("RAM", "4.2/16 GB", "📊", "#1ABC9C")
        self.disk_card = MetricCard("Disco C:", "124/512 GB", "💾", "#F39C12")
        self.temp_card = MetricCard("Temperatura", "45°C", "🌡️", "#E74C3C")
        
        metrics_grid.addWidget(self.cpu_card, 0, 0)
        metrics_grid.addWidget(self.ram_card, 0, 1)
        metrics_grid.addWidget(self.disk_card, 1, 0)
        metrics_grid.addWidget(self.temp_card, 1, 1)
        
        layout.addLayout(metrics_grid)
        
        # Ações rápidas
        actions_card = AnimatedCard("Ações Rápidas")
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        self.btn_quick = QPushButton("Otimização Rápida")
        self.btn_quick.setProperty("class", "SuccessButton")
        self.btn_quick.setFixedHeight(45)
        
        self.btn_deep = QPushButton("Limpeza Profunda")
        self.btn_deep.setProperty("class", "PrimaryButton")
        self.btn_deep.setFixedHeight(45)
        
        self.btn_analyze = QPushButton("Analisar Sistema")
        self.btn_analyze.setProperty("class", "SecondaryButton")
        self.btn_analyze.setFixedHeight(45)
        
        actions_layout.addWidget(self.btn_quick)
        actions_layout.addWidget(self.btn_deep)
        actions_layout.addWidget(self.btn_analyze)
        actions_layout.addStretch()
        
        actions_card.layout().addLayout(actions_layout)
        layout.addWidget(actions_card)
        
        # Barra de progresso
        progress_card = AnimatedCard("Progresso")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_card.layout().addWidget(self.progress_bar)
        layout.addWidget(progress_card)
        
        # Área de log
        log_card = AnimatedCard("Log de Operações")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(150)
        self.log_area.setProperty("class", "LogArea")
        log_card.layout().addWidget(self.log_area)
        layout.addWidget(log_card)
        
        # Recomendações
        recommendations_card = AnimatedCard("Recomendações")
        recommendations_layout = QVBoxLayout()
        
        rec1 = QLabel("- Seu SSD está com 85% de uso - Considere liberar espaço")
        rec1.setStyleSheet(f"color: {ThemeManager.COLORS['warning']}; padding: 5px;")
        
        rec2 = QLabel("- 15 programas podem ser removidos da inicialização")
        rec2.setStyleSheet(f"color: {ThemeManager.COLORS['info']}; padding: 5px;")
        
        rec3 = QLabel("- Última limpeza: 3 dias atrás")
        rec3.setStyleSheet(f"color: {ThemeManager.COLORS['text_secondary']}; padding: 5px;")
        
        recommendations_layout.addWidget(rec1)
        recommendations_layout.addWidget(rec2)
        recommendations_layout.addWidget(rec3)
        
        recommendations_card.layout().addLayout(recommendations_layout)
        layout.addWidget(recommendations_card)
        
    def log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "info": ThemeManager.COLORS['info'],
            "success": ThemeManager.COLORS['success'],
            "error": ThemeManager.COLORS['error'],
            "warning": ThemeManager.COLORS['warning']
        }
        
        icons = {
            "info": "[INFO]",
            "success": "[OK]",
            "error": "[ERRO]",
            "warning": "[AVISO]"
        }
        
        color = colors.get(msg_type, ThemeManager.COLORS['text_secondary'])
        icon = icons.get(msg_type, "[LOG]")
        
        formatted_msg = f'<span style="color: {color};"><b>[{timestamp}]</b> {icon} {message}</span><br>'
        
        self.log_area.insertHtml(formatted_msg)
        self.log_area.moveCursor(QTextCursor.End)
        
    def update_progress(self, value):
        """Atualiza barra de progresso"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(value)
        
    def set_buttons_enabled(self, enabled):
        """Habilita/desabilita botões"""
        self.btn_quick.setEnabled(enabled)
        self.btn_deep.setEnabled(enabled)
        self.btn_analyze.setEnabled(enabled)