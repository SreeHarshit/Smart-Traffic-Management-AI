"""
main.py
Smart Traffic Management AI
"""

import cv2

from config import VIDEO_PATH, WINDOW_NAME
from detector import VehicleDetector
from traffic_controller import TrafficController
from traffic_light import TrafficLightController
from dashboard import Dashboard


def main():

    print("Starting Smart Traffic AI...")

    detector = VehicleDetector()

    controller = TrafficController()

    traffic_light = TrafficLightController()

    dashboard = Dashboard()

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Error opening video.")
        return

    # Print video resolution
    print("Video Width :", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("Video Height:", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # Make OpenCV window resizable
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 1900, 900)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # -----------------------------
        # AI Detection
        # -----------------------------

        vehicles, results = detector.detect(frame)

        # Draw YOLO detections
        if len(results) > 0:
            annotated = results[0].plot()
        else:
            annotated = frame.copy()

        # -----------------------------
        # AI Decision
        # -----------------------------

        ai_data = controller.analyze(
            vehicles,
            annotated.shape[0]
        )

        # -----------------------------
        # Update Signal
        # -----------------------------

        traffic_light.update(ai_data)

        signal = traffic_light.get_state()

        # -----------------------------
        # Dashboard
        # -----------------------------

        screen = dashboard.draw(
            annotated,
            ai_data,
            signal
        )

        cv2.imshow(WINDOW_NAME, screen)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()