# ui/widgets.py
"""
Componentes reutilizáveis da interface - rook v3.0
Design: industrial/utilitarian dark com acentos ciano
"""
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QFont


# ── Paleta central ──────────────────────────────────────────────────────────
BG_BASE    = "#080F17"
BG_SURFACE = "#0D1B2A"
BG_CARD    = "#0F2035"
BORDER     = "#1A3A5C"
ACCENT     = "#00C6A7"      # ciano-menta
ACCENT2    = "#0F8CFF"      # azul elétrico
TEXT_PRI   = "#E8F4FF"
TEXT_SEC   = "#6B8FAB"
TEXT_DIM   = "#3E5A72"
DANGER     = "#E74C3C"
WARNING    = "#F0A500"


def _shadow(blur: int = 18, color: str = "#000000", alpha: int = 80) -> QGraphicsDropShadowEffect:
    """Helper que cria sombra drop consistente."""
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setColor(QColor(color + f"{alpha:02x}"))
    fx.setOffset(0, 4)
    return fx


class Card(QFrame):
    """Card com borda superior colorida e sombra profunda."""

    def __init__(self, title: str = "", accent_color: str = ACCENT, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet(f"""
            #card {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER};
                border-top: 2px solid {accent_color};
                border-radius: 10px;
            }}
        """)
        self.setGraphicsEffect(_shadow(22, "#000000", 90))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        if title:
            header_row = QHBoxLayout()
            header_row.setSpacing(10)

            # Barra lateral decorativa
            bar = QFrame()
            bar.setFixedSize(3, 18)
            bar.setStyleSheet(f"background: {accent_color}; border-radius: 2px;")

            title_label = QLabel(title.upper())
            title_label.setStyleSheet(f"""
                QLabel {{
                    color: {TEXT_PRI};
                    font-size: 11px;
                    font-weight: 700;
                    letter-spacing: 2px;
                    font-family: 'Consolas', 'Courier New', monospace;
                }}
            """)

            header_row.addWidget(bar)
            header_row.addWidget(title_label)
            header_row.addStretch()
            layout.addLayout(header_row)

            # Separador fino
            sep = QFrame()
            sep.setFrameShape(QFrame.HLine)
            sep.setFixedHeight(1)
            sep.setStyleSheet(f"background: {BORDER}; border: none;")
            layout.addWidget(sep)


class Button(QPushButton):
    """Botão com variantes visuais e efeito de hover suave."""

    VARIANTS = {
        "primary":   {"bg": "#0F3A6E", "hover": "#0F4F9A", "text": TEXT_PRI,  "border": ACCENT2},
        "success":   {"bg": "#0B3D35", "hover": "#0E5548", "text": ACCENT,    "border": ACCENT},
        "danger":    {"bg": "#4A1C1C", "hover": "#6B2020", "text": "#FF6B6B", "border": DANGER},
        "secondary": {"bg": "#0D1B2A", "hover": "#132438", "text": TEXT_SEC,  "border": BORDER},
        "ghost":     {"bg": "transparent", "hover": "#0D1B2A", "text": TEXT_SEC, "border": "transparent"},
    }

    def __init__(self, text: str, variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)

        c = self.VARIANTS.get(variant, self.VARIANTS["primary"])

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['bg']};
                color: {c['text']};
                border: 1px solid {c['border']};
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                font-family: 'Consolas', 'Courier New', monospace;
                letter-spacing: 0.5px;
                padding: 0 18px;
            }}
            QPushButton:hover {{
                background-color: {c['hover']};
                border-color: {ACCENT2};
            }}
            QPushButton:pressed {{
                background-color: {c['bg']};
                padding-top: 2px;
            }}
            QPushButton:disabled {{
                background-color: {BG_SURFACE};
                color: {TEXT_DIM};
                border-color: {TEXT_DIM};
            }}
        """)


class StatusBadge(QLabel):
    """Badge de status pequeno e inline."""

    STYLES = {
        "online":   (ACCENT,   "#0B3D35"),
        "warning":  (WARNING,  "#3D2B00"),
        "error":    (DANGER,   "#3D1010"),
        "neutral":  (TEXT_SEC, BG_SURFACE),
    }

    def __init__(self, text: str, status: str = "neutral", parent=None):
        super().__init__(f"  {text}  ", parent)
        fg, bg = self.STYLES.get(status, self.STYLES["neutral"])
        self.setStyleSheet(f"""
            QLabel {{
                color: {fg};
                background: {bg};
                border: 1px solid {fg};
                border-radius: 10px;
                font-size: 10px;
                font-weight: 700;
                font-family: 'Consolas', 'Courier New', monospace;
                letter-spacing: 1px;
                padding: 2px 0;
            }}
        """)
        self.setFixedHeight(20)


class LogArea(QFrame):
    """Área de log estilo terminal com linhas coloridas e scroll."""

    MAX_LINES = 120

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("logArea")
        self._lines: list[str] = []

        self.setStyleSheet(f"""
            #logArea {{
                background-color: {BG_BASE};
                border: 1px solid {BORDER};
                border-radius: 8px;
            }}
        """)
        self.setMinimumHeight(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(0)

        # Cabeçalho do terminal
        header = QHBoxLayout()
        for dot_color in ("#E74C3C", "#F0A500", "#1ABC9C"):
            dot = QFrame()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"""
                background: {dot_color};
                border-radius: 5px;
            """)
            header.addWidget(dot)
        header.addSpacing(10)
        cap = QLabel("OUTPUT")
        cap.setStyleSheet(f"""
            color: {TEXT_DIM};
            font-size: 10px;
            font-weight: 700;
            font-family: 'Consolas', 'Courier New', monospace;
            letter-spacing: 2px;
        """)
        header.addWidget(cap)
        header.addStretch()
        layout.addLayout(header)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background: {BORDER}; border: none; margin: 6px 0;")
        layout.addWidget(sep)

        # Área de texto
        self._log_label = QLabel()
        self._log_label.setWordWrap(True)
        self._log_label.setTextFormat(Qt.RichText)
        self._log_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self._log_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_SEC};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                line-height: 1.6;
                background: transparent;
            }}
        """)
        layout.addWidget(self._log_label)

    # Mapeamento de tipos → (cor, prefixo)
    _TYPE_META = {
        "info":    (ACCENT2,  "INFO "),
        "success": (ACCENT,   " OK  "),
        "warning": (WARNING,  "WARN "),
        "error":   (DANGER,   " ERR "),
    }

    def add_message(self, msg_type: str, message: str):
        """Adiciona uma linha ao log."""
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")

        color, prefix = self._TYPE_META.get(msg_type, (TEXT_SEC, " LOG "))

        line = (
            f'<span style="color:{TEXT_DIM};">[{ts}]</span> '
            f'<span style="color:{color};font-weight:700;">{prefix}</span> '
            f'<span style="color:{TEXT_PRI};">{message}</span>'
        )

        self._lines.insert(0, line)
        if len(self._lines) > self.MAX_LINES:
            self._lines = self._lines[:self.MAX_LINES]

        self._log_label.setText("<br>".join(self._lines))

    def clear(self):
        """Limpa o log."""
        self._lines.clear()
        self._log_label.setText("")