from setuptools import setup

setup(name='brambox',
      version='0.0.1',
      description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
      author='EAVISE',
      packages=['brambox',
                'brambox.boxes',
                'brambox.boxes.annotations',
                'brambox.boxes.detections',
                'brambox.boxes.util',
                'brambox.transforms'],
      scripts=['scripts/convert_annotations.py',
               'scripts/replace_image_channel.py',
               'scripts/show_annotations.py',
               'scripts/sparse_link.py',
               'scripts/swap_image_channel.py'],
      test_suite='tests')
