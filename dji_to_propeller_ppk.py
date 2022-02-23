#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess

from pathlib import Path

# Script to convert DJI PPK flight data to Propeller PPK spec
# Requires ExifTool (https://exiftool.org/)

parser = argparse.ArgumentParser(
    description='Script to convert DJI PPK flight data to Propeller PPK spec'
)
parser.add_argument('source_dir', help='Path to directory of DJI PPK flight directories to convert')
parser.add_argument('dest_dir', help='Path to output directory')
args = vars(parser.parse_args())

mission_list = os.listdir(args['source_dir'])
mission_list.sort()

# mission_dirs = [dir for dir in mission_list if not dir.startswith('.') and os.path.isdir(os.path.join(args['source_dir'], dir))]
mission_dirs = [dir for dir in mission_list if not dir.startswith('.') and os.path.isdir(os.path.join(args['source_dir'], dir))][:1]

mission_index = 1

for mission_dir in mission_dirs:
    abs_in_path = os.path.join(args['source_dir'], mission_dir)

    mission_prefix = f'Flight{mission_index:02}'

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
        '-EXIF:ShutterSpeedValue',
        '-EXIF:ImageWidth',
        '-EXIF:ImageHeight',
        '-EXIF:Model',
        '-EXIF:LensModel',
        '-EXIF:SerialNumber',
        '-EXIF:GPSLongitudeRef',
        '-EXIF:GPSLongitude',
        '-EXIF:GPSLatitudeRef',
        '-EXIF:GPSLatitude',
        '-EXIF:GPSAltitudeRef',
        '-EXIF:GPSAltitude',
        '-XMP:FlightXSpeed',
        '-XMP:FlightYSpeed',
        '-overwrite_original',
        abs_out_path
    ], stdout=subprocess.DEVNULL)



    # Convert PPKRAW.bin to GNSS.obs
    print(f'\tConverting GNSS observation file')

    gnss_files = [f for f in os.listdir(abs_in_path) if f.endswith('PPKRAW.bin')]

    if len(gnss_files) != 1:
        raise Exception(f'1 PPKRAW.bin file expected, found {len(gnss_files)} in {mission_dir}')

    src_gnss_path = os.path.join(abs_in_path, gnss_files[0])
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
        dst_gnss_path

    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
