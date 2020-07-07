# -*- coding: utf-8 -*-
import unittest
import numpy as np

try:
    import cv2
except ModuleNotFoundError:
    cv2 = None
import brambox as bb
from PIL import Image, ImageDraw


class TestChannelMixer(unittest.TestCase):
    def setUp(self):
        self.mixer = bb.transforms.ChannelMixer(4)

    def tearDown(self):
        pass

    @unittest.skipIf(cv2 is None, 'OpenCV not found, test depending on OpenCV')
    def test_basic_cv2(self):
        """ Test if mixing works with OpenCV """
        self.mixer.set_channels([(1, 0), (0, 1), (0, 0), (0, 2)])
        img0 = np.ones((10, 10, 3), np.uint8) * (0, 100, 255)
        img1 = np.ones((10, 10, 1), np.uint8) * 127
        res = np.ones((10, 10, 4), np.uint8) * (127, 100, 0, 255)

        out = self.mixer(img0, img1)
        self.assertTrue(np.array_equal(res, out))

    def test_basic_pil(self):
        """ Test if mixing works with Pillow """
        self.mixer.set_channels([(1, 0), (0, 1), (0, 0), (0, 2)])
        img0 = Image.new('RGB', (10, 10), (0, 100, 255))
        img1 = Image.new('L', (10, 10), 127)
        res = Image.new('RGBA', (10, 10), (127, 100, 0, 255))

        out = self.mixer(img0, img1)
        self.assertEqual(list(res.getdata()), list(out.getdata()))

    def test_input(self):
        """ Test whether the class catches when giving not enough images as input """
        self.mixer.set_channels(
            [(0, 0), (0, 1), (0, 2), (1, 0)]
        )  # This means we need 2 input images (more is allowed)
        img = Image.new('RGB', (5, 5))

        self.assertRaises(ValueError, self.mixer, img)
        try:
            self.mixer(img, img)
            self.mixer(img, img, img, img)
        except Exception as err:
            self.fail(
                f'ChannelMixer raised error when it is given at least the correct number of input images [{err}]'
            )

    def test_set_channels(self):
        """ Test if set_channels catches wrong input """
        self.assertRaises(ValueError, self.mixer.set_channels, [(0, 0), (1, 1)])


if __name__ == '__main__':
    unittest.main()
