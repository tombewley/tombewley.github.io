

# # Leaflet cluster map of talk locations
#
# (c) 2016-2017 R. Stuart Geiger, released under the MIT license
#
# Run this from the _talks/ directory, which contains .md files of all your talks. 
# This scrapes the location YAML field from each .md file, geolocates it with
# geopy/Nominatim, and uses the getorg library to output data, HTML,
# and Javascript for a standalone cluster map.
#
# Requires: glob, getorg, geopy

import glob
import getorg
from geopy import Nominatim
import datetime
import dateutil.parser as dup

g = glob.glob("*.md")


geocoder = Nominatim()
location_dict = {}
location = ""
link = ""


for file in g:
    with open(file, 'r') as f:
        lines = f.read()

        loc_start = lines.find('location: "') + 11
        lines_trim = lines[loc_start:]
        loc_end = lines_trim.find('"')
        location = lines_trim[:loc_end]

        loc_start = lines.find('title: "') + 8
        lines_trim = lines[loc_start:]
        loc_end = lines_trim.find('"')
        title = lines_trim[:loc_end]

        loc_start = lines.find('date: ') + 6
        lines_trim = lines[loc_start:]
        loc_end = lines_trim.find('\n')
        date = lines_trim[:loc_end]

        loc_start = lines.find('permalink: ') + 12
        lines_trim = lines[loc_start:]
        loc_end = lines_trim.find('\n')
        permalink = lines_trim[:loc_end]

        link = "<br/><a href='https://tombewley.com/"+permalink+"' target='_top'>"+title+"</a>"
        date = "<br/>"+dup.parse(date).strftime("%B %d, %Y")

        location_dict[location+link+date] = geocoder.geocode(location)
        print(location+link+date, "\n", location_dict[location+link+date])

m = getorg.orgmap.create_map_obj()
getorg.orgmap.output_html_cluster_map(location_dict, folder_name="../talkmap", hashed_usernames=False)