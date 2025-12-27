# radar/targets.py
import random
import math
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class Target:
    def __init__(self, angle, distance, strength=1.0):
        self.angle = angle
        self.distance = distance
        self.strength = strength
        self.trail = []   # [[angle, distance, alpha], ...]


class TargetManager:
    def __init__(self, max_km, count=6):
        self.max_km = max_km
        self.targets = self._generate_targets(count)

    def _generate_targets(self, n):
        return [
            Target(
                random.uniform(0, 360),
                random.uniform(0.15 * self.max_km, 0.85 * self.max_km),
                random.uniform(0.7, 1.3)
            )
            for _ in range(n)
        ]

    def reset(self, max_km, count=6):
        """Gọi khi đổi mode radar"""
        self.max_km = max_km
        self.targets = self._generate_targets(count)

    def update(self, sweep_angle):
        """Cập nhật trail khi tia quét đi qua"""
        for t in self.targets:
            diff = abs((sweep_angle - t.angle + 180) % 360 - 180)
            if diff < 2.0:
                t.trail.insert(0, [t.angle, t.distance, 255])

            for tr in t.trail:
                tr[2] -= 10

            t.trail = [tr for tr in t.trail if tr[2] > 0]

    def draw(self, painter, cx, cy, radius):
        """Vẽ target + đuôi mờ"""
        for t in self.targets:
            for ang, dist, alpha in t.trail:
                r = dist / self.max_km * radius
                rad = math.radians(90 - ang)

                x = cx + r * math.cos(rad)
                y = cy - r * math.sin(rad)

                size = int(6 * t.strength)
                painter.setBrush(QColor(0, 255, 0, int(alpha)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(x - size / 2),
                    int(y - size / 2),
                    size,
                    size
                )
