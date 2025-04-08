import unittest
from app.models import Amenity

class TestAmenity(unittest.TestCase):
    def test_create_amenity(self):
        """Test creating an amenity with valid data"""
        amenity = Amenity(name="WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_empty_name(self):
        """Test that empty name raises error"""
        with self.assertRaises(ValueError):
            Amenity(name="")
