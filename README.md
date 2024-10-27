# flipper-clone
flipper clone based around the raspberrypi pico board and some off the shelf parts 
\nthis project uses circuitpython version 8.x and you will encounter issues if you use older circuit python 7.x or 6.x libraries
### NOTE: only works if you are running each module/script separately
the pico lacks the required pins to support both the oled menu + buttons and the below mentioned parts
will be porting over this project to the pi zero w in near future
parts used:

+ pn532 rfid/nfc reader (this can do both 13.5mhz and 125 khz)
+ mrfc rfid reader(can only do 13.5mhz but is harder to use)
+ esp8266 01 wifi module (for wifi deauther based on esp deauther project by spacehuhn)
+ ssd1306 oled display(for the actual interface but takes up 2+2 for i2c version and 2+4 pins for the spi version)
+ badusb/rubber ducky(using the onboard usb port based on pico-ducky project by dbisu)



