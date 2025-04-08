import unittest
from app.models import Place
from app.extensions import db

class TestPlace(unittest.TestCase):
    def test_create_place(self):
        """Test creating a place with valid data"""
        place = Place(
            title="Test Place",
            description="Test Description",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060
        )
        self.assertEqual(place.title, "Test Place")
        self.assertEqual(place.price, 100.0)

    def test_invalid_price(self):
        """Test that negative price raises error"""
        with self.assertRaises(ValueError):
            Place(
                title="Test Place",
                description="Test Description",
                price=-100.0,
                latitude=40.7128,
                longitude=-74.0060
            )

    def test_invalid_coordinates(self):
        """Test that invalid coordinates raise error"""
        with self.assertRaises(ValueError):
            Place(
                title="Test Place",
                description="Test Description",
                price=100.0,
                latitude=100.0,  # Invalid latitude
                longitude=-74.0060
            )
