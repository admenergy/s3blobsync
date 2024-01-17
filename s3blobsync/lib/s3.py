import fnmatch
import os
import boto3
from tqdm import tqdm
import time
from .common import *

def assume_role(arn, external_id, access_key, secret_key):
    sts_client = boto3.client(
        'sts',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    assumed_role_object = sts_client.assume_role(
        RoleArn=arn,
        RoleSessionName="AssumeRoleSession1",
        ExternalId=external_id
    )
    return assumed_role_object['Credentials']

# AWS S3 Client
def get_s3_client(aws_credentials):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_credentials['AccessKeyId'],
        aws_secret_access_key=aws_credentials['SecretAccessKey'],
        aws_session_token=aws_credentials['SessionToken'],
    )
    return s3_client

# Download from S3
def download_from_s3(s3_client, bucket_name, key, download_path, valid_patterns=None):
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=key)
        file_size = response['ContentLength']
        storage_class = response.get('StorageClass', 'STANDARD')

        # Check if the blob has been processed already
        if (os.path.basename(key), file_size) in read_processed_files_list(os.getenv('PROCESSED_FILES_LIST_PATH')):
            print(f"Skipping {key}, already processed")
            return

        # If valid patterns is defined, check if the blob matches any of the patterns
        if valid_patterns and not any(fnmatch.fnmatch(os.path.basename(key), pattern) for pattern in valid_patterns):
            print(f"Skipping {key}, not matching filename patterns")
            return
    
        # Check if the file already exists locally
        if os.path.exists(download_path):
            local_file_size = os.path.getsize(download_path)
            if local_file_size == file_size:
                print(f"Skipping {key}, already exists with the same size.")
                return

        # Check for S3 Glacier or restricted access
        if storage_class == 'GLACIER' or storage_class == 'DEEP_ARCHIVE':
            print(f"Skipping {key}, file is in Glacier storage.")
            return
        
        # Ensure the directory structure exists before downloading
        directory = os.path.dirname(download_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        start_time = time.time()
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=os.path.basename(download_path), leave=False) as progress_bar:
            s3_client.download_file(bucket_name, key, download_path, Callback=lambda bytes_transferred: progress_bar.update(bytes_transferred))

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
        print(f"Downloaded {os.path.basename(download_path)} | {file_size/1024/1024:.0f} MB, {duration_str}, {rate_str}")

    except Exception as e:
        print(f"An error occurred when downloading {key}: {e}")