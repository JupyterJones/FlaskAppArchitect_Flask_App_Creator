from flask import Flask, request, render_template, jsonify
from requests import get
import pprint
app = Flask(__name__)
# Create a PrettyPrinter object
pp = pprint.PrettyPrinter(indent=4)
def fetch_search_results(query):
    search = get('https://ddg-api.herokuapp.com/search',
                 params={
                     'query': query,
                     'limit': 4,
                 })

    results = []
    for index, result in enumerate(search.json()):
        result_info = {
            'index': index + 1,
            'snippet': result['snippet'],
            'link': result['link']
        }
        results.append(result_info)

    # Pretty-print the dictionary
    pp.pprint(results)
    return results

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
 

