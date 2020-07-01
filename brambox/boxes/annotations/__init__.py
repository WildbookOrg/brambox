# -*- coding: utf-8 -*-
"""
Brambox boxes annotations module |br|
This package contains the actual annotation parsers. These parsers can be used to parse and generate annotation files.
"""

from .annotation import Annotation
from .formats import *

from .cvc import *
from .darknet import *
from .dollar import *
from .kitti import *
from .pascalvoc import *
from .pickle import *
from .vatic import *
from .yaml import *
