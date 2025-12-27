from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel
)


class StartupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radar Mode Selection")
        self.choice = None

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Chọn chế độ hoạt động radar"))

        btn_real = QPushButton("Radar Thật (COM)")
        btn_sim = QPushButton("Giả Lập Radar")

        btn_real.clicked.connect(self.select_real)
        btn_sim.clicked.connect(self.select_sim)

        layout.addWidget(btn_real)
        layout.addWidget(btn_sim)

    def select_real(self):
        self.choice = "REAL"
        self.accept()

    def select_sim(self):
        self.choice = "SIM"
        self.accept()
