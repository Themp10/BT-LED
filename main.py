import time

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bledom import BleLedDevice, run_sync,Effects
import asyncio
import pyautogui
from PIL import ImageGrab
import numpy as np
from sklearn.cluster import KMeans


def get_dominant_color(image, n_colors=1):
    image_array = np.array(image)
    pixels = image_array.reshape((-1, 3))
    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return tuple(dominant_colors[0])

def screenshot_and_get_dominant_color():
    downScale=8
    TVSize=(3840,2160)
    PCSize=(2560,1440)
    region=(0, 0, TVSize[0], TVSize[1])
    my_screenshot = ImageGrab.grab(bbox=region)
    my_screenshot.thumbnail((my_screenshot.width // downScale, my_screenshot.height // downScale))
    #my_screenshot.save(r'B:\Projects\Python\BT LED\sss.png')
    dominant_color = get_dominant_color(my_screenshot)
    return dominant_color



async def default_callable(device: BleLedDevice):
    device.set_brightness(100)
    a=0
    while True:
        colors=screenshot_and_get_dominant_color()

        a+=1
        time.sleep(0.5)
        await device.set_color(colors[0],colors[1],colors[2])
        print(a,colors)

        
async def main(func: callable):
    devices = await BleakScanner.discover()
    target_device_name = "ELK-BLEDOB"

    for device in devices:
        if device.name == target_device_name:
            print("Connecting to %s (%s)..." % (device.name, device.address))
            client = BleakClient(device)
            await client.connect()
    try:
        connected_device = await BleLedDevice.new(client)
        await func(connected_device)
    finally:
        # disconnect when we finish
        await client.disconnect()

def run_sync(func: callable = default_callable):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(func))

if __name__ == "__main__":
    run_sync()