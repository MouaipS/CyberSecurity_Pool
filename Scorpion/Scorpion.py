import argparse
import os
from datetime import datetime
from PIL import Image


VALID_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="images")
    return parser.parse_args()


def is_valid_extension(filepath: str) -> bool:
    return filepath.lower().endswith(VALID_EXT)


def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def display_image_data(image: Image.Image)-> None:
    print(f"Format        : {image.format}")
    print(f"Mode          : {image.mode}")
    print(f"Dimensions    : {image.width}x{image.height}")


def display_metadata(filepath: str):
    print(f"======================{filepath}=========================")
    stat = os.stat(filepath)
    print(f"File name : {os.path.basename(filepath)}")    
    print(f"File size : {stat.st_size} bytes")
    print(f"Last modified : {format_timestamp(stat.st_mtime)}")
    print(f"Last changed  : {format_timestamp(stat.st_ctime)}")
    #try:
    with Image.open(filepath) as image:
        display_image_data(image)
    #except


def scorpion():
    args = parse_args()
    for filepath in args.files:
        if not os.path.isfile(filepath):
            print("f{filepath}: no such file")
            continue
        if not is_valid_extension(filepath):
            print(f"{filepath}: unsupported extension")
            continue
        display_metadata(filepath)

if __name__ == "__main__":
    scorpion()
