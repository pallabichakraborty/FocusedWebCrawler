#Object to hold the website details
class WebsiteDataStore(object):

    # Initialize the class
    def __init__(self,url,page_size,page_depth,page_relevance,priority,access_order):
        self.url=url
        self.page_size=page_size
        self.page_depth=page_depth
        self.relevance=page_relevance
        self.priority=priority
        self.access_order=access_order

    # Format the way the class object data to output when converted to string format
    def __str__(self):
        return self.url+'|'+str(self.page_size)+'|'+str(self.page_depth)+'|'+str(self.relevance)+'|'+str(self.priority)+'|'+str(self.access_order)