import unittest

from hotel_data import get_hotels, create_reservation
from user_registration import get_password_hash
from schemas import SortBy

class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_false_date_format(self):
        self.assertRaises(ValueError, lambda: create_reservation("petr", "name", "address", 120, "2022/05/06", "2022/05/06", "room", 1))

    def test_hash_password(self):
        self.assertNotEqual(get_password_hash("12345"), "12345")
            

