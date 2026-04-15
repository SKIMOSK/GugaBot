"""
Simple tone-based sound effects for GugaBot.
Pure Python + pyaudio — no extra audio files needed.
If pyaudio is not installed, all methods silently no-op.
"""

import math
import struct
import threading

try:
    import pyaudio as _pyaudio
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False


class SoundManager:
    """Generates and plays short synthesised tones asynchronously."""

    RATE = 22_050  # Hz — good enough for tones

    def __init__(self):
        self.enabled = True

    # ------------------------------------------------------------------
    def _play(self, tones: list[tuple], duration: float, vol: float = 0.28):
        """
        tones : list of (freq_hz, t_start_sec, t_end_sec)
        Each tone segment is mixed together with a short linear fade-in/out.
        """
        if not _AVAILABLE or not self.enabled:
            return

        def _run():
            n = int(self.RATE * duration)
            samples = []
            for i in range(n):
                t = i / self.RATE
                s = 0.0
                for freq, t0, t1 in tones:
                    if t0 <= t <= t1:
                        seg = t1 - t0
                        fade = min((t - t0) / max(seg * 0.08, 0.005), 1.0,
                                   (t1 - t) / max(seg * 0.08, 0.005))
                        s += vol * fade * math.sin(2.0 * math.pi * freq * t)
                samples.append(max(-1.0, min(1.0, s)))

            raw = struct.pack(f"<{len(samples)}f", *samples)
            try:
                pa = _pyaudio.PyAudio()
                stream = pa.open(
                    format=_pyaudio.paFloat32,
                    channels=1,
                    rate=self.RATE,
                    output=True,
                )
                stream.write(raw)
                stream.stop_stream()
                stream.close()
                pa.terminate()
            except Exception:
                pass

        threading.Thread(target=_run, daemon=True, name="SoundFX").start()

    # ------------------------------------------------------------------
    # Named sounds
    # ------------------------------------------------------------------

    def wake(self):
        """Ascending two-tone chime — wake word detected."""
        self._play([(440, 0.00, 0.12), (660, 0.10, 0.26)], 0.30, vol=0.26)

    def action(self):
        """Tiny high tick — each discrete action executed."""
        self._play([(1_100, 0.00, 0.055)], 0.065, vol=0.14)

    def done(self):
        """Three-note ascending fanfare — task completed successfully."""
        self._play(
            [(523, 0.00, 0.12), (659, 0.10, 0.22), (784, 0.20, 0.42)],
            0.46, vol=0.26,
        )

    def error(self):
        """Falling two-note tone — error / failure."""
        self._play([(440, 0.00, 0.16), (330, 0.13, 0.34)], 0.38, vol=0.30)

    def confirm(self):
        """Double pulse alert — dangerous action needs confirmation."""
        self._play([(880, 0.00, 0.08), (880, 0.13, 0.21)], 0.28, vol=0.22)

    def stop(self):
        """Low thud — AI forcefully stopped."""
        self._play([(160, 0.00, 0.20)], 0.24, vol=0.38)
