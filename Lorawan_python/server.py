import binascii
import io
import pytesseract
from PIL import Image
from serial import Serial

ser = Serial('COM5', 9800, timeout=1)

while True:
    input('Enter anything to request a reading: ')

    ser.write(f'Image request'.encode())
    print('Image request sent.')

    img_received = False
    while not img_received:
        line = ser.readline()
        print('...')
        if line is not b'':
            # hack for buffer character dropping
            if line[0] == 120:
                line = line[1:]
            if line[-1] == 120:
                line = line[:-2]

            ibytes = binascii.unhexlify(line)
            image = Image.open(io.BytesIO(ibytes))
            image.save('./ser_out.jpg')
            text = pytesseract.image_to_string('ser_out.jpg', lang='lets')
            ser.write('Image received'.encode())
            print(f'Image received. Text: {text}')
            img_received = True
