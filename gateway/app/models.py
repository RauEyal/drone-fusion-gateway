from dataclasses import dataclass
from typing import Literal

SensorType = Literal["rf", "acoustic", "gps"]


@dataclass
class RawObservation:
    ts_unix_ms: int
    lat: float
    lon: float
    sensor_type: SensorType
    value: float
    aux: float = 0.0
    schema_version: str = "1.0"


@dataclass
class Detection:
    id: str
    ts_unix_ms: int
    lat: float
    lon: float
    confidence: float
    source: str
    schema_version: str
