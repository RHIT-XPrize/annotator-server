import json
from base_annotator import Annotator, AnnotationType

class AggregateConfidenceAnnotator(Annotator):
    def initialize(self):
        super().initialize()
        self.annotation_types.append(AggregateConfidenceAnnotation.ANNOTATION_UIMA_TYPE_NAME)

    def process(self, cas):
        all_pointing_confidences = cas['_views']['_InitialView']['Pointing']
        all_text_confidences = cas['_views']['_InitialView']['TextConfidence']

        if len(all_pointing_confidences) != len(all_text_confidences):
            print("Did not process the same number of blocks for each line of processing. Please try again!")

        for id in range(0, len(all_pointing_confidences)):
            block_id = all_pointing_confidences[id]['id']
            pointing_conf = all_pointing_confidences[id]['confidence']
            text_conf = all_text_confidences[id]['confidence']

            output_conf = pointing_conf * text_conf
            annotation = AggregateConfidenceAnnotation(block_id, output_conf)
            self.add_annotation(annotation)

class AggregateConfidenceAnnotation(AnnotationType):
    ANNOTATION_UIMA_TYPE_NAME = "edu.rosehulman.aixprize.pipeline.types.AggregateConfidence"
    
    def __init__(self, id, confidence):
        self.name = self.ANNOTATION_UIMA_TYPE_NAME
        self.id = id
        self.confidence = confidence
