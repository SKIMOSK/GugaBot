import threading

from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gugabot.ai.ancuta import AncutaAI
from gugabot.ai.buftea import BufteaAI
from gugabot.config import Config
from gugabot.logger import ActivityLogger
from gugabot.sounds import SoundManager
from gugabot.ui.settings_dialog import SettingsDialog
from gugabot.ui.styles import STYLESHEET
from gugabot.voice import VoiceListener

# Log-level → HTML colour
LOG_COLORS = {
    "info":     "#6aaa88",
    "action":   "#00ff88",
    "response": "#c5e8d5",
    "error":    "#ff3355",
    "wake":     "#00e5cc",
    "system":   "#3a6050",
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
        self.sounds = SoundManager()
        self.sounds.enabled = config.get("sounds_enabled", True)

        self.setWindowTitle("GugaBot")
        self.setMinimumSize(920, 640)
        self.resize(1140, 720)
        self.setStyleSheet(STYLESHEET)

        # Confirm banner widget (created lazily, inserted into log panel)
        self._confirm_banner: QFrame | None = None
        self._confirm_timer: QTimer | None = None
        self._confirm_countdown = 0

        self._build_ui()
        self._connect_signals()
        self._post_init()

    # ═══════════════════════════════════════════════ UI build
    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        vbox.addWidget(self._header())

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("content")
        splitter.setHandleWidth(3)
        splitter.addWidget(self._left_panel())
        splitter.addWidget(self._right_panel())
        splitter.setSizes([290, 850])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        vbox.addWidget(splitter, 1)

        vbox.addWidget(self._bottom_bar())

    # ── Header ────────────────────────────────────────────────────────
    def _header(self) -> QFrame:
        hdr = QFrame()
        hdr.setObjectName("header")
        hdr.setFixedHeight(58)
        lay = QHBoxLayout(hdr)
        lay.setContentsMargins(22, 0, 22, 0)
        lay.setSpacing(12)

        title = QLabel("GugaBot")
        title.setObjectName("app_title")
        lay.addWidget(title)

        version = QLabel("v2.0")
        version.setObjectName("status_text")
        version.setStyleSheet("color: #2e6045; font-size: 11px; margin-left: 4px;")
        lay.addWidget(version)

        lay.addStretch()

        self._dot = QLabel("●")
        self._dot.setObjectName("status_idle")
        lay.addWidget(self._dot)

        self._status_lbl = QLabel("Idle")
        self._status_lbl.setObjectName("status_text")
        lay.addWidget(self._status_lbl)

        lay.addSpacing(14)

        settings_btn = QPushButton("⚙")
        settings_btn.setObjectName("icon_btn")
        settings_btn.setFixedSize(36, 36)
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(self._open_settings)
        lay.addWidget(settings_btn)

        return hdr

    # ── Left panel ────────────────────────────────────────────────────
    def _left_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("panel")
        panel.setMinimumWidth(250)
        panel.setMaximumWidth(340)
        lay = QVBoxLayout(panel)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        # ── Ancuța ──────────────────────────────
        a_title = QLabel("Ancuța AI")
        a_title.setObjectName("section_title")
        lay.addWidget(a_title)

        a_desc = QLabel("Quick tasks · Gemini 1.5 Flash\nWake word: \"GugaBot\"")
        a_desc.setObjectName("section_desc")
        a_desc.setWordWrap(True)
        lay.addWidget(a_desc)

        self._ancuta_status = QLabel(
            "● Listening" if self.voice.available else "● Ready"
        )
        self._ancuta_status.setObjectName("ai_status_active")
        lay.addWidget(self._ancuta_status)

        row = QHBoxLayout()
        row.setSpacing(6)
        self._ancuta_input = QLineEdit()
        self._ancuta_input.setObjectName("ancuta_input")
        self._ancuta_input.setPlaceholderText("Quick command…")
        self._ancuta_input.returnPressed.connect(self._send_ancuta)
        row.addWidget(self._ancuta_input)

        send_btn = QPushButton("→")
        send_btn.setObjectName("send_btn")
        send_btn.setFixedWidth(32)
        send_btn.setToolTip("Send to Ancuța AI")
        send_btn.clicked.connect(self._send_ancuta)
        row.addWidget(send_btn)
        lay.addLayout(row)

        lay.addWidget(self._divider())

        # ── Buftea ──────────────────────────────
        b_title = QLabel("Buftea AI")
        b_title.setObjectName("section_title")
        lay.addWidget(b_title)

        b_desc = QLabel("Full PC control · Gemini 2.5 Pro\nSees your screen")
        b_desc.setObjectName("section_desc")
        b_desc.setWordWrap(True)
        lay.addWidget(b_desc)

        self._buftea_status = QLabel("● Idle")
        self._buftea_status.setObjectName("ai_status_idle")
        self._buftea_status.setStyleSheet("color: #3a6050; font-size: 12px; font-weight: 600;")
        lay.addWidget(self._buftea_status)

        # Session token usage mini-bar
        self._session_lbl = QLabel("Session tokens: —")
        self._session_lbl.setObjectName("section_desc")
        lay.addWidget(self._session_lbl)

        self._buftea_input = QTextEdit()
        self._buftea_input.setObjectName("prompt_input")
        self._buftea_input.setPlaceholderText(
            "Describe a task for Buftea AI…\ne.g. Open Chrome and search for cats"
        )
        self._buftea_input.setFixedHeight(88)
        lay.addWidget(self._buftea_input)

        self._start_btn = QPushButton("▶  Start Buftea AI")
        self._start_btn.setObjectName("primary_btn")
        self._start_btn.clicked.connect(self._start_buftea)
        lay.addWidget(self._start_btn)

        self._stop_btn = QPushButton("■  Stop")
        self._stop_btn.setObjectName("stop_btn")
        self._stop_btn.setEnabled(False)
        self._stop_btn.setToolTip("Stop all AI  (or say \"Guga stop\")")
        self._stop_btn.clicked.connect(self._stop_all)
        lay.addWidget(self._stop_btn)

        lay.addStretch()

        if self.voice.available:
            self._voice_lbl = QLabel("🎤  Voice active")
        else:
            self._voice_lbl = QLabel("🎤  Voice unavailable\n    (install pyaudio)")
        self._voice_lbl.setObjectName("voice_indicator")
        self._voice_lbl.setWordWrap(True)
        lay.addWidget(self._voice_lbl)

        return panel

    # ── Right panel (log + confirm banner) ───────────────────────────
    def _right_panel(self) -> QWidget:
        self._right_frame = QFrame()
        self._right_frame.setObjectName("panel")
        lay = QVBoxLayout(self._right_frame)
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

        # Placeholder widget for confirm banner — inserted above log
        self._banner_slot = QWidget()
        self._banner_slot.setVisible(False)
        self._banner_slot_layout = QVBoxLayout(self._banner_slot)
        self._banner_slot_layout.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._banner_slot)

        self._log = QTextEdit()
        self._log.setObjectName("log_display")
        self._log.setReadOnly(True)
        lay.addWidget(self._log, 1)

        return self._right_frame

    # ── Bottom bar ───────────────────────────────────────────────────
    def _bottom_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("bottom_bar")
        bar.setFixedHeight(34)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(16, 0, 16, 0)

        self._model_lbl = QLabel(self._model_text())
        self._model_lbl.setObjectName("status_bar_text")
        lay.addWidget(self._model_lbl)

        lay.addStretch()

        self._token_lbl = QLabel(self._token_text())
        self._token_lbl.setObjectName("status_bar_text")
        lay.addWidget(self._token_lbl)

        return bar

    # ── Helpers ──────────────────────────────────────────────────────
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
        return f"Ancuța: {ta:,} tok   |   Buftea: {tb:,} tok"

    # ═══════════════════════════════════════════════ Signals
    def _connect_signals(self):
        self.logger.log_added.connect(self._on_log)
        self.buftea.status_changed.connect(self._on_buftea_status)
        self.buftea.confirmation_needed.connect(self._on_confirmation_needed)

        if self.voice.available:
            self.voice.wake_word_detected.connect(self._on_wake_word)
            self.voice.command_detected.connect(self._on_voice_command)
            self.voice.status_changed.connect(self._on_voice_status)

    # ═══════════════════════════════════════════════ Slots
    @pyqtSlot(str, str, str)
    def _on_log(self, ts: str, level: str, msg: str):
        color = LOG_COLORS.get(level, "#6aaa88")
        ts_html = f'<span style="color:#2e6045">[{ts}]</span>'
        msg_html = f'<span style="color:{color}">{_escape_html(msg)}</span>'
        self._log.append(f"{ts_html} {msg_html}")
        self._log.verticalScrollBar().setValue(self._log.verticalScrollBar().maximum())
        self._token_lbl.setText(self._token_text())

        # Trigger sounds based on log level
        if level == "error":
            self.sounds.error()
        elif level == "action":
            self.sounds.action()
        elif level == "wake":
            self.sounds.wake()

    @pyqtSlot(str)
    def _on_buftea_status(self, state: str):
        if state == "running":
            self._buftea_status.setText("● Running")
            self._buftea_status.setStyleSheet("color: #00ff88; font-size: 12px; font-weight: 600;")
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)
            self._set_status("Buftea Active", "active")
        else:
            self._buftea_status.setText("● Idle")
            self._buftea_status.setStyleSheet("color: #3a6050; font-size: 12px; font-weight: 600;")
            self._start_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)
            self._set_status("Idle", "idle")
            self.sounds.done()
            self._session_lbl.setText(
                f"Session tokens: {self.buftea._session_tokens:,}"
            )

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

    # ═══════════════════════════════════════════════ Confirmation banner
    @pyqtSlot(str, str)
    def _on_confirmation_needed(self, label: str, details: str):
        self.sounds.confirm()
        self.logger.log(f"⚠ Confirmation required: {label}", "error")
        self._show_confirm_banner(label, details)

    def _show_confirm_banner(self, label: str, details: str):
        # Remove any existing banner
        self._hide_confirm_banner()

        banner = QFrame()
        banner.setObjectName("confirm_banner")
        bl = QVBoxLayout(banner)
        bl.setContentsMargins(14, 10, 14, 10)
        bl.setSpacing(6)

        title_row = QHBoxLayout()
        title_lbl = QLabel(f"⚠  {label}")
        title_lbl.setObjectName("confirm_banner_title")
        title_row.addWidget(title_lbl)
        title_row.addStretch()

        self._timer_lbl = QLabel("120s")
        self._timer_lbl.setObjectName("confirm_banner_timer")
        title_row.addWidget(self._timer_lbl)
        bl.addLayout(title_row)

        det_lbl = QLabel(details[:200] + ("…" if len(details) > 200 else ""))
        det_lbl.setObjectName("confirm_banner_detail")
        det_lbl.setWordWrap(True)
        bl.addWidget(det_lbl)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        deny_btn = QPushButton("✕  Deny")
        deny_btn.setObjectName("confirm_no_btn")
        deny_btn.clicked.connect(lambda: self._respond_confirm(False))
        btn_row.addWidget(deny_btn)

        allow_btn = QPushButton("✓  Allow")
        allow_btn.setObjectName("confirm_yes_btn")
        allow_btn.clicked.connect(lambda: self._respond_confirm(True))
        btn_row.addWidget(allow_btn)
        bl.addLayout(btn_row)

        self._confirm_banner = banner
        self._banner_slot_layout.addWidget(banner)
        self._banner_slot.setVisible(True)

        # Countdown timer (auto-deny at 0)
        self._confirm_countdown = 120
        self._confirm_timer = QTimer(self)
        self._confirm_timer.timeout.connect(self._tick_confirm)
        self._confirm_timer.start(1000)

    def _tick_confirm(self):
        self._confirm_countdown -= 1
        if self._timer_lbl:
            self._timer_lbl.setText(f"{self._confirm_countdown}s")
        if self._confirm_countdown <= 0:
            self._respond_confirm(False)

    def _respond_confirm(self, confirmed: bool):
        if self._confirm_timer:
            self._confirm_timer.stop()
            self._confirm_timer = None
        self._hide_confirm_banner()
        self.buftea.respond_confirmation(confirmed)
        verb = "allowed" if confirmed else "denied"
        self.logger.log(f"Dangerous action {verb}.", "system")

    def _hide_confirm_banner(self):
        if self._confirm_banner:
            self._banner_slot_layout.removeWidget(self._confirm_banner)
            self._confirm_banner.deleteLater()
            self._confirm_banner = None
        self._banner_slot.setVisible(False)

    # ═══════════════════════════════════════════════ User actions
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
        pos = self.pos()
        sz = self.size()
        self.buftea.set_window_rect(pos.x(), pos.y(), sz.width(), sz.height())
        self._session_lbl.setText("Session tokens: 0")
        self.buftea.start_task(prompt)

    def _stop_all(self):
        self.ancuta.stop()
        self.buftea.stop()
        # If a confirm is pending, auto-deny it
        if self._confirm_banner:
            self._respond_confirm(False)
        self._stop_btn.setEnabled(False)
        self._start_btn.setEnabled(True)
        self._buftea_status.setText("● Idle")
        self._buftea_status.setStyleSheet("color: #3a6050; font-size: 12px; font-weight: 600;")
        self._set_status("Idle", "idle")
        self.sounds.stop()
        self.logger.log("All AI stopped.", "system")

    def _open_settings(self):
        dlg = SettingsDialog(self.config, parent=self)
        if dlg.exec():
            self.ancuta.update_client()
            self.buftea.update_client()
            self.sounds.enabled = self.config.get("sounds_enabled", True)
            self._model_lbl.setText(self._model_text())
            self._token_lbl.setText(self._token_text())

    def _clear_log(self):
        self._log.clear()
        self.logger.clear()

    # ═══════════════════════════════════════════════ Helpers
    def _set_status(self, text: str, state: str):
        self._status_lbl.setText(text)
        colours = {"idle": "#3a6050", "active": "#00ff88", "error": "#ff3355"}
        c = colours.get(state, "#3a6050")
        self._dot.setStyleSheet(f"color: {c}; font-size: 18px;")

    def _post_init(self):
        self.logger.log("GugaBot started.", "system")
        if not self.config.get("api_key"):
            self.logger.log("No API key set — open ⚙ Settings to configure.", "error")
        if self.voice.available:
            self.voice.start()
            self.logger.log(
                'Voice active — say "GugaBot" to wake Ancuța AI, "Guga stop" to halt.',
                "system",
            )
        else:
            self.logger.log(
                "Voice unavailable — install pyaudio for voice control.", "system"
            )


# ── helpers ──────────────────────────────────────────────────────────────────
def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )
