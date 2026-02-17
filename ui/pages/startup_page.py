# ui/pages/startup_page.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                               QProgressBar)
from PySide6.QtCore import Qt, Signal, QTimer
from ui.components.log_area import LogArea
from styles.theme_manager import ThemeManager
import winreg

class StartupPage(QWidget):
    """Página de gerenciamento de inicialização"""
    
    log_message = Signal(str, str)
    
    def __init__(self, log_manager, system_manager):
        super().__init__()
        self.log_manager = log_manager
        self.system_manager = system_manager
        self.setup_ui()
        self.load_startup_items()
        
    def setup_ui(self):
        """Configura a interface da página"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Gerenciar Programas de Inicialização")
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
            "Gerencie quais programas iniciam automaticamente com o Windows. "
            "Desativar programas desnecessários pode melhorar o tempo de inicialização."
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
        
        # Tabela de programas
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Programa", "Comando", "Localização", "Ação"])
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
        
        self.btn_refresh = QPushButton("🔄 Atualizar Lista")
        self.btn_refresh.setFixedHeight(36)
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.setStyleSheet(self.get_button_style())
        
        actions_layout.addWidget(self.btn_refresh)
        actions_layout.addStretch()
        
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
        
        # Conectar botões
        self.btn_refresh.clicked.connect(self.load_startup_items)
        
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
        
    def load_startup_items(self):
        """Carrega itens de inicialização do registro"""
        self.table.setRowCount(0)
        
        try:
            # HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                self.add_registry_items(key, "HKCU")
                winreg.CloseKey(key)
            except:
                pass
                
            # HKEY_LOCAL_MACHINE
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                self.add_registry_items(key, "HKLM")
                winreg.CloseKey(key)
            except:
                pass
                
            self.log_area.add_message(f"Carregados {self.table.rowCount()} programas de inicialização", "success")
            
        except Exception as e:
            self.log_area.add_message(f"Erro ao carregar inicialização: {str(e)}", "error")
            
    def add_registry_items(self, key, location):
        """Adiciona itens do registro à tabela"""
        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                # Nome
                self.table.setItem(row, 0, QTableWidgetItem(name))
                
                # Comando (truncar se muito longo)
                cmd = value
                if len(cmd) > 60:
                    cmd = cmd[:60] + "..."
                self.table.setItem(row, 1, QTableWidgetItem(cmd))
                
                # Localização
                self.table.setItem(row, 2, QTableWidgetItem(location))
                
                # Botão desativar
                btn_disable = QPushButton("Desativar")
                btn_disable.setFixedHeight(28)
                btn_disable.setCursor(Qt.PointingHandCursor)
                btn_disable.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {ThemeManager.COLORS['error']};
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
                btn_disable.clicked.connect(lambda checked, n=name, l=location: self.disable_item(n, l))
                
                self.table.setCellWidget(row, 3, btn_disable)
                
                i += 1
            except WindowsError:
                break
                
    def disable_item(self, name, location):
        """Desativa um item de inicialização"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            if location == "HKCU":
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            else:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            
            self.log_area.add_message(f"Item desativado: {name}", "success")
            self.load_startup_items()  # Recarregar lista
            
        except Exception as e:
            self.log_area.add_message(f"Erro ao desativar {name}: {str(e)}", "error")
            
    def add_log_message(self, message, msg_type="info"):
        """Adiciona mensagem ao log"""
        if hasattr(self, 'log_area'):
            self.log_area.add_message(message, msg_type)

# Garantir que a classe seja exportada
__all__ = ['StartupPage']