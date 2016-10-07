import threading
from queue import PriorityQueue
from spider import Spider
from general import *
import sys

'''
Values to be passed:
#API_KEY = "AIzaSyD8nw8GEW61I3ShPP79yYwtk1rajNcskos"
#CSE_ID = "003568740217284927586:mgklx_pahbg"
#API_KEY = "AIzaSyCZ6KV8KsaPrIHZcD2q6JoIFIeNezKUDaQ"
#CSE_ID = "016218527239584144410:-xcbtsvw0d0"
'''

# Search String
SEARCH_STRING = "CAT"
# Number of links to crawl
NUMBER_OF_LINKS_TO_CRAWL=30
# Allowed depth of the pages from starting page
ALLOWED_PAGE_DEPTHS=2
# API Key for google custom search
API_KEY ="AIzaSyCZ6KV8KsaPrIHZcD2q6JoIFIeNezKUDaQ"
# Custom search engine ID for google searchs
CSE_ID ="016218527239584144410:-xcbtsvw0d0"
#http://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
# Project name for the project folder name
PROJECT_NAME= ''.join(e for e in SEARCH_STRING if e.isalnum())
# Run mode
RUN_MODE='FOCUSED'

crawl_limit_allowed=True


while(crawl_limit_allowed==True):
    Spider(PROJECT_NAME,SEARCH_STRING,API_KEY,CSE_ID,NUMBER_OF_LINKS_TO_CRAWL,ALLOWED_PAGE_DEPTHS,RUN_MODE)
    Spider.crawl_page()
    crawl_limit_allowed=Spider.check_crawled_link_limit()
