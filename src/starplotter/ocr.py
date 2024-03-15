import pytesseract
from src.starplotter import main


def ocr_integer(image):
    value = pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=0123456789")
    if value == "":
        return 0
    return int(pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=0123456789"))


def ocr_time(image):
    return pytesseract.image_to_string(image)


def thread_ocr(name_to_type: dict):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    while True:
        split_images = main.on_ocr_complete()
        data = {}
        for key, value in split_images["images"].items():
            if name_to_type[key] == "int":
                data[key] = ocr_integer(value)
            elif name_to_type[key] == "time":
                data[key] = ocr_time(value)
            else:
                print("Unknown type")
        main.on_get_ocr_data(data, split_images["timestamp"])
