import json
from base_annotator import Annotator, AnnotationType

class AggregateConfidenceAnnotator(Annotator):
    POINTING_CONFIDENCE_BOUNDS = [-1, 1]
    COLOR_CONFIDENCE_BOUNDS = [0, 1]

    def initialize(self):
        super().initialize()
        self.annotation_types.append(AggregateConfidenceAnnotation.ANNOTATION_UIMA_TYPE_NAME)

    def process(self, cas):
        all_pointing_confidences = cas['_views']['_InitialView']['Pointing']
        all_color_confidences = cas['_views']['_InitialView']['ColorConfidence']
#------------------------         
#         uses_actual_block_color = cas['_views']['_InitialView']['UsesActualBlockColor']
#         uses_gesture = cas['_views']['_InitialView']['UsesGesture']
#         uses_spatial_mods = cas['_views']['_InitialView']['UsesSpatialMods']
        
        if len(all_pointing_confidences) != len(all_color_confidences):
            print("Did not process the same number of blocks for each line of processing. Please try again!")
 
        pointing_confidences = dict()
        color_confidences = dict()
        for id in range(0, len(all_pointing_confidences)):
            block_id = all_pointing_confidences[id]['id']
            pointing_conf = all_pointing_confidences[id]['confidence']
            pointing_confidences[block_id] = pointing_conf
 
            color_conf = all_color_confidences[id]['confidence']
            color_confidences[block_id] = color_conf
 
        normalized_pointing_confidences = self.normalize_data(pointing_confidences, self.POINTING_CONFIDENCE_BOUNDS)
        normalized_color_confidences = self.normalize_data(color_confidences, self.COLOR_CONFIDENCE_BOUNDS)
# 
#         for block_id in normalized_pointing_confidences:
#             normalized_pointing_conf = normalized_pointing_confidences[block_id]
# #             normalized_text_conf = normalized_text_confidences[block_id]
# #             output_conf = (normalized_pointing_conf if usesGesture else 1) * (normalized_text_conf if uses_actual_block_color else 1) * (spatial_relationship_conf if uses_spatial_mods else 1)
#             annotation = AggregateConfidenceAnnotation(block_id, normalized_pointing_conf * spatial_relationship_conf, normalized_pointing_conf, 1)
#             self.add_annotation(annotation)

        print("Begining of Aggregation")
        
        id = cas['_views']['_InitialView']['MetadataSelectedBlock'][0]['id']
        print('SELECTED BLOCK ID:')
        print(id)
        
        spatial_relationship_conf = cas['_views']['_InitialView']['MetadataSelectedBlock'][0]['confidenceValue']
        print('SPATIAL CONFIDENCE:')
        print(spatial_relationship_conf)
        
        normalized_pointing_confidence = normalized_pointing_confidences[id]
        print('POINTING CONFIDENCE:')
        print(normalized_pointing_confidence)
        
        normalized_color_confidence = normalized_color_confidences[id]
        print('COLOR CONFIDENCE:')
        print(normalized_color_confidence)
        
        totalConfidence = normalized_pointing_confidence * spatial_relationship_conf * normalized_color_confidence
        print('TOTAL CONFIDENCE:')
        print(totalConfidence)
        
        annotation = AggregateConfidenceAnnotation(id, totalConfidence, normalized_pointing_confidence, normalized_color_confidence)
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
    
    def __init__(self, id, confidence, normalized_pointing_conf, normalized_color_conf):
        self.name = self.ANNOTATION_UIMA_TYPE_NAME
        self.id = id
        self.confidence = confidence
        self.normPointingConf = normalized_pointing_conf
        self.normColorConf = normalized_color_conf
