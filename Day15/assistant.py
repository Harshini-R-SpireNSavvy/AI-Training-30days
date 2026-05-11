#!/usr/bin/env python3
"""
Interactive document assistant (RAG prototype).
Run: python ingest.py  then  python assistant.py
"""
from pathlib import Path

from rag_core import ask

ROOT = Path(__file__).resolve().parent
CHROMA = ROOT / "chroma_db"


def main() -> None:
    if not CHROMA.exists():
        print("Index not found. Run: python ingest.py")
        return
    print("Day 15 Document Assistant — type 'quit' to exit.\n")
    while True:
        q = input("Question: ").strip()
        if not q:
            continue
        if q.lower() in {"quit", "exit", "q"}:
            break
        ans = ask(q, CHROMA)
        print("\n" + ans.text + "\n")
        if ans.is_idk:
            print("(Returned graceful IDK / low-confidence response.)\n")


if __name__ == "__main__":
    main()
