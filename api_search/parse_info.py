import pprint
import json
import shutil
pp = pprint.PrettyPrinter(indent=4)
# Open the text file for reading
with open("info.text", "r") as text_file:
    # Read the content of the file
    file_content = text_file.read()

    # Replace "][" with "],[" to separate the JSON objects with commas
    file_content = file_content.replace("][", "],[")

    # Wrap the content with square brackets to make it a valid JSON array
    json_content = f"[{file_content}]"

    # Parse the JSON data
    data = json.loads(json_content)

# Now 'data' contains a list of JSON objects
pp.pprint(data)

# Function to check for duplicate JSON objects
def is_duplicate(data, new_object):
    new_hash = hashlib.sha256(json.dumps(new_object, sort_keys=True).encode()).hexdigest()
    for existing_object in data:
        existing_hash = hashlib.sha256(json.dumps(existing_object, sort_keys=True).encode()).hexdigest()
        if new_hash == existing_hash:
            return True
    return False

# Define a list to store unique JSON objects

def json_convert():
    unique_data = []
    # Open the text file for reading
    with open("info.text", "r") as text_file:
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

            unique_data.append(obj)

        # Save the unique JSON data to a JSON file
        with open("unique_data.json", "w") as json_file:
            json.dump(unique_data, json_file, indent=4)
    shutil.copyfile('unique_data.json', 'templates/unique_data.html')        
    return unique_data

