import json
import os
from pathlib import Path


class Config:
    DEFAULT_SETTINGS = {
        "api_key": "",
        "ancuta_model": "google/gemini-flash-1.5",
        "buftea_model": "google/gemini-2.5-pro",
        "screenshot_interval": 10,
        "voice_enabled": True,
        "theme": "dark",
        "usage": {
            "ancuta": {"tokens_in": 0, "tokens_out": 0, "requests": 0},
            "buftea": {"tokens_in": 0, "tokens_out": 0, "requests": 0},
        },
    }

    def __init__(self):
        self.config_path = Path.home() / ".gugabot" / "settings.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings = self._load()

    def _load(self) -> dict:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                merged = self._deep_merge(self.DEFAULT_SETTINGS.copy(), data)
                return merged
            except (json.JSONDecodeError, OSError):
                pass
        return self._deep_copy(self.DEFAULT_SETTINGS)

    def _deep_copy(self, d: dict) -> dict:
        import copy
        return copy.deepcopy(d)

    def _deep_merge(self, base: dict, override: dict) -> dict:
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def save(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except OSError:
            pass

    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value):
        self.settings[key] = value
        self.save()

    def add_usage(self, agent: str, tokens_in: int, tokens_out: int):
        usage = self.settings.setdefault("usage", {})
        agent_usage = usage.setdefault(agent, {"tokens_in": 0, "tokens_out": 0, "requests": 0})
        agent_usage["tokens_in"] += tokens_in
        agent_usage["tokens_out"] += tokens_out
        agent_usage["requests"] += 1
        self.save()

    def reset_usage(self):
        self.settings["usage"] = {
            "ancuta": {"tokens_in": 0, "tokens_out": 0, "requests": 0},
            "buftea": {"tokens_in": 0, "tokens_out": 0, "requests": 0},
        }
        self.save()
