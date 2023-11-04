import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from azure.core.exceptions import ResourceExistsError
import base64
import hashlib

# Azure Upload to Blob Storage
def upload_to_azure(blob_service_client, container_name, blob_name, data_stream, overwrite=False):
    try: 
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data_stream)
        print(f"Uploaded {blob_name} to Azure Blob storage")
    except Exception as e:
        # If it exists already print that exception out cleanly in a single line, otherwise, paste the whole error
        if isinstance(e, ResourceExistsError):
            print(f"Blob {blob_name} already exists in container {container_name}")
        else:
            print(f"An error occurred: {e}")
        

# Azure Download from Blob Storage
def download_from_azure(blob_service_client, container_name, blob_name, file_name):
    try:
        container_client = blob_service_client.get_container_client(
            container_name)
        blob_client = container_client.get_blob_client(blob_name)
        with open(file_name, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f"Downloaded {blob_name} from Azure to {file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Azure Transfer from S3 to Blob Storage
def transfer_s3_to_azure(s3_client, blob_service_client, bucket_name, container_name):
    try:
        result = s3_client.list_objects_v2(Bucket=bucket_name)
        if result.get('Contents'):
            for item in result['Contents']:
                print(item['Key'])

                # Get object from S3 as a streaming response
                s3_object = s3_client.get_object(
                    Bucket=bucket_name, Key=item['Key'])
                data_stream = s3_object['Body']

                # Transfer the data to Azure Blob Storage
                # If the file exists, a 
                upload_to_azure(blob_service_client,
                                container_name, item['Key'], data_stream)
        else:
            print(f"No objects in bucket {bucket_name}")
    except Exception as e:
        print(f"An error occurred: {e}")
