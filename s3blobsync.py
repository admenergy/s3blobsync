from lib.s3 import *
from lib.blob import *
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment

def main():
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
    main()
