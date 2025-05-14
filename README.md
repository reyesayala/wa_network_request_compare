# Web Archiving Network Request Compare
Utilities for extracting network requests of archived websites and their live counterparts and compares the network requests.

## Getting Started
Some packages such as pyppeteer run best on python 3.6. The necessary packages are listed in environment.yml.

Instructions on how to install Anaconda for python can be found [here](https://docs.anaconda.com/anaconda/install/linux/).

Once anaconda is installed, import the environment with.
```
conda env create -f environment.yml
```
Activating and deactivating the anaconda environment.
```
conda activate python3_6
conda deactivate
```

## Usage
> **Notes:** Including the -h flag in any of the programs will display a description of all the command line flags.

### read_seed.py
This program takes a CSV file with the seed website URLs and outputs it into another CSV or a DB.
> A valid seed csv file should have the URLs as the first column, other columns are ignored.
> The output CSV file will have three columns, archive ID, URL ID, and URL.

Command syntax: 
```
python3 read_seed.py --csv=your/directory/Collection-seed-list.csv --db=urls.db --out=current_urls.csv --ext=1234
--name="Collection Name" --sort
```
Arguments:
* csv - The CSV file with the seed URLs. Interchangeable with --db as only one type of input is allowed.
* db - The DB file to store the URLs.
* out - The CSV file to write the URLs.
* ext - ID of the archive.
* name - Name of the archive.
* sort - (optional) Include to sort the output.

### create_archive_urls.py
This program takes the CSV or DB from the previous program and gets the Archive-It archive URL using the Archive-It API.  
> The output CSV file will have four columns, archive ID, URL ID, date, and archived URL.

Command syntax: 
```
python3 create_archive_urls.py --csv=current_urls.csv --db=urls.db --out=archive_urls.csv --banner
```
Arguments:
* csv - Input CSV file with current URLs. Interchangeable with --db as only one type of input is allowed.
* db - Input DB file with URLs, output is automatically inserted in db.
* out - The CSV file to write the URLs.
* banner - (optional) Include to generate URLs that has the banner, default removes banner.


### get_file_names.py
This program outputs a CSV file (called file_names.csv) which maps the current and archive URLs with their respective network request CSV files. This file acts as an index. 
> The output CSV will have four columns, current URl, archive URL, current network requests file name, archive network requests file name.

Command syntax:
```
python3 get_file_names.py --currcsv=current_index.csv --archcsv=archive_index.csv --out=file_names.csv --print
```
Arguments:
* currcsv - The CSV file with the current URLs index.
* archcsv - The CSV file with the archive URLs index.
* out - The CSV file to write the urls and file names. 
* print - (optional) Include to print urls and file names to stdout, default doesn't print.


### extract_network_requests.py

This program should be run twice, once for the current URLs (with current_urls.csv as input), and a second time for the archived URLs (with archive_urls.csv as input). 

This program has two outputs: 

<ol>
  <li>An index file with the extraction status of the current/archive URLs (called current_index.csv or archive_index.csv)</li>
  <li>A set of files each containing the network requests for the current or archive URLs (created in the directory "current_requests" or "archive_requests")</li>
</ol>



The index file will have six/seven columns, archive ID, URL ID, archive URL, site status, site message, extraction message, and date.

* site status - Contains 'LIVE' if the URL can be reached or redirected, and 'FAIL' if the URL could not be reached (ex. 404).
* site message - A reason on why site status was 'LIVE' or 'FAIL'. (ex. 'Redirected to https://..' or 'HTTPError: 404')
* extraction message - Either 'Extraction successful' or reason extraction was unsuccessful. (ex. 'Navigation Timeout Exceeded: 30000 ms exceeded.')

The output CSV files containing the network requests of the current/archive URLs will have five/six columns, archive ID, URL ID, URL, resource type, status code, and date.

> Date is only included if extracting network requests from archive URLs

Command syntax:
```
python3 extract_network_requests.py --csv=current_urls.csv --db=urls.db --csvout=current_requests/ --index=current_index.csv --timeout=30 --archive
```
Arguments:
* csv - Input CSV file with current/archive URLs. Interchangable with --db as only one type of input is allowed.
* db - Input DB file with current/archive URLs.
* csvout - The directory to store the CSV files containing the network requests.
* index - The CSV file to write the extraction status of the URLs.
* timeout - (optional) Specify duration before timeout for each site, in seconds, default 30 seconds.
* archive - Include if input CSV file or input DB file is used for archive URLs.

### analyze_csv.py

This program takes a csv file as input, the input csv file should have the following data (in order): `archive_id`, `url_id`, `url`, `site_status`, `site_message`, and `screenshot_message`.

The program categorizes each row of data by their `site_status` and `site_message`:
* site status - Contains 'LIVE' if the URL can be reached or redirected, and 'FAIL' if the URL could not be reached (ex. 404).
* site message - A reason on why site status was 'LIVE' or 'FAIL'. (ex. 'Redirected to https://..' or 'HTTPError: 404')

The output files will be in a folder called "csv_outputs" created at where this program is executed. 

Command syntax:
```
python3 analyze_csv.py current_index.csv
```

Argument:

* Input CSV file with `archive_id`, `url_id`, `url`, `site_status`, `site_message`, and `screenshot_message`.

### compare_network_requests.py

This program takes a csv file (an index file that was produced as ouput by get_file_names.py). The input csv file should have the following data in order: "current_url","archive_url","current_file_name", and "archive_file_name". 

For each pair of current requests file/archived request file, the program uses fuzzy comparison to match each current request to its archived counterpart. Then it checks to see if the status code of each request is different for the current and archived requests. Finally, it output which archived requests were not found in the current version, as well as a measure of interactional quality, defined as 

### select_archived_url.py

This program is a helper program and is optional to run. It takes in the file archive_urls.csv and and produces a smaller csv file by choosing a single capture date for each url. The choosing is done at random. This can help create a smaller sample of archive_urls.csv in case the file is too large/slow to run. 

## Authors
* **Brenda Reyes Ayala** 
* **Andy Li**
* **Xiaohui Liu**
## License
todo

## Acknowledgments 
todo
