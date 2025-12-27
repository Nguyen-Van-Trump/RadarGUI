# radar/canvas.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor

from config import RADAR_MARGIN, COLOR_BG
from radar.grid import GridManager
from radar.sweep import SweepController
from radar.targets import TargetManager


class RadarCanvas(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.grid_mgr = GridManager(step_km=10, max_km=50)
        self.sweep = SweepController()
        self.target_mgr = TargetManager(max_km=50)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_view)
        self.timer.start(30)

    def update_view(self):
        snap = self.model.get_snapshot()
        
        self.grid.set_range_mode(snap["range_mode"])
        self.targets.set_range_mode(snap["range_mode"])

        self.sweep.set_angle(snap["angle"])
        self.target_mgr.update_from_echo(snap["echoes"])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - RADAR_MARGIN

        painter.fillRect(self.rect(), QColor(*COLOR_BG))

        self.grid_mgr.draw(painter, cx, cy, radius)
        self.target_mgr.draw(painter, cx, cy, radius)
        self.sweep.draw(painter, cx, cy, radius)
