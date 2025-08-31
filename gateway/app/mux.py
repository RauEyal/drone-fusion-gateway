import asyncio
from typing import AsyncIterator, Iterable, Tuple

from gateway.app.drivers.udp_driver import UdpSensorDriver
from gateway.app.models import RawObservation


async def mux(drivers: Iterable[UdpSensorDriver]) -> AsyncIterator[RawObservation]:
    """
    Merge observations from multiple drivers into a single async stream

    """
    queue: asyncio.Queue[Tuple[int, RawObservation]] = asyncio.Queue(maxsize=1000)

    async def pump(idx: int, driver: UdpSensorDriver):
        async for ob in driver.stream():
            await queue.put((idx, ob))

    # Spawn a task per driver
    for i, d in enumerate(drivers):
        asyncio.create_task(pump(i, d))


    while True:
        _idx, obs = await queue.get()
        yield obs
