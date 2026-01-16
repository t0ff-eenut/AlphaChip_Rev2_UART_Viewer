"""
AlphaChip UART Image Viewer - Frame Parser

ESP32 SPI2UART ImageBridge 프레임 파싱 모듈
"""

import numpy as np
from typing import Callable, Optional
from protocol_config import (
    UART_STX, UART_ETX,
    IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_PAYLOAD_SIZE,
    ParserState
)


class FrameParser:
    """
    UART 이미지 프레임 파서
    
    프로토콜 구조:
    - STX: 0xA5 0xCD (2 bytes)
    - Width: 1 byte (ESP32 전송 순서)
    - Height: 1 byte
    - Payload: height * width bytes (64*64 = 4096 bytes)
    - Checksum: 2 bytes (sum & 0xFFFF, little endian)
    - ETX: 0xB5 0x7A (2 bytes)
    """
    
    def __init__(self, log_callback: Optional[Callable[[str], None]] = None):
        """
        Args:
            log_callback: 로그 메시지를 전달받을 콜백 함수
        """
        self.log_callback = log_callback
        self.reset()
        
        # 통계
        self.stx_count = 0
        self.etx_count = 0
        self.checksum_pass_count = 0
        self.checksum_fail_count = 0
    
    def _log(self, message: str):
        """로그 메시지 전송"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def reset(self):
        """파서 상태 초기화"""
        self.state = ParserState.WAIT_STX_1
        self.height = 0
        self.width = 0
        self.payload = bytearray()
        self.checksum_received = 0
        self.checksum_calc = 0
        self.payload_index = 0
    
    def _calculate_checksum(self, data: bytes) -> int:
        """체크섬 계산 (STX + height + width + payload의 합)"""
        return sum(data) & 0xFFFF
    
    def feed_byte(self, byte: int) -> np.ndarray | None:
        """
        한 바이트씩 파서에 입력
        
        Args:
            byte: 수신된 바이트 (0-255)
        
        Returns:
            완성된 이미지 프레임 (64x64 numpy array) 또는 None
        """
        
        if self.state == ParserState.WAIT_STX_1:
            if byte == 0xA5:  # STX_1
                # print(f"\n[STX_1] 0x{byte:02X} (A5)")
                self.state = ParserState.WAIT_STX_2
                self.checksum_calc = byte
            # else: 계속 STX 대기
        
        elif self.state == ParserState.WAIT_STX_2:
            if byte == 0xCD:  # STX_2
                # print(f"[STX_2] 0x{byte:02X} (CD) -> STX 완료!")
                self.state = ParserState.WAIT_HEIGHT
                self.checksum_calc += byte
                self.stx_count += 1
                print(f"[STX] 프레임 #{self.stx_count} 시작 [Signal: 0xA5CD, Input: 0xA5{byte:02X}]")  # ★ STX 완료 시에만 출력
            else:
                # print(f"[STX_2] 0x{byte:02X} (expected CD) -> 불일치, 리셋")
                self.reset()
                # ★ 현재 바이트가 STX_1인지 다시 확인
                if byte == 0xA5:
                    # print(f"\n[STX_1] 0x{byte:02X} (A5) <- 재확인")
                    self.state = ParserState.WAIT_STX_2
                    self.checksum_calc = byte
        
        elif self.state == ParserState.WAIT_HEIGHT:
            # ESP32는 WIDTH를 먼저 전송함 (utfs 구조체 순서)
            self.width = byte
            self.checksum_calc += byte
            self.state = ParserState.WAIT_WIDTH
            # print(f"[WIDTH] 0x{byte:02X} = {byte}")
        
        elif self.state == ParserState.WAIT_WIDTH:
            # ESP32는 HEIGHT를 나중에 전송함
            self.height = byte
            self.checksum_calc += byte
            self.payload = bytearray()
            self.payload_index = 0
            self.state = ParserState.WAIT_PAYLOAD
            # print(f"[HEIGHT] 0x{byte:02X} = {byte}")
            # print(f"[PAYLOAD] 수신 시작... ({self.height}x{self.width} = {self.height * self.width} bytes)")
        
        elif self.state == ParserState.WAIT_PAYLOAD:
            self.payload.append(byte)
            self.checksum_calc += byte
            self.payload_index += 1
            
            expected_size = self.height * self.width
            if self.payload_index >= expected_size:
                # print(f"[PAYLOAD] 수신 완료 ({self.payload_index} bytes)")
                self.state = ParserState.WAIT_CHECKSUM_L
        
        elif self.state == ParserState.WAIT_CHECKSUM_L:
            self.checksum_received = byte  # Low byte
            self.state = ParserState.WAIT_CHECKSUM_H
            # print(f"[CHKSUM_L] 0x{byte:02X}")
        
        elif self.state == ParserState.WAIT_CHECKSUM_H:
            self.checksum_received |= (byte << 8)  # High byte
            self.state = ParserState.WAIT_ETX_1
            # print(f"[CHKSUM_H] 0x{byte:02X} -> Checksum: 0x{self.checksum_received:04X}")
        
        elif self.state == ParserState.WAIT_ETX_1:
            if byte == 0xB5:  # ETX_1
                # print(f"[ETX_1] 0x{byte:02X} (B5)")
                self.state = ParserState.WAIT_ETX_2
            else:
                # print(f"[ETX_1] 0x{byte:02X} (expected B5) -> 불일치!")
                expected_size = self.height * self.width
                checksum_calc_now = self.checksum_calc & 0xFFFF
                print(f"[ETX_1 불일치] 0x{byte:02X} (expected 0xB5) | Payload: {self.payload_index}/{expected_size} bytes | Checksum calc: 0x{checksum_calc_now:04X}, recv: 0x{self.checksum_received:04X}")
                self.reset()
                # ★ 현재 바이트가 STX_1인지 다시 확인
                if byte == 0xA5:
                    # print(f"\n[STX_1] 0x{byte:02X} (A5) <- 재확인")
                    self.state = ParserState.WAIT_STX_2
                    self.checksum_calc = byte
        
        elif self.state == ParserState.WAIT_ETX_2:
            if byte == 0x7A:  # ETX_2
                self.etx_count += 1
                # 프레임 완성! 체크섬 검증
                checksum_calc_final = self.checksum_calc & 0xFFFF
                
                if checksum_calc_final == self.checksum_received:
                    self.checksum_pass_count += 1
                    print(f"[ETX] 프레임 #{self.etx_count} 완료 ✅ [Signal: 0xB57A, Input: 0xB5{byte:02X}] (체크섬 0x{self.checksum_received:04X})")  # ★ 성공만 출력
                    # 체크섬 일치 - 이미지 반환
                    try:
                        image = np.frombuffer(bytes(self.payload), dtype=np.uint8)
                        image = image.reshape((self.height, self.width))
                        self.reset()
                        return image
                    except ValueError as e:
                        print(f"[ETX] 이미지 reshape 실패: {e}")
                        self.reset()
                        return None
                else:
                    self.checksum_fail_count += 1
                    print(f"[ETX] 체크섬 실패 ❌ received=0x{self.checksum_received:04X}, calc=0x{checksum_calc_final:04X}")  # ★ 실패만 출력
            else:
                print(f"[ETX_2 불일치] 0x{byte:02X} (expected 0x7A)")  # ★ 에러만 출력
            
            self.reset()
            # ★ 현재 바이트가 STX_1인지 다시 확인 (프레임 연속 수신 시 중요!)
            if byte == 0xA5:
                # print(f"\n[STX_1] 0x{byte:02X} (A5) <- 재확인")
                self.state = ParserState.WAIT_STX_2
                self.checksum_calc = byte
        
        return None
    
    def feed_bytes(self, data: bytes) -> list[np.ndarray]:
        """
        여러 바이트를 한 번에 파서에 입력
        
        Args:
            data: 수신된 바이트 데이터
        
        Returns:
            완성된 이미지 프레임들의 리스트
        """
        frames = []
        for byte in data:
            frame = self.feed_byte(byte)
            if frame is not None:
                frames.append(frame)
        return frames
    
    def get_stats(self) -> dict:
        """파싱 통계 반환"""
        return {
            "stx_count": self.stx_count,
            "etx_count": self.etx_count,
            "checksum_pass": self.checksum_pass_count,
            "checksum_fail": self.checksum_fail_count,
        }


# 테스트용
if __name__ == "__main__":
    # 테스트 프레임 생성
    test_payload = bytes(range(256)) * 16  # 4096 bytes
    
    # 체크섬 계산
    checksum_data = bytes([0xA5, 0xCD, 64, 64]) + test_payload
    checksum = sum(checksum_data) & 0xFFFF
    
    # 프레임 조립
    test_frame = (
        bytes([0xA5, 0xCD]) +  # STX
        bytes([64, 64]) +       # width, height
        test_payload +          # payload
        bytes([checksum & 0xFF, (checksum >> 8) & 0xFF]) +  # checksum (little endian)
        bytes([0xB5, 0x7A])     # ETX
    )
    
    print(f"테스트 프레임 크기: {len(test_frame)} bytes")
    print(f"체크섬: 0x{checksum:04X}")
    
    # 파서 테스트
    parser = FrameParser(log_callback=print)
    frames = parser.feed_bytes(test_frame)
    
    if frames:
        print(f"파싱 성공! 이미지 크기: {frames[0].shape}")
        print(f"통계: {parser.get_stats()}")
    else:
        print("파싱 실패")
