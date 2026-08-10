# CINE001 Verification

## Static

Run:

```bash
pnpm cine:health
```

Expected:

```text
CINE001 FOUNDATION CHECK: PASS
```

## Frontend

```bash
pnpm install
pnpm --filter @cinemaos/web typecheck
pnpm --filter @cinemaos/web build
```

## API

```bash
cd services/agent-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Then:

```bash
curl http://localhost:8080/health
```

Expected JSON contains:

```json
{
  "status": "ok",
  "service": "cinemaos-agent-api",
  "milestone": "CINE001"
}
```
