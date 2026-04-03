"""Shared Blender context helpers for handler modules."""

from __future__ import annotations

try:
    import bpy  # type: ignore
except Exception:  # pragma: no cover
    bpy = None


class BlenderContext:
    @property
    def available(self) -> bool:
        return bpy is not None

    def lookup_object(self, name: str):
        if not self.available:
            return None
        return bpy.data.objects.get(name)

    def rename_active(self, name: str) -> str:
        if not self.available:
            return name
        obj = bpy.context.active_object
        if obj and name:
            obj.name = name
            if obj.data:
                obj.data.name = f"{name}_Mesh"
        return obj.name if obj else name


CTX = BlenderContext()
