# ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from radar.canvas import RadarCanvas
from config import GRID_LABEL_FONT_SIZE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Radar Display")
        self.showFullScreen()

        # ===== RADAR CANVAS =====
        self.radar = RadarCanvas()

        # ===== CONTROLS =====
        btn_exit = QPushButton("EXIT")
        btn_exit.clicked.connect(QApplication.quit)

        btn_marker = QPushButton("MARKER")
        btn_marker.setCheckable(True)
        btn_marker.clicked.connect(self.toggle_marker)

        # --- Direction ---
        btn_dir = QPushButton("Đảo chiều quét")
        btn_dir.clicked.connect(self.radar.toggle_direction)

        speed_label = QLabel("Tốc độ quét (deg/s)")
        self.speed_value = QLabel("0")

        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setRange(0, 16)
        speed_slider.setValue(0)
        speed_slider.valueChanged.connect(self.update_speed)

        # ===== RANGE MODE BUTTONS =====
        btn_mode1 = QPushButton("0–50 km")
        btn_mode2 = QPushButton("0–150 km")
        btn_mode3 = QPushButton("0–300 km")

        btn_mode1.clicked.connect(lambda: self.radar.set_mode(1))
        btn_mode2.clicked.connect(lambda: self.radar.set_mode(2))
        btn_mode3.clicked.connect(lambda: self.radar.set_mode(3))
        
        # --- Style ---
        for w in (btn_mode1, btn_mode2, btn_mode3, btn_dir):
            w.setFixedHeight(55)
            w.setStyleSheet("""
                QPushButton {
                    background-color: #202020;
                    color: #00ff00;
                    border: 1px solid #008800;
                }
            """)

        btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #aa0000;
                color: white;
                font-size: 20px;
            }
        """)

        speed_label.setStyleSheet(f"color:#00ff00; font-size:{GRID_LABEL_FONT_SIZE}px")
        self.speed_value.setStyleSheet("color:#00ff00; font-size:16px")

        # ===== LAYOUT RIGHT =====
        side = QVBoxLayout()
        side.addWidget(btn_marker)
        side.addWidget(btn_dir)
        side.addWidget(speed_label)
        side.addWidget(self.speed_value)
        side.addWidget(speed_slider)
        side.addWidget(btn_mode1)
        side.addWidget(btn_mode2)
        side.addWidget(btn_mode3)
        side.addStretch()
        side.addWidget(btn_exit)

        # ===== MAIN LAYOUT =====
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.radar, 1)
        layout.addLayout(side)

        self.setCentralWidget(container)

    # ================= CALLBACKS =================
    def toggle_marker(self):
        state = self.sender().isChecked()
        self.radar.marker_mgr.toggle(state)
        self.sender().setStyleSheet(
            "background-color: orange;" if state else ""
        )

    def update_speed(self, value):
        self.speed_value.setText(str(value))
        self.radar.set_speed(value)
