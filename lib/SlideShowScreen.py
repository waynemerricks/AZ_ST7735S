# SlideShowScreen.py
# Sets up a landscape screen 160 x 128 with a full screen image
# based on indexed bmps stored in /images/slideshow (by default)
import random, os

class SlideShowScreen:
    __slideshowDir = None
    __path = None
    
    def __init__(self, parentPath = "/images", slideshowDir = "slideshow"):
        self.__path = parentPath
        self.__slideshowDir = slideshowDir
        
    def _getRandomImage(self):
        return self.__slideshowDir + "/" + random.choice(os.listdir(self.__path + "/" + self.__slideshowDir + "/"))
    
    def getBackground(self):
        return self._getRandomImage()
