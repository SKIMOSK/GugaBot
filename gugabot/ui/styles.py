"""
GugaBot — Neon Aero theme.
Windows 7 Aero proportions + neon green/teal accents on a deep dark background.
Gradients simulate the glass-panel effect without platform transparency APIs.
"""

STYLESHEET = """
/* ═══════════════════════════════════════════════════
   GLOBAL
   ═══════════════════════════════════════════════════ */
QMainWindow, QDialog {
    background-color: #08100d;
    color: #c5e8d5;
    font-family: "Segoe UI", "Tahoma", "DejaVu Sans", sans-serif;
    font-size: 13px;
}

QWidget {
    background-color: transparent;
    color: #c5e8d5;
    font-size: 13px;
}

/* ═══════════════════════════════════════════════════
   HEADER — Aero gradient bar
   ═══════════════════════════════════════════════════ */
#header {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0   #0f2818,
        stop:0.4 #091a0f,
        stop:1   #060e09);
    border-bottom: 1px solid #00ff88;
}

#app_title {
    color: #00ff88;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 3px;
    font-family: "Segoe UI", "Tahoma", monospace;
}

/* ═══════════════════════════════════════════════════
   CONTENT AREA
   ═══════════════════════════════════════════════════ */
#content {
    background-color: #08100d;
}

/* ═══════════════════════════════════════════════════
   PANELS — glass card (Aero-style gradient + bright top edge)
   ═══════════════════════════════════════════════════ */
#panel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0   #112618,
        stop:0.3 #0b1c11,
        stop:1   #070f0a);
    border: 1px solid #1a4028;
    border-top: 1px solid #2e7048;
    border-radius: 4px;
}

#usage_card {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0d1e13,
        stop:1 #080f0b);
    border: 1px solid #1a4028;
    border-top: 1px solid #2a5838;
    border-radius: 4px;
    padding: 4px;
}

/* ═══════════════════════════════════════════════════
   TYPOGRAPHY
   ═══════════════════════════════════════════════════ */
#section_title {
    color: #00ff88;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
}

#section_desc {
    color: #5a8870;
    font-size: 11px;
    line-height: 1.6;
}

#form_label {
    color: #6aaa88;
    font-size: 12px;
    font-weight: 500;
}

/* ═══════════════════════════════════════════════════
   STATUS INDICATORS
   ═══════════════════════════════════════════════════ */
#status_idle   { color: #3a6050; font-size: 18px; }
#status_active { color: #00ff88; font-size: 18px; }
#status_error  { color: #ff3355; font-size: 18px; }
#status_text   { color: #5a9070; font-size: 12px; font-weight: 600; letter-spacing: 1px; }

#ai_status_idle   { color: #3a6050; font-size: 12px; font-weight: 600; }
#ai_status_active { color: #00ff88; font-size: 12px; font-weight: 600; }

#voice_indicator {
    color: #3a6050;
    font-size: 11px;
    font-style: italic;
}

/* ═══════════════════════════════════════════════════
   LOG DISPLAY — monospaced terminal
   ═══════════════════════════════════════════════════ */
#log_display {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #060e08, stop:1 #04080500);
    color: #a8d8b8;
    border: 1px solid #1a4028;
    border-top: 1px solid #2e7048;
    border-radius: 4px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 12px;
    padding: 8px;
    selection-background-color: #00ff8844;
    selection-color: #ffffff;
}

/* ═══════════════════════════════════════════════════
   TEXT INPUTS
   ═══════════════════════════════════════════════════ */
#prompt_input, #ancuta_input {
    background-color: #060e09;
    color: #c5e8d5;
    border: 1px solid #1a4028;
    border-top: 1px solid #2a5838;
    border-radius: 3px;
    padding: 5px 8px;
    font-size: 12px;
    selection-background-color: #00ff8844;
}

#prompt_input:focus, #ancuta_input:focus {
    border-color: #00ff88;
    border-top-color: #40ffaa;
}

/* ═══════════════════════════════════════════════════
   FORM INPUTS (settings)
   ═══════════════════════════════════════════════════ */
QLineEdit, QSpinBox {
    background-color: #060e09;
    color: #c5e8d5;
    border: 1px solid #1a4028;
    border-top: 1px solid #2a5838;
    border-radius: 3px;
    padding: 5px 8px;
    min-height: 26px;
    font-size: 13px;
    selection-background-color: #00ff8844;
}

QLineEdit:focus, QSpinBox:focus {
    border-color: #00ff88;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #0f2015;
    border: 1px solid #1a4028;
    width: 14px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #1a3020;
}
QSpinBox::up-arrow  { border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 5px solid #00ff88; width:0; height:0; }
QSpinBox::down-arrow{ border-left: 4px solid transparent; border-right: 4px solid transparent; border-top:    5px solid #00ff88; width:0; height:0; }

QComboBox {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #122018, stop:1 #080f0b);
    color: #c5e8d5;
    border: 1px solid #1a4028;
    border-top: 1px solid #2a5838;
    border-radius: 3px;
    padding: 5px 8px;
    min-height: 26px;
    font-size: 13px;
}

QComboBox:focus { border-color: #00ff88; }

QComboBox::drop-down {
    border-left: 1px solid #1a4028;
    width: 20px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #122018, stop:1 #0a1510);
}

QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #00ff88;
    width: 0;
    height: 0;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #0d1e13;
    border: 1px solid #00ff88;
    border-radius: 3px;
    color: #c5e8d5;
    selection-background-color: #00ff8830;
    selection-color: #00ff88;
    outline: none;
}

QCheckBox {
    color: #c5e8d5;
    spacing: 8px;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    background-color: #060e09;
    border: 1px solid #1a4028;
    border-radius: 3px;
}

QCheckBox::indicator:hover {
    border-color: #00ff88;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #00cc66, stop:1 #008844);
    border-color: #00ff88;
    image: none;
}

/* ═══════════════════════════════════════════════════
   BUTTONS — Aero bevel gradient
   ═══════════════════════════════════════════════════ */
#primary_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0   #1a6035,
        stop:0.5 #124428,
        stop:1   #0c3018);
    color: #00ff88;
    border: 1px solid #00cc66;
    border-top: 1px solid #40ff99;
    border-radius: 3px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 600;
    min-height: 28px;
    letter-spacing: 0.5px;
}

#primary_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0   #22783f,
        stop:0.5 #185433,
        stop:1   #103820);
    border-color: #00ff88;
    border-top-color: #66ffbb;
    color: #66ffbb;
}

#primary_btn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0c3018, stop:1 #1a6035);
    border-top-color: #00cc66;
}

#primary_btn:disabled {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #111a14, stop:1 #0a1009);
    color: #2a4030;
    border-color: #182818;
}

/* ── Stop button ── */
#stop_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3d0e18, stop:0.5 #280a10, stop:1 #1c0609);
    color: #ff3355;
    border: 1px solid #cc2244;
    border-top: 1px solid #ff6688;
    border-radius: 3px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 600;
    min-height: 28px;
}

#stop_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4f1220, stop:1 #280a10);
    border-color: #ff3355;
    border-top-color: #ff88aa;
    color: #ff6680;
}

#stop_btn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1c0609, stop:1 #3d0e18);
}

#stop_btn:disabled {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #160a0c, stop:1 #0e0608);
    color: #3a1c22;
    border-color: #1e0c10;
}

/* ── Ghost / text button ── */
#text_btn {
    background: transparent;
    color: #5a9070;
    border: 1px solid #1a4028;
    border-radius: 3px;
    padding: 4px 12px;
    font-size: 12px;
    min-height: 24px;
}

#text_btn:hover {
    color: #00ff88;
    border-color: #00ff88;
    background: #00ff8812;
}

/* ── Icon button (⚙) ── */
#icon_btn {
    background: transparent;
    color: #3a6050;
    border: 1px solid transparent;
    border-radius: 3px;
    font-size: 17px;
}

#icon_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a4028, stop:1 #0f2015);
    border: 1px solid #2e7048;
    color: #00ff88;
}

/* ── Send arrow button ── */
#send_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0d3a60, stop:1 #082040);
    color: #00e5ff;
    border: 1px solid #0088cc;
    border-top: 1px solid #00ccff;
    border-radius: 3px;
    padding: 4px 8px;
    font-size: 13px;
    font-weight: 700;
    min-height: 24px;
}

#send_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #104878, stop:1 #0a2850);
    border-color: #00e5ff;
    color: #66f2ff;
}

#send_btn:disabled {
    background: #0a1520;
    color: #1a4055;
    border-color: #0a2030;
}

/* ── Confirm (YES) button ── */
#confirm_yes_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a6035, stop:1 #0c3018);
    color: #00ff88;
    border: 1px solid #00cc66;
    border-top: 1px solid #40ff99;
    border-radius: 3px;
    padding: 6px 20px;
    font-size: 13px;
    font-weight: 700;
    min-height: 28px;
}
#confirm_yes_btn:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #22783f,stop:1 #103820); color: #66ffbb; border-color: #00ff88; }

/* ── Deny (NO) button ── */
#confirm_no_btn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3d0e18, stop:1 #1c0609);
    color: #ff3355;
    border: 1px solid #cc2244;
    border-top: 1px solid #ff6688;
    border-radius: 3px;
    padding: 6px 20px;
    font-size: 13px;
    font-weight: 700;
    min-height: 28px;
}
#confirm_no_btn:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4f1220,stop:1 #280a10); color: #ff6680; border-color: #ff3355; }

/* ═══════════════════════════════════════════════════
   CONFIRM BANNER (inline in log panel)
   ═══════════════════════════════════════════════════ */
#confirm_banner {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e0a00, stop:1 #140700);
    border: 1px solid #ff8800;
    border-top: 2px solid #ffaa00;
    border-radius: 4px;
}

#confirm_banner_title {
    color: #ffaa00;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}

#confirm_banner_detail {
    color: #cc8844;
    font-size: 12px;
    font-family: "Cascadia Code", "Consolas", monospace;
}

#confirm_banner_timer {
    color: #886644;
    font-size: 11px;
    font-style: italic;
}

/* ═══════════════════════════════════════════════════
   DIVIDER
   ═══════════════════════════════════════════════════ */
#divider {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 transparent, stop:0.2 #2e7048, stop:0.8 #2e7048, stop:1 transparent);
    border: none;
    max-height: 1px;
}

/* ═══════════════════════════════════════════════════
   BOTTOM STATUS BAR
   ═══════════════════════════════════════════════════ */
#bottom_bar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #060e09, stop:1 #040a07);
    border-top: 1px solid #1a4028;
}

#status_bar_text {
    color: #2e6045;
    font-size: 11px;
    font-family: "Cascadia Code", "Consolas", monospace;
}

/* ═══════════════════════════════════════════════════
   SETTINGS DIALOG TABS
   ═══════════════════════════════════════════════════ */
QTabWidget::pane {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0d1e13, stop:1 #070f0a);
    border: 1px solid #1a4028;
    border-top: none;
    border-radius: 0 0 4px 4px;
}

QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0e1c12, stop:1 #08100a);
    color: #3a6050;
    border: 1px solid #1a4028;
    border-bottom: none;
    padding: 7px 18px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-size: 13px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a5035, stop:1 #0d1e13);
    color: #00ff88;
    border-top: 2px solid #00ff88;
    border-left-color: #2e7048;
    border-right-color: #2e7048;
}

QTabBar::tab:hover:!selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #122018, stop:1 #0a1510);
    color: #5aaa80;
    border-top-color: #2e7048;
}

/* ═══════════════════════════════════════════════════
   SPLITTER
   ═══════════════════════════════════════════════════ */
QSplitter::handle {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0a1a0f, stop:0.5 #1a4028, stop:1 #0a1a0f);
    width: 3px;
}

/* ═══════════════════════════════════════════════════
   SCROLLBARS
   ═══════════════════════════════════════════════════ */
QScrollBar:vertical {
    background-color: #060e09;
    width: 8px;
    margin: 0;
    border-left: 1px solid #0f2015;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a4028, stop:1 #2e7048);
    border-radius: 3px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2e7048, stop:1 #00cc66);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QScrollBar:horizontal {
    height: 8px;
    background-color: #060e09;
    border-top: 1px solid #0f2015;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a4028, stop:1 #2e7048);
    border-radius: 3px;
}

/* ═══════════════════════════════════════════════════
   TOOLTIP
   ═══════════════════════════════════════════════════ */
QToolTip {
    background-color: #0d1e13;
    color: #00ff88;
    border: 1px solid #2e7048;
    border-radius: 3px;
    padding: 4px 8px;
    font-size: 12px;
}

/* ═══════════════════════════════════════════════════
   MESSAGE BOX (dialogs)
   ═══════════════════════════════════════════════════ */
QMessageBox {
    background-color: #0d1e13;
    color: #c5e8d5;
}

QMessageBox QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a6035, stop:1 #0c3018);
    color: #00ff88;
    border: 1px solid #00cc66;
    border-radius: 3px;
    padding: 5px 18px;
    min-width: 70px;
    font-size: 13px;
}
QMessageBox QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #22783f, stop:1 #103820);
    border-color: #00ff88;
}
"""
