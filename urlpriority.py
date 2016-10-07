import re

# Check from the URL and Hyperlink if a particular link is relevant or not
def check_if_link_relevant(url ,search_string,text):
    isPresent= False
    # If search string present in the link url
    for word in search_string.split():
        if(url.upper().find(word.upper()) >=0):
            isPresent= True
    # If search string present in the link url
    for word in search_string.split():
        if (text.upper().find(word.upper()) >= 0):
            isPresent = True

    return isPresent

#https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/
# Compute the sum of normalized occurences of the search words to get a relevance
def compute_page_Relevance(html_string,search_string):
    html_tag_strpd_text=clean_html_text(html_string)
    relevance=0
    allwordspresent=True
    # Calculate the total normalized frequency of the words in the search string
    for word in search_string.split():
        normcount=0
        normcount=compute_term_frequency(html_tag_strpd_text,word)
        relevance+=normcount
        if(normcount<=0):
            allwordspresent=False
    # If all the search terms are present in the HTML Page
    if(allwordspresent==True):
        relevance+=1
    return relevance

#Computes the normalized non overlapping occurences of a search word
def compute_term_frequency(clean_html_text,search_word):
    #Split the text of the document into words
    normalizeDocument = clean_html_text.lower().split()
    # Get normalized count of the words
    return normalizeDocument.count(search_word.lower()) / float(len(normalizeDocument))


# Strip HTML tags
#http://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def clean_html_text(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
