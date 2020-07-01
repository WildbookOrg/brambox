# -*- coding: utf-8 -*-
"""
Brambox boxes detections module |br|
This package contains the actual detection parsers. These parsers can be used to parse detection files.
"""

from .detection import Detection
from .formats import *

from .coco import *
from .dollar import *
from .pascalvoc import *
from .pickle import *
from .yaml import *
