from qt_compat import *
from qt_compat import QPalette, QColor
from config import COLOR_MAIN_BG


from radar.canvas import RadarCanvas
from data.radar_model import RadarModel
from data.com_input import RadarCOMInput
from data.simulator import RadarSimulator
from ui.startup_dialog import StartupDialog
from ui.simtarget_dialog import SimTargetDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ===== SET MAIN WINDOW BACKGROUND COLOR =====
        palette = self.palette()
        palette.setColor(
            QPalette.Window,
            QColor(*COLOR_MAIN_BG)
        )
        self.setPalette(palette)
        self.setAutoFillBackground(True)


        self.setWindowTitle("Radar PPI")
        self.showFullScreen()

        # ===== MODEL =====
        self.model = RadarModel()

        # ===== CANVAS =====
        self.radar = RadarCanvas(self.model)

        # ===== MARKER BUTTON =====
        self.btn_marker = QPushButton("MARKER")
        self.btn_marker.setCheckable(True)
        self.btn_marker.clicked.connect(self.toggle_marker)
        self._set_marker_style(False)

        # ===== TX STATUS =====
        self.btn_tx = QPushButton("TX OFF")
        self.btn_tx.setEnabled(False)
        self._set_tx_style(False)

        # ===== SWEEP SPEED DISPLAY =====
        self.lbl_speed = QLabel("SPEED: 0.0 deg/s")
        self.lbl_speed.setAlignment(AlignCenter)
        self.lbl_speed.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 18px;
                height: 40px;
            }
        """)

        # ===== EXIT =====
        btn_exit = QPushButton("EXIT")
        btn_exit.clicked.connect(QApplication.quit)
        btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #aa0000;
                color: white;
                font-size: 20px;
                height: 60px;
            }
        """)

        # ===== SIDE BAR =====
        side = QVBoxLayout()
        side.addWidget(self.btn_marker)
        side.addWidget(self.btn_tx)
        side.addWidget(self.lbl_speed)
        side.addStretch()
        side.addWidget(btn_exit)

        # ===== MAIN LAYOUT =====
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.radar, 1)
        layout.addLayout(side)

        self.setCentralWidget(container)

        # ===== DATA SOURCE =====
        self.input_device = None
        self.simulator = None
        self.sim_dialog = None

        self.select_mode()

        # ===== UI UPDATE TIMER =====
        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.update_status)
        self.ui_timer.start(100)

    # =============================
    # MODE SELECTION
    # =============================
    def select_mode(self):
        dlg = StartupDialog(self)
        dlg.exec()

        if dlg.choice == "REAL":
            self.start_real_radar()
        elif dlg.choice == "SIM":
            self.start_simulator()

    def start_real_radar(self):
        self.input_device = RadarCOMInput(self.model)
        self.input_device.start()

    def start_simulator(self):
        self.simulator = RadarSimulator(self.model)
        self.simulator.start()

        self.sim_dialog = SimTargetDialog(self.simulator)
        self.sim_dialog.show()

    # =============================
    # MARKER
    # =============================
    def toggle_marker(self):
        state = self.btn_marker.isChecked()
        self.radar.marker_mgr.toggle(state)
        self._set_marker_style(state)

    def _set_marker_style(self, state: bool):
        self.btn_marker.setStyleSheet("""
            QPushButton {
                background-color: %s;
                color: %s;
                font-size: 18px;
                height: 60px;
            }
        """ % (
            "orange" if state else "#202020",
            "black" if state else "#00ff00"
        ))

    # =============================
    # STATUS UPDATE
    # =============================
    def update_status(self):
        snap = self.model.get_snapshot()

        # TX
        tx_on = snap["tx_on"] and snap["connected"]
        self.btn_tx.setText("TX ON" if tx_on else "TX OFF")
        self._set_tx_style(tx_on)

        # SPEED DISPLAY (READ ONLY)
        self.lbl_speed.setText(f"TỐC ĐỘ QUÉT: {snap['speed']:.1f} deg/s")

    def _set_tx_style(self, tx_on: bool):
        self.btn_tx.setStyleSheet("""
            QPushButton {
                background-color: %s;
                color: %s;
                font-size: 22px;
                height: 70px;
            }
        """ % (
            "#00aa00" if tx_on else "black",
            "white" if tx_on else "#00ff00"
        ))

    # =============================
    # CLEAN EXIT
    # =============================
    def closeEvent(self, event):
        if self.input_device:
            self.input_device.stop()

        if self.simulator:
            self.simulator.stop()

        event.accept()
