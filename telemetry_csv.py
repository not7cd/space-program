"""Provides basic ability to log telemetry data to csv file"""

import csv
import time
import krpc
from glom import glom

CSV_SPEC = {
    "met": "vessel.met",
    "surf_speed": "flight.speed",
    "mean_altitude": "flight.mean_altitude",
    "g_force": "flight.g_force",
    "aoa": "flight.angle_of_attack",
    "sideslip": "flight.sideslip_angle",
    "atmosphere_density": "flight.atmosphere_density",
    "dynamic_pressure": "flight.dynamic_pressure",
}

INTERVAL = 1


class Telemetry:
    """Provides interface for basic telemetry"""

    def __init__(self, vessel):
        self.vessel = vessel
        self.flight = vessel.flight(self._reference_frame)

    @property
    def orbit(self):
        return self.vessel.orbit

    @property
    def _reference_frame(self):
        return self.vessel.orbit.body.reference_frame


if __name__ == "__main__":
    try:
        print("Connecting to KSP. Please accept the connection from kRPC window in KSP")
        conn = krpc.connect(name=__file__)
    except krpc.error.NetworkError as e:
        print("Failed to connect to kRPC server. Is KSP and the kRPC Server running?")
        raise e

    telemetry = Telemetry(conn.space_center.active_vessel)

    data_endpoints = {
        "space_center": conn.space_center,
        "vessel": telemetry.vessel,
        "flight": telemetry.flight,
        "orbit": telemetry.orbit,
    }

    filename = "telemetry/{}_{}.csv".format(
        data_endpoints["space_center"].ut, data_endpoints["vessel"].name
    )

    with open(filename, "w", newline="") as csvfile:
        fieldnames = list(CSV_SPEC.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        while True:
            row = glom(data_endpoints, CSV_SPEC)
            writer.writerow(row)
            print(row)

            time.sleep(INTERVAL)
