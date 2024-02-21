import sys

sys.path.append("")

from micropython import const

import uasyncio as asyncio
import aioble
import bluetooth

#import random
#import struct

# org.bluetooth.service.environmental_sensing
_LED_SERVICE = bluetooth.UUID("19B10000-E8F2-537E-4F6C-D104768A1214")
# org.bluetooth.characteristic.temperature
_LED_SERVICE_CHARATARISTIC = bluetooth.UUID("19B10001-E8F2-537E-4F6C-D104768A1214")
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000


# Register GATT server.
led_service = aioble.Service(_LED_SERVICE)
led_characteristic = aioble.Characteristic(
    ble_service, _LED_SERVICE, read=True, write=True
)
aioble.register_services(ble_service)


# Helper to encode the temperature characteristic encoding (sint16, hundredths of a degree).


# This would be periodically polling a hardware sensor.
async def service_task():
    # write LED status upon request
    
    while True:
        if led_characteristic.read:
            print("Read request")
            await led_characteristic.write(b"Hello World")
        await asyncio.sleep_ms(1000)


# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="mpy-ble_led",
            services=[_LED_SERVICE],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            print("Connection from", connection.device)
            await connection.disconnected()

# Run both tasks.
async def main():
    t1 = asyncio.create_task(service_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)


asyncio.run(main())