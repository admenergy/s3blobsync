import boto3
from tqdm import tqdm

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
def download_from_s3(s3_client, bucket_name, key, file_name):
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=key)
        file_size = response['ContentLength']

        with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name) as progress_bar:
            s3_client.download_file(bucket_name, key, file_name, Callback=lambda bytes_transferred: progress_bar.update(bytes_transferred))
        print(f"Downloaded {key} from S3 to {file_name}")
    except Exception as e:
        print(f"An error occurred when downloading {key}: {e}")