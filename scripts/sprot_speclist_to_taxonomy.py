#!/usr/bin/env python3

import argparse
import urllib.request
import sys
import re
import csv
csv.register_dialect('tsv', delimiter='\t', quoting=csv.QUOTE_NONE)
lookup_taxonomy = { 'A': 'Archaea',
                    'B': 'Bacteria',
                    'E': 'Eukaryota',
                    'V': 'Virus',
                    'O': 'Other',
                    'X': 'Unknown' }

parser = argparse.ArgumentParser(description='Read speclist from uniprot and parse for species code to taxonomy')
parser.add_argument('-o','--output', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='output file name or else will write to stdout')
parser.add_argument('-i', '--input', type=argparse.FileType('r'), nargs='?',
                    help='species list file from uniprot already downloaded otherwise will open and download')

parser.add_argument('--url', required=False,
                    default='https://www.uniprot.org/docs/speclist.txt',help='URL to download from instead of local file')

args = parser.parse_args()

matchsp = re.compile(r'(\S+)\s+([A-Z])\s+(\d+):\s+N=(.+)')

# this code is stupidly duplicated until I can figure out best way to deal with the encoding diff for url vs local file

csvout = csv.writer(args.output,dialect="tsv")
if args.input:
    for line in args.input:
        m = matchsp.match(line)
        if m:
            csvout.writerow([m.group(1),lookup_taxonomy[m.group(2)],m.group(3),m.group(4)])
else:
    with urllib.request.urlopen(args.url) as web:
        for line in web:
            m = matchsp.match(line.decode('utf-8'))
            if m:
                csvout.writerow([m.group(1),lookup_taxonomy[m.group(2)],m.group(3),m.group(4)])
