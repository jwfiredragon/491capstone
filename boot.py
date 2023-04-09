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


# Initializing LoRA port
uart_LoRa = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)
#task = kpu.load("/sd/paste_mnist.kmodel")
task = kpu.load("/sd/KPU/mnist/mnist.kmodel")
info=kpu.netinfo(task)
clock = time.clock()                # Create a clock object to track the FPS.
LoRa_buf = 128



# Pin Setup
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



# returns true if search_string was received from server
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

# Opens saved image file and sends it to server as bytes, along with timestamp and device ID
def send_image():

    LoRa_buf = 128  # LoraWAN buffer is 512 bytes

    # load image from SD card and convert it to bytes
    with open('/sd/reading1.jpg', 'rb') as img:
        iraw = img.read()
        ibytes = ubinascii.hexlify(iraw)

    id = bytes(machine.unique_id() + ' ', 'utf-8')
    now = time.localtime()
    timestamp = bytes(str(now[0])+'/'+str(now[1])+'/'+str(now[2])+'-'+str(now[3])+':'+str(now[4])+' ', 'utf-8')
    write_str = id + timestamp + ibytes + b'x'        # data to print/transmit
    # string padded with trailing 'x' as a workaround for bug where transmission sometimes drops last byte and adds it to the start of the next transmission

    print("Size of image string is: ", len(write_str),"\n\n")   # print length of transmitted string - debug

    for i in range(ceil(len(write_str)/LoRa_buf)):             # send 500 bytes at a time
        print(write_str[i*LoRa_buf:(i+1)*LoRa_buf], end='')     # Print hex string for debugging. Note that this will print b'...' each loop
        uart_LoRa.write(write_str[i*LoRa_buf:(i+1)*LoRa_buf])      # send over UART
        while(AUX.value() == 0):                                # wait for AUX pin rising edge (ie previous write finished)
            pass

    print("\nImage string complete.\n")     # debug

# Preprocesses image by reducing to grayscale and cropping, then saves to SD card
def mnist_run(img, dx, dy, dis, x00 =0, y00 = 80, nnn = 2):
    if nnn == 4:
        x00 = x00
        dy = dy
    img0 = img.copy((x00+dis*nnn,y00+nnn*0, dx, dy))
    img0.mean(10, threshold=True, offset=1, invert=0)  #A
    #img0.median(2, percentile=0.3, threshold=True, offset=-4, invert=True)
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
    # save image to SD card and load when sending to ensure it's sent in the .jpg format

    return max_index, pmax




#setup_pins()


#...........................................Main................................
while(True):


#.................................Wait for Request

    LED_ON()        #for debug
    sleep_ms(250)
    LED_OFF()
    sleep_ms(250)
    LED_ON()
    sleep_ms(250)
    LED_OFF()

    while(UART_read_search("Image request") == 0):
        sleep_ms(10)


#...................................Take image
    setup_camera()
    count_0 = 0
    count_4 = 0
    clock.tick()
    LED_ON()
    img=sensor.snapshot()
    LED_OFF()
# Update the FPS clock.
    #img.mean(1, threshold=True, offset=5, invert=True)
    #img.binary([(100,255)], invert = True)
    #img.erode(1)
    x00 = 0
    y00 = 140
    dx = 240
    dy = 80
    dis = 25
    p_thre = 0.95


    for i in range(0,1):
        class_num, pmax = mnist_run(img, dx, dy, dis,\
            x00 =x00, y00 = y00,\
            nnn=i)

#...................................LoRa
    sleep_ms(500)

    send_image()

    sleep_ms(2000)

    UART_read_search("Image received")
    sleep_ms(10)


# ~~~~~ Clean up ~~~~~
uart_LoRa.deinit()
del uart_LoRa
