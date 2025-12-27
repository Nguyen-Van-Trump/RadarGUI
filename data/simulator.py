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
        self.running = False
        self.last_time = time.time()
        
    def add_target(self, target: SimTarget):
        if len(self.targets) >= self.max_targets:
            return False
        self.targets.append(target)
        return True

