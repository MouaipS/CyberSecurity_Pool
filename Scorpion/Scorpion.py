import argparse
import os
from datetime import datetime
from PIL import Image, ExifTags


VALID_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="images")
    return parser.parse_args()


def is_valid_extension(filepath: str) -> bool:
    return filepath.lower().endswith(VALID_EXT)


def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def display_image_data(image: Image.Image) -> None:
    print(f"Format        : {image.format}")
    print(f"Mode          : {image.mode}")
    print(f"Size : { image.size}")
    print(f"Palette : {image.palette}")


def display_image_exif(image: Image.Image) -> None:
    exif_data = image.getexif()
    if not exif_data:
        print("No EXIF metadata found")
        return
    data = {}
    for k, v in exif_data.items():
        tag = ExifTags.TAGS.get(k, k)
        if isinstance(v, bytes):
            v = v.decode(errors="replace")
        data[tag] = v

    gps_info = exif_data.get_ifd(ExifTags.IFD.GPSInfo)
    if gps_info:
        gps_data = {}
        for tag_id, value in gps_info.items():
            balise = ExifTags.GPSTAGS.get(tag_id, tag_id)
            gps_data[balise] = value
        data["GPSInfo"] = gps_data

    exif_ifd = exif_data.get_ifd(ExifTags.IFD.Exif)
    if exif_ifd:
        exif_detail = {}
        for tag_id, value in exif_ifd.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            if isinstance(value, bytes):
                value = value.decode(errors="replace")
            exif_detail[tag] = value
        data["ExifDetail"] = exif_detail

    print("====================== EXIF metadata =========================")
    for k, v in data.items():
        if k in ("GPSInfo", "ExifDetail"):
            print(f" {k} :")
            for sub_tag, sub_value in v.items():
                print(f"   {sub_tag:<20}: {sub_value}")
            continue
        print(f" {k:<20}: {v}")


def display_metadata(filepath: str):
    print(f"======================{filepath}=========================")
    stat = os.stat(filepath)
    print(f"File name : {os.path.basename(filepath)}")    
    print(f"File size : {stat.st_size} bytes")
    print(f"Last modified : {format_timestamp(stat.st_mtime)}")
    print(f"Last changed  : {format_timestamp(stat.st_ctime)}")
    try:
        with Image.open(filepath) as image:
            display_image_data(image)
            display_image_exif(image)
    except OSError as e:
        print(f"Error: {e}")


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
