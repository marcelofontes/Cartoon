import cv2
import abc
import numpy as np
from abc import ABC, abstractmethod
from ..utils import dodgeNaive


"""
a transform is an action. Any type of action must follow the base class estruture (interface) below and must have the _run Method implemented
"""

class Transform(ABC):
    """Abstract Class for transformations"""
    def __init__(self):
        self._image = None
        self._transformedImage = None

    @abstractmethod
    def _run(self, image):
        """process Transforming imagem"""
        return 
    
    
    def render(self, image):
        """return the transformed image"""
        self._image = image
        self._transformedImage = self._run(self._image)
        return self._transformedImage



class PencilSketchTransform(Transform):
    """Apply pencil like Transform"""
    
    def __init__(self, width, height, bg_gray=None):
        self._width = width
        self._height = height
        self._backGround = None
        if bg_gray is not None:
            self._backGround = cv2.imread(bg_gray, cv2.CV_8UC1)
        
        if self._backGround is not None:
            self._backGround = cv2.resize(self._backGround, self._width, self._height)
        
        
    def _run(self, image_rgb):

        
        img_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
        img_blur= cv2.GaussianBlur(img_gray, (35,35), 0, 0)
        img_blend = cv2.divide(img_gray, img_blur, scale=256)
        
        if self._backGround is not None:
            img_blend = cv2.multiply(img_blend, self._backGround, scale=1./256)
        
        return cv2.cvtColor(img_blend, cv2.COLOR_GRAY2BGR)
 
        
class CartoonTransform(Transform):
    
    def _run(self, img_rgb, num_iter=2):
        numDownSamples = 1
        numBilateralFilters = num_iter
        img_color = img_rgb
        
        #downsample image using Gaussian pyramid
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)
            
        #  repeatedly apply small bilateral filter instead of applying one large filter
        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=15, sigmaSpace=10)
        
        # upsample image to original size
        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)
        
        # convert to grayscale and appl median blur
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)
        # img_blur = cv2.GaussianBlur(img_gray, (21,21), 0)
        
        # detect and enhance edges
        img_edge = cv2.adaptiveThreshold(img_blur, 255, 
                                         cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY,7,2)
        
        # convert back to color so that it cab be bit-ANDed with color image
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        
        return cv2.bitwise_and(img_color, img_edge)
        


class CartoonTransform2(Transform):

    def _run(self, image):
        
        Gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        Blur_image = cv2.GaussianBlur(Gray_image, (11, 11), 0)
        detect_edge = cv2.adaptiveThreshold(Blur_image, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 3)

        output = cv2.bitwise_and(image, image, mask=detect_edge)

       
        return output