# TemperatureScreen.py
# Sets up a landscape screen 160 x 128
#  ---------------------
#  | TITLE       temp  |
#  | TITLE       humid |
#  |             fan   |
#  | DECORATION        |
#  ---------------------
from ImageLabel import ImageLabel #Label with a picture
from adafruit_display_text import label #Text Label
import terminalio, displayio

class TemperatureScreen:
    # ****************************
    # *    SETTINGS VARIABLES    *
    # ****************************
    __COLD = 19 #too cold = this or below
    __HOT  = 27 #too hot = this or above
    __WET  = 40 #too humid/wet = this or above
    __DRY  = 15 #too dry = this or below
    
    #
    # ****************************
    # *    INTERNAL VARIABLES    *
    # ****************************
    __title = None
    __temperatureLabel = None
    __humidityLabel = None
    __decorationLabel = None
    __fanLabel = None
    __temperature = ""
    __humidity = ""
    __background = None
    __backgroundImage = False
    __fanOn = False
    __Group = None
    __backgroundColours = [
        0x000000,#black
        0xFF0000,#red
        0x00FF00,#green
        0x0000FF,#blue
        0xFFFF00,#yellow
        0x00FFFF,#light_blue
        0xFF00FF #purple
    ]
    __colourIndex = 0
    
    def __init__(self, title, temperatureTileBMP, humidityTileBMP, fanTileBMP, decorationBMP):
        self.__title = label.Label(terminalio.FONT, text=title, color=0xFFFFFF, x=5, y=12, scale=2)
        self.__temperatureLabel = ImageLabel("99 C", 1, temperatureTileBMP, 105, 5, tileWidth = 20, tileHeight = 20, numberOfTiles = 3)
        self.__humidityLabel = ImageLabel("99 %", 1, humidityTileBMP, 105, 30, tileWidth = 20, tileHeight = 20, numberOfTiles = 3)
        self.__fanLabel = ImageLabel("Off ", 1, fanTileBMP, 105, 55, tileWidth = 20, tileHeight = 20)
        self.__decorationLabel = ImageLabel("", 1, decorationBMP, 5, 90, tileWidth = 49, tileHeight = 40)
        
        self.__background = self.__backgroundColours[0]
        
        self.__Group = displayio.Group()
        self.__Group.append(self.__title)
        self.__Group.append(self.__temperatureLabel.getGroup())
        self.__Group.append(self.__humidityLabel.getGroup())
        self.__Group.append(self.__fanLabel.getGroup())
        self.__Group.append(self.__decorationLabel.getGroup())
    
    def getGroup(self):
        return self.__Group
    
    def hideAll(self):
        self.__Group.hidden = True
        
    def showAll(self):
        self.__Group.hidden = False

    def setBackgroundImage(self, imagePath):
        self.__backgroundImage = True
        self.__background = imagePath
    
    def getBackgroundColour(self):
        if self.__backgroundImage == True:
            self.cycleBackgroundColour()
        
        return self.__background
    
    def setBackgroundColour(self, colour):
        self.__backgroundImage = False
        self.__background = colour
    
    def cycleBackgroundColour(self):
        self.__colourIndex += 1
        
        if self.__colourIndex >= len(self.__backgroundColours):
            self.__colourIndex = 0
            
        self.__backgroundImage = False
        self.__background = self.__backgroundColours[self.__colourIndex]
        
    def isBackgroundImage(self):
        return self.__backgroundImage
    
    def getBackground(self):
        return self.__background
    
    def changeTitleText(self, text):
        self.__title.text = text
        
    def changeTitleColour(self, colour):
        self.__title.color = colour
        
    def setTemperature(self, temperature):
        if self.__temperature != temperature:
            self.__temperature = temperature
            self.__temperatureLabel.changeText(str(temperature) + " C")
        
            if temperature <= self.__COLD:
                self.setTemperatureCold()
            elif temperature >= self.__HOT:
                self.setTemperatureHot()
            else:
                self.setTemperatureOK()
    
    def setFanOn(self):
        self.__fanOn = True
        self.__fanLabel.changeText("On")
        self.animate()
        
    def setFanOff(self):
        self.__fanOn = False
        self.__fanLabel.changeText("Off")
    
    def setHumidity(self, humidity):
        if self.__humidity != humidity:
            self.__humidity = humidity
            self.__humidityLabel.changeText(str(humidity) + " %")
        
            if humidity >= self.__WET:
                self.setHumidityHigh()
            elif humidity <= self.__DRY:
                self.setHumidityLow()
            else:
                self.setHumidityOK()
        
    def setTemperatureHot(self):
        self.__temperatureLabel.changePicture(1)
    
    def setTemperatureCold(self):
        self.__temperatureLabel.changePicture(0)
    
    def setTemperatureOK(self):
        self.__temperatureLabel.changePicture(2)
    
    def setHumidityHigh(self):
        self.__humidityLabel.changePicture(0)
        
    def setHumidityLow(self):
        self.__humidityLabel.changePicture(1)
    
    def setHumidityOK(self):
        self.__humidityLabel.changePicture(2)
    
    def animate():
        #Change fan picture if we're turned to on
        if self.__fanOn:
            self.__fanLabel.togglePicture()
            
#test = TemperatureScreen("Example &\nTitle", "temperature_1-2.bmp", "humidity_1-2.bmp", "fan_1-2.bmp", "decoration.bmp")