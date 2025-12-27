# radar/targets.py
import math
from PyQt6.QtGui import QPen, QColor
from config import COLOR_TARGET, RANGE_MODES


class TargetManager:
    """Hiển thị echo radar"""

    def __init__(self, max_km):
        self.range_mode = 0
        self.echoes = []

    def set_range_mode(self, mode):
        self.range_mode = mode

    def update_from_echo(self, echoes):
        self.echoes = echoes

    def draw(self, painter, cx, cy, radius):
        max_km = RANGE_MODES[self.range_mode]["max_km"]
        for e in self.echoes:
            ang = e["angle"]
            km = e["range_km"]
            power = e.get("power", 1.0)

            r = e["range_km"] / max_km * radius
            rad = math.radians(90 - ang)

            x = cx + r * math.cos(rad)
            y = cy - r * math.sin(rad)

            alpha = int(255 * min(power, 1.0))
            painter.setPen(QPen(QColor(*COLOR_TARGET, alpha), 3))
            painter.drawPoint(int(x), int(y))
