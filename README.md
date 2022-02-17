
# CloudSploit Super De-duper
The CSV report from CloudSploit can be a bit unruly. The same issue is repeated multiple times if it's found for different **Regions** or **Resources**.

This script looks through each FAILed finding (because those are the ones we care about), and groups together the Regions and Resources into a single cell, so that each issue type is only listed once.

## Usage:

```
usage: cloudsploit-dedupe-csv.py [-h] [-o OUTPUT_FILE] cloudsploit_csv

Deduplicate CloudSploit report findings and filter for only FAILed issues. Does not delete or modify orignal file.

positional arguments:
  cloudsploit_csv       File path to the CloudSploit CSV report file to be parsed

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File path to the resultant deduped CloudSploit CSV. If omitted the file will be written to ./deduped-{original_filename}.csv
```

## Example:
### Run Cloudsploit and export report as CSV
```
$ /path/to/cloudsploit/index.js --config cloudsploit-config.js --csv /path/to/cloudsploit-report.csv
```
### Run the super deduper
**Basic**
```
$ ./cloudsploit-dedupe-csv.py /path/to/cloudsploit-report.csv
$ open ./dedupe-cloudsploit-report.csv
```
**Defining the output path**
```
$ ./cloudsploit-dedupe-csv.py -o /path/to/output.csv /path/to/cloudsploit-report.csv
$ open /path/to/output.csv
```

