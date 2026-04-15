import threading

from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollBar,
    QSizePolicy,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gugabot.ai.ancuta import AncutaAI
from gugabot.ai.buftea import BufteaAI
from gugabot.config import Config
from gugabot.logger import ActivityLogger
from gugabot.ui.settings_dialog import SettingsDialog
from gugabot.ui.styles import STYLESHEET
from gugabot.voice import VoiceListener

# Log level → HTML colour mapping
LOG_COLORS = {
    "info":     "#8b949e",
    "action":   "#39d353",
    "response": "#e6edf3",
    "error":    "#f85149",
    "wake":     "#00d26a",
    "system":   "#6a737d",
}


class MainWindow(QMainWindow):
    def __init__(
        self,
        config: Config,
        logger: ActivityLogger,
        ancuta: AncutaAI,
        buftea: BufteaAI,
        voice: VoiceListener,
    ):
        super().__init__()
        self.config = config
        self.logger = logger
        self.ancuta = ancuta
        self.buftea = buftea
        self.voice = voice

        self.setWindowTitle("GugaBot")
        self.setMinimumSize(900, 620)
        self.resize(1100, 700)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()
        self._connect_signals()
        self._post_init()

    # ------------------------------------------------------------------ UI build
    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        vbox.addWidget(self._header())

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("content")
        splitter.setHandleWidth(1)
        splitter.setStyleSheet("QSplitter::handle { background-color: #21262d; }")
        splitter.addWidget(self._left_panel())
        splitter.addWidget(self._right_panel())
        splitter.setSizes([280, 820])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        vbox.addWidget(splitter, 1)

        vbox.addWidget(self._bottom_bar())

    # ---- Header -------------------------------------------------------
    def _header(self) -> QFrame:
        hdr = QFrame()
        hdr.setObjectName("header")
        hdr.setFixedHeight(56)
        lay = QHBoxLayout(hdr)
        lay.setContentsMargins(20, 0, 20, 0)
        lay.setSpacing(10)

        title = QLabel("GugaBot")
        title.setObjectName("app_title")
        lay.addWidget(title)

        lay.addStretch()

        self._dot = QLabel("●")
        self._dot.setObjectName("status_idle")
        lay.addWidget(self._dot)

        self._status_lbl = QLabel("Idle")
        self._status_lbl.setObjectName("status_text")
        lay.addWidget(self._status_lbl)

        lay.addSpacing(12)

        settings_btn = QPushButton("⚙")
        settings_btn.setObjectName("icon_btn")
        settings_btn.setFixedSize(36, 36)
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(self._open_settings)
        lay.addWidget(settings_btn)

        return hdr

    # ---- Left panel ---------------------------------------------------
    def _left_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("panel")
        panel.setMinimumWidth(240)
        panel.setMaximumWidth(320)
        lay = QVBoxLayout(panel)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        # ── Ancuța section ──────────────────
        ancuta_title = QLabel("Ancuța AI")
        ancuta_title.setObjectName("section_title")
        lay.addWidget(ancuta_title)

        ancuta_desc = QLabel("Quick tasks · Gemini 1.5 Flash\nWake word: \"GugaBot\"")
        ancuta_desc.setObjectName("section_desc")
        ancuta_desc.setWordWrap(True)
        lay.addWidget(ancuta_desc)

        self._ancuta_status = QLabel("● Listening" if self.voice.available else "● Ready")
        self._ancuta_status.setObjectName("ai_status_active")
        lay.addWidget(self._ancuta_status)

        # Manual text input for Ancuța
        ancuta_row = QHBoxLayout()
        ancuta_row.setSpacing(6)
        self._ancuta_input = QLineEdit()
        self._ancuta_input.setObjectName("ancuta_input")
        self._ancuta_input.setPlaceholderText("Quick command…")
        self._ancuta_input.returnPressed.connect(self._send_ancuta)
        ancuta_row.addWidget(self._ancuta_input)

        send_ancuta = QPushButton("→")
        send_ancuta.setObjectName("send_btn")
        send_ancuta.setFixedWidth(32)
        send_ancuta.setToolTip("Send to Ancuța AI")
        send_ancuta.clicked.connect(self._send_ancuta)
        ancuta_row.addWidget(send_ancuta)
        lay.addLayout(ancuta_row)

        lay.addWidget(self._divider())

        # ── Buftea section ──────────────────
        buftea_title = QLabel("Buftea AI")
        buftea_title.setObjectName("section_title")
        lay.addWidget(buftea_title)

        buftea_desc = QLabel("Full PC control · Gemini 2.5 Pro\nSees your screen")
        buftea_desc.setObjectName("section_desc")
        buftea_desc.setWordWrap(True)
        lay.addWidget(buftea_desc)

        self._buftea_status = QLabel("● Idle")
        self._buftea_status.setObjectName("ai_status_idle")
        lay.addWidget(self._buftea_status)

        self._buftea_input = QTextEdit()
        self._buftea_input.setObjectName("prompt_input")
        self._buftea_input.setPlaceholderText("Describe a task for Buftea AI…\ne.g. Open Chrome and search for cats")
        self._buftea_input.setFixedHeight(90)
        lay.addWidget(self._buftea_input)

        self._start_btn = QPushButton("▶  Start Buftea AI")
        self._start_btn.setObjectName("primary_btn")
        self._start_btn.clicked.connect(self._start_buftea)
        lay.addWidget(self._start_btn)

        self._stop_btn = QPushButton("■  Stop")
        self._stop_btn.setObjectName("stop_btn")
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._stop_all)
        self._stop_btn.setToolTip("Stop all AI activity  (or say \"Guga stop\")")
        lay.addWidget(self._stop_btn)

        lay.addStretch()

        # Voice indicator
        if self.voice.available:
            self._voice_lbl = QLabel("🎤  Voice active")
        else:
            self._voice_lbl = QLabel("🎤  Voice unavailable\n    (install pyaudio)")
        self._voice_lbl.setObjectName("voice_indicator")
        self._voice_lbl.setWordWrap(True)
        lay.addWidget(self._voice_lbl)

        return panel

    # ---- Right panel (log) -------------------------------------------
    def _right_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("panel")
        lay = QVBoxLayout(panel)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(8)

        # Header row
        hdr = QHBoxLayout()
        log_lbl = QLabel("Activity Log")
        log_lbl.setObjectName("section_title")
        hdr.addWidget(log_lbl)
        hdr.addStretch()

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("text_btn")
        clear_btn.clicked.connect(self._clear_log)
        hdr.addWidget(clear_btn)
        lay.addLayout(hdr)

        self._log = QTextEdit()
        self._log.setObjectName("log_display")
        self._log.setReadOnly(True)
        lay.addWidget(self._log, 1)

        return panel

    # ---- Bottom bar --------------------------------------------------
    def _bottom_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("bottom_bar")
        bar.setFixedHeight(36)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(16, 0, 16, 0)
        lay.setSpacing(0)

        self._model_lbl = QLabel(self._model_text())
        self._model_lbl.setObjectName("status_bar_text")
        lay.addWidget(self._model_lbl)

        lay.addStretch()

        self._token_lbl = QLabel(self._token_text())
        self._token_lbl.setObjectName("status_bar_text")
        lay.addWidget(self._token_lbl)

        return bar

    # ---- Misc helpers ------------------------------------------------
    def _divider(self) -> QFrame:
        d = QFrame()
        d.setObjectName("divider")
        d.setFrameShape(QFrame.Shape.HLine)
        d.setFixedHeight(1)
        return d

    def _model_text(self) -> str:
        a = self.config.get("ancuta_model", "—")
        b = self.config.get("buftea_model", "—")
        return f"Ancuța: {a}   |   Buftea: {b}"

    def _token_text(self) -> str:
        usage = self.config.get("usage", {})
        a = usage.get("ancuta", {})
        b = usage.get("buftea", {})
        ta = a.get("tokens_in", 0) + a.get("tokens_out", 0)
        tb = b.get("tokens_in", 0) + b.get("tokens_out", 0)
        return f"Ancuța: {ta:,} tokens   |   Buftea: {tb:,} tokens"

    # ------------------------------------------------------------------ Signals
    def _connect_signals(self):
        self.logger.log_added.connect(self._on_log)
        self.buftea.status_changed.connect(self._on_buftea_status)

        if self.voice.available:
            self.voice.wake_word_detected.connect(self._on_wake_word)
            self.voice.command_detected.connect(self._on_voice_command)
            self.voice.status_changed.connect(self._on_voice_status)

    # ------------------------------------------------------------------ Slots
    @pyqtSlot(str, str, str)
    def _on_log(self, ts: str, level: str, msg: str):
        color = LOG_COLORS.get(level, "#8b949e")
        ts_html = f'<span style="color:#6a737d">[{ts}]</span>'
        msg_html = f'<span style="color:{color}">{_escape_html(msg)}</span>'
        self._log.append(f"{ts_html} {msg_html}")
        # Auto-scroll
        sb = self._log.verticalScrollBar()
        sb.setValue(sb.maximum())
        # Refresh token counter
        self._token_lbl.setText(self._token_text())

    @pyqtSlot(str)
    def _on_buftea_status(self, state: str):
        if state == "running":
            self._buftea_status.setText("● Running")
            self._buftea_status.setObjectName("ai_status_active")
            self._buftea_status.setStyleSheet("color: #39d353; font-size: 12px; font-weight: 500;")
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)
            self._set_status("Buftea Active", "active")
        else:
            self._buftea_status.setText("● Idle")
            self._buftea_status.setObjectName("ai_status_idle")
            self._buftea_status.setStyleSheet("color: #6a737d; font-size: 12px; font-weight: 500;")
            self._start_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)
            self._set_status("Idle", "idle")

    @pyqtSlot(str)
    def _on_wake_word(self, word: str):
        if word == "guga_stop":
            self._stop_all()
            self.logger.log("Stopped by voice command", "system")
        elif word == "gugabot":
            self.logger.log("Wake word detected — listening for command…", "wake")
            self._set_status("Listening…", "active")

    @pyqtSlot(str)
    def _on_voice_command(self, text: str):
        self.logger.log(f'Voice: "{text}"', "wake")
        self._set_status("Processing", "active")
        self.ancuta.process_request(text)

    @pyqtSlot(str)
    def _on_voice_status(self, msg: str):
        if msg:
            self._set_status(msg, "active")
        else:
            self._set_status("Idle", "idle")

    # ------------------------------------------------------------------ Actions
    def _send_ancuta(self):
        text = self._ancuta_input.text().strip()
        if not text:
            return
        self._ancuta_input.clear()
        self._set_status("Processing", "active")
        self.ancuta.process_request(text)

    def _start_buftea(self):
        prompt = self._buftea_input.toPlainText().strip()
        if not prompt:
            self.logger.log("Enter a task for Buftea AI first.", "error")
            return
        # Tell Buftea about this window so it avoids clicking on us
        pos = self.pos()
        sz = self.size()
        self.buftea.set_window_rect(pos.x(), pos.y(), sz.width(), sz.height())
        self.buftea.start_task(prompt)

    def _stop_all(self):
        self.ancuta.stop()
        self.buftea.stop()
        self._stop_btn.setEnabled(False)
        self._start_btn.setEnabled(True)
        self._buftea_status.setText("● Idle")
        self._buftea_status.setStyleSheet("color: #6a737d; font-size: 12px; font-weight: 500;")
        self._set_status("Idle", "idle")
        self.logger.log("All AI stopped.", "system")

    def _open_settings(self):
        dlg = SettingsDialog(self.config, parent=self)
        if dlg.exec():
            self.ancuta.update_client()
            self.buftea.update_client()
            self._model_lbl.setText(self._model_text())
            self._token_lbl.setText(self._token_text())

    def _clear_log(self):
        self._log.clear()
        self.logger.clear()

    # ------------------------------------------------------------------ Helpers
    def _set_status(self, text: str, state: str):
        self._status_lbl.setText(text)
        colours = {"idle": "#6a737d", "active": "#39d353", "error": "#f85149"}
        c = colours.get(state, "#6a737d")
        self._dot.setStyleSheet(f"color: {c}; font-size: 18px;")

    def _post_init(self):
        self.logger.log("GugaBot started.", "system")
        if not self.config.get("api_key"):
            self.logger.log("No API key set — open ⚙ Settings to add your OpenRouter key.", "error")
        if self.voice.available:
            self.voice.start()
            self.logger.log("Voice listener active — say \"GugaBot\" to wake Ancuța AI.", "system")
        else:
            self.logger.log("Voice unavailable — install pyaudio for voice activation.", "system")


# ── helpers ──────────────────────────────────────────────────────────────────
def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )
