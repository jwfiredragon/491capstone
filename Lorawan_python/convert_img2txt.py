# Simple LoRaWAN py program
# To run: Connect Pins as shown:
#
# Lora :  MCU
# M0  -> pin 31
# M1  -> pin 32
# Rxd -> pin 33
# Txd -> pin 34
# AUX -> pin 35
# Vcc -> 3.3V
# Gnd -> Gnd

from fpioa_manager import fm
from machine import UART
from Maix import GPIO
from time import sleep_ms
import sensor, image
import ubinascii
from math import floor

# ~~~~~ Set mode pins ~~~~~

    # "class GPIO(ID, MODE, PULL, VALUE)"

#p_M0 = GPIO(GPIOHS31, GPIO.OUT, GPIO.PULL_NONE)
#p_M1 = GPIO(GPIOHS32, GPIO.OUT, GPIO.PULL_NONE)
#p_M0.value(0)
#p_M1.value(0)

# ~~~~~ Setup ~~~~~
fm.register(33,fm.fpioa.UART1_TX)   # UART1_TX connects to Rxd
fm.register(34,fm.fpioa.UART1_RX)   # UART1_RX connects to Txd

uart_A = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)


# ~~~~~ Take picture ~~~~~

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

sensor.skip_frames(time = 1000) # Give the user time to get ready.

print("\nTaking a picture.\n")
image = sensor.snapshot()



# ~~~~~ Writing ~~~~~

LoRa_buf = 500  # LoraWAN buffer is 512 bytes

image = image.compressed(quality=20)        # compress image to reduce size
ibytes = image.to_bytes()                   # convert image to binary
print("bytes length: %d bytes[0]: " %(len(jpeg_bytes))  # print byte length
istr = (ubinascii.hexlify(ibytes))          # convert binary to hex

write_str = istr        # data to print/transmit
print("Size of image string is: ", len(write_str),"\n\n")   # print length of transmitted string
for i in range(floor(len(write_str)/LoRa_buf)):             # send 500 bytes at a time
    print(write_str[i*LoRa_buf:(i+1)*LoRa_buf], end='')     # Print hex string. Note that this will print b'...' each loop
    #uart_A.write(write_str[i*LoRa_buf:(i+1)*LoRa_buf])    # send over UART
    sleep_ms(20)

print("\nImage string complete.\n")

#write_str = "Example. "
#for i in range(10):
    #uart_A.write(write_str)
    #sleep_ms(20)

sleep_ms(500)


# ~~~~~ Reading ~~~~~
for i in range(100):
#while(True):

    if uart_A.any():
        read_data = uart_A.read()
        read_str = read_data.decode('utf-8')
        print("string = ",read_str)
    #else:
        #print("not available")

    sleep_ms(10)


# ~~~~~ Clean up ~~~~~
uart_A.deinit()
del uart_A



# reference: https://wiki.sipeed.com/soft/maixpy/en/api_reference/machine/uart.html
