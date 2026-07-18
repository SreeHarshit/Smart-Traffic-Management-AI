"""
config.py
Global configuration for Smart Traffic Management AI
"""

# ----------------------------
# YOLO
# ----------------------------

MODEL_PATH = "yolov8n.pt"
TRACKER = "bytetrack.yaml"

# ----------------------------
# Demo Videos
# ----------------------------

VIDEOS = {
    "Traffic": {
        "path": "videos/traffic.mp4",
        "emergency": False,
        "emergency_vehicle": None
    },

    "Ambulance": {
        "path": "videos/ambulance.mp4",
        "emergency": True,

        # YOLO detects the ambulance as a truck
        "emergency_vehicle": "truck"
    }
}

# Default video
DEFAULT_VIDEO = "Traffic"

# Current video (used until we add the website dropdown)
VIDEO_PATH = VIDEOS[DEFAULT_VIDEO]["path"]

# ----------------------------
# Vehicle Classes
# ----------------------------

VEHICLE_CLASSES = {
    "car",
    "bus",
    "truck",
    "motorcycle"
}

# ----------------------------
# Traffic Signal
# ----------------------------

MIN_GREEN = 20
MAX_GREEN = 90

YELLOW_TIME = 3
RED_TIME = 2

# ----------------------------
# Dashboard
# ----------------------------

WINDOW_NAME = "SMART TRAFFIC MANAGEMENT AI"

PANEL_WIDTH = 550
PANEL_HEIGHT = 380

# ----------------------------
# Colors (BGR)
# ----------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)

BLUE = (255, 120, 0)

GRAY = (40, 40, 40)
LIGHT_GRAY = (80, 80, 80)
DARK = (25, 25, 25)

CYAN = (255, 255, 0)
MAGENTA = (255, 0, 255)

# ----------------------------
# Congestion
# ----------------------------

LOW_LIMIT = 10
MEDIUM_LIMIT = 20
HIGH_LIMIT = 35
MAX_VEHICLES = 40

# ----------------------------
# Font
# ----------------------------

FONT = 0