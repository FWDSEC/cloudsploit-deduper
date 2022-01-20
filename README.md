
# CloudSploit Super De-duper
The CSV report from CloudSploit can be a bit unruly. The same issue is repeated multiple times if it's found for different **Regions** or **Resources**.

This script looks through each FAILed finding (because those are the ones we care about), and groups together the Regions and Resources into a single cell, so that each issue type is only listed once.

## Usage:

```
usage: cloudsploit-dedupe-csv.py [-h] cloudsploit_csv

Deduplicate CloudSploit report findings and filter for only FAILed issues. Does not delete or modify orignal file.

positional arguments:
  cloudsploit_csv  File path to the CloudSploit CSV report file to be parsed.

optional arguments:
  -h, --help       show this help message and exit
```

## Example:
```
$ /path/to/cloudsploit/index.js --config cloudsploit-config.js --csv /path/to/cloudsploit-report.csv
...
$ ./cloudsploit-dedupe-csv.py /path/to/cloudsploit-report.csv
$ open ./dedupe-cloudsploit-report.csv
```

