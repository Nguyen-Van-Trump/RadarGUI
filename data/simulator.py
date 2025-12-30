import math
import threading
import time
from config import RANGE_MODES, HYSTERESIS_RATIO

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
        
        # ===== SWEEP =====
        self.angle = 0.0
        self.speed = 0.0  # deg/s

        # ===== THREAD CONTROL =====
        self.running = False     # phát dữ liệu
        self.tx_on = True        # phát hay không
        self.alive = True        # vòng thread

        # ===== RANGE AUTO SCALE =====
        self.auto_scale = True
        self.range_mode = min(RANGE_MODES.keys())
        self.hysteresis_ratio = HYSTERESIS_RATIO

        self.last_time = time.time()

    # ================= CONTROL =================
    def stop(self):
        self.alive = False

    def add_target(self, target):
        if len(self.targets) >= self.max_targets:
            return False
        self.targets.append(target)
        return True
    
    def set_tx(self, state: bool):
        self.tx_on = state

    # ================= RANGE LOGIC =================
    def _max_target_range(self):
        max_r = 0.0
        for t in self.targets:
            _, r = t.polar()
            if r > max_r:
                max_r = r
        return max_r

    def _next_range_mode_up(self, current_mode):
        modes = sorted(RANGE_MODES.keys())
        idx = modes.index(current_mode)
        return modes[min(idx + 1, len(modes) - 1)]

    def _next_range_mode_down(self, current_mode):
        modes = sorted(RANGE_MODES.keys())
        idx = modes.index(current_mode)
        return modes[max(idx - 1, 0)]

    def _update_range_mode(self, max_range):
        if not self.auto_scale:
            return self.range_mode

        current_cfg = RANGE_MODES[self.range_mode]
        current_max = current_cfg["max_km"]

        # ===== TĂNG RANGE =====
        if max_range > current_max:
            return self._next_range_mode_up(self.range_mode)

        # ===== GIẢM RANGE (HYSTERESIS) =====
        lower_mode = self._next_range_mode_down(self.range_mode)
        lower_max = RANGE_MODES[lower_mode]["max_km"]

        if max_range < lower_max * self.hysteresis_ratio:
            return lower_mode

        return self.range_mode
    
    # ================= SWEEP CONTROL =================
    def set_sweep_angle(self, angle_deg: float):
        """
        Đặt lại vị trí đường quét (deg)
        """
        self.angle = angle_deg % 360

    def set_sweep_speed(self, speed_deg_s: float):
        """
        Đặt tốc độ quét (deg/s)
        """
        self.speed = max(0.0, min(16.0, speed_deg_s))

            
    # ================= TARGET CONTROL =================
    def remove_target(self, index):
        if 0 <= index < len(self.targets):
            self.targets.pop(index)

    def clear_targets(self):
        self.targets.clear()

    def reset(self):
        """
        Reset simulator về trạng thái ban đầu
        """
        self.running = False
        self.targets.clear()
        self.angle = 0.0
        self.range_mode = min(RANGE_MODES.keys())


    # ================= THREAD =================
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

            BEAM_WIDTH = 4.0  # deg

            for t in self.targets:
                t.step(dt)
                ang, r = t.polar()
                if self.tx_on:
                    if abs((ang - self.angle + 180) % 360 - 180) < BEAM_WIDTH / 2:
                        ranges.append(r)
                        power.append(t.power)

            # ===== AUTO SCALE =====
            max_range = self._max_target_range()
            self.range_mode = self._update_range_mode(max_range)

            # ===== FRAME =====
            frame = {
                "angle": self.angle,
                "speed": self.speed,
                "range_mode": self.range_mode,
                "ranges": ranges,
                "power": power,
                "status": {
                    "tx_on": self.tx_on,
                    "tx_mode": 1,
                    "dummy": [0] * 10
                }
            }

            self.model.buffer.write(frame)
            time.sleep(0.03)

