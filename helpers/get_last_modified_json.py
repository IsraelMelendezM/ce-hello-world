import os, json

def get_last_modified_json(folder_path):
    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Filter for JSON files
    json_files = [f for f in files if f.lower().endswith('.json')]

    if not json_files:
        print("No JSON files found in the folder.")
        return None

    # Get the most recently modified JSON file
    last_modified_json = max(json_files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))

    # Read the JSON file into memory
    json_file_path = os.path.join(folder_path, last_modified_json)
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    return data
