STYLESHEET = """
/* ===== Root / Background ===== */
QMainWindow, QDialog {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: "Segoe UI", "SF Pro Display", "Helvetica Neue", sans-serif;
    font-size: 13px;
}

QWidget {
    background-color: transparent;
    color: #e6edf3;
    font-size: 13px;
}

/* ===== Header ===== */
#header {
    background-color: #0d1117;
    border-bottom: 1px solid #21262d;
}

#app_title {
    color: #39d353;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
}

/* ===== Content ===== */
#content {
    background-color: #0d1117;
}

/* ===== Panels / Cards ===== */
#panel {
    background-color: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
}

#usage_card {
    background-color: #0d1117;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 8px;
}

/* ===== Typography ===== */
#section_title {
    color: #e6edf3;
    font-size: 14px;
    font-weight: 600;
}

#section_desc {
    color: #8b949e;
    font-size: 12px;
    line-height: 1.5;
}

#form_label {
    color: #8b949e;
    font-size: 12px;
    font-weight: 500;
}

/* ===== Status ===== */
#status_idle   { color: #6a737d; font-size: 18px; }
#status_active { color: #39d353; font-size: 18px; }
#status_error  { color: #f85149; font-size: 18px; }
#status_text   { color: #8b949e; font-size: 12px; font-weight: 500; }

#ai_status_idle   { color: #6a737d; font-size: 12px; font-weight: 500; }
#ai_status_active { color: #39d353; font-size: 12px; font-weight: 500; }

#voice_indicator {
    color: #6a737d;
    font-size: 11px;
}

/* ===== Log Display ===== */
#log_display {
    background-color: #0d1117;
    color: #e6edf3;
    border: 1px solid #21262d;
    border-radius: 6px;
    font-family: "Consolas", "Cascadia Code", "Courier New", monospace;
    font-size: 12px;
    padding: 8px;
    selection-background-color: #1f6feb;
}

/* ===== Prompt Input ===== */
#prompt_input {
    background-color: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
    selection-background-color: #1f6feb;
}

#prompt_input:focus {
    border-color: #39d353;
}

#ancuta_input {
    background-color: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
    selection-background-color: #1f6feb;
}

#ancuta_input:focus {
    border-color: #39d353;
}

/* ===== Form Inputs ===== */
#form_input, QLineEdit, QComboBox {
    background-color: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 10px;
    min-height: 28px;
    font-size: 13px;
    selection-background-color: #1f6feb;
}

#form_input:focus, QLineEdit:focus {
    border-color: #39d353;
    outline: none;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #8b949e;
    width: 0;
    height: 0;
    margin-right: 6px;
}

QComboBox QAbstractItemView {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    selection-background-color: #1f6feb;
}

/* ===== Buttons ===== */
#primary_btn {
    background-color: #238636;
    color: #ffffff;
    border: 1px solid #2ea043;
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 600;
    min-height: 32px;
}

#primary_btn:hover {
    background-color: #2ea043;
    border-color: #3fb950;
}

#primary_btn:pressed {
    background-color: #196127;
}

#primary_btn:disabled {
    background-color: #21262d;
    color: #6a737d;
    border-color: #30363d;
}

#stop_btn {
    background-color: #21262d;
    color: #f85149;
    border: 1px solid #f85149;
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 600;
    min-height: 32px;
}

#stop_btn:hover {
    background-color: #3d1a19;
    border-color: #ff7b72;
    color: #ff7b72;
}

#stop_btn:pressed {
    background-color: #5a1d1a;
}

#stop_btn:disabled {
    color: #6a737d;
    border-color: #30363d;
}

#text_btn {
    background-color: transparent;
    color: #8b949e;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    min-height: 28px;
}

#text_btn:hover {
    color: #e6edf3;
    border-color: #8b949e;
}

#icon_btn {
    background-color: transparent;
    color: #8b949e;
    border: 1px solid transparent;
    border-radius: 6px;
    font-size: 16px;
}

#icon_btn:hover {
    background-color: #21262d;
    color: #e6edf3;
    border-color: #30363d;
}

#send_btn {
    background-color: #1f6feb;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
    min-height: 28px;
}

#send_btn:hover {
    background-color: #388bfd;
}

#send_btn:disabled {
    background-color: #21262d;
    color: #6a737d;
}

/* ===== Divider ===== */
#divider {
    background-color: #21262d;
    border: none;
    max-height: 1px;
}

/* ===== Bottom Bar ===== */
#bottom_bar {
    background-color: #0d1117;
    border-top: 1px solid #21262d;
}

#status_bar_text {
    color: #6a737d;
    font-size: 11px;
    font-family: "Consolas", "Cascadia Code", monospace;
}

/* ===== Settings Tabs ===== */
QTabWidget::pane {
    border: 1px solid #21262d;
    border-radius: 0 6px 6px 6px;
    background-color: #161b22;
}

QTabBar::tab {
    background-color: #0d1117;
    color: #8b949e;
    border: 1px solid #21262d;
    border-bottom: none;
    padding: 8px 18px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: 13px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #161b22;
    color: #e6edf3;
    border-bottom: 1px solid #161b22;
}

QTabBar::tab:hover:!selected {
    background-color: #21262d;
    color: #e6edf3;
}

/* ===== Scrollbar ===== */
QScrollBar:vertical {
    background-color: #0d1117;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #30363d;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6a737d;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    height: 8px;
    background-color: #0d1117;
}

QScrollBar::handle:horizontal {
    background-color: #30363d;
    border-radius: 4px;
}

/* ===== Tooltip ===== */
QToolTip {
    background-color: #161b22;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 4px 8px;
}
"""
