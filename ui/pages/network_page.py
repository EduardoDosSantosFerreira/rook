# ui/pages/network_page.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QProgressBar, QFrame, QGridLayout)
from PySide6.QtCore import Qt, Signal, QTimer
from ui.components.log_area import LogArea
from styles.theme_manager import ThemeManager
import subprocess
import socket

class NetworkPage(QWidget):
    """Página de otimização de rede"""
    
    log_message = Signal(str, str)
    update_progress = Signal(int)
    
    def __init__(self, log_manager, system_manager):
        super().__init__()
        self.log_manager = log_manager
        self.system_manager = system_manager
        self.setup_ui()
        self.update_network_info()
        
    def setup_ui(self):
        """Configura a interface da página"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Otimização de Rede")
        title.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 24px;
                font-weight: 600;
            }}
        """)
        layout.addWidget(title)
        
        # Informações de rede
        info_label = QLabel("Informações de Rede")
        info_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 18px;
                font-weight: 600;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(info_label)
        
        # Cards de informação
        info_grid = QGridLayout()
        info_grid.setSpacing(10)
        
        self.ip_card = self.create_info_card("Endereço IP", "Carregando...")
        self.hostname_card = self.create_info_card("Nome do Computador", "Carregando...")
        self.status_card = self.create_info_card("Status da Conexão", "Carregando...")
        
        info_grid.addWidget(self.ip_card, 0, 0)
        info_grid.addWidget(self.hostname_card, 0, 1)
        info_grid.addWidget(self.status_card, 1, 0)
        
        layout.addLayout(info_grid)
        
        # Ações de rede
        actions_label = QLabel("Ferramentas de Rede")
        actions_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 18px;
                font-weight: 600;
                margin-top: 20px;
            }}
        """)
        layout.addWidget(actions_label)
        
        # Botões de ação
        btn_layout = QGridLayout()
        btn_layout.setSpacing(10)
        
        self.btn_flush_dns = QPushButton("🔄 Limpar Cache DNS")
        self.btn_flush_dns.setFixedHeight(45)
        self.btn_flush_dns.setCursor(Qt.PointingHandCursor)
        self.btn_flush_dns.setStyleSheet(self.get_action_button_style())
        
        self.btn_reset_winsock = QPushButton("🛠️ Resetar Winsock")
        self.btn_reset_winsock.setFixedHeight(45)
        self.btn_reset_winsock.setCursor(Qt.PointingHandCursor)
        self.btn_reset_winsock.setStyleSheet(self.get_action_button_style())
        
        btn_layout.addWidget(self.btn_flush_dns, 0, 0)
        btn_layout.addWidget(self.btn_reset_winsock, 0, 1)
        
        layout.addLayout(btn_layout)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(20)
        layout.addWidget(self.progress_bar)
        
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
        
        # Conectar botões
        self.btn_flush_dns.clicked.connect(self.flush_dns)
        self.btn_reset_winsock.clicked.connect(self.reset_winsock)
        
        # Timer para atualizar informações
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_network_info)
        self.update_timer.start(5000)
        
    def get_action_button_style(self):
        """Retorna estilo dos botões de ação"""
        return f"""
            QPushButton {{
                background-color: {ThemeManager.COLORS['background_card']};
                color: {ThemeManager.COLORS['text_primary']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                border: 1px solid {ThemeManager.COLORS['active']};
            }}
            QPushButton:disabled {{
                background-color: {ThemeManager.COLORS['background_secondary']};
                color: {ThemeManager.COLORS['text_secondary']};
            }}
        """
        
    def create_info_card(self, title, value):
        """Cria um card de informação"""
        card = QFrame()
        card.setObjectName("infoCard")
        card.setStyleSheet(f"""
            #infoCard {{
                background-color: {ThemeManager.COLORS['background_card']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {ThemeManager.COLORS['text_secondary']}; font-size: 12px;")
        
        value_label = QLabel(value)
        value_label.setObjectName("valueLabel")
        value_label.setWordWrap(True)
        value_label.setStyleSheet(f"""
            QLabel#valueLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 14px;
                font-weight: 600;
                margin-top: 5px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
        
    def update_network_info(self):
        """Atualiza informações de rede"""
        try:
            # Hostname
            hostname = socket.gethostname()
            self.hostname_card.value_label.setText(hostname)
            
            # IP (tentativa de obter IP local)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                self.ip_card.value_label.setText(ip)
            except:
                self.ip_card.value_label.setText("Não disponível")
            
            # Status da conexão
            try:
                result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                                       capture_output=True, text=True, shell=True, timeout=5)
                if result.returncode == 0:
                    self.status_card.value_label.setText("Conectado")
                    self.status_card.value_label.setStyleSheet(f"""
                        color: {ThemeManager.COLORS['success']};
                        font-size: 14px;
                        font-weight: 600;
                    """)
                else:
                    self.status_card.value_label.setText("Desconectado")
                    self.status_card.value_label.setStyleSheet(f"""
                        color: {ThemeManager.COLORS['error']};
                        font-size: 14px;
                        font-weight: 600;
                    """)
            except:
                self.status_card.value_label.setText("Verificando...")
                
        except Exception as e:
            if hasattr(self, 'log_area'):
                self.log_area.add_message(f"Erro ao atualizar rede: {str(e)}", "error")
            
    def flush_dns(self):
        """Limpa cache DNS"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.log_area.add_message("Limpando cache DNS...", "info")
        
        try:
            result = subprocess.run(['ipconfig', '/flushdns'], 
                                   capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.log_area.add_message("Cache DNS limpo com sucesso", "success")
            else:
                self.log_area.add_message("Erro ao limpar cache DNS", "error")
        except Exception as e:
            self.log_area.add_message(f"Erro: {str(e)}", "error")
            
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        
    def reset_winsock(self):
        """Reseta Winsock"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.log_area.add_message("Resetando Winsock...", "info")
        
        try:
            result = subprocess.run(['netsh', 'winsock', 'reset'], 
                                   capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.log_area.add_message("Winsock resetado com sucesso", "success")
            else:
                self.log_area.add_message("Erro ao resetar Winsock", "error")
        except Exception as e:
            self.log_area.add_message(f"Erro: {str(e)}", "error")
            
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        
    def add_log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        if hasattr(self, 'log_area'):
            self.log_area.add_message(message, msg_type)
        
    def update_progress(self, value):
        """Atualiza barra de progresso"""
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(value)

# Garantir que a classe seja exportada
__all__ = ['NetworkPage']