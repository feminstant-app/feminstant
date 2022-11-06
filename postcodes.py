import urllib.request
import json
#
#
# def get_postcode():
#     postcode = input('start typing your postcode')
#     url = 'https://api.postcodes.io/postcodes/{}/autocomplete'.format(postcode)
#     response = json.load(urllib.request.urlopen(url))
#     print(response['result'])
#
#
# get_postcode()


# # import json
# # import urllib.request
# #
# # api_key = 'ge-c01bb96784d8119e'
# # query = "https://api.geocode.earth/v1/reverse?" \
# #         "api_key="+api_key+"&"\
# #         "point.lat=-22.9519173&" \
# #         "point.lon=-43.2104950"
# #
# # response = json.load(urllib.request.urlopen(query))
# #
# # print(response) # print the entire response
# #
# # print(response['features'][0]['properties']['name'])      # Christ the Redeemer
# # print(response['features'][0]['properties']['label'])
#
#
import random
import pandas
import time

latitude = 12.9716
longitude = 77.5946
file_name = 'data.csv'


def generate_random_data(lat, lon, num_rows, file_name):
    with open(file_name, 'a') as output:
        output.write('timestamp,latitude,longitude\n')
        for _ in range(num_rows):
            time_stamp = time.time()
            generated_lat = random.random() / 100
            generated_lon = random.random() / 100
            output.write("{},{},{}\n".format(time_stamp, lat + generated_lat, lon + generated_lon))


generate_random_data(latitude, longitude, 10, file_name)

import requests

# api-endpoint
URL = "https://revgeocode.search.hereapi.com/v1/revgeocode"

# API key
api_key = 'pk4bs9lmq7kf62vszRwFtm9m9Y4IPRCyk2ZFYMHGrw4'

# Defining a params dictionary for the parameters to be sent to the API
PARAMS = {
    'at': '{},{}'.format(latitude, longitude),
    'apikey': api_key
}

# Sending get request and saving the response as response object
r = requests.get(url=URL, params=PARAMS)

# Extracting data in json format
data = r.json()

# Taking out title from JSON
address = data['items'][0]['title']

print(address)


