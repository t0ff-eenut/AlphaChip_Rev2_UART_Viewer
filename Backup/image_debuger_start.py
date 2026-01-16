
import numpy as np
import threading as THR
import queue_process
import opencv
import uart
import GUI

import code_viewer
import csv_output

# 설치
#   & C:/Users/iSEN_FW_PC1/AppData/Local/Programs/Python/Python313/python.exe -m pip install pyserial

# 실행
#  & C:/Users/iSEN_FW_PC1/AppData/Local/Programs/Python/Python313/python.exe "z:/iSEN/Chip/Debug 및 실험/ESP32-S3/SPI_UART_241015/image_debuger/image_viewer.py"

# & C:/Users/iSEN_FW_PC1/AppData/Local/Programs/Python/Python313/python.exe -m pip install opencv-python
# & C:/Users/iSEN_FW_PC1/AppData/Local/Programs/Python/Python313/python.exe -m pip install opencv-contrib-python

# & C:/Users/iSEN_FW_PC1/AppData/Local/Programs/Python/Python313/python.exe -m pip install pyinstaller

# PATH 설정
# https://velog.io/@dl950101/Python-%EC%84%A4%EC%B9%98%EC%99%80-%ED%99%98%EA%B2%BD%EC%84%A4%EC%A0%95-VScode%EC%97%90%EC%84%9C-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

if __name__ == '__main__':
    print("uart_init")
    serial_comport_handle = uart.uart_init()
    
    
    queue_process_thread = THR.Thread(name="Queue Process THREAD", target=queue_process.queue_process, daemon=1)     # ISP OUTPUT 동작 Thread
    queue_process_thread.start()
    
    print("opencv_tread")
    # OpenCV
    thr_viewer_thread = THR.Thread(name="Image Viewer THREAD", target=opencv.opencv_image_viewer, daemon=1)     # ISP OUTPUT 동작 Thread
    thr_viewer_thread.start()
    
    # # GUI Control
    # thr_GUI_thread = THR.Thread(name="GUI Control THREAD", target=GUI.GUI_start, daemon=1)     # GUI Control Thread
    # thr_GUI_thread.start()
    
    # Code Viewer
    thr_code_viewer_thread = THR.Thread(name="Code Viewer THREAD", target=code_viewer.code_viewer, daemon=1)     # ISP OUTPUT 동작 Thread
    thr_code_viewer_thread.start()
    
    # # CSV Viewer
    # thr_csv_output_thread = THR.Thread(name="CSV Output THREAD", target=csv_output.csv_output, daemon=1)     # ISP OUTPUT 동작 Thread
    # thr_csv_output_thread.start()
    
    print("view frame init")
    # Frame Value Initial
    F_view_frame = np.zeros((64,64), np.uint8)
    for i_index in range(64*64):
        F_view_frame[int(i_index / 64)][i_index % 64] = i_index % 256
    uart.Q_frame_buffer.append(F_view_frame)

    print("uart revice frame start")
    
    thr_uart_recive_thread = THR.Thread(name="UART Recive THREAD", target=uart.uart_recive_data_process, daemon=1)  # UART Recive Thread
    thr_uart_recive_thread.start()
    
    thr_uart_send_thread = THR.Thread(name="UART Send THREAD", target=uart.uart_send_cmd, daemon=1)                 # ISP OUTPUT 동작 Thread
    thr_uart_send_thread.start()
    
    uart.uart_recive_thread()

    print("end")