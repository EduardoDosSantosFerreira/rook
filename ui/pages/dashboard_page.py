# ui/pages/dashboard_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PySide6.QtCore import Qt, Signal, QTimer
from ui.components.metric_card import MetricCard
from ui.components.action_button import ActionButton
from ui.components.log_area import LogArea
from styles.theme_manager import ThemeManager
import psutil
import random

class DashboardPage(QWidget):
    """Página de Dashboard com visão geral do sistema"""
    
    log_message = Signal(str, str)
    
    def __init__(self, log_manager, system_manager):
        super().__init__()
        self.log_manager = log_manager
        self.system_manager = system_manager
        self.setup_ui()
        self.start_monitoring()
        
    def setup_ui(self):
        """Configura a interface do dashboard"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Grid de métricas
        metrics_layout = QGridLayout()
        metrics_layout.setSpacing(15)
        
        # Cards de métricas
        self.cpu_card = MetricCard(
            "CPU",
            "0%",
            "Uso atual do processador em tempo real.",
            "⚡",
            "#3498DB"
        )
        
        self.ram_card = MetricCard(
            "RAM",
            "0/0 GB",
            "Memória utilizada pelo sistema.",
            "📊",
            "#1ABC9C"
        )
        
        self.disk_card = MetricCard(
            "Disco C:",
            "0/0 GB",
            "Espaço ocupado na unidade principal.",
            "💾",
            "#F39C12"
        )
        
        self.temp_card = MetricCard(
            "Temperatura",
            "0°C",
            "Temperatura média do sistema.",
            "🌡️",
            "#E74C3C"
        )
        
        metrics_layout.addWidget(self.cpu_card, 0, 0)
        metrics_layout.addWidget(self.ram_card, 0, 1)
        metrics_layout.addWidget(self.disk_card, 1, 0)
        metrics_layout.addWidget(self.temp_card, 1, 1)
        
        layout.addLayout(metrics_layout)
        
        # Ações Rápidas
        actions_label = QLabel("Ações Rápidas")
        actions_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 18px;
                font-weight: 600;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(actions_label)
        
        actions_layout = QGridLayout()
        actions_layout.setSpacing(15)
        
        self.btn_quick = ActionButton(
            "Otimização Rápida",
            "Aplica ajustes básicos de desempenho.",
            "⚡",
            ThemeManager.COLORS['success']
        )
        
        self.btn_deep = ActionButton(
            "Limpeza Profunda",
            "Remove arquivos temporários e resíduos.",
            "🧹",
            ThemeManager.COLORS['active']
        )
        
        self.btn_analyze = ActionButton(
            "Analisar Sistema",
            "Verifica integridade e desempenho geral.",
            "🔍",
            ThemeManager.COLORS['info']
        )
        
        actions_layout.addWidget(self.btn_quick, 0, 0)
        actions_layout.addWidget(self.btn_deep, 0, 1)
        actions_layout.addWidget(self.btn_analyze, 0, 2)
        actions_layout.setColumnStretch(3, 1)
        
        layout.addLayout(actions_layout)
        
        # Área de log
        log_label = QLabel("Log de Operações")
        log_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 16px;
                font-weight: 600;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(log_label)
        
        self.log_area = LogArea()
        layout.addWidget(self.log_area)
        
        # Recomendações
        rec_label = QLabel("Recomendações")
        rec_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 16px;
                font-weight: 600;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(rec_label)
        
        self.rec_label = QLabel("• Sistema operacional atualizado")
        self.rec_label.setStyleSheet(f"color: {ThemeManager.COLORS['text_secondary']}; padding: 3px 0;")
        layout.addWidget(self.rec_label)
        
    def start_monitoring(self):
        """Inicia monitoramento em tempo real"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(2000)
        
    def update_metrics(self):
        """Atualiza as métricas em tempo real"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_card.update_value(f"{cpu_percent:.1f}%")
            
            # RAM
            memory = psutil.virtual_memory()
            used_gb = memory.used / (1024**3)
            total_gb = memory.total / (1024**3)
            self.ram_card.update_value(f"{used_gb:.1f}/{total_gb:.1f} GB")
            
            # Disco
            disk = psutil.disk_usage('C:')
            used_gb = disk.used / (1024**3)
            total_gb = disk.total / (1024**3)
            self.disk_card.update_value(f"{used_gb:.0f}/{total_gb:.0f} GB")
            
            # Temperatura (simulada)
            temp = random.randint(35, 65)
            self.temp_card.update_value(f"{temp}°C")
            
            # Atualizar recomendações
            if disk.percent > 85:
                self.rec_label.setText("⚠️ Disco C: acima de 85% - Considere liberar espaço")
                self.rec_label.setStyleSheet(f"color: {ThemeManager.COLORS['error']}; padding: 3px 0;")
                
        except Exception as e:
            self.add_log_message(f"Erro ao atualizar métricas: {str(e)}", "error")
            
    def add_log_message(self, message, msg_type="info"):
        """Adiciona mensagem à área de log"""
        self.log_area.add_message(message, msg_type)