# Works with Propeller PPK v2.0.0

_Works with Propeller PPK_ is a vendor-agnostic format that aircraft vendors can implement for out of the box compatibility with Propeller PPK.

An example data set is available [here](https://drive.google.com/drive/folders/1oYa4CrTnOa-PHhblCbttts_LLamHgDf-?usp=sharing).

## Changelog

### v2.0.0 2025-05-12

- V2 version of specification
    - Add Support for multiple GNSS file types
        - RTCM3
        - SBF
        - UBX
        - RINEX
    - Add Support for multiple metadata file types
        - MRK
        - CSV
    - Add additional fields to requested Image Exif headers
        - CameraSerialNumber
        - SerialNumber
        - ExposureTime
        - Make
    - Add Antenna Calibration to spec 
    - Add FAQ section

### v1.0.1 2024-08-12

- Clarify roll / pitch / yaw coordinate frame

### v1.0.0 2022-02-28

- Initial version of specification

## File structure

Captured data is stored into one directory per flight. Each flight directory contains:

- 1 JPEG file for each image captured
- 1 GNSS observation file covering the full period from takeoff to landing
- 1 flight metadata file containing GNSS timestamps and additional metadata for each image

Each file in the flight directory is prefixed with the flight directory name so the mapping is not lost if flight folders are merged. This prefix can be any string, but we suggest a sequential ordering.

### File structure requirements

Propeller PPK will validate that each flight directory uploaded meets the following requirements

| Field                          | Description                                          |
| ------------------------------ | ---------------------------------------------------- |
| Flight directory name / prefix | Must be unique for an uploaded collection of flights |
| Flight directory name / prefix | Must be <255 characters long                         |
| Flight directory               | Must contain between 1 - 9999 JPEG images            |
| Flight directory               | Must contain 1 GNSS file                             |
| Flight directory               | Must contain 1 metadata file                         |

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

| Field                   | Purpose                                                                    |                                                                                        |
| ----------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `DateTimeOriginal`      | Establishing data set capture time and detecting gaps between images       | Mandatory                                                                              |
| `ISO`                   | Validating images quality is high enough to produce an accurate survey     | Mandatory                                                                              |
| `ImageWidth`            | Validating images are high enough resolution to produce an accurate survey | Mandatory                                                                              |
| `ImageHeight`           | Validating images are high enough resolution to produce an accurate survey | Mandatory                                                                              |
| `Model`                 | Optimising photogrammetry camera parameters to produce an accurate survey  | Mandatory                                                                              |
| `GPSLongitude`          | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata file                    |
| `GPSLongitudeRef`       | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata file                    |
| `GPSLatitude`           | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata file                    |
| `GPSLatitudeRef`        | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata file                    |
| `GPSAltitude`           | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata file                    |
| `GPSAltitudeRef`        | Presenting images on a map during the upload process                       | Mandatory unless approximate position provided in the metadata file                    |
| `CameraSerialNumber`    | Identifies the specific camera that was used to capture images             | Mandatory                                                                              |
| `SerialNumber`          | Identifies the specific drone that was used to capture images              | Mandatory                                                                              |
| `LensModel`             | Optimising photogrammetry parameters to produce an accurate survey         | _Optional_                                                                             |
| `ShutterSpeedValue`     | Detecting motion blur in combination with speed derived from position      | _Optional_                                                                             |
| `ExposureTime`          | Detecting motion blur in combination with speed derived from position      | _Optional_                                                                             |
| `Make`                  | Optimising photogrammetry camera parameters to produce an accurate survey  | _Optional_                                                                             |

### Image requirements

Propeller PPK will validate that each flight directory uploaded meets the following requirements

| Field                                   | Description                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------- |
| File name                               | Must be <255 characters long                                                          |
| File name                               | Must match `:flightPrefix:_:sequentialNumber:.JPG` format                             |
| File name                               | Must match an entry in the metadata file                                              |
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
| `GPSLongitude` EXIF field               | Must be present unless approximate position provided in the metadata file             |
| `GPSLongitude` EXIF field               | Must be EXIF rational64u format                                                       |
| `GPSLongitudeRef` EXIF field            | Must be present unless approximate position provided in the metadata file             |
| `GPSLongitudeRef` EXIF field            | Must be the string 'E' or 'W' to denote the east or west hemisphere                   |
| `GPSLatitude` EXIF field                | Must be present unless approximate position provided in the metadata file             |
| `GPSLatitude` EXIF field                | Must be EXIF rational64u format                                                       |
| `GPSLatitudeRef` EXIF field             | Must be present unless approximate position provided in the metadata file             |
| `GPSLatitudeRef` EXIF field             | Must be the string 'N' or 'S' to denote the north or south hemisphere                 |
| `GPSAltitude` EXIF field                | Must be present unless approximate position provided in the metadata file             |
| `GPSAltitude` EXIF field                | Must be EXIF rational64u format                                                       |
| `GPSAltitudeRef` EXIF field             | Must be present unless approximate position provided in the metadata file             |
| `GPSAltitudeRef` EXIF field             | Must be the 8-bit unsigned integer `0` for above sea level or `1` for below sea level |
| `CameraSerialNumber` EXIF field         | Must be an ASCII string identifying the camera used                                   |
| `SerialNumber` EXIF field               | Must be an ASCII string identifying the drone used                                    |
| `LensModel` EXIF field                  | Must be an ASCII string identifying the lens model if present                         |
| `ShutterSpeedValue` EXIF field          | Must be EXIF rational64s format if present                                            |
| `ExposureTime` EXIF field               | Must be EXIF rational64s format if present                                            |
| `Make`                                  | Must be an ASCII string identifying the manufacturer of the camera if present         |

## GNSS and Metadata requirements

Propeller supports the following combinations of GNSS and Metadata files for each flight.

For multiple flights the same combination of GNSS and Metadata files must be used.
| GNSS File                                       | Metadata File                                                                 |
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| [SBF](#sbf)                                     | [MRK](#mrk-format)                                                            |
| [RTCM3](#rtcm3)                                 | [MRK](#mrk-format)                                                            |
| [UBX](#ubx)                                     | [MRK](#mrk-format)                                                            |
| [RINEX](#rinex)                                 | [MRK](#mrk-format)                                                            |
| [SBF](#sbf)                                     | [CSV](#csv-format)                                                            |
| [RTCM3](#rtcm3)                                 | [CSV](#csv-format)                                                            |
| [UBX](#ubx)                                     | [CSV](#csv-format)                                                            |
| [RINEX](#rinex)                                 | [CSV](#csv-format)                                                            |

Propeller PPK strongly prefers raw GNSS formats - SBF, RTCM3 and UBX - [see the FAQ section for more details](#faq).

## GNSS observations

GNSS observation data for each flight must be stored in a one of the following GNSS formats.
- [RINEX](#rinex)
- [SBF](#sbf)
- [UBX](#ubx)        
- [RTCM3](#rtcm3)

The GNSS observations must:

- Cover the period from aircraft take off to landing
- Have no gaps between epochs of > 1 second
- Have a constant sample rate of 5 - 20 Hz
- Include signals for:
  - GPS L1
  - GPS L2
  - GLONASS L1
  - GLONASS L2
  - Galileo E1
  - Galileo E5

Other signals can be included and may be used in future but will be ignored otherwise.

To ensure accurate GNSS solutions every epoch must contain at least 16 GPS, GLONASS and Galileo satellites. With dual-band measurements with a signal-to-noise ratio (SNR) of > 35 dBHz. It is acceptable to have an initialisation window of up to 60 seconds at the beginning of the file that does not meet these requirements.

GNSS files must contain at least 2 minutes of observations after initialisation when processed using an AeroPoint 2 as the GNSS reference or 10 minutes when processed using the Propeller Corrections Network or an AeroPoint 1.

### GNSS File requirements
Propeller PPK validates that each GNSS file meets the following requirements

| Field                                   | Description                                                                                                                                                                                                                         |
| --------------------------------------- | -------------------------------------------------------------------------------------                                                                                                                                               |
| File name                               | Must be <255 characters long                                                                                                                                                                                                        |
| First epoch timestamp                   | Must be before timestamp of first image in metadata file                                                                                                                                                                            |
| Last epoch timestamp                    | Must be after timestamp of last image in metadata file                                                                                                                                                                              |
| File                                    | Must contain `GPS L1` signal                                                                                                                                                                                                        |
| File                                    | Must contain `GPS L2` signal                                                                                                                                                                                                        |
| File                                    | Must contain `GLONASS L1` signal                                                                                                                                                                                                    |
| File                                    | Must contain `GLONASS L2` signal                                                                                                                                                                                                    |
| File                                    | Must contain `Galileo E1` signal                                                                                                                                                                                                    |
| File                                    | Must contain `Galileo E5` signal                                                                                                                                                                                                    |
| File                                    | Must contain at least 10 minutes of observations                                                                                                                                                                                    |
| Sample rate                             | Must be 5 - 20 Hz, (0.2s - 1s interval)                                                                                                                                                                                             |
| All epochs                              | Must be no gaps > 1 second between samples                                                                                                                                                                                          |
| Each epoch                              | Must contain at least 16 satellites with SNR > 35 dBHz on both bands                                                                                                                                                                |
| Each epoch                              | Must contain signal-to-noise (SNR) measurement for each satellite                                                                                                                                                                   |

## RINEX

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

### Corresponding Navigation file

A corresponding valid RINEX navigation file should be provided in the same flight folder which should contain ephemeris data for the constellations contained in the RINEX file.

This file should be in the `:flightPrefix:_GNSS.nav` format and conform to the RINEX navigation specification.

### RINEX requirements

Propeller PPK will validate that each RINEX file uploaded meets the [GNSS file requirements](#gnss-file-requirements) in addition to the following requirements.

| Field                         | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
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

## SBF

Propeller PPK expects that each SBF (Septentrio Binary Format) file conforms to the SBF specification and therefore each SBF block is valid and not malformed.

Propeller PPK uses the following SBF Message blocks. Additional SBF Messages are permitted but these will be ignored.
    - MeasEpoch
    - Navigation Page Blocks
    - Decoded GPS, GLONASS and Galileo message blocks.

### SBF requirements

Propeller PPK will validate that each SBF file uploaded meets the [GNSS file requirements](#gnss-file-requirements) in addition to the following requirements

| Field                         | Description                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------- |
| File name                     | Must match :flightPrefix:.sbf format                                              |
| File                          | Must conform to the SBF specification                                             |
| File                          | Must contain MeasEpoch blocks                                                     |
| File                          | Must contain Navigation Page Blocks and corresponding decoded message blocks      |

## UBX

Propeller PPK expects that each provided UBX file conforms to the UBX specification and therefore each UBX message is valid and not malformed.

Propeller PPK  uses the following UBX message types. Other message types specified by the UBX specification are allowed but will be ignored. 
- UBX-RXM-RAWX
- UBX-RXM-SFRBX

### UBX requirements

Propeller PPK will validate that each UBX file uploaded meets the [GNSS file requirements](#gnss-file-requirements) in addition to the following requirements

| Field                         | Description                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------- |
| File name                     | Must match :flightPrefix:.ubx format                                              |
| File                          | Must conform to the UBX specification                                             |
| File                          | Must contain UBX-RXM-RAWX blocks                                                  |
| File                          | Must contain UBX-RXM-SFRBX blocks                                                 |

## RTCM3

Propeller PPK expects that each RTCM3 file conforms to the RTCM3 spec and therefore each RTCM3 message is valid and not malformed.

Propeller PPK uses the following RTCM3 message. Additional RTCM3 messages are permitted but these will be ignored.

- GPS MSM5/MSM6/MSM7
- GLONASS MSM5/MSM6/MSM7
- GALILEO MSM5/MSM6/MSM7
- GPS Ephemeris
- GLONASS Ephemeris
- Galileo F/Nav Ephemeris
- Galileo I/Nav Ephemeris

### RTCM3 requirements

Propeller PPK will validate that each RTCM3 file uploaded meets the [GNSS file requirements](#gnss-file-requirements) in addition to the following requirements

| Field                         | Description                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------- |
| File name                     | Must match :flightPrefix:.rtcm3 format                                            |
| File                          | Must conform to the RTCM3 specification                                           |
| File                          | Must contain GPS MSM5/MSM6/MSM7 messages                                          |
| File                          | Must contain GLONASS MSM5/MSM6/MSM7 messages                                      |
| File                          | Must contain GPS Ephemeris messages                                               |


## Flight metadata

The flight metadata file contains additional information required to map each image to a PPK coordinate, as well as some aircraft specific metadata used to validate the uploaded data.

Flight Metadata can be provided in the following formats as long as the corresponding GNSS file conforms to one of the allowed combinations of the [GNSS and Metadata files](#gnss-and-metadata-requirements).

Only one metadata file should be provided per flight (not multiple files with the same metadata)
- [CSV](#csv-format)
- [MRK](#mrk-format)

### CSV format

Each flight metadata file must be stored in Microsoft Excel style CSV format with:

- File encoding: `UTF-8`
- Field delimiter: `,`
- Line ending: `\r\n`
- Quote character: `"`
- All string fields may contain up to 255 characters of valid Unicode

### Example CSV metadata file

```
Manufacturer,Propeller
Model,DemoUAV
Serial number,AJ34NF12
Camera Serial Number,3742BE02
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
| `Camera Serial Number`  | Identifies the specific camera that was used to capture the images                                       | Mandatory |
| `Firmware version`      | Identifies the aircraft firmware version, used by Propeller support to identify firmware specific issues | Mandatory |
| `Propeller PPK version` | Identifies the version of the Propeller PPK format generated                                             | Mandatory |

Headers must be encoded in Microsoft Excel style with:

- Fields containing `,` wrapped in `"` quotes
- `"` characters in fields encoded as `""`

For example the field `a string containing , and "` should be encoded as `"a string containing , and """`

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
| `GPS week number`                 | GPS week number for precise timestamp                                    |         | Positive integer                              | `2192`              | Mandatory                                                                                          |
| `Antenna offset north (m)`        | North component of offset from image focal plane to antenna phase center | Meters  | Fixed precision decimal with 3 decimal places | `0.025`             | Mandatory                                                                                          |
| `Antenna offset east (m)`         | East component of offset from image focal plane to antenna phase center  | Meters  | Fixed precision decimal with 3 decimal places | `-0.030`            | Mandatory                                                                                          |
| `Antenna offset up (m)`           | Up component of offset from image focal plane to antenna phase center    | Meters  | Fixed precision decimal with 3 decimal places | `0.190`             | Mandatory                                                                                          |
| `Roll (degrees)`                  | Camera / gimbal roll component (RPY convention)                          | Degrees | Fixed precision decimal with 2 decimal places | `0.13`              | _Optional_ - Not used in GNSS processing, but may be used in photogrammetry processing if present. |
| `Pitch (degrees)`                 | Camera / gimbal pitch component (RPY convention)                         | Degrees | Fixed precision decimal with 2 decimal places | `-90.00`            | _Optional_ - Not used in GNSS processing, but may be used in photogrammetry processing if present. |
| `Yaw (degrees)`                   | Camera / gimbal yaw component (RPY convention)                           | Degrees | Fixed precision decimal with 2 decimal places | `94.20`             | _Optional_ - Not used in GNSS processing, but may be used in photogrammetry processing if present. |
| `Approximate longitude (degrees)` | Longitude component of coarse GNSS coordinates for image                 | Degrees | Fixed precision decimal with 8 decimal places | `146.64916670`      | Mandatory unless `GPSLongitude` / `GPSLongitudeRef` Image EXIF headers provided                    |
| `Approximate latitude (degrees)`  | Latitude component of coarse GNSS coordinates for image                  | Degrees | Fixed precision decimal with 8 decimal places | `-35.85037326`      | Mandatory unless `GPSLatitude` / `GPSLatitudeRef` Image EXIF headers provided                      |
| `Approximate altitude (m)`        | Altitude component of coarse GNSS coordinates for image                  | Meters  | Fixed precision decimal with 3 decimal places | `280.124`           | Mandatory unless `GPSAltitude` / `GPSAltitudeRef` Image EXIF headers provided                      |

### Antenna offset conventions

The image focal plane to GNSS antenna phase center offset components are measured relative to the global ENU coordinate frame where:

- `Antenna offset north (m)` is positive when the GNSS antenna phase center is more north than the image focal plane
- `Antenna offset east (m)` is positive when the GNSS antenna phase center is more east than the image focal plane
- `Antenna offset up (m)` is positive when the GNSS antenna phase center is above the image focal plane

The GNSS antenna to image focal plane offset north / east / up components should be calculated using a lever-arm given the aircraft's geometry and roll / pitch / yaw values for each image.

If this is not possible and roll / pitch values are typically small (< 5 degrees) and the image sensor is mounted directly below the GNSS antenna a constant vertical offset may be supplied for the `Antenna offset` fields.

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
| `Propeller PPK version` header field                      | Must be <255 character long Unicode string                                                                                                                                                                                                                           |
| Body header row                                           | Must be present                                                                                                                                                                                                                                                      |
| Body header row                                           | Must be the string `Image,Timestamp (s),GPS week number,Antenna offset north (m),Antenna offset east (m),Antenna offset up (m),Roll (degrees),Pitch (degrees),Yaw (degrees),Approximate Longitude (degrees),Approximate Latitude (degrees),Approximate altitude (m)` |
| `Image` field                                             | Must match the file name of an uploaded image                                                                                                                                                                                                                        |
| `Timestamp (s)` field                                     | Must be a 6 decimal place fixed precision decimal                                                                                                                                                                                                                    |
| `Timestamp (s)` field                                     | Must be between `0` and `604799.999999`                                                                                                                                                                                                                              |
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


### MRK format

Each flight MRK metadata file must be stored in the `DJI` format with:

- File encoding: UTF-8
- Field delimiter: Tab
- Line ending: \r\n
- All fields may contain up to 255 characters of valid Unicode unless specified otherwise.


### Example metadata file
```
1 500270.541875 [2282]   -474,N    301,E    275,V 39.89927023,Lat -82.92870067,Lon 319.265,Ellh 1.982041, 1.388574, 3.559854 16,Q
2 500276.211321 [2282]   -472,N    302,E    294,V 39.89911983,Lat -82.92871638,Lon 319.153,Ellh 1.981736, 1.387111, 3.555887 16,Q
3 500280.209048 [2282]   -472,N    302,E    292,V 39.89897340,Lat -82.92873260,Lon 319.181,Ellh 1.982117, 1.386671, 3.550005 16,Q
```

The MRK file must contain one entry for each image, and must not contain duplicate entries or entries without corresponding images.

### MRK fields
The fields in the file should be as follows 

| Column                            | Field                                                                                                                | Description                                                                                                               | Unit               | Format                                        | Example value       |                                                                                                    |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------ | --------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------- |
| 1                                 | `Image sequence`                                                                                                     | Sequence of the images should start at one and increase by one per entry                                                  |                    | Positive integer                              | 1                   | Mandatory                                                                                          |
| 2                                 | `Precise image timestamp`                                                                                            | Precise Second of week of the image timestamp expressed in GPS time format for the UTC timezone                           | Seconds            | Fixed precision decimal with 6 decimal places | 500270.541875       | Mandatory                                                                                          |
| 3                                 | `GPS week number`                                                                                                    | GPS week number for precise timestamp in the UTC timezone -  Must be wrapped in `[]`                                      |                    | Positive integer                              | [2282]              | Mandatory                                                                                          |
| 4                                 | `North Antenna Phase Offset`                                                                                         | Offset (in mm) of the antenna phase center to camera CMOS sensor center in the north (N) direction.                       | Millimeters        | Integer                                       | -474,N              | Mandatory                                                                                          |
| 5                                 | `East Antenna Phase Offset`                                                                                          | Offset (in mm) of the antenna phase center to camera CMOS sensor center in the east (E) direction.                        | Millimeters        | Integer                                       | 301,E               | Mandatory                                                                                          |
| 6                                 | `Vertical Antenna Phase Offset`                                                                                      | Offset (in mm) of the antenna phase center to camera CMOS sensor center in the vertical (V) direction.                    | Millimeters        | Integer                                       | 275,V               | Mandatory                                                                                          |
| 7                                 | `Approximate latitude (degrees)`                                                                                     | Latitude component of coarse GNSS coordinates for image                                                                   | Degrees            | Fixed precision decimal with 8 decimal places | 39.89927023,Lat     | Mandatory                                                                                          |
| 8                                 | `Approximate longitude (degrees)`                                                                                    | Longitude component of coarse GNSS coordinates for image                                                                  | Degrees            | Fixed precision decimal with 8 decimal places | -82.92870067,Lon    | Mandatory                                                                                          |
| 9                                 | `Approximate altitude (m)`                                                                                           | Altitude component of coarse GNSS coordinates for image                                                                   | Meters             | Fixed precision decimal with 3 decimal places | 319.265,Ellh        | Mandatory                                                                                          |
| 10                                | `Standard deviation of positioning results for Approximate latitude (degrees) field`                                 | Standard deviation for Approximate latitude (degrees) field (Column 7)                                                    |                    | Fixed precision decimal with 6 decimal places | 1.982041,           | Not used by Propeller PPK currently but should be present to conform to the MRK specification      |
| 11                                | `Standard deviation of positioning results for Approximate longitude (degrees) field`                                | Standard deviation for Approximate longitude (degrees) field (Column 8)                                                   |                    | Fixed precision decimal with 6 decimal places | 1.388574,           | Not used by Propeller PPK currently but should be present to conform to the MRK specification      |
| 12                                | `Standard deviation of positioning results for Approximate altitude (m) field`                                       | Standard deviation for Approximate longitude (degrees) field (Column 9)                                                   |                    | Fixed precision decimal with 6 decimal places | 3.559854            | Not used by Propeller PPK currently but should be present to conform to the MRK specification      |
| 13                                | `RTK Status Flag`                                                                                                    |                                                                                                                           |                    |                                               | 16,Q                | Not used by Propeller PPK currently but should be present to conform to the MRK specification      |


### MRK requirements

Propeller PPK will validate that each MRK file uploaded meets the following requirements

| Field                                                     | Description                                                                                            |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| File Name                                                 | Must be <255 characters long                                                                           |
| File name                                                 | Must match :flightPrefix:_metadata.mrk format                                                          |
| MRK file                                                  | Conforms to the MRK specification                                                                      | 
| MRK file                                                  | Contains no empty rows                                                                                 |
| MRK file                                                  | Contains no duplicate entries                                                                          | 
| MRK file                                                  | Must contain exactly one entry for each image                                                          | 
| `Image sequence` field                                    | Must be present                                                                                        | 
| Precise Timestamp and GPS week Composite Timestamp        | GPS Time calculated from these fields is monotonically increasing                                      | 
| Precise Timestamp and GPS week Composite Timestamp        | Must be after the first epoch in the corresponding GNSS file                                           | 
| Precise Timestamp and GPS week Composite Timestamp        | Must be before last epoch in the corresponding GNSS file                                               | 
| `Precise Timestamp` field                                 | Must be present                                                                                        |
| `Precise Timestamp` field                                 | Must be a 6 decimal place fixed precision decimal                                                      | 
| `Precise Timestamp` field                                 | Must be for the UTC Timezone                                                                           | 
| `Precise Timestamp` field                                 | Must be in GPS time format                                                                             | 
| `Precise Timestamp` field                                 | Must be between `0` and `604799.999999`                                                                | 
| `GPS week` field                                          | Must be present                                                                                        | 
| `GPS week` field                                          | Must be in GPS time format                                                                             | 
| `GPS week` field                                          | Must be for the UTC Timezone                                                                           | 
| `GPS week` field                                          | Must be surrounded by `[]`                                                                             | 
| `GPS week` field                                          | Must be a positive integer                                                                             | 
| `North Antenna Phase Offset` field                        | Must be present                                                                                        | 
| `North Antenna Phase Offset` field                        | Must be in millimeters                                                                                 | 
| `North Antenna Phase Offset` field                        | Must be an integer                                                                                     | 
| `North Antenna Phase Offset` field                        | Must specify either N or S                                                                             | 
| `East Antenna Phase Offset` field                         | Must be present                                                                                        | 
| `East Antenna Phase Offset` field                         | Must be in millimeters                                                                                 | 
| `East Antenna Phase Offset` field                         | Must be an integer                                                                                     | 
| `East Antenna Phase Offset` field                         | Must specify either W or E                                                                             | 
| `Vertical Antenna Phase Offset` field                     | Must be present                                                                                        | 
| `Vertical Antenna Phase Offset` field                     | Must be in millimeters                                                                                 | 
| `Vertical Antenna Phase Offset` field                     | Must be an integer                                                                                     | 
| `Vertical Antenna Phase Offset` field                     | Must specify V                                                                                         | 
| `Approximate longitude (degrees)` field                   | Must be present                                                                                        | 
| `Approximate longitude (degrees)` field                   | Must be an 8 decimal place fixed precision decimal if present                                          | 
| `Approximate latitude (degrees)` field                    | Must be present                                                                                        | 
| `Approximate latitude (degrees)` field                    | Must be an 8 decimal place fixed precision decimal if present                                          | 
| `Approximate altitude (m)` field                          | Must be present                                                                                        | 
| `Approximate altitude (m)` field                          | Must be a 3 decimal place fixed precision decimal if present                                           |

## GPS Calibration Data 

Propeller PPK needs GPS calibration data to be provided in one of the following methods in addition to the antenna type in use.

Please see the [FAQ](#faq) for why Propeller needs this data.

### ANTEX File

GPS Antenna Calibration Data should be provided in the format of ANTEX file which should conform to the following [specification](https://files.igs.org/pub/data/format/antex14.txt).

This file needs to be provided to Propeller if this file is not already stored [here](https://www.ngs.noaa.gov/ANTCAL/LoadFile?file=ngs20.atx) and is not currently valid.

### Numbers for GNSS antenna specifications of Phase Centre offsets

Propeller also accepts numbers for GNSS antenna specifications of Phase Centre offsets for L1/L2.


## FAQ

Q: _What is the PPK spec? Why do we need to follow these requirements?_ 

A: The PPK spec is Propeller's standard for accepting and processing PPK data. This standard is based on common formats in the industry, and provides developers with a specific set of requirements for seamless integration with our workflow. If this spec is followed, your data will flow through our processing pipeline. 



Q: _We are unable to meet some of these requirements. Are we blocked from Propeller PPK?_  

A: No, not necessarily. While the PPK Spec is a source of truth for seamless integrations, we can be flexible on some of the requirements. Please reach out to drones@propelleraero.com.au with any specific requests.

Q: _Why doesn't Propeller support L5 data?_

A: Propeller AeroPoints collect L1/L2 data for PPK corrections in line with most of the CORS stations in the US. There is limited support for L5, and many stations do not support it at all.



Q: _Our drone can already collect RTK datasets. Can we upload without any additional engineering work?_

A: Yes, Propeller can accept data from any drone for high-accuracy and standard accuracy without the further engineering work. If your images include high-accuracy geotags, we can process those tags. Propeller PPK support is limited to drones that have completed the integration process. 



Q: _Why does Propeller prefer Raw GNSS data over computed GNSS formats such as RINEX_

A:  Conversion to formats such as RINEX from raw GNSS data is a lossy conversion process. This means that precision in values and data may get loss during this process. By using computed formats such as RINEX Propeller PPK may not be able to produce as accurate results as using raw GNSS data format.



Q: _Why does Propeller need Antenna Type and Antenna Calibration data_

A: Propeller needs the antenna type and antenna calibration data in order to provide a accurate PPK result as Propeller takes these into account when correcting geotags. Additionally this provides Propeller with the necessary information in order to troubleshoot poor PPK results.
