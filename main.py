#!/usr/bin/env python3
"""
GugaBot — Jarvis-like AI desktop assistant.

Usage:
    python main.py

Dependencies (install with: pip install -r requirements.txt):
    PyQt6, openai, pyautogui, Pillow, SpeechRecognition, pyaudio, pynput
"""

import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from gugabot.config import Config
from gugabot.logger import ActivityLogger
from gugabot.voice import VoiceListener
from gugabot.ai.ancuta import AncutaAI
from gugabot.ai.buftea import BufteaAI
from gugabot.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("GugaBot")
    app.setApplicationDisplayName("GugaBot")
    app.setOrganizationName("skimosk")

    # Shared services
    config = Config()
    logger = ActivityLogger()
    voice = VoiceListener()
    ancuta = AncutaAI(config, logger)
    buftea = BufteaAI(config, logger)

    window = MainWindow(config, logger, ancuta, buftea, voice)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
