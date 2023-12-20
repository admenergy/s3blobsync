import csv
import os
from lib.common import *
from lib.blob import *
from os import path
import fnmatch
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment

def main():
    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_CONNECTION_STRING'))

    # Ensure local download directory and inventory list directory exist
    if not os.path.exists(os.getenv('LOCAL_DOWNLOAD_PATH')):
        os.makedirs(os.getenv('LOCAL_DOWNLOAD_PATH'))
    os.makedirs(os.path.dirname(os.getenv('AZURE_LIST_PATH')), exist_ok=True)

    # Read the list of already processed files
    processed_files = read_processed_files_list(os.getenv('PROCESSED_FILES_LIST_PATH'))

    # List and download blobs
    container_client = blob_service_client.get_container_client(os.getenv('AZURE_CONTAINER_NAME'))
    blob_list = [blob.name for blob in container_client.list_blobs()]

    # Create the inventory file
    with open(os.getenv('AZURE_LIST_PATH'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Filepath', 'File Size (Bytes)', 'Storage Class'])

        for blob_name in blob_list:
            blob_client = container_client.get_blob_client(blob_name)
            blob_properties = blob_client.get_blob_properties()

            # Check if blob is directory-like, continue if it is
            is_directory_placeholder = any(b.startswith(blob_name + '/') for b in blob_list if b != blob_name)
            if blob_name.endswith('/') or is_directory_placeholder:
                continue

            # Extract details
            size = blob_properties.size
            download_path = os.path.join(os.getenv('LOCAL_DOWNLOAD_PATH'), blob_name)
            storage_class = blob_properties.blob_tier

            # Write the blob details to the inventory file
            writer.writerow([os.path.basename(blob_name), download_path, size, storage_class])

    # Define the filename patterns
    valid_patterns = ["*interval*.gz", "*cust*.gz", "*ADM_meter*.gz", "*usage_meter*.gz"]

    # Process each blob
    for blob_name in sorted(blob_list):
        blob_client = container_client.get_blob_client(blob_name)
        blob_properties = blob_client.get_blob_properties()
        blob_size = blob_properties.size

        download_path = os.path.join(os.getenv('LOCAL_DOWNLOAD_PATH'), blob_name)

        # Check if the blob has been processed already
        if (blob_name, blob_size) in processed_files:
            print(f"Skipping already processed file: {blob_name}")
            continue

        # Check if the blob name matches any of the valid patterns
        if not any(fnmatch.fnmatch(blob_name, pattern) for pattern in valid_patterns):
            print(f"Skipping {blob_name}, not matching filename patterns")
            continue

        # Check if this blob is a directory placeholder
        is_directory_placeholder = any(b.startswith(blob_name + '/') for b in blob_list if b != blob_name)

        # Check if the blob is directory-like
        if blob_name.endswith('/') or is_directory_placeholder:
            # Create the directory if it does not exist
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            continue

        # Ensure the directory structure exists before downloading
        directory = os.path.dirname(download_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        download_from_azure(blob_service_client, os.getenv('AZURE_CONTAINER_NAME'), blob_name, download_path)

if __name__ == "__main__":
    main()
