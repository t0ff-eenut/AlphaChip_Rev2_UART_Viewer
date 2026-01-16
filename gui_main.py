"""
AlphaChip UART Image Viewer - Main GUI

iSENSOR_UART_DEBUGER 스타일의 PyQt6 기반 이미지 뷰어
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QGridLayout, QLabel, QTextEdit, QGroupBox,
    QSpacerItem, QSizePolicy, QSpinBox
)
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QFont
import pyqtgraph as pg

from protocol_config import BaudRate, DEFAULT_BAUD_RATE
from uart_worker import UartWorker, get_available_ports


class MainWindow(QMainWindow):
    """메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AlphaChip UART Image Viewer")
        self.setGeometry(658, 294, 900, 800)  # 사용자가 조정한 크기 (위치, 크기)
        
        # 스타일 설정
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ddd;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                color: #ccc;
            }
            QPushButton {
                background-color: #404040;
                color: #fff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #606060;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #666;
            }
            QComboBox {
                background-color: #404040;
                color: #fff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #0f0;
                border: 1px solid #555;
                font-family: Consolas, monospace;
            }
            QSpinBox {
                background-color: #404040;
                color: #fff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        
        # --- 메인 레이아웃 ---
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # --- 좌측 패널 (제어 + 설정) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setFixedWidth(300)
        
        # --- 우측 패널 (이미지 + 로그) ---
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        # =====================================================================
        # 좌측 패널 구성
        # =====================================================================
        
        # 1. Connection 그룹
        conn_group = QGroupBox("Connection")
        conn_layout = QGridLayout()
        conn_group.setLayout(conn_layout)
        
        self.port_combo = QComboBox()
        self.baud_combo = QComboBox()
        self.connect_button = QPushButton("Connect")
        
        # COM Port 재검색 버튼
        self.refresh_port_button = QPushButton("🔍")
        self.refresh_port_button.setFixedWidth(30)
        self.refresh_port_button.setToolTip("COM Port 재검색")
        
        # Port 레이아웃
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_port_button)
        
        conn_layout.addWidget(QLabel("Port:"), 0, 0)
        conn_layout.addLayout(port_layout, 0, 1)
        conn_layout.addWidget(QLabel("Baud Rate:"), 1, 0)
        conn_layout.addWidget(self.baud_combo, 1, 1)
        conn_layout.addWidget(self.connect_button, 2, 0, 1, 2)
        
        self.refresh_port_button.clicked.connect(self.refresh_ports)
        self.populate_ports()
        self.populate_bauds()
        
        # 2. Status 그룹
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        
        self.status_label = QLabel("⚪ 연결 대기 중")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
                background-color: #3a3a3a;
                color: #888888;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setStyleSheet("font-size: 12px;")
        status_layout.addWidget(self.fps_label)
        
        self.frame_count_label = QLabel("Frames: 0")
        self.frame_count_label.setStyleSheet("font-size: 12px;")
        status_layout.addWidget(self.frame_count_label)
        
        # 3. Settings 그룹 - Min/Max 밝기 조절
        settings_group = QGroupBox("Min/Max Settings")
        settings_layout = QGridLayout()
        settings_group.setLayout(settings_layout)
        
        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 255)
        self.min_spin.setValue(10)
        self.min_spin.setPrefix("Min: ")
        
        self.max_spin = QSpinBox()
        self.max_spin.setRange(0, 255)
        self.max_spin.setValue(35)
        self.max_spin.setPrefix("Max: ")
        
        settings_layout.addWidget(QLabel("Min Level:"), 0, 0)
        settings_layout.addWidget(self.min_spin, 0, 1)
        settings_layout.addWidget(QLabel("Max Level:"), 1, 0)
        settings_layout.addWidget(self.max_spin, 1, 1)
        
        # Spacer로 빈 공간 확보
        settings_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 2, 0, 1, 2)
        
        # 좌측 패널에 위젯 추가
        left_layout.addWidget(conn_group)
        left_layout.addWidget(status_group)
        left_layout.addWidget(settings_group)
        left_layout.addStretch(1)
        
        # =====================================================================
        # 우측 패널 구성
        # =====================================================================
        
        # 1. 이미지 표시 영역
        image_group = QGroupBox("64x64 Image View")
        image_layout = QVBoxLayout()
        image_group.setLayout(image_layout)
        
        # pyqtgraph ImageView 사용
        self.image_view = pg.ImageView()
        self.image_view.ui.histogram.hide()  # 히스토그램 숨기기
        self.image_view.ui.roiBtn.hide()     # ROI 버튼 숨기기
        self.image_view.ui.menuBtn.hide()    # 메뉴 버튼 숨기기
        
        # 초기 빈 이미지 설정
        empty_image = np.zeros((64, 64), dtype=np.uint8)
        self.image_view.setImage(empty_image, autoLevels=True, autoRange=True)
        
        image_layout.addWidget(self.image_view)
        
        # 2. 로그 영역
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        
        # 우측 패널에 위젯 추가
        right_layout.addWidget(image_group, stretch=3)
        right_layout.addWidget(log_group, stretch=1)
        
        # =====================================================================
        # Signal/Slot 연결
        # =====================================================================
        self.connect_button.clicked.connect(self.toggle_connection)
        
        self.uart_worker = None
        
        # --- 이미지 밝기 평활화(Smoothing) 변수 ---
        self.smooth_min = None
        self.smooth_max = None
        self.alpha = 0.1  # 변화 속도 (0.0~1.0): 낮을수록 더 천천히 변화함 (예: 0.05)
    
    def populate_ports(self):
        """사용 가능한 시리얼 포트 목록 채우기"""
        self.port_combo.clear()
        ports = get_available_ports()
        
        for device, description in ports:
            self.port_combo.addItem(description, device)
        
        if not ports:
            self.port_combo.addItem("포트 없음")
    
    def refresh_ports(self):
        """COM Port 재검색"""
        self.populate_ports()
        port_count = self.port_combo.count()
        
        if port_count > 0 and "포트 없음" not in self.port_combo.itemText(0):
            self.log_text.append(f"🔍 COM Port 재검색 완료: {port_count}개 포트 발견")
        else:
            self.log_text.append("🔍 COM Port 재검색 완료: 포트를 찾을 수 없습니다")
    
    def populate_bauds(self):
        """Baud Rate 목록 채우기"""
        self.baud_combo.clear()
        for rate in BaudRate:
            self.baud_combo.addItem(str(rate.value), rate.value)
        
        # 기본값 설정 (2000000)
        default_index = self.baud_combo.findData(DEFAULT_BAUD_RATE)
        if default_index >= 0:
            self.baud_combo.setCurrentIndex(default_index)
    
    def toggle_connection(self):
        """연결/해제 토글"""
        if self.uart_worker and self.uart_worker.isRunning():
            # 연결 해제
            self.uart_worker.stop()
            self.connect_button.setText("Connect")
            self.log_text.append("연결 해제됨")
        else:
            # 연결
            port = self.port_combo.currentData()
            baud = self.baud_combo.currentData()
            
            if not port or "포트 없음" in str(port):
                self.log_text.append("오류: 시리얼 포트를 선택하세요")
                return
            
            self.uart_worker = UartWorker(port, baud)                       # -> uart_worker.py
            self.uart_worker.log_message.connect(self.log_text.append)
            self.uart_worker.new_image.connect(self.update_image)
            self.uart_worker.connection_status.connect(self.on_connection_status_changed)
            self.uart_worker.fps_update.connect(self.update_fps)
            self.uart_worker.frame_count_update.connect(self.update_frame_count)
            self.uart_worker.start()
            
            self.connect_button.setText("연결 중...")
            self.connect_button.setEnabled(False)
    
    @pyqtSlot(bool)
    def on_connection_status_changed(self, is_connected: bool):
        """연결 상태 변경 시 UI 업데이트"""
        self.connect_button.setEnabled(True)
        
        if is_connected:
            self.connect_button.setText("Disconnect")
            self.status_label.setText("🟢 연결됨")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 5px;
                    background-color: #1a4d1a;
                    color: #66ff66;
                }
            """)
        else:
            self.connect_button.setText("Connect")
            self.status_label.setText("⚪ 연결 대기 중")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 5px;
                    background-color: #3a3a3a;
                    color: #888888;
                }
            """)
            self.fps_label.setText("FPS: --")
            
            # 스레드 정리
            if self.uart_worker:
                self.uart_worker.deleteLater()
                self.uart_worker = None
    
    @pyqtSlot(np.ndarray)
    def update_image(self, image: np.ndarray):
        """이미지 업데이트"""
        # GUI에서 설정된 Min, Max 값 가져오기
        min_val = self.min_spin.value()
        max_val = self.max_spin.value()

        # 정규화 적용
        if max_val > min_val:
            normalized = ((image.astype(np.float32) - min_val) / (max_val - min_val) * 255)
            normalized = np.clip(normalized, 0, 255).astype(np.uint8)
        else:
            normalized = image
        
        # pyqtgraph에서 이미지 표시 (transpose하여 올바른 방향으로)
        self.image_view.setImage(normalized.T, autoLevels=False, levels=(0, 255), autoRange=False)
    
    @pyqtSlot(float)
    def update_fps(self, fps: float):
        """FPS 표시 업데이트"""
        self.fps_label.setText(f"FPS: {fps:.1f}")
    
    @pyqtSlot(int)
    def update_frame_count(self, count: int):
        """프레임 카운터 업데이트"""
        self.frame_count_label.setText(f"Frames: {count}")
    
    def closeEvent(self, event):
        """윈도우 닫힐 때 정리"""
        
        # 현재 창 크기 출력
        size = self.size()
        pos = self.pos()
        print(f"\n[GUI 닫힘] 창 크기: {size.width()}x{size.height()}, 위치: ({pos.x()}, {pos.y()})")
        
        if self.uart_worker and self.uart_worker.isRunning():
            self.uart_worker.stop()
        event.accept()


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 다크 테마 기본 설정
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
