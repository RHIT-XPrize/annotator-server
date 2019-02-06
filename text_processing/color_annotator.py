from base_annotator import Annotator, AnnotationType

import json
from tornado.ioloop import IOLoop
from tornado.web import Application

class Color(AnnotationType):
    ANNOTATION_UIMA_TYPE_NAME = "edu.rosehulman.aixprize.pipeline.types.Color"

    def __init__(self, color, start, end):
        self.name = self.ANNOTATION_UIMA_TYPE_NAME
        self.color = color
        self.begin = start
        self.end = end

def find_in_str(target, string, start=0):
    idx = string.find(target)
    if idx >= 0:
        return [ Color(target, start + idx, start + idx + len(target) - 1) ] + \
            find_in_str(target, string[idx + 1:], start=start + idx + 1)
    return [ ]

class ColorAnnotator(Annotator):
    def initialize(self):
        super().initialize()
        with open("color_dictionary.json", encoding='utf-8') as f:
            self.color_dict = json.load(f)
        self.annotation_types.append(Color.ANNOTATION_UIMA_TYPE_NAME)

    def process(self, cas):
        sofa_string = cas['_views']['_InitialView']['SpokenText'][0]['text']
        blocks = cas['_views']['_InitialView']['DetectedBlock']
        to_analyze = sofa_string
        for word in self.color_dict.keys:
            anns = find_in_str(word, to_analyze)
            for a in anns:
                print(a)
                self.add_annotation(a)
