from collections import deque
from threading import Lock
from typing import Deque, List

from gateway.app.models import Detection


class DetectionRepo:
    """ ring buffer to store recent detections """

    def __init__(self, capacity: int = 1000):
        self._detections: Deque[Detection] = deque(maxlen=capacity)
        self._lock = Lock()

    def add(self, detection: Detection) -> None:
        with self._lock:
            self._detections.append(detection)

    def list_recent(self, source: str = "fused", limit=50) -> List[Detection]:
        """ lists recent detections """
        with self._lock:
            items = list(self._detections)

        if source != "all":
            items = [d for d in items if d.source == source]

        return items[-limit:]
