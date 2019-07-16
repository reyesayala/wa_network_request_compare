import sqlite3
import argparse
import csv
from fuzzywuzzy import fuzz


def find_different_requests(request_pair):
	c_request = request_pair[0]
	a_request = request_pair[1]
	c_status = c_request["status_code"]
	a_status = a_request["status_code"]
	
	#we do not consider redirects with status 302 to be errors
	if(c_status!= a_status) and (a_status!="302") and (c_status!="302"):
		#print("Difference found!")
		print(c_request["url"], c_status, a_request["url"], a_status)
		return 1
	else:
		return 0
		

def	open_with_csv(index_file_name, curr_requests_name, arch_requests_name, csv_out_name, do_print):
	"""Parses both	index files	line by	line and writes	the	urls and file names	to the output file.

	Parameters
	----------
	curr_csv_name : str
		The CSV file with	the	current	screenshot index.
	arch_csv_name : str
		The CSV file with	the	archive	screenshots	index.
	csv_out_name :	str
		The CSV file to write	the	urls and file names.
	do_print :	bool
		Whether or not to	print the results to stdout.
		


	"""
	
	#read the index file 
	index_lst = []
	index_file = open(index_file_name, 'r')
	index_reader = csv.reader(index_file, delimiter=',')
	# skip the headers
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
		
		#read the csv files as dicts
		with open(arch_requests_name+"/"+a_file_name) as a_input:
			a_input_file = csv.DictReader(a_input)
			arch_requests_data = [row for row in a_input_file]
		a_input.close()
	
		with open(curr_requests_name+"/"+c_file_name) as c_input:
			c_input_file = csv.DictReader(c_input)
			curr_requests_data = [row for row in c_input_file]
		c_input.close()
		
		num_differences = 0
		missing_requests = 0
		print("Comparing ", c_file_name, " to ", a_file_name)
		
		for a_row in arch_requests_data:
			a_url = a_row["url"]
			#print("Archived url: ", a_url)
			#find the matching element in list of current network requests, from here:
			#https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
			#a_row = list(filter(lambda a_request: (c_url in a_request["url"]), arch_requests_data))
			c_row = list(filter(lambda c_request: (fuzz.partial_ratio(a_url.lower(),c_request["url"].lower())>90), curr_requests_data))
			if c_row: 
				#print("Match found!")
				#print("Current: ", c_url)
				#print("Archived: ", a_row[0]["url"])
				c_url = c_row[0]["url"]
				request_pair = (c_row[0], a_row)
				
				if find_different_requests(request_pair):
					num_differences = num_differences +1
			else:
				print("Archived request not found: ", a_url)
				missing_requests = missing_requests + 1
				
		if num_differences > 0:
			print("There are ", num_differences," differences between the current and archived websites")
		else:
			print("No differences found")
			
		if missing_requests > 0:
			print("There are ", missing_requests," requests in the archived site that are not present in the current site")
		else:
			print("No missing requests found")
			
		int_correspondence = (len(arch_requests_data)-missing_requests-num_differences)/len(arch_requests_data)
		print("Interactional correspondence: ", int_correspondence)
			
		


def	parse_args():
	"""Parses the command line	arguments

	Returns
	-------
	use_csv : bool
		Whether or not the input is a	CSV.
	curr_requests : str
		The CSV file with	the	current	websites' network requests.	
	arch_requests : str
		The CSV file with	the	archived websites' network requests.
	csv_out_name :	str
		The CSV file to write	the	file with the combined requests.
	do_print :	bool
		Whether or not to	print the results to stdout.

	"""

	parser	= argparse.ArgumentParser()

	# initializing	every line switch
	parser.add_argument("--index_file",	type=str, help="The	CSV	file that maps the current network requests to their archived counterparts")
	parser.add_argument("--curr_requests",	type=str, help="The	CSV	file with the current websites'	network	requests")
	parser.add_argument("--arch_requests",	type=str, help="The	CSV	file with the archived websites' network requests")
	parser.add_argument("--out", type=str,	help="The CSV file to write	file with the combined requests")
	parser.add_argument("--print",	action='store_true',
						help="(optional) Include to print	the	network	requests, default doesn't print")

	args =	parser.parse_args()

	# some	parameters checking
	if	args.index_file is	None:
		print("Must specify an index file\n")
		exit()
	if	args.curr_requests is None and args.arch_requests is None:
		print("Must provide input	file\n")
		exit()
	if	(args.curr_requests	is None	or args.arch_requests is None):
		print("Must provide both current and archive network requests	CSV	files\n")
		exit()
	if	args.out is	None:
		print("Must specify output file\n")
		exit()

	if	args.curr_requests is not None and args.arch_requests is not None:
		curr_requests_name = args.curr_requests
		arch_requests_name = args.arch_requests

	index_file_name = args.index_file
	csv_out_name =	args.out
	do_print =	args.print

	return	index_file_name, curr_requests_name,	arch_requests_name,	do_print, csv_out_name


def	main():
	index_file_name, curr_requests_name, arch_requests_name, do_print, csv_out_name	= parse_args()
	open_with_csv(index_file_name, curr_requests_name, arch_requests_name, csv_out_name, do_print)


main()

