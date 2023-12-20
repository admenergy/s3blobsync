import csv
import os
from lib.common import *
from lib.s3 import *
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment
 
def main():
    # Assume the role
    aws_credentials = assume_role(os.getenv('ROLE_ARN_TO_ASSUME'), os.getenv('EXTERNAL_ID'), os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_KEY'))

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)

    # Read the list of already processed files
    processed_files = read_processed_files_list(os.getenv('PROCESSED_FILES_LIST_PATH'))

    # List objects in the S3 bucket
    s3_objects = s3_client.list_objects_v2(Bucket=os.getenv('S3_BUCKET'))['Contents']

    # Create the inventory file
    os.makedirs(os.path.dirname(os.getenv('INVENTORY_LIST_PATH')), exist_ok=True)

    with open(os.getenv('INVENTORY_LIST_PATH'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Filepath', 'File Size (Bytes)', 'Storage Class'])

        # Process each object and write details to the CSV file
        for obj in s3_objects:
            key = obj['Key']
            size = obj['Size']
            storage_class = obj.get('StorageClass', 'STANDARD')  # Default to 'STANDARD' if not os.getenv('specified')

            download_path = os.path.join(os.getenv('LOCAL_DOWNLOAD_PATH'), key)

            # Check if the file is in the processed files list and its storage class
            if (os.path.basename(key), size) not in processed_files:
                # Ensure the directory structure exists before downloading
                directory = os.path.dirname(download_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                download_from_s3(s3_client, os.getenv('S3_BUCKET'), key, download_path)

            # Write the object details to the inventory file
            writer.writerow([os.path.basename(key), download_path, size, storage_class])

if __name__ == "__main__":
    main()
