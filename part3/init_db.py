"""
A simpler database initialization script that doesn't rely on FlaskGroup.
Use this if manage.py encounters dependencies issues.
"""

import os
import sys
from app import create_app
from app.extensions import db
from app.models import User, Place, Review, Amenity

def create_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()
    print('Database tables created successfully!')

def drop_db():
    """Drop database tables."""
    with app.app_context():
        db.drop_all()
    print('Database tables dropped successfully!')

def seed_db():
    """Seed database with initial data."""
    with app.app_context():
        # Create users with passwords
        admin = User(first_name="Admin", last_name="User", email="admin@example.com", password="admin123", is_admin=True)
        john = User(first_name="John", last_name="Doe", email="john@example.com", password="johndoe123")
        jane = User(first_name="Jane", last_name="Smith", email="jane@example.com", password="janesmith123")

        db.session.add_all([admin, john, jane])
        # Make sure we flush to generate IDs before referencing them
        db.session.flush()

        print(f"Created users with IDs: {admin.id, john.id, jane.id}")

        # Create amenities
        wifi = Amenity(name="Wi-Fi")
        parking = Amenity(name="Free Parking")
        pool = Amenity(name="Swimming Pool")
        kitchen = Amenity(name="Kitchen")

        db.session.add_all([wifi, parking, pool, kitchen])
        db.session.flush()

        # Create places
        place1 = Place(
            title="Cozy Apartment",
            description="A comfortable apartment in the city center",
            price=100.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner_id=john.id  # Using ID directly instead of object
        )
        place1.add_amenity(wifi)
        place1.add_amenity(kitchen)

        place2 = Place(
            title="Beach House",
            description="Beautiful house with ocean view",
            price=250.0,
            latitude=34.0522,
            longitude=-118.2437,
            owner_id=jane.id  # Using ID directly instead of object
        )
        place2.add_amenity(wifi)
        place2.add_amenity(pool)
        place2.add_amenity(parking)

        db.session.add_all([place1, place2])
        db.session.flush()

        print(f"Created places with IDs: {place1.id, place2.id}")

        # Create reviews - using IDs directly instead of objects
        review1 = Review(
            text="Great place to stay!",
            rating=5,
            user_id=jane.id,
            place_id=place1.id
        )

        review2 = Review(
            text="Wonderful location, very clean.",
            rating=4,
            user_id=john.id,
            place_id=place2.id
        )

        db.session.add_all([review1, review2])
        db.session.commit()

        print('Database seeded with initial data.')

if __name__ == '__main__':
    config_env = os.getenv('FLASK_CONFIG', 'development')
    config_class = f"config.{config_env.capitalize()}Config"
    app = create_app(config_class)

    if len(sys.argv) < 2:
        print("Usage: python init_db.py [create|drop|seed]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'create':
        create_db()
    elif command == 'drop':
        drop_db()
    elif command == 'seed':
        seed_db()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python init_db.py [create|drop|seed]")
