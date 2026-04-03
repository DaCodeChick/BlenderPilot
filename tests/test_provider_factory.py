"""Unit tests for provider factory across cloud and local providers."""

import unittest

from core.provider_factory import create_provider
from core.providers.anthropic_provider import AnthropicProvider
from core.providers.local_provider import LocalProvider
from core.providers.openai_provider import OpenAIProvider


class _Prefs:
    use_env_file = False
    openai_api_key = "sk-test"
    anthropic_api_key = "sk-ant-test"
    local_api_key = ""
    local_model = "local-model"
    local_base_url = "http://127.0.0.1:1234/v1"


class TestProviderFactory(unittest.TestCase):
    def setUp(self):
        self.prefs = _Prefs()

    def test_openai_provider(self):
        provider = create_provider("openai", self.prefs)
        self.assertIsInstance(provider, OpenAIProvider)

    def test_anthropic_provider(self):
        provider = create_provider("anthropic", self.prefs)
        self.assertIsInstance(provider, AnthropicProvider)

    def test_local_provider(self):
        provider = create_provider("local", self.prefs)
        self.assertIsInstance(provider, LocalProvider)


if __name__ == "__main__":
    unittest.main()
