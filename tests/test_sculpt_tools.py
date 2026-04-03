"""Tests for sculpt tool registration and simulated handlers."""

import unittest

from mcp_server.handler_modules import HANDLERS


class TestSculptTools(unittest.TestCase):
    def test_sculpt_tools_registered(self):
        self.assertIn("enter_sculpt_mode", HANDLERS)
        self.assertIn("set_sculpt_brush", HANDLERS)
        self.assertIn("sculpt_face_set_from_mask", HANDLERS)
        self.assertIn("sculpt_mask_flood_fill", HANDLERS)
        self.assertIn("sculpt_mesh_filter", HANDLERS)
        self.assertIn("sculpt_symmetrize", HANDLERS)
        self.assertIn("sculpt_brush_stroke_path", HANDLERS)
        self.assertIn("sculpt_draw_line_stroke", HANDLERS)
        self.assertIn("sculpt_voxel_remesh", HANDLERS)

    def test_sculpt_handlers_simulated(self):
        mode = HANDLERS["enter_sculpt_mode"]({"object_name": "Cube"})
        brush = HANDLERS["set_sculpt_brush"]({"brush_name": "Draw", "size": 42})
        flood = HANDLERS["sculpt_mask_flood_fill"]({"mode": "VALUE", "value": 1.0})
        line = HANDLERS["sculpt_draw_line_stroke"](
            {
                "object_name": "Cube",
                "start": [0.0, 0.0, 0.0],
                "end": [0.0, 0.0, 1.0],
                "steps": 8,
            }
        )
        remesh = HANDLERS["sculpt_voxel_remesh"](
            {"object_name": "Cube", "voxel_size": 0.1}
        )
        self.assertTrue(mode["simulated"])
        self.assertTrue(brush["simulated"])
        self.assertTrue(flood["simulated"])
        self.assertTrue(line["simulated"])
        self.assertTrue(remesh["simulated"])


if __name__ == "__main__":
    unittest.main()
