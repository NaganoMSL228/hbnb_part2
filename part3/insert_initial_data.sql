-- Initial data insertion for HBNB project

-- Insert admin user with fixed UUID if it doesn't exist yet
INSERT OR IGNORE INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    -- bcrypt hash of 'admin1234'
    '$2b$12$tM7G4yColXlSGwokWvRc0u2XGsxzT9EMm.EpzUGb2PFtDIrrHnkEO',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert initial amenities with hardcoded UUIDs (ignore if they already exist)
INSERT OR IGNORE INTO amenities (id, name, created_at, updated_at)
VALUES
    ('a1f7d6c0-36c9-4b12-8407-d1e6c0b1945a', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b2a5e8d1-47de-5c23-951a-e2f7d3c0a85b', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c3b9f2e3-58ef-6d34-a62b-f3g8e4d1b96c', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Display inserted data for verification
SELECT 'Admin user created:' as message;
SELECT id, first_name, last_name, email, is_admin FROM users;

SELECT 'Amenities created:' as message;
SELECT id, name FROM amenities;
