import sqlite3
import argparse
import csv
from fuzzywuzzy import fuzz


def find_different_requests(request_pair):
    """Checks if the status code of both current and archive URL match.

    Parameters
    ----------
    request_pair : tuple
        Tuple containing a single current network request info in the first index and
        a single archive network request info in the second index.

    """

    c_request = request_pair[0]
    a_request = request_pair[1]
    c_status = c_request["status_code"]
    a_status = a_request["status_code"]

    # we do not consider redirects with status 302 to be errors
    if(c_status!= a_status) and (a_status!="302") and (c_status!="302"):
        #print("Difference found!")
        print(c_request["url"], c_status, a_request["url"], a_status)
        return True
    else:
        return False

def check_archive_specific_url(dict_obj):
    """Checks if network request URL is archive-it specific. If it is, remove it from the list.

    Parameters
    ----------
    dict_obj : dict
        The dictionary object containing info related to one network request.

    """

    # URL of each network request
    url = dict_obj["url"]

    # Filtering out archive-it specific URLs'
    if "partner.archive-it.org" in url:
        print("Removing {} URL from network requests.".format(url))
        return False
    else:
        return True



def open_with_csv(index_file_name, curr_requests_path, arch_requests_path, csv_out_name, do_print):
    """Parses both index files line by line and writes the urls and file names to the output file.

    Parameters
    ----------
    index_file_name : str
        The CSV file that maps the current network requests to their archived counterparts.
    curr_csv_path : str
        The directory containing the CSV files with the current websites' network requests.
    arch_out_path : str
        The directory containing the CSV files with the archived websites' network requests.
    csv_out_name : str
        The CSV file to write the file with the combined requests.
    do_print : bool
        Whether or not to print the results to stdout.

    """
    with open(csv_out_name, 'w') as csv_file_out:
        csv_writer = csv.writer(csv_file_out, delimiter=',', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(["current_url", "current_filename", "archive_url", "archive_filename", "num_current_requests","num_archive_requests", "num_requests_in_common", "num_requests_with_errors", "ic"])
    

    # Read the index file
    index_lst = []
    index_file = open(index_file_name, 'r')
    index_reader = csv.reader(index_file, delimiter=',')

    # Skip the headers
    next(index_reader, None)
    

    for column in index_reader:
        index_lst.append(column)

    index_file.close()
    print("Index file has been read")

    for request_file in index_lst:
        c_url = request_file[0]
        a_url = request_file[1]
        c_file_name = request_file[2]
        a_file_name = request_file[3]

        print("-----------------------------------------------------")
        print("Current url: ", c_url)
        print("Archive url: ", a_url)

        try:
            # Read the csv files as dicts
            with open(arch_requests_path + "/" + a_file_name) as a_input:
                a_input_file = csv.DictReader(a_input)
                arch_requests_data = [row for row in a_input_file]

                # Close file
                a_input.close()
                print("There are ",len(arch_requests_data)," requests in archived website")

            with open(curr_requests_path + "/" + c_file_name) as c_input:
                c_input_file = csv.DictReader(c_input)
                curr_requests_data = [row for row in c_input_file]

                # Close file
                c_input.close()
                print("There are ",len(curr_requests_data)," requests in current website")



            num_errors = 0
            missing_requests = 0

            print("=============================================")
            print("Comparing ", c_file_name, " to ", a_file_name)

            # Filter out archive specific URLS -- UNDO
            #arch_requests_data = list(filter(check_archive_specific_url, arch_requests_data))
            matched_requests = []

            for a_row in arch_requests_data:
                a_url = a_row["url"]
            #print("Archived url: ", a_url)
            #find the matching element in list of current network requests, from here:
            #https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
            #a_row = list(filter(lambda a_request: (c_url in a_request["url"]), arch_requests_data))

                c_row = list(filter(lambda c_request: (fuzz.partial_ratio(a_url.lower(),c_request["url"].lower())>90), curr_requests_data))

                if c_row:
                    print("Match found!")
                    print("Current: ", c_url)
                    print("Archived: ", a_url)
                    c_url = c_row[0]["url"]
                    request_pair = (c_row[0], a_row)
                    matched_requests.append(request_pair)

                    # Checks if status code are different between two requests
                    if find_different_requests(request_pair):
                        num_errors = num_errors + 1

                else:
                    print("Network request not found: ", a_url)
                    missing_requests = missing_requests + 1

            # Number of network requests that have a different status code in archived site vs. current site
            if num_errors > 0:
                print("There are {} requests that have produced errors in the current and archived websites".format(num_errors))
            else:
                print("No differences found")

            #
            if missing_requests > 0:
                print("There are {} requests in the archived site that are not present in the current site".format(missing_requests))
            else:
                print("No missing requests found")

            #what the hell was I thinking?
            #int_correspondence = (len(arch_requests_data)-missing_requests-num_differences)/len(arch_requests_data)
            #int_correspondence_current = (len(arch_requests_data)-missing_requests-num_differences)/len(curr_requests_data)
            print("There are ", len(matched_requests)," requests both in the current and the archived version")

            num_requests_in_common = len(matched_requests)
            if num_requests_in_common!=0:
                requests_with_no_errors = num_requests_in_common - num_errors
                print("Requests with no errors: ", requests_with_no_errors)
                print("No. of requests in common: ", num_requests_in_common)
                ic = requests_with_no_errors/num_requests_in_common
                print("Interactional correspondence: ", ic)
                print("===================================================")
            else:
                print("Interactional correspondence: ", 0)
                print("===================================================")







        except FileNotFoundError:
            print("File Not found: ", arch_requests_path + "/" + a_file_name)
            
        with open(csv_out_name, 'a') as csv_file_out:
            csv_writer = csv.writer(csv_file_out, delimiter=',', quoting=csv.QUOTE_ALL)
            csv_writer.writerow([c_url, c_file_name, a_url, a_file_name, len(curr_requests_data), len(arch_requests_data),
                                 num_requests_in_common, num_errors, ic])
            
            
def parse_args():
    """Parses the command line arguments

    Returns
    -------
    index_file_name : str
        The CSV file that maps the current network requests to their archived counterparts.
    curr_requests_path : str
        The directory containing the CSV files with the current websites' network requests.
    arch_requests_path : str
        The directory containing the CSV files with the archived websites' network requests.
    csv_out_name : str
        The CSV file to write the file with the combined requests.
    do_print : bool
        Whether or not to print the results to stdout.

    """

    parser = argparse.ArgumentParser()

    # initializing every line switch
    parser.add_argument("--index_file", type=str, help="The CSV file that maps the current network requests to their archived counterparts")
    parser.add_argument("--curr_requests", type=str, help="The directory containing the CSV files with the current websites' network requests")
    parser.add_argument("--arch_requests", type=str, help="The directory containing the CSV files with the archived websites' network requests")
    parser.add_argument("--out", type=str, help="The CSV file to write file with the combined requests")
    parser.add_argument("--print_output", action='store_true', help="(optional) Include to print the network requests, default doesn't print")

    args = parser.parse_args()

    # Some parameter checking
    if args.index_file is None:
        print("Must specify an index file\n")
        exit()

    """
    if args.curr_requests is None and args.arch_requests is None:
        print("Must provide input file\n")
        exit()
    """

    if (args.curr_requests is None or args.arch_requests is None):
        print("Must provide both current and archive network requests CSV files\n")
        exit()

    if args.out is None:
        print("Must specify output file\n")
        exit()

    if args.curr_requests is not None and args.arch_requests is not None:
        curr_requests_path = args.curr_requests
        arch_requests_path = args.arch_requests

    index_file_name = args.index_file
    csv_out_name = args.out
    do_print = args.print_output

    return index_file_name, curr_requests_path, arch_requests_path, do_print, csv_out_name

def main():
    index_file_name, curr_requests_path, arch_requests_path, do_print, csv_out_name = parse_args()
    open_with_csv(index_file_name, curr_requests_path, arch_requests_path, csv_out_name, do_print)

main()

