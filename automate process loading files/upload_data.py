import psycopg2
import pandas as pd
import os

# Database configuration
db_config = {
    "host": "localhost",
    "dbname": "LMIA_project",
    "user": "postgres",
    "password": "Johnnynguyen08199",
    "port": 5432
}

# Folder path and schema details
folder_path = r"C:\Users\Johnn\Desktop\Data Engineer project\LMIA_evaluation_project\clean_data"
schema = "Schemas"

def upload_csvs_to_pgadmin(folder_path, db_config, schema):
    """
    Uploads multiple CSV files in a folder to PostgreSQL tables within a schema.

    Parameters:
    - folder_path (str): Path to the folder containing CSV files.
    - db_config (dict): Database configuration with keys (host, dbname, user, password, port).
    - schema (str): Schema name.

    Returns:
    - None
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_config["host"],
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"],
            port=db_config["port"]
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Ensure the schema exists
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")

        # Loop through all CSV files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                table_name = os.path.splitext(file_name)[0]  # Use file name as table name

                # Load the CSV into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Sanitize column names (wrap them in double quotes for PostgreSQL)
                sanitized_columns = ", ".join([f'"{col}" TEXT' for col in df.columns])  # Adjust data types as needed

                # Create table based on CSV column names and data types
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
                    {sanitized_columns}
                );
                """
                cursor.execute(create_table_query)

                # Insert data from the DataFrame into the table
                for _, row in df.iterrows():
                    row_values = "', '".join(map(lambda x: str(x).replace("'", "''"), row.values))  # Escape single quotes
                    insert_query = f"""
                    INSERT INTO {schema}.{table_name} VALUES ('{row_values}');
                    """
                    cursor.execute(insert_query)

                print(f"Data from {file_name} successfully uploaded to {schema}.{table_name}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Upload all CSV files in the folder
upload_csvs_to_pgadmin(folder_path, db_config, schema)
