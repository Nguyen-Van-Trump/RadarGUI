from qt_compat import *
from config import (
    COLOR_MAIN_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_ACCENT
)

from data.simulator import SimTarget


class SimTargetDialog(QDialog):
    def __init__(self, simulator):
        super().__init__()

        # ===== SET DIALOG BACKGROUND COLOR =====
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(*COLOR_MAIN_BG))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

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
        # ===== SET COLOR FOR FORM LABELS =====
        for i in range(form.rowCount()):
            label = form.itemAt(i, QFormLayout.LabelRole)
            if label and label.widget():
                label.widget().setStyleSheet(
                    f"color: rgb{COLOR_TEXT_SECONDARY};"
        )


        # --- đổi màu label trong form ---
        for lbl in self.findChildren(QLabel):
            lbl.setStyleSheet(f"color: rgb{COLOR_TEXT_SECONDARY};")

        main.addLayout(form)

        # ================= AUTO SCALE =================
        self.chk_auto = QCheckBox("Auto scale range")
        self.chk_auto.setChecked(True)
        self.chk_auto.setStyleSheet(
            f"color: rgb{COLOR_TEXT_PRIMARY};"
        )
        self.chk_auto.stateChanged.connect(
            lambda s: setattr(self.simulator, "auto_scale", bool(s))
        )
        main.addWidget(self.chk_auto)

        # ================= SWEEP CONTROL =================
        lbl_sweep = QLabel("Điều khiển đường quét")
        lbl_sweep.setStyleSheet(
            f"color: rgb{COLOR_TEXT_PRIMARY}; font-weight: bold;"
        )
        main.addWidget(lbl_sweep)

        sweep_form = QFormLayout()

        # --- Sweep angle ---
        angle_layout = QHBoxLayout()

        self.sweep_angle = QDoubleSpinBox()
        self.sweep_angle.setRange(0, 360)
        self.sweep_angle.setSuffix(" °")
        self.sweep_angle.setValue(0)

        btn_set_angle = QPushButton("SET")
        btn_set_angle.setFixedWidth(60)

        angle_layout.addWidget(self.sweep_angle)
        angle_layout.addWidget(btn_set_angle)

        sweep_form.addRow("Vị trí quét", angle_layout)

        btn_set_angle.clicked.connect(
            lambda: self.simulator.set_sweep_angle(self.sweep_angle.value())
        )

        # --- Sweep speed ---
        speed_layout = QHBoxLayout()

        self.sweep_speed = QSlider(Horizontal)
        self.sweep_speed.setRange(0, 16)
        self.sweep_speed.setValue(int(self.simulator.speed))

        self.lbl_speed = QLabel(f"{self.sweep_speed.value()} deg/s")
        self.lbl_speed.setFixedWidth(70)
        self.lbl_speed.setStyleSheet(
            f"color: rgb{COLOR_TEXT_PRIMARY};"
        )

        btn_set_speed = QPushButton("SET")
        btn_set_speed.setFixedWidth(60)

        speed_layout.addWidget(self.sweep_speed)
        speed_layout.addWidget(self.lbl_speed)
        speed_layout.addWidget(btn_set_speed)

        self.sweep_speed.valueChanged.connect(
            lambda v: self.lbl_speed.setText(f"{v} deg/s")
        )

        btn_set_speed.clicked.connect(
            lambda: self.simulator.set_sweep_speed(self.sweep_speed.value())
        )

        sweep_form.addRow("Tốc độ quét", speed_layout)
        for i in range(sweep_form.rowCount()):
            label = sweep_form.itemAt(i, QFormLayout.LabelRole)
            if label and label.widget():
                label.widget().setStyleSheet(
                    f"color: rgb{COLOR_TEXT_SECONDARY};"
                )

        main.addLayout(sweep_form)

        # ================= TX TOGGLE =================
        self.btn_tx = QPushButton("TX ON")
        self.btn_tx.setCheckable(True)
        self.btn_tx.setChecked(True)

        self.btn_tx.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb(0, 90, 0);
                color: rgb{COLOR_TEXT_PRIMARY};
                font-weight: bold;
                height: 32px;
            }}
        """)

        self.btn_tx.toggled.connect(self.toggle_tx)
        main.addWidget(self.btn_tx)

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
        lbl_list = QLabel("Danh sách mục tiêu")
        lbl_list.setStyleSheet(
            f"color: rgb{COLOR_TEXT_PRIMARY}; font-weight: bold;"
        )
        main.addWidget(lbl_list)

        self.list_targets = QListWidget()
        self.list_targets.setStyleSheet(f"""
            QListWidget {{
                background-color: rgb(20, 20, 20);
                color: rgb{COLOR_TEXT_PRIMARY};
            }}
        """)
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

    def delete_selected(self):
        row = self.list_targets.currentRow()
        if row >= 0:
            self.simulator.remove_target(row)
            self.list_targets.takeItem(row)

    def reset_simulator(self):
        self.simulator.reset()
        self.list_targets.clear()

    def toggle_tx(self, state: bool):
        self.simulator.set_tx(state)

        if state:
            self.btn_tx.setText("TX ON")
            self.btn_tx.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb(0, 90, 0);
                    color: rgb{COLOR_TEXT_PRIMARY};
                    font-weight: bold;
                }}
            """)
        else:
            self.btn_tx.setText("TX OFF")
            self.btn_tx.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb(40, 40, 40);
                    color: rgb{COLOR_TEXT_ACCENT};
                    font-weight: bold;
                }}
            """)
