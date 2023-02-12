# Simple LoRaWAN py program
# To run: Connect Pins as shown:
#
# Lora :  MCU
# M0  -> Gnd
# M1  -> Gnd
# Rxd -> pin 10
# Txd -> pin 9
# AUX -> none
# Vcc -> 5V
# Gnd -> Gnd

from fpioa_manager import fm
from machine import UART


# Setup
fm.register(9,fm.fpioa.UART1_TX)
fm.register(10,fm.fpioa.UART1_RX)

uart_A = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)

# Writing
write_str ='hello world\n'
for i in range(10):
    uart_A.write(write_str)

sleep_ms(500)

# Reading
read_data = uart_B.read()
read_str = read_data.decode('utf-8')
print("string = ",read_str)