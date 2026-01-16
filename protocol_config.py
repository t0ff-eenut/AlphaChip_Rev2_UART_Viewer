"""
AlphaChip UART Image Viewer - Protocol Configuration

ESP32 SPI2UART ImageBridge 프로토콜 설정
"""

from enum import IntEnum

# =============================================================================
# UART 프로토콜 상수
# =============================================================================

# STX/ETX 패턴
UART_STX = bytes([0xA5, 0xCD])  # STX: A5 CD
UART_ETX = bytes([0xB5, 0x7A])  # ETX: B5 7A

# 프레임 크기
UART_STX_SIZE = 2
UART_HEIGHT_SIZE = 1
UART_WIDTH_SIZE = 1
UART_CHECKSUM_SIZE = 2
UART_ETX_SIZE = 2
UART_HEADER_SIZE = UART_STX_SIZE + UART_HEIGHT_SIZE + UART_WIDTH_SIZE  # 4 bytes

# 이미지 크기
IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64
IMAGE_PAYLOAD_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT  # 4096 bytes

# 전체 프레임 크기
UART_FRAME_SIZE = UART_HEADER_SIZE + IMAGE_PAYLOAD_SIZE + UART_CHECKSUM_SIZE + UART_ETX_SIZE  # 4104 bytes


# =============================================================================
# Baud Rate 설정
# =============================================================================

class BaudRate(IntEnum):
    """지원하는 Baud Rate 목록"""
    BAUD_115200 = 115200
    BAUD_230400 = 230400
    BAUD_460800 = 460800
    BAUD_500000 = 500000
    BAUD_576000 = 576000
    BAUD_921600 = 921600
    BAUD_1000000 = 1000000
    BAUD_1152000 = 1152000
    BAUD_1500000 = 1500000
    BAUD_2000000 = 2000000
    BAUD_2500000 = 2500000
    BAUD_3000000 = 3000000


# 기본 Baud Rate (ESP32 펌웨어와 일치)
DEFAULT_BAUD_RATE = BaudRate.BAUD_2000000


# =============================================================================
# 파서 상태
# =============================================================================

class ParserState(IntEnum):
    """프레임 파서 상태"""
    WAIT_STX_1 = 0      # 0xA5 대기
    WAIT_STX_2 = 1      # 0xCD 대기
    WAIT_HEIGHT = 2     # Height 대기
    WAIT_WIDTH = 3      # Width 대기
    WAIT_PAYLOAD = 4    # Payload 수신
    WAIT_CHECKSUM_L = 5 # Checksum Low 대기     16bit -> 8 + 8
    WAIT_CHECKSUM_H = 6 # Checksum High 대기
    WAIT_ETX_1 = 7      # 0xB5 대기
    WAIT_ETX_2 = 8      # 0x7A 대기
