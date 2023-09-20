from flask import Flask, request, render_template
from requests import get

app = Flask(__name__)

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
        results.append(result_info)

    return results
    
@app.route('/', methods=['GET', 'POST'])
def index():  
    return render_template('duck_search.html')
    

@app.route('/duck_search', methods=['GET', 'POST'])
def duck_search():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            results = fetch_search_results(query)
    return render_template('duck_search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

