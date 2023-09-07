
# CloudSploit Super De-duper
**Deduplicate CloudSploit report findings and filter for only FAILed issues. Does not delete or modify orignal file.**

The CSV report from CloudSploit can be a bit unruly. The same issue is repeated multiple times if it's found for different **Regions** or **Resources**.

This script looks through each FAILed finding (because those are the ones we care about), and groups together the Regions and Resources into a single cell, so that each issue type is only listed once.

As a bonus it also outputs to `*.xlsx`, *AND* pulls down extra information about each finding from AquaSec (Cloudsploit's devs) including remediation guidance and links to relevant Microsoft articles. Only the finding title is sent to fetch this data, and never any sensitive or identifying information.

## Requirements
1. Python 3
2. Pipenv (https://pipenv-fork.readthedocs.io/en/latest/)

## Installation
1. Download the code: `git clone https://github.com/FWDSEC/cloudsploit-deduper.git`
2. Navigate into the code folder: `cd cloudsploit-deduper/`
3. Create python virtual environment: `pipenv --three`
4. Install python dependencies into the virtal env: `pipenv install`

## Usage:
`pipenv run cloudsploit-dedupe-csv.py [-h] [-o OUTPUT_FILE] cloudsploit_csv`
```
positional arguments:
  cloudsploit_csv       File path to the CloudSploit CSV report file to be parsed

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File path to the deduped CloudSploit XLSX file. If omitted the file will be written to ./deduped-{original_filename}.xlsx
```

## Example:
### Run Cloudsploit and export report as CSV
```
$ /path/to/cloudsploit/index.js --config cloudsploit-config.js --csv /path/to/cloudsploit-report.csv
```
### Run the super deduper
**Basic**
```
$ pipenv run cloudsploit-dedupe-csv.py /path/to/cloudsploit-report.csv
$ open ./deduped-cloudsploit-report.xlsx
```
**Defining the output path**
```
$ pipenv run cloudsploit-dedupe-csv.py -o /path/to/output.xlsx /path/to/cloudsploit-report.csv
$ open /path/to/output.xlsx
```
**Multiple subscriptions and/or CSVs to join**
```
$ cat /path/to/cloudsploit-reports/*.csv > /path/to/joined-cloudsploit-reports.csv
$ pipenv run cloudsploit-dedupe-csv.py -o /path/to/output.xlsx /path/to/joined-cloudsploit-reports.csv
$ open /path/to/output.xlsx
```

