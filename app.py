# app.py
import sys
from qt_compat import QApplication

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
