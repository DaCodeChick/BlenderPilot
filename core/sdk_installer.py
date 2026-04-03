# BlenderPilot - AI-driven Blender automation via MCP
# Copyright (C) 2026 BlenderPilot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Auto-installer for AI provider SDKs with Linux system package detection."""

import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import Optional, Tuple


class SDKInstaller:
    """Handles installation of AI provider SDKs."""

    PROVIDERS = {
        "openai": "openai",
        "anthropic": "anthropic",
    }

    @staticmethod
    def can_import(module_name: str) -> bool:
        """
        Check if a module can be imported.

        Args:
            module_name: Name of the module to check

        Returns:
            True if the module can be imported
        """
        spec = importlib.util.find_spec(module_name)
        return spec is not None

    @staticmethod
    def is_linux() -> bool:
        """Check if running on Linux."""
        return sys.platform.startswith("linux")

    @staticmethod
    def find_system_package(package_name: str) -> Optional[Path]:
        """
        Try to find a package in system site-packages (Linux only).

        Args:
            package_name: Name of the package

        Returns:
            Path to the package if found, None otherwise
        """
        if not SDKInstaller.is_linux():
            return None

        # Common system site-packages locations
        system_paths = [
            Path("/usr/lib/python3/dist-packages"),
            Path("/usr/local/lib/python3/dist-packages"),
            Path(
                f"/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
            ),
            Path(
                f"/usr/local/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
            ),
        ]

        for path in system_paths:
            package_path = path / package_name
            if package_path.exists():
                return path

        return None

    @staticmethod
    def add_system_site_packages():
        """
        Add system site-packages to sys.path if not already present.
        This allows Blender to use system-installed Python packages.
        """
        if not SDKInstaller.is_linux():
            return

        # Find system site-packages
        system_paths = [
            Path("/usr/lib/python3/dist-packages"),
            Path(
                f"/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
            ),
        ]

        for path in system_paths:
            if path.exists() and str(path) not in sys.path:
                sys.path.insert(0, str(path))

    @staticmethod
    def install_to_blender_python(package_name: str) -> Tuple[bool, str]:
        """
        Install a package to Blender's Python environment.

        Args:
            package_name: Name of the package to install

        Returns:
            Tuple of (success, message)
        """
        try:
            # Get Blender's Python executable
            python_exe = sys.executable

            # Run pip install
            result = subprocess.run(
                [python_exe, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode == 0:
                return True, f"Successfully installed {package_name}"
            else:
                return False, f"Failed to install {package_name}: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, f"Installation of {package_name} timed out"
        except Exception as e:
            return False, f"Error installing {package_name}: {str(e)}"

    @classmethod
    def ensure_provider_sdk(cls, provider_name: str) -> Tuple[bool, str]:
        """
        Ensure a provider SDK is available, installing if necessary.

        Strategy:
        1. Check if already importable (Blender Python or system)
        2. On Linux: check system packages and add to sys.path
        3. Install to Blender's Python as fallback

        Args:
            provider_name: Name of the provider ('openai', 'anthropic', etc.)

        Returns:
            Tuple of (success, message)
        """
        if provider_name not in cls.PROVIDERS:
            return False, f"Unknown provider: {provider_name}"

        package_name = cls.PROVIDERS[provider_name]

        # 1. Check if already importable
        if cls.can_import(package_name):
            return True, f"{package_name} is already available"

        # 2. On Linux: check system packages
        if cls.is_linux():
            system_path = cls.find_system_package(package_name)
            if system_path:
                # Add to sys.path
                if str(system_path) not in sys.path:
                    sys.path.insert(0, str(system_path))

                # Verify it works now
                if cls.can_import(package_name):
                    return True, f"{package_name} found in system packages"

        # 3. Install to Blender's Python
        return cls.install_to_blender_python(package_name)

    @classmethod
    def ensure_all_providers(cls) -> dict:
        """
        Ensure all provider SDKs are available.

        Returns:
            Dict mapping provider name to (success, message) tuples
        """
        results = {}

        for provider_name in cls.PROVIDERS:
            success, message = cls.ensure_provider_sdk(provider_name)
            results[provider_name] = (success, message)

        return results
