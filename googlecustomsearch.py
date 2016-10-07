from googleapiclient.discovery import build

# Method to perform Google search and generate 10 top results for a particular search string
def google_search(search_term, api_key, cse_id, numOfResults=10):
    # Create the custom search service
    service = build("customsearch", "v1", developerKey=api_key)
    # Generate the search result
    res = service.cse().list(q=search_term, cx=cse_id, num=numOfResults).execute()
    queryresult=""
    priority=999999
    # Collect the results
    for result in res['items']:
        queryresult=queryresult+result['link']+'|0|0|1|'+str(priority)+'|0\n'
        priority-=1
    return queryresult

