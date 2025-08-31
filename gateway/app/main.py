import asyncio
from typing import List

import uvicorn

from gateway.app.api.grpc_server import serve_grpc
from gateway.app.api.rest import build_app
from gateway.app.detection_repo import DetectionRepo
from gateway.app.drivers.udp_driver import UdpSensorDriver, ProtobufDecoder
from gateway.app.fusion import DualStrategy

from gateway.app.models import Detection
from gateway.app.mux import mux


def init_drivers() -> List[UdpSensorDriver]:
    rf = UdpSensorDriver(host="0.0.0.0", port=9000, sensor_type="rf", decoder=ProtobufDecoder())
    ac = UdpSensorDriver(host="0.0.0.0", port=9001, sensor_type="acoustic", decoder=ProtobufDecoder())
    gps = UdpSensorDriver(host="0.0.0.0", port=9002, sensor_type="gps", decoder=ProtobufDecoder())
    return [rf, ac, gps]


async def main_async():
    repo = DetectionRepo(capacity=1000)
    app = build_app(repo)

    drivers_list = init_drivers()
    observations = mux(drivers_list)
    fusion_strategy = DualStrategy()

    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8000))

    det_queue: asyncio.Queue[Detection] = asyncio.Queue(maxsize=1000)


    async def fusion_task():
        async for det in fusion_strategy.process(observations):
            repo.add(det)
            await det_queue.put(det)

    async def rest_task():
        await server.serve()

    await asyncio.gather(
        fusion_task(),
        rest_task(),
        serve_grpc(det_queue),
    )


if __name__ == "__main__":
    asyncio.run(main_async())
