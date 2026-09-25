from __future__ import annotations
from typing import Any, Protocol

class CinemaCollector(Protocol):
    name: str
    def collect(self) -> list[dict[str, Any]]:
        """Return normalized, source-aware records."""
        ...
