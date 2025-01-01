import cv2
from config import config



def dodgeV2(image, mask):
    return cv2.divide(image, 255-mask, scale=256)


img = cv2.imread(config.IMG_PATH + 'eu.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
img_gray_inv = 255 - img_gray
img_blur = cv2.GaussianBlur(img_gray_inv,(21,21),0,0)
img_blend = dodgeV2(img_gray, img_blur)

img_color = cv2.pyrDown(img)
img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
img_color = cv2.pyrUp(img_color)



while cv2.waitKey(1)!=27:
    cv2.imshow('teste',img_gray)

cv2.destroyWindow('teste')