# 3-Minute Demo Script — Day 15 Document Assistant

**Audience:** reviewer / cohort  
**Prereq:** `pip install -r requirements.txt`, then `python ingest.py`

---

### Minute 0:00–0:45 — What it is (45s)

> “This is a **retrieval-augmented** document assistant over **six internal markdown docs**. It does **vector search** in a local Chroma database, then either returns **quoted evidence with file-level citations**, or **refuses** when similarity is too weak—so we avoid confident wrong answers.”

**Show:** folder `documents/` with six files; mention topics (HR, product, safety, onboarding, API, glossary).

---

### Minute 0:45–1:45 — Live queries (60s)

Run:

```bash
python assistant.py
```

1. **In-corpus:**  
   *“What nominal DC voltage does Widget X require?”*  
   → Point out **bullets from the doc** + **Sources** line with `[02_product_specs.md — chunk …]`.

2. **Out-of-corpus:**  
   *“Who won the FIFA World Cup in 2022?”*  
   → Show the **graceful IDK** message (not in the knowledge base).

Type `quit`.

---

### Minute 1:45–2:45 — Quality evidence (60s)

Run:

```bash
python evaluate.py
```

> “Here are **10 scripted questions**: seven should be answered from the corpus with citations, three should trigger abstention. The script prints a **1–5 quality score** per question and writes `evaluation_results.json`.”

**Show:** mean score line + one row where `Expect IDK` vs `Got IDK` matches.

---

### Minute 2:45–3:00 — Close (15s)

> “Deliverables: **working RAG** in `rag_core.py` + `assistant.py`, **quality report** in `QUALITY_REPORT.md`, and this **3-minute demo** outline. Thresholds and tests live in code so we can iterate without changing the docs.”

---

**Stretch (if asked):** Open `rag_core.py` and point to `IDK_DISTANCE_THRESHOLD` and the `Sources:` formatter.
