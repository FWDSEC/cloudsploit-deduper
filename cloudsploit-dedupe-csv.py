#!/usr/bin/python3

import csv
import argparse
import pathlib
from os import path

parser = argparse.ArgumentParser( description='Deduplicate CloudSploit report findings and filter for only FAILed issues. Does not delete or modify orignal file.' )
parser.add_argument(
    'cloudsploit_csv',
    help='File path to the CloudSploit CSV report file to be parsed.',
    type=pathlib.Path
)

def main():

    args = parser.parse_args()

    csv_file = args.cloudsploit_csv

    issues = dict()
    
    with open( csv_file, newline='') as report_csv:
        report_reader = csv.reader( report_csv )

        is_header = True
        cols = []
        for row in report_reader:
            if is_header:
                is_header = False
                cols = list(map( lambda name: name.lower(), row))
                continue
            
            if row[cols.index('statusword')] != "FAIL":
                continue

            resource_region = f"Resource: {row[cols.index('resource')]}\nRegion: {row[cols.index('region')]},\n\n"

            if row[cols.index('title')] not in issues:
                issues[ row[ cols.index('title') ] ] = dict()
                issues[ row[ cols.index('title') ] ]['Category'] = row[cols.index('category')]
                issues[ row[ cols.index('title') ] ]['Title'] = row[cols.index('title')]
                issues[ row[ cols.index('title') ] ]['Description'] = row[cols.index('description')]
                issues[ row[ cols.index('title') ] ]['Resources and Regions'] = ""
                issues[ row[ cols.index('title') ] ]['Message'] = row[cols.index('message')]
            
            issues[ row[ cols.index('title') ] ]['Resources and Regions'] += resource_region
            
    deduped_file = f'deduped-{path.basename( csv_file )}'
    with open(deduped_file, 'w') as dd:
        dd.write( f"Category,Title,Description,Resources and Regions, Message,\n"  )
        for title in issues:
            for col in issues[title]:
                dd.write( f'"{issues[title][col]}",'  )
            dd.write( "\n" )

    print( f"Success! Deduped file: ./{deduped_file}" )


main()