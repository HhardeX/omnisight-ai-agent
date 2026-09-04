import pytest

from app.core.config import settings
from app.services.providers.factory import create_vlm_provider
from app.services.providers.null_vlm import NullVLMProvider
from app.services.providers.ollama_vlm import OllamaVLMProvider


def test_factory_creates_null_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "vlm_provider", "null")

    provider = create_vlm_provider()

    assert isinstance(provider, NullVLMProvider)


def test_factory_creates_ollama_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "vlm_provider", "ollama")
    monkeypatch.setattr(settings, "vlm_model", "qwen2.5vl:3b")

    provider = create_vlm_provider()

    assert isinstance(provider, OllamaVLMProvider)
    assert provider.model == "qwen2.5vl:3b"


def test_factory_rejects_unsupported_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "vlm_provider", "unsupported")

    with pytest.raises(ValueError, match="Unsupported VLM provider"):
        create_vlm_provider()
