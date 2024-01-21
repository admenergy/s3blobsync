import argparse
import csv
import os
from pathlib import Path
from .lib.common import *
from .lib.blob import *
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description='Blob Sync Script')
    parser.add_argument('--patterns', nargs='*', help='List of filename patterns to match')
    parser.add_argument('--env_file', type=str, default='.env', help='Path to the .env file')
    return parser.parse_args()

def download_blob(patterns=None, env_file='.env'):
    # Load environment variables
    env_path = Path(env_file)
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path, override=True)
    else:
        print(f"Warning: '.env' file not found at {env_path}.")

    # Determine valid_patterns
    valid_patterns = patterns
    if valid_patterns is None:
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

def main():
    args = parse_args()
    download_blob(patterns=args.patterns, env_file=args.env_file)

if __name__ == "__main__":
    main()
