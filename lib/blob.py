import fnmatch
import os
import time
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobBlock
import base64
import uuid
from tqdm import tqdm
from lib.common import *

# Azure Upload to Blob Storage
def upload_to_azure(blob_service_client, container_name, blob_name, data, block_id):
    try:
        container_client = blob_service_client.get_container_client(
            container_name)
        blob_client = container_client.get_blob_client(blob_name)

        # Upload the data as a block
        blob_client.stage_block(block_id, data)
        # print(f"Uploaded block {block_id} to Azure Blob storage: {blob_name}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")

# Azure Download from Blob Storage
def download_from_azure(blob_service_client, container_name, blob_name, download_path, valid_patterns=None):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_properties = blob_client.get_blob_properties()
        blob_size = blob_properties.size

        # Check if the blob has been processed already
        if (os.path.basename(blob_name), blob_size) in read_processed_files_list(os.getenv('PROCESSED_FILES_LIST_PATH')):
            print(f"Skipping {blob_name}, already processed")
            return

        # If valid patterns is defined, check if the blob matches any of the patterns
        if valid_patterns and not any(fnmatch.fnmatch(blob_name, pattern) for pattern in valid_patterns):
            print(f"Skipping {blob_name}, not matching filename patterns")
            return

        # Check if the local file exists and has the same size
        if os.path.exists(download_path):
            local_file_size = os.path.getsize(download_path)
            if local_file_size == blob_size:
                print(f"Skipping {blob_name}, already exists with the same size.")
                return

        # Check if the blob is directory-like.
        if blob_name.endswith('/'):
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            return
        
        # Ensure the directory structure exists before downloading
        directory = os.path.dirname(download_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        start_time = time.time()
        with open(download_path, "wb") as download_file, tqdm(total=blob_size, unit='B', unit_scale=True, desc=os.path.basename(download_path), leave=False) as progress_bar:
            # Download the blob in chunks
            stream = blob_client.download_blob()
            chunk_size = 1024 * 1024 * 10  # 10 MB chunks
            read_size = 0  # Track the amount of data read

            while read_size < blob_size:
                data = stream.read(chunk_size)
                download_file.write(data)
                read_size += len(data)
                progress_bar.update(len(data))
                
        # Retrieve information from tqdm
        elapsed_time = time.time() - start_time
        rate = progress_bar.format_dict['rate']

        # Calculate rate in MB/s
        rate = blob_size / elapsed_time / 1024 / 1024
        rate_str = f"{rate:.2f} MB/s"

        # Format elapsed time as minutes:seconds
        mins, secs = divmod(int(elapsed_time), 60)
        duration_str = f"{mins}:{secs:02d}"

        # Print the completion message with just the file name
        print(f"Downloaded {os.path.basename(download_path)} | {blob_size/1024/1024:.0f} MB, {duration_str}, {rate_str}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Azure Transfer from S3 to Blob Storage
def transfer_s3_to_azure(s3_client, blob_service_client, bucket_name, container_name, chunk_size=10*1024*1024):  # 10 MB chunk size
    try:
        result = s3_client.list_objects_v2(Bucket=bucket_name)
        if result.get('Contents'):
            for item in result['Contents']:
                try:
                    # Check if the file already exists on Azure
                    container_client = blob_service_client.get_container_client(
                        container_name)
                    blob_client = container_client.get_blob_client(item['Key'])

                    if blob_client.exists():
                        properties = blob_client.get_blob_properties()
                        s3_object = s3_client.head_object(
                            Bucket=bucket_name, Key=item['Key'])
                        if properties.size == s3_object['ContentLength']:
                            print(
                                f"Skipping {item['Key']}, already exists on Azure with the same size.")
                            continue

                    # Get object from S3 as a streaming response
                    s3_object = s3_client.get_object(
                        Bucket=bucket_name, Key=item['Key'])
                    data_stream = s3_object['Body']
                    file_size = s3_object['ContentLength']


                    start_time = time.time()
                    # Create a progress bar and upload in chunks
                    with tqdm(total=file_size, unit='B', unit_scale=True, desc=item['Key'], leave=False) as progress_bar:
                        block_list = []
                        for i in range(0, file_size, chunk_size):
                            block_id = base64.b64encode(
                                uuid.uuid4().bytes).decode('utf-8')
                            chunk = data_stream.read(chunk_size)
                            progress_bar.update(len(chunk))

                            upload_to_azure(
                                blob_service_client, container_name, item['Key'], chunk, block_id)
                            block_list.append(BlobBlock(block_id))

                        # Commit the block list to finalize the blob
                        if block_list:
                            blob_client.commit_block_list(block_list)

                    # Retrieve information from tqdm
                    elapsed_time = time.time() - start_time
                    rate = progress_bar.format_dict['rate']

                    # Calculate rate in MB/s
                    rate = file_size / elapsed_time / 1024 / 1024
                    rate_str = f"{rate:.2f} MB/s"

                    # Format elapsed time as minutes:seconds
                    mins, secs = divmod(int(elapsed_time), 60)
                    duration_str = f"{mins}:{secs:02d}"

                    # Print the completion message with just the file name
                    print(f"Uploaded {item['Key']} to Azure Blob Storage | {file_size/1024/1024:.0f} MB, {duration_str}, {rate_str}")

                except Exception as e:
                    print(f"Failed to transfer {item['Key']}: {e}")

        else:
            print(f"No objects in bucket {bucket_name}")
    except Exception as e:
        print(f"An error occurred while listing objects in the bucket: {e}")
