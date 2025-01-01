import cv2


class CaptureManager(object):
    
    def __init__(self, image, windowManager):
        self._image = image # imagem aberta do arquivo
        # self._isWritingImage = None
        self._capture = None # imagem capturada na tela
        self._imageFilename = None
        self._windowManager = windowManager
        self._resizeImage(self._image)
    
    
    @property
    def isWritingImage(self):
        return self._imageFilename is not None
    
        
    @property
    def capture(self):
        return self._capture
    
    @property
    def image(self):
        return self._image
    
    
    @capture.setter
    def capture(self, image):
        self._capture=image
    
    
    
    def updateImage(self):
        
        if self._capture is not None:
            self._windowManager.show(self._capture)
        else:
            self._windowManager.show(self._image)
        
        #checa se tem captura para salvar
        if self.isWritingImage:
            self.writeImage(self._imageFilename)
    
    
    def startWritingImage(self, filename):
        self._imageFilename = filename
        
    
    def writeImage(self, filename):
        """write the image to file"""
        cv2.imwrite(filename, self._capture)
        self._imageFilename = None
        
        
    def _resizeImage(self, image):
        x,y,_ = self._image.shape
        ar = y/x
        print(x,y)
        if x>600 or y > 400:
            x=int(600)
            y=int(x/ar)
            dim=(x,y)
            print(dim)
            self._image = cv2.resize(self._image, (x,y))