import threading


class FrameBuffer:
    """
    Buffer 1 frame (overwrite)
    - Giữ frame mới nhất
    - Thread-safe
    - Không tích lũy độ trễ
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._frame = None

    def write(self, frame: dict):
        with self._lock:
            self._frame = frame

    def read(self):
        with self._lock:
            frame = self._frame
            self._frame = None
            return frame
