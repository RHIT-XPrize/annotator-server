import math
import numpy
import json
from base_annotator import Annotator, AnnotationType

class CoordinateTransformationAnnotator(Annotator):
    heightFromTable = 0.5
    distanceRightOfRobot = 1
    angleOfKinect = 30
        
    def initialize(self):
        super().initialize()
        self.annotation_types.append(CoordinateTransformationAnnotation.ANNOTATION_UIMA_TYPE_NAME)
        
    def process(self, cas):
        x = cas['_views']['_InitialView']['MetadataSelectedBlock'][0]['x']
        y = cas['_views']['_InitialView']['MetadataSelectedBlock'][0]['y']
        z = cas['_views']['_InitialView']['MetadataSelectedBlock'][0]['z']
        
        coords = KinectCoords(x,y,z)
        coords = self.rotateCoordSystemAroundHorizontalAxis(coords, self.angleOfKinect)
        coords = self.translateCoordSystemHorizontally(coords, self.distanceRightOfRobot * -1)
        coords = self.translateCoordSystemVertically(coords, self.heightFromTable)
        
#         print('robot X: ', coords.x)
#         print('robot Y: ', coords.z)
#         print('robot Z: ', coords.y)
        annotation = CoordinateTransformationAnnotation(coords.x, coords.z, coords.y)
        self.add_annotation(annotation)
        
    def rotateCoordSystemAroundHorizontalAxis(self, kinectCoords, angle):
        angleInRadians = math.radians(angle)
        rotMatrix = numpy.array([[1,0,0,0],
                     [0,math.cos(angleInRadians),-1*math.sin(angleInRadians),0],
                     [0,math.sin(angleInRadians),math.cos(angleInRadians),0],
                     [0,0,0,1]])
        coordMatrix = numpy.array([[kinectCoords.x], 
                       [kinectCoords.y], 
                       [kinectCoords.z], 
                       [1]])
        resultMatrix = numpy.matmul(rotMatrix, coordMatrix)
        
        
        kinectCoords.x = resultMatrix[0][0]
        kinectCoords.y = resultMatrix[1][0]
        kinectCoords.z = resultMatrix[2][0]
        return kinectCoords
    
    def translateCoordSystemHorizontally(self, kinectCoords, xTransDist):
        kinectCoords.x = kinectCoords.x + xTransDist
        return kinectCoords
    
    def translateCoordSystemVertically(self, kinectCoords, height):
        kinectCoords.y = kinectCoords.y + height
        return kinectCoords

class KinectCoords:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    
class CoordinateTransformationAnnotation(AnnotationType):
    ANNOTATION_UIMA_TYPE_NAME = "edu.rosehulman.aixprize.pipeline.types.CoordinateTransformation"
    
    def __init__(self, x, y, z):
        self.name = self.ANNOTATION_UIMA_TYPE_NAME
        self.x = x
        self.y = y
        self.z = z
