import asyncio

from gateway.app.interfaces import SensorDriver, ObservationDecoder
from gateway.app.models import RawObservation
from gateway.generated.fusion.v1 import observations_pb2


class _DatagramProtocol(asyncio.DatagramProtocol):
    def __init__(self, q: "asyncio.Queue[bytes]"):
        self.q = q

    def datagram_received(self, data, addr):
        self.q.put_nowait(data)


class ProtobufDecoder:
    """ Example decoder that decodes bytes to RawObservation messages using protobuf """

    def decode(self, data: bytes) -> RawObservation:
        msg = observations_pb2.RawObservation()
        msg.ParseFromString(data)
        return RawObservation(
            ts_unix_ms=msg.ts_unix_ms,
            lat=msg.lat,
            lon=msg.lon,
            sensor_type=msg.sensor_type,
            value=msg.value,
            aux=getattr(msg, 'aux', 0.0)
        )


## add another decoder here if needed

class UdpSensorDriver(SensorDriver):
    """ UDP driver that decodes bytes to RawObservation messages """

    def __init__(self, decoder: ObservationDecoder, host: str, port: int, sensor_type: str, max_queue: int = 200):
        super().__init__(sensor_type)
        self.decoder = decoder
        self.host = host
        self.port = port
        self._raw_q: asyncio.Queue = asyncio.Queue(maxsize=max_queue)
        self._listening = False

    async def listen(self):
        """ Listen for UDP packets and put them in the queue """
        if self._listening: return
        loop = asyncio.get_running_loop()
        await loop.create_datagram_endpoint(
            lambda: _DatagramProtocol(self._raw_q),
            local_addr=(self.host, self.port)
        )
        self._listening = True
        print(f"UDP driver listening on {self.host}:{self.port} for sensor type {self.sensor_type}")

    async def stream(self):
        """ Yields an observation. never raises errors, just logs them """
        await self.listen()
        while True:
            try:
                data = await self._raw_q.get()
                obs = self.decoder.decode(data)
                if obs.sensor_type != self.sensor_type:
                    print(f"Warning: received sensor type {obs.sensor_type} but expected {self.sensor_type}")
                yield obs
            except Exception as e:
                print(f"Error in UDP driver for sensor type {self.sensor_type}: {e}")
