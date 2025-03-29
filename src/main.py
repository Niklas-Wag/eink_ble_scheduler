import asyncio
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError

async def run():
    print("Scanning for BLE devices...")
    
    # Discover devices
    devices = await BleakScanner.discover(timeout=10.0)
    target_device = None
    
    # Find our target device
    for d in devices:
        print(f"Found: {d}")
        if d.name and "ATC_11F242" in d.name:
            target_device = d
            break
    
    if not target_device:
        print("Target device not found")
        return
    
    print(f"\nFound target device: {target_device}")
    
    # Try both the address and the BleakDevice object
    connection_methods = [
        target_device.address,  # First try with address
        target_device  # Then try with the device object itself
    ]
    
    for method in connection_methods:
        try:
            print(f"\nAttempting to connect using {method}...")
            async with BleakClient(method) as client:
                print(f"Successfully connected to {target_device.name}!")
                print("Connection status:", client.is_connected)
                
                # Get services
                services = await client.get_services()
                print("\nServices:")
                for service in services:
                    print(service)
                
                # Add your device-specific communication here
                
                return  # Success - exit the function
                
        except BleakError as e:
            print(f"Connection failed: {e}")
            continue
    
    print("All connection attempts failed")

if __name__ == "__main__":
    asyncio.run(run())