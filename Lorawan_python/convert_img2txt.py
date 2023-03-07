# "convert_img2txt"
# By: N. Campbell - Thu Mar 2 2023
# This program takes an image, converts it to text using b64encode,
# and prints the converted string to the command line.

import sensor, image
from base64 import b64encode

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

sensor.skip_frames(time = 2000) # Give the user time to get ready.

print("Taking snapshot!")
sensor.snapshot().save("example.jpg")

write_str = base64.b64encode("example.jpg") # encode image
print("Example image encoded with base64: \n\n")
print(write_str)
