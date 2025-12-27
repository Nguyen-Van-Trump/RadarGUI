# radar/markers.py
import math
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen

from config import MARKER_SIZE, MARKER_MAX, COLOR_MARKER


class MarkerManager:
    """
    Quản lý marker (điểm dấu radar)
    - Toggle bật / tắt
    - Chuột trái: thêm marker
    - Chuột phải: xóa marker gần nhất
    """

    def __init__(self, max_markers=MARKER_MAX):
        self.enabled = False
        self.max_markers = max_markers
        self.markers = []   # [(angle, km)]

    # ================= CONTROL =================
    def toggle(self, state: bool):
        self.enabled = state
        if not state:
            self.markers.clear()

    def clear(self):
        self.markers.clear()

    # ================= INPUT =================
    def handle_mouse(self, event, cx, cy, radius, max_km):
        """
        Xử lý chuột cho marker
        Trả về True nếu có thay đổi để canvas update
        """
        if not self.enabled:
            return False

        dx = event.position().x() - cx
        dy = cy - event.position().y()
        dist_px = math.hypot(dx, dy)

        if dist_px > radius:
            return False

        angle = (90 - math.degrees(math.atan2(dy, dx))) % 360
        km = dist_px / radius * max_km

        # Chuột trái → thêm marker
        if event.button() == Qt.MouseButton.LeftButton:
            self.markers.append((angle, km))
            if len(self.markers) > self.max_markers:
                self.markers.pop(0)
            return True

        # RIGHT CLICK → REMOVE LATEST
        elif event.button() == Qt.MouseButton.RightButton and self.markers:
            self.markers.pop(-1)
            return True

        return False

    # ================= DRAW =================
    def draw(self, painter, cx, cy, radius, max_km):
        if not self.enabled:
            return

        r,g,b = COLOR_MARKER
        painter.setPen(QPen(QColor(r, g, b), 2))

        for ang, km in self.markers:
            r = km / max_km * radius
            rad = math.radians(90 - ang)

            x = cx + r * math.cos(rad)
            y = cy - r * math.sin(rad)

            # dấu thập
            painter.drawLine(int(x - MARKER_SIZE), int(y), int(x + MARKER_SIZE), int(y))
            painter.drawLine(int(x), int(y - MARKER_SIZE), int(x), int(y + MARKER_SIZE))

            # # nhãn
            # painter.drawText(
            #     int(x + 5),
            #     int(y - 5),
            #     f"{ang:.1f}°  {km:.1f}"
            # )
