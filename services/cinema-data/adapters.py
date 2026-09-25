from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class SourceAdapter:
    name: str
    collect_fn: Callable[[], list[dict[str, Any]]]

    def collect(self) -> list[dict[str, Any]]:
        return self.collect_fn()


def adapter_from_module(module_path: str) -> SourceAdapter:
    """Wrap an existing Python collector module without changing its code."""
    module = importlib.import_module(module_path)
    collect = getattr(module, "collect", None)
    if not callable(collect):
        raise TypeError(f"{module_path} must expose collect()")
    name = getattr(module, "name", module_path.rsplit(".", 1)[-1])
    return SourceAdapter(name=name, collect_fn=collect)


def collect_from_modules(module_paths: list[str]) -> list[dict[str, Any]]:
    """Collect raw records from multiple legacy/source modules."""
    records: list[dict[str, Any]] = []
    for module_path in module_paths:
        records.extend(adapter_from_module(module_path).collect())
    return records
