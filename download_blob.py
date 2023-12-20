import argparse
import csv
import os
from lib.common import *
from lib.blob import *
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description='Blob Sync Script')
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

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_CONNECTION_STRING'))

    # List and download blobs
    container_client = blob_service_client.get_container_client(os.getenv('AZURE_CONTAINER_NAME'))
    blob_list = [blob.name for blob in container_client.list_blobs()]

    # Create the inventory file
    os.makedirs(os.path.dirname(os.getenv('AZURE_LIST_PATH')), exist_ok=True)
    with open(os.getenv('AZURE_LIST_PATH'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Filepath', 'File Size (Bytes)', 'Storage Class'])

        # For each file, write the details to the inventory file and download the file
        for blob_name in blob_list:

            # Check if blob is directory-like, continue if it is
            is_directory_placeholder = any(b.startswith(blob_name + '/') for b in blob_list if b != blob_name)
            if blob_name.endswith('/') or is_directory_placeholder:
                continue
            
            # Extract details
            blob_client = container_client.get_blob_client(blob_name)
            blob_properties = blob_client.get_blob_properties()
            size = blob_properties.size
            download_path = os.path.join(os.getenv('LOCAL_DOWNLOAD_PATH'), blob_name)
            storage_class = blob_properties.blob_tier

            # Write the object details to the inventory file
            writer.writerow([os.path.basename(blob_name), download_path, size, storage_class])

            # Download the object
            download_from_azure(blob_service_client, os.getenv('AZURE_CONTAINER_NAME'), blob_name, download_path, valid_patterns=valid_patterns)

if __name__ == "__main__":
    main()
