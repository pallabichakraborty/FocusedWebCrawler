import os
from googlecustomsearch import *
from websitedatastore import *
from queue import PriorityQueue
import sys

# Each search crawled is a separate project (folder)
def create_project_dir(directory):
    # Create a project folder only if it does not exist
    if not os.path.exists(directory):
        print('Creating project:'+directory)
        os.makedirs(directory)

# Create queue and crawled files
def create_data_files(project_name,search_string, api_key, cse_id):
    # Queue file path
    queue=project_name+'/queue.txt'
    # Crawled File path
    crawled = project_name + '/crawled.txt'
    # Path for the crawled data ordered on the basis of the crawling order
    crawled_ordered = project_name + '/crawled_ordered.txt'
    # If the queue file does not exist then create a new file and dump 10 search results
    if not os.path.isfile(queue):
        write_file(queue,google_search(search_string, api_key, cse_id, 10))
    # If the crawled file does not exist then create the file
    if not os.path.isfile(crawled):
        write_file(crawled,'')
    # If the ordered crawled file does not exist then create the file
    if not os.path.isfile(crawled_ordered):
        write_file(crawled_ordered,'')

# Creates a new file
def write_file(file_name,data):
    f=open(file_name,'w')
    f.write(data)
    f.close()

# Add data to an existing file
def append_to_file(file_name,data):
    with open(file_name,'a') as file:
        file.write(data+'\n')

#Delete contents from the file
def delete_file_contents(file_name):
    with open(file_name,'w'):
        pass


# Iterate through a dictionary and write to a file
def dict_to_file(dictname,file_name):
    delete_file_contents(file_name)
    for k,v in dictname.items():
        append_to_file(file_name,str(v))


# Load contents from the file to the python dictionary
def file_to_dict(file_name):
    result=dict()
    with open(file_name, 'rt') as f:
        for line in f:
            #1st item - url
            position=line.find('|')
            url=line[:position]
            # 2nd item - page_size
            line=line[position+1:]
            position = line.find('|')
            page_size = line[:position]
            # 3rd item - page_depth
            line = line[position + 1:]
            position = line.find('|')
            page_depth = line[:position]
            # 4th item - relevance
            line = line[position + 1:]
            position = line.find('|')
            relevance = line[:position]
            # 5th item - priority
            line = line[position + 1:]
            position = line.find('|')
            priority = line[:position]
            # 6th item - access_order
            line = line[position + 1:]
            position = line.find('|')
            access_order = line[:position]
            websitedatastoredata = WebsiteDataStore(url,page_size,page_depth,relevance,priority,access_order)
            result[websitedatastoredata.url]=websitedatastoredata
    return result

# Find the maximum priority in the dictionary
def find_max_priority(dict):
    inv_map = {float(v.priority): k for k, v in dict.items()}
    maxpriority=max(inv_map, key=lambda key: key)
    return inv_map[maxpriority]

# Find the maximum access order in the dictionary
def find_max_access_order(dict):
    inv_map = {float(v.access_order): k for k, v in dict.items()}
    maxpriority=max(inv_map, key=lambda key: key)
    return inv_map[maxpriority]

# Find the minimum priority in the dictionary
def find_min_priority(dict):
    inv_map = {float(v.priority): k for k, v in dict.items()}
    minpriority=min(inv_map, key=lambda key: key)
    return inv_map[minpriority]

# Load a file and generate another file ordered on ascending access order
def file_to_ordered_file(src_file_name,dest_file_name):
    result=dict()
    with open(src_file_name, 'rt') as f:
        for line in f:
            #1st item - url
            position=line.find('|')
            url=line[:position]
            # 2nd item - page_size
            line=line[position+1:]
            position = line.find('|')
            page_size = line[:position]
            # 3rd item - page_depth
            line = line[position + 1:]
            position = line.find('|')
            page_depth = line[:position]
            # 4th item - relevance
            line = line[position + 1:]
            position = line.find('|')
            relevance = line[:position]
            # 5th item - priority
            line = line[position + 1:]
            position = line.find('|')
            priority = line[:position]
            # 6th item - access_order
            line = line[position + 1:]
            position = line.find('|')
            access_order = line[:position]
            websitedatastoredata = WebsiteDataStore(url,page_size,page_depth,relevance,priority,access_order)
            result[int(websitedatastoredata.access_order)]=websitedatastoredata

    delete_file_contents(dest_file_name)
    for k,v in sorted(result.items()):
        append_to_file(dest_file_name, str(v))
