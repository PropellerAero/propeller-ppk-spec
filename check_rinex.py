#!/usr/bin/env python3

# Script to check RINEX files meet specification

import argparse

parser = argparse.ArgumentParser(
    description='Script to check RINEX file meets specification'
)
parser.add_argument('path', help='Path to Propller PPK RINEX file')
args = vars(parser.parse_args())

file_path = args['path']

headers = []
epochs = []

in_header = True
with open(file_path) as fp:
    for line in fp:

        if in_header:
            if 'END OF HEADER' in line:
                in_header = False
            else:
                label = line[60:80].strip()
                headers.append({
                    'label': label,
                    'value': line[0:60].strip()
                })

        else:
            if line.startswith('>'):
                timestamp = line[2:30].strip()
                sats = []
                epoch = {
                    'timestamp': timestamp,
                    'sats': sats
                }
                epochs.append(epoch)
            else:
                sat = line[0:4].strip()
                code_l1 = line[5:20].strip()
                phase_l1 = line[20:35].strip()
                dop_l1 = line[35:50].strip()
                snr_l1 = line[50:65].strip()
                code_l2 = line[67:84].strip()
                phase_l2 = line[84:102].strip()
                dop_l2 = line[102:120].strip()
                snr_l2 = line[120:131].strip()

                sats.append({
                    'sat': sat,
                    'code_l1': float(code_l1) if code_l1 else None,
                    'phase_l1': float(phase_l1) if phase_l1 else None,
                    'dop_l1': float(dop_l1) if dop_l1 else None,
                    'snr_l1': float(snr_l1) if snr_l1 else None,
                    'code_l2': float(code_l2) if code_l2 else None,
                    'phase_l2': float(phase_l2) if phase_l2 else None,
                    'dop_l2': float(dop_l2) if dop_l2 else None,
                    'snr_l2': float(snr_l2) if snr_l2 else None,
                })


# Check all headers present

REQUIRED_HEADERS = [
    'RINEX VERSION / TYPE',
    'APPROX POSITION XYZ',
    'SYS / # / OBS TYPES',
    'TIME OF FIRST OBS',
    'SYS / PHASE SHIFT',
    'GLONASS SLOT / FRQ #',
    'GLONASS COD/PHS/BIS',
]

actual_headers = [h['label'] for h in headers]

for header in REQUIRED_HEADERS:
    if header not in actual_headers:
        print(f'{header} RINEX header not present')

min_valid_sats = None
max_valid_sats = None

for epoch in epochs:
    valid_sats = [sat for sat in epoch['sats'] if (sat['snr_l1'] or 0) > 35 and (sat['snr_l2'] or 0) > 35]
    valid_sats_count = len(valid_sats)

    if min_valid_sats is None or valid_sats_count < min_valid_sats:
        print(epoch['timestamp'], valid_sats_count)
        min_valid_sats = valid_sats_count

    if max_valid_sats is None or valid_sats_count > max_valid_sats:
        # print(epoch['timestamp'], valid_sats_count)
        max_valid_sats = valid_sats_count

print(f'Min valid sats in each epoch = {min_valid_sats}')
print(f'Max valid sats in each epoch = {max_valid_sats}')

# print(headers)
# print(epochs)
