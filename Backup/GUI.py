import threading as THR
import tkinter as tk
import memory


##########################################################################################################
# [ ADDR      ] [ VAL       ] [ R/W ] [ NAME       ] [ DEFAULT   ] [ MIN ] [ MAX ] [ BITS ] [ START ]
#  0x00000010    0x12345678    RW     LED_CTRL       0x00000000    0x00    0xFF     8         0
#  0x00000014    0x00000001    RW     ENABLE         0x00000001    0x00    0x01     1         8

# [Read] [Write Selected] [Write All]   검색: [________] [검색]
##########################################################################################################
# 🟩 1. 레지스터 목록 보기 및 편집
# 주소, 값, 읽기/쓰기 여부, 설명 필드 표시

# 값(VAL)은 Entry로 수정 가능하게

# 직접 수정 후 Write 버튼으로 반영

# 🟩 2. 읽기/쓰기 기능
# [Read] 버튼 클릭 시: 주소에 해당하는 값을 읽어서 표시

# [Write] 클릭 시: 값(VAL)을 쓰기

# 전체 레지스터 일괄 Write (Write All 버튼)

# 🟩 3. 검색 / 필터링
# 레지스터 이름 or 주소 기준 검색창 (Entry + Filter 버튼)

# 특정 조건만 필터링해서 볼 수 있음 (예: CPU 전용, ISP 전용 등)

# 🟩 4. 자동 갱신
# 일정 주기마다 읽어서 갱신 (Auto Refresh 체크박스 + 주기 설정 Spinbox)

# 🟩 5. 수정 전/후 비교
# 변경된 값은 하이라이트 처리 (ex: 노란색 배경)

# 원래 값과 수정 값 비교

# 🟩 6. 저장/불러오기
# 전체 레지스터 값을 파일로 저장/불러오기 (.csv or .json)

# 레지스터 테스트 시 유용함

        
        
# Label	        텍스트나 이미지를 표시하는 데 사용
# Button	    버튼을 생성, 클릭 이벤트 처리 가능
# Entry	        한 줄짜리 텍스트 입력 필드
# Text	        여러 줄 텍스트 입력 필드
# Checkbutton	체크박스 형태의 버튼
# Radiobutton	라디오 버튼 (옵션 중 하나 선택)
# Listbox	    리스트 항목을 보여주고 선택 가능
# Canvas	    도형, 이미지, 그래픽 등을 그릴 수 있는 공간
# Scale	        슬라이더 형태로 값 선택
# Spinbox	    숫자 또는 값 범위 선택용 위젯
# Scrollbar	    스크롤 바 추가 (Listbox, Text 등과 함께 사용)
# Frame	        다른 위젯들을 묶어 배치하는 용도 (컨테이너 역할)
# LabelFrame	테두리와 제목이 있는 Frame
# Toplevel	    새 창 생성 (메인 윈도우 외의 별도 창)
# Message	    자동 줄 바꿈이 적용된 Label (긴 텍스트 표시용)
# PanedWindow	여러 패널을 수평 또는 수직으로 나눌 수 있는 컨테이너
# Menu	        메뉴바, 드롭다운 메뉴 등을 구성할 때 사용
# Menubutton	메뉴를 열 수 있는 버튼 (드롭다운 형태)
# OptionMenu	드롭다운 선택 메뉴 (간단한 옵션 선택용

def greet():
    print("tkinter_thr - greet 실행")

def open_window():
    new_win = tk.Toplevel()
    tk.Label(new_win, text="새 창입니다").pack()

def hello():
    print("Hello!")

A_labelframe_reg_name = []
A_labelframe_reg_index = []

def reg_name_output(i_reg_count, s_reg_name, i_reg_val_int):
    return f"[{i_reg_count} - {0x3d0000 + (8 * i_reg_count):06X}] {s_reg_name:<85} {i_reg_val_int:>012} 0x{i_reg_val_int:>08X} 0b{i_reg_val_int:>032b}"

def refresh_all():
    print("새로고침 버튼 클릭됨")
    # read
    memory.Q_ui32_CMD_32bit.append("0")

def tkinter_thr():
    font_fixed = ("Courier New", 10)
    tk_viewer = tk.Tk()

    # 🌟 새로고침 버튼 추가 위치 시작
    top_frame = tk.Frame(tk_viewer)
    top_frame.pack(fill="x", padx=10, pady=5)

    refresh_button = tk.Button(top_frame, text="🔄 새로고침", font=font_fixed, command=refresh_all)
    refresh_button.pack(side="left")
    # 🌟 새로고침 버튼 추가 위치 끝

    ###########################################################################
    # 캔버스 + 스크롤바 기본 설정
    canvas = tk.Canvas(tk_viewer)
    scrollbar = tk.Scrollbar(tk_viewer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # 스크롤 자동 갱신
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    scrollable_frame.bind("<Configure>", on_configure)
    
    
    # 🖱 마우스 휠 이벤트 바인딩 (OS별)
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(event):  # Linux는 Button-4/5 사용
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    # Windows/macOS
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Linux (X11)
    canvas.bind_all("<Button-4>", _on_mousewheel_linux)
    canvas.bind_all("<Button-5>", _on_mousewheel_linux)
    ###########################################################################
    
    s_anchor = "w"
    #anchor="w" 왼
    #anchor="e" 오
    #anchor=s_anchor
    i_number_size = 10
    i_addr_size = 16
    i_rw_size = 10
    i_name_size = 50
    i_value_size = 10
    i_bits_size = 10
    
    ###########################################################################
    # 기본 틀 작성
    for i_reg_count in range(len(memory.A_REGISTERS)):
        
        labelframe_reg_name = tk.LabelFrame(scrollable_frame, text="REG 이름", font=font_fixed)
        # tk.Checkbutton(labelframe_reg_name, text="선택 1").pack(anchor="w")
        # tk.Checkbutton(labelframe_reg_name, text="선택 2").pack(anchor="w")
        
        # 번호  주소소  CPU R/W     ISP R/W     이름    Default     MIN     MAX     Bits    Start Bit #
        header_frame = tk.Frame(labelframe_reg_name)
        header_frame.pack(fill="x", padx=5, pady=2)

        tk.Label(header_frame, text="Number",       font=font_fixed, width=i_number_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="Addr",         font=font_fixed, width=i_addr_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="CPU R/W",      font=font_fixed, width=i_rw_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="ISP R/W",      font=font_fixed, width=i_rw_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="Name",         font=font_fixed, width=i_name_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="Value",        font=font_fixed, width=i_value_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="Min",          font=font_fixed, width=i_value_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="Max",          font=font_fixed, width=i_value_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="Bits",         font=font_fixed, width=i_bits_size, anchor=s_anchor).pack(side="left")
        tk.Label(header_frame, text="Start Bit",    font=font_fixed, width=i_bits_size, anchor=s_anchor).pack(side="left")
        
        def on_enter_pressed(event, i_reg_count, i_value_count):
            entry_value = event.widget  # 엔터가 눌린 Entry 위젯
            i_new_value = int(entry_value.get(), 16)
            # print("i_reg_count : ", i_reg_count)
            # print("i_value_count : ", i_value_count)
            i_original_value = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Value']]  # 원래 값

            try:
                # original_value와 new_value_int를 비교
                if i_original_value != i_new_value:
                    s_addr = hex(0x3d0000 + (8 * i_reg_count))[2:]
                    print("ADDR - ", s_addr)
                    
                    print(f"Value changed! Original: {hex(i_original_value)}, New: {hex(i_new_value)}")
                    
                    # write CMD
                    memory.Q_ui32_CMD_32bit.append("1")
                    # ADDR 
                    memory.Q_ui32_CMD_32bit.append(s_addr)
                    
                    # # 원래 값이 변경된 경우 메모리 업데이트
                    original = memory.copy.deepcopy(memory.A_REGISTERS[i_reg_count])
                    original[i_value_count][memory.REG_INDEX['Value']] = i_new_value
                    # print("original[i_value_count][memory.REG_INDEX['Value']] : ", original[i_value_count][memory.REG_INDEX['Value']])
                    # print("emory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Value']] : ", memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Value']])
                    s_reg_val_hex = memory.gen_32bit_process(original)[1][2:]
                    # print("reg_val_hex : ", s_reg_val_hex)
                    
                    # VALUE
                    memory.Q_ui32_CMD_32bit.append(s_reg_val_hex)

                    # read CMD
                    memory.Q_ui32_CMD_32bit.append("0")

            except ValueError:
                print("Invalid value. Please enter a valid hexadecimal number.")
        
        
        A_labelframe_reg_value = []
        for i_value_count in range(len(memory.A_REGISTERS[i_reg_count]) - 1, -1, -1):
            label_value = []
            # 값 라벨 추가 예시
            value_frame = tk.Frame(labelframe_reg_name)
            value_frame.pack(fill="x", padx=5, pady=2)
            label_value.append(value_frame)
            label = tk.Label(value_frame, text=str(len(memory.A_REGISTERS[i_reg_count]) - i_value_count),  font=font_fixed, width=i_number_size, anchor=s_anchor).pack(side="left")
            label_value.append(label)
            i_start_bits = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Start_Bits']]
            i_bits = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Bits']]
            i_bit_mask = 0
            for i_bit in range(i_bits):
                i_bit_mask = i_bit_mask | (1 << i_bit)
            i_addr = i_bit_mask << i_start_bits            
            label = tk.Label(value_frame, text=f"{i_addr:08X}",     font=font_fixed, width=i_addr_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            s_cpu_rw = memory.NUM_2_RW[memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['CPU_R/W']]]
            label = tk.Label(value_frame, text=s_cpu_rw,            font=font_fixed, width=i_rw_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            s_isp_rw = memory.NUM_2_RW[memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['ISP_R/W']]]
            label = tk.Label(value_frame, text=s_isp_rw,            font=font_fixed, width=i_rw_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            s_value_name = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['NAME']]
            label = tk.Label(value_frame, text=s_value_name,        font=font_fixed, width=i_name_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            
            # i_value = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Value']]
            # label = tk.Label(value_frame, text=f"{i_value:08X}",    font=font_fixed, width=i_value_size, anchor=s_anchor)
            # label.pack(side="left")
            # label_value.append(label)
            
            # 값 (Entry 위젯으로 수정 가능하게)
            i_value = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Value']]
            entry_value = tk.Entry(value_frame, font=font_fixed, width=i_value_size)
            entry_value.insert(0, f"{i_value:08X}")  # 초기값 설정
            entry_value.pack(side="left")
            # 엔터 키 이벤트 처리
            entry_value.bind("<Return>", lambda event, reg_count=i_reg_count, value_count=i_value_count: on_enter_pressed(event, reg_count, value_count))
            label_value.append(entry_value)
            
            i_min = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['MIN']]
            label = tk.Label(value_frame, text=f"{i_min:08X}",      font=font_fixed, width=i_value_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            i_max = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['MAX']]
            label = tk.Label(value_frame, text=f"{i_max:08X}",      font=font_fixed, width=i_value_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            i_bits = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Bits']]
            label = tk.Label(value_frame, text=f"{i_bits}",         font=font_fixed, width=i_bits_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            i_start_bits = memory.A_REGISTERS[i_reg_count][i_value_count][memory.REG_INDEX['Start_Bits']]
            label = tk.Label(value_frame, text=f"{i_start_bits}",   font=font_fixed, width=i_bits_size, anchor=s_anchor)
            label.pack(side="left")
            label_value.append(label)
            A_labelframe_reg_value.append(label_value)
        
        
        
        # labelframe_reg_name.pack(padx=10, pady=10, anchor=s_anchor)
        labelframe_reg_name.pack(fill="x", padx=10, pady=5)  # fill + padx로 같은 너비처럼 보이게
        # labelframe_reg_name.update_idletasks()  # 내부 정렬 강제 갱신
        A_labelframe_reg_name.append(labelframe_reg_name)
        A_labelframe_reg_index.append(A_labelframe_reg_value)
        
    # 수정 방법
    for i_reg_count in range(len(memory.A_REGISTERS)):
        reg_name = memory.REG_NUM_2_REG_NAME[i_reg_count]
        reg_val_int = memory.gen_32bit_process(memory.A_REGISTERS[i_reg_count])[0]

        A_labelframe_reg_name[i_reg_count].configure( # :>08X
            text=reg_name_output(i_reg_count, reg_name, reg_val_int)
        )
    
    tk_viewer.update_idletasks()  # 레이아웃 계산 완료
    required_width = labelframe_reg_name.winfo_reqwidth() + 30
    tk_viewer.geometry(f"{required_width}x600")  # 높이는 적당히 설정
    tk_viewer.mainloop()
    

def GUI_start():
    # tkinter
    thr_GUI_thread = THR.Thread(name="tkinter THREAD", target=tkinter_thr, daemon=1)     # GUI Control Thread
    thr_GUI_thread.start()
    
    # Recive REG Value
    while 1:
        try:
            if len(memory.Q_ui32_uart_reg_revice_64bit) > 0:
                A_reg_info = memory.Q_ui32_uart_reg_revice_64bit.pop(0)
                # print("ADDR : ", hex(A_reg_info[0]), "\tData", hex(A_reg_info[1]))
                memory.reg_setting_process(A_reg_info[0], A_reg_info[1])
            else:
                memory.time.sleep(0.001)
        except KeyboardInterrupt:
            break