"""
traffic_light.py
Smart Traffic Signal Controller
"""

from config import YELLOW_TIME


class TrafficLightController:

    def __init__(self):

        self.current_green = "North"

        self.state = "GREEN"

        self.timer = 30

        self.next_direction = "North"

        # Emergency mode flag
        self.emergency_mode = False

    def update(self, ai_data):

        # ==========================================
        # Emergency Vehicle Priority
        # ==========================================

        if ai_data.get("emergency", False):

            self.emergency_mode = True

            # Give green signal immediately
            self.current_green = ai_data["green"]

            self.state = "GREEN"

            self.timer = 15

            return

        else:
            self.emergency_mode = False

        # ==========================================
        # Normal Traffic Logic
        # ==========================================

        # Timer still running
        if self.timer > 0:
            self.timer -= 1
            return

        # GREEN -> YELLOW
        if self.state == "GREEN":

            self.state = "YELLOW"

            self.timer = YELLOW_TIME

            return

        # YELLOW -> GREEN
        if self.state == "YELLOW":

            # Decide which direction gets green next
            self.current_green = ai_data["green"]

            self.state = "GREEN"

            # Lock the timer
            self.timer = ai_data["green_time"]

    def get_state(self):

        return {

            "green_direction": self.current_green,

            "signal_state": self.state,

            "green_time": self.timer,

            "emergency": self.emergency_mode

        }