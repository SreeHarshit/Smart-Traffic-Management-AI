"""
traffic_controller.py
AI Decision Engine for Smart Traffic Management
"""

from config import *


class TrafficController:

    def __init__(self):

        self.current_green = "North"

        self.green_time = 30

        self.congestion = 0

        self.level = "LOW"

        self.status = "SMOOTH"

    def analyze(self, vehicles, frame_height):

        north = 0
        south = 0

        cars = 0
        buses = 0
        trucks = 0
        bikes = 0

        divider = frame_height // 2

        for vehicle in vehicles:

            vehicle_type = vehicle["type"]

            if vehicle_type == "car":
                cars += 1

            elif vehicle_type == "bus":
                buses += 1

            elif vehicle_type == "truck":
                trucks += 1

            elif vehicle_type == "motorcycle":
                bikes += 1

            if vehicle["cy"] < divider:
                north += 1
            else:
                south += 1

        total = north + south

        congestion = min(int((total / MAX_VEHICLES) * 100), 100)

        if total < LOW_LIMIT:
            level = "LOW"
            status = "SMOOTH"

        elif total < MEDIUM_LIMIT:
            level = "MEDIUM"
            status = "MODERATE"

        elif total < HIGH_LIMIT:
            level = "HIGH"
            status = "HEAVY"

        else:
            level = "SEVERE"
            status = "TRAFFIC JAM"

        # Decide which side should get GREEN
        if north >= south:
            current_green = "North"
            active = north
        else:
            current_green = "South"
            active = south

        # Fixed green timings
        if active >= 20:
            green_time = 60
        elif active >= 10:
            green_time = 45
        else:
            green_time = 30

        data = {

            "north": north,
            "south": south,

            "cars": cars,
            "buses": buses,
            "trucks": trucks,
            "bikes": bikes,

            "total": total,

            "congestion": congestion,

            "level": level,

            "status": status,

            "green": current_green,

            "green_time": green_time
        }

        return data