#!/usr/bin/python

import requests
import openlp

# setup PCO login credentials
# this is hardcoded to kirkland's token and secret key
pco_application_id = 'b98e22c011799eebe73facb8e2a54d5143ed1396bd4185176a9d5bcafb9b6c52'
pco_secret = '4ecc64e1a4951c271ebe0e79359020037d8a1627f2301eba93af3084d0a9ff03'

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
plan_date = plans['data'][plan_index]['attributes']['dates']
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

        song = openlp.Song(item_title,author,lyrics,arrangement_updated_at)
        service_manager.AddServiceItem(song)

    else:

        custom_slide = openlp.CustomSlide(item_title)
        service_manager.AddServiceItem(custom_slide)

service_manager.WriteOutput()

print "Done"
