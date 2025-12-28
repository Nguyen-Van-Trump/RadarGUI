import math
import threading
import time


class SimTarget:
    """
    Mục tiêu giả chuyển động trong mặt phẳng PPI
    """

    def __init__(self, angle_deg, range_km, speed_km_s, heading_deg, power=1.0):
        self.power = power

        # chuyển sang tọa độ Descartes
        rad = math.radians(90 - angle_deg)
        self.x = range_km * math.cos(rad)
        self.y = range_km * math.sin(rad)

        # vector vận tốc
        v_rad = math.radians(90 - heading_deg)
        self.vx = speed_km_s * math.cos(v_rad)
        self.vy = speed_km_s * math.sin(v_rad)

    def step(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def polar(self):
        r = math.hypot(self.x, self.y)
        ang = (90 - math.degrees(math.atan2(self.y, self.x))) % 360
        return ang, r

class RadarSimulator(threading.Thread):
    def __init__(self, model, max_targets=5):
        super().__init__(daemon=True)
        self.model = model
        self.targets = []
        self.max_targets = max_targets

        self.angle = 0.0
        self.speed = 24.0

        self.running = False      # CHỈ phát khi True
        self.alive = True         # điều khiển vòng thread

        self.last_time = time.time()

    def stop(self):
        self.alive = False

    def add_target(self, target):
        if len(self.targets) >= self.max_targets:
            return False
        self.targets.append(target)
        return True

    def run(self):
        self.last_time = time.time()

        while self.alive:
            now = time.time()
            dt = now - self.last_time
            self.last_time = now

            if not self.running:
                time.sleep(0.05)
                continue

            # ===== SWEEP =====
            self.angle = (self.angle + self.speed * dt) % 360

            ranges = []
            power = []

            for t in self.targets:
                t.step(dt)
                ang, r = t.polar()

                # echo gần tia quét
                BEAM_WIDTH = 3.0  # độ, có thể 3–6

                if abs((ang - self.angle + 180) % 360 - 180) < BEAM_WIDTH / 2:
                    ranges.append(r)
                    power.append(t.power)

            frame = {
                "angle": self.angle,
                "speed": self.speed,
                "ranges": ranges,
                "power": power,
                "status": {
                    "tx_on": self.running,
                    "tx_mode": 1,
                    "dummy": [0] * 10
                }
            }

            self.model.update_from_device(frame)
            time.sleep(0.03)

