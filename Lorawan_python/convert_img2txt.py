# Untitled - By: ncamp - Thu Mar 2 2023

import sensor, image

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

sensor.skip_frames(time = 2000) # Give the user time to get ready.

print("Taking snapshot!")
sensor.snapshot().save("example.jpg") # or "example.bmp" (or others)

write_str = base64.b64encode("example.jpg")
print("Example: /n/n")
print(write_str)
