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
from time import sleep_ms
import sensor, image
import ubinascii
from math import floor

# ~~~~~ Setup ~~~~~
fm.register(33,fm.fpioa.UART1_TX)   # UART1_TX connects to Rxd
fm.register(34,fm.fpioa.UART1_RX)   # UART1_RX connects to Txd

uart_A = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)


# ~~~~~ Take picture ~~~~~

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000) # Let new settings take affect.

sensor.skip_frames(time = 1000) # Give the user time to get ready.

print("Taking a picture.")
image = sensor.snapshot()


ibytes = ubinascii.b2a_base64(image)
istr = str(ibytes)[2:-3]


# ~~~~~ Writing ~~~~~

LoRa_buf = 500

write_str = istr
print("Size of image string is: ", len(write_str),"\n\n")
for i in range(floor(len(write_str)/LoRa_buf)): #for imageSize/500 times
    print(write_str[i*LoRa_buf:(i+1)*LoRa_buf]) #print 500 bytes at a time
    sleep_ms(10)

print("\nImage string complete.\n")



sleep_ms(500)

# ~~~~~ Clean up ~~~~~
uart_A.deinit()
del uart_A



# reference: https://wiki.sipeed.com/soft/maixpy/en/api_reference/machine/uart.html
