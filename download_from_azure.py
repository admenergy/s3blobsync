from lib.azure import *
from config import *
from os import path

def main():
    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

    # Ensure local download directory exists
    if not os.path.exists(LOCAL_DOWNLOAD_PATH):
        os.makedirs(LOCAL_DOWNLOAD_PATH)

    # List and download blobs
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    blob_list = [blob.name for blob in container_client.list_blobs()]

    # Process each blob
    for blob_name in sorted(blob_list):
        download_path = os.path.join(LOCAL_DOWNLOAD_PATH, blob_name)
        
        # Check if this blob is a directory placeholder by checking if there's any blob that starts with its name followed by a '/'
        is_directory_placeholder = any(b.startswith(blob_name + '/') for b in blob_list if b != blob_name)
        
        if blob_name.endswith('/') or is_directory_placeholder:
            print(f"Processing directory-like blob: {blob_name}")
            print(f"Local directory to be created: {download_path}")
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            continue
        
        print(f"Processing file blob: {blob_name}")
        print(f"Local file path for download: {download_path}")
        
        # Ensure the directory structure exists before downloading
        directory = os.path.dirname(download_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        download_from_azure(blob_service_client, AZURE_CONTAINER_NAME, blob_name, download_path)

if __name__ == "__main__":
    main()
