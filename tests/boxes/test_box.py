# -*- coding: utf-8 -*-
import unittest
from brambox.boxes import Box


class TestBox(unittest.TestCase):
    def setUp(self):
        self.box = Box()

    def tearDown(self):
        pass

    def test_create_method(self):
        """ Test the different create method signatures """
        box = Box.create()
        self.assertIsInstance(box, Box)

        self.box.class_label = 'randomlabel'
        box = box.create(self.box)
        self.assertEqual(box, self.box)

        self.assertRaises(TypeError, Box.create, 3.1415)


if __name__ == '__main__':
    unittest.main()
