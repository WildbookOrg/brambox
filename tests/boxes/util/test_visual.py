import unittest
import numpy as np
try:
    import cv2
except ModuleNotFoundError:
    cv2 = None
from PIL import Image, ImageDraw, ImageFont
import brambox.boxes as bbb

try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 10)
except FileNotFoundError:
    font = ImageFont.load_default()


class TestDrawBoxes(unittest.TestCase):
    def setUp(self):
        self.anno = bbb.Annotation()
        self.anno.class_label = 'object'
        self.anno.x_top_left = 5
        self.anno.y_top_left = 6
        self.anno.width = 10
        self.anno.height = 15

    def tearDown(self):
        pass

    @unittest.skipIf(cv2 is None, 'OpenCV not found, test depending on OpenCV')
    def test_draw_cv(self):
        """ Test if cv2 drawing works """
        img = np.zeros((25, 25, 3), np.uint8)
        res = bbb.draw_boxes(img.copy(), [self.anno], (255, 0, 0), True)

        cv2.rectangle(img, (5, 6), (15, 21), (0, 0, 255), 3)
        cv2.putText(img, 'object', (5, 1), cv2.FONT_HERSHEY_PLAIN, .75, (0, 0, 255), 1, cv2.LINE_AA)

        self.assertTrue(np.array_equal(img, res))

    def test_draw_pil(self):
        """ Test if Pillow drawing works """
        img = Image.new('RGB', (25, 25))
        res = bbb.draw_boxes(img.copy(), [self.anno], (255, 0, 0), True)

        imgdraw = ImageDraw.Draw(img)
        imgdraw.line([(5, 6), (15, 6), (15, 21), (5, 21), (5, 6)], (255, 0, 0), 3)
        imgdraw.text((5, -9), 'object', (255, 0, 0), font)

        self.assertEqual(list(res.getdata()), list(img.getdata()))

    def test_draw_detection(self):
        """ Test drawing a detection and printing its confidence value """
        det = bbb.Detection()
        det.confidence = .66
        det.class_label = 'obj'
        det.object_id = 1
        det.x_top_left = 10
        det.y_top_left = 10
        det.width = 10
        det.height = 10

        img = Image.new('RGB', (50, 50))
        res = bbb.draw_boxes(img.copy(), [det], (100, 0, 125), True)

        imgdraw = ImageDraw.Draw(img)
        imgdraw.line([(10, 10), (20, 10), (20, 20), (10, 20), (10, 10)], (100, 0, 125), 3)
        imgdraw.text((10, -5), 'obj 1|66.00%', (100, 0, 125), font)

        self.assertEqual(list(res.getdata()), list(img.getdata()))

    def test_draw_faded(self):
        """ Test drawing faded bounding boxes """
        anno2 = bbb.Annotation()
        anno2.difficult = True
        anno2.class_label = 'object'
        anno2.object_id = 2
        anno2.x_top_left = 20
        anno2.y_top_left = 20
        anno2.width = 10
        anno2.height = 10

        img = Image.new('RGB', (40, 40))
        res = bbb.draw_boxes(img.copy(), [self.anno, anno2], (255, 0, 0), True, faded=lambda a: a.difficult)

        imgdraw = ImageDraw.Draw(img)
        imgdraw.line([(5, 6), (15, 6), (15, 21), (5, 21), (5, 6)], (255, 0, 0), 3)
        imgdraw.text((5, -9), 'object', (255, 0, 0), font)
        imgdraw.line([(20, 20), (30, 20), (30, 30), (20, 30), (20, 20)], (255, 0, 0), 1)
        imgdraw.text((20, 7), 'object 2', (255, 0, 0), font)

        self.assertEqual(list(res.getdata()), list(img.getdata()))

    def test_draw_color_cycle(self):
        """ Test color cycle """
        anno1 = bbb.Annotation()
        anno1.class_label = 'a'
        anno1.x_top_left = 1
        anno1.y_top_left = 1
        anno1.width = 3
        anno1.height = 3
        anno2 = bbb.Annotation()
        anno2.class_label = 'b'
        anno2.x_top_left = 5
        anno2.y_top_left = 1
        anno2.width = 3
        anno2.height = 3
        anno3 = bbb.Annotation()
        anno3.class_label = 'c'
        anno3.x_top_left = 1
        anno3.y_top_left = 5
        anno3.width = 3
        anno3.height = 3
        anno4 = bbb.Annotation()
        anno4.class_label = 'b'
        anno4.x_top_left = 5
        anno4.y_top_left = 5
        anno4.width = 3
        anno4.height = 3

        img = Image.new('RGB', (10, 10))
        res = bbb.draw_boxes(img.copy(), [anno1, anno2, anno3, anno4])

        imgdraw = ImageDraw.Draw(img)
        imgdraw.line([(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)], (31, 119, 180), 3)
        imgdraw.line([(5, 1), (8, 1), (8, 4), (5, 4), (5, 1)], (255, 127, 14), 3)
        imgdraw.line([(1, 5), (4, 5), (4, 8), (1, 8), (1, 5)], (44, 160, 44), 3)
        imgdraw.line([(5, 5), (8, 5), (8, 8), (5, 8), (5, 5)], (255, 127, 14), 3)

        self.assertEqual(list(res.getdata()), list(img.getdata()))

    def test_draw_color_dict(self):
        """ Test color dict """
        anno1 = bbb.Annotation()
        anno1.class_label = 'a'
        anno1.x_top_left = 1
        anno1.y_top_left = 1
        anno1.width = 3
        anno1.height = 3
        anno2 = bbb.Annotation()
        anno2.class_label = 'b'
        anno2.x_top_left = 5
        anno2.y_top_left = 1
        anno2.width = 3
        anno2.height = 3
        anno3 = bbb.Annotation()
        anno3.class_label = 'c'
        anno3.x_top_left = 1
        anno3.y_top_left = 5
        anno3.width = 3
        anno3.height = 3
        anno4 = bbb.Annotation()
        anno4.class_label = 'b'
        anno4.x_top_left = 5
        anno4.y_top_left = 5
        anno4.width = 3
        anno4.height = 3

        img = Image.new('RGB', (10, 10))
        res = bbb.draw_boxes(img.copy(), [anno1, anno2, anno3, anno4], dict(a=(255, 0, 0), b=(0, 0, 255)))

        imgdraw = ImageDraw.Draw(img)
        imgdraw.line([(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)], (255, 0, 0), 3)
        imgdraw.line([(5, 1), (8, 1), (8, 4), (5, 4), (5, 1)], (0, 0, 255), 3)
        imgdraw.line([(5, 5), (8, 5), (8, 8), (5, 8), (5, 5)], (0, 0, 255), 3)

        self.assertEqual(list(res.getdata()), list(img.getdata()))


if __name__ == '__main__':
    unittest.main()
