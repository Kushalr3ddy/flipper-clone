# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support


import supervisor


import time
import digitalio
from board import *
import board
from duckyinpython import *
if(board.board_id == 'raspberry_pi_pico_w'):
    import wifi
    from webapp import *

###############################################
# Adapting the example in https://learn.adafruit.com/adafruit-oled-featherwing/python-usage
# to use with Raspberry Pi Pico and CircuitPython

import board
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

i2c = busio.I2C (scl=board.GP5, sda=board.GP4) # This RPi Pico way to call I2C

display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1) # Full screen white
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White
 
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
 
# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 54, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
splash.append(inner_sprite)
 
# Draw a label
text = "Nicolau dos"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
splash.append(text_area)

text = "Brinquedos"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=32, y=25)
splash.append(text_area)
 
while True:
    pass




###############################################







# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)

def startWiFi():
    import ipaddress
    # Get wifi details and more from a secrets.py file
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    print("Connect wifi")
    #wifi.radio.connect(secrets['ssid'],secrets['password'])
    wifi.radio.start_ap(secrets['ssid'],secrets['password'])

    HOST = repr(wifi.radio.ipv4_address_ap)
    PORT = 80        # Port to listen on
    print(HOST,PORT)

# turn off automatically reloading when files are written to the pico
#supervisor.disable_autoreload()
supervisor.runtime.autoreload = False

if(board.board_id == 'raspberry_pi_pico'):
    led = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)
elif(board.board_id == 'raspberry_pi_pico_w'):
    led = digitalio.DigitalInOut(board.LED)
    led.switch_to_output()


progStatus = False
progStatus = getProgrammingStatus()
print("progStatus", progStatus)
if(progStatus == False):
    print("Finding payload")
    # not in setup mode, inject the payload
    payload = selectPayload()
    print("Running ", payload)
    runScript(payload)

    print("Done")
else:
    print("Update your payload")

led_state = False

async def main_loop():
    global led,button1

    button_task = asyncio.create_task(monitor_buttons(button1))
    if(board.board_id == 'raspberry_pi_pico_w'):
        pico_led_task = asyncio.create_task(blink_pico_w_led(led))
        print("Starting Wifi")
        startWiFi()
        print("Starting Web Service")
        webservice_task = asyncio.create_task(startWebService())
        await asyncio.gather(pico_led_task, button_task, webservice_task)
    else:
        pico_led_task = asyncio.create_task(blink_pico_led(led))
        await asyncio.gather(pico_led_task, button_task)

asyncio.run(main_loop())
