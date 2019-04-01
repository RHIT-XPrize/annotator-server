import json
import rospy
import intera_interface
from base_annotator import Annotator, AnnotationType

class SampleRobotAnnotator(Annotator):
    def initialize(self,):
        super().initialize()
        self.annotation_types.append(RobotAnnotation.ANNOTATION_UIMA_TYPE_NAME)

    def process(self, cass):
        rospy.init_node("GraspingDemo")
        global limb
        limb = intera_interface.Limb('right')
        global gripper
        gripper = intera_interface.Gripper('right')
        gripper.open()
        gripper.close()
        annotation = RobotAnnotation()
        self.add_annotation(annotation)

class RobotAnnotation(AnnotationType):
    ANNOTATION_UIMA_TYPE_NAME = "edu.rosehulman.aixprize.pipeline.types.SampleSawyer"
    
    def __init__(self):
        self.name = self.ANNOTATION_UIMA_TYPE_NAME
