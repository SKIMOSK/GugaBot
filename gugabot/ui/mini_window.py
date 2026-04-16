"""
MiniWindow — compact always-on-top overlay.
Shows: [◀ Back]  [■ Stop]  status dot  last action text
Positioned in the top-right corner of the primary screen.
"""

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from gugabot.ai.ancuta import AncutaAI
from gugabot.ai.buftea import BufteaAI
from gugabot.logger import ActivityLogger
from gugabot.sounds import SoundManager


_MINI_STYLE = """
QWidget {
    background-color: #08100d;
    color: #c5e8d5;
    font-family: "Segoe UI", "Tahoma", sans-serif;
    font-size: 12px;
}

#mini_frame {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #112618, stop:1 #070f0a);
    border: 1px solid #00ff88;
    border-radius: 4px;
}

#mini_back_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0d3a60, stop:1 #082040);
    color: #00e5ff;
    border: 1px solid #0088cc;
    border-top: 1px solid #00ccff;
    border-radius: 3px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 700;
    min-width: 44px;
    min-height: 22px;
}
#mini_back_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #104878, stop:1 #0a2850);
    color: #66f2ff;
}

#mini_stop_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3d0e18, stop:1 #1c0609);
    color: #ff3355;
    border: 1px solid #cc2244;
    border-top: 1px solid #ff6688;
    border-radius: 3px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 700;
    min-width: 44px;
    min-height: 22px;
}
#mini_stop_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4f1220, stop:1 #280a10);
    color: #ff6680;
}
#mini_stop_btn:disabled {
    color: #3a1c22;
    border-color: #1e0c10;
    background: #120508;
}

#mini_status_dot { font-size: 14px; }
#mini_status_lbl { color: #3a6050; font-size: 11px; font-weight: 600; letter-spacing: 1px; }
#mini_action_lbl { color: #6aaa88; font-size: 11px; }
#mini_sep        { color: #1a4028; }
"""


class MiniWindow(QWidget):
    def __init__(
        self,
        main_window,         # MainWindow — shown on "back"
        ancuta: AncutaAI,
        buftea: BufteaAI,
        logger: ActivityLogger,
        sounds: SoundManager,
    ):
        super().__init__()
        self._main = main_window
        self._ancuta = ancuta
        self._buftea = buftea
        self._logger = logger
        self._sounds = sounds

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool           # no taskbar entry
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setStyleSheet(_MINI_STYLE)
        self.setFixedHeight(46)

        self._build_ui()
        self._connect_signals()

    # ── UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setObjectName("mini_frame")
        lay = QHBoxLayout(frame)
        lay.setContentsMargins(8, 4, 8, 4)
        lay.setSpacing(8)

        # Back button
        back_btn = QPushButton("◀ Back")
        back_btn.setObjectName("mini_back_btn")
        back_btn.setToolTip("Restore main window")
        back_btn.clicked.connect(self._go_back)
        lay.addWidget(back_btn)

        # Stop button
        self._stop_btn = QPushButton("■ Stop")
        self._stop_btn.setObjectName("mini_stop_btn")
        self._stop_btn.setToolTip("Stop all AI activity")
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._stop_all)
        lay.addWidget(self._stop_btn)

        # Separator
        sep = QLabel("|")
        sep.setObjectName("mini_sep")
        lay.addWidget(sep)

        # Status dot
        self._dot = QLabel("●")
        self._dot.setObjectName("mini_status_dot")
        self._dot.setStyleSheet("color: #3a6050;")
        lay.addWidget(self._dot)

        # Status label
        self._status_lbl = QLabel("Idle")
        self._status_lbl.setObjectName("mini_status_lbl")
        lay.addWidget(self._status_lbl)

        # Separator
        sep2 = QLabel("|")
        sep2.setObjectName("mini_sep")
        lay.addWidget(sep2)

        # Last action
        self._action_lbl = QLabel("—")
        self._action_lbl.setObjectName("mini_action_lbl")
        self._action_lbl.setMaximumWidth(340)
        lay.addWidget(self._action_lbl, 1)

        outer.addWidget(frame)

    # ── Signals ─────────────────────────────────────────────────────────
    def _connect_signals(self):
        self._logger.log_added.connect(self._on_log)
        self._buftea.status_changed.connect(self._on_buftea_status)

    @pyqtSlot(str, str, str)
    def _on_log(self, _ts: str, level: str, msg: str):
        if level in ("action", "wake", "response"):
            # Trim to fit the narrow label
            short = msg if len(msg) <= 60 else msg[:57] + "…"
            self._action_lbl.setText(short)

    @pyqtSlot(str)
    def _on_buftea_status(self, state: str):
        if state == "running":
            self._dot.setStyleSheet("color: #00ff88; font-size: 14px;")
            self._status_lbl.setText("Buftea Active")
            self._stop_btn.setEnabled(True)
        else:
            self._dot.setStyleSheet("color: #3a6050; font-size: 14px;")
            self._status_lbl.setText("Idle")
            self._stop_btn.setEnabled(False)

    # ── Actions ─────────────────────────────────────────────────────────
    def _go_back(self):
        self.hide()
        self._main.show()
        self._main.raise_()
        self._main.activateWindow()

    def _stop_all(self):
        self._ancuta.stop()
        self._buftea.stop()
        self._sounds.stop()
        self._stop_btn.setEnabled(False)
        self._logger.log("All AI stopped (mini).", "system")

    # ── Show / position ─────────────────────────────────────────────────
    def show_top_right(self):
        self.adjustSize()
        screen: QScreen = QApplication.primaryScreen()
        geom = screen.availableGeometry()
        # Width adapts to content; clamp so it doesn't overflow
        w = max(self.sizeHint().width(), 460)
        self.setFixedWidth(w)
        self.move(geom.right() - w - 8, geom.top() + 8)
        self.show()
        self.raise_()
