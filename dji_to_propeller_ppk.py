#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import csv
import json

from pathlib import Path
from subprocess import check_output

# Script to convert DJI PPK flight data to Propeller PPK spec
# Requires ExifTool and convbin on the PATH

parser = argparse.ArgumentParser(
    description='Script to convert DJI PPK flight data to Propeller PPK spec'
)
parser.add_argument('source_dir', help='Path to directory of DJI PPK flight directories to convert')
parser.add_argument('dest_dir', help='Path to output directory')
args = vars(parser.parse_args())

mission_list = os.listdir(args['source_dir'])
mission_list.sort()

mission_dirs = [dir for dir in mission_list if not dir.startswith('.') and os.path.isdir(os.path.join(args['source_dir'], dir))]

for mission_index, mission_dir in enumerate(mission_dirs):
    abs_in_path = os.path.join(args['source_dir'], mission_dir)

    mission_prefix = f'Flight{mission_index+1:02}'

    abs_out_path = os.path.join(args['dest_dir'], mission_prefix)
    print(f'Converting mission {mission_dir}')

    print(f'\tCreating output directory')
    Path(abs_out_path).mkdir(parents=True, exist_ok=True)

    image_files = [f for f in os.listdir(abs_in_path) if f.endswith('.JPG')]
    image_files.sort()

    print(f'\tCopying + updating {len(image_files)} images')

    for image_index, image_file in enumerate(image_files):
        src_image_path = os.path.join(abs_in_path, image_file)
        dst_image_path = os.path.join(abs_out_path, f'{mission_prefix}_{image_index+1:04}.JPG')
        shutil.copyfile(src_image_path, dst_image_path)

    # Filter metadata on all images in flight dir
    subprocess.run([
        'exiftool',
        # Ignore MarkerNote offset error, we're deleting these anyway
        '-m',
        # Remove all tags
        '-all=',
        '-tagsfromfile',
        '@',

        # Whitelist of tags to keep
        '-EXIF:DateTimeOriginal',
        '-EXIF:ISO',
        '-EXIF:ShutterSpeedValue',
        '-EXIF:ImageWidth',
        '-EXIF:ImageHeight',
        '-EXIF:Model',
        '-EXIF:LensModel',
        '-EXIF:GPSLongitudeRef',
        '-EXIF:GPSLongitude',
        '-EXIF:GPSLatitudeRef',
        '-EXIF:GPSLatitude',
        '-EXIF:GPSAltitudeRef',
        '-EXIF:GPSAltitude',
        '-overwrite_original',
        abs_out_path
    ], stdout=subprocess.DEVNULL)

    # Convert Timestamp.MRK to metadata.csv
    timestamp_files = [f for f in os.listdir(abs_in_path) if f.endswith('TIMESTAMP.MRK')]

    if len(timestamp_files) != 1:
        raise Exception(f'1 TIMESTAMP.MRK file expected, found {len(timestamp_files)} in {mission_dir}')


    exif_data = json.loads(check_output(['exiftool', '-json', abs_in_path]))
    exif_data.sort(key=lambda x: x['FileName'])

    src_timestamp_path = os.path.join(abs_in_path, timestamp_files[0])
    dst_timestamp_path = os.path.join(abs_out_path, f'{mission_prefix}_metadata.csv')

    with open(dst_timestamp_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['Manufacturer', 'Propeller'])
        writer.writerow(['Model', 'DemoUAV'])
        writer.writerow(['Serial number', 'AJ34NF12'])
        writer.writerow(['Firmware version', '1.75.24a_rev2'])
        writer.writerow(['Propeller PPK version', '1.0'])

        # Header
        writer.writerow(['Image', 'Timestamp (s)', 'GPS week number', 'Antenna offset north (m)', 'Antenna offset east (m)', 'Antenna offset up (m)', 'Roll (degrees)', 'Pitch (degrees)', 'Yaw (degrees)', 'Approximate longitude (degrees)', 'Approximate latitude (degrees)', 'Approximate altitude (m)'])

        with open(src_timestamp_path) as mrk_file:
            for line in mrk_file:
                [index, time, week, north, east, up, lat, lon, height,_,_,_,_] = line.split()

                index = int(index)
                image = f'{mission_prefix}_{index:04}.JPG'
                time = f'{float(time):.6f}'
                week = int(week[1:-1])
                north = int(north.split(',')[0]) / 1000
                north = f'{north:.3f}'
                east = int(east.split(',')[0]) / 1000
                east = f'{east:.3f}'
                up = int(up.split(',')[0]) / 1000
                up = f'{up:.3f}'
                lat = float(lat.split(',')[0])
                lat = f'{lat:.8f}'
                lon = float(lon.split(',')[0])
                lon = f'{lon:.8f}'
                height = float(height.split(',')[0])
                height = f'{height:.3f}'

                roll = float(exif_data[index-1]['CameraRoll'])
                roll = f'{roll:.2f}'

                pitch = float(exif_data[index-1]['CameraPitch'])
                pitch = f'{pitch:.2f}'

                yaw = float(exif_data[index-1]['CameraYaw'])
                yaw = f'{yaw:.2f}'

                writer.writerow([image, time, week, north, east, up, roll, pitch, yaw, lon, lat, height])





    # Convert PPKRAW.bin to GNSS.obs
    print(f'\tConverting GNSS observation file')

    gnss_files = [f for f in os.listdir(abs_in_path) if f.endswith('PPKRAW.bin')]

    if len(gnss_files) != 1:
        raise Exception(f'1 PPKRAW.bin file expected, found {len(gnss_files)} in {mission_dir}')

    src_gnss_path = os.path.join(abs_in_path, gnss_files[0])
    unfiltered_gnss_path = os.path.join(abs_out_path, f'{mission_prefix}_GNSS.obs.0')
    dst_gnss_path = os.path.join(abs_out_path, f'{mission_prefix}_GNSS.obs')

    subprocess.run([
        'convbin',
        '-r',
        'rtcm3',
        '-tr',
        '2022/01/08 00:00:00',
        '-v', '3.04',
        '-od',
        '-os',
        src_gnss_path,
        '-o',
        unfiltered_gnss_path

    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Filter RINEX header
    ALLOWED_RINEX_HEADERS = [
        'RINEX VERSION / TYPE',
        'APPROX POSITION XYZ',
        'SYS / # / OBS TYPES',
        'TIME OF FIRST OBS',
        'SYS / PHASE SHIFT',
        'GLONASS SLOT / FRQ #',
        'GLONASS COD/PHS/BIS',
        'END OF HEADER',
    ]

    with open(unfiltered_gnss_path) as file_in:
        with open(dst_gnss_path, 'w') as file_out:
            in_header = True
            for line in file_in:

                if in_header:
                    label = line[60:81].strip()

                    if label in ALLOWED_RINEX_HEADERS:
                        file_out.write(line)

                    if 'END OF HEADER' in label:
                        in_header = False

                else:
                    file_out.write(line)

    Path(unfiltered_gnss_path).unlink()
