import queue
import threading
import time

from PyQt6.QtCore import QObject, pyqtSignal


class VoiceListener(QObject):
    wake_word_detected = pyqtSignal(str)   # "gugabot" | "guga_stop"
    command_detected = pyqtSignal(str)
    status_changed = pyqtSignal(str)

    WAKE_GUGABOT = ["gugabot", "guga bot", "guga-bot"]
    WAKE_STOP = ["guga stop", "gugabot stop", "stop guga"]

    def __init__(self):
        super().__init__()
        self.available = False
        self._enabled = False
        self._thread: threading.Thread | None = None
        self._sr = None
        self._recognizer = None
        self._check_deps()

    def _check_deps(self):
        try:
            import speech_recognition as sr
            import pyaudio  # noqa: F401 — just verify it's installed
            self._sr = sr
            self._recognizer = sr.Recognizer()
            self._recognizer.energy_threshold = 300
            self._recognizer.dynamic_energy_threshold = True
            self.available = True
        except ImportError:
            self.available = False

    # ------------------------------------------------------------------
    def start(self) -> bool:
        if not self.available or self._enabled:
            return self.available
        self._enabled = True
        self._thread = threading.Thread(target=self._loop, daemon=True, name="VoiceListener")
        self._thread.start()
        return True

    def stop(self):
        self._enabled = False

    # ------------------------------------------------------------------
    def _loop(self):
        sr = self._sr
        while self._enabled:
            try:
                with sr.Microphone() as source:
                    self._recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=6)
                text = self._recognizer.recognize_google(audio).lower().strip()
                self._handle_text(text)
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception:
                time.sleep(0.5)

    def _handle_text(self, text: str):
        for phrase in self.WAKE_STOP:
            if phrase in text:
                self.wake_word_detected.emit("guga_stop")
                return

        for phrase in self.WAKE_GUGABOT:
            if phrase in text:
                self.wake_word_detected.emit("gugabot")
                self.status_changed.emit("Listening for command…")
                self._listen_for_command()
                return

    def _listen_for_command(self):
        sr = self._sr
        try:
            with sr.Microphone() as source:
                audio = self._recognizer.listen(source, timeout=8, phrase_time_limit=12)
            text = self._recognizer.recognize_google(audio)
            if text:
                self.command_detected.emit(text)
        except Exception:
            pass
        finally:
            self.status_changed.emit("")
