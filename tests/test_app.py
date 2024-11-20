import unittest
from unittest.mock import patch, MagicMock
from main import main
import json
from dataclasses import asdict
from src.models.hotel import Hotel, Amenities

class TestMainApplication(unittest.TestCase):

    def setUp(self):
        self.hotel1 = Hotel(id='1', destination_id=5432, name='Hotel One', description='Desc One',
                            location={}, amenities=Amenities(general=['wifi'], room=['tv']),
                            images={}, booking_conditions=[])
        self.hotel2 = Hotel(id='2', destination_id=5432, name='Hotel Two', description='Desc Two',
                            location={}, amenities=Amenities(general=['pool'], room=['bathtub']),
                            images={}, booking_conditions=[])

    @patch('src.data_integration.supplier_manager.SupplierManager.fetch_and_merge_data')
    @patch('sys.argv', ['main', '1', '5432'])
    def test_filter_by_id_and_destination(self, mock_fetch_and_merge_data):
        # Mock fetch_and_merge_data to return specific test data
        mock_fetch_and_merge_data.return_value = [self.hotel1, self.hotel2]

        with patch('builtins.print') as mocked_print:
            main()
            # Prepare expected output
            expected_hotels = [self.hotel1]
            expected_output = json.dumps([asdict(hotel) for hotel in expected_hotels], indent=2)
            mocked_print.assert_called_once_with(expected_output)

    @patch('src.data_integration.supplier_manager.SupplierManager.fetch_and_merge_data')
    @patch('sys.argv', ['main', 'none', '5432'])
    def test_filter_by_destination_only(self, mock_fetch_and_merge_data):
        # Mock fetch_and_merge_data to return specific test data
        mock_fetch_and_merge_data.return_value = [self.hotel1, self.hotel2]

        with patch('builtins.print') as mocked_print:
            main()
            # Prepare expected output
            expected_hotels = [self.hotel1, self.hotel2]
            expected_output = json.dumps([asdict(hotel) for hotel in expected_hotels], indent=2)
            mocked_print.assert_called_once_with(expected_output)

    @patch('src.data_integration.supplier_manager.SupplierManager.fetch_and_merge_data')
    @patch('sys.argv', ['main', 'none', 'none'])
    def test_no_filters(self, mock_fetch_and_merge_data):
        # Mock fetch_and_merge_data to return specific test data
        mock_fetch_and_merge_data.return_value = [self.hotel1, self.hotel2]

        with patch('builtins.print') as mocked_print:
            main()
            # Prepare expected output
            expected_hotels = [self.hotel1, self.hotel2]
            expected_output = json.dumps([asdict(hotel) for hotel in expected_hotels], indent=2)
            mocked_print.assert_called_once_with(expected_output)

if __name__ == '__main__':
    unittest.main()
