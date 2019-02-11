from base_annotator import Annotator, AnnotationType
from text_processing.rgb2lab import deltaE

import json
from tornado.ioloop import IOLoop
from tornado.web import Application

class TextConfidenceAnnotation(AnnotationType):
    ANNOTATION_UIMA_TYPE_NAME = "edu.rosehulman.aixprize.pipeline.types.TextConfidence"

    def __init__(self, id, confidence):
        self.name = self.ANNOTATION_UIMA_TYPE_NAME
        self.id = id
        self.confidence = confidence

def is_word_in_str(target, string, start=0):
    idx = string.find(target)
    return idx >= 0

class TextProcessingAnnotator(Annotator):
    def initialize(self):
        super().initialize()
        with open("./text_processing/color_dictionary.json", encoding='utf-8') as f:
            self.color_dict = json.load(f)
        self.annotation_types.append(TextConfidenceAnnotation.ANNOTATION_UIMA_TYPE_NAME)

    def process(self, cas):
        sofa_string = cas['_views']['_InitialView']['SpokenText'][0]['text']
        blocks = cas['_views']['_InitialView']['DetectedBlock']
       
        to_analyze = sofa_string
        all_colors_in_text = []
        for word in self.color_dict.keys():
            if is_word_in_str(word, to_analyze):
                all_colors_in_text.append(word)

        if len(all_colors_in_text) == 0:
            print("Did not find color in spoken text, cannot determine confidence rating based on text.")
            return
        
        color_to_find = all_colors_in_text[0]
        for block in blocks:
            block_id = block['id']
            red_hue = block['r_hue']
            green_hue = block['g_hue']
            blue_hue = block['b_hue']

            block_rgb = [red_hue, green_hue, blue_hue]
            analyzed_color_rgb = self.color_dict[color_to_find]
            confidence = deltaE(block_rgb, analyzed_color_rgb)
            
            annotation = TextConfidenceAnnotation(block_id, confidence)
            self.add_annotation(annotation)
