# -*- coding: utf-8 -*-
import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import YamlAnnotation, YamlParser

yaml_string = """img_1:
  '?':
  - coords: [0, 0, 0, 0]
    difficult: false
    lost: false
    occluded_fraction: 0.0
    truncated_fraction: 0.0
  person:
  - coords: [0, 0, 0, 0]
    difficult: true
    id: 1
    lost: false
    occluded_fraction: 0.0
    truncated_fraction: 0.0
img_2:
  '?':
  - coords: [0, 0, 0, 0]
    difficult: false
    lost: false
    occluded_fraction: 0.0
    truncated_fraction: 0.0
  - coords: [0, 0, 0, 0]
    difficult: false
    lost: false
    occluded_fraction: 0.0
    truncated_fraction: 0.0
  - coords: [0, 0, 0, 0]
    difficult: false
    lost: false
    occluded_fraction: 0.0
    truncated_fraction: 0.0
"""


class TestYamlAnnotation(unittest.TestCase):
    def setUp(self):
        self.anno = YamlAnnotation()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if serialization of one annotation works """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 10
        self.anno.y_top_left = 20
        self.anno.width = 30
        self.anno.height = 40
        self.anno.lost = True
        self.anno.occluded = False

        key, val = self.anno.serialize()
        self.assertEqual(key, 'person')
        self.assertEqual(val['coords'], [10, 20, 30, 40])
        self.assertTrue(val['lost'])
        self.assertFalse(val['difficult'])
        self.assertEqual(val['occluded_fraction'], 0.0)

    def test_deserialize(self):
        """ test if deserialization of one annotation works """
        self.anno.deserialize(
            {
                'coords': [10, 20, 30, 40],
                'difficult': True,
                'id': 1,
                'lost': True,
                'occluded_fraction': 70.0,
                'truncated_fraction': 0.0,
            },
            'person',
        )
        self.assertEqual(self.anno.class_label, 'person')
        self.assertEqual(self.anno.object_id, 1)
        self.assertEqual(self.anno.x_top_left, 10)
        self.assertEqual(self.anno.y_top_left, 20)
        self.assertEqual(self.anno.width, 30)
        self.assertEqual(self.anno.height, 40)
        self.assertEqual(self.anno.occluded_fraction, 0.7)
        self.assertEqual(self.anno.truncated_fraction, 0.0)
        self.assertTrue(self.anno.occluded)
        self.assertTrue(self.anno.lost)
        self.assertTrue(self.anno.difficult)


class TestYamlParser(unittest.TestCase):
    def setUp(self):
        self.parser = YamlParser()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test basic serialization with parser """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        testanno2.object_id = 1
        testanno2.difficult = True
        obj = {
            'img_1': [testanno1, testanno2],
            'img_2': [testanno1, testanno1, testanno1],
        }

        string = self.parser.serialize(obj)
        self.assertEqual(string, yaml_string)

    def test_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(yaml_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(type(obj['img_1']), list)
        self.assertEqual(len(obj['img_2']), 3)


if __name__ == '__main__':
    unittest.main()
