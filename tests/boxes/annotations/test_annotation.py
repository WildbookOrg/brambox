# -*- coding: utf-8 -*-
import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.detections.detection import Detection


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.anno = Annotation()

    def tearDown(self):
        pass

    def test_properties(self):
        """ Test various computed properties of the base Annotation class """
        self.assertFalse(self.anno.occluded)
        self.anno.occluded_fraction = 0.5
        self.assertTrue(self.anno.occluded)
        self.anno.occluded_fraction = 0.0
        self.anno.occluded = True
        self.assertAlmostEqual(self.anno.occluded_fraction, 1.0)

        self.assertFalse(self.anno.truncated)
        self.anno.truncated_fraction = 0.5
        self.assertTrue(self.anno.truncated)
        self.anno.truncated_fraction = 0.0
        self.anno.truncated = True
        self.assertAlmostEqual(self.anno.truncated_fraction, 1.0)

    def test_create_method(self):
        """ Test the different create method signatures """
        anno = Annotation.create()
        self.assertIsInstance(anno, Annotation)

        self.anno.class_label = 'randomlabel'
        anno = Annotation.create(self.anno)
        self.assertEqual(anno, self.anno)

        det = Detection()
        det.class_label = 'test'
        anno = Annotation.create(det)
        self.assertEqual(anno.class_label, 'test')
        self.assertEqual(anno.occluded, False)

    def test_repr(self):
        """ Test annotation __repr__ function """
        repr_string = "Annotation {class_label = '', object_id = None, x = 0.0, y = 0.0, w = 0.0, h = 0.0, ignore = False, lost = False, difficult = False, truncated_fraction = 0.0, occluded_fraction = 0.0, visible_x = 0.0, visible_y = 0.0, visible_w = 0.0, visible_h = 0.0}"
        self.assertEqual(repr(self.anno), repr_string)

    def test_print(self):
        """ Test annotation __str__ function """
        str_string = "Annotation {'', [0, 0, 0, 0]}"
        self.assertEqual(str(self.anno), str_string)

        str_string = "Annotation {'person' 1, [0, 0, 0, 0], difficult, lost, ignore, truncated 100.0%, occluded 60.0%}"
        self.anno.class_label = 'person'
        self.anno.object_id = 1
        self.anno.difficult = True
        self.anno.lost = True
        self.anno.ignore = True
        self.anno.truncated = True
        self.anno.occluded_fraction = 0.6
        self.assertEqual(str(self.anno), str_string)


if __name__ == '__main__':
    unittest.main()
