# Simple LoRaWAN Write py program
# To run: Connect Pins as shown:
# Tested to work on March 10, 2022
#
# Lora :  MCU
# M0  -> Gnd
# M1  -> Gnd
# Rxd -> pin 33
# Txd -> pin 34
# AUX -> none
# Vcc -> 3.3V
# Gnd -> Gnd

from fpioa_manager import fm
from machine import UART

# Setup
fm.register(33,fm.fpioa.UART1_TX) #Rxd
fm.register(34,fm.fpioa.UART1_RX) #Txd

uart_A = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)

# Program Loop
write_str ='hello world\n'
for i in range(10):
    uart_A.write(write_str)
