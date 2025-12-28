from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QDoubleSpinBox,
    QPushButton, QMessageBox, QHBoxLayout
)
from data.simulator import SimTarget


class SimTargetDialog(QDialog):
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        self.setWindowTitle("Tạo mục tiêu giả (SIM)")

        layout = QFormLayout(self)

        self.angle = QDoubleSpinBox()
        self.angle.setRange(0, 360)
        self.angle.setSuffix(" °")

        self.range_km = QDoubleSpinBox()
        self.range_km.setRange(0, 300)
        self.range_km.setSuffix(" km")

        self.speed = QDoubleSpinBox()
        self.speed.setRange(0, 5)
        self.speed.setSingleStep(0.1)
        self.speed.setSuffix(" km/s")

        self.heading = QDoubleSpinBox()
        self.heading.setRange(0, 360)
        self.heading.setSuffix(" °")

        layout.addRow("Góc ban đầu", self.angle)
        layout.addRow("Cự ly ban đầu", self.range_km)
        layout.addRow("Tốc độ mục tiêu", self.speed)
        layout.addRow("Hướng bay", self.heading)

        # ===== BUTTONS =====
        btn_add = QPushButton("Thêm mục tiêu")
        btn_add.clicked.connect(self.add_target)

        btn_start = QPushButton("START SIM")
        btn_start.clicked.connect(self.start_sim)

        btn_stop = QPushButton("STOP")
        btn_stop.clicked.connect(self.stop_sim)

        h = QHBoxLayout()
        h.addWidget(btn_add)
        h.addWidget(btn_start)
        h.addWidget(btn_stop)

        layout.addRow(h)

    def add_target(self):
        t = SimTarget(
            angle_deg=self.angle.value(),
            range_km=self.range_km.value(),
            speed_km_s=self.speed.value(),
            heading_deg=self.heading.value(),
        )

        if not self.simulator.add_target(t):
            QMessageBox.warning(
                self,
                "Giới hạn",
                "Chỉ được tạo tối đa số mục tiêu cho phép"
            )

    def start_sim(self):
        self.simulator.running = True

    def stop_sim(self):
        self.simulator.running = False
