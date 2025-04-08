from app.extensions import db
from .base_model import BaseModel

class Review(BaseModel):
    """Review model for user reviews of places"""
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def __init__(self, text, rating, place=None, user=None, place_id=None, user_id=None):
        super().__init__()
        self.text = text
        self.rating = rating

        if place:
            self.place = place
            self.place_id = place.id
        elif place_id:
            self.place_id = place_id

        if user:
            self.user = user
            self.user_id = user.id
        elif user_id:
            self.user_id = user_id

        self.validate_attributes()

    def validate_attributes(self):
        """Validate the review attributes"""
        if not isinstance(self.text, str) or not self.text:
            raise ValueError("Text must be a non-empty string")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")