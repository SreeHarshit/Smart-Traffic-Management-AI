"""
detector.py
Handles YOLO vehicle detection.
"""

from ultralytics import YOLO
from config import MODEL_PATH, VEHICLE_CLASSES


class VehicleDetector:

    def __init__(self):

        print("Loading YOLO model...")

        self.model = YOLO(MODEL_PATH)

        print("YOLO model loaded successfully.")

    def detect(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        vehicles = []

        if len(results) == 0:
            return vehicles, results

        result = results[0]

        if result.boxes is None:
            return vehicles, results

        for box in result.boxes:

            cls = int(box.cls[0])

            class_name = self.model.names[cls]

            if class_name not in VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = box.xyxy[0]

            vehicle = {

                "type": class_name,

                "id": int(box.id[0]) if box.id is not None else -1,

                "x1": int(x1),
                "y1": int(y1),

                "x2": int(x2),
                "y2": int(y2),

                "cx": int((x1 + x2) / 2),

                "cy": int((y1 + y2) / 2)
            }

            vehicles.append(vehicle)

        return vehicles, results