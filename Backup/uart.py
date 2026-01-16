import serial
import serial.tools.list_ports as sp
import memory

BAUD_RATE_115200 = 115200
BAUD_RATE_230400 = 230400
BAUD_RATE_460800 = 460800
BAUD_RATE_500000 = 500000
BAUD_RATE_576000 = 576000
BAUD_RATE_921600 = 921600
BAUD_RATE_1000000 = 1000000
BAUD_RATE_1152000 = 1152000
BAUD_RATE_1500000 = 1500000
BAUD_RATE_2000000 = 2000000
BAUD_RATE_2500000 = 2500000
BAUD_RATE_3000000 = 3000000
BAUD_RATE_3500000 = 3500000
BAUD_RATE_4000000 = 4000000

# BAUD_RATE_SEL = BAUD_RATE_115200
BAUD_RATE_SEL = BAUD_RATE_576000
# BAUD_RATE_SEL = BAUD_RATE_1000000
# BAUD_RATE_SEL = BAUD_RATE_1152000

IMAGE_SIGNAL    = 0xCC
CMD_SIGNAL      = 0xDD
CMD_ADDR        = 0xA5
READ_CMD        = (0 << 7)
WRITE_CMD       = (1 << 7)

b_exit = False
Q_frame_buffer = []


# Uart Recive 구조체
class uart_structer:
    def __init__(self, ui8_signal, ui8_cmd, i_addr_length, ui8_addr, i_data_length, ui8_data, ui8_chksum, ui8_dummy):
        self.ui8_signal = ui8_signal
        self.ui8_cmd = ui8_cmd
        self.i_addr_length = i_addr_length
        self.ui8_addr = ui8_addr
        self.i_data_length = i_data_length
        self.ui8_data = ui8_data
        self.ui8_chksum = ui8_chksum
        self.ui8_dummy = ui8_dummy

serial_component_handle = None
Q_ui8_uart_image_revice = []


# 디버그용
b_uart_image_recive_chk = False


################## UART INIT ##############################
def uart_init():
    global serial_component_handle
    
    A_comports = sp.comports()
    A_comport_devices = []
    A_esp32_usb_port = []
    A_usb_serial_port = []
    
    for comport in A_comports:
        print("")
        print("name : ", comport.name)
        print("device : ", comport.device)
        print("description : ", comport.description)
        print("hwid : ", comport.hwid)
        print("vid : ", comport.vid)
        print("pid : ", comport.pid)
        print("serial_number : ", comport.serial_number)
        print("location : ", comport.location)
        print("manufacturer : ", comport.manufacturer)
        print("product : ", comport.product)
        print("interface : ", comport.interface)
        # name :  COM5
        # device :  COM5
        # description :  USB-Enhanced-SERIAL CH343(COM5)
        # hwid :  USB VID:PID=1A86:55D3 SER=58CF028302 LOCATION=1-3
        # vid :  6790
        # pid :  21971
        # serial_number :  58CF028302
        # location :  1-3
        # manufacturer :  wch.cn
        # product :  None
        # interface :  None
        # ['USB', 'VID:PID=1A86:55D3', 'SER=58CF028302', 'LOCATION=1-3']
        A_comport_devices.append(comport.device)
        
        
        if len(comport.hwid.split(" ")) > 1:                    # ['USB', 'VID:PID=1A86:55D3', 'SER=58CF028302', 'LOCATION=1-3']
            if len(comport.hwid.split(" ")[1].split("=")) > 1:  # ['VID:PID', '1A86:7523']
                print(comport.hwid.split(" ")[1])               # 'VID:PID=1A86:55D3'
                if comport.hwid.split(" ")[1].split("=")[1] == '303A:4001':         # ESP32-S3 USB Port
                    A_esp32_usb_port.append(comport.device)                         # COM5
                if comport.hwid.split(" ")[1].split("=")[1] == '1A86:7523':         # USB to TTL UART Module
                    A_usb_serial_port.append(comport.device)                        # COM5
            
    if len(A_esp32_usb_port) == 1 and len(A_usb_serial_port) == 0:
        serial_component_handle = serial.Serial(A_esp32_usb_port[0], BAUD_RATE_SEL)
        s_comport_name = A_esp32_usb_port[0]
    elif len(A_esp32_usb_port) == 0 and len(A_usb_serial_port) == 1:
        serial_component_handle = serial.Serial(A_usb_serial_port[0], BAUD_RATE_SEL)
        s_comport_name = A_usb_serial_port[0]
    else:
        print("Connected COM ports: " + str(A_comport_devices))
        s_sel_COM = input()
        serial_component_handle = serial.Serial("COM"+str(s_sel_COM), BAUD_RATE_SEL)
        s_comport_name = "COM"+str(s_sel_COM)
        
    print("")
    print("")
    print("Connect ", s_comport_name)
    return serial_component_handle
################## UART INIT ##############################


# 패리티 비트, 체크섬, ACK/NACK, 해밍 코드
# 체크섬
def checksum(uart_data_class_value):
    # XOR 기반 체크섬 계산
    checksum = 0
    
    if isinstance(uart_data_class_value.ui8_signal, bytes):
        checksum ^= uart_data_class_value.ui8_signal[0]
    else:
        checksum ^= uart_data_class_value.ui8_signal
    
    if isinstance(uart_data_class_value.ui8_cmd, bytes):
        checksum ^= uart_data_class_value.ui8_cmd[0]
    else:
        checksum ^= uart_data_class_value.ui8_cmd
        
    if isinstance(uart_data_class_value.i_addr_length, bytes):
        checksum ^= uart_data_class_value.i_addr_length[0]
    else:
        checksum ^= uart_data_class_value.i_addr_length
        
    if isinstance(uart_data_class_value.ui8_addr, list):
        for byte in uart_data_class_value.ui8_addr:
            if isinstance(byte, bytes):
                checksum ^= byte[0]
            else:
                checksum ^= byte
    else:
        if isinstance(uart_data_class_value.ui8_addr, bytes):
            checksum ^= uart_data_class_value.ui8_addr[0]
        else:
            checksum ^= uart_data_class_value.ui8_addr
            
    if isinstance(uart_data_class_value.i_data_length, bytes):
        checksum ^= uart_data_class_value.i_data_length[0]
    else:
        checksum ^= uart_data_class_value.i_data_length
        
    if isinstance(uart_data_class_value.ui8_data, list):
        for byte in uart_data_class_value.ui8_data:
            if isinstance(byte, bytes):
                checksum ^= byte[0]
            else:
                checksum ^= byte
    else:
        if isinstance(uart_data_class_value.ui8_data, bytes):
            checksum ^= uart_data_class_value.ui8_data[0]
        else:
            checksum ^= uart_data_class_value.ui8_data    
    
    return checksum

######### ESP32 <- PC
################## UART Sender Tramsaction ##############################
def uart_sender_transaction(s_signal, i_addr_leng, s_addr, i_data_leng, s_data):
    # 공간 만들기
    uart_image_send_signal_data = uart_structer(bytes.fromhex("00"),    # ui8_signal
                                                bytes.fromhex("00"),    # ui8_cmd
                                                0,                      # i_addr_length
                                                [],                     # ui8_addr
                                                0,                      # i_data_length
                                                [],                     # ui8_data
                                                bytes.fromhex("00"),    # ui8_chksum
                                                bytes.fromhex("00"),    # ui8_dummy
                                                )
    # 공간 만들기
    A_by_addr = []
    A_by_data = []
    for i_count in range(i_addr_leng):
        # 8자리(32bit) CMD 쪼개기
        A_by_addr.extend(bytes.fromhex(s_addr[2*i_count : 2*(i_count) + 2]))
    for i_count in range(i_data_leng):
        # 8자리(32bit) CMD 쪼개기
        A_by_data.extend(bytes.fromhex(s_data[2*i_count : 2*(i_count) + 2]))

    # IMAGE 수신 Signal
    uart_image_send_signal_data.ui8_signal = bytes.fromhex(format(int(s_signal, 16), '02X'))
    uart_image_send_signal_data.ui8_cmd = bytes.fromhex(format(WRITE_CMD, '02X'))
    # uart_image_send_signal_data.ui8_cmd = bytes([CMD_SIGNAL])
    uart_image_send_signal_data.i_addr_length = bytes.fromhex(format(i_addr_leng, '02X'))
    uart_image_send_signal_data.ui8_addr = A_by_addr
    uart_image_send_signal_data.i_data_length = bytes.fromhex(format(i_data_leng, '02X'))
    uart_image_send_signal_data.ui8_data = A_by_data
    uart_image_send_signal_data.ui8_chksum = bytes.fromhex(format(checksum(uart_image_send_signal_data), '02X'))

    A_send_uart = bytearray()
    A_send_uart.extend(uart_image_send_signal_data.ui8_signal)      # 8bit
    A_send_uart.extend(uart_image_send_signal_data.ui8_cmd)         # 8bit
    A_send_uart.extend(uart_image_send_signal_data.i_addr_length)   # 8bit
    A_send_uart.extend(uart_image_send_signal_data.ui8_addr)        # 8bit
    A_send_uart.extend(uart_image_send_signal_data.i_data_length)   # 8bit
    A_send_uart.extend(uart_image_send_signal_data.ui8_data)        # 8bit
    A_send_uart.extend(uart_image_send_signal_data.ui8_chksum)      # 8bit
    A_send_uart.extend(uart_image_send_signal_data.ui8_dummy)       # 8bit
    serial_component_handle.write(A_send_uart)
    memory.time.sleep(0.001)
################## UART Sender Tramsaction ##############################

######### ESP32 -> PC
################## UART Recive Thread ##############################
def uart_recive_thread():
    while 1:
        Q_ui8_uart_image_revice.append(serial_component_handle.read())   ## read CMD Signal(Byte단위[8bit])
        # memory.time.sleep(0.000001)
################## UART Recive Thread ##############################

################## UART Recive Frame ##############################
def uart_recive_data_process():
    global b_exit, b_uart_image_recive_chk
    # 매번 UART 읽기 변수
    by_uart_read_8bit = 0
    
    # 공간 만들기
    uartrecive_uart_recive_buf = uart_structer(   
                                               bytes.fromhex("00"),    # ui8_signal
                                               bytes.fromhex("00"),    # ui8_cmd
                                               0,                      # i_addr_length
                                               [],                     # ui8_addr
                                               0,                      # i_data_length
                                               [],                     # ui8_data
                                               bytes.fromhex("00"),    # ui8_chksum
                                               bytes.fromhex("00"),    # ui8_dummy
                                               )
    # 공간 만들기
        
    # 이미지 변수
    F_recive_frame_64 = memory.np.zeros((64,64), memory.np.uint8) # Frame 변수
    b_frame_start_signal = False
    b_chksum_done = False
    
    # 디버그용
    i_error_bit_count = 0
    
    if b_uart_image_recive_chk:
        # uart_sender_transaction(s_signal, i_addr_leng, s_addr, i_data_leng, s_data)
        uart_sender_transaction(hex(IMAGE_SIGNAL), 1, hex(CMD_ADDR), 4, "00")
        
    ## Tread 반복
    while True:
        try:
            if len(Q_ui8_uart_image_revice) > 0:
                by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                ##############################
                # 들어오는 Bit
                # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                # print("by_uart_read_8bit : ", by_uart_read_8bit)
                ##############################
                
##########################################################################################################
# 이미지 데이터 시그널 수신
##########################################################################################################
                if by_uart_read_8bit[0] == IMAGE_SIGNAL:                     # 0xCC
                    # print(i_count, " : ui8_signal : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                    uartrecive_uart_recive_buf.ui8_signal = by_uart_read_8bit[0]
                    while len(Q_ui8_uart_image_revice) == 0:
                        memory.time.sleep(0.001)
                    by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                    
                    ####################
                    # Write CMD
                    ####################
                    # CMD가 1이라면 -> WRITE_CMD
                    # 1000_0000
                    if by_uart_read_8bit[0] == WRITE_CMD:
                        # print(i_count, " : ui8_cmd : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                        uartrecive_uart_recive_buf.ui8_cmd = by_uart_read_8bit[0]
                        while len(Q_ui8_uart_image_revice) == 0:
                            memory.time.sleep(0.001)
                        by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                        ####################
                        # ADDR length
                        ####################
                        uartrecive_uart_recive_buf.i_addr_length = by_uart_read_8bit[0]
                        # print("i_addr_len : ", i_addr_len)
                        ####################
                        # ADDR
                        ####################
                        # ADDR Check
                        # X111_1111
                        for i_len in range(uartrecive_uart_recive_buf.i_addr_length):
                            # print("count : ", i_len)
                            while len(Q_ui8_uart_image_revice) == 0:
                                memory.time.sleep(0.001)
                            by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                            if by_uart_read_8bit[0] == 0:  # Addr == 0
                                uartrecive_uart_recive_buf.ui8_addr = []
                            uartrecive_uart_recive_buf.ui8_addr.append(by_uart_read_8bit[0])
                        
                        # print("ui8_addr : ", uartrecive_uart_recive_buf.ui8_addr)    
                        # print("len(ui8_addr) : ", len(uartrecive_uart_recive_buf.ui8_addr))
                        
                        for i_len in range(uartrecive_uart_recive_buf.i_addr_length):
                            if uartrecive_uart_recive_buf.ui8_addr[i_len] < 64:
                                ####################
                                # Data length
                                ####################
                                while len(Q_ui8_uart_image_revice) == 0:
                                    memory.time.sleep(0.001)
                                by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                                uartrecive_uart_recive_buf.i_data_length = by_uart_read_8bit[0]
                                # print("i_data_len : ", i_data_len)
                                ####################
                                # IMAGE 
                                ####################
                                # ADDR 63을 받지 못하고 다시 0인 경우
                                if uartrecive_uart_recive_buf.ui8_addr[i_len] == 0 and b_frame_start_signal:
                                    b_frame_start_signal = False
                                    # 이미지 1장 Queue 입력
                                    Q_frame_buffer.append(F_recive_frame_64.copy())
                                    if i_error_bit_count > 0:
                                        print("error_bit : ", i_error_bit_count)
                                        i_error_bit_count = 0
                                    uartrecive_uart_recive_buf.ui8_data = []
                                    # print("a newframe")
                                    
                                # ADDR 0인 경우 = 새로운 이미지
                                if uartrecive_uart_recive_buf.ui8_addr[i_len] == 0:
                                    if b_frame_start_signal == False:
                                        b_frame_start_signal = True
                                        
                                # N ADDR에 대한 64개 Pixel 값 받기
                                for i_pixel_x in range(uartrecive_uart_recive_buf.i_data_length):
                                    while len(Q_ui8_uart_image_revice) == 0:
                                        memory.time.sleep(0.001)
                                    by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read Pixel Code (Byte단위[8bit])
                                    uartrecive_uart_recive_buf.ui8_data.append(by_uart_read_8bit[0])
                                    # F_recive_frame_64[int(uartrecive_uart_recive_buf.ui8_addr[i_len])][i_pixel_x] = by_uart_read_8bit[0]
                                
                                ####################
                                # Check Sum 
                                ####################
                                while len(Q_ui8_uart_image_revice) == 0:
                                    memory.time.sleep(0.001)
                                by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read chksum (Byte단위[8bit])
                                uartrecive_uart_recive_buf.ui8_chksum = by_uart_read_8bit[0]
                                
                                # 동기화 기능 활성화 인 경우
                                if b_uart_image_recive_chk:
                                    if checksum(uartrecive_uart_recive_buf) == uartrecive_uart_recive_buf.ui8_chksum:
                                        uart_sender_transaction(hex(IMAGE_SIGNAL), 1, hex(CMD_ADDR), 4, "00")
                                    else:                                        
                                        uart_sender_transaction(hex(IMAGE_SIGNAL), 1, hex(CMD_ADDR), 4, "03")
                                else:
                                    if checksum(uartrecive_uart_recive_buf) == uartrecive_uart_recive_buf.ui8_chksum:
                                        # print("\nchksum ok")
                                        # print("\nui8_addr[i_len]:", uartrecive_uart_recive_buf.ui8_addr[i_len])
                                        for i_pixel_x in range(64):
                                            F_recive_frame_64[int(uartrecive_uart_recive_buf.ui8_addr[i_len])][i_pixel_x] = uartrecive_uart_recive_buf.ui8_data[i_pixel_x]
                                    else:
                                        print("\nIMAGE_SIGNAL -> chksum X")
                                        # Error Bit 증가
                                        i_error_bit_count += 1
                                        
                                # ADDR 63인 경우
                                if uartrecive_uart_recive_buf.ui8_addr[i_len] >= 63:
                                    b_frame_start_signal = False
                                    # 이미지 1장 Queue 입력
                                    Q_frame_buffer.append(F_recive_frame_64.copy())
                                    if i_error_bit_count > 0:
                                        print("error_bit : ", i_error_bit_count)
                                        i_error_bit_count = 0
                                    uartrecive_uart_recive_buf.ui8_data = []
                                    # print("newframe")
                                    
                            # ADDR ERROR
                            else:
                                print("\nIMAGE_SIGNAL -> ADDR ERROR")
                                # Addr 배열 초기화
                                uartrecive_uart_recive_buf.ui8_addr = []
                                # Data 배열 초기화
                                uartrecive_uart_recive_buf.ui8_data = []
                                # Error Bit 증가
                                i_error_bit_count += 1
                                
                                # 동기화 기능 활성화 인 경우
                                if b_uart_image_recive_chk:
                                    uart_sender_transaction(hex(IMAGE_SIGNAL), 1, hex(CMD_ADDR), 4, "02")
                                break
                            
                    # CMD ERROR
                    else:
                        print("\nIMAGE_SIGNAL -> CMD ERROR : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                        # Addr 배열 초기화
                        uartrecive_uart_recive_buf.ui8_addr = []
                        # Data 배열 초기화
                        uartrecive_uart_recive_buf.ui8_data = []
                        # Error Bit 증가
                        i_error_bit_count += 1
                        
                        # 동기화 기능 활성화 인 경우
                        if b_uart_image_recive_chk:
                            uart_sender_transaction(hex(IMAGE_SIGNAL), 1, hex(CMD_ADDR), 4, "01")


                            
##########################################################################################################
# REG 데이터 시그널 수신
##########################################################################################################      
                elif by_uart_read_8bit[0] == CMD_SIGNAL:
                    # ##############################
                    # # 들어오는 Bit
                    # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                    # ##############################
                    # print("REG_SIGANL")
                    uartrecive_uart_recive_buf.ui8_signal = by_uart_read_8bit[0]
                    while len(Q_ui8_uart_image_revice) == 0:
                        memory.time.sleep(0.001)
                    by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                    # ##############################
                    # # 들어오는 Bit
                    # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                    # ##############################
                    ####################
                    # Write CMD
                    ####################
                    # CMD가 1이라면 -> WRITE_CMD
                    # 1000_0000
                    if by_uart_read_8bit[0] == WRITE_CMD:
                        uartrecive_uart_recive_buf.ui8_cmd = by_uart_read_8bit[0]
                        while len(Q_ui8_uart_image_revice) == 0:
                            memory.time.sleep(0.001)
                        by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                        # ##############################
                        # # 들어오는 Bit
                        # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                        # ##############################
                        ####################
                        # ADDR length
                        ####################
                        uartrecive_uart_recive_buf.i_addr_length = by_uart_read_8bit[0]
                        # print("i_addr_len : ", i_addr_len)
                        ####################
                        # ADDR
                        ####################
                        # ADDR Check
                        # X111_1111
                        for i_len in range(uartrecive_uart_recive_buf.i_addr_length):
                            # print("count : ", i_len)
                            while len(Q_ui8_uart_image_revice) == 0:
                                memory.time.sleep(0.001)
                            by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                            # ##############################
                            # # 들어오는 Bit
                            # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                            # ##############################
                            uartrecive_uart_recive_buf.ui8_addr.append(by_uart_read_8bit[0])
                        ####################
                        # Data length
                        ####################
                        while len(Q_ui8_uart_image_revice) == 0:
                            memory.time.sleep(0.001)
                        by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                        # ##############################
                        # # 들어오는 Bit
                        # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                        # ##############################
                        uartrecive_uart_recive_buf.i_data_length = by_uart_read_8bit[0]
                        # print("i_addr_len : ", i_addr_len)
                        ####################
                        # Data
                        ####################
                        # ADDR Check
                        # X111_1111
                        for i_len in range(uartrecive_uart_recive_buf.i_data_length):
                            # print("count : ", i_len)
                            while len(Q_ui8_uart_image_revice) == 0:
                                memory.time.sleep(0.001)
                            by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read CMD Signal(Byte단위[8bit])
                            # ##############################
                            # # 들어오는 Bit
                            # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                            # ##############################
                            uartrecive_uart_recive_buf.ui8_data.append(by_uart_read_8bit[0])
                        ####################
                        # Check Sum 
                        ####################
                        while len(Q_ui8_uart_image_revice) == 0:
                            memory.time.sleep(0.001)
                        by_uart_read_8bit = Q_ui8_uart_image_revice.pop(0)   ## read chksum (Byte단위[8bit])
                        # ##############################
                        # # 들어오는 Bit
                        # print(" : by_uart_read_8bit : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                        # ##############################
                        uartrecive_uart_recive_buf.ui8_chksum = by_uart_read_8bit[0]
                        
                        # chksum = checksum_cmd(uartrecive_uart_recive_buf)
                        chksum = checksum(uartrecive_uart_recive_buf)
                        if chksum == uartrecive_uart_recive_buf.ui8_chksum:
                            # 동기화 기능 활성화 인 경우
                            if b_uart_image_recive_chk:
                                uart_sender_transaction(hex(CMD_SIGNAL), 1, hex(CMD_ADDR), 4, "00")
                            
                            # REG Queue 저장
                            i_reg_addr_32bit = 0
                            i_reg_data_32bit = 0
                            i_q_reg_insert = []
                            for i_sel_8bit in range(4):
                                i_reg_addr_32bit = i_reg_addr_32bit | (uartrecive_uart_recive_buf.ui8_addr[i_sel_8bit] << (8 * i_sel_8bit))
                                i_reg_data_32bit = i_reg_data_32bit | (uartrecive_uart_recive_buf.ui8_data[i_sel_8bit] << (8 * i_sel_8bit))
                            # print("i_reg_addr_32bit : ", hex(i_reg_addr_32bit), end="\t")
                            # print("i_reg_data_32bit : ", hex(i_reg_data_32bit))
                            i_q_reg_insert.append(i_reg_addr_32bit)
                            i_q_reg_insert.append(i_reg_data_32bit)
                            memory.Q_ui32_uart_reg_revice_64bit.append(i_q_reg_insert)
                            
                            # Addr 배열 초기화
                            uartrecive_uart_recive_buf.ui8_addr = []
                            # Data 배열 초기화
                            uartrecive_uart_recive_buf.ui8_data = []
                            
                            if i_error_bit_count > 0:
                                print("error_bit : ", i_error_bit_count)
                                i_error_bit_count = 0
                        else:
                            # 동기화 기능 활성화 인 경우
                            if b_uart_image_recive_chk:
                                uart_sender_transaction(hex(CMD_SIGNAL), 1, hex(CMD_ADDR), 4, "03")
                            print("\nCMD_SIGNAL -> chksum X")
                            # Error Bit 증가
                            i_error_bit_count += 1
 
                    # CMD ERROR
                    else:
                        print("\nCMD_SIGNAL -> CMD ERROR : ", by_uart_read_8bit[0], " ", hex(by_uart_read_8bit[0]))
                        # Addr 배열 초기화
                        uartrecive_uart_recive_buf.ui8_addr = []
                        # Data 배열 초기화
                        uartrecive_uart_recive_buf.ui8_data = []
                        # Error Bit 증가
                        i_error_bit_count += 1
                        
                        # 동기화 기능 활성화 인 경우
                        if b_uart_image_recive_chk:
                            uart_sender_transaction(hex(CMD_SIGNAL), 1, hex(CMD_ADDR), 4, "01")
                        
                else:
                    # Addr 배열 초기화
                    uartrecive_uart_recive_buf.ui8_addr = []
                    # Data 배열 초기화
                    uartrecive_uart_recive_buf.ui8_data = []
                    # Error Bit 증가
                    if i_error_bit_count > 0:
                        i_error_bit_count += 1
                        
            if b_exit == True:
                print("uart b_exit")
                break
            
            memory.time.sleep(0.0001)
        except KeyboardInterrupt:
            b_exit = True
            break
    ## Tread 반복
    
# 입력 값 겁증
# A~F 이외 불가
def cmd_check(s_input):
    i_pass = 0
    # 8자리 이상
    if len(s_input) > 8:
        i_pass = 1
    else:
        for i in range(len(s_input)):
            # 정상 범위
            if not(
                # a 이상 f 이하
                (ord(s_input[i]) >= 97 and ord(s_input[i]) <= 102) 
                # A 이상 F 이하
                or (ord(s_input[i]) >= 65 and ord(s_input[i]) <= 70) 
                # 0 이상 9이하
                or (ord(s_input[i]) >= 48 and ord(s_input[i]) <= 57) 
                ):
                i_pass = 2
                break
    return i_pass

# 8자리 만들기
def cmd_length(s_input):
    s_output = s_input
    for i_count in range(8 - len(s_input)):
        s_output = "0" + s_output
    return s_output
    
# CMD 전송
def uart_send_cmd():
    global b_exit
    b_CMD = False
    b_ADDR_done = False
    s_addr = ""
    s_data = ""
    
    while True:
        try:
            # if b_CMD:
            #     if not b_ADDR_done:
            #         print("addr : ",end="")
            #     else:
            #         print("value : ",end="")
            
            # 타이핑 CMD 입력
            while len(memory.Q_ui32_CMD_32bit) == 0:
                memory.time.sleep(0.0001)
                
            s_hex_input = memory.Q_ui32_CMD_32bit.pop(0)
            i_cmd_chk_error = cmd_check(s_hex_input)
            # 명령어 동작 #####################################################################
            if i_cmd_chk_error == 0:
                # 8자리 생성
                s_hex_input_8 = cmd_length(s_hex_input)
                # print("s_hex_input_8 : ", s_hex_input_8)
                if b_CMD:
                    if not b_ADDR_done:
                        s_addr = s_hex_input_8
                        b_ADDR_done = True
                    else:
                        s_data = s_hex_input_8
                        # uart_sender_transaction(hex(CMD_SIGNAL), 1, hex(CMD_ADDR)[2:], 4, s_data)
                        uart_sender_transaction(hex(CMD_SIGNAL), 4, s_addr, 4, s_data)
                        b_CMD = False
                        b_ADDR_done = False
                
                # 전송한 CMD가 1이면
                elif s_hex_input == "1":
                    # ADDR, DATA 2회 더 입력
                    # uart_sender_transaction(hex(CMD_SIGNAL), 1, hex(CMD_ADDR)[2:], 4, s_data)
                    s_addr = hex(CMD_ADDR)[2:]
                    s_data = s_hex_input_8
                    b_CMD = True
                    uart_sender_transaction(hex(CMD_SIGNAL), 1, s_addr, 4, s_data)
                else:
                    s_addr = hex(CMD_ADDR)[2:]
                    s_data = s_hex_input_8
                    uart_sender_transaction(hex(CMD_SIGNAL), 1, s_addr, 4, s_data)
            # 명령어 동작 #####################################################################
            elif i_cmd_chk_error == 1:
                print(s_hex_input, " is Length Over(Under 8 Length)")
            elif i_cmd_chk_error == 2:
                print(s_hex_input, " is Wrong CMD")
            else:
                print(s_hex_input, " is ERROR")
            
        except KeyboardInterrupt:
            b_exit = True
            break