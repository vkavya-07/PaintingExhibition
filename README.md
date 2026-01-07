# PaintingExhibition

Painting gallery REST API using FastAPI and SQLModel. Features role-based operations for `user` and `admin`.

Run locally:

- Install dependencies (pip or virtualenv)
- Start app: `uvicorn app.main:app --reload`
- Run tests: `pytest -q`

---

## Usage examples

List paintings (user):

curl -sX GET "http://localhost:8000/paintings/" -H "x-role: user"

Add a painting (admin):

curl -sX POST "http://localhost:8000/paintings/" -H "Content-Type: application/json" -H "x-role: admin" -d '{"createdBy":"Alice","size":"24x36","isAvailableForSale":true,"price":1000.0}'

Update painting (PUT, admin):

curl -sX PUT "http://localhost:8000/paintings/1" -H "Content-Type: application/json" -H "x-role: admin" -d '{"createdBy":"Alice","size":"30x40","isAvailableForSale":true,"price":1100.0}'

Patch painting (PATCH, admin):

curl -sX PATCH "http://localhost:8000/paintings/1" -H "Content-Type: application/json" -H "x-role: admin" -d '{"price":1200.0}'

Buy painting (PATCH by user):

curl -sX PATCH "http://localhost:8000/paintings/1/buy" -H "Content-Type: application/json" -H "x-role: user" -d '{"soldTo":"Dave","soldDate":"2024-01-01T12:00:00+00:00"}'

Query sold paintings (admin):

curl -sX GET "http://localhost:8000/paintings/sold?createdBy=Alice&min_price=500&sort_by=price" -H "x-role: admin"

---

## Health check

A lightweight health endpoint is available at `GET /health/` which returns JSON like `{"status": "ok", "uptime": 1.234}`. Tests include a healthcheck to ensure the endpoint is available in CI.

## Development & Git hooks

Install dev tools and enable pre-commit locally:

- python -m pip install -r dev-requirements.txt
- pre-commit install
- pre-commit run --all-files

Git / push helper (PowerShell): `scripts/publish_instructions.ps1` — run it after installing `git` and `gh` and configuring your GitHub CLI login.