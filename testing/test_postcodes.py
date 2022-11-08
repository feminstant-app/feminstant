from unittest import TestCase, main
from utils.postcodes import PostcodeManager


class TestPostcodeManager(TestCase):

    def test_is_valid_postcode_with_valid_postcode(self):
        postcode_manager = PostcodeManager()
        test_postcode = 'CM2 9ES'
        result = postcode_manager.is_valid_postcode(test_postcode)
        self.assertTrue(result)

    def test_is_valid_postcode_with_invalid_postcode(self):
        postcode_manager = PostcodeManager()
        test_postcode = 'AB1 2DF'
        result = postcode_manager.is_valid_postcode(test_postcode)
        self.assertFalse(result)

    def test_get_location_from_postcode(self):
        postcode_manager = PostcodeManager()
        test_postcode = 'CM2 9ES'
        latitude, longitude = postcode_manager.get_location_from_postcode(test_postcode)
        self.assertEqual((round(latitude, 2), round(longitude, 2)), (51.72, 0.47))

    def test_get_address_from_location(self):
        postcode_manager = PostcodeManager()
        test_latitude = 51.71856
        test_longitude = 0.47043
        result = postcode_manager.get_address_from_location(test_latitude, test_longitude)
        self.assertEqual(result['street'], 'Brian Close')
        self.assertEqual(result['city'], 'Chelmsford')

    def test_street_and_city_from_postcode(self):
        postcode_manager = PostcodeManager()
        test_postcode = 'CM2 9ES'
        street, city = postcode_manager.get_street_and_city_from_postcode(test_postcode)
        self.assertEqual(street, 'Brian Close')
        self.assertEqual(city, 'Chelmsford')


if __name__ == '__main__':
    main()
