import cv2
from config.config import IMG_PATH
from src.Canvas import Canvas


img = cv2.imread(IMG_PATH + 'face3.jpg')
wnd = Canvas(img)
wnd.run()