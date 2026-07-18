from flask import Flask, render_template, Response, jsonify
import cv2

from config import VIDEO_PATH, VIDEOS, DEFAULT_VIDEO
from detector import VehicleDetector
from traffic_controller import TrafficController
from traffic_light import TrafficLightController
from dashboard import Dashboard

# =====================================================
# Flask App
# =====================================================

app = Flask(__name__)

print("Loading AI Modules...")

detector = VehicleDetector()
controller = TrafficController()
traffic_light = TrafficLightController()
dashboard = Dashboard()

print("AI Ready!")

# =====================================================
# Current Demo Configuration
# =====================================================

current_demo = DEFAULT_VIDEO

VIDEO_PATH = VIDEOS[current_demo]["path"]

video_info = VIDEOS[current_demo]

cap = cv2.VideoCapture(VIDEO_PATH)

# =====================================================
# Red Light Violation Variables
# =====================================================

violated_ids = set()

violation_count = 0

stop_line = 0

# =====================================================
# Analytics Variables
# =====================================================

vehicle_stats = {
    "car": 0,
    "motorcycle": 0,
    "bus": 0,
    "truck": 0
}

traffic_history = []

MAX_HISTORY = 30

emergency_count = 0

last_vehicle_total = 0

# =====================================================
# Frame Generator
# =====================================================

def generate_frames():

    global cap
    global VIDEO_PATH
    global video_info
    global current_demo

    global violated_ids
    global violation_count
    global stop_line

    global vehicle_stats
    global traffic_history
    global emergency_count
    global last_vehicle_total
    while True:

        success, frame = cap.read()

        if not success:

            cap.release()
            cap = cv2.VideoCapture(VIDEO_PATH)
            continue

        # -----------------------------
        # YOLO Detection
        # -----------------------------

        vehicles, results = detector.detect(frame)

        # -----------------------------
        # Live Analytics
        # -----------------------------

        current_counts = {
            "car": 0,
            "motorcycle": 0,
            "bus": 0,
            "truck": 0
        }

        for vehicle in vehicles:

            vehicle_type = vehicle["type"].lower()

            if vehicle_type in current_counts:
                current_counts[vehicle_type] += 1

        vehicle_stats = current_counts.copy()

        last_vehicle_total = sum(current_counts.values())

        traffic_history.append(last_vehicle_total)

        if len(traffic_history) > MAX_HISTORY:
            traffic_history.pop(0)

        # -----------------------------
        # Draw Detection
        # -----------------------------

        if results and len(results) > 0:
            annotated = results[0].plot()
        else:
            annotated = frame.copy()

        # -----------------------------
        # AI Traffic Analysis
        # -----------------------------

        ai_data = controller.analyze(
            vehicles,
            frame.shape[0]
        )

        # -----------------------------
        # Traffic Signal
        # -----------------------------

        traffic_light.update(ai_data)

        signal = traffic_light.get_state()

        # -----------------------------
        # Emergency Vehicle Detection
        # -----------------------------

        emergency_detected = False

        if video_info["emergency"]:

            emergency_vehicle = video_info["emergency_vehicle"]

            for vehicle in vehicles:

                if vehicle["type"] == emergency_vehicle:

                    emergency_detected = True
                    emergency_count += 1

                    x1 = vehicle["x1"]
                    y1 = vehicle["y1"]
                    x2 = vehicle["x2"]
                    y2 = vehicle["y2"]

                    cv2.rectangle(
                        annotated,
                        (x1, y1),
                        (x2, y2),
                        (255, 0, 255),
                        3
                    )

                    cv2.putText(
                        annotated,
                        "EMERGENCY VEHICLE",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 255),
                        2
                    )

                    break

        ai_data["emergency"] = emergency_detected

        # -----------------------------
        # Stop Line
        # -----------------------------

        stop_line = frame.shape[0] // 2

        cv2.line(
            annotated,
            (0, stop_line),
            (annotated.shape[1], stop_line),
            (0, 0, 255),
            3
        )

        cv2.putText(
            annotated,
            "STOP LINE",
            (20, stop_line - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        # -----------------------------
        # Red Light Violation Detection
        # -----------------------------

        for vehicle in vehicles:

            vehicle_id = vehicle["id"]

            if vehicle_id == -1:
                continue

            if vehicle_id in violated_ids:
                continue

            x1 = vehicle["x1"]
            y1 = vehicle["y1"]
            x2 = vehicle["x2"]
            y2 = vehicle["y2"]

            cy = vehicle["cy"]

            if signal["green_direction"] == "South":

                if cy < stop_line:

                    violated_ids.add(vehicle_id)
                    violation_count += 1

                    cv2.rectangle(
                        annotated,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        annotated,
                        "RED LIGHT VIOLATION",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

            else:

                if cy > stop_line:

                    violated_ids.add(vehicle_id)
                    violation_count += 1

                    cv2.rectangle(
                        annotated,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        annotated,
                        "RED LIGHT VIOLATION",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )
                            # -----------------------------
        # Dashboard Data
        # -----------------------------

        ai_data["violations"] = violation_count
        ai_data["emergency"] = emergency_detected

        # -----------------------------
        # Dashboard
        # -----------------------------

        final_frame = dashboard.draw(
            annotated,
            ai_data,
            signal
        )

        # -----------------------------
        # Encode Frame
        # -----------------------------

        ret, buffer = cv2.imencode(
            ".jpg",
            final_frame
        )

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame_bytes +
            b'\r\n'
        )


# =====================================================
# Flask Routes
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analytics")
def analytics():

    return render_template("analytics.html")


@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# =====================================================
# Live Analytics API
# =====================================================

@app.route("/stats")
def stats():

    return jsonify({

        "cars": vehicle_stats["car"],
        "bikes": vehicle_stats["motorcycle"],
        "buses": vehicle_stats["bus"],
        "trucks": vehicle_stats["truck"],

        "total": last_vehicle_total,

        "violations": violation_count,

        "emergency": emergency_count,

        "history": traffic_history

    })
# =====================================================
# Change Demo
# =====================================================

@app.route("/change_demo/<demo>")
def change_demo(demo):

    global current_demo
    global VIDEO_PATH
    global video_info
    global cap

    global violation_count
    global violated_ids

    global vehicle_stats
    global traffic_history
    global emergency_count
    global last_vehicle_total

    if demo not in VIDEOS:
        return "Invalid Demo"

    current_demo = demo

    VIDEO_PATH = VIDEOS[current_demo]["path"]

    video_info = VIDEOS[current_demo]

    # -----------------------------
    # Reset Analytics
    # -----------------------------

    violation_count = 0
    violated_ids.clear()

    emergency_count = 0

    last_vehicle_total = 0

    traffic_history.clear()

    vehicle_stats = {
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0
    }

    # -----------------------------
    # Reload Video
    # -----------------------------

    if cap.isOpened():
        cap.release()

    cap = cv2.VideoCapture(VIDEO_PATH)

    print(f"Switched to {current_demo}")

    return "OK"


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )