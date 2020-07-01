# -*- coding: utf-8 -*-
import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.detections.detection import Detection


class TestDetection(unittest.TestCase):
    def setUp(self):
        self.det = Detection()

    def tearDown(self):
        pass

    def test_properties(self):
        """ Test various computed properties of the base Annotation class """
        pass

    def test_create_method(self):
        """ Test the different create method signatures """
        det = Detection.create()
        self.assertIsInstance(det, Detection)

        self.det.class_label = 'randomlabel'
        det = Detection.create(self.det)
        self.assertEqual(det, self.det)

        anno = Annotation()
        anno.class_label = 'test'
        det = Detection.create(anno)
        self.assertEqual(det.class_label, 'test')
        self.assertAlmostEqual(det.confidence, 1.0)

    def test_repr(self):
        """ Test annotation __repr__ function """
        repr_string = 'Detection {class_label = , object_id = None, x = 0.0, y = 0.0, w = 0.0, h = 0.0, confidence = 0.0}'
        self.assertEqual(repr(self.det), repr_string)

    def test_print(self):
        """ Test annotation __str__ function """
        str_string = "Detection {'', [0, 0, 0, 0], 0.0%}"
        self.assertEqual(str(self.det), str_string)


if __name__ == '__main__':
    unittest.main()
