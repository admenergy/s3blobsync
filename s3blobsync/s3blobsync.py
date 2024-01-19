import argparse
from pathlib import Path
from .lib.s3 import *
from .lib.blob import *
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description='Blob Sync Script')
    parser.add_argument('--env-file', type=str, default='.env', help='Path to the .env file')
    return parser.parse_args()

def s3blobsync():
    # Parse command line arguments
    args = parse_args()
    
    # Load environment variables
    # Check if the .env file exists at the specified path
    env_path = Path(args.env_file)
    if env_path.is_file():
        # Load environment variables from the specified .env file
        load_dotenv(dotenv_path=env_path)
    else:
        print(f"Warning: '.env' file not found at {env_path}.")

    # Assume the role
    aws_credentials = assume_role(os.getenv('ROLE_ARN_TO_ASSUME'), os.getenv('EXTERNAL_ID'), os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_KEY'))

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)

    # Setup Azure Blob Service Client
    # Replace with your Azure connection string
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv('AZURE_CONNECTION_STRING'))

    # Transfer from S3 to Azure storage
    # Replace with your Azure container name
    transfer_s3_to_azure(s3_client, blob_service_client,
                         os.getenv('S3_BUCKET'), os.getenv('AZURE_CONTAINER_NAME'))

if __name__ == "__main__":
    s3blobsync()
