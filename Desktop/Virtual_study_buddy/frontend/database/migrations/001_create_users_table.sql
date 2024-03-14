CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    date_of_birth TIMESTAMP,
    profile_picture VARCHAR(255),
    bio VARCHAR(255),
    location VARCHAR(100),
    account_status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    last_updated_at TIMESTAMP DEFAULT NOW(),
    otp_secret VARCHAR(16),
    otp_enabled BOOLEAN DEFAULT FALSE
);