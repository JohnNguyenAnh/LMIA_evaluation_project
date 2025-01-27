import pandas as pd
from sqlalchemy import create_engine

# Define your Neon PostgreSQL database credentials
username = "LMIA_tables_owner"
password = "0bTSUZwis2Cc"
host = "ep-proud-violet-a5ozki1h.us-east-2.aws.neon.tech"  # typically something like "<project_name>.neon.tech"
dbname = "LMIA_tables"

# Define the path to your CSV file
csv_file_path = r"C:\Users\Johnn\Desktop\Data Engineer project\LMIA_evaluation_project\clean_data"

# Create a connection string
connection_string = f"postgresql+psycopg2://{username}:{password}@{host}/{dbname}"

# Establish a connection to the Neon database
try:
    engine = create_engine(connection_string)
    connection = engine.connect()
    print("Successfully connected to Neon PostgreSQL database!")
except Exception as e:
    print("Error connecting to Neon PostgreSQL database:", e)
    exit()

# Load the CSV file into a Pandas DataFrame
try:
    df = pd.read_csv(csv_file_path)
    print(f"Loaded data from {csv_file_path} successfully!")
except Exception as e:
    print("Error loading CSV file:", e)
    exit()

# Define the target table name in your database
table_name = "your_table_name"

# Upload the DataFrame to the PostgreSQL table
try:
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Data uploaded successfully to table '{table_name}'!")
except Exception as e:
    print("Error uploading data to Neon PostgreSQL database:", e)

# Close the connection
finally:
    connection.close()
    print("Database connection closed.")