import csv
import os
from lib.aws import *
from config import *

def read_processed_files_list(filepath):
    #Read or create the processed files list and return a set of tuples with file name and size.
    processed_files = set()
    
    # Check if file exists, if not, create it with a header
    if not os.path.isfile(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Filename', 'File Size'])

    with open(filepath, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            if len(row) >= 2:
                processed_files.add((row[0], int(row[1])))
    return processed_files

def main():
    # Assume the role
    aws_credentials = assume_role(ROLE_ARN_TO_ASSUME, EXTERNAL_ID, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)

    # Read the list of already processed files
    processed_files = read_processed_files_list(PROCESSED_FILES_LIST_PATH)

    # List objects in the S3 bucket
    s3_objects = s3_client.list_objects_v2(Bucket=S3_BUCKET)['Contents']

    # Create the inventory file
    os.makedirs(os.path.dirname(INVENTORY_LIST_PATH), exist_ok=True)

    with open(INVENTORY_LIST_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Filepath', 'File Size (Bytes)', 'Storage Class'])

        # Process each object and write details to the CSV file
        for obj in s3_objects:
            key = obj['Key']
            size = obj['Size']
            storage_class = obj.get('StorageClass', 'STANDARD')  # Default to 'STANDARD' if not specified

            download_path = os.path.join(LOCAL_DOWNLOAD_PATH, key)

            # Check if the file is in the processed files list and its storage class
            if (os.path.basename(key), size) not in processed_files and storage_class not in ['GLACIER', 'DEEP_ARCHIVE']:
                # Ensure the directory structure exists before downloading
                directory = os.path.dirname(download_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                download_from_s3(s3_client, S3_BUCKET, key, download_path)

            # Write the object details to the inventory file
            writer.writerow([os.path.basename(key), download_path, size, storage_class])

if __name__ == "__main__":
    main()
