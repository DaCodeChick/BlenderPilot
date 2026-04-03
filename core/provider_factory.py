"""Factory for constructing provider adapters from addon preferences."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from .provider_interface import ProviderInterface
from .providers.anthropic_provider import AnthropicProvider
from .providers.openai_provider import OpenAIProvider


def _load_env_file() -> None:
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def _pick_api_key(provider_name: str, prefs) -> Optional[str]:
    if provider_name == "openai":
        return prefs.openai_api_key or os.environ.get("OPENAI_API_KEY")
    if provider_name == "anthropic":
        return prefs.anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
    return None


def create_provider(provider_name: str, prefs) -> ProviderInterface:
    """Instantiate provider from name and user preferences."""
    if prefs.use_env_file:
        _load_env_file()

    api_key = _pick_api_key(provider_name, prefs)
    if not api_key:
        raise ValueError(f"Missing API key for provider: {provider_name}")

    kwargs = {
        "model": "gpt-4.1-mini"
        if provider_name == "openai"
        else "claude-3-5-haiku-latest"
    }
    if provider_name == "openai":
        return OpenAIProvider(api_key, **kwargs)
    if provider_name == "anthropic":
        return AnthropicProvider(api_key, **kwargs)
    raise ValueError(f"Unsupported provider: {provider_name}")
