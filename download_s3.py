import argparse
import csv
import os
from lib.common import *
from lib.s3 import *
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description='Azure Blob Sync Script')
    parser.add_argument('--patterns', nargs='*', help='List of filename patterns to match')
    return parser.parse_args()
 
def main():
    # Parse command line arguments
    args = parse_args()

    # Load environment variables
    load_dotenv()

    # Determine valid_patterns
    if args.patterns is not None:
        valid_patterns = args.patterns
    else:
        valid_patterns_env = os.getenv('VALID_PATTERNS')
        valid_patterns = valid_patterns_env.split(',') if valid_patterns_env else None

    # Assume the role
    aws_credentials = assume_role(os.getenv('ROLE_ARN_TO_ASSUME'), os.getenv('EXTERNAL_ID'), os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_KEY'))

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)

    # List objects in the S3 bucket
    s3_objects = s3_client.list_objects_v2(Bucket=os.getenv('S3_BUCKET'))['Contents']

    # Create the inventory file
    os.makedirs(os.path.dirname(os.getenv('INVENTORY_LIST_PATH')), exist_ok=True)
    with open(os.getenv('INVENTORY_LIST_PATH'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Filepath', 'File Size (Bytes)', 'Storage Class'])

        # For each file, write the details to the inventory file and download the file
        for obj in s3_objects:

            # Extract the details
            key = obj['Key']
            size = obj['Size']
            storage_class = obj.get('StorageClass', 'STANDARD')  # Default to 'STANDARD' if not os.getenv('specified')
            download_path = os.path.join(os.getenv('LOCAL_DOWNLOAD_PATH'), key)

            # Write the object details to the inventory file
            writer.writerow([os.path.basename(key), download_path, size, storage_class])

            # Download the object
            download_from_s3(s3_client, os.getenv('S3_BUCKET'), key, download_path, valid_patterns=valid_patterns)

if __name__ == "__main__":
    main()
