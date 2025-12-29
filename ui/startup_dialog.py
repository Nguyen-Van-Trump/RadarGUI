from qt_compat import *
from config import COLOR_MAIN_BG, COLOR_TEXT_PRIMARY


class StartupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ===== SET DIALOG BACKGROUND COLOR =====
        palette = self.palette()
        palette.setColor(
            QPalette.Window,
            QColor(*COLOR_MAIN_BG)
        )
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setWindowTitle("Radar Mode Selection")
        self.choice = None

        layout = QVBoxLayout(self)

        # ===== TITLE LABEL =====
        lbl_title = QLabel("Chọn chế độ hoạt động radar")
        lbl_title.setStyleSheet(
            f"color: rgb{COLOR_TEXT_PRIMARY};"
        )

        # làm chữ rõ và nổi hơn
        font = lbl_title.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        lbl_title.setFont(font)

        lbl_title.setAlignment(AlignCenter)
        layout.addWidget(lbl_title)

        # ===== BUTTONS =====
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
