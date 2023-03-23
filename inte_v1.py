from fpioa_manager import fm
from Maix import GPIO
from time import sleep_ms
from machine import UART
import machine
import utime
import image,sensor
import ubinascii
from math import floor, ceil
from board import board_info

import utime
import image

#fm.register(PIN9,fm.fpioa.UART2_TX)
#fm.register(PIN10,fm.fpioa.UART2_RX)
uart_B = UART(UART.UART2, 115200, 8, None, 1, timeout=10)
import sensor, image, time, lcd, math
import KPU as kpu
#task = kpu.load("/sd/paste_mnist.kmodel")
task = kpu.load("/sd/KPU/mnist/mnist.kmodel")
info=kpu.netinfo(task)

lcd.init(freq=15000000)
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.set_vflip(True)
#sensor.set_hmirror(0) #flip camera
sensor.set_auto_gain(True)
sensor.set_auto_whitebal(True)
sensor.set_gainceiling(2)
#sensor.strech_char(1)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

fm.register(31, fm.fpioa.GPIO0, force=True)     #M0
fm.register(32, fm.fpioa.GPIO2, force=True)    #M1
fm.register(35, fm.fpioa.GPIOHS2)               #AUX

pinM0 = GPIO(GPIO.GPIO0, GPIO.OUT)
pinM1 = GPIO(GPIO.GPIO2, GPIO.OUT)
AUX = GPIO(GPIO.GPIOHS2, GPIO.IN)

pinM0.value(0)
pinM1.value(0)

fm.register(33,fm.fpioa.UART1_TX)   # UART1_TX connects to Rxd
fm.register(34,fm.fpioa.UART1_RX)   # UART1_RX connects to Txd

uart_A = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)


fm.register(6, fm.fpioa.GPIO3, force=True)
fm.register(7, fm.fpioa.GPIO4, force=True)
fm.register(8, fm.fpioa.GPIO5)

pin6 = GPIO(GPIO.GPIO3, GPIO.OUT)
pin7 = GPIO(GPIO.GPIO4, GPIO.OUT)
pin8 = GPIO(GPIO.GPIO5, GPIO.OUT)


LoRa_buf = 128

def mnist_run(img, dx, dy, dis, x00 =0, y00 = 80, nnn = 2):
    if nnn == 4:
        x00 = x00
        dy = dy
    img0 = img.copy((x00+dis*nnn,y00+nnn*0, dx, dy))
    img0.mean(2, threshold=True, offset=1, invert=True)  #A
    img0.median(2, percentile=0.3, threshold=True, offset=-4, invert=True)
    #img0.midpoint(2, bias=0.3, threshold=True, offset=0, invert=True)
    #img0.mode(2, threshold=True, offset=0, invert=True)  #B

    #img0.binary([(110,255)], invert = True)
    for dx0 in range(dx):
        for dy0 in range(dy):
            a0 = img0.get_pixel(dx0,dy0)
            img.set_pixel(x00+dis*nnn+dx0,y00+nnn*0+dy0,a0)
    #img1 = img0.copy((1,1, dx-1, dy-1))
    img1 = img0
    img1 = img1.resize(28,28)
    img1 = img1.to_grayscale(0)
    #imgl = imgl.histeq(1)
    img1.pix_to_ai()
    fmap=kpu.forward(task,img1)
    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)
    kpu.fmap_free(fmap)
    image2 = img0.copy((1,1, dx-1, dy-1))
    image2.save('reading.jpg')
#    img.save("example.jpg")
#    pic_stream=bytearray(img, "utf-8")
#    file_path = "uft8encodding.txt"
#    with open(file_path,"w") as file:
#        file.write(pic_stream)
#    file.close()
#   print(pic_stream)
    #machine.idle()
    #print(test_stream)
    pin6.value(1)
    pin7.value(1)
    pin8.value(1)
#    print("LEDs ON")

#    sleep_ms(500)

#    pin6.value(0)
#    pin7.value(0)
#    pin8.value(0)
#    print("LEDs OFF")

#    sleep_ms(500)
    return max_index, pmax



num_list = [0, 0, 0, 0]
p_list = [0,0,0,0]
angle_list = [0,0,0,0]
while(True):
    count_0 = 0
    count_4 = 0
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    #img.mean(1, threshold=True, offset=5, invert=True)
    #img.binary([(100,255)], invert = True)
    #img.erode(1)
    #sensor.skip_frames(time = 2000)
    x00 = 91
    y00 = 50
    dx = 100
    dy = 140
    dis = 70
    p_thre = 0.85
    for i in range(0,1):
        class_num, pmax = mnist_run(img, dx, dy, dis,\
            x00 =x00, y00 = y00,\
            nnn=i)
        if pmax > p_thre:
            num_list[i] = class_num
            p_list[i] = pmax
#            img.save("example.jpg")
         #   print(pic_stream)
    for i in range(0,1):
        if i == 1:
            x00 = x00
            dy = dy
#        img.draw_rectangle((x00+dis*i,y00+i*0, dx, dy), color=255)
    R_list = []
    c_color = []
    x_list = [101+3, 175+2, 241, 263]
    y_list = [176-6, 193-6, 156-6, 84-6]


    sleep_ms(500)

    read_str=""
    while(("Image request" in read_str)!= True):

        if uart_A.any():
           read_data = uart_A.read()
           read_str = read_data.decode('utf-8')
           print("string = ",read_str)
        else:
           #pass #print("not available")
            print("not available")
    with open('/sd/reading.jpg', 'rb') as img:
        iraw = img.read()
        ibytes = ubinascii.hexlify(iraw)
    #ibytes = ubinascii.b2a_base64(iraw)
    #ibytes = b''
    #for i in range(len(iraw)/256):
        #ibytes += ubinascii.b2a_base64(iraw[i*256:(i+1)*256])[:-2]


    write_str = ibytes + b'x'        # data to print/transmit

    print("Size of image string is: ", len(write_str),"\n\n")   # print length of transmitted string

    for i in range(ceil(len(write_str)/LoRa_buf)):             # send 500 bytes at a time
        print(write_str[i*LoRa_buf:(i+1)*LoRa_buf], end='')     # Print hex string. Note that this will print b'...' each loop
        uart_A.write(write_str[i*LoRa_buf:(i+1)*LoRa_buf])      # send over UART
        while(AUX.value() == 0):                                # wait for AUX pin rising edge
            pass
        sleep_ms(10)

    print("\nImage string complete.\n")


    sleep_ms(500)



    read_str=""
    while(read_str != "Image received"):

        if uart_A.any():
            read_data = uart_A.read()
            read_str = read_data.decode('utf-8')
            print("string = ",read_str)
        #else:
            #print("not available")

        sleep_ms(10)


# ~~~~~ Clean up ~~~~~
uart_A.deinit()
del uart_A


  #software workflow:
    # Check connection to the server
    # After connection is made, check schedule to take picture
    # After the Timer runs out/request been received
    # Take picture
    #  OPTIONAL: pre-processing of the image
    # UART transmission of the data to the LORAWAN chip
    # LORAWAN send the data (ideally with check sum?)
    # Receive a ACK signal from server
    # Server side OCR
    # Report data to user




