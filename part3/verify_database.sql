-- Verification script to check all tables and data

-- Check database structure
SELECT 'Database structure verification:' as message;
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- Check users table
SELECT 'Users in the database:' as message;
SELECT id, first_name, last_name, email, is_admin FROM users;

-- Check amenities table
SELECT 'Amenities in the database:' as message;
SELECT * FROM amenities;

-- Check table structure
SELECT 'Table structure:' as message;
.schema users
.schema places
.schema amenities
.schema reviews
.schema place_amenity

-- Check foreign key constraints
SELECT 'Foreign key constraints:' as message;
PRAGMA foreign_key_list(places);
PRAGMA foreign_key_list(reviews);
PRAGMA foreign_key_list(place_amenity);
