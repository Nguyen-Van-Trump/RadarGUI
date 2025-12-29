from qt_compat import *

from config import RADAR_MARGIN, COLOR_RADAR_BG, DEFAULT_RANGE_MODE
from radar.grid import GridManager
from radar.sweep import SweepController
from radar.targets import TargetManager
from radar.markers import MarkerManager


class RadarCanvas(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        # ===== MANAGERS =====
        self.grid_mgr = GridManager()
        self.sweep = SweepController()
        self.target_mgr = TargetManager()
        self.marker_mgr = MarkerManager()

        # set range mặc định ngay khi khởi tạo
        self.grid_mgr.set_range_mode(DEFAULT_RANGE_MODE)
        self.target_mgr.set_range_mode(DEFAULT_RANGE_MODE)

        # ===== UPDATE TIMER =====
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_view)
        self.timer.start(30)

        # cho phép nhận sự kiện chuột
        self.setMouseTracking(True)

    # ================= UPDATE =================
    def update_view(self):
        self.model.poll_buffer() # Đọc frame từ buffer
        
        snap = self.model.get_snapshot()

        # ===== RANGE MODE =====
        rm = snap.get("range_mode", DEFAULT_RANGE_MODE)
        self.grid_mgr.set_range_mode(rm)
        self.target_mgr.set_range_mode(rm)

        # ===== SWEEP =====
        self.sweep.set_angle(snap["angle"])

        # ===== TARGETS =====
        self.target_mgr.update_from_echo(snap["echoes"])

        self.update()

    # ================= INPUT =================
    def mousePressEvent(self, event):
        if not self.marker_mgr.enabled:
            return

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - RADAR_MARGIN

        changed = self.marker_mgr.handle_mouse(
            event,
            cx,
            cy,
            radius,
            self.target_mgr.max_km
        )

        if changed:
            self.update()

    # ================= DRAW =================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(RenderAntialias)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - RADAR_MARGIN

        painter.fillRect(self.rect(), QColor(*COLOR_RADAR_BG))

        self.grid_mgr.draw(painter, cx, cy, radius)
        self.target_mgr.draw(painter, cx, cy, radius)

        # ===== MARKERS =====
        self.marker_mgr.draw(
            painter,
            cx,
            cy,
            radius,
            self.target_mgr.max_km
        )

        self.sweep.draw(painter, cx, cy, radius)
