"""
dashboard.py
Professional Smart Traffic AI Dashboard
"""

import cv2
import numpy as np
from config import *


class Dashboard:

    def __init__(self):
        self.panel_width = PANEL_WIDTH
        self.bg = (35, 35, 35)
        self.card_color = (55, 55, 55)

    def put(self, img, text, x, y,
            scale=0.7,
            color=WHITE,
            thickness=2):

        cv2.putText(
            img,
            text,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            color,
            thickness
        )

    def create_dashboard(self, frame):

        if frame is None:
            raise ValueError("Frame passed to dashboard is None.")

        h, w = frame.shape[:2]

        dashboard = np.full(
            (h, self.panel_width, 3),
            self.bg,
            dtype=np.uint8
        )

        return np.hstack((frame, dashboard))

    def card(self, img, x, y, w, h):

        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            self.card_color,
            -1
        )

    def traffic_light(self, img, x, y, state):

        cv2.rectangle(
            img,
            (x, y),
            (x + 70, y + 180),
            (45, 45, 45),
            -1
        )

        red = (70, 70, 70)
        yellow = (70, 70, 70)
        green = (70, 70, 70)

        if state == "RED":
            red = RED

        elif state == "YELLOW":
            yellow = YELLOW

        elif state == "GREEN":
            green = GREEN

        cv2.circle(img, (x + 35, y + 35), 20, red, -1)
        cv2.circle(img, (x + 35, y + 90), 20, yellow, -1)
        cv2.circle(img, (x + 35, y + 145), 20, green, -1)

    def progress_bar(self, img, x, y, width, value):

        cv2.rectangle(
            img,
            (x, y),
            (x + width, y + 20),
            LIGHT_GRAY,
            2
        )

        fill = int(width * value / 100)

        color = GREEN

        if value > 40:
            color = YELLOW

        if value > 70:
            color = RED

        cv2.rectangle(
            img,
            (x, y),
            (x + fill, y + 20),
            color,
            -1
        )

    def warning_banner(self, img, x, y, text):

        cv2.rectangle(
            img,
            (x, y),
            (x + 490, y + 45),
            RED,
            -1
        )

        self.put(
            img,
            text,
            x + 10,
            y + 30,
            0.8,
            WHITE,
            2
        )

    def draw(self, frame, ai_data, signal):

        canvas = self.create_dashboard(frame)

        panel_x = frame.shape[1] + 15

        self.put(
            canvas,
            "SMART TRAFFIC AI",
            panel_x,
            35,
            0.9,
            CYAN,
            2
        )

        cv2.line(
            canvas,
            (panel_x, 45),
            (canvas.shape[1] - 15, 45),
            CYAN,
            2
        )

        # ---------------- Vehicle Count ----------------

        y = 65

        self.card(
            canvas,
            panel_x,
            y,
            520,
            155
        )

        self.put(
            canvas,
            "VEHICLE COUNT",
            panel_x + 10,
            y + 25,
            0.7,
            YELLOW
        )

        self.put(
            canvas,
            f"Cars : {ai_data['cars']}",
            panel_x + 20,
            y + 60
        )

        self.put(
            canvas,
            f"Buses : {ai_data['buses']}",
            panel_x + 20,
            y + 90
        )

        self.put(
            canvas,
            f"Trucks : {ai_data['trucks']}",
            panel_x + 20,
            y + 120
        )

        self.put(
            canvas,
            f"Bikes : {ai_data['bikes']}",
            panel_x + 250,
            y + 60
        )

        self.put(
            canvas,
            f"Total : {ai_data['total']}",
            panel_x + 250,
            y + 90
        )

        # ---------------- Road Status ----------------

        y = 240

        self.card(
            canvas,
            panel_x,
            y,
            520,
            110
        )

        self.put(
            canvas,
            "ROAD STATUS",
            panel_x + 10,
            y + 25,
            0.7,
            YELLOW
        )

        self.put(
            canvas,
            f"Northbound : {ai_data['north']}",
            panel_x + 20,
            y + 60
        )

        self.put(
            canvas,
            f"Southbound : {ai_data['south']}",
            panel_x + 20,
            y + 90
        )
                # ---------------- Congestion ----------------

        y = 370

        self.card(
            canvas,
            panel_x,
            y,
            520,
            110
        )

        self.put(
            canvas,
            "CONGESTION",
            panel_x + 10,
            y + 25,
            0.7,
            YELLOW
        )

        self.progress_bar(
            canvas,
            panel_x + 20,
            y + 45,
            420,
            ai_data["congestion"]
        )

        self.put(
            canvas,
            f"{ai_data['congestion']} %",
            panel_x + 20,
            y + 90
        )

        # ---------------- Traffic Signal ----------------

        y = 500

        self.card(
            canvas,
            panel_x,
            y,
            520,
            260
        )

        self.put(
            canvas,
            "TRAFFIC SIGNAL",
            panel_x + 10,
            y + 25,
            0.7,
            CYAN
        )

        self.traffic_light(
            canvas,
            panel_x + 20,
            y + 35,
            signal["signal_state"]
        )

        self.put(
            canvas,
            f"Direction : {signal['green_direction']}",
            panel_x + 100,
            y + 60
        )

        self.put(
            canvas,
            f"State : {signal['signal_state']}",
            panel_x + 100,
            y + 95
        )

        self.put(
            canvas,
            f"Green Time : {ai_data['green_time']} sec",
            panel_x + 100,
            y + 130
        )

        self.put(
            canvas,
            f"Traffic : {ai_data['status']}",
            panel_x + 100,
            y + 165
        )

        # ---------------- Emergency Status ----------------

        if ai_data.get("emergency", False):

            cv2.rectangle(
                canvas,
                (panel_x + 90, y + 185),
                (panel_x + 500, y + 220),
                (0, 0, 255),
                -1
            )

            self.put(
                canvas,
                "EMERGENCY VEHICLE DETECTED",
                panel_x + 105,
                y + 208,
                0.65,
                WHITE,
                2
            )

        else:

            cv2.rectangle(
                canvas,
                (panel_x + 90, y + 185),
                (panel_x + 500, y + 220),
                (0, 180, 0),
                -1
            )

            self.put(
                canvas,
                "NO EMERGENCY",
                panel_x + 200,
                y + 208,
                0.7,
                WHITE,
                2
            )

        # ---------------- Traffic Jam Warning ----------------

        if ai_data["level"] == "SEVERE":

            self.warning_banner(
                canvas,
                panel_x,
                780,
                "TRAFFIC JAM DETECTED"
            )

        return canvas