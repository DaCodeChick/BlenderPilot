"""Tests for prompt context augmentation with project images."""

import unittest


def _augment(
    prompt: str, use_image_input: bool, image_source: str, image_names, selected: str
):
    if not use_image_input or image_source != "project":
        return prompt
    if not image_names:
        return prompt
    extra = [
        "",
        "Blender project image context:",
        f"- available_images: {', '.join(image_names)}",
    ]
    if selected:
        extra.append(f"- selected_image: {selected}")
    return prompt + "\n" + "\n".join(extra)


class TestPromptContext(unittest.TestCase):
    def test_no_context_when_disabled(self):
        out = _augment("make a cube", False, "project", ["A.png"], "A.png")
        self.assertEqual(out, "make a cube")

    def test_project_context_appended(self):
        out = _augment(
            "use texture", True, "project", ["Texture1.png", "B.png"], "Texture1.png"
        )
        self.assertIn("available_images", out)
        self.assertIn("selected_image", out)


if __name__ == "__main__":
    unittest.main()
