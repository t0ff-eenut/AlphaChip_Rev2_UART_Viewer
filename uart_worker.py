"""
AlphaChip UART Image Viewer - UART Worker Thread

PyQt6 QThread 기반 UART 수신 워커
"""

import serial
import serial.tools.list_ports
from PyQt6.QtCore import QThread, pyqtSignal
import numpy as np

from protocol_config import DEFAULT_BAUD_RATE
from frame_parser import FrameParser


class UartWorker(QThread):
    """
    UART 통신을 처리하는 워커 스레드
    
    100ms 간격으로 이미지 수신을 목표로 최적화
    """
    
    # Signals
    new_image = pyqtSignal(np.ndarray)      # 새 이미지 프레임
    log_message = pyqtSignal(str)            # 로그 메시지
    connection_status = pyqtSignal(bool)     # 연결 상태 (True: 연결됨)
    fps_update = pyqtSignal(float)           # FPS 업데이트
    frame_count_update = pyqtSignal(int)     # 프레임 카운터 업데이트
    
    def __init__(self, port: str, baud_rate: int = DEFAULT_BAUD_RATE):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.running = False
        self.serial_port = None
        # 파서에 로그 콜백 연결
        self.parser = FrameParser(log_callback=self._parser_log)
        
        # FPS 계산용
        self._frame_count = 0
        self._total_frames = 0
        self._last_fps_time = 0
    
    def _parser_log(self, message: str):
        """파서에서 오는 로그를 GUI에 전달"""
        self.log_message.emit(message)      # emit -> GUI 업데이트
    
    def run(self):
        """스레드 메인 루프"""
        import time
        
        self.running = True
        self._frame_count = 0
        self._total_frames = 0
        self._last_fps_time = time.time()
        
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.05  # 50ms timeout (100ms 프레임 간격의 절반)
            )
            self.connection_status.emit(True)
            self.log_message.emit(f"✓ {self.port} 연결됨 @ {self.baud_rate} bps")
            
        except serial.SerialException as e:
            self.log_message.emit(f"✗ 연결 실패: {e}")
            self.connection_status.emit(False)
            self.running = False
            return
        
        # 메인 수신 루프
        _rx_count = 0
        _total_bytes = 0
        while self.running:
            try:
                # 버퍼에 데이터가 있으면 읽기
                if self.serial_port.in_waiting > 0:
                    # 가능한 많이 읽어서 파서에 전달
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    
                    # ★ 터미널에 raw 데이터 출력 (디버그용 - 주석처리)
                    # _rx_count += 1
                    # _total_bytes += len(data)
                    # hex_str = " ".join(f"{b:02X}" for b in data[:32])  # 처음 32바이트만
                    # if len(data) > 32:
                    #     hex_str += " ..."
                    # print(f"[RX {_rx_count:04d}] ({len(data):4d} bytes, total: {_total_bytes:7d}) | {hex_str}")
                    
                    # 바이트 단위로 파싱
                    for byte in data:
                        frame = self.parser.feed_byte(byte)
                        if frame is not None:
                            # 새 프레임 수신!
                            self._frame_count += 1
                            self._total_frames += 1
                            self.new_image.emit(frame)
                            self.frame_count_update.emit(self._total_frames)
                
                # FPS 계산 (1초마다)
                current_time = time.time()
                if current_time - self._last_fps_time >= 1.0:
                    fps = self._frame_count / (current_time - self._last_fps_time)
                    self.fps_update.emit(fps)
                    self._frame_count = 0
                    self._last_fps_time = current_time
                    
            except serial.SerialException as e:
                self.log_message.emit(f"✗ 시리얼 오류: {e}")
                self.running = False
        
        # 정리
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.log_message.emit("포트 닫힘")
        
        self.connection_status.emit(False)
    
    def stop(self):
        """스레드 종료 요청"""
        self.running = False
        self.log_message.emit("UART 스레드 종료 요청...")
        self.wait(2000)  # 최대 2초 대기


def get_available_ports() -> list[tuple[str, str]]:
    """
    사용 가능한 시리얼 포트 목록 반환
    
    Returns:
        [(포트명, 설명), ...] 리스트
    """
    ports = serial.tools.list_ports.comports()
    result = []
    
    for port in ports:
        description = port.description or port.device
        result.append((port.device, f"{port.device}: {description}"))
    
    return result
