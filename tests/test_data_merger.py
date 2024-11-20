import unittest
from src.models.hotel import *
from src.data_integration.data_merger import merge_hotels, merge_two_hotels, merge_locations, merge_amenities, merge_lists_unique, merge_images

class TestDataMerger(unittest.TestCase):
    def setUp(self):
        # Initialize common objects used across tests
        self.amenities1 = Amenities(general=['wifi', 'breakfast'], room=['tv', 'iron'])
        self.amenities2 = Amenities(general=['pool'], room=['tv', 'hair dryer'])
        self.hotel1 = Hotel(
            id='1', 
            destination_id=5432, 
            name='Hotel Alpha', 
            description='Nice location near the sea.', 
            location={'address': '123 Beach Ave', 'city': 'BeachCity', 'country': 'Beachland', 'lat': 34.123456, 'lng': -45.123456, 'postal_code': '12345'}, 
            amenities=self.amenities1, 
            images= ImageCategory(
                rooms=[Image(link='http://example.com/img1.jpg', description='Room view')],
                site=[],
                amenities=[]
            ),
            booking_conditions=['No pets allowed', 'Check-in after 3 PM']
        )
        self.hotel2 = Hotel(
            id='1', 
            destination_id=5432, 
            name='Hotel Alpha', 
            description='Great spot for family vacations.', 
            location={'address': '123 Beach Ave', 'city': 'BeachCity', 'country': 'Beachland', 'lat': None, 'lng': None, 'postal_code': '12345'}, 
            amenities=self.amenities2, 
            images= ImageCategory(
                rooms=[Image(link='http://example.com/img2.jpg', description='New Room view')],
                site=[],
                amenities=[]
            ),
            booking_conditions=['All children are welcome']
        )

    def test_merge_two_hotels(self):
        merged_hotel = merge_two_hotels(self.hotel1, self.hotel2)
        self.assertEqual(merged_hotel.description, 'Great spot for family vacations.')
        self.assertEqual(len(merged_hotel.amenities.general), 3)
        self.assertEqual(len(merged_hotel.amenities.room), 3)
        self.assertEqual(len(merged_hotel.images.rooms), 2)
        self.assertEqual(len(merged_hotel.booking_conditions), 3)

    def test_merge_locations(self):
        merged_location = merge_locations(self.hotel1.location, self.hotel2.location)
        self.assertEqual(merged_location['lat'], 34.123456)  # Ensure it retains non-None value
        self.assertEqual(merged_location['lng'], -45.123456)  # Ensure it retains non-None value

    def test_merge_amenities(self):
        merged_amenities = merge_amenities(self.amenities1, self.amenities2)
        self.assertIn('wifi', merged_amenities.general)
        self.assertIn('pool', merged_amenities.general)
        self.assertIn('hair dryer', merged_amenities.room)

    def test_merge_lists_unique(self):
        combined_conditions = merge_lists_unique(self.hotel1.booking_conditions, self.hotel2.booking_conditions)
        self.assertEqual(len(combined_conditions), 3)  # Should combine and deduplicate

    def test_merge_images(self):
        additional_images = ImageCategory(
            rooms=[Image(link='http://example.com/img2.jpg', description='New Room view')],
            site=[],
            amenities=[]
        )
        merged_images = merge_images(self.hotel1.images.rooms, additional_images.rooms)
        self.assertEqual(len(merged_images), 2)  # Should add the new image without duplicating the existing one

if __name__ == '__main__':
    unittest.main()
