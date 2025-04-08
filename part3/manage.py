import os
import click
from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db
from app.models import User, Place, Review, Amenity

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
cli = FlaskGroup(app)

@cli.command('create_db')
def create_db():
    """Create the database tables."""
    db.create_all()
    click.echo('Database tables created.')

@cli.command('drop_db')
def drop_db():
    """Drop the database tables."""
    db.drop_all()
    click.echo('Database tables dropped.')

@cli.command('seed_db')
def seed_db():
    """Seed the database with initial data."""
    # Create users
    admin = User(first_name="Admin", last_name="User", email="admin@example.com", is_admin=True)
    john = User(first_name="John", last_name="Doe", email="john@example.com")
    jane = User(first_name="Jane", last_name="Smith", email="jane@example.com")

    db.session.add(admin)
    db.session.add(john)
    db.session.add(jane)
    db.session.commit()

    # Create amenities
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Free Parking")
    pool = Amenity(name="Swimming Pool")
    kitchen = Amenity(name="Kitchen")

    db.session.add(wifi)
    db.session.add(parking)
    db.session.add(pool)
    db.session.add(kitchen)
    db.session.commit()

    # Create places
    place1 = Place(
        title="Cozy Apartment",
        description="A comfortable apartment in the city center",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=john
    )
    place1.add_amenity(wifi)
    place1.add_amenity(kitchen)

    place2 = Place(
        title="Beach House",
        description="Beautiful house with ocean view",
        price=250.0,
        latitude=34.0522,
        longitude=-118.2437,
        owner=jane
    )
    place2.add_amenity(wifi)
    place2.add_amenity(pool)
    place2.add_amenity(parking)

    db.session.add(place1)
    db.session.add(place2)
    db.session.commit()

    # Create reviews
    review1 = Review(
        text="Great place to stay!",
        rating=5,
        user=jane,
        place=place1
    )

    review2 = Review(
        text="Wonderful location, very clean.",
        rating=4,
        user=john,
        place=place2
    )

    db.session.add(review1)
    db.session.add(review2)
    db.session.commit()

    click.echo('Database seeded with initial data.')

if __name__ == '__main__':
    cli()
