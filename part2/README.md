# HBNB - Holberton BnB

## Overview

This project is a web application for managing a Bed and Breakfast (BnB) service. It includes functionalities for managing users, places, reviews, and amenities. The application is built using Flask and Flask-RESTx for the API.

## Project Structure
```
part2
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── v1
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hbnb.git
   cd hbnb
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python run.py
```
The server will start, and you can access the API at `http://localhost:5000/api/v1/`.

## API Endpoints
- **Users**: Manage user accounts and authentication.
- **Places**: Manage places and their details.
- **Reviews**: Manage reviews for places.
- **Amenities**: Manage amenities associated with places.

## API Endpoints Details

### User Management API
The User Management API provides endpoints for managing user accounts in the system.

#### Endpoints:
1. **Create User** (POST `/api/v1/users/`)
   - Creates a new user account
   - Request body:
     ```json
     {
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@example.com"
     }
     ```
   - Status codes:
     - 201: User created successfully
     - 400: Email already registered or invalid input

2. **Get All Users** (GET `/api/v1/users/`)
   - Returns a list of all users
   - Status code: 200

3. **Get User by ID** (GET `/api/v1/users/<user_id>`)
   - Returns details of a specific user
   - Status codes:
     - 200: Success
     - 404: User not found

4. **Update User** (PUT `/api/v1/users/<user_id>`)
   - Updates user information
   - Request body: Same as create user
   - Status codes:
     - 200: User updated successfully
     - 404: User not found
     - 400: Invalid input data

### Amenity Management API
The Amenity Management API provides endpoints for managing amenities that can be associated with places.

#### Endpoints:
1. **Create Amenity** (POST `/api/v1/amenities/`)
   - Creates a new amenity
   - Request body:
     ```json
     {
       "name": "Wi-Fi"
     }
     ```
   - Status codes:
     - 201: Amenity created successfully
     - 400: Invalid input data

2. **Get All Amenities** (GET `/api/v1/amenities/`)
   - Returns a list of all amenities
   - Status code: 200

3. **Get Amenity by ID** (GET `/api/v1/amenities/<amenity_id>`)
   - Returns details of a specific amenity
   - Status codes:
     - 200: Success
     - 404: Amenity not found

4. **Update Amenity** (PUT `/api/v1/amenities/<amenity_id>`)
   - Updates amenity information
   - Request body: Same as create amenity
   - Status codes:
     - 200: Amenity updated successfully
     - 404: Amenity not found
     - 400: Invalid input data

## Business Logic
The Business Logic layer is responsible for managing the core functionality of the application. It includes the following entities:

### User
Represents a user in the system.
- **Attributes**: `id`, `name`, `email`, `password`
- **Methods**:
  - `create_user(name, email, password)`: Creates a new user.
  - `get_user(user_id)`: Retrieves a user by ID.

### Place
Represents a place in the system.
- **Attributes**: `id`, `name`, `description`, `location`, `price`
- **Methods**:
  - `create_place(name, description, location, price)`: Creates a new place.
  - `get_place(place_id)`: Retrieves a place by ID.

### Review
Represents a review for a place.
- **Attributes**: `id`, `user_id`, `place_id`, `rating`, `comment`
- **Methods**:
  - `create_review(user_id, place_id, rating, comment)`: Creates a new review.
  - `get_review(review_id)`: Retrieves a review by ID.

### Amenity
Represents an amenity associated with a place.
- **Attributes**: `id`, `name`
- **Methods**:
  - `create_amenity(name)`: Creates a new amenity.
  - `get_amenity(amenity_id)`: Retrieves an amenity by ID.

### Examples
Here are some examples of how the classes and methods can be used:

```python
# Creating a new user
user = User.create_user(name="John Doe", email="john@example.com", password="securepassword")

# Retrieving a user by ID
user = User.get_user(user_id=1)

# Creating a new place
place = Place.create_place(name="Cozy Cottage", description="A cozy cottage in the woods", location="123 Forest Lane", price=100)

# Retrieving a place by ID
place = Place.get_place(place_id=1)

# Creating a new review
review = Review.create_review(user_id=1, place_id=1, rating=5, comment="Amazing place!")

# Retrieving a review by ID
review = Review.get_review(review_id=1)

# Creating a new amenity
amenity = Amenity.create_amenity(name="WiFi")

# Retrieving an amenity by ID
amenity = Amenity.get_amenity(amenity_id=1)
```