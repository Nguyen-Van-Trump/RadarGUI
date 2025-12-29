# radar/cursor.py
import math
from qt_compat import QColor, QPen

class CursorManager:
    def __init__(self):
        self.pos = None   # QPointF hoặc None

    def update_position(self, pos):
        self.pos = pos

    def draw(self, painter, cx, cy, radius, max_km, screen_h):
        if not self.pos:
            return

        dx = self.pos.x() - cx
        dy = cy - self.pos.y()
        dist_px = math.hypot(dx, dy)
        if dist_px > radius:
            return

        angle = (90 - math.degrees(math.atan2(dy, dx))) % 360
        km = dist_px / radius * max_km

        painter.setPen(QPen(QColor(0, 255, 0)))
        painter.drawText(
            20,
            screen_h - 20,
            f"Góc: {angle:6.1f}°    Cự ly: {km:6.1f} km"
        )
