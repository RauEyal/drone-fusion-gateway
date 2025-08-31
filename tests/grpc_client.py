import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import grpc
from gateway.generated.fusion.v1 import detections_pb2_grpc, detections_pb2

def main():
    channel = grpc.insecure_channel("localhost:50051")
    stub = detections_pb2_grpc.FusionStreamStub(channel)
    req = detections_pb2.SubscribeRequest(fused_only=False)
    for i, det in enumerate(stub.Subscribe(req)):
        print(det)
        if i >= 10:
            break

if __name__ == "__main__":
    main()