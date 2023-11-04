from lib.aws import *
from lib.azure import *
from config import *

def main():
    # Assume the role
    aws_credentials = assume_role(ROLE_ARN_TO_ASSUME, EXTERNAL_ID, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)

    # Setup Azure Blob Service Client
    # Replace with your Azure connection string
    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_CONNECTION_STRING)

    # Transfer from S3 to Azure storage
    # Replace with your Azure container name
    transfer_s3_to_azure(s3_client, blob_service_client,
                         S3_BUCKET, AZURE_CONTAINER_NAME)

if __name__ == "__main__":
    main()
