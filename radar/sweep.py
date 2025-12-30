# radar/sweep.py
import math
from qt_compat import QPen, QColor
from config import COLOR_SWEEP


class SweepController:
    """Viewer tia quét radar"""

    def __init__(self):
        self.angle = 0.0

    def set_angle(self, angle):
        self.angle = angle % 360

    def draw(self, painter, cx, cy, radius):
        rad = math.radians(90 - self.angle)
        x = int(cx + radius * math.cos(rad))
        y = int(cy - radius * math.sin(rad))

        painter.setPen(QPen(QColor(*COLOR_SWEEP), 2))
        painter.drawLine(cx, cy, x, y)
