# flipper-clone
flipper clone based around the raspberrypi pico board and some off the shelf parts 
this project uses circuitpython version 8.x and you will encounter issues if you use older circuit python 7.x or 6.x libraries
### NOTE: this project is still in development and only few functionalities work as of now
parts used:
pn532 rfid/nfc reader (this can do both 13.5mhz and 125 khz)
mrfc rfid reader(can only do 13.5mhz but is harder to use)
esp8266 01 wifi module (for wifi deauther based on esp deauther project by spacehuhn)
ssd1306 oled display(for the actual interface)
badusb/rubber ducky(using the onboard usb port based on pico-ducky project by dbisu)



TODO:
+ add ir remote code cloning functionality
+ implement interactive menu with push buttons 
+ add radio functionality
+ add bluetooth support
+ make a standalone library for easier use
+ add support for pico w
