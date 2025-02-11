# ImageLabel.py
# Creates a displayio label with an image either to the right or left hand side
# This uses tiles to allow you to change the image to a given tile in the original bitmap
from adafruit_display_text import label #Text Label
import displayio, terminalio
import adafruit_imageload

class ImageLabel:
    # ****************************
    # *    INTERNAL VARIABLES    *
    # ****************************
    __text = None
    __label = None
    __picture = None
    __canvas = None
    __tileGrid = None
    __currentTile = 0
    __numberOfTiles = 0
    
    # function __init__
    # Sets up the ImageLabel
    # @param self: ignore this, weird Python conventions, won't mention this again in rest of class
    # @param text: Text for the label
    # @param textSize: Multiplier for Font size.  Has to be an Integer, starts at 1 for 1x system size.
    # @param imagePath: file name inside /images on the Pico
    # @param xPos: x position of the label relative to the parent group
    # @param yPos: y position of the label relative to the parent group
    # @param numberOfTiles [2]: Number of changeable tiles in the given image, defaults to 2
    # @param tileWidth [40]: Width of a tile in pixels, defaults to 40
    # @param tileHeight [40]: Height of a tile in pixels, defaults to 40
    # @param onLeft [True]: Put text on the left, defaults to True (on right if False)
    def __init__(self, text, textSize, imagePath, xPos, yPos, numberOfTiles = 2, tileWidth = 40, tileHeight = 40, onLeft = True):
        
        # Set Up the canvas variable
        self.__canvas = displayio.Group(x = xPos, y = yPos)
        
        # Set Up the label variable
        self.__text = text
        
        # Set up the number of tiles variable
        self.__numberOfTiles = numberOfTiles
        
        # Set Up the picture and pull out the palette so we can set index 0 to transparent
        self.__picture, palette = adafruit_imageload.load("/images/" + imagePath, bitmap=displayio.Bitmap, palette=displayio.Palette)
        palette.make_transparent(0)
        
        # Create a TileGrid to hold the bitmap
        # The onLeft offset to clear the text is a bit of a hack based on chars * 6 * scale + 4 for a bit of a buffer
        # There doesn't seem to be a built in way to do this without more external libraries
        if onLeft:
            self.__tileGrid = displayio.TileGrid(self.__picture, pixel_shader=palette, x = (self._textLength() * 6 * textSize) + 4, width = 1, height = 1, tile_width = tileWidth, tile_height = tileHeight, default_tile = 0)
        else:
            self.__tileGrid = displayio.TileGrid(self.__picture, pixel_shader=palette, x = 0, width = 1, height = 1, tile_width = tileWidth, tile_height = tileHeight, default_tile = 0)
        
        # Create the label for the picture
        if onLeft:
            self.__label = self._createLabel(0, int(self.__picture.height / 2), 0xFFFFFF, self.__text, textSize)
        else:
            self.__label = self._createLabel(int(self.__picture.width / self.__numberOfTiles) + 4, int(self.__picture.height / 2), 0xFFFFFF, self.__text, textSize)
        
        # Add to canvas
        self.__canvas.append(self.__tileGrid)
        self.__canvas.append(self.__label)
    
    # function _textLength
    # Checks string for \n if so splits string and finds longest of each substring
    # This can then be used to determine label picture offset
    # @return string length or longest segment length if it contains \n
    def _textLength(self):
        length = -1
        
        if "\n" not in self.__text:
            length = len(self.__text)
        else:            
            tmpText = self.__text.split("\n")
            
            for sub in tmpText:
                if len(sub) > length:
                    length = len(sub)
        
        return length
    
    # function _createLabel
    # Internal method to create an adafruit Label
    # @param x: X co-ordinate for label relative to this ImageLabel
    # @param y: Y co-ordinate for label relative to this ImageLabel
    # @param text: Text to display
    # @param scale: Scale of text to display
    # @return adafruit Label object
    def _createLabel(self, x, y, colour, text, scale):
        return label.Label(terminalio.FONT, text=text, color=colour, x=x, y=y, scale=scale)
    
    # function getGroup
    # Gets the displayio.Group that this object holds
    # Need this in order to add to the screen
    # @return displayio.Group: self.__canvas
    def getGroup(self):
        return self.__canvas
    
    # function changePicture
    # Changes the picture of this label to the given tile number
    # @param tileNo: Tile number to change to (there is no checking for out of bounds so be careful)
    def changePicture(self, tileNo):
        self.__tileGrid[0] = tileNo
        self.__currentTile = tileNo
        
    # function togglePicture
    # Changes the picture of this label to the next tile, loops around to 0 if out of range
    def togglePicture(self):
        
        self.__currentTile += 1
        
        if self.__currentTile >= self.__numberOfTiles:
            self.__currentTile = 0
        
        self.changePicture(self.__currentTile)
    
    # function changeText
    # Changes the text on this label
    # There is no resizing of the picture on the screen so stick to the same text length
    # @param text: Text to change label to
    def changeText(self, text):
        self.__label.text = text

#pictureLabel = ImageLabel("Test", 2, "test.bmp", 50, 50, 2, 40, 40)