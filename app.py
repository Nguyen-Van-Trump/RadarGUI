<<<<<<< HEAD
# app.py
import sys
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
=======
import sys
import math
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QPushButton, QHBoxLayout, QVBoxLayout,
    QLabel, QSlider
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen


# ================= TARGET =================
class Target:
    def __init__(self, angle, distance, strength=1.0):
        self.angle = angle
        self.distance = distance
        self.strength = strength
        self.trail = []


# ================= RADAR CANVAS =================
class RadarCanvas(QWidget):
    def __init__(self):
        super().__init__()

        self.angle = 0.0
        self.speed = 4.0          # deg/s
        self.direction = 1

        self.range_modes = {
            1: (10, 50),
            2: (30, 150),
            3: (60, 300)
        }
        self.mode = 1
        self.step_km, self.max_km = self.range_modes[self.mode]

        self.setMouseTracking(True)
        self.mouse_pos = None

        self.targets = self.generate_targets(6)
        
                # ===== MARKERS =====
        self.marker_enabled = False
        self.markers = []   # [(angle, km)]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_radar)
        self.timer.start(30)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_radar)
        self.timer.start(30)

    def generate_targets(self, n):
        return [
            Target(
                random.uniform(0, 360),
                random.uniform(0.15 * self.max_km, 0.85 * self.max_km),
                random.uniform(0.7, 1.3)
            )
            for _ in range(n)
        ]
# ---------- MARKER ----------
    def toggle_marker(self, state: bool):
        self.marker_enabled = state
        if not state:
            self.markers.clear()
        self.update()

    def mousePressEvent(self, event):
        if not self.marker_enabled:
            return

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - 80

        dx = event.position().x() - cx
        dy = cy - event.position().y()
        dist_px = math.hypot(dx, dy)
        if dist_px > radius:
            return

        angle = (90 - math.degrees(math.atan2(dy, dx))) % 360
        km = dist_px / radius * self.max_km

        # LEFT CLICK → ADD
        if event.button() == Qt.MouseButton.LeftButton:
            self.markers.append((angle, km))
            if len(self.markers) > 3:
                self.markers.pop(0)

        # RIGHT CLICK → REMOVE LATEST
        elif event.button() == Qt.MouseButton.RightButton and self.markers:
            self.markers.pop(-1)

    def set_mode(self, mode):
        self.mode = mode
        self.step_km, self.max_km = self.range_modes[mode]
        self.targets = self.generate_targets(6)
        self.markers.clear()
        self.update()

    def set_speed(self, value):
        self.speed = float(value)

    def toggle_direction(self):
        self.direction *= -1

    def update_radar(self):
        dt = 0.03
        self.angle = (self.angle + self.direction * self.speed * dt) % 360

        for t in self.targets:
            diff = abs((self.angle - t.angle + 180) % 360 - 180)
            if diff < 2.0:
                t.trail.insert(0, [t.angle, t.distance, 255])
            for tr in t.trail:
                tr[2] -= 10
            t.trail = [tr for tr in t.trail if tr[2] > 0]

        self.update()

    def mouseMoveEvent(self, event):
        self.mouse_pos = event.position()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - 80

        painter.fillRect(self.rect(), QColor(0, 0, 0))

        self.draw_polar_grid(painter, cx, cy, radius)
        self.draw_targets(painter, cx, cy, radius)
        self.draw_markers(painter, cx, cy, radius)
        self.draw_sweep_line(painter, cx, cy, radius)
        self.draw_cursor_info(painter, cx, cy, radius)

    def draw_markers(self, painter, cx, cy, radius):
        painter.setPen(QPen(QColor(255, 165, 0), 2))
        for ang, km in self.markers:
            r = km / self.max_km * radius
            rad = math.radians(90 - ang)
            x = cx + r * math.cos(rad)
            y = cy - r * math.sin(rad)

            painter.drawLine(int(x - 8), int(y), int(x + 8), int(y))
            painter.drawLine(int(x), int(y - 8), int(x), int(y + 8))
            painter.drawText(int(x + 10), int(y - 10),
                             f"{ang:.1f}°  {km:.1f}")

    # ===== GRID =====
    def draw_polar_grid(self, painter, cx, cy, radius):
        num_rings = self.max_km // self.step_km
        painter.setPen(QPen(QColor(0, 120, 0), 1))

        for i in range(1, num_rings + 1):
            ri = int(radius * i / num_rings)
            painter.drawEllipse(cx - ri, cy - ri, ri * 2, ri * 2)
            painter.drawText(cx + 5, cy - ri + 15, f"{i * self.step_km}")

        for deg in range(0, 360, 10):
            rad = math.radians(90 - deg)
            x = int(cx + radius * math.cos(rad))
            y = int(cy - radius * math.sin(rad))

            if deg in (0, 90, 180, 270):
                pen = QPen(QColor(0, 180, 0), 2.5)
            elif deg % 30 == 0:
                pen = QPen(QColor(0, 140, 0), 2)
            else:
                pen = QPen(QColor(0, 90, 0), 1)

            painter.setPen(pen)
            painter.drawLine(cx, cy, x, y)

            if deg % 30 == 0:
                tx = int(cx + (radius + 22) * math.cos(rad))
                ty = int(cy - (radius + 22) * math.sin(rad))
                painter.setPen(QColor(0, 220, 0))
                painter.drawText(tx - 12, ty + 6, f"{deg}°")

    # ===== TARGETS =====
    def draw_targets(self, painter, cx, cy, radius):
        for t in self.targets:
            for ang, dist, alpha in t.trail:
                r = dist / self.max_km * radius
                rad = math.radians(90 - ang)
                x = cx + r * math.cos(rad)
                y = cy - r * math.sin(rad)

                size = int(6 * t.strength)
                painter.setBrush(QColor(0, 255, 0, int(alpha)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(int(x - size / 2), int(y - size / 2), size, size)

    # ===== SWEEP =====
    def draw_sweep_line(self, painter, cx, cy, radius):
        rad = math.radians(90 - self.angle)
        x = int(cx + radius * math.cos(rad))
        y = int(cy - radius * math.sin(rad))
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.drawLine(cx, cy, x, y)

    # ===== CURSOR =====
    def draw_cursor_info(self, painter, cx, cy, radius):
        if not self.mouse_pos:
            return

        dx = self.mouse_pos.x() - cx
        dy = cy - self.mouse_pos.y()
        dist_px = math.hypot(dx, dy)
        if dist_px > radius:
            return

        angle = (90 - math.degrees(math.atan2(dy, dx))) % 360
        km = dist_px / radius * self.max_km

        painter.setPen(QColor(0, 255, 0))
        painter.drawText(
            20, self.height() - 20,
            f"Góc: {angle:6.1f}°    Cự ly: {km:6.1f} km"
        )


# ================= MAIN WINDOW =================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radar Display")
        self.showFullScreen()

        self.radar = RadarCanvas()

        # --- Buttons ---
        btn1 = QPushButton("Mode 1\n0–50 km")
        btn2 = QPushButton("Mode 2\n0–150 km")
        btn3 = QPushButton("Mode 3\n0–300 km")
        btn_marker = QPushButton("MARKER") # MARKER BUTTON
        btn_marker.setCheckable(True)
        # CONNECT
        btn1.clicked.connect(lambda: self.radar.set_mode(1))
        btn2.clicked.connect(lambda: self.radar.set_mode(2))
        btn3.clicked.connect(lambda: self.radar.set_mode(3))
        # MARKER CONNECT
        def toggle():
            state = btn_marker.isChecked()
            self.radar.toggle_marker(state)
            btn_marker.setStyleSheet(
                "background-color: orange;" if state else ""
            )

        btn_marker.clicked.connect(toggle)

        # --- Speed slider + display ---
        speed_title = QLabel("TỐC ĐỘ QUÉT")
        speed_value = QLabel(f"{self.radar.speed:.1f} °/s")

        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setRange(0, 16)
        speed_slider.setValue(int(self.radar.speed))

        def update_speed(v):
            self.radar.set_speed(v)
            speed_value.setText(f"{v:.1f} °/s")

        speed_slider.valueChanged.connect(update_speed)

        # --- Direction ---
        btn_dir = QPushButton("Đảo chiều quét")
        btn_dir.clicked.connect(self.radar.toggle_direction)

        # --- Exit ---
        btn_exit = QPushButton("EXIT")
        btn_exit.clicked.connect(QApplication.quit)

        # --- Style ---
        for w in (btn1, btn2, btn3, btn_dir):
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
                font-size: 16px;
            }
        """)

        speed_title.setStyleSheet("color:#00ff00; font-weight:bold")
        speed_value.setStyleSheet("color:#00ff00; font-size:16px")

        # --- Layout ---
        side = QVBoxLayout()
        side.addWidget(btn_marker)
        side.addWidget(btn1)
        side.addWidget(btn2)
        side.addWidget(btn3)
        side.addSpacing(20)
        side.addWidget(speed_title)
        side.addWidget(speed_value)
        side.addWidget(speed_slider)
        side.addWidget(btn_dir)
        side.addStretch()
        side.addWidget(btn_exit)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.radar, 1)
        layout.addLayout(side)
        self.setCentralWidget(container)


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
>>>>>>> edc500f (initial commit)
