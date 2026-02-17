# ui/pages/diagnostics_page.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QProgressBar, QGridLayout, QFrame)
from PySide6.QtCore import Qt, Signal, QTimer
from ui.components.log_area import LogArea
from styles.theme_manager import ThemeManager
import psutil
import platform
import subprocess

class DiagnosticsPage(QWidget):
    """Página de diagnóstico do sistema"""
    
    log_message = Signal(str, str)
    progress_updated = Signal(int)
    
    def __init__(self, log_manager, system_manager):
        super().__init__()
        self.log_manager = log_manager
        self.system_manager = system_manager
        self.setup_ui()
        self.update_system_info()
        
    def setup_ui(self):
        """Configura a interface da página"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Diagnóstico do Sistema")
        title.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 24px;
                font-weight: 600;
            }}
        """)
        layout.addWidget(title)
        
        # Grid de informações
        info_grid = QGridLayout()
        info_grid.setSpacing(15)
        
        self.info_labels = {}
        info_items = [
            ("Sistema Operacional", "os", "🖥️"),
            ("Processador", "cpu", "⚡"),
            ("Memória RAM", "ram", "📊"),
            ("Disco C:", "disk", "💾"),
        ]
        
        for i, (title, key, icon) in enumerate(info_items):
            card = self.create_info_card(title, "Carregando...", icon)
            info_grid.addWidget(card, i // 2, i % 2)
            self.info_labels[key] = card.findChild(QLabel, "valueLabel")
        
        layout.addLayout(info_grid)
        
        # Botões de diagnóstico
        btn_layout = QGridLayout()
        btn_layout.setSpacing(10)
        
        self.btn_sfc = QPushButton("🔍 Executar SFC /scannow")
        self.btn_sfc.setFixedHeight(40)
        self.btn_sfc.setCursor(Qt.PointingHandCursor)
        self.btn_sfc.clicked.connect(self.run_sfc)
        self.btn_sfc.setStyleSheet(self.get_button_style())
        
        self.btn_chkdsk = QPushButton("💿 Verificar Disco (CHKDSK)")
        self.btn_chkdsk.setFixedHeight(40)
        self.btn_chkdsk.setCursor(Qt.PointingHandCursor)
        self.btn_chkdsk.clicked.connect(self.run_chkdsk)
        self.btn_chkdsk.setStyleSheet(self.get_button_style())
        
        btn_layout.addWidget(self.btn_sfc, 0, 0)
        btn_layout.addWidget(self.btn_chkdsk, 0, 1)
        
        layout.addLayout(btn_layout)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(20)
        layout.addWidget(self.progress_bar)
        
        # Área de log
        log_label = QLabel("Resultados do Diagnóstico")
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
        self.log_area.setMaximumHeight(200)
        layout.addWidget(self.log_area)
        
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
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
                border: 1px solid {ThemeManager.COLORS['active']};
            }}
        """
        
    def create_info_card(self, title, value, icon):
        """Cria um card de informação"""
        card = QFrame()
        card.setObjectName("infoCard")
        card.setStyleSheet(f"""
            #infoCard {{
                background-color: {ThemeManager.COLORS['background_card']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # Título com ícone
        title_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"color: {ThemeManager.COLORS['info']}; font-size: 20px;")
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {ThemeManager.COLORS['text_secondary']}; font-size: 12px;")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("valueLabel")
        value_label.setWordWrap(True)
        value_label.setStyleSheet(f"""
            QLabel#valueLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 13px;
                margin-top: 5px;
            }}
        """)
        
        layout.addLayout(title_layout)
        layout.addWidget(value_label)
        
        return card
        
    def update_system_info(self):
        """Atualiza informações do sistema"""
        try:
            # Sistema Operacional
            os_info = f"{platform.system()} {platform.release()}"
            if 'os' in self.info_labels:
                self.info_labels['os'].setText(os_info)
            
            # Processador
            cpu_info = platform.processor() or "Desconhecido"
            if len(cpu_info) > 50:
                cpu_info = cpu_info[:50] + "..."
            if 'cpu' in self.info_labels:
                self.info_labels['cpu'].setText(cpu_info)
            
            # Memória RAM
            memory = psutil.virtual_memory()
            total_gb = memory.total / (1024**3)
            used_gb = memory.used / (1024**3)
            if 'ram' in self.info_labels:
                self.info_labels['ram'].setText(f"{used_gb:.1f} GB / {total_gb:.1f} GB ({memory.percent}%)")
            
            # Disco
            disk = psutil.disk_usage('C:')
            total_gb = disk.total / (1024**3)
            used_gb = disk.used / (1024**3)
            if 'disk' in self.info_labels:
                self.info_labels['disk'].setText(f"{used_gb:.1f} GB / {total_gb:.1f} GB ({disk.percent}%)")
            
        except Exception as e:
            self.add_log_message(f"Erro ao atualizar informações: {str(e)}", "error")
            
    def run_sfc(self):
        """Executa SFC /scannow"""
        self.log_area.add_message("Iniciando SFC /scannow...", "info")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.progress_updated.emit(0)
        
        try:
            result = subprocess.run(['sfc', '/scannow'], 
                                   capture_output=True, text=True, shell=True)
            
            if "did not find any integrity violations" in result.stdout:
                self.log_area.add_message("SFC: Nenhuma violação de integridade encontrada", "success")
            elif "found corrupt files and successfully repaired" in result.stdout:
                self.log_area.add_message("SFC: Arquivos corrompidos encontrados e reparados", "success")
            else:
                self.log_area.add_message("SFC: Verificação concluída", "info")
                
        except Exception as e:
            self.log_area.add_message(f"Erro no SFC: {str(e)}", "error")
        finally:
            self.progress_bar.setVisible(False)
            self.progress_updated.emit(100)
            
    def run_chkdsk(self):
        """Executa CHKDSK"""
        self.log_area.add_message("Verificando disco C:...", "info")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.progress_updated.emit(0)
        
        try:
            result = subprocess.run(['chkdsk', 'C:', '/scan'], 
                                   capture_output=True, text=True, shell=True)
            
            if "no problems" in result.stdout.lower():
                self.log_area.add_message("CHKDSK: Nenhum problema encontrado no disco", "success")
            else:
                self.log_area.add_message("CHKDSK: Verificação concluída", "info")
                
        except Exception as e:
            self.log_area.add_message(f"Erro ao executar CHKDSK: {str(e)}", "error")
            
        self.progress_bar.setVisible(False)
        self.progress_updated.emit(100)
        
    def add_log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        self.log_area.add_message(message, msg_type)