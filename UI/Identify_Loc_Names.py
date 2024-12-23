#Loops through txt files in current directory and enters into MasterLocationFile.txt all location names years and number of references
import spacy
import wikipedia
import os
import en_core_web_sm
import csv

import requests
from bs4 import BeautifulSoup as bsoup
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def set_up_old_name_dictionary():
    "Webscrape to find create a dictionary of old names of locations (keys) and their modern names (values)"
    # ----------------webscraping set-up----------------------
    url = 'https://www.leadthecompetition.in/GK/old-and-new-names-of-cities-in-india.html'
    site = requests.get(url)
    soup = bsoup(site.text, 'html.parser')
    site_txt = soup.get_text()
    old_to_new_names = {}

    # Identify the table or relevant section containing the data
    # Assuming the table rows (<tr>) contain both old and new city names in <td> tags
    table = soup.find('table')  # Assuming there's only one table
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:  # Make sure there are at least 2 columns (old name, new name)
            old_name = cells[2].get_text().strip()  # First column: Old name
            new_name = cells[1].get_text().strip()  # Second column: New name
            old_to_new_names[old_name] = new_name

    #temporary comment bc WebDriver not working

    # Set up the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Navigate to the URL
        driver.get('https://www.nationsonline.org/oneworld/historical_countrynames.htm')

        # Wait for the page to fully load and display the table
        driver.implicitly_wait(5)  # wait for a maximum of 5 seconds

        # Find the table element
        tables = driver.find_elements(By.TAG_NAME, 'table')
        print(f"Number of tables found: {len(tables)}")

        if tables:
            for table in tables[3:]:
                rows = table.find_elements(By.TAG_NAME, 'tr')
                # Extract data from the rows
                for row in rows[2:]:  # Skip header row
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    if len(columns) == 2:  # Check if there are two columns
                        historical_name = columns[0].text.strip()
                        country_name = columns[1].text.strip()
                        old_to_new_names[historical_name] = country_name

            # Output the country names dictionary
            #print(old_to_new_names)

        else:
            print("No tables found on the page.")

    finally:
        # Close the browser
        driver.quit()
    return old_to_new_names

def get_current_name(old_to_new_names, word):
    "Return the current name given a historic name"
    # Iterate through the keys of the dictionary
    for historical_name in old_to_new_names.keys():
        # Check if the key starts with the provided word (case-insensitive)
        if historical_name.lower().startswith(word.lower()):
            return old_to_new_names[historical_name]  # Return the corresponding value
    return None  # Return None if no match is found

def change_ii_to_u(word):
    "Reinterpret ü that scans as ii for words that may have been missinterpreted"
    for index in range(len(word) - 2):
        if word[index] == 'i' and word[index + 1] == 'i':
            new_word = word[:index]
            new_word += 'u'
            new_word += word[index + 2:]
            return new_word
        return word

def to_unique_dict(gpe_list):
    "from a list of all places, get unique items and the number of times each item is mentioned"
    place_dict = {}
    for place in gpe_list:
        if place_dict.get(place) == None:
            place_dict[place] = 0
        place_dict[place] += 1
    return place_dict

#---------------cases for searching for whether a word is a place------------------

def case_1_first_try(place):
    "get summary without auto_suggested page. Used auto_place for spellcheck only"
    page_object = wikipedia.page(place, auto_suggest=True)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(place, sentences = 3, auto_suggest=False))
    place = auto_place
    return place, summary

def case_2a_disambiguation(place):
    "use auto_suggested place with 'the' to increase specificity of the search"
    page_object = wikipedia.page(place, auto_suggest=True)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary("The " + auto_place, sentences = 3, auto_suggest=False)) #creates more specificity. We want the most important noun by t
    return auto_place, summary

def case_2b_disambiguation(place):
    "use auto_suggested place, but don't use 'the'"
    page_object = wikipedia.page(place, auto_suggest=True)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(auto_place, sentences = 3, auto_suggest=False))# Let wikipedia auto suggest something
    place = auto_place
    return place, summary

def case_2ba_2xdisambiguation(place):
    "use 'the' in page suggestion instead of during getting summary"
    page_object = wikipedia.page("The" + place, auto_suggest=True)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(auto_place, sentences = 3, auto_suggest=False))# Let wikipedia auto suggest something
    place = auto_place
    return place, summary

def case_2bb(place):
    "drop auto_suggest on wiki search to avoid dropping letter bug in wikipedia's python library"
    page_object = wikipedia.page(place, auto_suggest=False)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(auto_place, sentences = 3, auto_suggest=False))# Let wikipedia auto suggest something
    place = auto_place
    return place, summary

def case_2bc_disabigaution_after_no_auto(place):
    "drop auto_suggest on wiki search to avoid dropping letter bug in wikipedia's python library"
    "and use 'the' to get specific results"
    page_object = wikipedia.page("the" + place, auto_suggest=False)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(auto_place, sentences = 3, auto_suggest=False))# Let wikipedia auto suggest something
    place = auto_place
    return place, summary

def case_3_other_err(place):
    "use auto_suggested place"
    page_object = wikipedia.page(place, auto_suggest=True)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(auto_place, sentences = 3, auto_suggest=False))# Let wikipedia auto suggest something
    place = auto_place
    return place, summary

def case_3a_the_causes_issue(place):
    "if place starts with 'the' drop 'the' and use auto_suggest"
    page_object = wikipedia.page(place[:4], auto_suggest=True)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(auto_place, sentences = 3, auto_suggest=False))# Let wikipedia auto suggest something
    place = auto_place
    return place, summary

def case_3b_letter_drop_bug(place):
    "use no autosuggest to get correct word. Bug example: China reads as 'Chi a'"
    page_object = wikipedia.page(place, auto_suggest=False)
    auto_place = page_object.original_title
    summary = str(wikipedia.summary(auto_place, sentences = 3, auto_suggest=False))# Let wikipedia auto suggest something
    place = auto_place
    return place, summary

#----------------------------------------------------------------------------------

def reroute_errors_to_get_place_summary(place, other_error, og_place, number_references):
    "through a series of try and catch logic navigates 9 cases that could get the correct value"
    try:
        place, summary = case_1_first_try(place)
    except wikipedia.DisambiguationError:
        try:
             place, summary = case_2a_disambiguation(place)
        except:
            try:
                place, summary = case_2b_disambiguation(place)
            except:
                try:
                    place, summary = case_2ba_2xdisambiguation(place)
                except:
                    try:
                        place, summary = case_2bb(place)
                    except wikipedia.DisambiguationError:
                        try:
                            place, summary = case_2bc_disabigaution_after_no_auto(place)
                        except:
                            other_error.append([og_place, number_references])
                            summary = ''
                    except:
                        other_error.append([og_place, number_references])
                        summary = ''
    except Exception as err:
        try:
            place, summary = case_3_other_err(place)
        except:
            if (place[:4]).lower() == "the ":
                try:
                    place, summary = case_3a_the_causes_issue(place)
                except:
                    summary = ''
                    other_error.append([og_place, number_references])
            else:
                try:
                    place, summary = case_3b_letter_drop_bug(place)
                except:
                    summary = ''
                    other_error.append([og_place, number_references])
    return place, summary, other_error

def sort_through_gpe_list(place_dict, verified_cities, verified_countries, verified_other_places, verified_possibly_places, verified_other_error):
    "sort a list of nlp selected geopolitical locations"
    everything_valid = []
    cities = []
    countries = []
    other_places = []
    possibly_place = []
    other_error = []
    loc_types = ["river ", "state ", "island", "region ", "kingdom ", "land ", "mountain ", "territory "]
    for place in place_dict.keys():
        og_place = place #save info for second chance words
        number_references = place_dict.get(place)
        summary = ''
        print(place)
        if place in verified_cities:
            cities.append(place)
            break
        if place in verified_countries:
            countries.append(place)
            break
        if place in verified_other_places:
            other_places.append(place)
            break
        if place in verified_possibly_places:
            possibly_place.append(place)
            break
        if place in verified_other_error:
            other_error.append(place)
            break
        place, summary, other_error = reroute_errors_to_get_place_summary(place, other_error, og_place, number_references)
        if (summary != ''):
            if ('city ' in summary) or ('village ' in summary) or ('town ' in summary):
                if(place in everything_valid):
                    for index, city_num_pair in enumerate(cities):
                        if (city_num_pair[0] == place):
                            new_num = city_num_pair[1] + number_references
                            cities[index][1] = new_num
                else:
                    everything_valid.append(place)
                    cities.append([place, number_references])
            elif ('country ' in summary):
                if(place in everything_valid):
                    for index, country_num_pair in enumerate(countries):
                        if (country_num_pair[0] == place):
                            new_num = country_num_pair[1] + number_references
                            countries[index][1] = new_num
                else:
                    everything_valid.append(place)
                    countries.append([place, number_references])
            elif True in (ele in summary for ele in loc_types):
                if(place in everything_valid):
                    for index, loc_num_pair in enumerate(other_places):
                        if (loc_num_pair[0] == place):
                            new_num = loc_num_pair[1] + number_references
                            other_places[index][1] = new_num
                else:
                    everything_valid.append(place)
                    other_places.append([place, number_references])
            else:
                possibly_place.append([og_place, number_references]) #gives things that aren't all locations some are peoples or mythological places or religious figures
    return(cities, countries, other_places, possibly_place, other_error)

def give_words_a_second_chance(old_to_new_names, possibly_place, other_error, cities, countries, other_places, verified_cities, verified_countries, verified_other_places, verified_possibly_place, verified_other_error):
    "search output for missspelled or old names, correct and reprocess"
    second_chance_words = []
    second_chance_dict = {}
    for place in other_error:
        if "ii" in place[0]:
            fixed_place = change_ii_to_u(place[0])
            print("from ii")
            second_chance_words.append([fixed_place, place[1]])
    for place in possibly_place:
        new_place = get_current_name(old_to_new_names, place[0])
        if new_place != None:
            second_chance_words.append([new_place, place[1]])
            print("from_new_place")
    for pair in second_chance_words:
        print(pair)
        second_chance_dict[pair[0]] = pair[1]
    #apply old loc to possibly_places here
    cities2, countries2, other_places2, possibly_place2, other_error2 = sort_through_gpe_list(second_chance_dict, verified_cities, verified_countries, verified_other_places, verified_possibly_place, verified_other_error)
    cities += cities2
    countries += countries2
    other_places += other_places2
    return cities, countries, other_places

def write_output(cities, countries, other_places, text_year, file, writer):
    "Add results from a text file to the csv file"
    print(text_year)
    for city in cities:
        row = [text_year, city[0], str(city[1])]
        writer.writerow(row)
    for country in countries:
        row = [text_year, country[0], str(country[1])]
        writer.writerow(row)
    for place in other_places:
        row = [text_year, place[0], str(place[1])]
        writer.writerow(row)

def is_abreviation(word):
    if len(word) >= 4:
        if word[1] == '.' and word[3] == '.':
            return True
    return False

def select_label(title):
    digits = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
    number_found = False
    label = ""
    for letter in title:
        if number_found == False and letter in digits:
            number_found = True
        if number_found == True:
            label += letter
    label = label[:len(label)-11]
    return label

def nlp_main(directory):
    os.chdir(directory)
    #load nlp dictionary and get file directories
    nlp = spacy.load("en_core_web_sm")
    dir_list = os.listdir()
    # Extract old and new names from websites
    old_to_new_names = set_up_old_name_dictionary()
    # For each text file, if it is not the output file, sort out locations Iterating through the directory
    with open("MasterLocationFile.csv", "w",) as file:
        writer = csv.writer(file)
        writer.writerow(["year", "place", "times mentioned"])
        verified_cities = []
        verified_countries = []
        verified_other_error = []
        verified_other_places = []
        verified_possibly_places = []
        for text_file in dir_list:
            length = len(text_file)
            # Make sure file is a text file
            if text_file[length - 4:] == '.txt' and text_file != "MasterLocationFile.txt":
                text_year = select_label(text_file)
                formatted_year = ""
                for letter in text_year:
                    if letter != ' ':
                        formatted_year += letter
                text_year = formatted_year
                text = nlp(open(text_file).read())
                print(text_year)
                gpe = []#geo-political entities labeled by spacy
                loc = []#non-political locations labeled by spacy
                for ent in text.ents:
                    if (ent.label_ == 'LOC' and len(ent.text) > 2):
                        loc.append(ent.text.lower())
                    elif (ent.label_ == 'GPE' and len(ent.text) > 2 and is_abreviation(ent.text) == False): #skip 2 letter words and anything that could turn into a state abreviation
                        gpe.append(ent.text.lower())
                all_places = gpe# + loc
                place_dict = to_unique_dict(all_places)
                cities, countries, other_places, possibly_place, other_error = sort_through_gpe_list(place_dict, verified_cities, verified_countries, verified_other_places, verified_possibly_places, verified_other_error)
                verified_cities += cities
                verified_countries += countries
                verified_other_places += other_places
                verified_possibly_places += possibly_place
                verified_other_error += other_error
                cities, countries, other_places = give_words_a_second_chance(old_to_new_names, possibly_place, other_error, cities, countries, other_places, verified_cities, verified_countries, verified_other_places, verified_possibly_places, verified_other_error)
                write_output(cities, countries, other_places, text_year, file, writer)
