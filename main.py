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
# *    SETTING VARIABLES     *
# ****************************
TEN_SECONDS = 10000 #10 seconds in millis for use with time compare
ANIMATE_DELAY = 250 #time between animate calls for screen items in millis 250 = 4 frames/updates per second
SENSOR_DELAY = 2000 #2 seconds in millis for time between sensor updates

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
  
def convertToMillis(nanoSeconds):
    return nanoSeconds // 1000000 #divide discarding remainder

# Get system uptime now in millis (we use nanoseconds because the normal time
# in millis is only accurate ish for the first couple of hours the system is
# turned on)
# @see https://learn.adafruit.com/clue-sensor-plotter-circuitpython/time-in-circuitpython#time-dot-monotonic-3060336.
def getNow():
    return convertToMillis(time.monotonic_ns())

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
    
    # Each "screen" will stay on for 10 seconds but we need to move away from time.sleep
    # in order to animate/do other things while waiting
    startTime = getNow()
    lastAnimate = startTime
    lastSensorUpdate = startTime
    
    tft.setBackgroundColour(temperatureScreen.getBackgroundColour())
    temperatureScreen.showAll()
    
    #Keep showing for 10 seconds
    
    while getNow() - startTime < TEN_SECONDS:
        
        #Check if we need to animate
        if getNow() - lastAnimate >= ANIMATE_DELAY:
            temperatureScreen.animate()
            lastAnimate = getNow()
        
        #Check/Update sensors
        if getNow() - lastSensorUpdate >= SENSOR_DELAY:
            temperatureScreen.setTemperature(readTemperatureSensor())
            temperatureScreen.setHumidity(readHumiditySensor())
            lastSensorUpdate = getNow()
            
        time.sleep(0.1) #sleep for 1/10 second so we don't peg the CPU while waiting on this screen
    
    #Finished so hide this screen
    temperatureScreen.hideAll()
    temperatureScreen.cycleBackgroundColour()
    temperatureScreen.toggleFan() #just for fan example, swap this based on sensor information
    
    #Next Screen
    tft.setBackgroundImage(slideshowScreen.getBackground())
    time.sleep(10) #not doing anything useful here so just sleep