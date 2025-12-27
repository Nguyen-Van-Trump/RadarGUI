# radar/sweep.py
import math
from PyQt6.QtGui import QPen, QColor


class SweepController:
    """
    Quản lý tia quét radar
    - Góc (degree)
    - Tốc độ (deg/s)
    - Hướng quay
    """

    def __init__(self, speed=0.0):
        self.angle = 0.0          # độ, 0 = Bắc
        self.speed = speed       # deg/s
        self.direction = 1       # 1: CW, -1: CCW

    # ================= CONFIG =================
    def set_speed(self, value):
        self.speed = float(value)

    def toggle_direction(self):
        self.direction *= -1

    def reset(self):
        self.angle = 0.0

    # ================= UPDATE =================
    def update(self, dt):
        """
        dt: thời gian giữa 2 frame (giây)
        """
        self.angle = (self.angle + self.direction * self.speed * dt) % 360

    # ================= DRAW =================
    def draw(self, painter, cx, cy, radius):
        """
        Vẽ tia quét
        """
        rad = math.radians(90 - self.angle)
        x = int(cx + radius * math.cos(rad))
        y = int(cy - radius * math.sin(rad))

        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.drawLine(cx, cy, x, y)
