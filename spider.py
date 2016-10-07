from urllib.request import urlopen
from link_finder import LinkFinder
from general import *
from baseurl import *
from urlpriority import *
import sys

class Spider:

    #Class Variables(Shared among all instances)
    project_name= ''
    search_string =''
    domain_name = ''
    queue_file =''
    crawled_file = ''
    api_key=''
    cse_id=''
    queue = dict()
    crawled=dict()
    number_of_links_to_crawl = 0
    links_crawled = 0
    access_order=1
    run_mode='FOCUSED'
    bfs_priority_data=11

    # Initialize the class variables
    def __init__(self, project_name, search_string,api_key,cse_id,number_of_links_to_crawl,allowed_page_depth,run_mode):
        Spider.project_name=project_name
        Spider.search_string=search_string
        Spider.api_key=api_key
        Spider.cse_id=cse_id
        Spider.number_of_links_to_crawl=number_of_links_to_crawl
        Spider.queue_file=Spider.project_name+'/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.crawled_ordered_file=Spider.project_name+ '/crawled_ordered.txt'
        Spider.run_mode=run_mode
        self.boot()
        # If BFS to be run, then get the minimum priority as the API prioritizes on higher priority
        if(Spider.run_mode=='BFS'):
            self.find_priority_value()

    # Generates all the dictionaries and background data required for running the api
    @staticmethod
    def boot():
        # Create the project folder if does not exist
        create_project_dir(Spider.project_name)
        # Create the log files
        create_data_files(Spider.project_name, Spider.search_string, Spider.api_key, Spider.cse_id)
        # Dictionary to contain all the links yet to be crawled
        Spider.queue=file_to_dict(Spider.queue_file)
        # Dictionary to contain all the already crawled links
        Spider.crawled=file_to_dict(Spider.crawled_file)
        # Get the number of already crawled links
        Spider.links_crawled=len(Spider.crawled)
        # Get the maximum access order
        if(len(Spider.crawled)!=0):
            access_order=find_max_access_order(Spider.crawled)
        else:
            access_order=1

    # Used in case of the BFS Crawling. This calculated the minimum priority so that the links generated are picked up in the order they are added
    @staticmethod
    def find_priority_value():
        page_url = find_min_priority(Spider.queue)
        priority_data =Spider.queue[page_url]
        Spider.bfs_priority_data=int(priority_data.priority)

    # Method used to perform the actual crawling, this reads the HTML string, gathers the links in its contents. The url is then removed from the queue and added to the crawled dictionary so that it is not crawled again
    # In the end it updates all the files with the current situation.
    @staticmethod
    def crawl_page():
        # Find the maximum priority so that it can be picked for the crawling
        page_url = find_max_priority(Spider.queue)
        # Fetch data from the dictionary for the page url
        websitedatastore = Spider.queue[page_url]
        # If the page is already not crawled then go ahead with the crawling
        if page_url not in Spider.crawled:
            print('Crawling ' + page_url)
            print('Priority :' + websitedatastore.priority)
            print('Queue: ' + str(len(Spider.queue)) + ' | Crawled: ' + str(Spider.links_crawled))
            print('Reading HTML Page. Please wait....')
            # Add the links from the URL
            Spider.add_links_to_queue(Spider.gather_links(page_url),page_url)
            # Fetch the modified data for the page url from the dictionary
            websitedatastore = Spider.queue[page_url]
            # If the URL is available in the queue then delete it else pass
            if page_url in Spider.queue:
                try:
                    del Spider.queue[page_url]
                except KeyError:
                    print("Exception:crawl_page:" + sys.exc_info())
                    pass
            # Add the page details in the Crawled List
            Spider.crawled[page_url] = websitedatastore
            # Increment the total number of pages crawled
            Spider.links_crawled += 1
            # Update all the files
            Spider.update_files()

    # Method called by crawl_page method, this extracts the HTML body, generates the relevance of the page and then passes the page to the LinkFinder class to fetch all the links in page
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            # Get the details of the Page from the dictionary
            websitedatastore = Spider.queue[page_url]
            # Open the url and get the response
            response = urlopen(page_url)
            # Get the HTML data in bytes and then convert it to string UTF-8 format
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
            # Get the Page Size
            websitedatastore.page_size=len(html_bytes)
            # Compute the relevance of the page
            websitedatastore.relevance=compute_page_Relevance(html_string, Spider.search_string)
            # Assign the access order for the data
            websitedatastore.access_order=Spider.access_order
            Spider.access_order+=1
            # Assign the data back to the dictionary
            Spider.queue[page_url]=websitedatastore
            # If running BFS, then the priority to be the 1 less than the minimum priority so that it is picked up only after all the ones in the queue are completed for all the new links discovered from the page
            if (Spider.run_mode == 'BFS'):
                priority_data = Spider.bfs_priority_data-1
                Spider.bfs_priority_data-=1
            # For Focused crawling, assign the relevance of the parent HTML page to be the priority of the linked URL
            else:
                priority_data=websitedatastore.relevance
            # Pass the HTML data for link gathering
            finder = LinkFinder(page_url, Spider.search_string,str(int(websitedatastore.page_depth)+1),priority_data,Spider.run_mode)
            # Feed the HTML string to the HTML Parser
            finder.feed(html_string)
        except:
            print('Error: Cannot crawl page')
            print("Error: "+str(sys.exc_info()[0])+str(sys.exc_info()[1]))
            return set()
        return finder.page_links()

    # Adds the links returned by the LinkFinder Class to the dictionary
    @staticmethod
    def add_links_to_queue(datastoreset,page_url):
        # Fetch all the links fetched and generate objects
        for datastore in datastoreset:
            if datastore.url in Spider.queue:
                # If Run mode is focused then if any link is pointed by multiple pages then add the priorities
                if Spider.run_mode!='BFS':
                    if datastore.url!=page_url:
                        websitedata = Spider.queue[datastore.url]
                        websitedata.priority = str(float(websitedata.priority) + float(datastore.priority))
                        Spider.queue[datastore.url] = websitedata
                continue
            # If the discovered link is already crawled then ignore
            if datastore.url in Spider.crawled:
                continue
            Spider.queue[datastore.url] = datastore

    # Updates all the files using the content of the dictionaries
    @staticmethod
    def update_files():
        # Write the queue data into the queue.txt
        dict_to_file(Spider.queue, Spider.queue_file)
        # Write the crawled data into the crawled.txt
        dict_to_file(Spider.crawled, Spider.crawled_file)
        # Write the ordered crawled data into crawled_ordered file
        file_to_ordered_file(Spider.crawled_file,Spider.crawled_ordered_file)

    # Checks if the number of crawled pages has exceeded the expected to be crawled page or not
    @staticmethod
    def check_crawled_link_limit():
        if Spider.links_crawled >= Spider.number_of_links_to_crawl:
            return False
        else:
            return True













