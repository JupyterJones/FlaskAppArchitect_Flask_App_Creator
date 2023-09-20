import requests
from requests import get

    
def fetch_search_results(query):
    """  
    Fetch search results for a given query using DuckDuckGo API.

    :param query: Search query string  
    :return: List of search results  
    """
    search = get('https://api.duckduckgo.com/',
                 params={
                     'q': query,
                     'format': 'json',
                     'no_redirect': 1,
                     'no_html': 1,
                     'skip_disambig': 'true',
                 })

    results = []
    for index, result in enumerate(search.json().get('Results', [])):
        result_info = {
            'index': index + 1,
            'snippet': result['Text'],
            'link': result['FirstURL']
        }
        print(result_info)
        results.append(result_info)

    return results    


# Example query
query = "What is a famous statue in Europe ?"
search_results = fetch_search_results(query)
print(search_results)
# Print the search results
for index, result in enumerate(search_results, start=1):
    print(f"[{index}] {result.get('Text', '')} URL: {result.get('FirstURL', '')}")

