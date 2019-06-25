# Web Archiving Screenshot Compare
Utilities for creating screenshots of archived websites and their live counterparts and compares the two screenshots.

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

### create-archive_urls.py
This program takes the CSV or DB from the previous program and gets the Archive-It archive URL.  
> The output CSV file will have three columns, archive ID, URL ID, and URL.

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
This program outputs a CSV file which maps the current and archive URLs with their respective screenshots.
> The output CSV will have four columns, current URl, archive URL, current screenshot file name, archive screenshot file name.

Command syntax:
```
python3 get_file_names.py --currcsv=current_index/ --archcsv=archive_index/ --db=urls.db --out=file_names.csv --print
```
Arguments:
* currcsv - The CSV file with the current screenshots index.
* archcsv - The CSV file with the archive screenshots index.
* db - Input DB file with urls. Interchangeable with using --currcsv and --archcsv since only one type of input is allowed. 
* out - The CSV file to write the urls and file names. 
* print - (optional) Include to print urls and file names to stdout, default doesn't print.


## Authors
* **Brenda Reyes Ayala** 
* **Andy Li**
## License
todo

## Acknowledgments 
todo
