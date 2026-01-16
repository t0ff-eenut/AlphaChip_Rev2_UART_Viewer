import memory
import opencv

b_exit = False
Q_code_viewer_buffer = []

def code_viewer():
    global b_exit
    while 1:
        try:
            if len(Q_code_viewer_buffer) > 0:                
                pop_data = Q_code_viewer_buffer.pop(0)
                # print("code_viewer\n", pop_data)
                F_pop_frame = pop_data[0]
                # print("code_viewer ")
                # print(F_pop_frame)
                # cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
                # | 매개변수               | 설명                                                            |
                # | ------------------ | ------------------------------------------------------------- |
                # | `img`              | 대상 이미지                                                        |
                # | `text`             | 출력할 문자열                                                       |
                # | `org`              | 시작 좌표 (왼쪽 아래 기준)                                              |
                # | `fontFace`         | 폰트 종류 (`cv2.FONT_HERSHEY_SIMPLEX`, `FONT_HERSHEY_COMPLEX`, 등) |
                # | `fontScale`        | 크기 (기본=1.0)                                                   |
                # | `color`            | 텍스트 색상 (BGR 튜플)                                               |
                # | `thickness`        | 글자 두께                                                         |
                # | `lineType`         | 선 스타일 (`cv2.LINE_AA`, `cv2.LINE_8`, 등)                        |
                # | `bottomLeftOrigin` | True이면 원점 기준을 아래로 (기본은 False)                                 |
                F_text_image = memory.np.ones((1024, 1120, 3), dtype=memory.np.uint8) * 255
                
                for x in range(64): 
                    opencv.cv2.putText(F_text_image,                        # 대상 이미지
                                        str(x),                       # 출력할 텍스트
                                        # "255",                       # 출력할 텍스트
                                        (((x + 1) * 17), 10),                     # 위치 (왼쪽 아래 좌표 기준)
                                        opencv.cv2.FONT_HERSHEY_SIMPLEX,    # 폰트
                                        0.25,                                # 폰트 크기(scale)
                                        (0, 0, 255),                          # 색상 (B, G, R)
                                        1,                                  # 두께
                                        opencv.cv2.LINE_AA)                 # 선 타입 (안티에일리어싱)
                    
                for y in range(64): 
                    opencv.cv2.putText(F_text_image,                        # 대상 이미지
                                        str(y),                       # 출력할 텍스트
                                        (0, ((y + 1) * 15)+ 10),                      # 위치 (왼쪽 아래 좌표 기준)
                                        opencv.cv2.FONT_HERSHEY_SIMPLEX,    # 폰트
                                        0.25,                                # 폰트 크기(scale)
                                        (0, 0, 255),                          # 색상 (B, G, R)
                                        1,                                  # 두께
                                        opencv.cv2.LINE_AA)                 # 선 타입 (안티에일리어싱)
                
                for y in range(64):
                    for x in range(64):    
                        opencv.cv2.putText(F_text_image,                        # 대상 이미지
                                            str(F_pop_frame[y][x]),             # 출력할 텍스트
                                            (17 + (x * 17), 10 + 15 + (y*15)),                          # 위치 (왼쪽 아래 좌표 기준)
                                            opencv.cv2.FONT_HERSHEY_SIMPLEX,    # 폰트
                                            0.25,                                # 폰트 크기(scale)
                                            (0, 0, 0),                        # 색상 (B, G, R)
                                            1,                                  # 두께
                                            opencv.cv2.LINE_AA)                 # 선 타입 (안티에일리어싱)
                    
                opencv.Q_code_viewer_output_buffer.append([F_text_image,pop_data[1]])
                
            else:
                memory.time.sleep(0.001)
                
            if b_exit == True:
                print("code_viewer b_exit")
                break
        except KeyboardInterrupt:
            b_exit = True
            break
    