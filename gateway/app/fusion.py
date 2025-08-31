from typing import AsyncIterator

from gateway.app.interfaces import FusionStrategy
from gateway.app.models import RawObservation, Detection


def make_detection_from(obs, source="fused") -> Detection:
    confidence = 0.5
    if obs.sensor_type == "rf":
        confidence = min(1.0, obs.value / 100.0)
    return Detection(
        id=f"{obs.sensor_type}-{obs.ts_unix_ms}",
        ts_unix_ms=obs.ts_unix_ms,
        lat=obs.lat,
        lon=obs.lon,
        confidence=confidence,
        source=source,
        schema_version=obs.schema_version,
    )


class RawPassThrough(FusionStrategy):
    """ Example fusion that just passes through raw observations as detections """
    async def process(self, observations: AsyncIterator[RawObservation]) -> AsyncIterator[Detection]:
        async for obs in observations:
            yield make_detection_from(obs, source=obs.sensor_type)

class DualStrategy(FusionStrategy):
    """ Example fusion that yields two detections for each observation """
    async def process(self, observations: AsyncIterator[RawObservation]) -> AsyncIterator[Detection]:
        async for obs in observations:
            yield make_detection_from(obs) # fused
            yield make_detection_from(obs, source=obs.sensor_type)


