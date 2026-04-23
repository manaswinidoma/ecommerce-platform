CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR (100) UNIQUE NOT NULL,
    password_hash VARCHAR (255) NOT NULL,
    email VARCHAR (255) UNIQUE NOT NULL,
    firstname VARCHAR (100) NOT NULL,
    lastname VARCHAR (100) NOT NULL,
    date_of_birth DATE,
    user_role VARCHAR(100) DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
)
