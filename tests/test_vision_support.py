"""Unit tests for provider vision support metadata."""

import unittest

from core.providers.anthropic_provider import AnthropicProvider
from core.providers.local_provider import LocalProvider
from core.providers.openai_provider import OpenAIProvider


class TestVisionSupport(unittest.TestCase):
    def test_openai_supports_vision(self):
        self.assertTrue(OpenAIProvider("k").supports_vision())

    def test_anthropic_supports_vision(self):
        self.assertTrue(AnthropicProvider("k").supports_vision())

    def test_local_supports_vision(self):
        self.assertTrue(
            LocalProvider(
                "", base_url="http://127.0.0.1:1234/v1", model="local-model"
            ).supports_vision()
        )


if __name__ == "__main__":
    unittest.main()
