# radar/targets.py
import math
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from config import COLOR_TARGET, RANGE_MODES, DEFAULT_RANGE_MODE


class TargetManager:
    def __init__(self):
        # init an toàn theo range mặc định
        self.range_mode = DEFAULT_RANGE_MODE
        self.max_km = RANGE_MODES[self.range_mode]["max_km"]
        self.targets = []

    def set_range_mode(self, mode):
        if mode not in RANGE_MODES:
            mode = DEFAULT_RANGE_MODE

        self.range_mode = mode
        self.max_km = RANGE_MODES[mode]["max_km"]

        # lọc bỏ target ngoài range (an toàn)
        self.targets = [
            t for t in self.targets
            if t["range_km"] <= self.max_km
        ]

    def update_from_echo(self, echoes):
        # echoes: list of dict {angle, range_km, power}
        self.targets = [
            e for e in echoes
            if e["range_km"] <= self.max_km
        ]

    def draw(self, painter, cx, cy, radius):
        if self.max_km <= 0:
            return

        for t in self.targets:
            r = t["range_km"] / self.max_km * radius
            # góc radar: 0° = Bắc
            import math
            rad = math.radians(90 - t["angle"])
            x = int(cx + r * math.cos(rad))
            y = int(cy - r * math.sin(rad))

            power = t.get("power", 1.0)
            alpha = max(50, min(255, int(255 * power)))

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 255, 0, alpha))
            painter.drawEllipse(x - 3, y - 3, 6, 6)

