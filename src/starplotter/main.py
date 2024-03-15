import queue
from threading import Thread
from typing import Tuple, Dict

import dxcam
from matplotlib import pyplot as plt

from src.starplotter import capture
import ocr

Region = Tuple[int, int, int, int]  # (x, y, w, h)
ValueCoordinateMapping = Dict[str, Region]  # {"speed": (x, y, w, h), "rpm": (x, y, w, h)}...

stack_frames = queue.LifoQueue()
stack_split_images = queue.LifoQueue()
stack_ocr_data = queue.LifoQueue()


def on_get_frame(frame, timestamp):
    # print("Got frame")
    stack_frames.put({"frame": frame, "timestamp": timestamp})


def on_split_complete():
    # print("Split complete")
    return stack_frames.get()


def on_get_split_images(split_images, timestamp):
    # print("Got split images")
    stack_split_images.put({"images": split_images, "timestamp": timestamp})


name_to_type = {"speed_booster": "int", "altitude_booster": "int", "speed_ship": "int", "altitude_ship": "int",
                "time": "time"}


def on_ocr_complete():
    # print("OCR complete")
    return stack_split_images.get()


def on_get_ocr_data(data, timestamp):
    print("Got OCR data")
    print(data)
    stack_ocr_data.put({"data": data, "timestamp": timestamp})


def on_plot_complete():
    print("Plot complete")
    return stack_ocr_data.get()


def plot_data(data, timestamp):
    print("Plotting data")
    print(data)
    print(timestamp)
    print("Main loop")

    speed_booster.append(data["speed_booster"])
    speed_ship.append(data["speed_ship"])
    altitude_booster.append(data["altitude_booster"])
    altitude_ship.append(data["altitude_ship"])
    str_time = data["time"][1:]
    print(str_time)
    int_time = int(str_time.split(":")[0]) * 3600 + int(str_time.split(":")[1]) * 60 + int(str_time.split(":")[2])
    if data["time"][0] == "-":
        int_time = -int_time
    t.append(int_time)

    ship.cla()
    booster.cla()
    ship.plot(t, speed_ship, 'r', lw=1)
    ship.plot(t, altitude_ship, 'b', lw=1)
    booster.plot(t, speed_booster, 'r', lw=1)
    booster.plot(t, altitude_booster, 'b', lw=1)
    print(t, speed_ship, altitude_ship, speed_booster, altitude_booster)
    plt.pause(0.1)


if __name__ == "__main__":
    cap_region = (210, 1090, 1000, 90)
    vcm = {"speed_booster": (170, 10, 55, 20),
           "altitude_booster": (170, 25, 55, 20),
           "speed_ship": (793, 10, 55, 20),
           "altitude_ship": (793, 25, 55, 20),
           "time": (455, 25, 100, 30),
           }
    # No need to set the buffer size to 1 to prevent reading old frames, because it "won't pop the processed frame
    # from the buffer. "
    camera = dxcam.create()
    camera.start(region=(cap_region[0], cap_region[1], cap_region[2] + cap_region[0],
                         cap_region[3] + cap_region[1]), target_fps=35)

    thread1 = Thread(target=capture.thread_grab, args=(camera,))
    thread2 = Thread(target=capture.thread_split_images, args=(vcm,))
    thread3 = Thread(target=ocr.thread_ocr, args=(name_to_type,))
    thread1.start()
    thread2.start()
    thread3.start()
    fig, (ship, booster) = plt.subplots(2, 1)
    t = []
    speed_booster = []
    speed_ship = []
    altitude_booster = []
    altitude_ship = []


    # while True:
    #     print("Main loop")
    #     data = stack_ocr_data.get()
    #     plot_data(data, data["timestamp"])
    thread1.join()
    thread2.join()
    thread3.join()
    print("Main loop")

    while True:
        print("Main loop")
        data = on_plot_complete()
        plot_data(data["data"], data["timestamp"])
