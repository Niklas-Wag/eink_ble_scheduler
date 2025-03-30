import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = "3D:6E:57:11:F2:42"
WRITE_CHAR_UUID = "00001337-0000-1000-8000-00805f9b34fb"
NOTIFY_CHAR_UUID = "00001337-0000-1000-8000-00805f9b34fb"

# Notification handler to print received responses
def notification_handler(sender, data):
    print(f"Received response: {data.hex()}")

async def send_to_display():
    try:
        async with BleakClient(DEVICE_ADDRESS, timeout=60) as client:
            print(f"Connected to {DEVICE_ADDRESS}")
            # Enable notifications
            await client.start_notify(NOTIFY_CHAR_UUID, notification_handler)
            print("Notifications enabled - waiting for responses...")

            # Send initialization command as seen in the communication log.
            init_cmd = "0064FF8951ABF0000000008022000020000000"
            await client.write_gatt_char(WRITE_CHAR_UUID, bytes.fromhex(init_cmd), response=True)
            print(f"Sent initialization command: {init_cmd}")
            # Short delay to allow the device to process the initialization
            await asyncio.sleep(1)

            # Prepare image data (replace with your actual image hex data)
            image_hex = "<YOUR_IMAGE_HEX_DATA>"  # update with your actual hex string
            image_hex = image_hex.replace("\n", "").replace(" ", "").replace(",", "")

            # Send image data in chunks (using 480 hex characters per chunk)
            chunk_size = 480
            upload_part = 0
            start_time = asyncio.get_event_loop().time()

            while image_hex:
                chunk = image_hex[:chunk_size]
                image_hex = image_hex[chunk_size:]
                # Prepend the command prefix "03" to the image chunk
                cmd = bytes.fromhex("03" + chunk)
                await client.write_gatt_char(WRITE_CHAR_UUID, cmd, response=False)
                print(f"Sent part {upload_part}, remaining: {len(image_hex)} chars")
                upload_part += 1
                await asyncio.sleep(0.01)

            elapsed_time = asyncio.get_event_loop().time() - start_time
            print(f"Image data sent in {elapsed_time:.2f} seconds")

            # Send block completion command (as indicated by "0002" in the communication)
            complete_cmd = "0002"
            await client.write_gatt_char(WRITE_CHAR_UUID, bytes.fromhex(complete_cmd), response=True)
            print(f"Sent completion command: {complete_cmd}")
            await asyncio.sleep(1)

            # Send display command to trigger image display ("0003")
            display_cmd = "0003"
            await client.write_gatt_char(WRITE_CHAR_UUID, bytes.fromhex(display_cmd), response=True)
            print(f"Sent display command: {display_cmd}")

            # Wait to receive any responses before disconnecting
            await asyncio.sleep(5)
            await client.stop_notify(NOTIFY_CHAR_UUID)

    except Exception as e:
        print(f"Error: {e}")

asyncio.run(send_to_display())
