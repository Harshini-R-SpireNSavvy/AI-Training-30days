"""PostgreSQL or SQLite via SQLAlchemy (architecture targets Postgres; SQLite for quick Postman runs)."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Generator

from sqlalchemy import DateTime, String, Text, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


class ChatTurn(Base):
    __tablename__ = "chat_turns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_message: Mapped[str] = mapped_column(Text)
    assistant_message: Mapped[str] = mapped_column(Text)
    retrieval_sources_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


def _engine_kwargs(url: str) -> dict:
    if url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {}


engine = create_engine(settings.database_url, **_engine_kwargs(settings.database_url))
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_turn(
    session: Session,
    turn_id: str,
    user_message: str,
    assistant_message: str,
    sources: list[dict],
) -> None:
    row = ChatTurn(
        id=turn_id,
        user_message=user_message,
        assistant_message=assistant_message,
        retrieval_sources_json=json.dumps(sources),
    )
    session.add(row)
    session.commit()
