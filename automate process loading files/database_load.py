import pandas as pd
import os
from sqlalchemy import create_engine

# Database connection setup
user = 'postgres'  # Replace with your PostgreSQL username
password = 'Johnnynguyen08199'  # Replace with your PostgreSQL password
host = 'localhost'  # Replace with your PostgreSQL host (usually localhost)
port = '5432'  # Replace with your PostgreSQL port (default is 5432)
database = 'project'  # Replace with the name of your database

# Create a connection engine using SQLAlchemy
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

# Directory containing cleaned CSV files
cleaned_data_path = r'C:/Users/Johnn/Desktop/Data Engineer project/LMIA_evaluation_project/clean_data'

# Debugging: Check if the directory exists
print(f"Directory path being used: {cleaned_data_path}")
if not os.path.exists(cleaned_data_path):
    print("Directory does not exist!")
else:
    print("Directory exists.")

# Debugging: Print all files in the directory
print("Files in the directory before processing:")
file_list = os.listdir(cleaned_data_path)
if len(file_list) == 0:
    print("No files found in the directory.")
else:
    for file_name in file_list:
        print(file_name)

# Function to load CSV files into PostgreSQL
def load_csv_to_postgres(directory, engine):
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            # Create a table name from the file name (without extension)
            table_name = os.path.splitext(file_name)[0].lower()  # Convert to lowercase for compatibility
            
            print(f"Attempting to load file: {file_name} into table: {table_name}")

            try:
                # Load CSV into a DataFrame
                df = pd.read_csv(file_path)
                
                # Debugging: Print DataFrame info to confirm content
                print(f"Loading data from: {file_name}")
                print(df.head())  # Print the first few rows to verify
                
                # Load the DataFrame to PostgreSQL as a table
                df.to_sql(table_name, con=engine, if_exists='replace', index=False)
                print(f"Successfully loaded '{file_name}' into PostgreSQL as table '{table_name}'")
            except Exception as e:
                print(f"Error loading file '{file_name}': {e}")

# Run the function to load all cleaned CSV files
load_csv_to_postgres(cleaned_data_path, engine)