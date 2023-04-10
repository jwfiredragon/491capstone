#Program: Basic server functionality 
#Purpose: To send image request to device and perform OCR on received data
import binascii
import io
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from serial import Serial

ser = Serial('COM3', 9800, timeout=1)

while True:
    input('Enter anything to request a reading: ')

    ser.write(f'Image request'.encode())
    print('Image request sent.')

    img_received = False
    while not img_received:
        line = ser.readline()
        print('...')
        if line is not b'':
            # Workaround for buffer dropping characters
            # Removes leading/trailing 'x's (ASCII code 120) if present
            if line[0] == 120:
                line = line[1:]
            if line[-1] == 120:
                line = line[:-2]

            # msg[0] = device ID, msg[1] = timestamp, msg[2] = image bytes
            msg = line.split(b' ')

            # Convert the received message into an image
            ibytes = binascii.unhexlify(msg[2])
            image = Image.open(io.BytesIO(ibytes))

            # preprocess image to join disconnected line segments for more consistent OCR
            # small radius Gaussian blur, then conversion to pure black and white
            image = image.filter(ImageFilter.GaussianBlur(radius=2))
            fn = lambda x : 255 if x > 90 else 0
            image = image.convert('L').point(fn, mode='1')

            image.save('./ser_out.bmp')

            # Send receipt acknowledgement to device
            ser.write('Image received'.encode())

            # Perform OCR on image and print result
            text = pytesseract.image_to_string('ser_out.bmp', lang='lets',  config='-c tessedit_char_whitelist=0123456789')
            message0 = msg[0].decode('utf-8')
            message1 = msg[1].decode('utf-8')
            print(f'Reading from ID {message0} at {message1}: {text}')
            
            img_received = True
