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
    """Wraps pyautogui with DPI-aware screenshot scaling."""

    def __init__(self):
        # Scale factors: multiply AI-image coords by these to get logical screen coords.
        # Updated every time take_screenshot_base64() is called.
        self.last_scale_x: float = 1.0
        self.last_scale_y: float = 1.0

    # ── Input ──────────────────────────────────────────────────────────
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

    # ── Screenshot ─────────────────────────────────────────────────────
    def take_screenshot(self) -> Image.Image:
        return pyautogui.screenshot()

    def take_screenshot_base64(self, max_width: int = 1280) -> str:
        """
        Capture the screen and return a base64-encoded PNG.

        Handles Windows DPI scaling: pyautogui.screenshot() returns physical
        pixels, but pyautogui.click() uses logical pixels.  We normalise the
        image to the logical resolution first so that coordinates the AI reads
        off the image map directly to what pyautogui.click() expects.

        self.last_scale_x / last_scale_y are set here and used by BufteaAI
        to convert any further AI-image coords → logical screen coords if the
        image was additionally downscaled for token efficiency.
        """
        img = self.take_screenshot()
        phys_w, phys_h = img.size

        # Step 1 — normalise to logical resolution (DPI fix)
        logical_w, logical_h = pyautogui.size()
        if phys_w != logical_w or phys_h != logical_h:
            img = img.resize((logical_w, logical_h), Image.LANCZOS)

        cur_w, cur_h = img.size  # now equals logical resolution

        # Step 2 — downscale for token efficiency
        if cur_w > max_width:
            ratio = max_width / cur_w
            img = img.resize((max_width, int(cur_h * ratio)), Image.LANCZOS)

        final_w, final_h = img.size

        # Store scale so BufteaAI can convert AI coords → screen coords
        self.last_scale_x = logical_w / final_w
        self.last_scale_y = logical_h / final_h

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    # ── App / system ───────────────────────────────────────────────────
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
            if system == "Linux":
                subprocess.Popen(["xdg-open", app_name])

    def medal_clip(self):
        pyautogui.hotkey("ctrl", "f8")

    def get_screen_size(self) -> tuple[int, int]:
        size = pyautogui.size()
        return size.width, size.height

    # ── Window management ──────────────────────────────────────────────
    def activate_window(self, title_substring: str) -> str:
        """Bring the first window whose title contains title_substring to focus."""
        try:
            import pygetwindow as gw
            matches = [w for w in gw.getAllWindows()
                       if title_substring.lower() in w.title.lower() and w.title.strip()]
            if not matches:
                return f"no window found matching '{title_substring}'"
            win = matches[0]
            try:
                win.restore()
            except Exception:
                pass
            win.activate()
            time.sleep(0.35)
            return f"focused: {win.title}"
        except ImportError:
            # pygetwindow not installed — fall back to Alt+Tab approach
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.3)
            return "focused (fallback: alt+tab)"
        except Exception as exc:
            return f"activate failed: {exc}"

    def get_open_windows(self) -> list[str]:
        """Return titles of all visible windows (excluding blank ones)."""
        try:
            import pygetwindow as gw
            return [w.title for w in gw.getAllWindows() if w.title.strip()]
        except Exception:
            return []
