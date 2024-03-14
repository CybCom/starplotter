import threading
from typing import Tuple, Dict

import PIL.ImageShow
import cv2
from PIL import Image

from capturer import capture

# from ocr import ocr
# from plotter import plot

Region = Tuple[int, int, int, int]  # (x, y, w, h)
ValueCoordinateMapping = Dict[str, Region]  # {"speed": (x, y, w, h), "rpm": (x, y, w, h)}...


def on_get_split_frame(cropped_img, timestamp):
    Image.fromarray(cropped_img["time"]).show()


def main():
    cap_region = (210, 1090, 1000, 90)
    vcm = {"speed_booster": (170, 10, 55, 20),
           "altitude_booster": (170, 25, 55, 20),
           "speed_ship": (793, 10, 55, 20),
           "altitude_ship": (793, 25, 55, 20),
           "time": (455, 25, 100, 30),
           }
    capture.capture(cap_region)
    capture.split_img(vcm)


if __name__ == "__main__":
    main()
