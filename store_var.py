import uos
from fpioa_manager import fm
from board import board_info
from Maix import GPIO


def write_variable_to_flash(filename, variable):
    with open(filename, 'w') as f:
        f.write(str(variable))

def read_variable_from_flash(filename):
    try:
        with open(filename, 'r') as f:
            value = f.read()
            return value
    except OSError:
        print("Error: File not found")
        return None

def set_specific_pins_low(pins):
    for pin_number in pins:
        gpio_pin = GPIO(pin_number, GPIO.OUT)
        gpio_pin.value(1)

def init_gpio_output(pin_number):
    fm.register(pin_number, fm.fpioa.GPIOHS0 + pin_number)
    gpio_pin = GPIO(GPIO.GPIOHS0 + pin_number, GPIO.OUT)
    return gpio_pin

def toggle_gpio(pin):
    pin.value(not pin.value())


variable_to_store = "ffaa"
filename = "stored_variable.txt"

write_variable_to_flash(filename, variable_to_store)
stored_variable = read_variable_from_flash(filename)

if stored_variable is not None:
    print("Stored variable:", stored_variable)

# Initialize GPIOHS26 as an output pin
pin_hs19 = init_gpio_output(board_info.GPIOHS19)

#pins_to_set_low = [27, 28]
#set_specific_pins_low(pins_to_set_low)

while True:
    toggle_gpio(pin_hs19)
    time.sleep(1)
