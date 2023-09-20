from flask import request, render_template, Blueprint, redirect
from requests import get
import json
import re
import shutil
import hashlib
import os
import logging
from logging.handlers import RotatingFileHandler
import uuid
# Configure this files logger
# Configure logging
current_dir = os.getcwd()+'/api_search/current_directory.log'
#print("Current working directory: {0}".format(current_dir))
# Create a file handler to write log messages to a single file with rotation
file_handler = RotatingFileHandler(current_dir, maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Set the formatter for log messages
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')

file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Example log messages
#logger.debug('This is a debug message')
#logger.info('This is an info message')
#logger.warning('This is a warning message')
#logger.error('This is an error message')
#logger.critical('This is a critical message')

# Now, for the api_search Blueprint, specify its template folder
api_search_bp = Blueprint("api_search", __name__, template_folder="templates", static_folder="static", static_url_path="assets", url_prefix="/api_search")

@api_search_bp.route('/', methods=['GET', 'POST'])
def index():
    logger.info("Starting api_index")
    #logger log current directory
    current_dir = os.getcwd()
    logger.debug("Current_Working_Directory: {0}".format(current_dir))  
    #display my template in api_search/templates/index.html
    return redirect('/api_search/apisearch')

def save_messages(info):
    """
    Save the messages to a file.
    :param info: Info to save (list)
    """
    filename = "api_search/info.json"
    with open(filename, 'a') as file:
        json.dump(info, file)
    logger.info("Info Saved",info)    
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

@api_search_bp.route('/apisearch', methods=['GET', 'POST'])
def apisearch():
    info = None
    cnt=0
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            cnt=cnt+1
            info = fetch_search_results(query)
            save_messages(info)
        for line in info:
            cnt=cnt+100
            save_data(line)
            logger.info("LINE: ",line,cnt)    
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
@api_search_bp.route('/json_convert')
def json_convert():
    unique_data = []
    # Open the text file for reading
    with open("api_search/info.json", "r") as text_file:
        # Read the content of the file
        file_content = text_file.read()
        logger.debug("FILE_CONTENT: ",file_content)
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
        with open("api_search/unique_data.json", "w") as json_file:
            json.dump(unique_data, json_file, indent=4)
            logger.info("UNIQUE_DATA: ",unique_data)
    # Generate a unique filename with a UUID
    unique_id = str(uuid.uuid4()) + '_unique_data.html'

    # Specify the target directory for the new file
    target_directory = 'api_search/templates/'

    # Construct the full path for the new file
    new_file_path = target_directory + unique_id
    # Backup the existing unique_data.html to the new file
    shutil.copyfile('api_search/templates/unique_data.html', new_file_path)
    #copy new data to unique_data.html       
    shutil.copyfile('api_search/unique_data.json', 'api_search/templates/unique_data.html')        
    return render_template('unique_data.html')  # Return the HTML template

@api_search_bp.route('/unique_data', methods=['GET'])
def unique_data():
    #print the current directory
    current_directory = os.getcwd()
    #print("Current working directory: {0}".format(current_directory))
    return render_template('unique_data.html')  # Return the HTML template

def save_data(line):
    """
    Save the messages to a file.
    :param info: Info to save (list)
    """
    file_name = "api_search/info.text"
    with open(file_name, 'a') as file:
        #write the data to a non-json text file
        file.write(line['content'] + '\n')
        return "Info Saved"

@api_search_bp.route('/info_json', methods=['GET'])
def info_json():
    parsed_data = []

    try:
        # Open the JSON file for reading
        with open("api_search/unique_data.json", "r") as file:
            for line in file:
                try:
                    # Attempt to parse each line as a JSON object
                    data = json.loads(line)
                    parsed_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    except FileNotFoundError:
        logger.debug("File_Not_Found")
        return "File not found"
    logger.info("PARSED_DATA: ",parsed_data)
    return render_template('info_json.html', parsed_data=parsed_data)

@api_search_bp.route('/json_html', methods=['GET'])
def json_html():
    return render_template('unique_data.html')

@api_search_bp.route('/view_text', methods=['GET'])
def view_text():
    #print the current directory
    current_directory = os.getcwd()
    print("Current working directory: {0}".format(current_directory))
    parsed_data = []

    # Open the JSON file for reading
    file_name = "api_search/unique_data.json"
    with open(file_name, "r") as file:
        for line in file:
            if len(line) > 10:
                logger.info(line)
                
                # Find the URLs in the text using regular expression
                urls = re.findall(r'(https?://\S+)', line)

                # Create Markdown links for each URL found
                for url in urls:
                    markdown_link = f"[{url}]({url})"
                    line = line.replace(url, markdown_link)
                parsed_data.append(line)
    return render_template('info_json.html', parsed_data=parsed_data)
# Define a function to get the JSON file path
def getfile():
    current_directory = os.getcwd()
    file_name = current_directory + "/api_search/unique_data.json"
    logger.info("File name: %s", file_name)
    return file_name
# Define a function to preprocess the data
def preprocess_data(data):
    processed_data = []
    for item in data:
        if isinstance(item, dict):
            if 'href' in item:
                processed_data.append({'href': item.get('href', ''), 'text': item.get('text', '')})
            else:
                processed_data.append({'text': item.get('text', '')})
        else:
            # Handle cases where item is not a dictionary (e.g., non-dict elements in the list)
            processed_data.append({'text': str(item)})
    return processed_data

# Define a route to display the info
@api_search_bp.route('/info')
def display_info():
    try:
        json_file = getfile()
        logger.info("JSON file: %s", json_file)

        with open(json_file, "r") as file:
            data = json.load(file)
            logger.info("Data from JSON file: %s", data)

        processed_data = preprocess_data(data)

        return render_template('info.html', data=processed_data)

    except Exception as e:
        logger.error("Error: %s", str(e))
        return "An error occurred while processing the data."


