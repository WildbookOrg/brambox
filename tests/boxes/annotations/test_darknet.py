# -*- coding: utf-8 -*-
import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import DarknetAnnotation, DarknetParser

darknet_string = """3 0.0 0.0 0.0 0.0
3 0.0 0.0 0.0 0.0
0 0.0 0.0 0.0 0.0
"""


class TestDarknetAnnotation(unittest.TestCase):
    def setUp(self):
        self.image_width = 1000
        self.image_height = 500
        self.class_label_map = ['person', 'car', 'tv', '']
        self.anno = DarknetAnnotation()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if serialization of one annotation works """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 35
        self.anno.y_top_left = 30
        self.anno.width = 30
        self.anno.height = 40

        string = self.anno.serialize(
            self.class_label_map, self.image_width, self.image_height
        )
        self.assertEqual(string, '0 0.05 0.1 0.03 0.08')

    def test_serialize_class_label_index(self):
        """ test if class label index is correctly mapped """
        self.anno.class_label = 'tv'
        string = self.anno.serialize(
            self.class_label_map, self.image_width, self.image_height
        )
        self.assertEqual(string, '2 0.0 0.0 0.0 0.0')

    def test_serialize_no_class_label_map(self):
        """ If no class_label_map is given, the annotation should try to get a number """
        string = self.anno.serialize(None, self.image_width, self.image_height)
        self.assertEqual(string, '? 0.0 0.0 0.0 0.0')

        self.anno.class_label = '5'
        string = self.anno.serialize(None, self.image_width, self.image_height)
        self.assertEqual(string, '5 0.0 0.0 0.0 0.0')

        self.anno.class_label = 'willnotwork'
        self.assertRaises(
            ValueError, self.anno.serialize, None, self.image_width, self.image_height
        )

    def test_deserialize(self):
        """ test if deserialization of one annotation works """
        string = '1 0.05 0.1 0.03 0.08'
        self.anno.deserialize(
            string, self.class_label_map, self.image_width, self.image_height
        )
        self.assertEqual(self.anno.class_label, 'car')
        self.assertAlmostEqual(self.anno.x_top_left, 35)
        self.assertAlmostEqual(self.anno.y_top_left, 30)
        self.assertAlmostEqual(self.anno.width, 30)
        self.assertAlmostEqual(self.anno.height, 40)
        self.assertFalse(self.anno.occluded)
        self.assertFalse(self.anno.lost)

    def test_deserialize_no_class_label_map(self):
        """ If no class_label_map is given, the annotation should use the index as class_label """
        string = '1 0.0 0.0 0.0 0.0'
        self.anno.deserialize(string, None, self.image_width, self.image_height)
        self.assertEqual(self.anno.class_label, '1')

        string = '? 0.0 0.0 0.0 0.0'
        self.anno.deserialize(string, None, self.image_width, self.image_height)
        self.assertEqual(self.anno.class_label, '')


class TestDarknetParser(unittest.TestCase):
    def setUp(self):
        self.parser = DarknetParser(
            image_width=1000,
            image_height=500,
            class_label_map=['person', 'car', 'tv', ''],
        )

    def tearDown(self):
        pass

    def test_init_required_kwargs(self):
        """ test if constructor raises correct error when required kwargs
            are missing
        """
        self.assertRaises(ValueError, DarknetParser)
        self.assertRaises(ValueError, DarknetParser, image_width=0)
        self.assertRaises(
            ValueError,
            DarknetParser,
            image_width=None,
            image_height=0,
            class_label_map=[],
        )
        self.assertRaises(
            ValueError,
            DarknetParser,
            image_width=0,
            image_height=None,
            class_label_map=[],
        )

    def test_serialize(self):
        """ test basic serialization with parser """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        obj = [testanno1, testanno1, testanno2]

        string = self.parser.serialize(obj)
        self.assertEqual(string, darknet_string)

    def test_serialize_ignore_lost(self):
        """ Test serialization behaviour of parser with lost annotations """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno3 = Annotation()
        testanno2.class_label = 'person'
        testanno3.lost = True
        obj = [testanno3, testanno1, testanno3, testanno1, testanno2, testanno3]

        string = self.parser.serialize(obj)
        self.assertEqual(string, darknet_string)

    def test_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(darknet_string)
        self.assertEqual(type(obj), list)
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[0].class_label, '')
        self.assertEqual(obj[2].class_label, 'person')


if __name__ == '__main__':
    unittest.main()
