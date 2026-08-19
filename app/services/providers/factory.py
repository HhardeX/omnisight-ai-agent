from app.core.config import settings
from app.services.providers.null_vlm import NullVLMProvider
from app.services.providers.ollama_vlm import OllamaVLMProvider
from app.services.vlm import VLMProvider


def create_vlm_provider() -> VLMProvider:
    """Create the configured VLM provider."""

    if settings.vlm_provider == "null":
        return NullVLMProvider()

    if settings.vlm_provider == "ollama":
        if settings.vlm_model:
            return OllamaVLMProvider(model=settings.vlm_model)
        return OllamaVLMProvider()

    raise ValueError(
        f"Unsupported VLM provider: {settings.vlm_provider}"
    )#