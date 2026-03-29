# ui/main_window.py
"""
Janela principal do rook - Windows Optimizer
As otimizações rodam em QThread separada para nunca travar a UI.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor
from ui.widgets import (
    Card, Button, LogArea, StatusBadge,
    ACCENT, ACCENT2, BG_BASE, BG_SURFACE, BG_CARD,
    BORDER, TEXT_PRI, TEXT_SEC, TEXT_DIM, DANGER, WARNING
)

_ACCENT   = ACCENT
_ACCENT2  = ACCENT2
_BG_BASE  = BG_BASE
_TEXT_PRI = TEXT_PRI
_TEXT_SEC = TEXT_SEC
_BORDER   = BORDER


# ─────────────────────────────────────────────────────────────────────────────
# Worker — roda as otimizações em thread separada
# ─────────────────────────────────────────────────────────────────────────────
class OptimizerWorker(QThread):
    """Thread que executa as otimizações sem bloquear a UI."""

    log_signal    = Signal(str, str)
    status_signal = Signal(str)
    done_signal   = Signal()

    def __init__(self, optimizer, selected: dict):
        super().__init__()
        self.optimizer = optimizer
        self.selected  = selected

    def _log(self, tipo: str, msg: str):
        self.log_signal.emit(tipo, msg)

    def run(self):
        sel = self.selected
        try:
            if sel.get("restore_point"):
                self._log("info", "Criando ponto de restauracao...")
                ok = self.optimizer.create_restore_point()
                self._log(
                    "success" if ok else "warning",
                    "Ponto de restauracao criado" if ok
                    else "Falha ao criar ponto de restauracao"
                )

            if sel.get("visual_effects"):
                self._log("info", "Ajustando efeitos visuais...")
                ok = self.optimizer.adjust_visual_effects()
                self._log(
                    "success" if ok else "warning",
                    "Efeitos visuais ajustados" if ok
                    else "Falha ao ajustar efeitos visuais"
                )

            if sel.get("hibernation"):
                self._log("info", "Desativando hibernacao...")
                ok = self.optimizer.disable_hibernation()
                self._log(
                    "success" if ok else "warning",
                    "Hibernacao desativada" if ok
                    else "Falha ao desativar hibernacao (requer admin)"
                )

            if sel.get("power_plan"):
                self._log("info", "Ativando plano de energia...")
                ok = self.optimizer.enable_ultimate_performance()
                self._log(
                    "success" if ok else "warning",
                    "Plano de energia ativado" if ok
                    else "Falha ao ativar plano de energia"
                )

            if sel.get("tracking"):
                self._log("info", "Interrompendo telemetria e rastreamento...")
                n = self.optimizer.stop_tracking_processes()
                self._log("success", f"{n} processos/servicos de rastreamento interrompidos")

            if sel.get("cleanup"):
                self._log("info", "Limpando arquivos temporarios...")
                files, mb = self.optimizer.clean_temp_files()
                self._log("success", f"{files} itens removidos - {mb} MB liberados")

            if sel.get("cpu_priority"):
                self._log("info", "Ajustando prioridade da CPU...")
                ok = self.optimizer.prioritize_cpu()
                self._log(
                    "success" if ok else "warning",
                    "Prioridade de CPU ajustada" if ok
                    else "Falha ao ajustar prioridade (requer admin)"
                )

            self._log("info",    "-" * 48)
            self._log("success", "Todas as otimizacoes foram concluidas!")
            self._log("info",    "Reinicie o computador para aplicar todas as alteracoes.")
            self._log("info",    "-" * 48)
            self.status_signal.emit("Otimizacoes concluidas. Reinicie o sistema.")

        except Exception as exc:
            self._log("error", f"Erro inesperado durante otimizacao: {exc}")
            self.status_signal.emit(f"Erro: {exc}")

        finally:
            self.done_signal.emit()


# ─────────────────────────────────────────────────────────────────────────────
# Janela principal
# ─────────────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):

    def __init__(self, logger, optimizer):
        super().__init__()
        self.logger    = logger
        self.optimizer = optimizer
        self._worker: OptimizerWorker | None = None
        self._checkboxes: dict[str, QCheckBox] = {}

        self.setWindowTitle("rook - Windows Optimizer")
        self.setMinimumSize(860, 640)
        self.resize(960, 740)
        self.setStyleSheet(self._global_style())

        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_header())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )

        content_widget = QWidget()
        content_widget.setStyleSheet(f"background: {_BG_BASE};")
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(32, 28, 32, 32)
        self.content_layout.setSpacing(20)

        self._add_status_bar()
        self._add_optimization_card()
        self._add_action_card()
        self._add_log_card()
        self.content_layout.addStretch()

        scroll.setWidget(content_widget)
        root_layout.addWidget(scroll)
        root_layout.addWidget(self._build_footer())

        self._setup_fade_in()
        self._load_recent_logs()

    # ── Estilos ───────────────────────────────────────────────────────────────
    def _global_style(self) -> str:
        return f"""
            QMainWindow, QWidget {{
                background-color: {_BG_BASE};
                color: {_TEXT_PRI};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {BG_SURFACE};
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {_BORDER};
                border-radius: 4px;
                min-height: 24px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {_ACCENT}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
            QScrollBar:horizontal {{
                border: none;
                background: {BG_SURFACE};
                height: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:horizontal {{
                background: {_BORDER};
                border-radius: 4px;
                min-width: 24px;
            }}
            QScrollBar::handle:horizontal:hover {{ background: {_ACCENT}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
            QToolTip {{
                background: {BG_CARD};
                color: {_TEXT_PRI};
                border: 1px solid {_BORDER};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            }}
        """

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_SURFACE};
                border-bottom: 1px solid {_BORDER};
            }}
        """)
        row = QHBoxLayout(header)
        row.setContentsMargins(28, 0, 28, 0)
        row.setSpacing(0)

        logo = QLabel("rook")
        logo.setStyleSheet(f"""
            QLabel {{
                color: {_ACCENT};
                font-size: 22px;
                font-weight: 900;
                font-family: 'Consolas', 'Courier New', monospace;
                letter-spacing: 3px;
            }}
        """)
        slash    = QLabel("  /  ")
        slash.setStyleSheet(f"color: {TEXT_DIM}; font-size: 16px;")
        subtitle = QLabel("windows optimizer")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {_TEXT_SEC};
                font-size: 12px;
                font-family: 'Consolas', 'Courier New', monospace;
                letter-spacing: 1px;
            }}
        """)
        row.addWidget(logo)
        row.addWidget(slash)
        row.addWidget(subtitle)
        row.addStretch()

        ver = QLabel("v3.0")
        ver.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DIM};
                font-size: 10px;
                font-weight: 700;
                font-family: 'Consolas', 'Courier New', monospace;
                letter-spacing: 2px;
                padding: 3px 8px;
                border: 1px solid {_BORDER};
                border-radius: 4px;
            }}
        """)
        row.addWidget(ver)
        return header

    # ── Footer ────────────────────────────────────────────────────────────────
    def _build_footer(self) -> QFrame:
        footer = QFrame()
        footer.setFixedHeight(28)
        footer.setStyleSheet(f"""
            QFrame {{
                background: {BG_SURFACE};
                border-top: 1px solid {_BORDER};
            }}
        """)
        row = QHBoxLayout(footer)
        row.setContentsMargins(28, 0, 28, 0)

        self._status_label = QLabel("Pronto.")
        self._status_label.setStyleSheet(f"""
            color: {_TEXT_SEC};
            font-size: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        """)
        row.addWidget(self._status_label)
        row.addStretch()

        hint = QLabel("Requer privilegios de administrador")
        hint.setStyleSheet(f"""
            color: {TEXT_DIM};
            font-size: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        """)
        row.addWidget(hint)
        return footer

    def _set_status(self, msg: str):
        self._status_label.setText(msg)

    # ── Info bar ──────────────────────────────────────────────────────────────
    def _add_status_bar(self):
        bar = QFrame()
        bar.setStyleSheet(f"""
            QFrame {{
                background: {BG_SURFACE};
                border: 1px solid {_BORDER};
                border-radius: 8px;
            }}
        """)
        row = QHBoxLayout(bar)
        row.setContentsMargins(18, 10, 18, 10)
        row.setSpacing(14)

        icon = QLabel("i")
        icon.setStyleSheet(f"""
            color: {_ACCENT};
            font-size: 14px;
            font-weight: 900;
            font-family: 'Consolas', monospace;
        """)
        row.addWidget(icon)

        msg = QLabel(
            "Selecione as otimizacoes desejadas e clique em <b>Executar</b>. "
            "Um ponto de restauracao e criado antes de qualquer modificacao."
        )
        msg.setStyleSheet(f"color: {_TEXT_SEC}; font-size: 12px;")
        msg.setWordWrap(True)
        row.addWidget(msg, 1)

        self.content_layout.addWidget(bar)

    # ── Card de otimizacoes ───────────────────────────────────────────────────
    def _add_optimization_card(self):
        card = Card("Otimizacoes Disponiveis", accent_color=_ACCENT)
        layout = card.layout()

        features = [
            ("restore_point",  ">>", "Ponto de Restauracao",
             "Cria snapshot do sistema antes das alteracoes", True),
            ("visual_effects", ">>", "Efeitos Visuais",
             "Maximo desempenho - desativa animacoes e transparencia", True),
            ("hibernation",    ">>", "Hibernacao",
             "Desativa e libera espaco em disco (hiberfil.sys)", True),
            ("power_plan",     ">>", "Plano de Energia",
             "Ativa o plano Ultimate Performance", True),
            ("tracking",       ">>", "Telemetria e Rastreamento",
             "Desativa processos e servicos de telemetria do Windows", True),
            ("cleanup",        ">>", "Limpeza de Arquivos",
             "Remove arquivos .tmp e temporarios do sistema", True),
            ("cpu_priority",   ">>", "Prioridade da CPU",
             "Prioriza apps em execucao sobre servicos de fundo", True),
        ]

        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid_layout = QVBoxLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(6)

        for key, icon_ch, name, desc, default in features:
            row_frame = QFrame()
            row_frame.setObjectName("optRow")
            row_frame.setStyleSheet(f"""
                #optRow {{
                    background: {BG_SURFACE};
                    border: 1px solid {_BORDER};
                    border-radius: 7px;
                }}
                #optRow:hover {{
                    border-color: {_ACCENT2};
                    background: #0e2035;
                }}
            """)

            row = QHBoxLayout(row_frame)
            row.setContentsMargins(14, 10, 14, 10)
            row.setSpacing(12)

            cb = QCheckBox()
            cb.setChecked(default)
            cb.setCursor(Qt.PointingHandCursor)
            cb.setStyleSheet(f"""
                QCheckBox::indicator {{
                    width: 17px;
                    height: 17px;
                    border-radius: 4px;
                    border: 2px solid {_BORDER};
                    background: transparent;
                }}
                QCheckBox::indicator:hover {{ border-color: {_ACCENT}; }}
                QCheckBox::indicator:checked {{
                    background-color: {_ACCENT};
                    border-color: {_ACCENT};
                }}
                QCheckBox::indicator:checked:hover {{ background-color: #00dbb8; }}
            """)
            self._checkboxes[key] = cb

            ic = QLabel(icon_ch)
            ic.setFixedWidth(28)
            ic.setStyleSheet(f"font-size: 11px; color: {_ACCENT}; background: transparent; font-family: monospace; font-weight: bold;")

            txt = QVBoxLayout()
            txt.setSpacing(1)
            n_lbl = QLabel(name)
            n_lbl.setStyleSheet(f"color: {_TEXT_PRI}; font-weight: 600; font-size: 13px; background: transparent;")
            d_lbl = QLabel(desc)
            d_lbl.setStyleSheet(f"color: {_TEXT_SEC}; font-size: 11px; background: transparent;")
            txt.addWidget(n_lbl)
            txt.addWidget(d_lbl)

            row.addWidget(cb)
            row.addWidget(ic)
            row.addLayout(txt, 1)

            row_frame.mousePressEvent = lambda _e, c=cb: c.setChecked(not c.isChecked())
            grid_layout.addWidget(row_frame)

        layout.addWidget(grid_widget)

        quick = QHBoxLayout()
        quick.setSpacing(8)
        btn_all  = Button("Selecionar Todas", "ghost")
        btn_none = Button("Desmarcar Todas",  "ghost")
        btn_all.setFixedHeight(32)
        btn_none.setFixedHeight(32)
        btn_all.clicked.connect(self._select_all)
        btn_none.clicked.connect(self._deselect_all)
        quick.addWidget(btn_all)
        quick.addWidget(btn_none)
        quick.addStretch()
        layout.addLayout(quick)

        self.content_layout.addWidget(card)

    # ── Card de acao ──────────────────────────────────────────────────────────
    def _add_action_card(self):
        card = Card(accent_color=_ACCENT2)
        layout = card.layout()

        row = QHBoxLayout()
        row.setSpacing(12)

        self.btn_optimize = Button(">>  Executar Otimizacoes Selecionadas", "success")
        self.btn_optimize.setFixedHeight(46)
        self.btn_optimize.setStyleSheet(
            self.btn_optimize.styleSheet()
            + "QPushButton { font-size: 14px; letter-spacing: 1px; }"
        )
        self.btn_optimize.clicked.connect(self._run_optimizations)

        btn_clear = Button("Limpar Log", "ghost")
        btn_clear.setFixedHeight(46)
        btn_clear.setFixedWidth(110)
        btn_clear.clicked.connect(self._clear_log)

        row.addWidget(self.btn_optimize, 1)
        row.addWidget(btn_clear)
        layout.addLayout(row)
        self.content_layout.addWidget(card)

    # ── Card de log ───────────────────────────────────────────────────────────
    def _add_log_card(self):
        card = Card("Log de Operacoes", accent_color=TEXT_DIM)
        layout = card.layout()
        self.log_area = LogArea()
        self.log_area.setMinimumHeight(200)
        layout.addWidget(self.log_area)
        self.content_layout.addWidget(card)

    # ── Fade-in ───────────────────────────────────────────────────────────────
    def _setup_fade_in(self):
        self.setWindowOpacity(0.0)
        anim = QPropertyAnimation(self, b"windowOpacity", self)
        anim.setDuration(350)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self._fade_anim = anim

    # ── Logica ────────────────────────────────────────────────────────────────
    def _load_recent_logs(self):
        for msg_type, message in self.logger.get_recent(20):
            self.log_area.add_message(msg_type, message)

    def _select_all(self):
        for cb in self._checkboxes.values():
            cb.setChecked(True)
        self.log_area.add_message("info", "Todas as otimizacoes selecionadas")

    def _deselect_all(self):
        for cb in self._checkboxes.values():
            cb.setChecked(False)
        self.log_area.add_message("info", "Todas as otimizacoes desmarcadas")

    def _clear_log(self):
        self.log_area.clear()
        self._set_status("Log limpo.")

    def _get_selected(self) -> dict[str, bool]:
        return {k: cb.isChecked() for k, cb in self._checkboxes.items()}

    def _run_optimizations(self):
        """Inicia o worker em QThread — UI permanece responsiva."""
        if self._worker and self._worker.isRunning():
            return

        selected = self._get_selected()
        if not any(selected.values()):
            self.log_area.add_message("warning", "Nenhuma otimizacao selecionada")
            return

        names_map = {
            "restore_point":  "Ponto de Restauracao",
            "visual_effects": "Efeitos Visuais",
            "hibernation":    "Hibernacao",
            "power_plan":     "Plano de Energia",
            "tracking":       "Telemetria e Rastreamento",
            "cleanup":        "Limpeza de Arquivos",
            "cpu_priority":   "Prioridade da CPU",
        }
        self.log_area.add_message("info", "-" * 48)
        self.log_area.add_message("info", "Iniciando otimizacoes selecionadas:")
        for key, enabled in selected.items():
            if enabled:
                self.log_area.add_message("info", f"  > {names_map.get(key, key)}")
        self.log_area.add_message("info", "-" * 48)

        self.btn_optimize.setEnabled(False)
        self.btn_optimize.setText("[ aguarde ] Executando...")
        self._set_status("Executando otimizacoes em segundo plano...")

        self._worker = OptimizerWorker(self.optimizer, selected)
        self._worker.log_signal.connect(self.log_area.add_message)
        self._worker.status_signal.connect(self._set_status)
        self._worker.done_signal.connect(self._on_done)
        self._worker.start()

    def _on_done(self):
        self.btn_optimize.setEnabled(True)
        self.btn_optimize.setText(">>  Executar Otimizacoes Selecionadas")

    # ── API publica ───────────────────────────────────────────────────────────
    def show_warning(self, message: str):
        self.log_area.add_message("warning", message)
        self._set_status(f"Aviso: {message}")

    def show_success(self, message: str):
        self.log_area.add_message("success", message)
        self._set_status(message)