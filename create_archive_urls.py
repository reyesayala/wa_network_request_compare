import argparse
import sqlite3
import csv
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib.request
import urllib3




def create_with_csv(csv_out_name, csv_in_name, remove_banner):
    """Finds the archive urls using the input csv file with current urls, and outputs it into a csv.

    Parameters
    ----------
    csv_in_name : str
        The CSV file with the current urls.
    csv_out_name : str
        The CSV file to write the archive urls.
    remove_banner : bool
        Whether or not to generate urls that include Archive-It banner.

    """
    # Create a session
    session = requests.Session()
    
    # Define a retry strategy
    retry_strategy = Retry(
    total=5,  # Total number of retries
    backoff_factor=1,  # Waits 1 second between retries, then 2s, 4s, 8s...
    status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry on
    method_whitelist=["HEAD", "GET", "OPTIONS"]  # Methods to retry
    )

    # Mount the retry strategy to the session
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    
    with open(csv_in_name, 'r') as csv_file_in:
        csv_reader = csv.reader(csv_file_in)
        with open(csv_out_name, 'w+') as csv_file_out:
            csv_writer = csv.writer(csv_file_out, delimiter=',', quoting=csv.QUOTE_ALL)
            csv_writer.writerow(["archive_id", "url_id", "date", "archive_url"])

            count = 0
            for line in csv_reader:
                if count == 0:      # skip the header
                    count += 1
                    continue

                archive_id = line[0]
                url_id = line[1]
                url = line[2]
                archive_url = "https://wayback.archive-it.org/{0}/*/{1}".format(archive_id, url)

                #for each live url, use the Archive-It API to return a list of all timestamps that were archived 
                print("url #" + url_id + ": " + archive_url)
                prefix = "https://wayback.archive-it.org/"+archive_id
                prefix2 = "/timemap/cdx?url="
                postfix = "&fl=timestamp"
                request_url = prefix+prefix2+url+postfix
                print(" request url :"+request_url)
                
                try:

                    #request the timestamp
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}
                    response = session.get(request_url, headers=headers) 
                    timestamps = response.text.split("\n")
                    timestamps.remove('')
                    print(timestamps)
                    
                    timestamp_urls = []
                    for item in timestamps: 
                        if remove_banner: 
                            archived_url = prefix+"/"+item+"if_/"+url
                        else:
                            archived_url = prefix+"/"+item+url
                        
                        timestamp_urls.append(archived_url)
                    print(timestamp_urls)
                    
                    #write to a csv file the archive id, the url id, and the final, archived url
                    for final_url in timestamp_urls: 
                        for date in timestamps:
                            csv_writer.writerow([archive_id, url_id, date, final_url])

                    
                except requests.exceptions.ConnectionError as e:
                    print(f"Error connecting to the server: {e}")
                except requests.exceptions.HTTPError as e:
                    print(f"HTTP error occurred: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred: {e}")




def parse_args():
    """Parses the arguments passed in from the command line.

    Returns
    -------
    csv_in_name : str
        The CSV file with the current urls.
    csv_out_name : str
        The CSV file to write the archive urls.
    use_db : bool
        Whether or not the input is DB.
    use_csv : bool
        Whether or not the input is CSV.
    make_csv : bool
        Whether or not to output a CSV when use_db is True.
    remove_banner : bool
        Whether or not to generate urls that include Archive-It banner.

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=str, help="Input DB file with urls, output is automatically inserted in db")
    parser.add_argument("--csv", type=str, help="Input CSV file with current urls")
    parser.add_argument("--out", type=str, help="The CSV file to write the urls")
    parser.add_argument("--banner", action='store_true',
                        help="(optional) Include to generate urls that has the banner, default removes banner")

    args = parser.parse_args()

    # some error checking
    if args.db is None and args.csv is None:
        print("Must include input file\n")
        exit()
    if args.db is not None and args.csv is not None:
        print("Must only specify one type in input file\n")
        exit()
    if args.csv is not None and args.out is None:
        print("Must specify output location\n")
        exit()
        
    if args.db is not None:
        use_db = True
        connect_sql(args.db)
    else:
        use_db = False
                
    if args.csv is not None:
        use_csv = True
        csv_in_name = args.csv
    else:
        use_csv = False

    if args.out is not None:
        csv_out_name = args.out
        make_csv = True
    else:
        make_csv = False

    remove_banner = not args.banner

    return use_db, use_csv, make_csv, args.out, args.csv, remove_banner

        
# creates the db and table to store the URLs
def connect_sql(path):
    """Creates or connects the DB file and create the necessary tables. """
    global connection, cursor    

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    connection.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS archive_urls (archiveID INT, urlID INT, date TEXT, url TEXT, "
                   "FOREIGN KEY (archiveID) REFERENCES collection_name(archiveID));")
    cursor.execute("DELETE FROM archive_urls;")
    connection.commit()
    

def main():
    use_db, use_csv, make_csv, csv_out_name, csv_in_name, remove_banner = parse_args()
    print("Getting archive urls...")
    if use_csv:
        
        print("Reading CSV")
        create_with_csv(csv_out_name, csv_in_name, remove_banner)
    if use_db:
        create_with_db(make_csv, csv_out_name, remove_banner)
    

main()


