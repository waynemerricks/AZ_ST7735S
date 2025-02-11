# AZ_ST7735S.py
# AZ Delivery 1.77" SPI TFT 128x160 Pixels ST7735S / ST7735 2.7V - 3.3V 50mA
# https://www.amazon.co.uk/AZDelivery-%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90-Display-128X160-Pixels/dp/B078JBBPXK
#
#
# REQUIRES:
#
# - an RPI Pico with Adafruit Circuit Python already installed
#   Currently Circuit Python 9.2.4 https://circuitpython.org/board/raspberry_pi_pico/
# - Adafruit circuit python libraries (not all of it only the parts you want to use)
#   Currently adafruit-circuitpython-bundle-9.x-mpy-20250208.zip
#   https://circuitpython.org/libraries
#   Unzip and copy these files to the pico / lib directory:
#    - adafruit_display_shapes directory (for drawing rectangles etc)
#    - adafruit_display_text directory (for drawing labels/text)
#    - adafruit_st7735r.mpy (driver file for the screen)
#
# WIRING:
#
# TFT Pin 1 - GND  --> Pico Pin 38 GND
# TFT Pin 2 - VCC  --> Pico Pin 40 VBUS (Should be USB 5v)
# TFT Pin 3 - SCK  --> Pico Pin 24 GP18 | SPI0 SCK
# TFT Pin 4 - SDA  --> Pico Pin 25 GP19 | SPI0 TX
# TFT Pin 5 - RES  --> Pico Pin 21 GP16 | SPI0 RX
# TFT Pin 6 - RS   --> Pico Pin 26 GP20
# TFT Pin 7 - CS   --> Pico Pin 22 GP17 | SPI0 CSn
# TFT Pin 8 - LEDA --> Pico Pin 36 3V3 (Out) - This will always display at full brightness you need to PWM control this pin to change brightness levels
#
# ***
# *** WARNING:
# *** DO NOT plug TFT Pin 8 into VBUS by mistake as it will send 5V to the screen and potentially damage it
# *** 
#
# REFERENCES:
#
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
# https://learn.adafruit.com/1-8-tft-display/circuitpython-displayio-quickstart-2
# https://learn.adafruit.com/circuitpython-display-support-using-displayio
# https://www.az-delivery.uk/products/1-77-zoll-tft-display-kostenfreies-e-book
# JVickers Comment about DC pin and ebook: https://www.amazon.co.uk/AZDelivery-%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90-Display-128X160-Pixels/dp/B078JBBPXK
# -  "RS is the same as DC/A0 that you see on other displays"
# https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf
# https://docs.circuitpython.org
# https://educ8s.tv/raspberry-pi-pico-color-display-st7735-tutorial/ - Pin outs don't work with this screen and setup shown here
# - I'm not sure why these pinouts are non-working however there were some comments about the PICO having 2 different SPI pins/buses
#   one of which is incompatible with this screen.  This set up seems to be the incompatible one which is labeled as SPI1 on the Pico (this may be my misunderstanding).
# https://www.youtube.com/watch?v=qym-P4GTdIU - educ8s video benchmarking actually contains different pinouts that work
# - Code with above video example: https://github.com/educ8s/CircuitPython-Pi-Calculation-Benchmark/blob/main/code.py
# - This uses pin outs from the Pico labeled as SPI0.  I didn't change my original code other than to reflect the new pins and everything started working
#   after this change.  My theory is SPI0 is required for this screen although I still don't understand why SPI1 and 0 are different.
#
# *****************
# *               *
# * AZ_ST7735S.py *
# *               *
# *****************
#
#
# Code imports for Screen
import busio, board #Pico and Lower Level Stuff
from adafruit_st7735r import ST7735R #Screen Driver
import displayio, terminalio #Graphics stuff
from adafruit_display_text import label #Text Label 

class AZ_ST7735S:
    # ****************************
    # *    INTERNAL VARIABLES    *
    # ****************************
    # TFT Pins Definitions - These are where the wiring from the screen need to go on the Pico
    __tft_cs  = board.GP17 #also called the chip select pin
    __tft_dc  = board.GP20 #also called the command pin | this TFT labels it as RS for some reason
    __tft_sck = board.GP18 #also called the clock pin
    __tft_sda = board.GP19 #also called the MOSI pin
    __tft_res = board.GP16 #also called the reset pin

    # TFT Dimensions in Pixels
    __tft_width=128
    __tft_height=160

    # TFT Orientation 90 = Landscape left to right, 0 = Portrait, 180 = Portrait upside down, 270 = landscape right to left
    __tft_orientation=90

    # Reference to screen once initialised
    __tft_screen = None

    # Background Set
    __hasBackground = False
    
    # ****************************
    # *   FUNCTION DEFINITIONS   *
    # ****************************
    #
    # function initialiseScreen
    # This does all the behind the scenes screen setup with the driver and a canvas for drawing onto
    # @param orientation: 0 = Portrait, 90 = Landscape left to right, 180 = Upside Down, 270 = Landscape right to left
    def initialiseScreen(self, orientation):
        self.__tft_orientation=orientation

        # Release any resources that may already be in use (from previous code runs)
        displayio.release_displays()

        # Setup Screen communication with SPI
        SPI = busio.SPI(clock=self.__tft_sck, MOSI=self.__tft_sda)
        display_bus = displayio.FourWire(SPI, command=self.__tft_dc, chip_select=self.__tft_cs, reset=self.__tft_res)

        # Setup Screen Driver
        # if landscape swap width and height
        if self.__tft_orientation == 90 or self.__tft_orientation == 270:
            tmp = self.__tft_width
            self.__tft_width = self.__tft_height
            self.__tft_height = tmp

        # This screen has reverse order RGB (bgr) colour values so we need to set bgr = True otherwise colours are backwards
        # (e.g. you use blue but see red if you don't set this to True)
        display = ST7735R(display_bus, width=self.__tft_width, height=self.__tft_height, rotation=self.__tft_orientation, bgr=True)

        # Get a screen reference that allows us to put groups of items onto it
        self.__tft_screen = displayio.Group()

        # Set the display to use our screen group
        display.root_group = self.__tft_screen
        
        # Set the screen to black
        self.setBackgroundColour(0x000000)
        
    # function getScreen
    # Gets a reference to screen, if it hasn't been initialised yet, it will do so with default values
    # @return reference to TFT screen to use for drawing
    def getScreen(self):
        if self.__tft_screen == None:
            self.initialiseScreen(self.__tft_orientation)
        
        return self.__tft_screen
    
    def getWidth(self):
        return self.__tft_width
    
    def getHeight(self):
        return self.__tft_height
    
    def getOrientation(self):
        return self.__tft_orientation

    # Creates an adafruit_display_text -> label at the given co-ordinates
    # @param x = x co-ordinate to display label
    # @param y = y co-ordinate to display label
    # @param colour = Hex value for colour (same as HTML e.g. 0x0000FF = Blue)
    # @param text = Text to display, if the text is too long, it will go off the screen
    # @return Label you can append to a display group
    def createLabel(self, x, y, colour, text):
        return label.Label(terminalio.FONT, text=text, color=colour, x=x, y=y)
    
    # Sets layer 0 to the given colour
    # @param colour = Hex value for colour (same as HTML e.g. 0x0000FF = Blue)
    def setBackgroundColour(self, colour):
        
        color_bitmap = displayio.Bitmap(self.__tft_width, self.__tft_height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = colour
        background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette,x=0, y=0)
        
        # If we have a background already, remove it and replace with new colour
        if self.__hasBackground:
            #Remove Layer 0
            self.__tft_screen.pop(0)
            
        #Put this as layer 0
        self.__tft_screen.insert(0, background)        
        self.__hasBackground = True
        
    # Sets layer 0 to an image from disk stored on the pico under /images
    def setBackgroundImage(self, imageFile):
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap("/images/" + imageFile)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        
        if self.__hasBackground:
            #Remove Layer 0
            self.__tft_screen.pop(0)
        
        self.__tft_screen.insert(0, tile_grid)
        self.__hasBackground = True
