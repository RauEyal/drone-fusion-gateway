import asyncio
import grpc

from gateway.app.models import Detection
from gateway.generated.fusion.v1 import detections_pb2_grpc, detections_pb2


class FusionStreamServicer(detections_pb2_grpc.FusionStreamServicer):
    """ gRPC server that streams Detection messages to clients"""
    def __init__(self, det_queue: "asyncio.Queue[Detection]"):
        self.det_queue = det_queue

    async def Subscribe(self, request, context):
        while True:
            det: Detection = await self.det_queue.get()
            if request.fused_only and det.source != "fused":
                continue
            yield detections_pb2.Detection(
                id=det.id, ts_unix_ms=det.ts_unix_ms, lat=det.lat, lon=det.lon,
                confidence=det.confidence, source=det.source, schema_version=det.schema_version,
            )

async def serve_grpc(det_queue: "asyncio.Queue[Detection]"):
    server = grpc.aio.server()
    detections_pb2_grpc.add_FusionStreamServicer_to_server(FusionStreamServicer(det_queue), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
