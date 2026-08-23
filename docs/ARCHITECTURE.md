# AeroIndex India - Architecture

## Overview

AeroIndex India is organized as a modular monorepo to enable independent development and deployment of:

1. **Frontend** (React + TS + Vite + Tailwind)
2. **Backend API** (FastAPI + PostgreSQL)
3. **Intelligence modules** (analytics and signal engines)

## Top-Level Layout

- `frontend/` UI layer for dashboards and operator workflows
- `backend/` API and orchestration layer
- `intelligence/` pluggable computation modules
- `data/demo/` sample datasets for local development
- `docs/` design and contracts
- `tests/` system-wide tests

## Backend Layering

`backend/app/` follows clean module boundaries:

- `api/` route registration and endpoint handlers
- `models/` SQLAlchemy models
- `schemas/` Pydantic request/response models
- `services/` business/service orchestration (placeholder)
- `db/` engine/session/base
- `core/` settings, shared configs, constants

## Intelligence Layer

`intelligence/modules/` isolates engines so each can evolve independently:

- `apix_engine/`
- `quality/`
- `anomaly/`
- `backtesting/`

Each module exposes a minimal `service.py`/`__init__.py` placeholder today and can later be promoted to package-level APIs.

## Data Flow (Target State)

1. Frontend calls Backend API
2. Backend validates payloads and orchestrates services
3. Services invoke relevant Intelligence modules
4. Results persisted in PostgreSQL and returned to frontend

## Non-Goals (Current Scaffold)

- No live airline scraping
- No production anomaly/business heuristics
- No cron scheduling/worker pipelines yet
