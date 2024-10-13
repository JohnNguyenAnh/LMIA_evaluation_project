import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pandas as pd
import psycopg2
from collections import defaultdict

# Database connection setup
user = 'postgres'
password = 'Johnnynguyen08199'
host = 'localhost'
port = '5432'
database = 'postgres'
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
metadata = MetaData()

# Function to automate loading all CSV files in a directory into PostgreSQL
def load_csv_to_postgres(directory):
    # Iterate through all files in the specified directory
    for file_name in os.listdir(directory):
        # Check if the file is a CSV
        if file_name.endswith('.csv'):
            # Generate the table name from the file name (remove the extension)
            table_name = os.path.splitext(file_name)[0]
            
            # Create the full file path
            file_path = os.path.join(directory, file_name)
            
            # Load the CSV into a Pandas DataFrame
            try:
                df = pd.read_csv(file_path)
                # Load the DataFrame into PostgreSQL
                df.to_sql(table_name, con=engine, if_exists='replace', index=False)
                print(f"Successfully loaded data from {file_name} into the {table_name} table.")
            except Exception as e:
                print(f"Error loading {file_name}: {e}")

# Specify the directory containing your CSV files
csv_directory = 'C:\Users\Johnn\Desktop\Data Engineer project\LMIA_evaluation_project\clean_data'  

# Call the function to load all CSVs in the specified directory
load_csv_to_postgres(csv_directory)

# Step 2: Reflect the metadata to get all the table info
metadata.reflect(bind=engine)

# Step 3: Find common columns across all tables
table_columns = {}
for table_name, table in metadata.tables.items():
    table_columns[table_name] = [column.name for column in table.columns]

# Step 4: Identify columns that appear in more than one table
column_frequency = defaultdict(int)
for columns in table_columns.values():
    for column in columns:
        column_frequency[column] += 1

# Columns that appear in more than one table are common columns
common_columns = [column for column, count in column_frequency.items() if count > 1]

print(f"Common Columns: {common_columns}")

# Step 5: Function to create a reference table for each common column
def create_and_populate_reference_table(engine, column_name, metadata):
    reference_table_name = f'{column_name}_reference'

    # Create the reference table dynamically
    reference_table = Table(
        reference_table_name, metadata,
        Column(f'{column_name}_id', Integer, primary_key=True),
        Column(column_name, String, nullable=False)
    )
    
    if not engine.dialect.has_table(engine, reference_table_name):
        reference_table.create(engine)
    
    # Populate the reference table with distinct values from the main tables
    with engine.connect() as connection:
        for table_name in metadata.tables.keys():
            if column_name in table_columns[table_name]:
                insert_query = f"""
                INSERT INTO {reference_table_name} ({column_name})
                SELECT DISTINCT {column_name}
                FROM {table_name}
                WHERE {column_name} IS NOT NULL
                ON CONFLICT DO NOTHING;
                """
                connection.execute(insert_query)

# Create and populate reference tables for each common column
for column_name in common_columns:
    create_and_populate_reference_table(engine, column_name, metadata)

# Step 6: Function to add foreign keys
def add_foreign_keys(engine, column_name, metadata):
    reference_table_name = f'{column_name}_reference' 

    with engine.connect() as connection:
        for table_name in metadata.tables.keys():
            if column_name in table_columns[table_name]:
                # Add new column for the foreign key
                alter_query = f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name}_id INT;
                """
                connection.execute(alter_query)

                # Populate the foreign key column
                update_query = f"""
                UPDATE {table_name}
                SET {column_name}_id = (
                    SELECT {column_name}_id
                    FROM {reference_table_name}
                    WHERE {table_name}.{column_name} = {reference_table_name}.{column_name}
                );
                """
                connection.execute(update_query)

                # Drop the original column
                drop_query = f"""
                ALTER TABLE {table_name}
                DROP COLUMN {column_name};
                """
                connection.execute(drop_query)

                # Add foreign key constraint
                fk_query = f"""
                ALTER TABLE {table_name}
                ADD CONSTRAINT fk_{column_name}
                FOREIGN KEY ({column_name}_id)
                REFERENCES {reference_table_name}({column_name}_id);
                """
                connection.execute(fk_query)

# Add foreign keys for each common column
for column_name in common_columns:
    add_foreign_keys(engine, column_name, metadata)
