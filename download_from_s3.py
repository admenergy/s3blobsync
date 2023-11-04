import os
from lib.aws import *
from config import *

def main():
    # Assume the role
    aws_credentials = assume_role(ROLE_ARN_TO_ASSUME, EXTERNAL_ID, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)

    # List objects in the S3 bucket
    s3_objects = s3_client.list_objects_v2(Bucket=S3_BUCKET)['Contents']

    # Download each object
    for obj in s3_objects:
        key = obj['Key']
        download_path = os.path.join(LOCAL_DOWNLOAD_PATH, key)
        
        # Ensure the directory structure exists before downloading
        directory = os.path.dirname(download_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        download_from_s3(s3_client, S3_BUCKET, key, download_path)

if __name__ == "__main__":
    main()