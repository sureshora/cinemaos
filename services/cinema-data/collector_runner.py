from __future__ import annotations
import importlib
import json
from pathlib import Path
from typing import Any
from .pipeline import merge_artist_records, normalize_records

def run_collectors(module_names: list[str]) -> list[dict[str, Any]]:
    records=[]
    for module_name in module_names:
        module=importlib.import_module(module_name)
        collect=getattr(module,"collect",None)
        if not callable(collect):
            raise TypeError(f"{module_name} must expose collect()")
        records.extend(normalize_records(collect(), getattr(module,"name",module_name)))
    return merge_artist_records(records)

def write_json(records: list[dict[str, Any]], path: str | Path) -> Path:
    target=Path(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    return target
