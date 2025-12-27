# radar/canvas.py
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor

from .grid import GridManager
from .targets import TargetManager
from .markers import MarkerManager
from .cursor import CursorManager
from .sweep import SweepController
from config import RADAR_MARGIN, RANGE_MODES, MARKER_MAX


class RadarCanvas(QWidget):
    def __init__(self):
        super().__init__()

        # ===== RANGE MODES =====
        self.range_modes = RANGE_MODES
        self.mode = 2
        self.step_km, self.max_km = self.range_modes[self.mode].values()

        # ===== SUBSYSTEMS =====
        self.grid_mgr = GridManager(self.step_km, self.max_km)
        self.target_mgr = TargetManager(self.max_km)
        self.marker_mgr = MarkerManager(max_markers=MARKER_MAX)
        self.cursor_mgr = CursorManager()
        self.sweep = SweepController()

        # ===== TIMER =====
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_radar)
        self.timer.start(30)

        self.setMouseTracking(True)

    # ================= UPDATE =================
    def update_radar(self):
        dt = 0.03
        self.sweep.update(dt)
        self.target_mgr.update(self.sweep.angle)
        self.update()

    # ================= MODE =================
    def set_mode(self, mode):
        self.mode = mode
        self.step_km, self.max_km = self.range_modes[mode].values()

        self.grid_mgr.set_range(self.step_km, self.max_km)
        self.target_mgr.reset(self.max_km)
        self.marker_mgr.clear()

        self.update()

    # ================= SPEED / DIR =================
    def set_speed(self, value):
        self.sweep.set_speed(value)

    def toggle_direction(self):
        self.sweep.toggle_direction()

    # ================= MOUSE =================
    def mouseMoveEvent(self, event):
        self.cursor_mgr.update_position(event.position())
        self.update()

    def mousePressEvent(self, event):
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - RADAR_MARGIN

        used = self.marker_mgr.handle_mouse(
            event,
            cx, cy,
            radius,
            self.max_km
        )

        if used:
            self.update()

    # ================= PAINT =================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - RADAR_MARGIN

        painter.fillRect(self.rect(), QColor(0, 0, 0))

        # ===== DRAW ORDER =====
        self.grid_mgr.draw(painter, cx, cy, radius)
        self.target_mgr.draw(painter, cx, cy, radius)
        self.marker_mgr.draw(painter, cx, cy, radius, self.max_km)
        self.sweep.draw(painter, cx, cy, radius)
        self.cursor_mgr.draw(
            painter,
            cx, cy,
            radius,
            self.max_km,
            h
        )
