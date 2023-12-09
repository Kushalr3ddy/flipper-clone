import time
import board
import digitalio
#import simpleio
import busio
import mfrc522




sck = board.GP6  # SPI clock pin
mosi = board.GP7  # SPI MOSI pin TX
miso = board.GP8  # SPI MISO pin RX

spi = busio.SPI(clock=sck, MOSI=mosi, MISO=miso)  # Create SPI bus
cs = digitalio.DigitalInOut(board.GP9)  # SPI chip select pin
rst = digitalio.DigitalInOut(board.GP12)  # MFRC522 reset pin

rfid = mfrc522.MFRC522(spi, cs, rst)  # Initialize MFRC522 reader
rfid.set_antenna_gain(0x07 << 4)  # Set antenna gain to maximum

print("\n***** Scan your RFID tag/card *****\n")

prev_data = ""  # Previous UID data
prev_time = 0  # Previous time stamp
timeout = 1  # Timeout in seconds

while True:
    (status, tag_type) = rfid.request(rfid.REQALL)  # Request any card type

    if status == rfid.OK:
        (status, raw_uid) = rfid.anticoll()  # Get card UID

        if status == rfid.OK:
            rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])  # Format UID as a string

            if rfid_data != prev_data:  # Check if UID is different from previous one
                prev_data = rfid_data
                print("Card detected! UID: {}".format(rfid_data))

                

                prev_time = time.monotonic()  # Update previous time stamp
            else:
                if time.monotonic() - prev_time > timeout:  # Check for timeout
                    prev_data = ""
                    print("Waiting for a new card...")

    time.sleep(0.1)  # Delay for 0.1 second