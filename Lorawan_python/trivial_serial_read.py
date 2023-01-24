
# To run: connect PIN15 has been connected to PIN10, and PIN17 has been connected to PIN9
# -> Verrified as working by NC and SY, on Jan. 24



from fpioa_manager import fm
from machine import UART
fm.register(15,fm.fpioa.UART1_TX) 
fm.register(17,fm.fpioa.UART1_RX)
fm.register(9,fm.fpioa.UART2_TX)
fm.register(10,fm.fpioa.UART2_RX)

uart_A = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)
uart_B = UART(UART.UART2, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)
write_str ='hello world'
for i in range(20):
    uart_A.write(write_str)
    read_data = uart_B.read()
    read_str = read_data.decode('utf-8')
    print("string = ",read_str)
    if read_str == write_str:
        print("baudrate:115200 bits:8 parity:None stop:1 ---check Successfully")

# clean up
uart_A.deinit()
uart_B.deinit()
del uart_A
del uart_B
