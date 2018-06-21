# from openlp import ServiceManager
# print "Hello World!"

import json
import os

from os.path import expanduser
from sys import platform

home = expanduser("~")
OLPRoot = os.path.join(home, "olp")

if not os.path.exists(OLPRoot):
    os.makedirs(os.path.join(home, "olp"))

filename=os.path.join(OLPRoot, "test_openlp.osj")

json_object = None
with open(filename,'r') as f:
    json_object = json.load(f)

# write to a default path with plan_name as the filename
default_path = os.path.join(home, "Documents")
full_path = os.path.join(default_path,"test_openlp_out")

with open(full_path, 'w') as outfile:
    json.dump(json_object, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    print "Wrote Output to {0}".format(full_path) #this is new syntax to me - I would write it as: print "Wrote Output to %s" % (full_path)

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

items_url = plan_content['data']['links']['items']
items = requests.get(items_url, auth=(pco_application_id,pco_secret)).json()

service_manager = openlp.ServiceManager(plan_date)

for item in items['data']:
    item_title = item['attributes']['title']
    print "{0}".format(item_title)

    item_url = item['links']['self']
    item_data = requests.get(item_url, auth=(pco_application_id,pco_secret)).json()

    if item_data['data']['attributes']['item_type'] == 'song':

        arrangement_url = item_data['data']['links']['arrangement']
        arrangement = requests.get(arrangement_url, auth=(pco_application_id,pco_secret)).json()

        song_url = item_data['data']['links']['song']
        song_data = requests.get(song_url, auth=(pco_application_id,pco_secret)).json()
        author = song_data['data']['attributes']['author']

        if author is None:
            author = "Unknown"

        lyrics = arrangement['data']['attributes']['lyrics']
        arrangement_updated_at = arrangement['data']['attributes']['updated_at']

        song = openlp.Song(item_title,author,lyrics,arrangement_updated_at)
        service_manager.AddServiceItem(song)

    else:

        custom_slide = openlp.CustomSlide(item_title)
        service_manager.AddServiceItem(custom_slide)

service_manager.WriteOutput()

print "Done"
