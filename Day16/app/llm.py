"""
LLM adapter — stub implementation so the stack runs without API keys.
Swap `StubLLM` for a hosted model client in production.
"""
from __future__ import annotations


class StubLLM:
    """Deterministic stand-in for an LLM: grounds the reply in provided context only."""

    def complete(self, user_message: str, context_chunks: list[str]) -> str:
        if not context_chunks:
            return (
                "I could not find relevant passages in the vector index for this query. "
                "Please try a different wording or expand the knowledge base."
            )
        joined = " ".join(context_chunks)[:800]
        return (
            f"[StubLLM] Based on retrieved context: {joined}\n\n"
            f"Question addressed: {user_message.strip()[:200]}"
        )
