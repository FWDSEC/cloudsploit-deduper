
# CloudSploit Super De-duper
**Deduplicate CloudSploit report findings and filter for only FAILed issues. Does not delete or modify orignal file.**

The CSV report from CloudSploit can be a bit unruly. The same issue is repeated multiple times if it's found for different **Regions** or **Resources**.

This script looks through each FAILed finding (because those are the ones we care about), and groups together the Regions and Resources into a single cell, so that each issue type is only listed once.

As a bonus it also outputs to `*.xlsx`, *AND* pulls down extra information about each finding from AquaSec (Cloudsploit's devs) including remediation guidance and links to relevant Microsoft articles. Only the finding title is sent to fetch this data, and never any sensitive or identifying information.

## Arguments
```
positional arguments:
  cloudsploit_csv       File path to the CloudSploit CSV report file to be parsed

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File path to the deduped CloudSploit XLSX file. If omitted the file will be written to ./deduped-{original_filename}.xlsx
```

## Prerequisite
Run Cloudsploit and export report as CSV
```
/path/to/cloudsploit/index.js --config cloudsploit-config.js --csv /path/to/cloudsploit-report.csv
```

## Run with Docker

### Build
1. Clone git repo
```
git clone https://github.com/FWDSEC/cloudsploit-deduper.git && cd cloudsploit-deduper
```
2. Build the docker image
```
docker build -t cloudsploit-deduper:latest .
```

### Basic Usage
```
docker run --rm -t -v </path/to/cloudsploit-report-dir>:/tmp cloudsploit-deduper:latest /tmp/<cloudsploit-report.csv>
```
Replace the options wrapped in `< >`'s with your own paths and filenames.

**Note:** The `/tmp` is a requirement and only applies to the filepath within the Docker container.

When the container finishes running you will have the file `deduped-cloudsploit-report.xlsx` inside whatever you defined as your `/path/to/cloudsploit-report-dir`. The automatic naming prefixes the original filename with `deduped-` and swaps the extension to `.xlsx`.

### Advanced Examples:

#### Define the output filename
```
docker run --rm -t -v /path/to/cloudsploit-report-dir:/tmp cloudsploit-deduper:latest  -o /tmp/my-new-spiffy-file.xlsx /tmp/cloudsploit-report.csv
```
For the `-o` arguemnt, the filename can be anything but it must start with `/tmp` and end with `.xlsx`.

**Note:** The `/tmp` is a requirement and only applies to the filepath within the Docker container.

#### Joining multiple Cloudsploit reports

*This can be done by simply concatenating the CSVs together, and then running the deduper on the resultant CSV file.*
```
cat /path/to/cloudsploit-reports-dir/*.csv > /path/to/joined-cloudsploit-reports.csv
```
```
docker run --rm -t -v /path/to/cloudsploit-report-dir:/tmp cloudsploit-deduper:latest -o /tmp/deduped-cloudsploit-report.xlsx /tmp/joined-cloudsploit-reports.csv
```

***

## Run natively
*For those who prefer more installation steps, or can't get Docker to run in their Windows VM because the cheap SKU doesn't offer nested virtualization.*

### Requirements
1. Python 3
2. Pipenv (https://pipenv-fork.readthedocs.io/en/latest/)

### Installation
1. Download the code:
```
git clone https://github.com/FWDSEC/cloudsploit-deduper.git
```
2. Navigate into the code folder:
```
cd cloudsploit-deduper/
```
3. Create python virtual environment:
```
pipenv --three
```
5. Install python dependencies into the virtal env:
```
pipenv install
```

### Basic Usage:
```
pipenv run cloudsploit-dedupe-csv.py /path/to/cloudsploit-report.csv
```

### Advanced Examples
#### Defining the output path
```
pipenv run cloudsploit-dedupe-csv.py -o /path/to/output.xlsx /path/to/cloudsploit-report.csv
```
#### Multiple subscriptions and/or CSVs to join
```
cat /path/to/cloudsploit-reports/*.csv > /path/to/joined-cloudsploit-reports.csv
```
```
pipenv run cloudsploit-dedupe-csv.py -o /path/to/output.xlsx /path/to/joined-cloudsploit-reports.csv
```

