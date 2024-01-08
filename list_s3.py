import csv
import os
from lib.s3 import *
from dotenv import load_dotenv

def read_processed_files_list(filepath):
    """ Read the processed files list and return a set of tuples with file name and size. """
    processed_files = set()
    with open(filepath, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            if len(row) >= 2:
                processed_files.add((row[0], int(row[1])))
    return processed_files

def main():
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

if __name__ == "__main__":
    main()