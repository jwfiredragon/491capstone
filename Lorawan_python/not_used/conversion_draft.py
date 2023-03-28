import binascii
import io
from PIL import Image

with open('TestImage.png', 'rb') as img:
    # convert image to base64 bytes
    ibytes = binascii.b2a_base64(img.read())
    # convert bytes to string, stripping header/footer characters
    istr = str(ibytes)[2:-3]
    # write string to file for reference
    with open('convert.txt', 'w') as out:
        out.write(istr)

    # convert string back to bytes
    ibytes2 = bytes(istr, 'utf-8')
    # decode bytes from base64
    iout = binascii.a2b_base64(ibytes2)

    # open image from bytes
    image = Image.open(io.BytesIO(iout))
    # save image
    image.save('./convert.jpg')