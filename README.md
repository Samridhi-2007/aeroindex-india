# AeroIndex India Monorepo (SIH26056)

Production-structured monorepo scaffold for fare intelligence workflows.

## Monorepo Structure

- `frontend/` — React + TypeScript + Vite + Tailwind app shell
- `backend/` — FastAPI + PostgreSQL service scaffold
- `intelligence/` — modular analysis engines (`apix_engine`, `quality`, `anomaly`, `backtesting`)
- `data/demo/` — placeholder demo airfare JSON
- `docs/` — architecture and API contract docs
- `tests/` — test suites (unit/integration/e2e placeholders)

## Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health endpoint:

- `GET http://127.0.0.1:8000/health`

## Notes

- This is an integration-ready scaffold only.
- No real scraping, anomaly logic, or business rules are implemented yet.
- Secrets are never hardcoded; use environment variables.
