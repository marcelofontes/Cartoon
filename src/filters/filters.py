import cv2
from abc import ABC, abstractmethod
from scipy.interpolate import UnivariateSpline
import numpy as np
from ..utils import create_LUT_8UC1

"""
a Filter is an action. Any type of action must follow the base class estruture (interface) below and must have the _run Method implemented
"""

class Filter(ABC):
    """Abstract Class for transformations"""
    def __init__(self):
        self._image = None
        self._filteredImage = None

    @abstractmethod
    def _run(self, image):
        """process Transforming imagem"""
        return 
    
    
    def render(self, image):
        """return the transformed image"""
        self._image = image
        self._filteredImage = self._run(self._image)
        return self._filteredImage



class CoolingFilter(Filter):
    
    def __init__(self):
        self.incr_ch_lut = create_LUT_8UC1([0,64,128,192,256],
                                           [0,70,140,210,256])
        self.decr_ch_lut = create_LUT_8UC1([0,64,128,192,256], 
                                           [0,30,80,120,192])
    
    
    def _run(self, img_rgb):
        c_r, c_g, c_b = cv2.split(img_rgb)
        c_r = cv2.LUT(c_r, self.incr_ch_lut).astype(np.uint8)
        c_b = cv2.LUT(c_b, self.decr_ch_lut).astype(np.uint8)
        img_rgb = cv2.merge((c_r, c_g, c_b))
        
        c_b =cv2.LUT(c_b, self.decr_ch_lut).astype(np.uint8)
        
        #increase color saturation
        c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
        c_s = cv2.LUT(c_s, self.incr_ch_lut).astype(np.uint8)
        return cv2.cvtColor(cv2.merge((c_h, c_s, c_v)), cv2.COLOR_HSV2RGB)
        

class WarmingFilter(Filter):
    
    def __init__(self):
        self.incr_ch_lut = create_LUT_8UC1([0,64,128,192,256], [0,70,140,210,256])
        self.decr_ch_lut = create_LUT_8UC1([0,64,128,192,256], [0,30,80,120,192])
    
    
    def _run(self, img_rgb):
        c_r, c_g, c_b = cv2.split(img_rgb)
        c_r = cv2.LUT(c_r, self.decr_ch_lut).astype(np.uint8)
        c_b = cv2.LUT(c_b, self.incr_ch_lut).astype(np.uint8)
        img_rgb = cv2.merge((c_r, c_g, c_b))
        
        # decrease color saturation
        c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
        c_s = cv2.LUT(c_s, self.decr_ch_lut).astype(np.uint8)
        return cv2.cvtColor(cv2.merge((c_h, c_s, c_v)), cv2.COLOR_HSV2RGB)



        
        

