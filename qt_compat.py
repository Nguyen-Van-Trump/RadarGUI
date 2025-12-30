QT_VERSION = None

try:
    # ===== PyQt6 =====
    from PyQt6.QtCore import Qt, QTimer, QPointF
    from PyQt6.QtGui import (
        QPainter, QColor, QPen, QPalette
    )
    from PyQt6.QtWidgets import *

    NoPen = Qt.PenStyle.NoPen
    AlignCenter = Qt.AlignmentFlag.AlignCenter
    Horizontal = Qt.Orientation.Horizontal
    MouseLeft = Qt.MouseButton.LeftButton
    MouseRight = Qt.MouseButton.RightButton

    def event_pos(event):
        return event.position()

    RenderAntialias = QPainter.RenderHint.Antialiasing

    QT_VERSION = 6

except ImportError:
    # ===== PyQt5 =====
    from PyQt5.QtCore import Qt, QTimer, QPointF
    from PyQt5.QtGui import (
        QPainter, QColor, QPen, QPalette
    )
    from PyQt5.QtWidgets import *

    NoPen = Qt.NoPen
    AlignCenter = Qt.AlignCenter
    Horizontal = Qt.Horizontal
    MouseLeft = Qt.LeftButton
    MouseRight = Qt.RightButton

    def event_pos(event):
        return event.pos()

    RenderAntialias = QPainter.Antialiasing

    QT_VERSION = 5
