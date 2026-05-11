# Day 15 — Document Assistant: Quality Report

## Scope

- **Corpus:** 6 markdown documents under `documents/` (handbook, product specs, safety, onboarding, API reference, glossary).
- **Pipeline:** Chunking → Chroma persistent store with default embeddings → top-k retrieval → distance-based **abstention** (“I don’t know”) → cited extractive answer from accepted chunks.

## Design choices

1. **Citations:** Every non-IDK answer ends with a **Sources** list pointing to `[filename — chunk N]` and embedding distance as a transparency aid for reviewers.
2. **Graceful IDK:** If the best retrieved chunk’s distance exceeds `IDK_DISTANCE_THRESHOLD` in `rag_core.py`, the assistant returns a fixed, user-safe message instead of guessing.
3. **No external LLM:** Keeps the prototype runnable offline after ingest; generation is **grounded extraction** from retrieved text only, which reduces unsupported invention.

## Aggregate metrics (after `python evaluate.py`)

Run the evaluator locally, then read `evaluation_results.json` or the auto-generated table below.

<!-- AUTO_TABLE_START -->

| Q | Expect IDK | Got IDK | Score (1–5) | Best distance | Notes |
|---|------------|---------|---------------|---------------|-------|
| Q1 | False | False | 5 | 0.484 | Grounded answer with citations and key facts. |
| Q2 | False | False | 5 | 0.464 | Grounded answer with citations and key facts. |
| Q3 | False | False | 5 | 0.439 | Grounded answer with citations and key facts. |
| Q4 | False | False | 5 | 0.607 | Grounded answer with citations and key facts. |
| Q5 | False | False | 5 | 1.016 | Grounded answer with citations and key facts. |
| Q6 | False | False | 5 | 0.863 | Grounded answer with citations and key facts. |
| Q7 | False | False | 5 | 0.790 | Grounded answer with citations and key facts. |
| Q8 | True | True | 5 | 1.823 | Correctly abstained with IDK-style response. |
| Q9 | True | True | 5 | 1.533 | Correctly abstained with IDK-style response. |
| Q10 | False | False | 5 | 0.262 | Grounded answer with citations and key facts. |

_JSON metrics: `evaluation_results.json`_
<!-- AUTO_TABLE_END -->

## Interpretation guide

| Score | Meaning |
|-------|---------|
| 5 | Expected behavior: grounded answer with citations, or correct abstention. |
| 3 | Partial: missing keyword or weak citation linkage. |
| 2 | Serious miss: wrong abstention or failure to abstain on out-of-corpus questions. |
| 1 | (Reserved) total failure — not observed in default benchmark. |

## Risks and next steps

- **Threshold sensitivity:** The IDK gate is a single global distance cutoff; production systems often use calibrated per-topic thresholds or a cross-encoder reranker.
- **Synthesis:** Without an LLM, answers are excerpt-style; adding a small local model with strict “cite-only” prompting would improve fluency while keeping grounding.
