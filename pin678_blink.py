# Untitled - By: ncamp - Tue Mar 21 2023

from fpioa_manager import fm
from Maix import GPIO
from time import sleep_ms



# LED pin 6 7 8
fm.register(6, fm.fpioa.GPIO3, force=True)
fm.register(7, fm.fpioa.GPIO4, force=True)
fm.register(8, fm.fpioa.GPIO5)

pin6 = GPIO(GPIO.GPIO3, GPIO.OUT)
pin7 = GPIO(GPIO.GPIO4, GPIO.OUT)
pin8 = GPIO(GPIO.GPIO5, GPIO.OUT)


while(True):
    pin6.value(1)
    pin7.value(1)
    pin8.value(1)
    print("LEDs ON")

    sleep_ms(500)

    pin6.value(0)
    pin7.value(0)
    pin8.value(0)
    print("LEDs OFF")

    sleep_ms(500)
