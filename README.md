# Mini Multi-Sensors -> Fusion Gateway

This demo shows: UDP/Protobuf ingest, simple fusion, gRPC streaming + REST API.

## Quick Start

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r gateway/requirements.txt

# Run the setup script to generate protobuf files and create necessary __init__.py files
python setup_protobufs.py

python -m gateway.app.main
```

Run simulators in another terminal:
```
python sim/run_all_sensors.py
```

Enter the sensor's number you want to run

REST:
```
curl "http://localhost:8000/detections?source=fused&limit=5"
```

gRPC:
run small gRPC subscriber - disconnects after 10 messages
```
python grpc_client.py
```
