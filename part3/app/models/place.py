from app.extensions import db
from .base_model import BaseModel

# Association table for place-amenity many-to-many relationship
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place model representing accommodations"""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy='dynamic'))

    def __init__(self, title, description, price, latitude, longitude, owner=None, owner_id=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        if owner:
            self.owner = owner
            self.owner_id = owner.id
        elif owner_id:
            self.owner_id = owner_id

        self.validate_attributes()

    def validate_attributes(self):
        """Validate the place attributes"""
        if not isinstance(self.title, str) or not self.title:
            raise ValueError("Title must be a non-empty string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a non-negative number")
        if not isinstance(self.latitude, (int, float)) or not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be a number between -90 and 90")
        if not isinstance(self.longitude, (int, float)) or not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be a number between -180 and 180")

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)
        db.session.commit()

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            db.session.commit()
