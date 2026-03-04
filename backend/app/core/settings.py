from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    max_items_per_source: int = int(os.getenv("JARVIS_MAX_ITEMS_PER_SOURCE", "20"))
    request_timeout_seconds: int = int(os.getenv("JARVIS_REQUEST_TIMEOUT_SECONDS", "10"))
    user_agent: str = os.getenv("JARVIS_USER_AGENT", "jarvis-intelligence-bot/1.0")


settings = Settings()
