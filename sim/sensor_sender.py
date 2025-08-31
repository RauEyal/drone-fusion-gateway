import os
import socket
import sys
import time
from dataclasses import dataclass

THIS_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gateway.generated.fusion.v1 import observations_pb2

SENSORS_TYPES = ["rf", "acoustic", "gps"]


def now_ms() -> int:
    return int(time.time() * 1000)


@dataclass
class SensorSender:
    sensor_type: str
    host: str = os.getenv("TARGET_HOST", "127.0.0.1")
    port: int = int(os.getenv("TARGET_PORT", "9000"))
    lat: float = float(os.getenv("LAT", "0.0"))
    lon: float = float(os.getenv("LON", "0.0"))

    def __post_init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.sensor_type not in SENSORS_TYPES:
            raise ValueError(f"Unknown sensor type: {self.sensor_type}")

    def send(self, value: float, aux: float = 0.0, *, lat: float = None, lon: float = None, ts_unix_ms: int = None):
        msg = observations_pb2.RawObservation(
            ts_unix_ms=ts_unix_ms or now_ms(),
            lat=lat if lat is not None else self.lat,
            lon=lon if lon is not None else self.lon,
            sensor_type=self.sensor_type,
            value=value,
            aux=aux
        )
        self.sock.sendto(msg.SerializeToString(), (self.host, self.port))
        return msg

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
