from abc import ABC, abstractmethod
from typing import AsyncIterator, Protocol

from .models import RawObservation, Detection

class ObservationDecoder(Protocol):
    def decode(self, data: bytes) -> RawObservation: ...

class SensorDriver(ABC):
    """ abstract class for sensor decoding bytes to Observation messages """
    def __init__(self, sensor_type):
        self.sensor_type = sensor_type

    @abstractmethod
    async def stream(self) -> AsyncIterator[RawObservation]:
        """ Yields an observation. never raises errors, just logs them """
        pass

class FusionStrategy(ABC):
    """ Process the observations and yields Detections """
    @abstractmethod
    async def process(self, observations: AsyncIterator[RawObservation]) -> AsyncIterator[Detection]:
        """ process an observation. never raises errors, just logs them """
        pass

