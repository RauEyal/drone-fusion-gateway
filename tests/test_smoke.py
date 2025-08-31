import asyncio

from gateway.app.drivers.udp_driver import UdpSensorDriver, ProtobufDecoder
from gateway.app.mux import mux

async def main():
    # Ports must match to the same ones the simulators are sending to
    rf  = UdpSensorDriver(host="0.0.0.0", port=9000, decoder=ProtobufDecoder(), sensor_type="rf")
    ac  = UdpSensorDriver(host="0.0.0.0", port=9001, decoder=ProtobufDecoder(), sensor_type="acoustic")
    gps = UdpSensorDriver(host="0.0.0.0", port=9002, decoder=ProtobufDecoder(), sensor_type="gps")

    count = 0
    # run and turn on sensors simulators
    async for obs in mux([rf, ac, gps]):
        print(obs)
        count += 1
        if count >= 10:
            break

if __name__ == "__main__":
    asyncio.run(main())