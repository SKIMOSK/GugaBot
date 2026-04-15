from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
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
        self.setMinimumSize(520, 440)
        if parent:
            self.setStyleSheet(parent.styleSheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        tabs = QTabWidget()
        tabs.addTab(self._tab_api(), "API & Models")
        tabs.addTab(self._tab_general(), "General")
        tabs.addTab(self._tab_usage(), "Usage")
        root.addWidget(tabs, 1)

        # Footer buttons
        footer = QWidget()
        footer.setObjectName("bottom_bar")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 8, 16, 8)
        footer_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("text_btn")
        cancel_btn.clicked.connect(self.reject)
        footer_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("primary_btn")
        save_btn.clicked.connect(self._save)
        footer_layout.addWidget(save_btn)

        root.addWidget(footer)

    # ------------------------------------------------------------------
    def _tab_api(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(self._label("OpenRouter API Key"))
        self._api_key = QLineEdit()
        self._api_key.setObjectName("form_input")
        self._api_key.setPlaceholderText("sk-or-v1-…")
        self._api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self._api_key.setText(self.config.get("api_key", ""))
        lay.addWidget(self._api_key)

        toggle = QPushButton("Show / Hide key")
        toggle.setObjectName("text_btn")
        toggle.clicked.connect(self._toggle_key_visibility)
        lay.addWidget(toggle)

        lay.addWidget(self._divider())

        # Ancuța model
        lay.addWidget(self._label("Ancuța AI model  (quick tasks)"))
        self._ancuta_model = QComboBox()
        self._ancuta_model.setObjectName("form_input")
        for m in [
            "google/gemini-flash-1.5",
            "google/gemini-flash-1.5-8b",
            "google/gemini-2.0-flash-001",
            "openai/gpt-4o-mini",
            "anthropic/claude-3-haiku",
        ]:
            self._ancuta_model.addItem(m)
        self._set_combo(self._ancuta_model, self.config.get("ancuta_model", "google/gemini-flash-1.5"))
        lay.addWidget(self._ancuta_model)

        # Buftea model
        lay.addWidget(self._label("Buftea AI model  (full PC control)"))
        self._buftea_model = QComboBox()
        self._buftea_model.setObjectName("form_input")
        for m in [
            "google/gemini-2.5-pro",
            "google/gemini-pro-1.5",
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o",
            "openai/gpt-4-turbo",
        ]:
            self._buftea_model.addItem(m)
        self._set_combo(self._buftea_model, self.config.get("buftea_model", "google/gemini-2.5-pro"))
        lay.addWidget(self._buftea_model)

        lay.addStretch()
        return tab

    # ------------------------------------------------------------------
    def _tab_general(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(self._label("Buftea AI — screenshot interval"))
        self._interval = QComboBox()
        self._interval.setObjectName("form_input")
        self._interval.addItems(["5 seconds", "10 seconds", "30 seconds", "1 minute"])
        interval_map = {5: 0, 10: 1, 30: 2, 60: 3}
        idx = interval_map.get(self.config.get("screenshot_interval", 10), 1)
        self._interval.setCurrentIndex(idx)
        lay.addWidget(self._interval)

        note = QLabel(
            "This controls how long Buftea AI waits between taking a new\n"
            "screenshot and sending it to the model."
        )
        note.setObjectName("section_desc")
        lay.addWidget(note)

        lay.addStretch()
        return tab

    # ------------------------------------------------------------------
    def _tab_usage(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

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
        lay = QVBoxLayout(card)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(4)

        lbl = QLabel(title)
        lbl.setObjectName("section_title")
        lay.addWidget(lbl)

        tok_in = data.get("tokens_in", 0)
        tok_out = data.get("tokens_out", 0)
        reqs = data.get("requests", 0)
        total = tok_in + tok_out

        for text in [
            f"Input tokens:   {tok_in:,}",
            f"Output tokens:  {tok_out:,}",
            f"Total tokens:   {total:,}",
            f"Requests:       {reqs:,}",
        ]:
            row = QLabel(text)
            row.setObjectName("section_desc")
            row.setFont(self._mono_font())
            lay.addWidget(row)

        return card

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("form_label")
        return lbl

    def _divider(self) -> QFrame:
        d = QFrame()
        d.setObjectName("divider")
        d.setFrameShape(QFrame.Shape.HLine)
        d.setFixedHeight(1)
        return d

    def _set_combo(self, combo: QComboBox, value: str):
        idx = combo.findText(value)
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def _mono_font(self):
        from PyQt6.QtGui import QFont
        f = QFont("Consolas", 11)
        f.setStyleHint(QFont.StyleHint.Monospace)
        return f

    def _toggle_key_visibility(self):
        if self._api_key.echoMode() == QLineEdit.EchoMode.Password:
            self._api_key.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self._api_key.setEchoMode(QLineEdit.EchoMode.Password)

    def _reset_usage(self):
        self.config.reset_usage()
        # Refresh the tab by closing/re-opening — simple approach
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "GugaBot", "Usage statistics reset.")

    def _save(self):
        self.config.set("api_key", self._api_key.text().strip())
        self.config.set("ancuta_model", self._ancuta_model.currentText())
        self.config.set("buftea_model", self._buftea_model.currentText())
        interval_values = [5, 10, 30, 60]
        self.config.set("screenshot_interval", interval_values[self._interval.currentIndex()])
        self.accept()
