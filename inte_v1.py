from fpioa_manager import fm
from Maix import GPIO
from time import sleep_ms
from machine import UART
import machine
import ubinascii
from math import floor, ceil
from board import board_info
import sensor, image, time, math
import KPU as kpu
import utime



uart_LoRa = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)
#task = kpu.load("/sd/paste_mnist.kmodel")
task = kpu.load("/sd/KPU/mnist/mnist.kmodel")
info=kpu.netinfo(task)
clock = time.clock()                # Create a clock object to track the FPS.
LoRa_buf = 128



def setup_pins():
    fm.register(31, fm.fpioa.GPIO0, force=True)     #M0
    fm.register(32, fm.fpioa.GPIO2, force=True)    #M1
    fm.register(35, fm.fpioa.GPIOHS2)               #AUX

    fm.register(6, fm.fpioa.GPIO3, force=True)
    fm.register(7, fm.fpioa.GPIO4, force=True)
    fm.register(8, fm.fpioa.GPIO5)

    fm.register(33,fm.fpioa.UART1_TX)   # UART1_TX connects to Rxd
    fm.register(34,fm.fpioa.UART1_RX)   # UART1_RX connects to Txd


    uart_B = UART(UART.UART2, 115200, 8, None, 1, timeout=10)

    pinM0 = GPIO(GPIO.GPIO0, GPIO.OUT)
    pinM1 = GPIO(GPIO.GPIO2, GPIO.OUT)
    AUX = GPIO(GPIO.GPIOHS2, GPIO.IN)

    pinM0.value(0)
    pinM1.value(0)

    pin6 = GPIO(GPIO.GPIO3, GPIO.OUT)
    pin7 = GPIO(GPIO.GPIO4, GPIO.OUT)
    pin8 = GPIO(GPIO.GPIO5, GPIO.OUT)

def setup_camera():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_vflip(True)
    sensor.set_auto_gain(True)
    sensor.set_auto_whitebal(True)
    sensor.set_gainceiling(2)
    sensor.skip_frames(time=2000)



def UART_read_search(search_string):

    if uart_LoRa.any():
        read_data = uart_LoRa.read()
        read_str = read_data.decode('utf-8')
        if (search_string in read_str):
            print("string = ",read_str)         # for debug
            return 1
    return 0


def LED_ON():

    pin6.value(1)
    pin7.value(1)
    pin8.value(1)


def LED_OFF():

    pin6.value(0)
    pin7.value(0)
    pin8.value(0)




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
    image2.save('reading1.jpg')

    return max_index, pmax


setup_camera()

setup_pins()


#...........................................Main................................
while(True):


#.................................Wait for Request

    sleep_ms(500)   # for debug

    while(UART_read_search("Image request") == 0):
        sleep_ms(10)

    uart_LoRa.write("Request received")

#...................................Take image
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
#...................................LoRa
    sleep_ms(500)

    read_str=""

    UART_read_search("Image received")
    sleep_ms(10)
    send_image()
    sleep_ms(500)

    read_str=""
    UART_read_search("Image received")
    sleep_ms(10)


# ~~~~~ Clean up ~~~~~
uart_LoRa.deinit()
del uart_LoRa










