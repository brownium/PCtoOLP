#!/usr/bin/python

import requests
import openlp
import re
from datetime import datetime
from planningcenter_auth import pco_application_id, pco_secret

def SplitLyricsIntoVerses(lyrics):
    
    # walk through the lyrics, one line at a time
    # if we have a double empty line followed by more than one line, 
    # create a new verse
    
    # the return value will be an array of hashes with 2 elements:  
    # verseTag and raw_slide (matches openLP requirements)
    
    # create a regular expression for potential VERSE,CHORUS tags included
    # inline inside the lyrics... these are on a single line and 
    verseMarkerPattern = re.compile('^(v|verse|c|chorus|b|bridge|prechorus|instrumental|intro|outro|vamp|breakdown|ending|interlude|tag)\s*\d*$',re.IGNORECASE)
    
    lyrics_lines = lyrics.split("\n")
    
    foundEmptyLine = 0
    verseNumber = 1
    verseLines = ''
    outputVerses = []
    verseTagFromLyrics = ''
    nextVerseTagFromLyrics = ''

    for line in lyrics_lines:

        # strip out curly braces and the content inside {}
        line = re.sub('{.*?}+','',line)
        # strip out any extraneous tags <...>
        line = re.sub('<.*?>','',line)
        # remove beginning/trailing whitespace and line breaks
        line = line.rstrip()
        line = line.lstrip()
                
        # if we found any of the verse/chorus markers, 
        # save the text and treat this like a blank line
        if verseMarkerPattern.search(line):
            if len(verseTagFromLyrics):
                nextVerseTagFromLyrics = line
            else:
                verseTagFromLyrics = line
            line=''
                
        if len(line) == 0:
            foundEmptyLine = 1
        
        if foundEmptyLine and len(verseLines):                
            verse = {}
            
            # add verse tags from the lyrics if they are there and
            # reset the verseTagFromLyrics variable
            if len(verseTagFromLyrics):
                verse['verseTag'] = verseTagFromLyrics
                if len(nextVerseTagFromLyrics):
                    verseTagFromLyrics = nextVerseTagFromLyrics
                    nextVerseTagFromLyrics = ''
                else:
                    verseTagFromLyrics = ''
            else:
                verse['verseTag'] = "V{0}".format(verseNumber)
                verseNumber += 1

            verse['raw_slide'] = verseLines
            outputVerses.append(verse)
            
            # reset state variables, including saving this line
            verseLines = line
            foundEmptyLine = 0
        else:       
            if len(verseLines):
                verseLines += "\n" + line
            else:
                verseLines = line
            foundEmptyLine = 0  
            
    # put the very last verseLines into the outputVerses array
    if len(verseLines):
        verse = {}
        if len(verseTagFromLyrics):
            verse['verseTag'] = verseTagFromLyrics
        else:
            verse['verseTag'] = "V{0}".format(verseNumber)
        verse['raw_slide'] = verseLines
        outputVerses.append(verse)
    
    return outputVerses

# Get ServiceTypes

service_types_url = 'https://api.planningcenteronline.com/services/v2/service_types'

service_types = requests.get(service_types_url, auth=(pco_application_id,pco_secret)).json()

index = 0
for service_type in service_types['data']:
    service_type_name = service_type['attributes']['name']
    service_type_url = service_type['links']['self']

    print "{0}\t{1}\t{2}".format(index, service_type_name, service_type_url)
    index += 1

service_index = input("Enter Index (far left number) of Desired Service Type:  ")
service_type_name = service_types['data'][service_index]['attributes']['name']
service_type_url =  service_types['data'][service_index]['links']['self']

# Get service type URL:
service_type = requests.get(service_type_url, auth=(pco_application_id,pco_secret)).json()

# Get plans URL:
service_type_plans_url = service_type['data']['links']['plans']
service_type_plans_url += "?order=-sort_date"

plans = requests.get(service_type_plans_url, auth=(pco_application_id,pco_secret)).json()

index = 0
for plan in plans['data']:
    plan_date = plan['attributes']['dates']
    print "{0}\t{1}".format(index,plan_date)
    index += 1

plan_index = input("Enter Index (far left number) of Desired Plan Date:  ")

# create a YYYYMMDD plan_date
datetime_object = datetime.strptime(plans['data'][plan_index]['attributes']['dates'], '%B %d, %Y' )
plan_date = datetime.strftime(datetime_object, '%Y%m%d')

plan_url = plans['data'][plan_index]['links']['self']

plan_content = requests.get(plan_url, auth=(pco_application_id,pco_secret)).json()

items_url = plan_content['data']['links']['items'] + "?include=song,arrangement"
items = requests.get(items_url, auth=(pco_application_id,pco_secret)).json()

service_manager = openlp.ServiceManager(plan_date)

for item in items['data']:
    item_title = item['attributes']['title']
    print "{0}".format(item_title)

    if item['attributes']['item_type'] == 'song':
        arrangement_id = item['relationships']['arrangement']['data']['id']
        song_id = item['relationships']['song']['data']['id']

        # get arrangement from "included" resources
        arrangement_data = {}
        song_data = {}
        for included_item in items['included']:
            if included_item['type'] == 'Song' and included_item['id'] == song_id:
                song_data = included_item
            elif included_item['type'] == 'Arrangement' and included_item['id'] == arrangement_id:
                arrangement_data = included_item
                
            # if we have both song and arrangement set, stop iterating
            if len(song_data) and len(arrangement_data):
                break
            
        author = song_data['attributes']['author']   
        if author is None:
            author = "Unknown"

        lyrics = arrangement_data['attributes']['lyrics']
        arrangement_updated_at = arrangement_data['attributes']['updated_at']

        # split the lyrics into verses
        verses = []
        verses = SplitLyricsIntoVerses(lyrics)

        song = openlp.Song(item_title,author,verses,arrangement_updated_at)
        service_manager.AddServiceItem(song)

    else:

        custom_slide = openlp.CustomSlide(item_title)
        service_manager.AddServiceItem(custom_slide)

service_manager.WriteOutput()

print "Done"