from flask import Flask, request, render_template
from requests import get
import json
import re
import shutil
import hashlib

app = Flask(__name__)

def save_messages(info):
    """
    Save the messages to a file.
    :param info: Info to save (list)
    """
    filename = "info.json"
    with open(filename, 'a') as file:
        json.dump(info, file)
    return "Info Saved"

def fetch_search_results(query):
    """  
    Fetch search results for a given query.  

    :param query: Search query string  
    :return: List of search results  
    """
    search = get('https://ddg-api.herokuapp.com/search',
                 params={
                     'query': query,
                     'limit': 3,
                 })

    snippets = ""
    for index, result in enumerate(search.json()):
        snippet = f'[{index + 1}] "{result["snippet"]}" URL:{result["link"]}.'
        snippets += snippet

    response = "Here are some updated web searches. Use this to improve user response:"
    response += snippets

    return [{'role': 'system', 'content': response}]

@app.route('/', methods=['GET', 'POST'])
def search():
    info = None
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            info = fetch_search_results(query)
            save_messages(info)
        for line in info:
            save_data(line)    
    return render_template('search.html', info=info)

# Function to check for duplicate JSON objects
def is_duplicate(data, new_object):
    new_hash = hashlib.sha256(json.dumps(new_object, sort_keys=True).encode()).hexdigest()
    for existing_object in data:
        existing_hash = hashlib.sha256(json.dumps(existing_object, sort_keys=True).encode()).hexdigest()
        if new_hash == existing_hash:
            return True
    return False

# Define a list to store unique JSON objects
@app.route('/json_convert')
def json_convert():
    unique_data = []
    # Open the text file for reading
    with open("info.json", "r") as text_file:
        # Read the content of the file
        file_content = text_file.read()

        # Replace "][" with "],[" to separate the JSON objects with commas
        file_content = file_content.replace("][", "],[")

        # Wrap the content with square brackets to make it a valid JSON array
        json_content = f"[{file_content}]"

        # Parse the JSON data as a list of objects
        data = json.loads(json_content)

        # Iterate through the data and add unique objects to unique_data
        for obj in data:
            if not is_duplicate(unique_data, obj):
                unique_data.append(obj)

        # Save the unique JSON data to a JSON file
        with open("unique_data.json", "w") as json_file:
            json.dump(unique_data, json_file, indent=4)
    shutil.copyfile('unique_data.json', 'templates/unique_data.html')        
    return render_template('unique_data.html')  # Return the HTML template

@app.route('/unique_data', methods=['GET'])
def unique_data():
    return render_template('unique_data.html')  # Return the HTML template

def save_data(line):
    """
    Save the messages to a file.
    :param info: Info to save (list)
    """
    file_name = "info.text"
    with open(file_name, 'a') as file:
        #write the data to a non-json text file
        file.write(line['content'] + '\n')
        return "Info Saved"

@app.route('/info_json', methods=['GET'])
def info_json():
    parsed_data = []

    try:
        # Open the JSON file for reading
        with open("unique_data.json", "r") as file:
            for line in file:
                try:
                    # Attempt to parse each line as a JSON object
                    data = json.loads(line)
                    parsed_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    except FileNotFoundError:
        return "File not found"

    return render_template('info_json.html', parsed_data=parsed_data)

@app.route('/json_html', methods=['GET'])
def json_html():
    return render_template('unique_data.html')

@app.route('/view_text', methods=['GET'])
def view_text():
    parsed_data = []

    # Open the JSON file for reading
    with open("unique_data.json", "r") as file:
        for line in file:
            if len(line) > 10:
                
                # Find the URLs in the text using regular expression
                urls = re.findall(r'(https?://\S+)', line)

                # Create Markdown links for each URL found
                for url in urls:
                    markdown_link = f"[{url}]({url})"
                    line = line.replace(url, markdown_link)
                parsed_data.append(line)
    return render_template('info_json.html', parsed_data=parsed_data)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
