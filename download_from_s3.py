from lib.aws import assume_role, get_s3_client
from config import *


def main():
    # Assume the role
    aws_credentials = assume_role(ROLE_ARN_TO_ASSUME, EXTERNAL_ID, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    # Get the S3 client
    s3_client = get_s3_client(aws_credentials)




if __name__ == "__main__":
    main()
