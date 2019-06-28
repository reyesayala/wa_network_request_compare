import sqlite3
import argparse
import csv

def open_with_csv(curr_csv_name, arch_csv_name, csv_out_name, do_print):
    """Parse both index files line by line and writes the urls and file names to the output file.

    Parameter
    ---------
    curr_csv_name : str
        The CSV file with the current URLs index.
    arch_csv_name : str
        The CSV file with the archive URLs index.
    csv_out_name : str
        The CSV file to write the URLs and file names.
    do_print : bool
        Whether or not to print the results to stdout.

    """

    with open(curr_csv_name, 'r') as curr_csv_file:
        curr_csv_reader = csv.reader(curr_csv_file)
        with open(arch_csv_name, 'r') as arch_csv_file:
            arch_csv_reader = csv.reader(arch_csv_file)

            with open(csv_out_name, 'w+') as csv_file_out:
                csv_writer = csv.writer(csv_file_out, delimiter=',', quoting=csv.QUOTE_ALL)
                csv_writer.writerow(['current_url', 'archive_url', 'current_file_name', 'archive_file_name'])

                # Skip header
                next(curr_csv_reader)
                next(arch_csv_reader)
                
                # First row in index files
                crow = next(curr_csv_reader)
                arow = next(arch_csv_reader)

                try:
                    while True:

                        [carchive_id, curl_id, curl] = crow[:3]
                        cextraction_status = crow[-1]
                        [aarchive_id, aurl_id, adate, aurl] = arow[:4]
                        aextraction_status = arow[-1]
                        
                        curl_id = int(curl_id)
                        aurl_id = int(aurl_id)

                        # Increments archive index
                        if curl_id > aurl_id or aextraction_status != "Extraction successful":
                            arow = next(arch_csv_reader)
                        # Increments current index
                        elif curl_id < aurl_id or cextraction_status != "Extraction successful":
                            crow = next(curr_csv_reader)
                        # Found matching url
                        else:
                            current_filename = "{0}.{1}.csv".format(carchive_id, curl_id)
                            archive_filename = "{0}.{1}.{2}.csv".format(aarchive_id, aurl_id, adate)

                            csv_writer.writerow([curl, aurl, current_filename, archive_filename])

                            if do_print:
                                print("{0}, {1}, {2}, {3}".format(curl, aurl, current_filename, archive_filename))
                            # Checks if next element in archive index is the same url captured on a different date
                            arow = next(arch_csv_reader)

                except StopIteration:
                    pass

def open_with_db(csv_out_name, do_print):
    """Gets the url and file names using a sql query and writing it to CSV

    Parameters
    ----------
    csv_out_name : str
        The CSV file to write the URLs and file names.
    do_print : bool
        Whether or not to rpint the results to stdout.

    """

    pass

def parse_args():
    """Parses the command line arguments

    Returns
    -------
    curr_csv_name : str
        The CSV file with the current URLs index.
    arch_csv_name : str
        The CSV file with the archive URLs index.
    csv_out_name : str
        The CSV file to write the URLs and file names.
    use_csv : bool
        Whether or not the input is a CSV.
    use_db : bool
        Whether or not the input is a DB.
    do_print : bool
        Whether or not to print the results to stdout.

    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--currcsv", type=str, help="The CSV file with the current network request index")
    parser.add_argument("--archcsv", type=str, help="The CSV file with the archive network request index")
    parser.add_argument("--db", type=str, help="Input DB file with the URLs")
    parser.add_argument("--out", type=str, help="The CSV file to write the urls and file names")
    parser.add_argument("--print", action='store_true', \
            help="(Optional) Include to print URLs and file names to stdout, default doesn't print")

    args = parser.parse_args()

    # Parameter checks
    if args.currcsv is None and args.archcsv is None and args.db is None:
        print("Must provide input file\n")
        exit()

    if args.db is not None and not (args.currcsv is None and args.archcsv is None):
        print("Must only use one type of input file\n")
        exit()

    if args.db is None and (args.currcsv is None or args.archcsv is None):
        print("Must provide both current and archive index CSV files\n")
        exit()

    if args.out is None:
        print("Must specify output file\n")
        exit()

    if args.currcsv is not None and args.archcsv is not None:
        use_csv = True
    else:
        use_csv = False

    if args.db is not None:
        use_db = True
        connect_sql(args.db)
    else:
        use_db = False

    return args.out, args.currcsv, args.archcsv, use_csv, use_db, args.print

def connect_sql(path):
    """Connects the DB file. """

    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    connection.commit()

def main():
    csv_out_name, curr_csv_name, arch_csv_name, use_csv, use_db, do_print = parse_args()

    if use_csv:
        open_with_csv(curr_csv_name, arch_csv_name, csv_out_name, do_print)
    if use_db:
        open_with_db(csv_out_name, do_print)

main()
