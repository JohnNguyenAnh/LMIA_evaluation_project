import os
import pandas as pd

# Define a function to clean the data and prepare it for PostgreSQL loading
def clean_csv_files(input_directory, output_directory):
    # Create the output directory if it does not exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through all files in the input directory
    for file_name in os.listdir(input_directory):
        # Check if the file is a CSV
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_directory, file_name)
            try:
                # Load the CSV into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Step 1: Normalize column names (lowercase and replace spaces with underscores)
                df.columns = df.columns.str.lower().str.replace(' ', '_')

                # Step 2: Convert year columns to numeric (remove commas and change type)
                for col in df.columns:
                    if col.isdigit():  # Assuming year columns are named like "2016", "2017", etc.
                        df[col] = df[col].str.replace(',', '').astype(float)

                # Step 3: Strip whitespace from string columns
                str_columns = df.select_dtypes(include='object').columns
                df[str_columns] = df[str_columns].apply(lambda x: x.str.strip())

                # Step 4: Handle missing values (fill with 0 for simplicity)
                df.fillna(0, inplace=True)

                # Save the cleaned DataFrame to the output directory
                cleaned_file_path = os.path.join(output_directory, file_name)
                df.to_csv(cleaned_file_path, index=False)
                
                print(f"Successfully cleaned and saved: {file_name}")
            except Exception as e:
                print(f"Error cleaning {file_name}: {e}")

# Set input and output directories for cleaning
clean_data_input_path = r'C:\Users\Johnn\Desktop\Data Engineer project\LMIA_evaluation_project\clean_data'
clean_data_output_path = r'C:\Users\Johnn\Desktop\Data Engineer project\LMIA_evaluation_project\clean_data'

# Clean the CSV files
clean_csv_files(clean_data_input_path, clean_data_output_path)

# List the cleaned files to confirm successful cleaning
cleaned_files = os.listdir(clean_data_output_path)
cleaned_files