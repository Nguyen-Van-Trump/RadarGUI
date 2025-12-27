from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QDoubleSpinBox,
    QPushButton, QMessageBox
)
from data.simulator import SimTarget


class SimTargetDialog(QDialog):
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        self.setWindowTitle("Tạo mục tiêu giả (tối đa 5)")

        layout = QFormLayout(self)

        self.angle = QDoubleSpinBox()
        self.angle.setRange(0, 360)
        self.angle.setSuffix(" °")

        self.range_km = QDoubleSpinBox()
        self.range_km.setRange(0, 300)
        self.range_km.setSuffix(" km")

        self.speed = QDoubleSpinBox()
        self.speed.setRange(0, 5)
        self.speed.setSuffix(" km/s")
        self.speed.setSingleStep(0.1)

        self.heading = QDoubleSpinBox()
        self.heading.setRange(0, 360)
        self.heading.setSuffix(" °")

        layout.addRow("Góc ban đầu", self.angle)
        layout.addRow("Cự ly ban đầu", self.range_km)
        layout.addRow("Tốc độ mục tiêu", self.speed)
        layout.addRow("Hướng bay", self.heading)

        btn = QPushButton("Thêm mục tiêu")
        btn.clicked.connect(self.add_target)
        layout.addWidget(btn)

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
                "Chỉ được tạo tối đa 5 mục tiêu giả"
            )
