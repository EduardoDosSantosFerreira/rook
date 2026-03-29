# ui/main_window.py
"""
Janela principal da aplicação com checkboxes personalizáveis
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea, QCheckBox
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from ui.widgets import Card, Button, LogArea


class MainWindow(QMainWindow):
    """Janela principal do rook"""
    
    def __init__(self, logger, optimizer):
        super().__init__()
        self.logger = logger
        self.optimizer = optimizer
        self._running = False
        self._checkboxes = {}
        
        self.setWindowTitle("rook - Windows Optimizer")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)
        
        # Aplicar estilo global
        self.setStyleSheet(self._get_global_style())
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        
        # Layout principal
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Área de conteúdo com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(25)
        
        # Adicionar cards
        self._add_welcome_card()
        self._add_optimization_card()
        self._add_action_card()
        self._add_log_card()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        # Configurar animação
        self._setup_animation()
        
        # Carregar logs iniciais
        self._load_recent_logs()
    
    def _get_global_style(self) -> str:
        """Retorna o estilo global da aplicação"""
        return """
            QMainWindow {
                background-color: #0B1C2D;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #102A43;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #1F4E79;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #163A5F;
            }
            QScrollBar:horizontal {
                border: none;
                background-color: #102A43;
                height: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background-color: #1F4E79;
                border-radius: 5px;
                min-width: 30px;
            }
        """
    
    def _create_header(self) -> QFrame:
        """Cria o cabeçalho da aplicação"""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background-color: #102A43;
                border-bottom: 1px solid #1F4E79;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(25, 0, 25, 0)
        
        title = QLabel("rook")
        title.setStyleSheet("""
            QLabel {
                color: #E6F1FF;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        
        subtitle = QLabel("Windows Optimizer")
        subtitle.setStyleSheet("""
            QLabel {
                color: #9FB3C8;
                font-size: 12px;
                margin-left: 10px;
            }
        """)
        
        version = QLabel("v3.0")
        version.setStyleSheet("""
            QLabel {
                color: #1F4E79;
                font-size: 11px;
                font-weight: 600;
            }
        """)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(version)
        
        return header
    
    def _add_welcome_card(self):
        """Adiciona card de boas-vindas"""
        card = Card()
        layout = card.layout()
        
        welcome = QLabel("Bem-vindo ao rook")
        welcome.setStyleSheet("""
            QLabel {
                color: #E6F1FF;
                font-size: 20px;
                font-weight: 600;
            }
        """)
        
        description = QLabel(
            "Selecione as otimizações desejadas e clique no botão para aplicar. "
            "Todas as alterações são registradas e um ponto de restauração é criado "
            "antes das modificações para garantir segurança."
        )
        description.setWordWrap(True)
        description.setStyleSheet("""
            QLabel {
                color: #9FB3C8;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        
        layout.addWidget(welcome)
        layout.addWidget(description)
        
        self.content_layout.addWidget(card)
    
    def _add_optimization_card(self):
        """Adiciona card com checkboxes para selecionar otimizações"""
        card = Card("Selecione as Otimizações")
        layout = card.layout()
        
        # Descrição
        info = QLabel("Marque as opções que deseja aplicar:")
        info.setStyleSheet("""
            QLabel {
                color: #9FB3C8;
                font-size: 12px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(info)
        
        # Lista de funcionalidades com checkboxes
        features = [
            ("restore_point", "💾", "Ponto de Restauração", 
             "Cria um ponto de restauração do sistema antes das alterações", True),
            ("visual_effects", "🎨", "Efeitos Visuais", 
             "Ajusta para máximo desempenho (desativa animações e transparência)", True),
            ("hibernation", "💤", "Hibernação", 
             "Desativa para liberar espaço em disco (economiza GB no C:)", True),
            ("power_plan", "⚡", "Plano de Energia", 
             "Ativa o plano Ultimate Performance para máximo desempenho", True),
            ("tracking", "🛡️", "Processos de Rastreamento", 
             "Interrompe processos de telemetria do Windows", True),
            ("cleanup", "🧹", "Limpeza de Arquivos", 
             "Remove arquivos temporários e .tmp para liberar espaço", True),
            ("cpu_priority", "⚙️", "Prioridade CPU", 
             "Prioriza aplicações em execução sobre serviços de fundo", True),
        ]
        
        # Container para os checkboxes
        checkboxes_layout = QVBoxLayout()
        checkboxes_layout.setSpacing(12)
        
        for key, icon, name, desc, default in features:
            # Container para cada checkbox
            item_layout = QHBoxLayout()
            
            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(default)
            checkbox.setStyleSheet("""
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1F4E79;
                    background-color: transparent;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked {
                    background-color: #1ABC9C;
                    border: 2px solid #1ABC9C;
                    border-radius: 4px;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #3498DB;
                }
            """)
            
            # Ícone
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 18px;")
            icon_label.setFixedWidth(40)
            
            # Texto
            text_layout = QVBoxLayout()
            name_label = QLabel(name)
            name_label.setStyleSheet("color: #E6F1FF; font-weight: 500; font-size: 13px;")
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("color: #9FB3C8; font-size: 11px;")
            desc_label.setWordWrap(True)
            
            text_layout.addWidget(name_label)
            text_layout.addWidget(desc_label)
            
            # Adicionar ao layout
            item_layout.addWidget(checkbox)
            item_layout.addWidget(icon_label)
            item_layout.addLayout(text_layout)
            item_layout.addStretch()
            
            checkboxes_layout.addLayout(item_layout)
            
            # Armazenar referência
            self._checkboxes[key] = checkbox
        
        layout.addLayout(checkboxes_layout)
        
        # Botões de seleção rápida
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(10)
        
        btn_select_all = Button("Selecionar Todas", "secondary")
        btn_select_all.setFixedHeight(32)
        btn_select_all.clicked.connect(self._select_all)
        
        btn_deselect_all = Button("Desmarcar Todas", "secondary")
        btn_deselect_all.setFixedHeight(32)
        btn_deselect_all.clicked.connect(self._deselect_all)
        
        quick_layout.addWidget(btn_select_all)
        quick_layout.addWidget(btn_deselect_all)
        quick_layout.addStretch()
        
        layout.addLayout(quick_layout)
        
        self.content_layout.addWidget(card)
    
    def _add_action_card(self):
        """Adiciona card com botão de ação"""
        card = Card()
        layout = card.layout()
        
        # Botão principal
        self.btn_optimize = Button("▶ Executar Otimizações Selecionadas", "success")
        self.btn_optimize.clicked.connect(self._run_optimizations)
        layout.addWidget(self.btn_optimize)
        
        self.content_layout.addWidget(card)
    
    def _add_log_card(self):
        """Adiciona card de log"""
        card = Card("Log de Operações")
        layout = card.layout()
        
        self.log_area = LogArea()
        layout.addWidget(self.log_area)
        
        self.content_layout.addWidget(card)
    
    def _setup_animation(self):
        """Configura animação de entrada"""
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()
    
    def _load_recent_logs(self):
        """Carrega logs recentes"""
        for msg_type, message in self.logger.get_recent(20):
            self.log_area.add_message(msg_type, message)
    
    def _select_all(self):
        """Seleciona todas as checkboxes"""
        for checkbox in self._checkboxes.values():
            checkbox.setChecked(True)
        self.log_area.add_message("info", "Todas as otimizações selecionadas")
    
    def _deselect_all(self):
        """Desmarca todas as checkboxes"""
        for checkbox in self._checkboxes.values():
            checkbox.setChecked(False)
        self.log_area.add_message("info", "Todas as otimizações desmarcadas")
    
    def _get_selected_optimizations(self) -> dict:
        """Retorna dicionário com otimizações selecionadas"""
        return {
            key: checkbox.isChecked()
            for key, checkbox in self._checkboxes.items()
        }
    
    def _run_optimizations(self):
        """Executa as otimizações selecionadas"""
        if self._running:
            return
        
        selected = self._get_selected_optimizations()
        
        # Verificar se alguma opção foi selecionada
        if not any(selected.values()):
            self.log_area.add_message("warning", "Nenhuma otimização selecionada")
            return
        
        self._running = True
        self.btn_optimize.setEnabled(False)
        self.btn_optimize.setText("⏳ Executando...")
        
        # Log das opções selecionadas
        self.log_area.add_message("info", "=" * 50)
        self.log_area.add_message("info", "Otimizações selecionadas:")
        for key, enabled in selected.items():
            if enabled:
                names = {
                    "restore_point": "Ponto de Restauração",
                    "visual_effects": "Efeitos Visuais",
                    "hibernation": "Hibernação",
                    "power_plan": "Plano de Energia",
                    "tracking": "Processos de Rastreamento",
                    "cleanup": "Limpeza de Arquivos",
                    "cpu_priority": "Prioridade CPU"
                }
                self.log_area.add_message("info", f"  ✓ {names.get(key, key)}")
        self.log_area.add_message("info", "=" * 50)
        
        # Usar QTimer para não travar a UI
        QTimer.singleShot(100, lambda: self._execute_optimizations(selected))
    
    def _execute_optimizations(self, selected: dict):
        """Executa as otimizações selecionadas"""
        try:
            # Ponto de restauração (sempre primeiro se selecionado)
            if selected.get("restore_point"):
                self.log_area.add_message("info", "📝 Criando ponto de restauração...")
                if self.optimizer.create_restore_point():
                    self.log_area.add_message("success", "✅ Ponto de restauração criado")
                else:
                    self.log_area.add_message("warning", "⚠️ Falha ao criar ponto de restauração")
            
            # Efeitos visuais
            if selected.get("visual_effects"):
                self.log_area.add_message("info", "🎨 Ajustando efeitos visuais...")
                if self.optimizer.adjust_visual_effects():
                    self.log_area.add_message("success", "✅ Efeitos visuais ajustados")
                else:
                    self.log_area.add_message("warning", "⚠️ Falha ao ajustar efeitos visuais")
            
            # Hibernação
            if selected.get("hibernation"):
                self.log_area.add_message("info", "💤 Desativando hibernação...")
                if self.optimizer.disable_hibernation():
                    self.log_area.add_message("success", "✅ Hibernação desativada")
                else:
                    self.log_area.add_message("warning", "⚠️ Falha ao desativar hibernação")
            
            # Plano de energia
            if selected.get("power_plan"):
                self.log_area.add_message("info", "⚡ Ativando plano Ultimate Performance...")
                if self.optimizer.enable_ultimate_performance():
                    self.log_area.add_message("success", "✅ Plano Ultimate Performance ativado")
                else:
                    self.log_area.add_message("warning", "⚠️ Falha ao ativar plano de energia")
            
            # Processos de rastreamento
            if selected.get("tracking"):
                self.log_area.add_message("info", "🛡️ Interrompendo processos de rastreamento...")
                stopped = self.optimizer.stop_tracking_processes()
                self.log_area.add_message("success", f"✅ {stopped} processos interrompidos")
            
            # Limpeza de arquivos
            if selected.get("cleanup"):
                self.log_area.add_message("info", "🧹 Limpando arquivos temporários...")
                files, mb = self.optimizer.clean_temp_files()
                self.log_area.add_message("success", f"✅ {files} arquivos removidos ({mb} MB liberados)")
            
            # Prioridade CPU
            if selected.get("cpu_priority"):
                self.log_area.add_message("info", "⚙️ Ajustando prioridade da CPU...")
                if self.optimizer.prioritize_cpu():
                    self.log_area.add_message("success", "✅ Prioridade CPU ajustada")
                else:
                    self.log_area.add_message("warning", "⚠️ Falha ao ajustar prioridade CPU")
            
            # Mensagem final
            self.log_area.add_message("success", "=" * 50)
            self.log_area.add_message("success", "✅ Todas as otimizações selecionadas foram concluídas!")
            self.log_area.add_message("info", "📝 Reinicie o computador para aplicar todas as alterações")
            self.log_area.add_message("success", "=" * 50)
            
        except Exception as e:
            self.log_area.add_message("error", f"❌ Erro durante otimização: {e}")
        
        finally:
            self._running = False
            self.btn_optimize.setEnabled(True)
            self.btn_optimize.setText("▶ Executar Otimizações Selecionadas")
    
    def show_warning(self, message: str):
        """Exibe mensagem de aviso"""
        self.log_area.add_message("warning", f"⚠️ {message}")
    
    def show_success(self, message: str):
        """Exibe mensagem de sucesso"""
        self.log_area.add_message("success", f"✅ {message}")