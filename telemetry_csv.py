"""Provides basic ability to log telemetry data to csv file"""

import csv
import time
import krpc
from glom import glom

CSV_SPEC = {
    "ut": "space_center.ut",
    "surf_speed": "flight.speed",
    "mean_altitude": "flight.mean_altitude",
    "g_force": "flight.g_force",
    "aoa": "flight.angle_of_attack",
    "sideslip": "flight.sideslip_angle",
    "atmosphere_density": "flight.atmosphere_density",
    "dynamic_pressure": "flight.dynamic_pressure",
}

INTERVAL = 1

if __name__ == "__main__":
    try:
        print("Connecting to KSP. Please accept the connection from kRPC window in KSP")
        conn = krpc.connect(name=__file__)
    except krpc.error.NetworkError as e:
        print("Failed to connect to kRPC server. Is KSP and the kRPC Server running?")
        raise e

    data_endpoints = {
        "space_center": conn.space_center,
        "vessel": conn.space_center.active_vessel,
        "flight": conn.space_center.active_vessel.flight(
            conn.space_center.active_vessel.orbit.body.reference_frame
        ),
        "orbit": conn.space_center.active_vessel.orbit,
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
