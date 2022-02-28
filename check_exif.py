#!/usr/bin/env python3

# Script to check all images in the specified folder have the required EXIF tags
# Requires ExifTool on the PATH

import argparse
import json

from subprocess import check_output


parser = argparse.ArgumentParser(
    description='Script to check all images in the specified folder have the required EXIF tags'
)
parser.add_argument('source_dir', help='Path to directory of Propller PPK flight directories to convert')
args = vars(parser.parse_args())

source_dir = args['source_dir']

exif_data = json.loads(check_output(['exiftool', '-r', '-json', source_dir]))

REQUIRED_TAGS = [
    'DateTimeOriginal',
    'GPSAltitude',
    'GPSAltitudeRef',
    'GPSLatitude',
    'GPSLatitudeRef',
    'GPSLongitude',
    'GPSLongitudeRef',
    'ImageHeight',
    'ImageWidth',
    'ISO',
    # 'LensModel',
    'Model',
    'ShutterSpeedValue',
]

for img_exif in exif_data:
    for tag in REQUIRED_TAGS:
        if tag not in img_exif:
            fname = img_exif['SourceFile']
            print(f'{fname} missing {tag}')

print(f'Finished scanning {len(exif_data)} images')