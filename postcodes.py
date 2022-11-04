
#
import urllib.request
import json


def get_postcode():
    postcode = input('start typing your postcode')
    url = 'https://api.postcodes.io/postcodes/{}/autocomplete'.format(postcode)
    response = json.load(urllib.request.urlopen(url))
    print(response['result'])


get_postcode()


