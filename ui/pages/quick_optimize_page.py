# ui/pages/quick_optimize_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PySide6.QtCore import Qt, Signal, QTimer
from ui.components.log_area import LogArea
from styles.theme_manager import ThemeManager
import os
import tempfile
import shutil
from pathlib import Path

class QuickOptimizePage(QWidget):
    """Página de otimização rápida"""
    
    log_message = Signal(str, str)
    progress_updated = Signal(int)  # Renomeado para não conflitar com o método
    
    def __init__(self, log_manager, system_manager):
        super().__init__()
        self.log_manager = log_manager
        self.system_manager = system_manager
        self.is_running = False
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface da página"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Otimização Rápida")
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
            "Aplica ajustes básicos de desempenho no sistema, "
            "incluindo limpeza de arquivos temporários e otimizações simples."
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
        
        # Botão iniciar
        self.btn_start = QPushButton("▶ Iniciar Otimização Rápida")
        self.btn_start.setFixedHeight(45)
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.setStyleSheet(f"""
            QPushButton {{
                background-color: {ThemeManager.COLORS['success']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['active']};
            }}
            QPushButton:disabled {{
                background-color: {ThemeManager.COLORS['background_secondary']};
                color: {ThemeManager.COLORS['text_secondary']};
            }}
        """)
        
        layout.addWidget(self.btn_start)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(20)
        layout.addWidget(self.progress_bar)
        
        # Área de log
        log_label = QLabel("Log da Operação")
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
        
        # Conectar botão
        self.btn_start.clicked.connect(self.start_optimization)
        
    def start_optimization(self):
        """Inicia o processo de otimização"""
        if self.is_running:
            return
            
        self.is_running = True
        self.btn_start.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.log_area.add_message("Iniciando otimização rápida...", "info")
        
        # Simular progresso
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_optimization_step)
        self.timer.start(500)
        
    def run_optimization_step(self):
        """Executa um passo da otimização"""
        self.progress += 20
        self.progress_bar.setValue(self.progress)
        self.progress_updated.emit(self.progress)  # Emitir sinal
        
        if self.progress == 20:
            self.clean_temp_files()
        elif self.progress == 40:
            self.clean_prefetch()
        elif self.progress == 60:
            self.clear_dns_cache()
        elif self.progress == 80:
            self.log_area.add_message("Otimizações aplicadas", "success")
        elif self.progress >= 100:
            self.finish_optimization()
            
    def clean_temp_files(self):
        """Limpa arquivos temporários"""
        try:
            temp_dir = tempfile.gettempdir()
            count = 0
            for item in Path(temp_dir).glob('*'):
                try:
                    if item.is_file():
                        item.unlink()
                        count += 1
                except:
                    pass
            self.log_area.add_message(f"Arquivos temporários: {count} itens removidos", "success")
        except Exception as e:
            self.log_area.add_message(f"Erro ao limpar temporários: {str(e)}", "error")
            
    def clean_prefetch(self):
        """Limpa pasta Prefetch"""
        try:
            prefetch_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch')
            if os.path.exists(prefetch_dir):
                count = 0
                for file in Path(prefetch_dir).glob('*.pf'):
                    try:
                        file.unlink()
                        count += 1
                    except:
                        pass
                self.log_area.add_message(f"Cache Prefetch: {count} arquivos removidos", "success")
        except Exception as e:
            self.log_area.add_message(f"Erro ao limpar Prefetch: {str(e)}", "error")
            
    def clear_dns_cache(self):
        """Limpa cache DNS"""
        try:
            import subprocess
            subprocess.run(['ipconfig', '/flushdns'], capture_output=True)
            self.log_area.add_message("Cache DNS limpo com sucesso", "success")
        except Exception as e:
            self.log_area.add_message(f"Erro ao limpar cache DNS: {str(e)}", "error")
            
    def finish_optimization(self):
        """Finaliza a otimização"""
        self.timer.stop()
        self.log_area.add_message("✅ Otimização rápida concluída!", "success")
        self.progress_bar.setVisible(False)
        self.btn_start.setEnabled(True)
        self.is_running = False
        
    def add_log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        self.log_area.add_message(message, msg_type)