# AZ_ST7735S
Circuit Python using a Raspberry Pi Pico with an AZ Delivery 1.77" SPI TFT 128x160 screen

This is more for my own memory aid than any serious coding.  I am not a python or micro/embedded systems programmer
by a very long way!

This is a small set of Circuit Python files to get a TFT screen working with the original Raspberry Pi Pico

![pico-tft-example](https://github.com/user-attachments/assets/38c40685-3ae8-4ca8-9446-962fccebbb02)

It uses an AZ Delivery 1.77" SPI TFT (ST7735S / ST7735), google didn't help too much with the documentation for this
so this is just my cobbled together list of things to get it working as of 10/02/2025.

The screen in particular is this one from AZ Delivery / Amazon:
* AZ Delivery 1.77" SPI TFT 128x160 Pixels ST7735S / ST7735 2.7V - 3.3V 50mA
* https://www.az-delivery.uk/products/1-77-zoll-spi-tft-display
* https://www.amazon.co.uk/AZDelivery-%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90-Display-128X160-Pixels/dp/B078JBBPXK

# REQUIRES:
 - an RPI Pico with Adafruit Circuit Python already installed
   Currently Circuit Python 9.2.4 https://circuitpython.org/board/raspberry_pi_pico/
 - Adafruit circuit python libraries (not all of it only the parts you want to use)
   Currently adafruit-circuitpython-bundle-9.x-mpy-20250208.zip
   https://circuitpython.org/libraries
   Unzip and copy these files to the pico / lib directory:
    - adafruit_display_shapes directory (for drawing rectangles etc) * Not used in this example code yet
    - adafruit_display_text directory (for drawing labels/text)
    - adafruit_st7735r.mpy (driver file for the screen)

# WIRING:

 - TFT Pin 1 - GND  --> Pico Pin 38 GND
 - TFT Pin 2 - VCC  --> Pico Pin 40 VBUS (Should be USB 5v)
 - TFT Pin 3 - SCK  --> Pico Pin 24 GP18 | SPI0 SCK
 - TFT Pin 4 - SDA  --> Pico Pin 25 GP19 | SPI0 TX
 - TFT Pin 5 - RES  --> Pico Pin 21 GP16 | SPI0 RX
 - TFT Pin 6 - RS   --> Pico Pin 26 GP20
 - TFT Pin 7 - CS   --> Pico Pin 22 GP17 | SPI0 CSn
 - TFT Pin 8 - LEDA --> Pico Pin 36 3V3 (Out) - This will always display at full brightness you need to PWM control this pin to change brightness levels

 ***
 *** WARNING:
 *** DO NOT plug TFT Pin 8 into VBUS by mistake as it will send 5V to the screen and potentially damage it
 *** 

# REFERENCES:

* https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
* https://learn.adafruit.com/1-8-tft-display/circuitpython-displayio-quickstart-2
* https://learn.adafruit.com/circuitpython-display-support-using-displayio
* https://www.az-delivery.uk/products/1-77-zoll-tft-display-kostenfreies-e-book
* JVickers Comment about DC pin and ebook: https://www.amazon.co.uk/AZDelivery-%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90-Display-128X160-Pixels/dp/B078JBBPXK
  -  "RS is the same as DC/A0 that you see on other displays"
* https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf
* https://docs.circuitpython.org
* https://educ8s.tv/raspberry-pi-pico-color-display-st7735-tutorial/ - Pin outs don't work with this screen and setup shown here
  - I'm not sure why these pinouts are non-working however there were some comments about the PICO having 2 different SPI pins/buses
    one of which is incompatible with this screen.  This set up seems to be the incompatible one which is labeled as SPI1 on the Pico (this may be my misunderstanding).
* https://www.youtube.com/watch?v=qym-P4GTdIU - educ8s video benchmarking actually contains different pinouts that work
  - Code with above video example: https://github.com/educ8s/CircuitPython-Pi-Calculation-Benchmark/blob/main/code.py
  - This uses pin outs from the Pico labeled as SPI0.  I didn't change my original code other than to reflect the new pins and everything started working
    after this change.  My theory is SPI0 is required for this screen although I still don't understand why SPI1 and 0 are different.
