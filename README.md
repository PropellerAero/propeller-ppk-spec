# Works with Propeller PPK v0.1

_Works with Propeller PPK_ is a vendor-agnostic format that aircraft vendors can implement for out of the box compatibility with Propeller PPK.

An example data set is available [here](https://drive.google.com/drive/folders/1oYa4CrTnOa-PHhblCbttts_LLamHgDf-?usp=sharing).

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

Images should captured at the native sensor resolution and aspect ratio without any cropping and saved in JPEG format. Images must be at least 12-megapixels.

Images must be named with the flight prefix and a unique (within the flight) 4 digit incrementing number and end in the `.JPG` extension, e.g. `Flight01_0123.JPG`.

Propeller PPK uses the following EXIF headers. Other headers are permitted and will be ignored.

| Field               | Purpose                                                                    |                                                                          |
| ------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `DateTimeOriginal`  | Establishing data set capture time and detecting gaps between images       | Mandatory                                                                |
| `ISO`               | Validating images quality is high enough to produce an accurate survey     | Mandatory                                                                |
| `ImageWidth`        | Validating images are high enough resolution to produce an accurate survey | Mandatory                                                                |
| `ImageHeight`       | Validating images are high enough resolution to produce an accurate survey | Mandatory                                                                |
| `Model`             | Optimising photogrammetry camera parameters to produce an accurate survey  | Mandatory                                                                |
| `GPSLongitude`      | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| `GPSLongitudeRef`   | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| `GPSLatitude`       | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| `GPSLatitudeRef`    | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| `GPSAltitude`       | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| `GPSAltitudeRef`    | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata.json file |
| `LensModel`         | Optimising photogrammetry parameters to produce an accurate survey         | _Optional_                                                               |
| `ShutterSpeedValue` | Detecting motion blur in combination with speed derived from position      | _Optional_                                                               |

### Image requirements

Propeller PPK will validate that each flight directory uploaded meets the following requirements

| Field                                   | Description                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------- |
| File name                               | Must be <255 characters long                                                          |
| File name                               | Must match `:flightPrefix:_:sequentialNumber:.JPG` format                             |
| File name                               | Must match an entry in the metadata.csv file                                          |
| `DateTimeOriginal` EXIF field           | Must be present                                                                       |
| `DateTimeOriginal` EXIF field           | Must be an ASCII date string of format `YYYY:MM:DD HH:MM:SS`                          |
| `ISO` EXIF field                        | Must be present                                                                       |
| `ISO` EXIF field                        | Must be EXIF unsigned int format                                                      |
| `ISO` EXIF field                        | Must be < `1600` (recommended maximum `400`)                                          |
| `ImageWidth` EXIF field                 | Must be present                                                                       |
| `ImageWidth` EXIF field                 | Must be unsigned short/long field                                                     |
| `ImageHeight` EXIF field                | Must be present                                                                       |
| `ImageHeight` EXIF field                | Must be unsigned short/long field                                                     |
| `ImageWidth`, `ImageHeight` EXIF fields | Image size (ImageWidth x ImageHeight) must be at least 12 megapixels                  |
| `Model` EXIF field                      | Must be an ASCII string identifying the camera model                                  |
| `GPSLongitude` EXIF field               | Must be present unless approximate position provided in the metadata.json file        |
| `GPSLongitude` EXIF field               | Must be EXIF rational64u format                                                       |
| `GPSLongitudeRef` EXIF field            | Must be present unless approximate position provided in the metadata.json file        |
| `GPSLongitudeRef` EXIF field            | Must be the string 'E' or 'W' to denote the east or west hemisphere                   |
| `GPSLatitude` EXIF field                | Must be present unless approximate position provided in the metadata.json file        |
| `GPSLatitude` EXIF field                | Must be EXIF rational64u format                                                       |
| `GPSLatitudeRef` EXIF field             | Must be present unless approximate position provided in the metadata.json file        |
| `GPSLatitudeRef` EXIF field             | Must be the string 'N' or 'S' to denote the north or south hemisphere                 |
| `GPSAltitude` EXIF field                | Must be present unless approximate position provided in the metadata.json file        |
| `GPSAltitude` EXIF field                | Must be EXIF rational64u format                                                       |
| `GPSAltitudeRef` EXIF field             | Must be present unless approximate position provided in the metadata.json file        |
| `GPSAltitudeRef` EXIF field             | Must be the 8-bit unsigned integer `0` for above sea level or `1` for below sea level |
| `LensModel` EXIF field                  | Must be an ASCII string identifying the lens model if present                         |
| `ShutterSpeedValue` EXIF field          | Must be EXIF rational64s format if present                                            |

## GNSS observations

GNSS observation data for each flight must be stored in RINEX version 3.04 format. The GNSS observations must:

- Cover the period from aircraft take off to landing
- Have no gaps between epochs of > 1 second
- Have a constant sample rate of 1 - 20 Hz
- Include signals for:
  - GPS L1
  - GPS L2
  - GLONASS L1
  - GLONASS L2
  - Galileo E1
  - Galileo E5

Other signals can be included and may be used in future and will be ignored otherwise.

To ensure accurate GNSS solutions, every epoch must contain at least 16 GPS, GLONASS and Galileo satellites with dual-band measurements both with a signal-to-noise ratio (SNR) of > 35. An initialisation window of up to 60 seconds at the beginning of the file that does not meet these requirements is acceptable.

### RINEX headers

Propeller PPK uses the following RINEX headers. Other headers allowed by the RINEX specification are permitted and will be ignored.

| Header field         | Purpose                                               |           |
| -------------------- | ----------------------------------------------------- | --------- |
| RINEX VERSION / TYPE | Validating RINEX version is correct                   | Mandatory |
| APPROX POSITION XYZ  | Verifying that the flight is with the site boundary   | Mandatory |
| SYS / # / OBS TYPES  | Mapping observations to signals during PPK processing | Mandatory |
| TIME OF FIRST OBS    | Verifying RINEX file overlaps survey time range       | Mandatory |
| SYS / PHASE SHIFT    | Mapping observations to signals during PPK processing | Mandatory |
| GLONASS SLOT / FRQ # | Input to PPK processing                               | Mandatory |
| GLONASS COD/PHS/BIS  | Input to PPK processing                               | Mandatory |
| END OF HEADER        | Denotes end of header                                 | Mandatory |

### RINEX requirements

Propeller PPK will validate that each RINEX file uploaded meets the following requirements

| Field                         | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
| File name                     | Must be <255 characters long                                                |
| File name                     | Must match `:flightPrefix:_GNSS.obs` format                                 |
| `RINEX VERSION / TYPE` header | Must be RINEX version 3.04                                                  |
| `APPROX POSITION XYZ` header  | Must be present and contain the approximate WGS84 coordinates of the flight |
| `SYS / # / OBS TYPES` header  | Must be present and valid RINEX format                                      |
| `TIME OF FIRST OBS` header    | Must be present and valid RINEX format                                      |
| `SYS / PHASE SHIFT` header    | Must be present and valid RINEX format                                      |
| `SYS / PHASE SHIFT` header    | Must contain `G L1C` signal                                                 |
| `SYS / PHASE SHIFT` header    | Must contain `G L2W` signal                                                 |
| `SYS / PHASE SHIFT` header    | Must contain `R L1C` signal                                                 |
| `SYS / PHASE SHIFT` header    | Must contain `R L2P` signal                                                 |
| `SYS / PHASE SHIFT` header    | Must contain `E L1B` signal                                                 |
| `SYS / PHASE SHIFT` header    | Must contain `E L7Q` signal                                                 |
| `GLONASS SLOT / FRQ #` header | Must be present and valid RINEX format                                      |
| `GLONASS COD/PHS/BIS` header  | Must be present and valid RINEX format                                      |
| First epoch timestamp         | Must be before timestamp of first image in metadata.json file               |
| Last epoch timestamp          | Must be after timestamp of last image in metadata.json file                 |
| Sample rate                   | Must be 1 - 20 Hz, (0.05s - 1s interval)                                    |
| All epochs                    | Must be no gaps > 1 second between samples                                  |
| Each epoch                    | Must contain at least 16 satellites with SNR > 35 dBHz on both bands        |
| Each epoch                    | Must contain doppler frequency measurement for each satellite               |
| Each epoch                    | Must contain signal-to-noise (SNR) measurement for each satellite           |

## Flight metadata

The flight metadata file contains additional information required to map each image to a PPK coordinate, as well as some aircraft specific metadata used to validate the uploaded data.

### CSV format

Each flight metadata file must be stored in Microsoft Excel style CSV format with:

- File encoding: `UTF-8`
- Field delimiter: `,`
- Line ending: `\r\n`
- Quote character: `"`
- All string fields may contain up to 255 characters of valid Unicode

### Example metadata file

```
Manufacturer,Propeller
Model,DemoUAV
Serial number,AJ34NF12
Firmware version,1.75.24a_rev2
Propeller PPK version,1.0
Image,Timestamp (s),GPS week number,Antenna offset north (m),Antenna offset east (m),Antenna offset up (m),Roll (degrees),Pitch (degrees),Yaw (degrees),Approximate Longitude (degrees),Approximate Latitude (degrees),Approximate altitude (m)
Flight01_0001.JPG,105277.650307,2192,0.025,-0.030,0.190,0.00,-90.00,94.20,146.64916670,-35.85037326,280.124
Flight01_0002.JPG,105281.932945,2192,0.011,-0.018,0.193,0.00,-90.00,98.70,146.64947564,-35.85041480,280.044
Flight01_0003.JPG,105284.443190,2192,0.004,-0.003,0.195,0.00,-90.00,98.70,146.64975396,-35.85045122,280.071
...
```

The file is comprised of:

1. A header section, containing flight / aircraft specific information
2. A body containing image specific information

### Header fields

| Header                  | Purpose                                                                                                  |           |
| ----------------------- | -------------------------------------------------------------------------------------------------------- | --------- |
| `Manufacturer`          | Unique string that identifies your organisation (e.g. `Propeller`)                                       | Mandatory |
| `Model`                 | Unique string that identifies the model of aircraft (e.g. `DroneOne`)                                    | Mandatory |
| `Serial number`         | Identifies the specific aircraft (e.g. `AJ34NF12`)                                                       | Mandatory |
| `Firmware version`      | Identifies the aircraft firmware version, used by Propeller support to identify firmware specific issues | Mandatory |
| `Propeller PPK version` | Identifies the version of the Propeller PPK format generated, currently always set to `1.0`              | Mandatory |

### Body header row

The body section must start with the static header row

```
Image,Timestamp (s),GPS week number,Antenna offset north (m),Antenna offset east (m),Antenna offset up (m),Roll (degrees),Pitch (degrees),Yaw (degrees),Approximate longitude (degrees),Approximate latitude (degrees),Approximate altitude (m)
```

This is used to delimit the header and body sections and give human-readable context.

### Body fields

The body section must contain one entry for every image captured.

| Field                             | Description                                                              | Unit    | Format                                        | Example value       |                                                                                                    |
| --------------------------------- | ------------------------------------------------------------------------ | ------- | --------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------- |
| `Image`                           | File name for corresponding image                                        |         | String matching file name                     | `Flight01_0001.JPG` | Mandatory                                                                                          |
| `Timestamp (s)`                   | Precise image timestamp measured since start of GPS week                 | Seconds | Fixed precision decimal with 6 decimal places | `105277.650307`     | Mandatory                                                                                          |
| `GPS week number`                 | GPS week number for precise timestamp                                    |         | Positive integer decimal                      | `2192`              | Mandatory                                                                                          |
| `Antenna offset north (m)`        | North component of offset from image focal plane to antenna phase center | Meters  | Fixed precision decimal with 3 decimal places | `0.025`             | Mandatory                                                                                          |
| `Antenna offset east (m)`         | East component of offset from image focal plane to antenna phase center  | Meters  | Fixed precision decimal with 3 decimal places | `-0.030`            | Mandatory                                                                                          |
| `Antenna offset up (m)`           | Up component of offset from image focal plane to antenna phase center    | Meters  | Fixed precision decimal with 3 decimal places | `0.190`             | Mandatory                                                                                          |
| `Roll (degrees)`                  | Aircraft RPY convention roll component                                   | Degrees | Fixed precision decimal with 2 decimal places | `0.13`              | _Optional_ - Not used in GNSS processing, but may be used in photogrammetry processing if present. |
| `Pitch (degrees)`                 | Aircraft RPY convention pitch component                                  | Degrees | Fixed precision decimal with 2 decimal places | `-90.00`            | _Optional_ - Not used in GNSS processing, but may be used in photogrammetry processing if present. |
| `Yaw (degrees)`                   | Aircraft RPY convention yaw component                                    | Degrees | Fixed precision decimal with 2 decimal places | `94.20`             | _Optional_ - Not used in GNSS processing, but may be used in photogrammetry processing if present. |
| `Approximate longitude (degrees)` | Longitude component of coarse GNSS coordinates for image                 | Degrees | Fixed precision decimal with 8 decimal places | `146.64916670`      | Mandatory unless `GPSLongitude` / `GPSLongitudeRef` Image EXIF headers provided                    |
| `Approximate latitude (degrees)`  | Latitude component of coarse GNSS coordinates for image                  | Degrees | Fixed precision decimal with 8 decimal places | `-35.85037326`      | Mandatory unless `GPSLatitude` / `GPSLatitudeRef` Image EXIF headers provided                      |
| `Approximate altitude (m)`        | Altitude component of coarse GNSS coordinates for image                  | Meters  | Fixed precision decimal with 3 decimal places | `280.124`           | Mandatory unless `GPSAltitude` / `GPSAltitudeRef` Image EXIF headers provided                      |

### Antenna offset conventions

The image focal plane to GNSS antenna offset components are measured relative to the global ENU coordinate frame where:

- `Antenna offset north (m)` is positive when the GNSS antenna is more north than the image focal plane
- `Antenna offset east (m)` is positive when the GNSS antenna is more east than the image focal plane
- `Antenna offset up (m)` is positive when the GNSS antenna is above the image focal plane

The GNSS antenna to image focal plane offset north / east / up components should be calculated using a lever-arm given the aircraft's geometry and roll / pitch / yaw values for each image.

If this is not possible and roll / pitch values are typically small (< 5 degrees) and the image sensor is mounted directly below the GNSS antenna a constant vertical offset may be supplied in the `Antenna offset up (m)` field.

### Metadata file requirements

Propeller PPK will validate that each RINEX file uploaded meets the following requirements

| Field                                                     | Description                                                                                                                                                                                                                                                          |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| File name                                                 | Must be <255 characters long                                                                                                                                                                                                                                         |
| File name                                                 | Must match `:flightPrefix:_metadata.csv` format                                                                                                                                                                                                                      |
| `Manufacturer` header field                               | Must be present                                                                                                                                                                                                                                                      |
| `Manufacturer` header field                               | Must be <255 character long Unicode string                                                                                                                                                                                                                           |
| `Model` header field                                      | Must be present                                                                                                                                                                                                                                                      |
| `Model` header field                                      | Must be <255 character long Unicode string                                                                                                                                                                                                                           |
| `Serial number` header field                              | Must be present                                                                                                                                                                                                                                                      |
| `Serial number` header field                              | Must be <255 character long Unicode string                                                                                                                                                                                                                           |
| `Firmware version` header field                           | Must be present                                                                                                                                                                                                                                                      |
| `Firmware version` header field                           | Must be <255 character long Unicode string                                                                                                                                                                                                                           |
| `Propeller PPK version` header field                      | Must be present                                                                                                                                                                                                                                                      |
| `Propeller PPK version` header field                      | Must be the string `1.0`                                                                                                                                                                                                                                             |
| Body header row                                           | Must be present                                                                                                                                                                                                                                                      |
| Body header row                                           | Must be the string `Image,Timestamp (s),GPS week number,Antenna offset north (m),Antenna offset east (m),Antenna offset up (m),Roll (degrees),Pitch (degrees),Yaw (degrees),Approximate Longitude (degrees),Approximate Latitude (degrees),Approximate altitude (m)` |
| `Image` field                                             | Must match the file name of an uploaded image                                                                                                                                                                                                                        |
| `Timestamp (s)` field                                     | Must be a 6 decimal place fixed precision decimal                                                                                                                                                                                                                    |
| `Timestamp (s)` field                                     | Must be between `0` and `604800.999999`                                                                                                                                                                                                                              |
| `GPS week number` field                                   | Must be a positive integer                                                                                                                                                                                                                                           |
| Composite timestamp (`Timestamp (s)` + `GPS week number`) | Must be after first epoch in RINEX file                                                                                                                                                                                                                              |
| Composite timestamp (`Timestamp (s)` + `GPS week number`) | Must be before last epoch in RINEX file                                                                                                                                                                                                                              |
| `Antenna offset north (m)` field                          | Must be a 3 decimal place fixed precision decimal                                                                                                                                                                                                                    |
| `Antenna offset east (m)` field                           | Must be a 3 decimal place fixed precision decimal                                                                                                                                                                                                                    |
| `Antenna offset up (m)` field                             | Must be a 3 decimal place fixed precision decimal                                                                                                                                                                                                                    |
| Antenna offset fields                                     | Vector offset (square-root of sum of squares of offset components) must not be `0`                                                                                                                                                                                   |
| `Roll (degrees)` field                                    | Must be a 2 decimal place fixed precision decimal if present                                                                                                                                                                                                         |
| `Pitch (degrees)` field                                   | Must be a 2 decimal place fixed precision decimal if present                                                                                                                                                                                                         |
| `Yaw (degrees)` field                                     | Must be a 2 decimal place fixed precision decimal if present                                                                                                                                                                                                         |
| `Approximate longitude (degrees)` field                   | Must be present if `GPSLongitude` / `GPSLongitudeRef` image EXIF headers are not provided                                                                                                                                                                            |
| `Approximate longitude (degrees)` field                   | Must be an 8 decimal place fixed precision decimal if present                                                                                                                                                                                                        |
| `Approximate latitude (degrees)` field                    | Must be present if `GPSLatitude` / `GPSLatitudeRef` image EXIF headers are not provided                                                                                                                                                                              |
| `Approximate latitude (degrees)` field                    | Must be an 8 decimal place fixed precision decimal if present                                                                                                                                                                                                        |
| `Approximate altitude (degrees)` field                    | Must be present if `GPSAltitude` / `GPSAltitudeRef` image EXIF headers are not provided                                                                                                                                                                              |
| `Approximate altitude (degrees)` field                    | Must be a 3 decimal place fixed precision decimal if present                                                                                                                                                                                                         |
