import math
from qt_compat import QColor, QPen

from config import (
    COLOR_GRID_MAIN, COLOR_GRID_MINOR, COLOR_GRID_STEP,
    GRID_MAIN_PEN, GRID_MINOR_PEN, GRID_STEP_PEN,
    RANGE_MODES, DEFAULT_RANGE_MODE
)


class GridManager:
    def __init__(self, step_km=None, max_km=None):
        # khởi tạo an toàn theo DEFAULT_RANGE_MODE
        self.range_mode = DEFAULT_RANGE_MODE
        cfg = RANGE_MODES[self.range_mode]

        self.step_km = step_km if step_km is not None else cfg["step_km"]
        self.max_km = max_km if max_km is not None else cfg["max_km"]

    # ===== API MỚI – DÙNG CHO CANVAS =====
    def set_range_mode(self, mode):
        if mode not in RANGE_MODES:
            mode = DEFAULT_RANGE_MODE

        cfg = RANGE_MODES[mode]
        self.range_mode = mode
        self.step_km = cfg["step_km"]
        self.max_km = cfg["max_km"]

    # ===== API CŨ – GIỮ LẠI =====
    def set_range(self, step_km, max_km):
        self.step_km = step_km
        self.max_km = max_km

    def draw(self, painter, cx, cy, radius):
        if self.step_km <= 0 or self.max_km <= 0:
            return

        num_rings = int(self.max_km // self.step_km)
        if num_rings <= 0:
            return

        # ===== VÒNG CỰ LY =====
        for i in range(1, num_rings + 1):
            ri = int(radius * i / num_rings)

            painter.setPen(QPen(QColor(0, 255, 0), 1))
            painter.drawEllipse(cx - ri, cy - ri, ri * 2, ri * 2)

            painter.setPen(QColor(0, 220, 0))
            painter.drawText(cx + 6, cy - ri + 14, f"{i * self.step_km}")

        # ===== VẠCH GÓC =====
        for deg in range(0, 360, 10):
            rad = math.radians(90 - deg)
            x = int(cx + radius * math.cos(rad))
            y = int(cy - radius * math.sin(rad))

            if deg in (0, 90, 180, 270):
                pen = QPen(QColor(*COLOR_GRID_MAIN), GRID_MAIN_PEN)
            elif deg % 30 == 0:
                pen = QPen(QColor(*COLOR_GRID_STEP), GRID_STEP_PEN)
            else:
                pen = QPen(QColor(*COLOR_GRID_MINOR), GRID_MINOR_PEN)

            painter.setPen(pen)
            painter.drawLine(cx, cy, x, y)

            if deg % 30 == 0:
                tx = int(cx + (radius + 22) * math.cos(rad))
                ty = int(cy - (radius + 22) * math.sin(rad))
                painter.setPen(QColor(0, 220, 0))
                painter.drawText(tx - 12, ty + 6, f"{deg}°")
