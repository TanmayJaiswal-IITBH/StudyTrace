import pytest
from pydantic import ValidationError

from memory_service.config import Settings


def test_model_ids_are_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MODEL_NANO")
    with pytest.raises(ValidationError, match="model_nano"):
        Settings(_env_file=None)


def test_secrets_never_appear_in_repr() -> None:
    settings = Settings(
        _env_file=None,
        nebius_api_key="sk-live-123",
        token_encryption_key="fernet-xyz",  # noqa: S106 (dummy value)
    )
    assert "sk-live-123" not in repr(settings)
    assert "fernet-xyz" not in repr(settings)
    assert settings.nebius_api_key.get_secret_value() == "sk-live-123"
