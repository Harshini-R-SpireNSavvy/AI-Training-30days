# Day 16 — Architecture + FastAPI + Postman

> **Note:** The assignment is **Day 16**. A **Day16** folder is used here (Day 15 is already the RAG mini-project).

## Expected deliverables

| Deliverable | Location |
|-------------|----------|
| Architecture diagram + written flow | `ARCHITECTURE.md` |
| FastAPI API | `app/main.py` (`GET /health`, `POST /v1/chat`) |
| Postman tests | `postman/Day16-API.postman_collection.json` |

## Stack (conceptual)

**User → Frontend → API (FastAPI) → Python AI backend → LLM + Vector DB (Chroma) + PostgreSQL**

- **Dev default:** SQLite file `day16_local.db` so you can hit the API immediately.
- **Prod-shaped:** set `DATABASE_URL` to PostgreSQL (see `docker-compose.yml`).

## Run the API

From this folder (`Day16`):

```powershell
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Postman

1. Postman → **Import** → choose `postman/Day16-API.postman_collection.json`.
2. Collection variable **`base_url`** defaults to `http://127.0.0.1:8000`.
3. Run **Health**, then **Chat** requests. Expect `200` and JSON with `id`, `answer`, `retrieval`.

## PostgreSQL (optional)

```powershell
docker compose up -d
```

Copy `.env.example` to `.env` and use the **postgresql** `DATABASE_URL` line from the comments inside `.env.example`. Restart uvicorn; tables are created on startup.

## Layout

- `app/main.py` — routes  
- `app/orchestration.py` — retrieve → LLM → save turn  
- `app/vector_store.py` — Chroma  
- `app/llm.py` — stub LLM (no API key)  
- `app/db.py` — SQLAlchemy models + session  
