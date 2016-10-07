from html.parser import HTMLParser
from urllib import parse
from urlpriority import *
from exclusion import *
from baseurl import *
from websitedatastore import *


class LinkFinder(HTMLParser):

    search_string=''
    atag=''
    aattrs=''
    avalue=''

    # Initiate the initializer
    def __init__(self,page_url,search_string,page_depth,priority,run_mode):
        super().__init__()
        self.page_url=page_url
        self.search_string=search_string
        self.links=set()
        self.page_depth=page_depth
        self.priority=priority
        self.run_mode=run_mode

    # Overriding the parent method
    def handle_starttag(self, tag, attrs):
        self.atag =tag
        self.aattrs=attrs

    # Overriding the parent method
    def handle_data(self, data):
        # Fetch the data for the tag
        self.avalue=data
        # Pick up data only for the a tag
        if self.atag == 'a':
            # for the link check for the href attribute
            for (attribute, value) in self.aattrs:
                if attribute == "href":
                    url=value
                    # If BFS do not check for the relevance of the page just perform the robot.txt access check
                    if(self.run_mode=='BFS'):
                        if (value[:2] == "//"):
                            url = "www." + value[2:]
                        # For incomplete urls or relative URLS
                        elif (value[:1] == '/' and value.find('www.') <= 0):
                            url = parse.urljoin(find_base_url(self.page_url), value)
                        # Check robot.txt
                        if check_robot_txt(url,'pallabi-edu-agent'):
                            self.links.add(url)
                    # If BFS do not check for the relevance of the page just perform the robot.txt access check
                    else:
                        # Check for the relevance of the link and hyperlink, if relevant then only go ahead else skip the link
                        if (check_if_link_relevant(value, self.search_string, self.avalue)):
                            if (value[:2] == "//"):
                                url = "www." + value[2:]
                            elif (value[:1] == '/' and value.find('www.')<=0):
                                url = parse.urljoin(find_base_url(self.page_url), value)
                            # Check robot.txt
                            if check_robot_txt(url,'pallabi-edu-agent'):
                                self.links.add(url)

    # Output the page links retrieved by going through the HTML text of the website
    def page_links(self):
        datastoreset=set()
        for link in self.links:
            websitedatastore=WebsiteDataStore(link,0,self.page_depth,0,self.priority,0)
            datastoreset.add(websitedatastore)
        return datastoreset

    #Pass in case of error
    def error(self, message):
        pass



