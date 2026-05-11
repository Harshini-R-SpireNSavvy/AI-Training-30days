"""
Day 15 — minimal RAG core: Chroma persistence, chunking, retrieval, citations, IDK gate.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
from chromadb.utils import embedding_functions

# Chroma default embedding distances are not 0–1 across all models; tune on the
# held-out questions in evaluate.py so in-corpus Q&A clears while OOD stays IDK.
IDK_DISTANCE_THRESHOLD = 1.05
TOP_K = 4


@dataclass
class CitedPassage:
    source: str
    chunk_index: int
    text: str
    distance: float


@dataclass
class RAGAnswer:
    text: str
    citations: list[CitedPassage]
    is_idk: bool
    best_distance: float | None


def _default_collection(chroma_dir: Path, collection_name: str = "day15_kb"):
    chroma_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(chroma_dir))
    ef = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(name=collection_name, embedding_function=ef)


def chunk_markdown(text: str, max_chars: int = 450, overlap: int = 60) -> list[str]:
    """Split on paragraphs, then hard-wrap long blocks for embedding."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    for para in paragraphs:
        if len(para) <= max_chars:
            chunks.append(para)
            continue
        start = 0
        while start < len(para):
            end = min(start + max_chars, len(para))
            chunks.append(para[start:end].strip())
            start = end - overlap if end < len(para) else len(para)
    return chunks


def ingest_documents(
    docs_dir: Path,
    chroma_dir: Path,
    collection_name: str = "day15_kb",
) -> int:
    coll = _default_collection(chroma_dir, collection_name)
    existing = coll.get()
    if existing and existing.get("ids"):
        coll.delete(ids=existing["ids"])

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict[str, Any]] = []

    md_files = sorted(docs_dir.glob("*.md"))
    for path in md_files:
        raw = path.read_text(encoding="utf-8")
        parts = chunk_markdown(raw)
        for i, chunk in enumerate(parts):
            cid = f"{path.name}::{i}"
            ids.append(cid)
            documents.append(chunk)
            metadatas.append({"source": path.name, "chunk_index": i})

    if not ids:
        return 0

    coll.add(ids=ids, documents=documents, metadatas=metadatas)
    return len(ids)


def retrieve(
    query: str,
    chroma_dir: Path,
    collection_name: str = "day15_kb",
    k: int = TOP_K,
) -> list[CitedPassage]:
    coll = _default_collection(chroma_dir, collection_name)
    res = coll.query(query_texts=[query], n_results=k)
    out: list[CitedPassage] = []
    if not res["documents"] or not res["documents"][0]:
        return out
    for doc, meta, dist in zip(
        res["documents"][0],
        res["metadatas"][0],
        res["distances"][0],
        strict=True,
    ):
        out.append(
            CitedPassage(
                source=str(meta["source"]),
                chunk_index=int(meta["chunk_index"]),
                text=str(doc),
                distance=float(dist),
            )
        )
    return out


IDK_MESSAGE = (
    "I do not have enough information in the provided documents to answer that "
    "confidently. If this is important, try rephrasing or ask about topics covered "
    "in the handbook, product specs, safety, onboarding, API reference, or glossary."
)


def compose_answer(
    query: str,
    passages: list[CitedPassage],
    distance_threshold: float = IDK_DISTANCE_THRESHOLD,
) -> RAGAnswer:
    if not passages:
        return RAGAnswer(text=IDK_MESSAGE, citations=[], is_idk=True, best_distance=None)

    best = passages[0]
    if best.distance > distance_threshold:
        return RAGAnswer(
            text=IDK_MESSAGE,
            citations=passages,
            is_idk=True,
            best_distance=best.distance,
        )

    best_d = best.distance
    used: list[CitedPassage] = [best]
    for p in passages[1:]:
        if len(used) >= 3:
            break
        if p.source != best.source:
            continue
        if p.distance <= best_d + 0.35:
            used.append(p)
    lines: list[str] = []
    lines.append("Here is what the indexed documents support:")
    for p in used:
        snippet = p.text.replace("\n", " ").strip()
        if len(snippet) > 320:
            snippet = snippet[:317] + "..."
        lines.append(f"- {snippet}")
    lines.append("")
    lines.append("Sources:")
    for p in used:
        lines.append(f"  • [{p.source} — chunk {p.chunk_index}] (relevance distance {p.distance:.3f})")

    body = "\n".join(lines)
    return RAGAnswer(
        text=body,
        citations=used,
        is_idk=False,
        best_distance=best.distance,
    )


def ask(
    query: str,
    chroma_dir: Path,
    collection_name: str = "day15_kb",
    distance_threshold: float = IDK_DISTANCE_THRESHOLD,
) -> RAGAnswer:
    passages = retrieve(query, chroma_dir, collection_name)
    return compose_answer(query, passages, distance_threshold=distance_threshold)
