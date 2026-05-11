"""Vector DB (Chroma) — document chunks for RAG-style retrieval."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from chromadb.utils import embedding_functions

from app.config import settings

_COLLECTION = "day16_kb"


def _collection():
    path = Path(settings.chroma_path)
    path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(path))
    ef = embedding_functions.DefaultEmbeddingFunction()
    return client.get_or_create_collection(name=_COLLECTION, embedding_function=ef)


def seed_if_empty() -> int:
    coll = _collection()
    if coll.count() > 0:
        return 0
    docs = [
        (
            "policy-remote",
            "Remote work policy: engineers may work remotely up to three days per week.",
        ),
        (
            "policy-api",
            "API rate limits: 100 requests per minute per key for the public tier.",
        ),
        (
            "support-db",
            "PostgreSQL stores transactional data: users, billing, and audit logs.",
        ),
    ]
    ids, texts, metas = [], [], []
    for i, (doc_id, text) in enumerate(docs):
        ids.append(f"{doc_id}::{i}")
        texts.append(text)
        metas.append({"doc_id": doc_id})
    coll.add(ids=ids, documents=texts, metadatas=metas)
    return len(ids)


def search(query: str, k: int = 3) -> list[dict[str, Any]]:
    coll = _collection()
    res = coll.query(query_texts=[query], n_results=k)
    out: list[dict[str, Any]] = []
    if not res["documents"] or not res["documents"][0]:
        return out
    for doc, meta, dist in zip(
        res["documents"][0],
        res["metadatas"][0],
        res["distances"][0],
        strict=True,
    ):
        out.append(
            {
                "text": doc,
                "doc_id": meta.get("doc_id", "unknown"),
                "distance": float(dist),
            }
        )
    return out
