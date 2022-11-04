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

# import requests
#
# url = "https://uk-address-and-postcodes.p.rapidapi.com/rapidapi/v1/autocomplete/addresses"
#
# querystring = {"query":"Oxford street, Soho"}
#
# headers = {
# 	"X-RapidAPI-Key": "3802d17ac5msh1840dc36a2001b8p14d2cfjsneb24ecd19966",
# 	"X-RapidAPI-Host": "uk-address-and-postcodes.p.rapidapi.com"
# }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
#
# print(response.text)

# from urllib.parse import quote
# import requests
# import json
#
# # Request parameters
# api_key = "PCW45-12345-12345-1234X"
# country_code = "UK"
# search_term = "NR14 7PZ"
#
# # Prepare request and encode user-entered parameters with %xx encoding
# request_url = f"https://ws.postcoder.com/pcw/{api_key}/address/{country_code}/{quote(search_term, safe='')}"
#
# # Send request
# response = requests.get(request_url)
#
# # Process response
# if response.status_code == 200:
#     json = response.json()
#     if len(json) > 0:
#         for address in json:
#             print(address["summaryline"])
#     else:
#         print("No results")
# else:
#     print(f"Request error: {response.content.decode()}")
