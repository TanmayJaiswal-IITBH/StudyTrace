import pytest
from fastapi.testclient import TestClient

from memory_service.api import app


def test_health_reports_ok_when_database_is_reachable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    resp = TestClient(app).get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_is_503_when_database_is_unreachable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@127.0.0.1:1/db")
    resp = TestClient(app).get("/health")
    assert resp.status_code == 503
    assert resp.json() == {"status": "error"}
