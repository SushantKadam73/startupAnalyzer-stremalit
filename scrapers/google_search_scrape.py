from googlesearch import search

def google_search(query):
    google_urls=[]
    for j in search(query,num_results=5):
        google_urls.append(j)
    return google_urls

    