import json
import re
import threading

from openai import OpenAI

from gugabot.config import Config
from gugabot.logger import ActivityLogger


class BaseAI:
    def __init__(self, config: Config, logger: ActivityLogger):
        self.config = config
        self.logger = logger
        self._client: OpenAI | None = None
        self._stop_event = threading.Event()
        self._refresh_client()

    # ------------------------------------------------------------------
    def _refresh_client(self):
        api_key = self.config.get("api_key", "")
        if api_key:
            self._client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/skimosk/gugabot",
                    "X-Title": "GugaBot",
                },
            )
        else:
            self._client = None

    def update_client(self):
        self._refresh_client()

    # ------------------------------------------------------------------
    @property
    def is_running(self) -> bool:
        return not self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    def _reset_stop(self):
        self._stop_event.clear()

    # ------------------------------------------------------------------
    def _parse_action(self, text: str) -> dict:
        """Extract the first JSON object from the model's response."""
        # Strip markdown code fences
        text = text.strip()
        for fence in ("```json", "```"):
            if fence in text:
                parts = text.split(fence)
                for part in parts[1:]:
                    candidate = part.split("```")[0].strip()
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        pass

        # Try raw JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find a JSON object anywhere in the text
        match = re.search(r"\{[\s\S]*?\}", text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # Fallback: treat whole response as a "speak" action
        return {"action": "speak", "text": text, "description": text}

    # ------------------------------------------------------------------
    def _record_usage(self, agent_key: str, usage):
        if usage:
            self.config.add_usage(
                agent_key,
                getattr(usage, "prompt_tokens", 0),
                getattr(usage, "completion_tokens", 0),
            )
