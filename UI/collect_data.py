# Script that scans each text document in the directory and then compiles the data into a excel sheet

import os
import collections
import re
import pandas as pd

# Function that saves the given data to an xlsx file
def save_to_excel(word_count, output_file):
    # Convert Counter to DataFrame
    df = pd.DataFrame(word_count.items(), columns=['Word', 'Count'])
    
    # Save to Excel
    df.to_excel(output_file, index=False)


def count_main(directory):

    os.chdir(directory)
    # Grab the current directory
    dir_list = os.listdir()

    # Initialize counter for words
    word_count = collections.Counter()

    # Iterate through the directory
    for i in dir_list:
        length = len(i)
        # Make sure file is a txt document
        if i[length - 4:] == '.txt':
            current_file = open(i, encoding="utf8")

            # Get data from file
            data = current_file.read()

            current_file.close()

            # Find all 'words' in the file
            words = re.findall(r'\b\w+\b', data.lower())

            # Add found words to counter
            word_count.update(words)

    # Save as xlsx file
    save_to_excel(word_count, "FullWordCount.xlsx")
