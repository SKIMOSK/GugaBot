from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from gugabot.config import Config


class SettingsDialog(QDialog):
    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Settings — GugaBot")
        self.setMinimumSize(540, 500)
        if parent:
            self.setStyleSheet(parent.styleSheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        tabs = QTabWidget()
        tabs.addTab(self._tab_api(), "API & Models")
        tabs.addTab(self._tab_safety(), "Safety & Limits")
        tabs.addTab(self._tab_general(), "General")
        tabs.addTab(self._tab_usage(), "Usage")
        root.addWidget(tabs, 1)

        # Footer
        footer = QWidget()
        footer.setObjectName("bottom_bar")
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(16, 8, 16, 8)
        fl.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("text_btn")
        cancel_btn.clicked.connect(self.reject)
        fl.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("primary_btn")
        save_btn.clicked.connect(self._save)
        fl.addWidget(save_btn)

        root.addWidget(footer)

    # ──────────────────────────────────────────────────────────── Tabs
    def _tab_api(self) -> QWidget:
        tab, lay = self._make_tab()

        lay.addWidget(self._lbl("OpenRouter API Key"))
        self._api_key = QLineEdit()
        self._api_key.setPlaceholderText("sk-or-v1-…")
        self._api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self._api_key.setText(self.config.get("api_key", ""))
        lay.addWidget(self._api_key)

        toggle = QPushButton("Show / Hide key")
        toggle.setObjectName("text_btn")
        toggle.clicked.connect(self._toggle_key)
        lay.addWidget(toggle)

        lay.addWidget(self._divider())

        lay.addWidget(self._lbl("Ancuța AI model  (quick tasks, no screen)"))
        self._ancuta_model = self._combo([
            "google/gemini-flash-1.5",
            "google/gemini-flash-1.5-8b",
            "google/gemini-2.0-flash-001",
            "openai/gpt-4o-mini",
            "anthropic/claude-3-haiku",
        ], self.config.get("ancuta_model", "google/gemini-flash-1.5"))
        lay.addWidget(self._ancuta_model)

        lay.addWidget(self._lbl("Buftea AI model  (full PC control, screen-aware)"))
        self._buftea_model = self._combo([
            "google/gemini-2.5-pro",
            "google/gemini-pro-1.5",
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o",
            "openai/gpt-4-turbo",
        ], self.config.get("buftea_model", "google/gemini-2.5-pro"))
        lay.addWidget(self._buftea_model)

        lay.addStretch()
        return tab

    # ------------------------------------------------------------------
    def _tab_safety(self) -> QWidget:
        tab, lay = self._make_tab()

        # Max tokens per request
        lay.addWidget(self._lbl("Buftea AI — max tokens per request"))
        self._max_req = self._combo(
            ["256", "512", "1024", "2048", "4096", "8192"],
            str(self.config.get("buftea_max_tokens_per_request", 1024)),
        )
        lay.addWidget(self._max_req)

        note_req = QLabel(
            "Limits how long each individual response from Buftea AI can be."
        )
        note_req.setObjectName("section_desc")
        note_req.setWordWrap(True)
        lay.addWidget(note_req)

        lay.addWidget(self._divider())

        # Max tokens per session
        lay.addWidget(self._lbl("Buftea AI — max tokens per session (0 = unlimited)"))
        sess_row = QHBoxLayout()
        self._max_session = QSpinBox()
        self._max_session.setRange(0, 2_000_000)
        self._max_session.setSingleStep(10_000)
        self._max_session.setValue(self.config.get("buftea_max_tokens_per_session", 0))
        self._max_session.setSpecialValueText("Unlimited")
        sess_row.addWidget(self._max_session)
        sess_row.addStretch()
        lay.addLayout(sess_row)

        note_sess = QLabel(
            "Buftea AI will stop automatically once this many tokens have been used\n"
            "in the current task session. Resets each time you start a new task."
        )
        note_sess.setObjectName("section_desc")
        note_sess.setWordWrap(True)
        lay.addWidget(note_sess)

        lay.addWidget(self._divider())

        # No-ask toggle
        self._no_ask = QCheckBox(
            "Allow dangerous actions without asking  (terminal, delete, download, scripts)"
        )
        self._no_ask.setChecked(self.config.get("buftea_allow_dangerous_no_ask", False))
        lay.addWidget(self._no_ask)

        warn = QLabel(
            "⚠  By default Buftea AI pauses and asks for confirmation before running\n"
            "terminal commands, deleting files, downloading, or installing software.\n"
            "Enabling this disables that safety check — use with care."
        )
        warn.setObjectName("section_desc")
        warn.setWordWrap(True)
        lay.addWidget(warn)

        lay.addStretch()
        return tab

    # ------------------------------------------------------------------
    def _tab_general(self) -> QWidget:
        tab, lay = self._make_tab()

        lay.addWidget(self._lbl("Buftea AI — screenshot interval"))
        self._interval = self._combo(
            ["5 seconds", "10 seconds", "30 seconds", "1 minute"],
            {5: "5 seconds", 10: "10 seconds", 30: "30 seconds", 60: "1 minute"}.get(
                self.config.get("screenshot_interval", 10), "10 seconds"
            ),
        )
        lay.addWidget(self._interval)

        note = QLabel(
            "How long Buftea AI waits between each screenshot cycle.\n"
            "Shorter = faster reactions, more tokens used."
        )
        note.setObjectName("section_desc")
        note.setWordWrap(True)
        lay.addWidget(note)

        lay.addWidget(self._divider())

        self._sounds = QCheckBox("Enable sound effects")
        self._sounds.setChecked(self.config.get("sounds_enabled", True))
        lay.addWidget(self._sounds)

        lay.addStretch()
        return tab

    # ------------------------------------------------------------------
    def _tab_usage(self) -> QWidget:
        tab, lay = self._make_tab()

        usage = self.config.get("usage", {})
        lay.addWidget(self._usage_card("Ancuța AI", usage.get("ancuta", {})))
        lay.addWidget(self._usage_card("Buftea AI", usage.get("buftea", {})))

        reset_btn = QPushButton("Reset all usage statistics")
        reset_btn.setObjectName("stop_btn")
        reset_btn.clicked.connect(self._reset_usage)
        lay.addWidget(reset_btn)

        lay.addStretch()
        return tab

    def _usage_card(self, title: str, data: dict) -> QFrame:
        card = QFrame()
        card.setObjectName("usage_card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(3)

        h = QLabel(title)
        h.setObjectName("section_title")
        cl.addWidget(h)

        ti = data.get("tokens_in", 0)
        to = data.get("tokens_out", 0)
        rq = data.get("requests", 0)
        for text in [
            f"Input tokens:   {ti:>12,}",
            f"Output tokens:  {to:>12,}",
            f"Total tokens:   {ti + to:>12,}",
            f"Requests:       {rq:>12,}",
        ]:
            lbl = QLabel(text)
            lbl.setObjectName("section_desc")
            from PyQt6.QtGui import QFont
            f = QFont("Cascadia Code", 11)
            f.setStyleHint(QFont.StyleHint.Monospace)
            lbl.setFont(f)
            cl.addWidget(lbl)
        return card

    # ──────────────────────────────────────────────────────────── Helpers
    def _make_tab(self) -> tuple[QWidget, QVBoxLayout]:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(10)
        return tab, lay

    def _lbl(self, text: str) -> QLabel:
        l = QLabel(text)
        l.setObjectName("form_label")
        return l

    def _divider(self) -> QFrame:
        d = QFrame()
        d.setObjectName("divider")
        d.setFrameShape(QFrame.Shape.HLine)
        d.setFixedHeight(1)
        return d

    def _combo(self, items: list[str], current: str) -> QComboBox:
        cb = QComboBox()
        cb.addItems(items)
        idx = cb.findText(current)
        if idx >= 0:
            cb.setCurrentIndex(idx)
        return cb

    def _toggle_key(self):
        em = self._api_key.echoMode()
        self._api_key.setEchoMode(
            QLineEdit.EchoMode.Normal
            if em == QLineEdit.EchoMode.Password
            else QLineEdit.EchoMode.Password
        )

    def _reset_usage(self):
        self.config.reset_usage()
        QMessageBox.information(self, "GugaBot", "Usage statistics have been reset.")

    # ──────────────────────────────────────────────────────────── Save
    def _save(self):
        self.config.set("api_key", self._api_key.text().strip())
        self.config.set("ancuta_model", self._ancuta_model.currentText())
        self.config.set("buftea_model", self._buftea_model.currentText())
        self.config.set("buftea_max_tokens_per_request", int(self._max_req.currentText()))
        self.config.set("buftea_max_tokens_per_session", self._max_session.value())
        self.config.set("buftea_allow_dangerous_no_ask", self._no_ask.isChecked())
        interval_map = {"5 seconds": 5, "10 seconds": 10, "30 seconds": 30, "1 minute": 60}
        self.config.set("screenshot_interval", interval_map.get(self._interval.currentText(), 10))
        self.config.set("sounds_enabled", self._sounds.isChecked())
        self.accept()
