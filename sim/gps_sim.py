import os
import sys
import time

from sensor_sender import SensorSender

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    with SensorSender(port=int(os.getenv("TARGET_PORT", "9002")), sensor_type="gps") as tx:
        lat, lon = float(os.getenv("LAT", -33.8690)), float(os.getenv("LON", 151.2095))
        heading = float(os.getenv("HEADING", 90.0))
        speed = float(os.getenv("SPEED", 10.0))
        while True:
            tx.send(value=speed, aux=heading, lat=lat, lon=lon)
            # print(f"===== gps =====\n{msg}")
            time.sleep(1.0)


if __name__ == "__main__":
    main()
