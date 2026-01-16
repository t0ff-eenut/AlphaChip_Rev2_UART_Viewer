import cv2
import threading as THR
from PIL import Image
import uart
import code_viewer

Q_image_viewer_buffer = []
Q_code_viewer_output_buffer = []

def opencv_image_viewer():

    # print("cv open")
    cv2.startWindowThread()
    cv2.namedWindow("IMAGE", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("IMAGE", 1024, 1024)
    cv2.moveWindow("IMAGE", 0, 0)
    
    cv2.namedWindow("CODE", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("CODE", 1024, 1024)
    cv2.moveWindow("CODE", 1024, 0)
    
    
    while 1:
        try:
            if len(Q_image_viewer_buffer) > 0:
                # print(len(uart.Q_frame_buffer))
                pop_data = Q_image_viewer_buffer.pop(0)
                # print("opencv ")
                # print(pop_data)
                F_pop_frame = pop_data[0]
                
                cv2.imshow("IMAGE", F_pop_frame)
                # cv2.imwrite('image_save\Capture_' + str(i_image_num) + '.pgm', F_pop_frame)
                
                # code_viewer.Q_code_viewer_buffer.append(F_pop_frame)
                
                if len(Q_code_viewer_output_buffer) > 0:
                    pop_data = Q_code_viewer_output_buffer.pop(0)
                    F_pop_code = pop_data[0]
                    cv2.imshow("CODE", F_pop_code)
                
            else:
                if cv2.waitKey(1) & 0xFF == 27 : # enter ESC
                    uart.b_exit = True
                    break
                # print("wait x")
                # 아래 2개 라인을 추가하여 imshow로 열린 image라는 title의 창의 상단 메뉴 x버튼이 정상동작하게 함.
                if cv2.getWindowProperty('IMAGE', cv2.WND_PROP_VISIBLE) < 1:
                    uart.b_exit = True
                    break
        except KeyboardInterrupt:
            uart.b_exit = True
            break

    # cv2.destroyAllWindows()