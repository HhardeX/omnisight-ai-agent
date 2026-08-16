from app.services.providers.null_vlm import NullVLMProvider
from app.services.vlm import VLMProvider


def create_vlm_provider() -> VLMProvider:
    """Create the configured VLM provider."""
    return NullVLMProvider()