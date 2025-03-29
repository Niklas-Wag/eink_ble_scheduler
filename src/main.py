import asyncio
import bleak
import binascii
import time

DEVICE_NAME = "ATC_11F242"
SERVICE_UUID = "13187b10-eba9-a3ba-044e-83d3217d9a38"
WRITE_CHARACTERISTIC_UUID = "4b646063-6264-f3a7-8941-e65356ea82fe"

# Example image as hex data (replace with actual data)
IMG_DATA = "0000000007fffffffffffffffffc00000000000007fffffffffffffffffc0000"
CHUNK_SIZE = 240  # Adjust chunk size based on BLE characteristics


def hex_to_bytes(hex_str):
    return binascii.unhexlify(hex_str)


async def send_command(client, command):
    await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, command, response=True)


def chunk_image(img_hex):
    return [img_hex[i:i + CHUNK_SIZE * 2] for i in range(0, len(img_hex), CHUNK_SIZE * 2)]


async def upload_image(client, img_hex):
    img_chunks = chunk_image(img_hex)
    print(f"Sending image in {len(img_chunks)} parts...")

    await send_command(client, hex_to_bytes("0000"))  # Start transmission
    await send_command(client, hex_to_bytes("020000"))  # Prepare image upload

    start_time = time.time()

    for index, chunk in enumerate(img_chunks):
        cmd = "03" + chunk
        await send_command(client, hex_to_bytes(cmd))
        print(f"Sent chunk {index + 1}/{len(img_chunks)}")
        await asyncio.sleep(0.1)

    await send_command(client, hex_to_bytes("01"))  # End transmission

    elapsed_time = time.time() - start_time
    print(f"Upload completed in {elapsed_time:.2f} seconds")


async def main():
    devices = await bleak.BleakScanner.discover()
    target_device = next((d for d in devices if d.name and DEVICE_NAME in d.name), None)

    if not target_device:
        print("Device not found.")
        return

    print(f"Connecting to {target_device.name} ({target_device.address})...")
    async with bleak.BleakClient(target_device.address) as client:
        if not await client.is_connected():
            print("Failed to connect.")
            return

        print("Connected. Uploading image...")
        await upload_image(client, IMG_DATA)
        print("Image upload complete.")


if __name__ == "__main__":
    asyncio.run(main())
