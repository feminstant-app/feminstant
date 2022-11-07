import requests
from config import GEOAPIFY_API_KEY


class PostcodeManager:

    def __init__(self):
        self.api_key = GEOAPIFY_API_KEY

    @staticmethod
    def is_valid_postcode(postcode):
        try:
            return requests.get(f'https://api.postcodes.io/postcodes/{postcode}/validate').json()['result']
        except (KeyError, requests.exceptions.RequestException):
            return True  # if the api fails, then don't prevent the user from moving forward

    @staticmethod
    def get_location_from_postcode(postcode):
        try:
            if PostcodeManager.is_valid_postcode(postcode):
                postcode_data = requests.get(f'https://api.postcodes.io/postcodes/{postcode}').json()['result']
                return postcode_data['latitude'], postcode_data['longitude']
            else:
                return None, None
        except (KeyError, requests.exceptions.RequestException):
            return None, None

    def get_address_from_location(self, latitude, longitude):
        try:
            url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&apiKey={self.api_key}"
            data = requests.get(url).json()['features'][0]['properties']
            return data
        except (KeyError, requests.exceptions.RequestException):
            return {}

    def get_street_and_city_from_postcode(self, postcode):
        try:
            data = self.get_address_from_location(*self.get_location_from_postcode(postcode))
            return data['street'], data['city']
        except KeyError:
            return None, None
