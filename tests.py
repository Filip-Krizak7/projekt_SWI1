import unittest
from xmlrpc.client import boolean

from sqlalchemy import false, true

from hotel_data import get_hotels, create_reservation
from user_registration import get_password_hash
from schemas import SortBy

class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_hotels(self):
        result = True
        if(len(get_hotels("Prague", 1, SortBy.PRICE, 100, 150, "2022-05-06", "2022-05-08", 1, 1, 0)) == 0):
            result = False
            
        self.assertTrue(result)

    def test_false_date_format(self):
        self.assertRaises(ValueError, lambda: create_reservation("petr", "name", "address", 120, "2022/05/06", "2022/05/06", "room", 1))

    def test_hash_password(self):
        self.assertNotEqual(get_password_hash("12345"), "12345")
            

