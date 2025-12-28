from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QDoubleSpinBox, QPushButton, QListWidget,
    QListWidgetItem, QHBoxLayout, QCheckBox,
    QLabel, QSlider
)
from PyQt6.QtCore import Qt
from data.simulator import SimTarget


class SimTargetDialog(QDialog):
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        self.setWindowTitle("Radar Simulator Control")

        main = QVBoxLayout(self)

        # ================= TARGET INPUT =================
        form = QFormLayout()

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

        form.addRow("Góc mục tiêu", self.angle)
        form.addRow("Cự ly mục tiêu", self.range_km)
        form.addRow("Tốc độ mục tiêu", self.speed)
        form.addRow("Hướng bay", self.heading)

        main.addLayout(form)

        # ================= AUTO SCALE =================
        self.chk_auto = QCheckBox("Auto scale range")
        self.chk_auto.setChecked(True)
        self.chk_auto.stateChanged.connect(
            lambda s: setattr(self.simulator, "auto_scale", bool(s))
        )
        main.addWidget(self.chk_auto)

        # ================= SWEEP CONTROL =================
        main.addWidget(QLabel("Điều khiển đường quét"))

        sweep_form = QFormLayout()

        # --- Sweep angle ---
        angle_layout = QHBoxLayout()

        self.sweep_angle = QDoubleSpinBox()
        self.sweep_angle.setRange(0, 360)
        self.sweep_angle.setSuffix(" °")
        self.sweep_angle.setValue(0)

        btn_set_angle = QPushButton("SET")
        btn_set_angle.setFixedWidth(60)
        btn_set_angle.clicked.connect(
            lambda: self.simulator.set_sweep_angle(self.sweep_angle.value())
        )

        angle_layout.addWidget(self.sweep_angle)
        angle_layout.addWidget(btn_set_angle)

        sweep_form.addRow("Vị trí quét", angle_layout)

        # --- Sweep speed ---
        speed_layout = QHBoxLayout()

        self.sweep_speed = QSlider(Qt.Orientation.Horizontal)
        self.sweep_speed.setRange(0, 16)
        self.sweep_speed.setValue(int(self.simulator.speed))

        self.lbl_speed = QLabel(f"{self.sweep_speed.value()} deg/s")
        self.lbl_speed.setFixedWidth(70)

        btn_set_speed = QPushButton("SET")
        btn_set_speed.setFixedWidth(60)
        btn_set_speed.clicked.connect(
            lambda: self.simulator.set_sweep_speed(self.sweep_speed.value())
        )

        speed_layout.addWidget(self.sweep_speed)
        speed_layout.addWidget(self.lbl_speed)
        speed_layout.addWidget(btn_set_speed)

        self.sweep_speed.valueChanged.connect(
            lambda v: self.lbl_speed.setText(f"{v} deg/s")
        )

        sweep_form.addRow("Tốc độ quét", speed_layout)

        main.addLayout(sweep_form)


        # ================= BUTTONS =================
        btn_add = QPushButton("Thêm mục tiêu")
        btn_add.clicked.connect(self.add_target)

        btn_start = QPushButton("START")
        btn_start.clicked.connect(lambda: setattr(self.simulator, "running", True))

        btn_stop = QPushButton("STOP")
        btn_stop.clicked.connect(lambda: setattr(self.simulator, "running", False))

        h_btn = QHBoxLayout()
        h_btn.addWidget(btn_add)
        h_btn.addWidget(btn_start)
        h_btn.addWidget(btn_stop)

        main.addLayout(h_btn)

        # ================= TARGET LIST =================
        main.addWidget(QLabel("Danh sách mục tiêu"))

        self.list_targets = QListWidget()
        self.list_targets.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        main.addWidget(self.list_targets)

        # ================= DELETE / RESET =================
        btn_del = QPushButton("Xóa mục tiêu đã chọn")
        btn_del.clicked.connect(self.delete_selected)

        btn_reset = QPushButton("RESET SIMULATOR")
        btn_reset.clicked.connect(self.reset_simulator)

        h2 = QHBoxLayout()
        h2.addWidget(btn_del)
        h2.addWidget(btn_reset)

        main.addLayout(h2)

    # ================= CALLBACKS =================
    def add_target(self):
        t = SimTarget(
            angle_deg=self.angle.value(),
            range_km=self.range_km.value(),
            speed_km_s=self.speed.value(),
            heading_deg=self.heading.value(),
        )

        if self.simulator.add_target(t):
            self.list_targets.addItem(
                f"A={self.angle.value():.1f}° | "
                f"R={self.range_km.value():.1f} km | "
                f"V={self.speed.value():.1f} km/s"

            )

    def send_sweep(self):
        self.simulator.set_sweep_angle(self.sweep_angle.value())
        self.simulator.set_sweep_speed(self.sweep_speed.value())

    def delete_selected(self):
        row = self.list_targets.currentRow()
        if row >= 0:
            self.simulator.remove_target(row)
            self.list_targets.takeItem(row)

    def reset_simulator(self):
        self.simulator.reset()
        self.list_targets.clear()
