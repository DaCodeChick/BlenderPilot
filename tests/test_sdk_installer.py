"""Unit tests for SDK installer behavior."""

import unittest
from unittest import mock

from core.sdk_installer import SDKInstaller


class TestSDKInstaller(unittest.TestCase):
    def test_unknown_provider(self):
        ok, msg = SDKInstaller.ensure_provider_sdk("not-a-provider")
        self.assertFalse(ok)
        self.assertIn("Unknown provider", msg)

    @mock.patch("core.sdk_installer.SDKInstaller.can_import", return_value=True)
    def test_provider_already_available(self, _mock_import):
        ok, msg = SDKInstaller.ensure_provider_sdk("openai")
        self.assertTrue(ok)
        self.assertIn("already available", msg)

    @mock.patch("core.sdk_installer.SDKInstaller.can_import", side_effect=[False, True])
    @mock.patch("core.sdk_installer.SDKInstaller.find_system_package")
    @mock.patch("core.sdk_installer.SDKInstaller.is_linux", return_value=True)
    def test_linux_system_package_path(self, _mock_linux, mock_find, _mock_import):
        mock_find.return_value = "/usr/lib/python3/dist-packages"
        ok, msg = SDKInstaller.ensure_provider_sdk("openai")
        self.assertTrue(ok)
        self.assertIn("system packages", msg)


if __name__ == "__main__":
    unittest.main()
