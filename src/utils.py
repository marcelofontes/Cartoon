import cv2
from scipy.interpolate import UnivariateSpline


def dodgeNaive(image, mask):
    return 255 - cv2.divide(255 - image, 255 - mask, scale=256)



def create_LUT_8UC1(x, y):
    spl = UnivariateSpline(x,y)
    return spl(range(256))