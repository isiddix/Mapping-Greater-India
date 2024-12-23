#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importing necessary libraries
# geopy is used for geolocation (Google Maps API is being utilized here)
from geopy.geocoders import GoogleV3

# folium is used to create interactive maps
import folium
from folium.plugins import GroupedLayerControl

# os is used to work with the operating system, such as changing directories
import os

# csv is used for reading data from CSV files
import csv

# numpy is used for mathematical operations, here to calculate quantiles
import numpy as np

# Function to read data from the CSV file and populate lists
def read_data(filename, location_names, location_years, location_frequency):
    # Open and read the file
    file = open(filename, "r", encoding='utf-8')
    data = csv.reader(file)
    for row in data:
        # Skip the header row
        if row != ["year", "place", "times mentioned"]:
            # Populate the respective lists
            location_years.append(row[0])
            location_names.append(row[1].capitalize())  # Capitalize location names
            location_frequency.append(int(row[2]))  # Convert frequency to integer
    file.close()

# Function to create dictionaries for storing location details
def create_name_dictionaries(location_names, location_years, location_frequency, loc_names_and_years, loc_names_and_freqs):
    for i in range(len(location_names)):
        # If the year is already in the dictionary for a location, skip
        if loc_names_and_years[location_names[i]] == [location_years[i]] or location_years[i] in loc_names_and_years[location_names[i]]:
            continue
        else:
            # Otherwise, append the year and frequency
            loc_names_and_years[location_names[i]].append(location_years[i])
            loc_names_and_freqs[location_names[i]].append(location_frequency[i])

# Function to get geographical coordinates for the locations
def geolocate_coordinates(key, location_names, loc_coordinates):
    # Initialize Google Maps geolocator with the provided API key
    app = GoogleV3(
        api_key=key,
        domain="maps.googleapis.com",
    )
    for loc_name in location_names:
        location = app.geocode(loc_name)  # Geocode the location name
        if location:  # If location is found, store its latitude and longitude
            loc_coordinates[loc_name] = (location.latitude, location.longitude)

# Calculate quantiles for the location frequencies
def calculate_quantiles(location_frequency):
    sorted_frequency_list = sorted(location_frequency)  # Sort frequencies
    # Compute quantiles
    q1 = np.quantile(sorted_frequency_list, 0.5)
    q2 = np.quantile(sorted_frequency_list, 0.75)
    q3 = np.quantile(sorted_frequency_list, 0.95)
    q4 = np.quantile(sorted_frequency_list, 1.00)
    return q1, q2, q3, q4

# Initialize FeatureGroups for each year
def initialize_feature_groups(m, location_years, year_feature_groups):
    for year in location_years:
        year_feature_groups[year] = folium.FeatureGroup(name=year, show=True)
        m.add_child(year_feature_groups[year])  # Add the FeatureGroup to the map

# Add a legend to the map to represent quantile-based colors
def create_map_legend(m, colors, color_labels):
    legend_html = f'''
<div style="position: fixed;
     bottom: 50px; left: 50px; width: 200px; height: 125px;
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.85;">
     &nbsp; <b>Legend</b> <br>
     &nbsp; {color_labels[0]} &nbsp; <i class="fa fa-circle" style="color:{colors[0]}"></i><br>
     &nbsp; {color_labels[1]} &nbsp; <i class="fa fa-circle" style="color:{colors[1]}"></i><br>
     &nbsp; {color_labels[2]} &nbsp; <i class="fa fa-circle" style="color:{colors[2]}"></i><br>
     &nbsp; {color_labels[3]} &nbsp; <i class="fa fa-circle" style="color:{colors[3]}"></i><br>
</div>
'''
    m.get_root().html.add_child(folium.Element(legend_html))  # Add legend HTML to the map

# Select marker color based on frequency quantiles
def select_marker_color(total_frequency_count, q1, q2, q3, colors):
    if total_frequency_count <= q1:
        return colors[0]
    elif total_frequency_count <= q2:
        return colors[1]
    elif total_frequency_count <= q3:
        return colors[2]
    else:
        return colors[3]
    
# Pretty print year frequencies for tooltips/popups in the map markers
def pretty_print_yearfreqs(list_of_years, list_of_frequencies):
    container_str = ""
    for i in range(len(list_of_years)):
        container_str += str(list_of_years[i]) + " "
        if list_of_frequencies[i] == 1:
            container_str += "(1 mention), "
        else:
            container_str += "(" + str(list_of_frequencies[i]) + " mentions), "
    container_str = container_str[:-2]  # Remove the last comma and space
    return container_str

# Add markers to the map based on location data
def create_markers(location_years, location_names, loc_coordinates, loc_names_and_years, loc_names_and_freqs, year_feature_groups, q1, q2, q3, colors):
    for i in range(len(location_years)):
        year = location_years[i]
        loc = location_names[i]
        if loc in loc_coordinates:
            years = loc_names_and_years[loc]
            frequencies = loc_names_and_freqs[loc]
            total_frequency_count = sum(frequencies)
            # Create a popup with location details
            popup = folium.Popup('<div style="text-align: center;">{}: {}</div>'.format(loc, pretty_print_yearfreqs(years, frequencies)),
                     min_width=150,
                     max_width=150)
            # Determine marker color
            marker_color = select_marker_color(total_frequency_count, q1, q2, q3, colors)
            # Add the marker to the appropriate FeatureGroup
            folium.Marker(
                location=[loc_coordinates[loc][0], loc_coordinates[loc][1]],
                popup=popup,
                tooltip=loc,
                icon=folium.Icon(color=marker_color)).add_to(year_feature_groups[year])

# Main function to orchestrate the creation of the interactive map
def map_main(directory, filename, key, map_name):
    os.chdir(directory)  # Change to the specified directory

    # Initialize lists for location details
    location_names = []
    location_years = []
    location_frequency = []

    read_data(filename, location_names, location_years, location_frequency)

    # Key: Location Name 
    # Value: List of the years of the articles in which the given location name is mentioned
    loc_names_and_years = {name: [year] for name, year in zip(location_names, location_years)}

    # Key: Location Name 
    # Value: List of the frequencies of location name appearing in each article 
    loc_names_and_freqs = {name: [freq] for name, freq in zip(location_names, location_frequency)}

    #Fills loc_names_and_years and loc_names_and_freqs with appropriate values
    create_name_dictionaries(location_names, location_years, location_frequency, loc_names_and_years, loc_names_and_freqs)

    loc_coordinates = {}  # Dictionary to store coordinates of locations
    geolocate_coordinates(key, location_names, loc_coordinates)  # Fetch coordinates using Google Geolocator Service API Key

    # Initialize the map, zoomed into India
    m = folium.Map(location=(22.31365087985112, 79.54999620079177), zoom_start=5)

    # Compute quantiles for frequency-based marker colors
    q1, q2, q3, q4 = calculate_quantiles(location_frequency)

    # CITE: https://python-visualization.github.io/folium/latest/reference.html
    # You can put things in a FeatureGroup object and handle them as a single layer
    # Create FeatureGroups for each year
    year_feature_groups = {}
    initialize_feature_groups(m, location_years, year_feature_groups)

    # Define marker colors and their legend labels
    colors = ["lightblue", "blue", "darkblue", "black"]
    color_labels = [f"< {q1} (50th quantile)", f"< {q2} (75th quantile)", f"< {q3} (95th quantile)", f"< {q4} (100th quantile)"]
    create_map_legend(m, colors, color_labels)  # Add the legend

    # Add markers to different feature groups based on year, will be displayed on final map
    create_markers(location_years, location_names, loc_coordinates, loc_names_and_years, loc_names_and_freqs, year_feature_groups, q1, q2, q3, colors)

    # CITE: https://python-visualization.github.io/folium/latest/reference.html#folium.plugins.GroupedLayerControl
    # GroupedLayerControl creates a Layer Control with groups of overlays.
    # Add grouped layer control for interactive toggling of years
    GroupedLayerControl(
        groups={'Years': list(year_feature_groups.values())},
        exclusive_groups=False,
        collapsed=False
    ).add_to(m)

    # Save the map to an HTML file
    map_name_final = map_name + ".html"
    m.save(map_name_final)