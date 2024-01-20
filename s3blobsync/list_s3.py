import argparse
import csv
import os
from pathlib import Path
from .lib.s3 import *
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description='Blob Sync Script')
    parser.add_argument('--env-file', type=str, default='.env', help='Path to the .env file')
    return parser.parse_args()

def list_s3(env_file='.env'):
    env_path = Path(env_file)
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path, override=True)
        print(f"Loaded environment variables from {env_path}.")
    else:
        print(f"Warning: '.env' file not found at {env_path}.")

    # Assume the role
    aws_credentials = assume_role(os.getenv('ROLE_ARN_TO_ASSUME'), os.getenv('EXTERNAL_ID'), os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_KEY'))

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)

    # List objects in the S3 bucket
    s3_objects = s3_client.list_objects_v2(Bucket=os.getenv('S3_BUCKET'))['Contents']

    # Create the inventory file directory if it doesn't exist
    os.makedirs(os.path.dirname(os.getenv('INVENTORY_LIST_PATH')), exist_ok=True)

    # Open the inventory CSV file to write
    with open(os.getenv('INVENTORY_LIST_PATH'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Filepath', 'File Size (Bytes)', 'Storage Class'])

        # Process each object and write details to the CSV file
        for obj in s3_objects:
            key = obj['Key']
            size = obj['Size']
            storage_class = obj.get('StorageClass', 'STANDARD')  # Default to 'STANDARD' if not specified

            # Generate the local download path (for inventory purposes only)
            download_path = os.path.join(os.getenv('LOCAL_DOWNLOAD_PATH'), key)

            # Write the object details to the inventory file
            writer.writerow([os.path.basename(key), download_path, size, storage_class])

            # Note: The download process has been removed from this script.

def main():
    args = parse_args()
    download_from_s3(patterns=args.patterns, env_file=args.env_file)

if __name__ == "__main__":
    main()