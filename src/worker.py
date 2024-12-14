import boto3
import csv
import os
import psycopg2
from utils.aws_client import get_s3_client
from utils.database import DATABASE_CONFIG

# Create an S3 client
s3_client = get_s3_client()

# Define the directory where files will be temporarily stored
TEMP_DIR = "temp"

# Ensure the TEMP_DIR exists
os.makedirs(TEMP_DIR, exist_ok=True)

def download_file(bucket_name, file_key):
    """
    Download a file from S3 to the local TEMP_DIR.
    """
    local_file_path = os.path.join(TEMP_DIR, file_key)
    s3_client.download_file(bucket_name, file_key, local_file_path)
    print(f"Downloaded file {file_key} from bucket {bucket_name}.")
    return local_file_path

def process_file(bucket_name, file_key):
    """
    Process a CSV file from S3 and insert its rows into the database.
    """
    # Download the file
    file_path = download_file(bucket_name, file_key)

    # Connect to the database
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    try:
        # Read the CSV file and insert rows into the database
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip the header row
            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO my_table (column1, column2, column3, file_key)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (*row, file_key)  # Append the file_key to the row
                )
            conn.commit()
            print(f"File {file_key} processed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error processing file {file_key}: {e}")
    finally:
        cursor.close()
        conn.close()

    # Clean up the local file
    os.remove(file_path)
    print(f"Temporary file {file_path} deleted.")