import os
import random
import sys
import time

from sim.sensor_sender import SensorSender

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    with SensorSender(port=int(os.getenv("TARGET_PORT", "9001")), sensor_type="gps") as tx:
        lat, lon = float(os.getenv("LAT", -33.8690)), float(os.getenv("LON", 151.2095))
        db = random.uniform(55, 75)  # float(os.getenv("DB", 10.0))
        while True:
            tx.send(value=db, lat=lat, lon=lon)
            print("acoustic - speed sent")
            time.sleep(0.2)


if __name__ == "__main__":
    main()
