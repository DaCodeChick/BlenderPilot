# BlenderPilot - AI-driven Blender automation via MCP
# Copyright (C) 2026 BlenderPilot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Abstract base class for AI provider implementations."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ToolCall:
    """Represents a single MCP tool call from the AI."""

    tool_name: str
    arguments: Dict[str, Any]
    id: Optional[str] = None  # Some providers include call IDs

    def __str__(self):
        """String representation."""
        args_str = ", ".join(f"{k}={v}" for k, v in self.arguments.items())
        return f"{self.tool_name}({args_str})"


@dataclass
class ProviderResponse:
    """Response from an AI provider."""

    tool_calls: List[ToolCall]
    raw_response: Any  # Original provider response
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """Whether the request was successful."""
        return self.error is None

    def __str__(self):
        """String representation."""
        if not self.success:
            return f"Error: {self.error}"
        return f"ProviderResponse({len(self.tool_calls)} tool calls)"


class ProviderInterface(ABC):
    """Abstract interface for AI providers."""

    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the provider.

        Args:
            api_key: API key for the provider
            **kwargs: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.config = kwargs

    @abstractmethod
    def generate_tool_calls(
        self,
        prompt: str,
        available_tools: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        image_path: Optional[str] = None,
    ) -> ProviderResponse:
        """
        Generate MCP tool calls from a user prompt.

        Args:
            prompt: User's text prompt
            available_tools: List of available MCP tools with their schemas
            max_tokens: Maximum tokens for the response
            temperature: Sampling temperature (0.0-2.0)
            image_path: Optional path to an input image for vision-capable models

        Returns:
            ProviderResponse with tool calls or error
        """
        pass

    @abstractmethod
    def supports_vision(self) -> bool:
        """
        Whether this provider supports vision/image input.

        Returns:
            True if vision is supported
        """
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test if the API key is valid and the provider is reachable.

        Returns:
            True if connection successful
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable name of the provider.

        Returns:
            Provider name (e.g., "OpenAI", "Anthropic")
        """
        pass

    def __str__(self):
        """String representation."""
        return f"{self.name} Provider"
