from app.extensions import db
from .base_model import BaseModel

class Amenity(BaseModel):
    """Amenity model representing features of places"""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        """Validate the amenity attributes"""
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
        if len(self.name) > 50:
            raise ValueError("Name must be 50 characters or less")