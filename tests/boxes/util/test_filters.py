# -*- coding: utf-8 -*-
import unittest
import brambox.boxes as bbb


class TestImageBoundsFilter(unittest.TestCase):
    def setUp(self):
        # construct box that is in bounds
        self.box = bbb.Box()
        self.box.x_top_left = 2.0
        self.box.y_top_left = 2.0
        self.box.width = 5.0
        self.box.height = 10.0
        self.bounds = (1.0, 1.0, 9.0, 13.0)
        self.f = bbb.ImageBoundsFilter(self.bounds)

    def test_in_bounds(self):
        """Box is in bounds, all box dimensions are smaller than the bounds
        """
        self.assertTrue(self.f(self.box))

    def test_in_bound_edges(self):
        """Box is in bounds, all bounds equal the box dimensions
        """
        self.box.x_top_left = self.bounds[0]
        self.box.y_top_left = self.bounds[1]
        self.box.width = self.bounds[2] - self.bounds[0]
        self.box.height = self.bounds[3] - self.bounds[1]
        self.assertTrue(self.f(self.box))

    def test_out_bounds_left(self):
        """Box is out of bounds, only on the left side
        """
        self.box.x_top_left = self.bounds[0] - 1.0
        self.assertFalse(self.f(self.box))

    def test_out_bounds_right(self):
        """Box is out of bounds, only on the right side
        """
        self.box.width = self.bounds[2]
        self.assertFalse(self.f(self.box))

    def test_out_bounds_top(self):
        """Box is out of bounds, only on the top side
        """
        self.box.y_top_left = self.bounds[1] - 1.0
        self.assertFalse(self.f(self.box))

    def test_out_bounds_bottom(self):
        """Box is out of bounds, only on the bottom side
        """
        self.box.height = self.bounds[3]
        self.assertFalse(self.f(self.box))


class TestOcclusionAreaFilter(unittest.TestCase):
    def setUp(self):
        self.anno = bbb.Annotation()
        self.visible_range = (0.5, 0.7)
        self.f = bbb.OcclusionAreaFilter(self.visible_range)

    def test_not_occluded(self):
        """Annotation is not occluded
        """
        self.occluded = False
        self.assertTrue(self.f(self.anno))

    def test_occlusion_in_range(self):
        """Annotation is occluded but in range of the allowed visible area
        """
        visible_fraction = 0.6
        self.anno.occluded_fraction = 1 - visible_fraction
        self.assertTrue(self.f(self.anno))

    def test_occlusion_in_range_upper_bound(self):
        """Annotation is occluded and the visible fraction equals the upper bound
        """
        visible_fraction = self.visible_range[1]
        self.anno.occluded_fraction = 1 - visible_fraction
        self.assertTrue(self.f(self.anno))

    def test_occlusion_in_range_lower_bound(self):
        """Annotation is occluded and the visible fraction equals the lower bound
        """
        visible_fraction = self.visible_range[0]
        self.anno.occluded_fraction = 1 - visible_fraction
        self.assertTrue(self.f(self.anno))

    def test_occlusion_outside_range_upper_bound(self):
        """Annotation is occluded and the visible fraction > the upper bound
        """
        visible_fraction = self.visible_range[1] + 0.1
        self.anno.occluded_fraction = 1 - visible_fraction
        self.assertFalse(self.f(self.anno))


if __name__ == '__main__':
    unittest.main()
