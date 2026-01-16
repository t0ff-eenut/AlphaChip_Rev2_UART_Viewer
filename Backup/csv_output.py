import csv
import memory
import opencv
from datetime import datetime

b_exit = False
Q_csv_output_buffer = []

def csv_output():
    global b_exit
    
    # 현재 날짜 및 시간
    now = datetime.now()
    # 문자열로 변환
    now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    
    code_data = []
    F_bakcup = memory.np.zeros((64,64),dtype=memory.np.uint8)
    diff_code_data = []
    
    while 1:
        try:
            
            if len(Q_csv_output_buffer) > 0:
                
                
                pop_data = Q_csv_output_buffer.pop(0)
                print("csv ")
                print(pop_data)
                F_pop_frame = pop_data[0]
                
                # Frame Number
                code_data.append([pop_data[1]])
                # 범례
                code_data_x = [""]
                for x in range(64):
                    code_data_x.append(str(x))
                code_data.append(code_data_x)
                        
                for y in range(64):
                    code_data_x = []
                    code_data_x.append(str(y))
                    for x in range(64):
                        # print(F_pop_frame[y][x],end=' ')
                        # print(str(F_pop_frame[y][x]),end=' ')
                        code_data_x.append(str(F_pop_frame[y][x]))
                    # print(code_data_x)
                    # print()
                    code_data.append(code_data_x)
                
                
                
                code_data.append("")
                # for y in range(4):
                #     code_data_x = ["value"]
                #     for x in range(64*y, 64*(y+1), 1):
                #         code_data_x.append(str(x))
                #     code_data.append(code_data_x)
                #     code_data_x = ["count"]
                #     for x in range(64*y, 64*(y+1), 1):
                        
                #         count = 0
                #         for index in range(64):
                #             count += memory.np.count_nonzero(F_pop_frame[index] == x)
                #         code_data_x.append(count)
                        
                #     code_data.append(code_data_x)
                
                
                code_data_x = ["value"]
                for x in range(256):
                    code_data_x.append(str(x))
                code_data.append(code_data_x)
                code_data_x = ["count"]
                for x in range(256):
                    count = 0
                    for index in range(64):
                        count += memory.np.count_nonzero(F_pop_frame[index] == x)
                    code_data_x.append(count)
                code_data.append(code_data_x)
                code_data.append("")
                
                # print()
                # for y in range(64):
                #     print(code_data[y])
                # print(len(Q_csv_output_buffer))        
                # data = [
                #     ["Name", "Age", "City"],
                #     ["Alice", 30, "Seoul"],
                #     ["Bob", 25, "Busan"]
                # ]
                # print(code_data)
                # CSV 파일로 저장
                with open("csv/image_"+now_str+".csv", "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(code_data)
                    

                F_diff_frame = opencv.cv2.absdiff(F_bakcup, F_pop_frame)
                # Frame Number
                diff_code_data.append([str(pop_data[1] - 1) + " ---> " + str(pop_data[1])])
                # 범례
                diff_code_data_x = [""]
                for x in range(64):
                    diff_code_data_x.append(str(x))
                diff_code_data.append(diff_code_data_x)
                        
                for y in range(64):
                    diff_code_data_x = []
                    diff_code_data_x.append(str(y))
                    for x in range(64):
                        # print(F_pop_frame[y][x],end=' ')
                        # print(str(F_pop_frame[y][x]),end=' ')
                        diff_code_data_x.append(str(F_diff_frame[y][x]))
                    # print(code_data_x)
                    # print()
                    diff_code_data.append(diff_code_data_x)
                    
                    
                diff_code_data.append("")
                # for y in range(4):
                #     diff_code_data_x = ["value"]
                #     for x in range(64*y, 64*(y+1), 1):
                #         diff_code_data_x.append(str(x))
                #     diff_code_data.append(diff_code_data_x)
                #     diff_code_data_x = ["count"]
                #     for x in range(64*y, 64*(y+1), 1):
                #         count = 0
                #         for index in range(64):
                #             count += memory.np.count_nonzero(F_diff_frame[index] == x)
                        
                #         diff_code_data_x.append(count)
                #     diff_code_data.append(diff_code_data_x)
                    
                diff_code_data_x = ["value"]
                for x in range(256):
                    diff_code_data_x.append(str(x))
                diff_code_data.append(diff_code_data_x)
                diff_code_data_x = ["count"]
                for x in range(256):
                    count = 0
                    for index in range(64):
                        count += memory.np.count_nonzero(F_diff_frame[index] == x)
                    diff_code_data_x.append(count)
                diff_code_data.append(diff_code_data_x)
                diff_code_data.append("") 
                    
                    
                with open("csv/diff_image_"+now_str+".csv", "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(diff_code_data)
                    
                F_bakcup = F_pop_frame
                
            else:
                memory.time.sleep(0.001)
                
            if b_exit == True:
                print("code_viewer b_exit")
                break
        except KeyboardInterrupt:
            b_exit = True
            break
    