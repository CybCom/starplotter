import time
import dxcam

import main
from main import ValueCoordinateMapping


def thread_grab(camera: dxcam):
    while True:
        image = camera.get_latest_frame()  # Waits for a new frame
        main.on_get_frame(image, time.time())


def thread_split_images(value_coordinate_map: ValueCoordinateMapping):
    for i in range(1):
        while True:
            frame = main.on_split_complete()
            full_img = frame["frame"]
            split_images = {}
            for key, value in value_coordinate_map.items():
                x, y, w, h = value
                split_images[key] = full_img[y:y + h, x:x + w]
            main.on_get_split_images(split_images, frame["timestamp"])


if __name__ == "__main__":
    cap_region = (50, 840, 1160, 100)
    vcm = {"speed": (0, 0, 100, 100), "rpm": (0, 0, 100, 100)}
    thread_grab(cap_region)
    thread_split_images(vcm)
