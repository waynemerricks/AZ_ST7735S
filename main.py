# main.py
# Imports
from AZ_ST7735S import AZ_ST7735S
from ImageLabel import ImageLabel
from adafruit_display_text import label #Text Label
import displayio, terminalio
import os, microcontroller, gc, random
import time

# ****************************
# *       STARTUP CODE       *
# ****************************
# This isn't needed but it is nice to see if things are actually loading
board_type = os.uname().machine
print(f"Board: {board_type}")
print(f"Cpu Frequency: {microcontroller.cpu.frequency/1000000} MHz")

# ****************************
# *       HELPER CODE        *
# ****************************
def hideAllLabels():
    temperatureLabel.getGroup().hidden = True
    humidityLabel.getGroup().hidden = True
    titleLabel.hidden = True
    pictureLabel.getGroup().hidden = True
    
def showAllLabels():
    temperatureLabel.getGroup().hidden = False
    humidityLabel.getGroup().hidden = False
    titleLabel.hidden = False
    pictureLabel.getGroup().hidden = False

def getRandomImage():
    return "slideshow/" + random.choice(os.listdir("/images/slideshow/"))

# ****************************
# *      SCREEN SETUP        *
# ****************************
# Setup the screen rotated to be landscape
print("Initialising Screen")
tft = AZ_ST7735S()
tft.initialiseScreen(90) #0 for portrait, in theory 180 for upside down, 270 for landscape in other direction
print(f"Screen Resolution: {tft.getWidth()} x {tft.getHeight()} @ {tft.getOrientation()} degrees")


# ****************************
# *    MAIN SCREEN LAYOUT    *
# ****************************
# label = ImageLabel("Text to Show"
#                    Font Size: 1 = default, 2 = 2x default, 3 = 3x default etc.  Can only scale by whole numbers
#                    "Name of indexed bitmap with full green as transparent in slot 0" - This needs to be saved in the pico images directory
#                    X co-ordinate
#                    Y co-ordinate
#                    Number of tiles in the image defaults to 2
#                    TileWidth (Pixels) defaults to 40
#                    TileHeight (Pixels) defaults to 40
#                    True/False, True = Text to the left of picture, False = Text on the right, defaults to True
temperatureLabel = ImageLabel("34 C", 1, "temperature_1-2.bmp", 105, 5, tileWidth = 20, tileHeight = 20)
humidityLabel = ImageLabel("34 %", 1, "humidity_1-2.bmp", 105, 30, tileWidth = 20, tileHeight = 20, onLeft = False)
titleLabel = label.Label(terminalio.FONT, text="Demo &\nText", color=0xFFFFFF, x=5, y=12, scale=2)
pictureLabel = ImageLabel("", 1, "lizard.bmp", 5, 80, tileWidth = 80, tileHeight = 40)
textLabel = label.Label(terminalio.FONT, text="Hello World", color=0xFF0000, x=15, y=60, scale=2)
textLabel.hidden = True

# Add Labels to screen
tft.getScreen().append(temperatureLabel.getGroup())
tft.getScreen().append(humidityLabel.getGroup())
tft.getScreen().append(titleLabel)
tft.getScreen().append(pictureLabel.getGroup())
tft.getScreen().append(textLabel)
time.sleep(3)

# ****************************
# *     MAIN SCREEN LOOP     *
# ****************************
while True:
    # Show bitmap picture
    tft.setBackgroundImage(getRandomImage())
    hideAllLabels()
    time.sleep(3)

    # Set screen colour to Blue
    tft.setBackgroundColour(0x0000FF)
    temperatureLabel.togglePicture() #can also do temperatureLabel.changePicture(0) for first tile, (1) for second tile
    temperatureLabel.changeText("37 C")
    humidityLabel.togglePicture()
    humidityLabel.changeText("32 %")
    showAllLabels()
    time.sleep(3)

    # Show bitmap picture
    tft.setBackgroundImage(getRandomImage())
    hideAllLabels()
    time.sleep(3)
    
    # Set screen colour to Red
    tft.setBackgroundColour(0xFF0000)
    temperatureLabel.togglePicture()
    temperatureLabel.changeText("39 C")
    humidityLabel.togglePicture()
    humidityLabel.changeText("24 %")
    showAllLabels()
    time.sleep(3)
    
    # Show bitmap picture
    tft.setBackgroundImage(getRandomImage())
    hideAllLabels()
    time.sleep(3)

    # Show bitmap picture and labels
    tft.setBackgroundImage(getRandomImage())
    temperatureLabel.togglePicture()
    temperatureLabel.changeText("32 C")
    humidityLabel.togglePicture()
    humidityLabel.changeText("15 %")
    showAllLabels()
    time.sleep(3)

    # Show bitmap picture
    tft.setBackgroundImage(getRandomImage())
    hideAllLabels()
    time.sleep(3)
    
    # Set screen colour to Green
    tft.setBackgroundColour(0x00FF00)
    temperatureLabel.togglePicture()
    temperatureLabel.changeText("35 C")
    humidityLabel.togglePicture()
    humidityLabel.changeText("18 %")
    showAllLabels()
    time.sleep(3)
    
    # Set screen to black and show time
    tft.setBackgroundColour(0x000000)
    hideAllLabels()
    textLabel.hidden = False
    time.sleep(5)
    textLabel.hidden = True
    
