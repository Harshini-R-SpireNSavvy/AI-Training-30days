# Day 15 — MINI PROJECT: Document Assistant (5+ docs)

Self-contained **RAG prototype** over six markdown files with **citations**, **graceful “I don’t know”** behavior, and a **10-question evaluation** with numeric quality scores.

## Quick start

```bash
cd Day15
pip install -r requirements.txt
python ingest.py
python assistant.py
```

## Evaluation & report

```bash
python evaluate.py
```

- Writes `evaluation_results.json` (full answers + scores).
- Patches the auto table in `QUALITY_REPORT.md` between the `AUTO_TABLE` markers.

## Deliverables checklist

| Deliverable | Location |
|-------------|----------|
| Working RAG prototype | `rag_core.py`, `ingest.py`, `assistant.py`, `chroma_db/` (after ingest) |
| Quality report | `QUALITY_REPORT.md` + `evaluation_results.json` |
| 3-minute demo | `DEMO_SCRIPT.md` |

## Project layout

- `documents/` — knowledge base (6 `.md` files).
- `rag_core.py` — chunking, ingest, retrieve, IDK gate, cited answers.
- `ingest.py` — CLI to rebuild the index.
- `assistant.py` — interactive Q&A.
- `evaluate.py` — 10 test questions with 1–5 scores.

## Note

First `ingest.py` run may download the default embedding model used by Chroma; requires network once.
