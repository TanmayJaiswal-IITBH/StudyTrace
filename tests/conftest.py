"""Test setup: dummy settings so no real .env, database or model call is ever needed."""

import os
from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest

os.environ["MODEL_NANO"] = "test-nano"
os.environ["MODEL_SUPER"] = "test-super"
os.environ["MODEL_ULTRA"] = "test-ultra"
# A developer's .env must never point the suite at a real database or key.
os.environ["DATABASE_URL"] = ""
os.environ["NEBIUS_API_KEY"] = ""

from memory_service.config import get_settings  # noqa: E402  (after the env is set)


@pytest.fixture(autouse=True)
def _fresh_settings() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_llm() -> MagicMock:
    """Placeholder for the llm.py mock; Oct 13 patches the real gateway here."""
    return MagicMock(name="llm")
