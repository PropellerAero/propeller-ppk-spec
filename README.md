# Works with Propeller PPK v0.1

_Works with Propeller PPK_ is a vendor-agnostic file format specification that aircraft vendors can implement to be compatible with the Propeller PPK geotag and photogrammetry processing platform.

## File structure

Captured data should be split into one directory per flight. Each flight directory should contain:

- 1 JPEG file for each image captured
- 1 RINEX format GNSS observation file covering the full period from takeoff to landing
- 1 flight metadata file containing GNSS timestamps and other metadata for each image

Each file in the flight directory should have its name prefixed with the flight directory name so the mapping is not lost if flight folders are merged.

Requirements

| Field          | Description                                          |
| -------------- | ---------------------------------------------------- |
| Directory name | Must be unique for an uploaded collection of flights |
| Directory name | Must be <255 characters long                         |

Example file structure

```
Flights/

```

## Images

JPEG

Minimum resolution

ISO

All images must be same resolution

| Field          | Description                              |
| -------------- | ---------------------------------------- |
| File name      | Must match :flightPrefix\_:imageName.JPG |
| Directory name | Must be <255 characters long             |

### EXIF headers

| Field     | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |

## GNSS observations

## Flight metadata
