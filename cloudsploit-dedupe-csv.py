#!/usr/bin/python3

import csv
import argparse
import pathlib
import os
import requests
import re
import xlsxwriter

parser = argparse.ArgumentParser( description='Deduplicate CloudSploit report findings and filter for only FAILed issues. Does not delete or modify orignal file.' )
parser.add_argument(
    'cloudsploit_csv',
    help='File path to the CloudSploit CSV report file to be parsed',
    type=pathlib.Path
)
parser.add_argument(
    '-o','--output_file',
    help='File path to the deduped CloudSploit XLSX file. If omitted the file will be written to ./deduped-{original_filename}.xlsx',
    type=pathlib.Path
)

def main():

    args = parser.parse_args()

    csv_file = args.cloudsploit_csv

    issues = dict()
    maxlens = {
        'category': 0,
        'title': 0    
    }
    
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
                maxlens['category'] = max( maxlens['category'], len(row[cols.index('category')]) )
                issues[ row[ cols.index('title') ] ]['Title'] = row[cols.index('title')]
                maxlens['title'] = max( maxlens['title'], len(row[cols.index('title')]) )
                issues[ row[ cols.index('title') ] ]['Description'] = row[cols.index('description')]
                issues[ row[ cols.index('title') ] ]['Resources and Regions'] = ""
                issues[ row[ cols.index('title') ] ]['Message'] = row[cols.index('message')]
                for key,content in cloudsploit_guide( row[cols.index('category')], row[cols.index('title')] ).items():
                    issues[ row[ cols.index('title') ] ][key] = content
            
            issues[ row[ cols.index('title') ] ]['Resources and Regions'] += resource_region
            
    deduped_file = f'deduped-{pathlib.Path( csv_file ).stem}.xlsx' if args.output_file == None else f'{args.output_file}.xlsx'
    headers = ("Category", "Title", "Description", "Resources and Regions", "Message", "More Info", "Azure Link", "Recommended Action")
    wrappables = ( headers[2], headers[4], headers[5], headers[7] )
    # Write XLSX
    workbook = xlsxwriter.Workbook( deduped_file )
    worksheet = workbook.add_worksheet()
    # Styling
    worksheet.freeze_panes( 1, 0 )
    excel_formats = {
        "blank": workbook.add_format(),
        "url": workbook.get_default_url_format(),
        "header": workbook.add_format( {'bold':True, 'bg_color':'#BFBFBF'} ),
        "wrap": workbook.add_format( {'text_wrap':True,'valign':'top'} )
    }
    for fmt in excel_formats.values():
        fmt.set_valign('top')
    # Write headers
    for i, hdr in enumerate(headers):
        worksheet.write( 0, i, hdr, excel_formats['header'] )
        col_width = 50 # Default column width
        if hdr in ("Category","Title"):
            col_width = maxlens[ hdr.lower() ] # "Auto-fit" column width
        elif hdr not in wrappables:
            col_width = 20 # De-emphasis column width
        worksheet.set_column( i, i, col_width )
    # Write records
    row = 1
    for title in issues:
        col = 0
        for hdr in issues[title]:
            cell = issues[title][hdr]
            style = excel_formats['blank']
            if hdr in wrappables:
                style = excel_formats['wrap']
            if hdr.lower() == "azure link":
                worksheet.write_url( row, col, cell, excel_formats['url'] )
            else:
                worksheet.write( row, col, cell, style )
            col+=1
        row+=1
    workbook.close()

    print( f"\nSuccess! Deduped file to ./{deduped_file}" )
    os.system( f"open {deduped_file}" )


def cloudsploit_guide( cat, title ):

    guide = dict()
    cat_f = cat.lower().replace( " ", "" )
    title_f = title.lower().replace( " ", "-" )

    print( f"\rFetching extra info for {title_f}", end="" )

    res = requests.get( f'https://raw.githubusercontent.com/aquasecurity/cloud-security-remediation-guides/master/en/azure/{cat_f}/{title_f}.md', timeout=10 )

    print( f'\r{"Done": <100}', end="" )

    if res.status_code != 200:
        return guide

    rows = [
        "More Info",
        "AZURE Link",
        "Recommended Action"
    ]
    for r in rows:
        guide[ r ] = re.search( f"\| \*\*{r}\*\* \| ([^|]+)", res.text )[1]

    return guide


main()