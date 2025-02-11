# main.py
# Imports
from AZ_ST7735S import AZ_ST7735S
from ImageLabel import ImageLabel
from TemperatureScreen import TemperatureScreen
from SlideShowScreen import SlideShowScreen
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
# Code to check %age of free memory on the pico can be removed
def free(full=False):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))
  
# ****************************
# *   SENSOR READING CODE    *
# ****************************

# I don't have the sensors to hand so this is dummy random number code
# Replace this
def readTemperatureSensor():
    return random.randint(15, 32)

def readHumiditySensor():
    return random.randint(10, 50)

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

#Setup Temperature Screen
temperatureScreen = TemperatureScreen("Demo &\nText", "temperature_1-2.bmp", "humidity_1-2.bmp", "fan_1-2.bmp", "decoration.bmp")
temperatureScreen.hideAll()
tft.getScreen().append(temperatureScreen.getGroup())

#Set initial values for Temperature Screen
temperatureScreen.setTemperature(readTemperatureSensor())
temperatureScreen.setHumidity(readHumiditySensor())

#Setup SlideShow Screen
slideshowScreen = SlideShowScreen()


# ****************************
# *     MAIN SCREEN LOOP     *
# ****************************
while True:
    print("Free Memory: " + free(False))
    
    tft.setBackgroundColour(temperatureScreen.getBackgroundColour())
    temperatureScreen.showAll()
    time.sleep(10)
    temperatureScreen.hideAll()
    temperatureScreen.setTemperature(readTemperatureSensor())
    temperatureScreen.setHumidity(readHumiditySensor())
    temperatureScreen.cycleBackgroundColour()
    tft.setBackgroundImage(slideshowScreen.getBackground())
    time.sleep(10)