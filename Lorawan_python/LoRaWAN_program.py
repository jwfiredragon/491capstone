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

# Setup
fm.register(34,fm.fpioa.UART1_TX)
fm.register(33,fm.fpioa.UART1_RX)

uart_A = UART(UART.UART1, 9600, 34, None, 1, timeout=1000, read_buf_len=4096)
uart_B = UART(UART.UART2, 9600, 33, None, 1, timeout=1000, read_buf_len=4096)



# take picture

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

sensor.skip_frames(time = 2000) # Give the user time to get ready.

println("Taking a picture.")
sensor.snapshot().save("example.jpg") # or "example.bmp" (or others)

println("Finished taking picture.")


# Writing
write_str = base64.b64encode("example.jpg")
for i in range(floor(len(write_str)/500)): #send 500 bytes at a time
    uart_A.write(write_str[i*500:i*500+501])
    time.sleep_ms(10)

sleep_ms(500)


# Reading
read_data = uart_B.read()
read_str = read_data.decode('utf-8')
print("string = ",read_str)
