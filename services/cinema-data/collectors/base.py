from __future__ import annotations
from typing import Any, Protocol

class Collector(Protocol):
    name: str
    def collect(self) -> list[dict[str, Any]]:
        ...
