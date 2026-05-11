#!/usr/bin/env python3
"""Build / refresh the local vector index from Day15/documents."""
from pathlib import Path

from rag_core import ingest_documents

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "documents"
CHROMA = ROOT / "chroma_db"


def main() -> None:
    n = ingest_documents(DOCS, CHROMA)
    print(f"Ingested {n} chunks from {DOCS} into {CHROMA}")


if __name__ == "__main__":
    main()
