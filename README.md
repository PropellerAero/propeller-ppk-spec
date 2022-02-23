# Works with Propeller PPK v1.0

_Works with Propeller PPK_ is a vendor-agnostic format that aircraft vendors can implement for out of the box compatibility with Propeller PPK.

<!-- TODO - link -->

An example data set is available here.

## File structure

Captured data is stored into one directory per flight. Each flight directory contains:

- 1 JPEG file for each image captured
- 1 RINEX format GNSS observation file covering the full period from takeoff to landing
- 1 flight metadata CSV file containing GNSS timestamps and additional metadata for each image

Each file in the flight directory is prefixed with the flight directory name so the mapping is not lost if flight folders are merged. This prefix can be any string, but we suggest a sequential ordering.

### File structure requirements

Propeller PPK will validate that each flight directory uploaded meets the following requirements

| Field                          | Description                                          |
| ------------------------------ | ---------------------------------------------------- |
| Flight directory name / prefix | Must be unique for an uploaded collection of flights |
| Flight directory name / prefix | Must be <255 characters long                         |
| Flight directory               | Must contain at least 1 JPEG image                   |
| Flight directory               | Must contain 1 GNSS.obs RINEX file                   |
| Flight directory               | Must contain 1 metadata.csv metadata file            |

### Example directory structure

```
Flights/
    Flight01/
        Flight01_0001.JPG
        Flight01_0002.JPG
        Flight01_0003.JPG
        ...
        Flight01_GNSS.obs
        Flight01_metadata.csv
    Flight02/
        Flight02_0001.JPG
        Flight02_0002.JPG
        Flight02_0003.JPG
        ...
        Flight02_GNSS.obs
        Flight02_metadata.csv
    Flight03/
        Flight03_0001.JPG
        Flight03_0002.JPG
        Flight03_0003.JPG
        ...
        Flight03_GNSS.obs
        Flight03_metadata.csv
```

## Images

Images should captured at the native sensor resolution and aspect ratio without any cropping and saved in JPEG format.

Images must be at least 12-megapixels

Images must be named with the flight prefix and a unique (within the flight) 4 digit incrementing number and end in the `.JPG` extension, e.g. `Flight01_0123.JPG`.

Propeller PPK uses the following EXIF / XMP headers. Other headers are permitted and will be ignored.

| Type | Field             | Purpose                                                                    |                                                                          |
| ---- | ----------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| EXIF | DateTimeOriginal  | Establishing data set capture time and detecting gaps between images       | Mandatory                                                                |
| EXIF | ImageWidth        | Validating images are high enough resolution to produce an accurate survey | Mandatory                                                                |
| EXIF | ImageHeight       | Validating images are high enough resolution to produce an accurate survey | Mandatory                                                                |
| EXIF | Model             | Optimising photogrammetry camera parameters to produce an accurate survey  | Mandatory                                                                |
| EXIF | GPSLongitude      | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| EXIF | GPSLongitudeRef   | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| EXIF | GPSLatitude       | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| EXIF | GPSLatitudeRef    | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| EXIF | GPSAltitude       | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| EXIF | GPSAltitudeRef    | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| EXIF | LensModel         | Optimising photogrammetry parameters to produce an accurate survey         | _Optional_                                                               |
| EXIF | ShutterSpeedValue | Detecting motion blur in combination with flight speed                     | _Optional_                                                               |
| XMP  | FlightXSpeed      | Detecting motion blur in combination with shutter speed                    | _Optional_                                                               |
| XMP  | FlightYSpeed      | Detecting motion blur in combination with shutter speed                    | _Optional_                                                               |

### Image requirements

Propeller PPK will validate that each flight directory uploaded meets the following requirements

| Field                               | Description                                                                           |
| ----------------------------------- | ------------------------------------------------------------------------------------- |
| File name                           | Must be <255 characters long                                                          |
| File name                           | Must match `:flightPrefix:\_:sequentialNumber:.JPG` format                            |
| DateTimeOriginal EXIF field         | Must be present                                                                       |
| DateTimeOriginal EXIF field         | Must be an ASCII date string of format `YYYY:MM:DD HH:MM:SS`                          |
| ImageWidth EXIF field               | Must be present                                                                       |
| ImageWidth EXIF field               | Must be unsigned short/long field                                                     |
| ImageHeight EXIF field              | Must be present                                                                       |
| ImageHeight EXIF field              | Must be unsigned short/long field                                                     |
| ImageWidth, ImageHeight EXIF fields | Image size (ImageWidth x ImageHeight) must be at least 12 megapixels                  |
| Model EXIF field                    | Must be an ASCII string identifying the camera model                                  |
| GPSLongitude EXIF field             | Must be present unless approximate position provided in the metadata.json file        |
| GPSLongitude EXIF field             | Must be EXIF rational64u format                                                       |
| GPSLongitudeRef EXIF field          | Must be present unless approximate position provided in the metadata.json file        |
| GPSLongitudeRef EXIF field          | Must be the string 'E' or 'W' to denote the east or west hemisphere                   |
| GPSLatitude EXIF field              | Must be present unless approximate position provided in the metadata.json file        |
| GPSLatitude EXIF field              | Must be EXIF rational64u format                                                       |
| GPSLatitudeRef EXIF field           | Must be present unless approximate position provided in the metadata.json file        |
| GPSLatitudeRef EXIF field           | Must be the string 'N' or 'S' to denote the north or south hemisphere                 |
| GPSAltitude EXIF field              | Must be present unless approximate position provided in the metadata.json file        |
| GPSAltitude EXIF field              | Must be EXIF rational64u format                                                       |
| GPSAltitudeRef EXIF field           | Must be present unless approximate position provided in the metadata.json file        |
| GPSAltitudeRef EXIF field           | Must be the 8-bit unsigned integer `0` for above sea level or `1` for below sea level |
| LensModel EXIF field                | Must be an ASCII string identifying the lens model if present                         |
| ShutterSpeedValue EXIF field        | Must be EXIF rational64s format if present                                            |
| FlightXSpeed EXIF field             | Must be XMP `real` floating point format if present                                   |
| FlightYSpeed EXIF field             | Must be XMP `real` floating point format if present                                   |

<!-- TODO validate ISO? -->

## GNSS observations

RINEX headers
'RINEX VERSION / TYPE',
'APPROX POSITION XYZ',
'SYS / # / OBS TYPES',
'TIME OF FIRST OBS',
'SYS / PHASE SHIFT',
'GLONASS SLOT / FRQ #',
'GLONASS COD/PHS/BIS',
'END OF HEADER',

## Flight metadata
