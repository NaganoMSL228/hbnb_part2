from .base_model import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        # Validate attributes
        self.validate_attributes()

    def validate_attributes(self):
        if not isinstance(self.text, str) or not self.text:
            raise ValueError("Text must be a non-empty string")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not isinstance(self.place, Place):
            raise ValueError("Place must be an instance of Place")
        if not isinstance(self.user, User):
            raise ValueError("User must be an instance of User")