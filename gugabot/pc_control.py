import base64
import io
import os
import platform
import subprocess
import time

import pyautogui
from PIL import Image

# Move mouse to top-left corner to abort (safety)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25


class PCController:
    def click(self, x: int, y: int):
        pyautogui.click(x, y)
        time.sleep(0.1)

    def right_click(self, x: int, y: int):
        pyautogui.rightClick(x, y)
        time.sleep(0.1)

    def double_click(self, x: int, y: int):
        pyautogui.doubleClick(x, y)
        time.sleep(0.1)

    def move_to(self, x: int, y: int):
        pyautogui.moveTo(x, y, duration=0.3)

    def type_text(self, text: str, interval: float = 0.04):
        # typewrite has issues with unicode; use pyperclip + paste for reliability
        try:
            import pyperclip
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
        except ImportError:
            pyautogui.typewrite(text, interval=interval)

    def press_key(self, key: str):
        if "+" in key:
            parts = [p.strip() for p in key.split("+")]
            pyautogui.hotkey(*parts)
        else:
            pyautogui.press(key.strip())

    def scroll(self, x: int, y: int, direction: str, amount: int = 3):
        clicks = amount if direction == "up" else -amount
        pyautogui.scroll(clicks, x=x, y=y)

    def drag(self, x1: int, y1: int, x2: int, y2: int, duration: float = 0.5):
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, duration=duration, button="left")

    def take_screenshot(self) -> Image.Image:
        return pyautogui.screenshot()

    def take_screenshot_base64(self, max_width: int = 1280) -> str:
        img = self.take_screenshot()
        # Downscale if very large to save tokens
        w, h = img.size
        if w > max_width:
            ratio = max_width / w
            img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def open_app(self, app_name: str):
        system = platform.system()
        try:
            if system == "Windows":
                os.startfile(app_name)
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen([app_name])
        except (FileNotFoundError, OSError):
            # Try with 'xdg-open' on Linux
            if system == "Linux":
                subprocess.Popen(["xdg-open", app_name])

    def medal_clip(self):
        # Medal default clip hotkey — users can change in Medal settings
        pyautogui.hotkey("ctrl", "f8")

    def get_screen_size(self) -> tuple[int, int]:
        size = pyautogui.size()
        return size.width, size.height
