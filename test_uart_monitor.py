"""
UART 데이터 직접 모니터링 도구

수신되는 raw 바이트 데이터를 실시간으로 확인
"""

import serial
import serial.tools.list_ports


def list_ports():
    """사용 가능한 포트 목록 출력"""
    ports = serial.tools.list_ports.comports()
    print("\n=== 사용 가능한 COM 포트 ===")
    for i, port in enumerate(ports):
        print(f"  [{i}] {port.device}: {port.description}")
    return ports


def monitor_uart(port: str, baud_rate: int = 2000000):
    """
    UART 데이터 모니터링
    
    Args:
        port: COM 포트 (예: "COM3")
        baud_rate: 보레이트 (기본: 2000000)
    """
    print(f"\n=== UART 모니터링 시작 ===")
    print(f"포트: {port}")
    print(f"보레이트: {baud_rate}")
    print(f"Ctrl+C로 종료")
    print("=" * 50)
    
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud_rate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1
        )
        print(f"✓ {port} 연결됨\n")
        
        byte_count = 0
        line_count = 0
        
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                
                # Hex 형식으로 출력
                hex_str = " ".join(f"{b:02X}" for b in data)
                
                # ASCII 형식 (출력 가능한 문자만)
                ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in data)
                
                byte_count += len(data)
                line_count += 1
                
                # 출력
                print(f"[{line_count:04d}] ({len(data):3d} bytes, total: {byte_count:6d}) | {hex_str[:60]}...")
                
                # STX 패턴 감지 (0xAA 0x55)
                for i in range(len(data) - 1):
                    if data[i] == 0xAA and data[i+1] == 0x55:
                        print(f"       ★ STX 패턴 감지! 위치: {i}")
                
                # ETX 패턴 감지 (0x55 0xAA)
                for i in range(len(data) - 1):
                    if data[i] == 0x55 and data[i+1] == 0xAA:
                        print(f"       ★ ETX 패턴 감지! 위치: {i}")
                        
    except serial.SerialException as e:
        print(f"✗ 오류: {e}")
    except KeyboardInterrupt:
        print("\n\n모니터링 종료")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("포트 닫힘")


def main():
    ports = list_ports()
    
    if not ports:
        print("사용 가능한 포트가 없습니다.")
        return
    
    # 포트 선택
    try:
        choice = input("\n포트 번호 선택 (또는 COM 이름 직접 입력): ").strip()
        
        if choice.isdigit():
            port = ports[int(choice)].device
        elif choice.upper().startswith("COM"):
            port = choice.upper()
        else:
            port = f"COM{choice}"
        
        # 보레이트 선택
        baud_input = input("보레이트 (기본: 2000000): ").strip()
        baud_rate = int(baud_input) if baud_input else 2000000
        
        monitor_uart(port, baud_rate)
        
    except (ValueError, IndexError) as e:
        print(f"잘못된 입력: {e}")


if __name__ == "__main__":
    main()
