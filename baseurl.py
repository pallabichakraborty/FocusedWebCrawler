from urllib.parse import urlparse

#Find domain of a particular site
#http://stackoverflow.com/questions/9626535/get-domain-name-from-url
def find_base_url(url):
    # Compute URI
    parsed_uri = urlparse(url)
    # Compute Domain Name
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain
