import os
import pandas as pd
from sqlalchemy import create_engine, text

# Database credentials (replace with your own values)
db_config = {
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 5432,
    "database": "your_database"
}

# Create PostgreSQL engine
engine = create_engine(
    f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
)

# SQL commands to create the tables
create_tables_sql = """
-- Create industries table
CREATE TABLE IF NOT EXISTS industries (
    industry_id SERIAL PRIMARY KEY,
    naics_code VARCHAR(10),
    sector_name VARCHAR(255)
);

-- Create regions table
CREATE TABLE IF NOT EXISTS regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(255)
);

-- Create streams table
CREATE TABLE IF NOT EXISTS streams (
    stream_id SERIAL PRIMARY KEY,
    stream_name VARCHAR(255)
);

-- Create noc_levels table
CREATE TABLE IF NOT EXISTS noc_levels (
    noc_id SERIAL PRIMARY KEY,
    noc_code VARCHAR(10),
    occupation VARCHAR(255)
);

-- Create lmia_applications table
CREATE TABLE IF NOT EXISTS lmia_applications (
    application_id SERIAL PRIMARY KEY,
    year INT,
    industry_id INT REFERENCES industries(industry_id),
    region_id INT REFERENCES regions(region_id),
    stream_id INT REFERENCES streams(stream_id),
    noc_id INT REFERENCES noc_levels(noc_id),
    positions_requested INT,
    positions_approved INT
);
"""

# Execute the SQL command to create tables
def create_tables(engine):
    with engine.connect() as conn:
        conn.execute(text(create_tables_sql))
    print("Tables created successfully.")

create_tables(engine)

