from logging_config import logger
from bleak import BleakScanner

class BLEManager:
    def __init__(self):
        self.logger = logger

    async def scan_for_devices(self):
        self.logger.info("Scanning for BLE devices...")

        try:
            found_devices = await BleakScanner.discover()
            atc_devices = [device.name for device in found_devices if device.name and device.name.startswith("ATC_")]

            self.logger.info(f"Discovered ATC devices: {atc_devices}")
            return atc_devices

        except Exception as e:
            self.logger.error("Failed to scan for BLE devices", exc_info=True)
            return []
