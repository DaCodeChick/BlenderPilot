"""Strict validation utilities for MCP tool calls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

try:
    from ..mcp_server.tool_definitions import TOOLS_BY_NAME  # type: ignore
except Exception:  # pragma: no cover
    from mcp_server.tool_definitions import TOOLS_BY_NAME  # type: ignore


@dataclass
class ValidationResult:
    valid: bool
    error: Optional[str] = None


class ToolCallValidator:
    """Validate tool call name and arguments against tool schema."""

    def __init__(self) -> None:
        self.tools = TOOLS_BY_NAME

    def validate(self, tool_name: str, arguments: Dict[str, Any]) -> ValidationResult:
        if tool_name not in self.tools:
            return ValidationResult(False, f"Unknown tool: {tool_name}")
        schema = self.tools[tool_name]["inputSchema"]
        if not isinstance(arguments, dict):
            return ValidationResult(False, "Arguments must be an object")
        return self._validate_object(arguments, schema)

    def _validate_object(
        self, value: Dict[str, Any], schema: Dict[str, Any]
    ) -> ValidationResult:
        if schema.get("type") != "object":
            return ValidationResult(False, "Invalid schema: root is not object")

        properties = schema.get("properties", {})
        required = schema.get("required", [])
        additional = schema.get("additionalProperties", True)

        for key in required:
            if key not in value:
                return ValidationResult(False, f"Missing required field: {key}")

        if not additional:
            unknown_keys = [k for k in value.keys() if k not in properties]
            if unknown_keys:
                return ValidationResult(
                    False, f"Unknown field(s): {', '.join(unknown_keys)}"
                )

        for key, item in value.items():
            if key not in properties:
                continue
            result = self._validate_value(item, properties[key], key)
            if not result.valid:
                return result

        return ValidationResult(True)

    def _validate_value(
        self, item: Any, schema: Dict[str, Any], field_name: str
    ) -> ValidationResult:
        expected_type = schema.get("type")
        if expected_type == "string":
            if not isinstance(item, str):
                return ValidationResult(False, f"{field_name} must be a string")
            enum = schema.get("enum")
            if enum and item not in enum:
                return ValidationResult(
                    False, f"{field_name} must be one of: {', '.join(enum)}"
                )
            return ValidationResult(True)

        if expected_type == "number":
            if not isinstance(item, (int, float)):
                return ValidationResult(False, f"{field_name} must be a number")
            return ValidationResult(True)

        if expected_type == "array":
            if not isinstance(item, list):
                return ValidationResult(False, f"{field_name} must be an array")
            min_items = schema.get("minItems")
            max_items = schema.get("maxItems")
            if min_items is not None and len(item) < min_items:
                return ValidationResult(
                    False, f"{field_name} requires at least {min_items} items"
                )
            if max_items is not None and len(item) > max_items:
                return ValidationResult(
                    False, f"{field_name} allows at most {max_items} items"
                )
            item_schema = schema.get("items")
            if item_schema:
                for index, value in enumerate(item):
                    result = self._validate_value(
                        value, item_schema, f"{field_name}[{index}]"
                    )
                    if not result.valid:
                        return result
            return ValidationResult(True)

        if expected_type == "object":
            if not isinstance(item, dict):
                return ValidationResult(False, f"{field_name} must be an object")
            return self._validate_object(item, schema)

        return ValidationResult(
            False, f"Unsupported schema type for {field_name}: {expected_type}"
        )


def validate_tool_call(tool_name: str, arguments: Dict[str, Any]) -> ValidationResult:
    """Convenience function for one-off validation."""
    return ToolCallValidator().validate(tool_name, arguments)
