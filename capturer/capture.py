import time
import dxcam
from PIL import Image

from controller import main
from controller.main import Region, ValueCoordinateMapping

frame_stack = []


def capture(capture_region: Region):
    # No need to set the buffer size to 1 to prevent reading old frames, because it "won't pop the processed frame
    # from the buffer. "
    camera = dxcam.create()
    camera.start(region=(capture_region[0], capture_region[1], capture_region[2] + capture_region[0],
                         capture_region[3] + capture_region[1]), target_fps=35)
    for i in range(1):
        image = camera.get_latest_frame()  # Waits for a new frame
        frame_stack.append({"img": image, "timestamp": time.time()})
    camera.stop()
    del camera


def split_img(value_coordinate_map: ValueCoordinateMapping):
    for i in range(1):
        if len(frame_stack) > 0:
            frame = frame_stack.pop()
            full_img = frame["img"]
            cropped_img = {}
            for key, value in value_coordinate_map.items():
                x, y, w, h = value
                cropped_img[key] = full_img[y:y + h, x:x + w]
            main.on_get_split_frame(cropped_img, frame["timestamp"])


if __name__ == "__main__":
    cap_region = (50, 840, 1160, 100)
    vcm = {"speed": (0, 0, 100, 100), "rpm": (0, 0, 100, 100)}
    capture(cap_region)
    split_img(vcm)
