from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal


class ActivityLogger(QObject):
    log_added = pyqtSignal(str, str, str)  # timestamp, level, message

    LEVELS = {"info", "action", "response", "error", "wake", "system"}

    def __init__(self):
        super().__init__()
        self._entries: list[dict] = []

    def log(self, message: str, level: str = "info"):
        if level not in self.LEVELS:
            level = "info"
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {"timestamp": timestamp, "level": level, "message": message}
        self._entries.append(entry)
        self.log_added.emit(timestamp, level, message)

    def get_all(self) -> list[dict]:
        return list(self._entries)

    def clear(self):
        self._entries.clear()
