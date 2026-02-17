# ui/pages/services_page.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                               QProgressBar, QComboBox)
from PySide6.QtCore import Qt, Signal, QTimer
from ui.components.log_area import LogArea
from styles.theme_manager import ThemeManager
import subprocess

class ServicesPage(QWidget):
    """Página de gerenciamento de serviços"""
    
    log_message = Signal(str, str)
    
    def __init__(self, log_manager, system_manager):
        super().__init__()
        self.log_manager = log_manager
        self.system_manager = system_manager
        self.services = []
        self.setup_ui()
        self.load_services()
        
    def setup_ui(self):
        """Configura a interface da página"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Gerenciar Serviços do Windows")
        title.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 24px;
                font-weight: 600;
            }}
        """)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(
            "Gerencie os serviços do Windows. Desativar serviços desnecessários "
            "pode melhorar o desempenho e a segurança do sistema."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_secondary']};
                font-size: 14px;
                margin-bottom: 20px;
            }}
        """)
        layout.addWidget(desc)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("Filtrar:")
        filter_label.setStyleSheet(f"color: {ThemeManager.COLORS['text_secondary']};")
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Todos", "Em Execução", "Parados"])
        self.filter_combo.setFixedWidth(150)
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {ThemeManager.COLORS['background_card']};
                color: {ThemeManager.COLORS['text_primary']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 6px;
                padding: 5px;
            }}
        """)
        
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # Tabela de serviços
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nome", "Nome de Exibição", "Status", "Ação"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {ThemeManager.COLORS['background_card']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 8px;
                gridline-color: {ThemeManager.COLORS['border']};
            }}
            QTableWidget::item {{
                padding: 8px;
                color: {ThemeManager.COLORS['text_primary']};
            }}
            QTableWidget::item:selected {{
                background-color: {ThemeManager.COLORS['active']};
            }}
            QHeaderView::section {{
                background-color: {ThemeManager.COLORS['background_secondary']};
                color: {ThemeManager.COLORS['text_primary']};
                padding: 8px;
                border: none;
                font-weight: 600;
            }}
        """)
        
        layout.addWidget(self.table)
        
        # Botões de ação
        actions_layout = QHBoxLayout()
        
        self.btn_refresh = QPushButton("🔄 Atualizar")
        self.btn_refresh.setFixedHeight(36)
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.setStyleSheet(self.get_button_style())
        
        actions_layout.addWidget(self.btn_refresh)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)
        
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
        self.btn_refresh.clicked.connect(self.load_services)
        
    def get_button_style(self):
        """Retorna estilo dos botões"""
        return f"""
            QPushButton {{
                background-color: {ThemeManager.COLORS['background_card']};
                color: {ThemeManager.COLORS['text_primary']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                border: 1px solid {ThemeManager.COLORS['active']};
            }}
        """
        
    def load_services(self):
        """Carrega lista de serviços"""
        self.table.setRowCount(0)
        self.services = []
        
        try:
            result = subprocess.run(['sc', 'query', 'state=', 'all'], 
                                   capture_output=True, text=True, shell=True)
            
            lines = result.stdout.split('\n')
            current_service = {}
            
            for line in lines:
                if 'SERVICE_NAME:' in line:
                    if current_service:
                        self.services.append(current_service)
                    current_service = {'name': line.split(':')[1].strip()}
                elif 'DISPLAY_NAME:' in line:
                    current_service['display_name'] = line.split(':')[1].strip()
                elif 'STATE' in line:
                    if 'RUNNING' in line:
                        current_service['state'] = 'running'
                    else:
                        current_service['state'] = 'stopped'
                        
            if current_service:
                self.services.append(current_service)
                
            self.apply_filter()
            self.log_area.add_message(f"Carregados {len(self.services)} serviços", "success")
            
        except Exception as e:
            self.log_area.add_message(f"Erro ao carregar serviços: {str(e)}", "error")
            
    def apply_filter(self):
        """Aplica filtro à tabela"""
        filter_text = self.filter_combo.currentText()
        self.table.setRowCount(0)
        
        for service in self.services[:20]:  # Limitar a 20 serviços para performance
            # Aplicar filtro
            if filter_text == "Em Execução" and service.get('state') != 'running':
                continue
            elif filter_text == "Parados" and service.get('state') != 'stopped':
                continue
                
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Nome
            self.table.setItem(row, 0, QTableWidgetItem(service.get('name', '')))
            
            # Nome de exibição
            self.table.setItem(row, 1, QTableWidgetItem(service.get('display_name', '')))
            
            # Status
            status_item = QTableWidgetItem(service.get('state', 'unknown'))
            if service.get('state') == 'running':
                status_item.setForeground(Qt.green)
            else:
                status_item.setForeground(Qt.red)
            self.table.setItem(row, 2, status_item)
            
            # Botão de ação
            btn = QPushButton("Parar" if service.get('state') == 'running' else "Iniciar")
            btn.setFixedHeight(28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ThemeManager.COLORS['success'] if service.get('state') != 'running' else ThemeManager.COLORS['error']};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {ThemeManager.COLORS['warning']};
                }}
            """)
            
            if service.get('state') == 'running':
                btn.clicked.connect(lambda checked, n=service.get('name'): self.stop_service(n))
            else:
                btn.clicked.connect(lambda checked, n=service.get('name'): self.start_service(n))
                
            self.table.setCellWidget(row, 3, btn)
            
    def stop_service(self, service_name):
        """Para um serviço"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        try:
            result = subprocess.run(['net', 'stop', service_name], 
                                   capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.log_area.add_message(f"Serviço {service_name} parado", "success")
                QTimer.singleShot(1000, self.load_services)
            else:
                self.log_area.add_message(f"Erro ao parar {service_name}", "error")
        except Exception as e:
            self.log_area.add_message(f"Erro: {str(e)}", "error")
            
        self.progress_bar.setVisible(False)
            
    def start_service(self, service_name):
        """Inicia um serviço"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        try:
            result = subprocess.run(['net', 'start', service_name], 
                                   capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.log_area.add_message(f"Serviço {service_name} iniciado", "success")
                QTimer.singleShot(1000, self.load_services)
            else:
                self.log_area.add_message(f"Erro ao iniciar {service_name}", "error")
        except Exception as e:
            self.log_area.add_message(f"Erro: {str(e)}", "error")
            
        self.progress_bar.setVisible(False)
            
    def add_log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        if hasattr(self, 'log_area'):
            self.log_area.add_message(message, msg_type)

# Garantir que a classe seja exportada
__all__ = ['ServicesPage']