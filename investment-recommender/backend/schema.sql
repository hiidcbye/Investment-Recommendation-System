CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'medium', 'high')),
    budget INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS investments (
    id SERIAL PRIMARY KEY,
    fund_name VARCHAR(100) UNIQUE,
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'medium', 'high')),
    returns FLOAT,
    min_investment INT,
    category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS recommendation_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    investment_id INT REFERENCES investments(id),
    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
