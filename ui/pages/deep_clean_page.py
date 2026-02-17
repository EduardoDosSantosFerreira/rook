# ui/pages/deep_clean_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, QCheckBox
from PySide6.QtCore import Qt, Signal, QTimer
from ui.components.log_area import LogArea
from styles.theme_manager import ThemeManager
import os
import tempfile
import shutil
from pathlib import Path

class DeepCleanPage(QWidget):
    """Página de limpeza profunda"""
    
    log_message = Signal(str, str)
    progress_updated = Signal(int)  # Renomeado
    
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
        title = QLabel("Limpeza Profunda")
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
            "Remove arquivos temporários, cache do sistema, esvazia a lixeira "
            "e realiza uma limpeza completa para liberar espaço em disco."
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
        
        # Opções de limpeza
        options_label = QLabel("Opções de Limpeza:")
        options_label.setStyleSheet(f"""
            QLabel {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 16px;
                font-weight: 600;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(options_label)
        
        self.chk_temp = QCheckBox("Arquivos Temporários")
        self.chk_temp.setChecked(True)
        self.chk_temp.setStyleSheet(f"""
            QCheckBox {{
                color: {ThemeManager.COLORS['text_primary']};
                font-size: 14px;
                padding: 5px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {ThemeManager.COLORS['border']};
                background-color: transparent;
            }}
            QCheckBox::indicator:checked {{
                background-color: {ThemeManager.COLORS['success']};
                border: 2px solid {ThemeManager.COLORS['success']};
            }}
        """)
        
        self.chk_recycle = QCheckBox("Esvaziar Lixeira")
        self.chk_recycle.setChecked(True)
        self.chk_recycle.setStyleSheet(self.chk_temp.styleSheet())
        
        self.chk_prefetch = QCheckBox("Prefetch")
        self.chk_prefetch.setChecked(True)
        self.chk_prefetch.setStyleSheet(self.chk_temp.styleSheet())
        
        layout.addWidget(self.chk_temp)
        layout.addWidget(self.chk_recycle)
        layout.addWidget(self.chk_prefetch)
        
        # Botão iniciar
        self.btn_start = QPushButton("🧹 Iniciar Limpeza Profunda")
        self.btn_start.setFixedHeight(45)
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.setStyleSheet(f"""
            QPushButton {{
                background-color: {ThemeManager.COLORS['active']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: {ThemeManager.COLORS['hover']};
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
        self.btn_start.clicked.connect(self.start_cleanup)
        
    def start_cleanup(self):
        """Inicia o processo de limpeza"""
        if self.is_running:
            return
            
        self.is_running = True
        self.btn_start.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.log_area.add_message("Iniciando limpeza profunda...", "info")
        
        # Simular progresso
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_cleanup_step)
        self.timer.start(800)
        
    def run_cleanup_step(self):
        """Executa um passo da limpeza"""
        self.progress += 25
        self.progress_bar.setValue(self.progress)
        self.progress_updated.emit(self.progress)
        
        if self.progress == 25 and self.chk_temp.isChecked():
            self.clean_temp_files()
        elif self.progress == 50 and self.chk_recycle.isChecked():
            self.clean_recycle_bin()
        elif self.progress == 75 and self.chk_prefetch.isChecked():
            self.clean_prefetch()
        elif self.progress >= 100:
            self.finish_cleanup()
            
    def clean_temp_files(self):
        """Limpa arquivos temporários"""
        try:
            temp_dir = tempfile.gettempdir()
            count = 0
            size = 0
            
            for item in Path(temp_dir).glob('*'):
                try:
                    if item.is_file():
                        size += item.stat().st_size
                        item.unlink()
                        count += 1
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                except:
                    pass
                    
            size_mb = size / (1024 * 1024)
            self.log_area.add_message(
                f"Arquivos temporários: {count} itens removidos ({size_mb:.1f} MB)", 
                "success"
            )
        except Exception as e:
            self.log_area.add_message(f"Erro ao limpar temporários: {str(e)}", "error")
            
    def clean_recycle_bin(self):
        """Esvazia a lixeira"""
        try:
            import ctypes
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0001)
            self.log_area.add_message("Lixeira esvaziada com sucesso", "success")
        except Exception as e:
            self.log_area.add_message(f"Erro ao esvaziar lixeira: {str(e)}", "error")
            
    def clean_prefetch(self):
        """Limpa pasta Prefetch"""
        try:
            prefetch_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch')
            if os.path.exists(prefetch_dir):
                count = 0
                for file in Path(prefetch_dir).glob('*'):
                    try:
                        if file.is_file():
                            file.unlink()
                            count += 1
                    except:
                        pass
                        
                self.log_area.add_message(f"Prefetch: {count} arquivos removidos", "success")
        except Exception as e:
            self.log_area.add_message(f"Erro ao limpar Prefetch: {str(e)}", "error")
            
    def finish_cleanup(self):
        """Finaliza a limpeza"""
        self.timer.stop()
        self.log_area.add_message("✅ Limpeza profunda concluída!", "success")
        self.progress_bar.setVisible(False)
        self.btn_start.setEnabled(True)
        self.is_running = False
        
    def add_log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        self.log_area.add_message(message, msg_type)