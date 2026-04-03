"""Unit tests for provider adapters (offline-safe)."""

import unittest

from core.providers.anthropic_provider import AnthropicProvider
from core.providers.openai_provider import OpenAIProvider


class TestProviders(unittest.TestCase):
    def test_openai_provider_metadata(self):
        provider = OpenAIProvider("test-key")
        self.assertEqual(provider.name, "OpenAI")
        self.assertTrue(provider.supports_vision())

    def test_anthropic_provider_metadata(self):
        provider = AnthropicProvider("test-key")
        self.assertEqual(provider.name, "Anthropic")
        self.assertTrue(provider.supports_vision())

    def test_openai_missing_sdk_graceful(self):
        provider = OpenAIProvider("test-key")
        response = provider.generate_tool_calls("make cube", [])
        # In CI/local this may fail due to missing sdk or bad key; both are acceptable
        self.assertFalse(response.success)

    def test_anthropic_missing_sdk_graceful(self):
        provider = AnthropicProvider("test-key")
        response = provider.generate_tool_calls("make cube", [])
        self.assertFalse(response.success)


if __name__ == "__main__":
    unittest.main()
