import cv2
from .managers.CaptureManager import CaptureManager
from .managers.WindowManager import WindowManager
from .transforms.Transforms import PencilSketchTransform, CartoonTransform, CartoonTransform2
from .filters.filters import WarmingFilter, CoolingFilter

class Canvas(object):
    def __init__(self, image):
        self._windowManager = WindowManager('Cameo',self.onKeypress)
        self._captureManager = None
        self._image = image
        self._action = None         # any action like filter, transform and so on
        self._actualImage = image


    def run(self):
        """run the main loop"""
        self._captureManager = CaptureManager(self._image, self._windowManager)
        self._windowManager.createWindow()
        
        while self._windowManager.isWindowCreated:
            self._captureManager.updateImage()
            self._windowManager.processEvents()
    
    
    def onKeypress(self, keycode):
        """
            handle a keypress
            s -> save the actual image
            c -> capture actual image
            escape -> quit
        """
        
        if keycode == 115: #s- > save
            self._captureManager.capture=self._actualImage
            self._captureManager.startWritingImage('screeshot.png')
            
        elif keycode == 116: # t -> transform
            w, h, _= self._image.shape
            self._performAction(PencilSketchTransform(w,h))
                  
        elif keycode == 119: # w-> warming filter
            self._performAction(WarmingFilter())
        
        elif keycode == 100: #d-> for cooling filter
            self._performAction(CoolingFilter())
            
        elif keycode == 99: #c-> cartoon
            self._performAction(CartoonTransform())
        
        elif keycode ==117: # u -> undo
            self._captureManager.capture = self._image    
            self._actualImage=self._image
        
        elif keycode == 27: # escape   
            self._windowManager.destroyWindow()


    def _performAction(self, action):
        self._action = action
        self._actualImage = self._action.render(self._actualImage)
        self._captureManager.capture = self._actualImage

# if __name__ == "__main__":
#     Cameo().run()             
        
            
    