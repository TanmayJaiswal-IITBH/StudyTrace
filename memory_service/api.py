"""FastAPI app: the HTTP surface of the memory service."""

from functools import lru_cache

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import Engine, create_engine, make_url, text
from sqlalchemy.exc import SQLAlchemyError

from memory_service.config import get_settings

app = FastAPI(title="StudyTrace memory service")


@lru_cache
def _engine(database_url: str) -> Engine:
    url = make_url(database_url)
    # A health probe must fail fast when the database host does not answer.
    connect_args = {"connect_timeout": 3} if url.get_backend_name() == "postgresql" else {}
    return create_engine(url, connect_args=connect_args)


@app.get("/health")
def health() -> JSONResponse:
    database_url = get_settings().database_url
    if database_url:
        try:
            with _engine(database_url).connect() as conn:
                conn.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return JSONResponse({"status": "error"}, status_code=503)
    return JSONResponse({"status": "ok"})
