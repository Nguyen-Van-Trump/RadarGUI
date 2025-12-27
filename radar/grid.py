# radar/grid.py
import math
from PyQt6.QtGui import QColor, QPen

from config import COLOR_GRID_MAIN, COLOR_GRID_MINOR, COLOR_GRID_STEP, GRID_MAIN_PEN, GRID_MINOR_PEN, GRID_STEP_PEN


class GridManager:
    def __init__(self, step_km, max_km):
        self.step_km = step_km
        self.max_km = max_km

    def set_range(self, step_km, max_km):
        """Gọi khi đổi chế độ radar"""
        self.step_km = step_km
        self.max_km = max_km

    def draw(self, painter, cx, cy, radius):
        num_rings = self.max_km // self.step_km
        painter.setPen(QPen(QColor(0, 255, 0), 1))

        # ===== VÒNG CỰ LY =====
        for i in range(1, num_rings + 1):
            ri = int(radius * i / num_rings)
            painter.drawEllipse(cx - ri, cy - ri, ri * 2, ri * 2)
            painter.drawText(
                cx + 5,
                cy - ri + 15,
                f"{i * self.step_km}"
            )

        # ===== VẠCH GÓC =====
        for deg in range(0, 360, 10):
            rad = math.radians(90 - deg)
            x = int(cx + radius * math.cos(rad))
            y = int(cy - radius * math.sin(rad))

            if deg in (0, 90, 180, 270):
                r,g,b = COLOR_GRID_MAIN
                pen = QPen(QColor(r,g,b), GRID_MAIN_PEN)
            elif deg % 30 == 0:
                r,g,b = COLOR_GRID_STEP
                pen = QPen(QColor(0, 90, 0), GRID_STEP_PEN)
            else:
                r,g,b = COLOR_GRID_MINOR
                pen = QPen(QColor(0, 50, 0), GRID_MINOR_PEN)

            painter.setPen(pen)
            painter.drawLine(cx, cy, x, y)

            # nhãn góc
            if deg % 30 == 0:
                tx = int(cx + (radius + 22) * math.cos(rad))
                ty = int(cy - (radius + 22) * math.sin(rad))
                painter.setPen(QColor(0, 220, 0))
                painter.drawText(tx - 12, ty + 6, f"{deg}°")
