import unittest
from app.models import Review

class TestReview(unittest.TestCase):
    def test_create_review(self):
        """Test creating a review with valid data"""
        review = Review(text="Great place!", rating=5)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)

    def test_invalid_rating(self):
        """Test that invalid rating raises error"""
        with self.assertRaises(ValueError):
            Review(text="Great place!", rating=6)

    def test_empty_text(self):
        """Test that empty text raises error"""
        with self.assertRaises(ValueError):
            Review(text="", rating=5)
