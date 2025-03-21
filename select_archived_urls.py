import csv
import sys
from random import sample
import numpy as np
#from tabulate import tabulate


def find_all_instances(lst, value):
    instances = []
    for i, sublist in enumerate(lst):
        for j, item in enumerate(sublist):
            if item == value:
                instances.append((i, j))
    return instances


#input_csv is the original file with all of the archived URLs
#this file will be sampled rnadom
def main():
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    
    with open(input_csv, 'r') as read_obj: 
    # Return a reader object which will 
    # iterate over lines in the given csvfile 
        csv_reader = csv.reader(read_obj) 
        next(csv_reader, None) # skip header
        
        # convert string to list 
        list_of_csv = list(csv_reader) 
        #print(list_of_csv) 
        
    url_ids = []
        
    for item in list_of_csv:
        url_id = item[1]
        url_ids.append(url_id)
        
    url_ids = list(set(url_ids))
    print(url_ids)
    

#for each seed (archive_id), randomly choose exactly one archived url and write it to output
    with open(output_csv, 'w+') as csv_file_out:
         csv_writer = csv.writer(csv_file_out, delimiter=',', quoting=csv.QUOTE_ALL)
         csv_writer.writerow(["archive_id", "url_id", "date", "archive_url"])
         for id in url_ids:
            answer = find_all_instances(list_of_csv, id)
            random_sample = sample(answer, 1)
            print(random_sample)
            index = random_sample[0][0]
            print(list_of_csv[index][0])
            archive_id = list_of_csv[index][0]
            url_id = list_of_csv[index][1]
            date = list_of_csv[index][2] 
            archive_url = list_of_csv[index][3]
            csv_writer.writerow([archive_id, url_id, date, archive_url])

        
    
          
          
main()
