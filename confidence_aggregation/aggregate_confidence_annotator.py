import json
from base_annotator import Annotator, AnnotationType

class AggregateConfidenceAnnotator(Annotator):
    POINTING_CONFIDENCE_BOUNDS = [-1, 1]
    TEXT_CONFIDENCE_BOUNDS = [0, 1]

    def initialize(self):
        super().initialize()
        self.annotation_types.append(AggregateConfidenceAnnotation.ANNOTATION_UIMA_TYPE_NAME)

    def process(self, cas):
        all_pointing_confidences = cas['_views']['_InitialView']['Pointing']
        all_text_confidences = cas['_views']['_InitialView']['TextConfidence']

        if len(all_pointing_confidences) != len(all_text_confidences):
            print("Did not process the same number of blocks for each line of processing. Please try again!")

        pointing_confidences = dict()
        text_confidences = dict()
        for id in range(0, len(all_pointing_confidences)):
            block_id = all_pointing_confidences[id]['id']
            pointing_conf = all_pointing_confidences[id]['confidence']
            pointing_confidences[block_id] = pointing_conf

            text_conf = all_text_confidences[id]['confidence']
            text_confidences[block_id] = text_conf

        normalized_pointing_confidences = self.normalize_data(pointing_confidences, self.POINTING_CONFIDENCE_BOUNDS)
        normalized_text_confidences = self.normalize_data(text_confidences, self.TEXT_CONFIDENCE_BOUNDS)

        for block_id in normalized_pointing_confidences:
            normalized_pointing_conf = normalized_pointing_confidences[block_id]
            normalized_text_conf = normalized_text_confidences[block_id]

            output_conf = normalized_pointing_conf * normalized_text_conf
            annotation = AggregateConfidenceAnnotation(block_id, output_conf)
            self.add_annotation(annotation)

    def normalize_data(self, data_to_normalize, data_bounds):
        min_value = data_bounds[0]
        max_value = data_bounds[1]
        data_range = max_value - min_value

        normalized_data = dict()
        for block_id, value in data_to_normalize.items():
            normalized_value = (value - min_value) / data_range
            normalized_data[block_id] = value
        return normalized_data
        
class AggregateConfidenceAnnotation(AnnotationType):
    ANNOTATION_UIMA_TYPE_NAME = "edu.rosehulman.aixprize.pipeline.types.AggregateConfidence"
    
    def __init__(self, id, confidence):
        self.name = self.ANNOTATION_UIMA_TYPE_NAME
        self.id = id
        self.confidence = confidence
