import binascii
import io
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
        if line is not b'':
            # hack for buffer character dropping
            if line[0] == 120:
                line = line[1:]

            ibytes = binascii.unhexlify(line)
            image = Image.open(io.BytesIO(ibytes))
            image.save('./ser_out.jpg')
            ser.write('Image received'.encode())
            print('Image received.')
            img_received = True