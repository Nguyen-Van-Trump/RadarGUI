# config.py

# ================= RADAR GEOMETRY =================
RADAR_MARGIN = 0            # lề ngoài radar (px)

# ================= RANGE MODES =================
RANGE_MODES = {
    1: {"step_km": 10, "max_km": 50},
    2: {"step_km": 30, "max_km": 150},
    3: {"step_km": 60, "max_km": 300},
}

# ================= SWEEP =================
SWEEP_DEFAULT_SPEED = 0    # deg/s
SWEEP_MIN_SPEED = 0
SWEEP_MAX_SPEED = 16

# ================= COLORS =================
COLOR_BG = (0, 0, 0)

COLOR_GRID_MAIN = (0, 120, 0)
COLOR_GRID_STEP = (0,100,0)
COLOR_GRID_MINOR = (0, 90, 0)

COLOR_SWEEP = (0, 255, 0)

COLOR_TARGET = (0, 255, 0)
COLOR_TARGET_TRAIL = (0, 255, 0)

COLOR_MARKER = (255, 165, 0)   # cam
COLOR_CURSOR_TEXT = (0, 255, 0)

# ================= GRID STYLE =================
GRID_MAIN_PEN = 1.5
GRID_STEP_PEN = 1
GRID_MINOR_PEN = 0.8

GRID_LABEL_FONT_SIZE = 10

# ================= MARKER =================
MARKER_MAX = 10
MARKER_SIZE = 5

# ================= CURSOR =================
CURSOR_TEXT_OFFSET = 20
