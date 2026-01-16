
import memory
import uart
import opencv
import code_viewer
import csv_output

i_count = 0

def queue_process():
    global i_count    
    while 1:
        try:
            if len(uart.Q_frame_buffer) > 0:
                print("i_count : ", i_count)
                F_pop_frame = uart.Q_frame_buffer.pop(0)
                opencv.Q_image_viewer_buffer.append([F_pop_frame, i_count])
                code_viewer.Q_code_viewer_buffer.append([F_pop_frame, i_count])
                csv_output.Q_csv_output_buffer.append([F_pop_frame, i_count])
                i_count += 1
            else:
                memory.time.sleep(0.001)
        except KeyboardInterrupt:
            uart.b_exit = True
            break