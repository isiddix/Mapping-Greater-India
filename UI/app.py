import eel
import os
import base64
from ocr_multiple_files import ocr_main
from Identify_Loc_Names import nlp_main
from newLocCoord import map_main
from collect_data import count_main

# Setup
current_dir = os.getcwd()
api_dir = os.path.join(current_dir, "uploads")
upload_dir = os.path.join(api_dir, "pdfs")
text_dir = os.path.join(upload_dir, "Text Docs")
map_dir = os.path.join(api_dir, "maps")

# Function to read the api key from the api.txt file
def read_api():
    os.chdir(api_dir)

    with open('api.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    file.close()

    os.chdir(current_dir)

    return content

# Function that deletes everything within a specified directory
def delete_contents(directory_path):
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"The path '{directory_path}' is not a directory.")

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)  # Remove file or symbolic link
        elif os.path.isdir(item_path):
            # Recursively call delete_contents on the subdirectory
            delete_contents(item_path)
            # After the directory is empty, remove it
            os.rmdir(item_path)

# Initialize the eel instance and set the 'web' folder as the location for HTML files
eel.init('web')

# Function that deletes the files within upload_dir
@eel.expose
def delete_files():
    delete_contents(upload_dir)

    return f"Upload folder cleared"

# Function that allows for the changing of the api key
@eel.expose
def change_api(new_key):
    os.chdir(api_dir)

    with open('api.txt', 'w') as file:
        file.write(new_key)

    file.close()

    os.chdir(current_dir)

    return f"API key sucessfully changed"

# Function that creates a xlsx file containing word counts of all text docs currently in the uploads dir
@eel.expose
def count_all():
    count_main(text_dir)

    return f"xlsx file sucessfully created"

# Function to make the map
@eel.expose
def make_map(map_name):

    api_key = read_api()

    filename = "MasterLocationFile.csv"

    map_main(text_dir, filename, api_key, map_name)

    name = map_name + ".html"

    src_path = os.path.join(text_dir, name)

    dst_path = os.path.join(api_dir, 'maps', name)

    os.rename(src_path, dst_path)

    return f"Map: {map_name} sucessfully created"

# Function that retrieves a list of available maps from the maps directory within the uploads directory
@eel.expose
def get_available_maps():
    if not os.path.exists(map_dir):
        return []  # Return an empty list if the maps directory doesn't exist

    # List all HTML files in the maps directory
    map_files = [file for file in os.listdir(map_dir) if file.endswith(".html")]

    # Remove file extensions from the map names
    map_names = [os.path.splitext(file)[0] for file in map_files]

    return map_names

# Function that pulls up the map
@eel.expose
def display_map(selected_map):
    # Construct the full path of the HTML map file
    map_path = os.path.join(map_dir, f"{selected_map}.html")

    # Check if the file exists
    if not os.path.exists(map_path):
        return f"Map '{selected_map}' not found."

    # Open the map file in the default web browser
    import webbrowser
    webbrowser.open(f"file://{map_path}")

    return f"Displaying map: {selected_map}"

# Function that performs ocr on all pdfs of the pdfs folder within the uploads directory
@eel.expose
def process_ocr_directory():

    ocr_main(upload_dir)

    return f"Files sucessfully OCRed"

# Function that performs nlp on all text files of the Text Docs folder within the uploads directory
@eel.expose
def process_nlp_directory():

    nlp_main(text_dir)

    return f"Directory sucessfully NLPed."

# Function that handles uploading files from a specified directory to the directory within the app
@eel.expose
def save_file(filename, binary_data):
    # Decode Base64 data back to binary
    data = binary_data.split(",")[1]
    file_data = base64.b64decode(data)

    # Define full path and save file
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as file:
        file.write(file_data)

    return f"Files, including: '{filename}' saved at: '{file_path}'"


# Start the Eel server to run the HTML file
eel.start('index.html', size=(800, 600), mode='firefox')  # specify 'chrome' or 'firefox'
