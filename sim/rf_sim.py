import os
import random
import sys
import time

from sensor_sender import SensorSender

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    with SensorSender(port=int(os.getenv("TARGET_PORT", "9000")), sensor_type="rf") as tx:
        lat, lon = float(os.getenv("LAT", -33.8688)), float(os.getenv("LON", 151.2093))
        while True:
            rssi = random.uniform(30, 70)
            tx.send(value=rssi, lat=lat, lon=lon)
            print("rf - rssi sent")
            time.sleep(0.2)
if __name__ == "__main__":
  main()
