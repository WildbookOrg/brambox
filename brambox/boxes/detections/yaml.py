# -*- coding: utf-8 -*-
#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
"""
YAML
----
"""

import yaml
from .detection import *

__all__ = ['YamlDetection', 'YamlParser']


class YamlDetection(Detection):
    """ YAML image detection """

    def serialize(self):
        """ generate a yaml detection object """
        class_label = '?' if self.class_label == '' else self.class_label
        obj = {
            'coords': [
                int(self.x_top_left),
                int(self.y_top_left),
                int(self.width),
                int(self.height),
            ],
            'score': self.confidence * 100,
        }
        if self.object_id is not None:
            obj['id'] = self.object_id

        return (class_label, obj)

    def deserialize(self, yaml_obj, class_label):
        """ parse a yaml detection object """
        self.class_label = '' if class_label == '?' else class_label
        self.x_top_left = float(yaml_obj['coords'][0])
        self.y_top_left = float(yaml_obj['coords'][1])
        self.width = float(yaml_obj['coords'][2])
        self.height = float(yaml_obj['coords'][3])
        self.confidence = yaml_obj['score'] / 100
        if 'id' in yaml_obj:
            self.object_id = yaml_obj['id']


class YamlParser(Parser):
    """
    This parser generates a lightweight human readable detection format.
    With only one file for the entire dataset, this format will save you precious HDD space and will also be parsed faster.

    Example:
        >>> detections.yaml
            img1:
              car:
                - coords: [x,y,w,h]
                  score: 56.76
              person:
                - coords: [x,y,w,h]
                  id: 1
                  score: 90.1294132
                - coords: [x,y,w,h]
                  id: 2
                  score: 12.120
            img2:
              car:
                - coords: [x,y,w,h]
                  score: 50
    """

    parser_type = ParserType.SINGLE_FILE
    box_type = YamlDetection
    extension = '.yaml'

    def serialize(self, detections):
        """ Serialize input dictionary of detections into one string """
        result = {}
        for img_id in detections:
            img_res = {}
            for det in detections[img_id]:
                new_det = self.box_type.create(det)
                key, val = new_det.serialize()
                if key not in img_res:
                    img_res[key] = [val]
                else:
                    img_res[key] += [val]
            result[img_id] = img_res

        return yaml.dump(result)

    def deserialize(self, string):
        """ Deserialize a detection file into a dictionary of detections """
        yml_obj = yaml.load(string)

        result = {}
        for img_id in yml_obj:
            det_res = []
            for class_label, detections in yml_obj[img_id].items():
                for det_yml in detections:
                    det = self.box_type()
                    det.deserialize(det_yml, class_label)
                    det_res += [det]
            result[img_id] = det_res

        return result
