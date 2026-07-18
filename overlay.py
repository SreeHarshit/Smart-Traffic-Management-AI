"""
overlay.py
Road overlays for Smart Traffic AI
"""

import cv2

from config import *


class RoadOverlay:

    def __init__(self):

        self.alpha = 0.30

    # ---------------------------------------------

    def draw_divider(self, frame):

        h, w = frame.shape[:2]

        divider = h // 2

        cv2.line(
            frame,
            (0, divider),
            (w, divider),
            WHITE,
            3
        )

        cv2.putText(
            frame,
            "NORTHBOUND",
            (20, divider - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            WHITE,
            2
        )

        cv2.putText(
            frame,
            "SOUTHBOUND",
            (20, divider + 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            WHITE,
            2
        )

        return divider

    # ---------------------------------------------

    def draw_overlay(self, frame, signal):

        overlay = frame.copy()

        h, w = frame.shape[:2]

        divider = self.draw_divider(overlay)

        if signal["green_direction"] == "North":

            cv2.rectangle(
                overlay,
                (0, 0),
                (w, divider),
                GREEN,
                -1
            )

            cv2.rectangle(
                overlay,
                (0, divider),
                (w, h),
                RED,
                -1
            )

        else:

            cv2.rectangle(
                overlay,
                (0, 0),
                (w, divider),
                RED,
                -1
            )

            cv2.rectangle(
                overlay,
                (0, divider),
                (w, h),
                GREEN,
                -1
            )