import logging
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.extensions import db
from app.services.repositories.user_repository import UserRepository

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HBnBFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # Replace generic repository with specialized UserRepository
            self.user_repo = UserRepository()
            # Keep other repositories as-is
            self.place_repo = SQLAlchemyRepository(Place)
            self.amenity_repo = SQLAlchemyRepository(Amenity)
            self.review_repo = SQLAlchemyRepository(Review)
            self._initialized = True

    # Update user-related methods to use the specialized repository

    def create_user(self, user_data):
        logger.debug(f"Creating user with data: {user_data}")
        # Extract the password before creating the user
        password = user_data.pop('password', None)

        # Create user instance
        user = User(**user_data)

        # Hash the password if provided
        if password:
            user.hash_password(password)

        user.validate()
        self.user_repo.add(user)
        logger.debug(f"User created with ID: {user.id}")
        return user

    def get_user(self, user_id):
        logger.debug(f"Looking for user with ID: {user_id}")
        user = self.user_repo.get(user_id)
        if user:
            logger.debug(f"Found user: {user.first_name} {user.last_name}")
        else:
            logger.debug("User not found")
        return user

    def get_user_by_email(self, email):
        # Use the specialized method instead of get_by_attribute
        return self.user_repo.get_by_email(email)

    def get_all_users(self):
        """Retrieve all users from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user with new data"""
        user = self.get_user(user_id)
        if not user:
            return None

        # Handle password update separately
        password = user_data.pop('password', None)
        if password:
            user.hash_password(password)

        # Update other fields
        for key, value in user_data.items():
            if hasattr(user, key) and key != 'password':
                setattr(user, key, value)

        # Save changes
        db.session.commit()
        return user

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        if len(amenity_data['name']) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        if 'name' in amenity_data and len(amenity_data['name']) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
        return self.amenity_repo.update(amenity_id, amenity_data)

    def create_place(self, place_data):
        logger.debug(f"Attempting to create place with data: {place_data}")

        # Extract owner_id and amenities from place_data
        owner_id = place_data.pop('owner_id', None)
        amenities_ids = place_data.pop('amenities', [])

        if not owner_id:
            raise ValueError("owner_id is required")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"User with id {owner_id} not found")

        try:
            # Create place with core data
            place = Place(
                **place_data,
                owner=owner
            )

            # Add amenities after place creation
            for amenity_id in amenities_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
                else:
                    logger.warning(f"Amenity {amenity_id} not found")

            self.place_repo.add(place)
            logger.debug(f"Place added to repository with owner {owner.id}")

            return place

        except Exception as e:
            logger.error(f"Error creating place: {str(e)}")
            raise ValueError(str(e))

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        try:
            # Handle special relationships separately
            if 'owner_id' in place_data:
                owner = self.user_repo.get(place_data['owner_id'])
                if not owner:
                    raise ValueError(f"Owner with id {place_data['owner_id']} not found")
                place.owner = owner
                place_data.pop('owner_id')

            if 'amenities' in place_data:
                amenity_ids = place_data.pop('amenities')
                # Clear existing amenities
                place.amenities = []
                # Add new amenities
                for amenity_id in amenity_ids:
                    amenity = self.amenity_repo.get(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)

            # Update regular attributes
            for key, value in place_data.items():
                setattr(place, key, value)

            # Save changes
            db.session.commit()
            return place

        except Exception as e:
            logger.error(f"Error updating place: {str(e)}")
            db.session.rollback()
            raise ValueError(str(e))

    def create_review(self, review_data):
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")

        user_id = review_data.pop('user_id', None)
        place_id = review_data.pop('place_id', None)

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(
            **review_data,
            user=user,
            place=place
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, review_data):
        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    def is_valid_email(self, email):
        """Validate email format"""
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def has_user_reviewed_place(self, user_id, place_id):
        """Check if a user has already reviewed a place"""
        reviews = self.get_reviews_by_place(place_id)
        for review in reviews:
            if review.user.id == user_id:
                return True
        return False