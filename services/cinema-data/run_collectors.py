from __future__ import annotations
import argparse
from pathlib import Path
from .collector_runner import run_collectors, write_json

parser=argparse.ArgumentParser(description="Run CinemaOS cinema-data collectors")
parser.add_argument("modules", nargs="+", help="Python module paths exposing collect()")
parser.add_argument("--output", default="apps/cinema-intelligence/data/collected_artists.json")
args=parser.parse_args()

records=run_collectors(args.modules)
target=write_json(records,args.output)
print(f"COLLECTION COMPLETE: {len(records)} artist records -> {target}")
