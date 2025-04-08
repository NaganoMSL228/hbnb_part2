-- Sample SQL queries to test the database schema

-- Find all places owned by a specific user
SELECT p.* FROM places p
JOIN users u ON p.owner_id = u.id
WHERE u.email = 'admin@hbnb.io';

-- Find all reviews for a specific place
SELECT r.*, u.first_name, u.last_name
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.place_id = 'place_id_here';

-- Find all places with a specific amenity
SELECT p.* FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE a.name = 'WiFi';

-- Get average rating for a place
SELECT place_id, AVG(rating) as average_rating
FROM reviews
GROUP BY place_id;

-- Get all amenities for a specific place
SELECT a.* FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'place_id_here';
