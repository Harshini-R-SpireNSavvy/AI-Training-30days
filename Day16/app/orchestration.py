"""Python AI backend: orchestrates Vector DB retrieval + LLM + persistence contract."""
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.db import save_turn
from app.llm import StubLLM
from app.vector_store import search

_llm = StubLLM()


def run_chat_pipeline(session: Session, user_message: str) -> dict[str, Any]:
    hits = search(user_message, k=3)
    chunks = [h["text"] for h in hits]
    answer = _llm.complete(user_message, chunks)
    turn_id = str(uuid.uuid4())
    save_turn(
        session,
        turn_id=turn_id,
        user_message=user_message,
        assistant_message=answer,
        sources=hits,
    )
    return {
        "id": turn_id,
        "answer": answer,
        "retrieval": hits,
    }
