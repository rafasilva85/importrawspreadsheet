import csv
from faker import Faker
import argparse

def generate_random_csv(filename, num_rows=1000):
    """Generate a CSV file with random data."""
    fake = Faker()

    # Define the headers
    headers = ["column1", "column2", "column3"]

    # Open the file and write the data
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the header row

        for _ in range(num_rows):
            row = [
                fake.name(),             # Random name
                fake.job(),              # Random job title
                fake.email()             # Random email
            ]
            writer.writerow(row)  # Write the data row

    print(f"{num_rows} rows of random data written to {filename}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a CSV file with random data.")
    parser.add_argument("filename", type=str, help="The name of the CSV file to create.")
    parser.add_argument("--rows", type=int, default=1000, help="The number of rows to generate (default: 1000).")
    args = parser.parse_args()

    # Generate the CSV file
    generate_random_csv(args.filename, args.rows)