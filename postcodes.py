import requests


def get_postcode():
    response = requests.get('https://api.postcodes.io/postcodes/:E10AU/nearest')
    postcodes_nearby = response.json()

    return postcodes_nearby


print(get_postcode())


