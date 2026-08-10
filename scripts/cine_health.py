from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

required = [
    "package.json",
    "pnpm-workspace.yaml",
    "tsconfig.base.json",
    ".env.example",
    "apps/web/package.json",
    "apps/web/app/page.tsx",
    "services/agent-api/requirements.txt",
    "services/agent-api/app/main.py",
    "packages/contracts/package.json",
    "packages/agents/package.json",
    "packages/scenarios/package.json",
    "packages/core/package.json",
    "docs/cine/CINE001.md",
]

missing = [p for p in required if not (ROOT / p).exists()]

if missing:
    print("CINE001 FAILED")
    for item in missing:
        print(f"  MISSING: {item}")
    sys.exit(1)

print("CINE001 FOUNDATION CHECK: PASS")
print(f"Project root: {ROOT}")
print(f"Checked files: {len(required)}")
