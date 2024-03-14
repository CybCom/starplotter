import time

import cv2
import dxcam

frame_stack = []


def capture(capture_region):
    # set the buffer size to 1 to prevent reading old frames
    camera = dxcam.create()
    camera.start(region=capture_region, target_fps=35)
    for i in range(10):
        image = camera.get_latest_frame()  # Waits for a new frame
        frame_stack.append({"img": image, "timestamp": time.time()})
    camera.stop()
    del camera


def split_img(value_coordinate_map):

    for i in range(10):
        if len(frame_stack) > 0:
            print("Captured")
            frame = frame_stack.pop()
            img = frame["img"]
            x, y, w, h = value_coordinate_map["speed"]
            cropped_img = img[y:y + h, x:x + w]
            cv2.imshow("cropped", cropped_img)
            cv2.waitKey(100)
            print("Got frame at", frame["timestamp"])


cap_region = (50, 840, 50 + 1160, 840 + 100)
vcm = {"speed": (0, 0, 100, 100)}

if __name__ == "__main__":
    capture(cap_region)
    split_img(vcm)
