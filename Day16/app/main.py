from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db import get_session, init_db
from app.orchestration import run_chat_pipeline
from app.vector_store import seed_if_empty


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    seed_if_empty()
    yield


app = FastAPI(
    title="Day 16 AI Stack API",
    version="1.0.0",
    description="User → Frontend → API → Python AI backend → LLM + Vector DB + PostgreSQL (SQLite dev).",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    id: str
    answer: str
    retrieval: list[dict]


@app.get("/health")
def health():
    return {"status": "ok", "service": "day16-api"}


@app.post("/v1/chat", response_model=ChatResponse)
def chat(body: ChatRequest, db: Session = Depends(get_session)):
    return run_chat_pipeline(db, body.message)
