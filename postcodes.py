# import json
# import urllib.request
#
#
# api_key = 'ge-01af88a050253ba8'
#
#
# def extract_postcode_via_auto_type():
#         text = input("Type a city")
#         endpoint = "https://api.geocode.earth/v1/autocomplete?" \
#                     "api_key="+api_key+"&"\
#                     "text={}".format(text)
#         response = json.load(urllib.request.urlopen(endpoint))
#         print(response['features'][0]['properties']['label'])
#
#
# extract_postcode_via_auto_type()
#
#
#
import urllib.request
import json


def get_postcode():
    postcode = input('start typing your postcode')
    url = 'https://api.postcodes.io/postcodes/{}/autocomplete'.format(postcode)
    response = json.load(urllib.request.urlopen(url))
    print(response['result'])


get_postcode()

