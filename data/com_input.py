import threading
import time
import serial
import serial.tools.list_ports


class RadarCOMInput(threading.Thread):
    """
    Thread nhận dữ liệu radar qua COM
    Tự quét cổng, không phụ thuộc COM cố định
    """

    BAUDRATES = [115200, 57600, 38400]

    def __init__(self, model):
        super().__init__(daemon=True)
        self.model = model
        self.running = False
        self.ser = None

    # =======================
    # SCAN COM PORT
    # =======================
    def scan_and_connect(self):
        ports = list(serial.tools.list_ports.comports())

        for port in ports:
            for baud in self.BAUDRATES:
                try:
                    ser = serial.Serial(port.device, baud, timeout=0.2)
                    if self._is_radar_device(ser):
                        self.ser = ser
                        print(f"[RADAR] Connected {port.device} @ {baud}")
                        return True
                    ser.close()
                except Exception:
                    pass
        return False

    def _is_radar_device(self, ser):
        """
        Radar handshake / test packet
        (cần chỉnh theo thiết bị thật)
        """
        try:
            ser.write(b"PING\n")
            resp = ser.readline()
            return b"RADAR" in resp
        except Exception:
            return False

    # =======================
    # THREAD
    # =======================
    def run(self):
        self.running = True

        if not self.scan_and_connect():
            print("[RADAR] No radar device found")
            return

        while self.running:
            frame = self.read_frame()
            if frame:
                self.model.buffer.write(frame)

    def stop(self):
        self.running = False
        if self.ser:
            self.ser.close()

    # =======================
    # READ FRAME
    # =======================
    def read_frame(self):
        """
        Ví dụ frame ASCII:
        A=123.4;S=24.0;R=12.5,18.2;P=0.8,0.4;TX=1
        """
        try:
            line = self.ser.readline().decode().strip()
            if not line:
                return None

            return self.parse_line(line)
        except Exception:
            return None

    def parse_line(self, line):
        data = {}
        for part in line.split(";"):
            if "=" in part:
                k, v = part.split("=")
                data[k] = v

        return {
            "angle": float(data.get("A", 0)),
            "speed": float(data.get("S", 0)),
            "ranges": [float(x) for x in data.get("R", "").split(",") if x],
            "power": [float(x) for x in data.get("P", "").split(",") if x],
            "status": {
                "tx_on": data.get("TX", "0") == "1",
                "tx_mode": int(data.get("MODE", 0)),
                "dummy": [0] * 10
            }
        }
