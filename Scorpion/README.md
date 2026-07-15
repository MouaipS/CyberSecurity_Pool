# Exercice II - Scorpion

The scorpion programm allow you to extract the metadata (file information and EXIF data) from one or several images, by providing them as parameters.

### How to use it :

```
./Scorpion FILE1 [FILE2 ...]
```

The programm accepts the following extensions:
- .jpg/.jpeg
- .png
- .gif
- .bmp

### How the program works ?

###### First step : checking the files

For each file given as a parameter, we first check with `os.path.isfile` that it actually exists, then check its extension against the list of valid ones. Any file that fails one of these checks is reported and skipped, without stopping the processing of the remaining files.

###### Second step : file information

"display_metadata" uses `os.stat` to retrieve the file's information : size in bytes, last modification date and last change date. Timestamps are formatted into a readable `YYYY-MM-DD HH:MM:SS` string with "format_timestamp".

###### Third step : image data

The file is opened with Pillow's `Image.open`. "display_image_data" then prints its format (JPEG, PNG, ...), its mode (RGB, RGBA, ...), its size (width x height) and its palette.

###### Fourth step : EXIF metadata

"display_image_exif" reads the image's EXIF data with `getexif()`. Each tag id is translated into its human-readable name with `ExifTags.TAGS`. GPS information (`IFD.GPSInfo`) and detailed EXIF information (`IFD.Exif`) are extracted separately from the main EXIF dict, and their own tag ids are translated with `ExifTags.GPSTAGS`/`ExifTags.TAGS`, then displayed as nested sub-sections. If the image has no EXIF data at all, a message is printed instead.

### Error handling

- A missing file or an unsupported extension is reported and the programm moves on to the next file instead of crashing.
- Errors raised by Pillow while opening or reading a corrupted/invalid image (`OSError`) are caught and printed, without stopping the processing of the remaining files.
