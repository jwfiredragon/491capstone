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
from math import floor, ceil
from board import board_info
import utime

def send_image():

    LoRa_buf = 128  # LoraWAN buffer is 512 bytes

    with open('/sd/reading.jpg', 'rb') as img:
        iraw = img.read()
        ibytes = ubinascii.hexlify(iraw)

    write_str = ibytes + b'x'        # data to print/transmit

    print("Size of image string is: ", len(write_str),"\n\n")   # print length of transmitted string - debug

    for i in range(ceil(len(write_str)/LoRa_buf)):             # send 500 bytes at a time
        print(write_str[i*LoRa_buf:(i+1)*LoRa_buf], end='')     # Print hex string. Note that this will print b'...' each loop
        uart_LoRa.write(write_str[i*LoRa_buf:(i+1)*LoRa_buf])      # send over UART
        while(AUX.value() == 0):                                # wait for AUX pin rising edge
            pass

    print("\nImage string complete.\n")     # debug


# returns true if search_string was received from server
def UART_read_search(search_string):

    if uart_LoRa.any():
        read_data = uart_LoRa.read()
        read_str = read_data.decode('utf-8')
        if (search_string in read_str):
            print("string = ",read_str)         # for debug
            return 1
    return 0



#~~~~~~~~~~~~~~~~~~~~~~ start of program ~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~ Lora Setup ~~~~~
fm.register(31, fm.fpioa.GPIO0)         #M0
pinM0 = GPIO(GPIO.GPIO0, GPIO.OUT)

fm.register(32, fm.fpioa.GPIO2)         #M1
pinM1 = GPIO(GPIO.GPIO2, GPIO.OUT)

fm.register(35, fm.fpioa.GPIOHS2)       #AUX
AUX = GPIO(GPIO.GPIOHS2, GPIO.IN)

# Set M0 M1 to Mode 00
pinM0.value(0)
pinM1.value(0)

# Lora UART
fm.register(33,fm.fpioa.UART1_TX)   # UART1_TX connects to Rxd
fm.register(34,fm.fpioa.UART1_RX)   # UART1_RX connects to Txd

uart_LoRa = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)

def LED_ON():

    pin6.value(1)
    pin7.value(1)
    pin8.value(1)


def LED_OFF():

    pin6.value(0)
    pin7.value(0)
    pin8.value(0)

LED_ON()
delay(500)
LED_OFF()


while(True):

    # ~~~~~ Wait for Request ~~~~~

    sleep_ms(500)   # for debug

    while(UART_read_search("Image request") == 0):
        sleep_ms(10)

    #uart_LoRa.write("Request received")


    # ~~~~~ Take picture ~~~~~

    sensor.reset() # Initialize the camera sensor.
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
    sensor.skip_frames(time = 2000) # Let new settings take affect.

    sensor.skip_frames(time = 1000) # Give the user time to get ready.

    print("\nTaking a picture.\n")
    image = sensor.snapshot()
    image2 = image.copy((100,100,300,200))
    image2.save('reading.jpg')

    sleep_ms(100)

    # ~~~~~ Writing ~~~~~

    send_image()
    sleep_ms(100)

    # ~~~~~ Reading ~~~~~

    while(UART_read_search("Image received") == 0):
        sleep_ms(10)




# ~~~~~ Clean up ~~~~~
uart_LoRa.deinit()
del uart_LoRa






