import pandas as pd
import os

# Define the folder where your cleaned CSV files are stored
folder_path = "C:/Users/Johnn/Desktop/Data Engineer project/LMIA_evaluation_project/clean_data"
# Load each CSV file in the folder into a DataFrame and perform consistency checks
data_summary = {}

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path)
            # Summary: File name and the first few rows
            print(f"--- Summary for {filename} ---")
            print(df.head(), "\n")
            
            # Check for missing values
            missing_values = df.isnull().sum()
            print(f"Missing Values for {filename}:")
            print(missing_values[missing_values > 0], "\n")
            
            # Data types summary
            print(f"Data Types for {filename}:")
            print(df.dtypes, "\n")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")