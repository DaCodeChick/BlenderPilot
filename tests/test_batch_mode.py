"""Unit tests for batch prompt parsing behavior."""

import unittest


def _parse_batch(prompt: str, enabled: bool, max_items: int):
    if not enabled:
        return [prompt]
    prompts = [line.strip() for line in prompt.splitlines() if line.strip()]
    return prompts[:max_items]


class TestBatchMode(unittest.TestCase):
    def test_single_mode_keeps_prompt(self):
        data = _parse_batch("a\nb", enabled=False, max_items=5)
        self.assertEqual(data, ["a\nb"])

    def test_batch_mode_splits_lines(self):
        data = _parse_batch("a\n\n b \n", enabled=True, max_items=5)
        self.assertEqual(data, ["a", "b"])

    def test_batch_mode_respects_limit(self):
        data = _parse_batch("a\nb\nc", enabled=True, max_items=2)
        self.assertEqual(data, ["a", "b"])


if __name__ == "__main__":
    unittest.main()
